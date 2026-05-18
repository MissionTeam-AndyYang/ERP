param(
  [string]$DocxPath = "docs/database/食品管理系統Database Schema_0.0.25.docx",
  [string]$SqlPath = "docs/database/ewdb20260515.sql",
  [string]$OutSqlPath = "docs/database/EWDB_WORD_CONVERTED_SCHEMA_20260515.sql",
  [string]$OutFkPath = "docs/database/EWDB_WORD_INFERRED_FK_CANDIDATES_20260515.md",
  [string]$OutDiffPath = "docs/database/EWDB_WORD_SQL_REVISION_REPORT_20260515.md"
)

$ErrorActionPreference = "Stop"

function Get-CellText($cell, $ns) {
  return (($cell.SelectNodes('.//w:t', $ns) | ForEach-Object { $_.'#text' }) -join '').Trim()
}

function Get-ColumnType($desc) {
  $text = ($desc -replace '；', ';').Trim()
  $segments = @($text -split ';' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
  $typeText = ($segments -join ' ')

  if ($typeText -match '(?i)AUTO_INCREMENT') { return 'BIGINT UNSIGNED NOT NULL AUTO_INCREMENT' }
  if ($typeText -match '(?i)longtext') { return 'LONGTEXT NULL' }
  if ($typeText -match '(?i)mediumtext') { return 'MEDIUMTEXT NULL' }
  if ($typeText -match '(?i)(^|[^A-Za-z])text([^A-Za-z]|$)') { return 'TEXT NULL' }
  if ($typeText -match '(?i)\bvarchar\s*\(\s*(\d+)\s*\)') { return "VARCHAR($($Matches[1])) NULL" }
  if ($typeText -match '(?i)\bchar\s*\(\s*(\d+)\s*\)') { return "CHAR($($Matches[1])) NULL" }
  if ($typeText -match '(?i)datetime') { return 'DATETIME NULL' }
  if ($typeText -match '(?i)timestamp') { return 'TIMESTAMP NULL' }
  if ($typeText -match '(?i)(^|[^A-Za-z])date([^A-Za-z]|$)') { return 'DATE NULL' }
  if ($typeText -match '(?i)double') { return 'DOUBLE NULL' }
  if ($typeText -match '(?i)float') { return 'FLOAT NULL' }
  if ($typeText -match '(?i)\bdecimal\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)') { return "DECIMAL($($Matches[1]),$($Matches[2])) NULL" }
  if ($typeText -match '(?i)(bigint|tinyint|smallint|mediumint|int)') { return ($Matches[1].ToUpper() + ' NULL') }
  if ($typeText -match '數值如下') { return 'INT NULL' }
  if ($typeText -match '日期|時間') { return 'INT NULL' }
  if ($typeText -match '文字|備註|comment|名稱|地址|編號|帳號|密碼|token') { return 'VARCHAR(255) NULL' }
  return 'VARCHAR(255) NULL'
}

function Normalize-ColumnName($name) {
  return (($name -replace [char]0x00A0, ' ') -replace '\s+', '').Trim()
}

function Normalize-TableName($text) {
  if ($text -match '^\s*([A-Za-z0-9_]+)\s*\(') { return $Matches[1] }
  return $null
}

function Get-DocTables($path) {
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $zip = [System.IO.Compression.ZipFile]::OpenRead((Resolve-Path $path))
  try {
    $entry = $zip.GetEntry('word/document.xml')
    $reader = New-Object System.IO.StreamReader($entry.Open())
    $xmlText = $reader.ReadToEnd()
    $reader.Close()
  } finally {
    $zip.Dispose()
  }

  [xml]$xml = $xmlText
  $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
  $ns.AddNamespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
  $body = $xml.SelectSingleNode('//w:body', $ns)
  $recent = New-Object System.Collections.Generic.List[string]
  $tables = [ordered]@{}

  foreach ($node in $body.ChildNodes) {
    if ($node.LocalName -eq 'p') {
      $txt = (($node.SelectNodes('.//w:t', $ns) | ForEach-Object { $_.'#text' }) -join '').Trim()
      if ($txt) {
        $recent.Add($txt)
        if ($recent.Count -gt 8) { $recent.RemoveAt(0) }
      }
    } elseif ($node.LocalName -eq 'tbl') {
      $ctx = ($recent | Select-Object -Last 1)
      $tableName = Normalize-TableName $ctx
      if (-not $tableName) { continue }

      $columns = New-Object System.Collections.Generic.List[object]
      $rows = $node.SelectNodes('.//w:tr', $ns)
      foreach ($row in $rows) {
        $cells = $row.SelectNodes('./w:tc', $ns)
        if ($cells.Count -lt 1) { continue }
        $name = Normalize-ColumnName (Get-CellText $cells[0] $ns)
        if (-not $name -or $name -match 'Product:|Version:|Document Revision') { continue }
        $desc = ''
        if ($cells.Count -gt 1) { $desc = Get-CellText $cells[1] $ns }
        $columns.Add([pscustomobject]@{
          Name = $name
          Description = $desc
          Type = Get-ColumnType $desc
          IsPk = ($desc -match '<PK>')
          IsUnique = ($desc -match 'UNIQUE KEY')
        })
      }

      $tables[$tableName] = [pscustomobject]@{
        Name = $tableName
        Title = $ctx
        Columns = $columns
      }
    }
  }

  return $tables
}

function Get-SqlTables($path) {
  $sql = Get-Content -Raw -Encoding UTF8 $path
  $tables = @{}
  $matches = [regex]::Matches($sql, '(?s)CREATE TABLE IF NOT EXISTS `([^`]+)` \((.*?)\) ENGINE=')
  foreach ($m in $matches) {
    $name = $m.Groups[1].Value
    $body = $m.Groups[2].Value
    $cols = [ordered]@{}
    foreach ($line in ($body -split "`n")) {
      $t = $line.Trim().TrimEnd(',')
      if ($t -match '^`([^`]+)`\s+(.+)$') {
        $cols[$Matches[1]] = $Matches[2]
      }
    }
    $tables[$name] = $cols
  }
  return $tables
}

function Get-FkTargets($desc) {
  $targets = New-Object System.Collections.Generic.List[string]
  $patterns = @(
    '關[連聯]至([^；，,。]+?)資料表',
    '對應至([^；，,。]+?)資料表'
  )
  foreach ($pattern in $patterns) {
    foreach ($m in [regex]::Matches($desc, $pattern)) {
      $raw = $m.Groups[1].Value.Trim()
      $raw = $raw -replace '\s+', ''
      foreach ($part in ($raw -split '/')) {
        $clean = $part.Trim()
        if ($clean -and $clean -match '^[A-Za-z0-9_]+$') { $targets.Add($clean) }
      }
    }
  }
  return @($targets | Select-Object -Unique)
}

$docTables = Get-DocTables $DocxPath
$sqlTables = Get-SqlTables $SqlPath
$docTableNames = @($docTables.Keys)
$sqlTableNames = @($sqlTables.Keys)
$bt = [char]96

$fkRows = New-Object System.Collections.Generic.List[object]
$highConfidenceConstraints = New-Object System.Collections.Generic.List[string]

$sqlOut = New-Object System.Collections.Generic.List[string]
$sqlOut.Add('-- Converted from Word schema: 食品管理系統Database Schema_0.0.25.docx')
$sqlOut.Add('-- Generated on 2026-05-15')
$sqlOut.Add('-- Notes:')
$sqlOut.Add('-- 1. Single-target inferred relationships are emitted as FOREIGN KEY constraints.')
$sqlOut.Add('-- 2. Multi-target relationships are emitted as comments because MySQL cannot enforce polymorphic FK directly.')
$sqlOut.Add('-- 3. Review this file before applying it to a database.')
$sqlOut.Add('')
$sqlOut.Add('SET NAMES utf8mb4;')
$sqlOut.Add('SET FOREIGN_KEY_CHECKS = 0;')
$sqlOut.Add('')

foreach ($tableName in $docTableNames) {
  $table = $docTables[$tableName]
  $sqlOut.Add("CREATE TABLE IF NOT EXISTS $bt$tableName$bt (")
  $lines = New-Object System.Collections.Generic.List[string]
  $pkCols = @()
  $uniqueCols = @()

  foreach ($col in $table.Columns) {
    $safeName = $col.Name -replace '`', ''
    $lines.Add("  $bt$safeName$bt $($col.Type)")
    if ($col.IsPk) { $pkCols += $safeName }
    if ($col.IsUnique -and -not $col.IsPk) { $uniqueCols += $safeName }

    $targets = @(Get-FkTargets $col.Description)
    if ($targets.Count -gt 0) {
      $refField = if ($safeName -match '_id$|^id$') { 'id' } else { 'no' }
      $isKeyLike = ($safeName -match '(^id$|^no$|_id$|_no$|Id$|No$)') -and ($safeName -notmatch 'name|displayName|Name')
      $targetExists = $targets.Count -eq 1 -and $docTables.Contains($targets[0])
      $targetHasField = $false
      if ($targetExists) {
        $targetHasField = @($docTables[$targets[0]].Columns | Where-Object { $_.Name -eq $refField }).Count -gt 0
      }
      $confidence = if ($isKeyLike -and $targetExists -and $targetHasField) { 'high' } elseif (-not $isKeyLike) { 'denormalized_or_label' } else { 'needs_review' }
      $fkRows.Add([pscustomobject]@{
        FromTable = $tableName
        FromField = $safeName
        ToTables = ($targets -join ' / ')
        ToField = $refField
        Confidence = $confidence
        SourceText = $col.Description
      })
      if ($confidence -eq 'high') {
        $constraintName = "fk_${tableName}_${safeName}" -replace '[^A-Za-z0-9_]', '_'
        $target = $targets[0]
        $highConfidenceConstraints.Add("ALTER TABLE $bt$tableName$bt ADD CONSTRAINT $bt$constraintName$bt FOREIGN KEY ($bt$safeName$bt) REFERENCES $bt$target$bt ($bt$refField$bt);")
      } else {
        $lines.Add("  -- FK candidate: $bt$safeName$bt -> $($targets -join ' / ')($bt$refField$bt), $confidence")
      }
    }
  }

  if ($pkCols.Count -gt 0) {
    $lines.Add("  PRIMARY KEY ($((@($pkCols) | ForEach-Object { $bt + $_ + $bt }) -join ', '))")
  }
  foreach ($colName in $uniqueCols) {
    $key = "uq_${tableName}_${colName}" -replace '[^A-Za-z0-9_]', '_'
    $lines.Add("  UNIQUE KEY $bt$key$bt ($bt$colName$bt)")
  }
  for ($i = 0; $i -lt $lines.Count; $i++) {
    $suffix = if ($i -lt $lines.Count - 1) { ',' } else { '' }
    $sqlOut.Add($lines[$i] + $suffix)
  }
  $sqlOut.Add(') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;')
  $sqlOut.Add('')
}

$sqlOut.Add('-- High-confidence inferred FK constraints')
$sqlOut.Add('-- Apply after reviewing existing data quality and target uniqueness.')
foreach ($constraint in $highConfidenceConstraints) { $sqlOut.Add($constraint) }
$sqlOut.Add('')

$sqlOut.Add('SET FOREIGN_KEY_CHECKS = 1;')
Set-Content -LiteralPath $OutSqlPath -Value $sqlOut -Encoding UTF8

$fkMd = New-Object System.Collections.Generic.List[string]
$fkMd.Add('# EWDB Word Inferred FK Candidates')
$fkMd.Add('')
$fkMd.Add('日期：2026-05-15')
$fkMd.Add('')
$fkMd.Add('本文件從 Word 欄位描述中的「關連至 / 關聯至 / 對應至 XXX 資料表」推論 FK。')
$fkMd.Add('')
$fkMd.Add('| From table | From field | To table(s) | To field | Confidence | Source |')
$fkMd.Add('|---|---|---|---|---|---|')
foreach ($row in ($fkRows | Sort-Object FromTable, FromField)) {
  $src = ($row.SourceText -replace '\|', '/' -replace "`r|`n", ' ')
  $fkMd.Add("| $bt$($row.FromTable)$bt | $bt$($row.FromField)$bt | $bt$($row.ToTables)$bt | $bt$($row.ToField)$bt | $($row.Confidence) | $src |")
}
Set-Content -LiteralPath $OutFkPath -Value $fkMd -Encoding UTF8

$diffMd = New-Object System.Collections.Generic.List[string]
$diffMd.Add('# EWDB Word Converted SQL vs ewdb20260515.sql Revision Report')
$diffMd.Add('')
$diffMd.Add('日期：2026-05-15')
$diffMd.Add('')
$diffMd.Add('## Summary')
$diffMd.Add('')
$diffMd.Add("- Word tables: $($docTableNames.Count)")
$diffMd.Add("- Existing SQL tables: $($sqlTableNames.Count)")
$diffMd.Add("- Inferred FK candidates: $($fkRows.Count)")
$diffMd.Add("- High-confidence single-target FK candidates: $(($fkRows | Where-Object { $_.Confidence -eq 'high' }).Count)")
$diffMd.Add("- Needs-review polymorphic or ambiguous FK candidates: $(($fkRows | Where-Object { $_.Confidence -ne 'high' }).Count)")
$diffMd.Add('')

$missingInSql = @($docTableNames | Where-Object { -not $sqlTables.ContainsKey($_) })
$missingInDoc = @($sqlTableNames | Where-Object { -not $docTables.Contains($_) })
$diffMd.Add('## Table Difference')
$diffMd.Add('')
$diffMd.Add("- Word only tables: " + ($(if ($missingInSql.Count) { $missingInSql -join ', ' } else { 'None' })))
$diffMd.Add("- Existing SQL only tables: " + ($(if ($missingInDoc.Count) { $missingInDoc -join ', ' } else { 'None' })))
$diffMd.Add('')

$diffMd.Add('## Field Difference')
$diffMd.Add('')
$diffMd.Add('| Table | Word only fields | Existing SQL only fields | Suggested action |')
$diffMd.Add('|---|---|---|---|')
foreach ($tableName in ($docTableNames | Sort-Object)) {
  if (-not $sqlTables.ContainsKey($tableName)) { continue }
  $wordFields = @($docTables[$tableName].Columns | ForEach-Object { $_.Name })
  $sqlFields = @($sqlTables[$tableName].Keys)
  $wordOnly = @($wordFields | Where-Object { $_ -notin $sqlFields })
  $sqlOnly = @($sqlFields | Where-Object { $_ -notin $wordFields })
  if ($wordOnly.Count -or $sqlOnly.Count) {
    $action = 'Review and align Word/SQL before generating ORM models.'
    $diffMd.Add("| $bt$tableName$bt | $($wordOnly -join ', ') | $($sqlOnly -join ', ') | $action |")
  }
}
$diffMd.Add('')

$diffMd.Add('## Existing SQL Revision Priorities')
$diffMd.Add('')
$diffMd.Add('### P0: Do not apply all FK constraints automatically')
$diffMd.Add('')
$diffMd.Add('Word descriptions contain useful relationship text, but some fields are polymorphic, such as references to `material / inproduct / product`. These cannot be represented by one normal MySQL FK.')
$diffMd.Add('')
$diffMd.Add('### P1: Fix clear naming mismatches')
$diffMd.Add('')
$diffMd.Add('- `process_capacity.commnet` should become `comment`.')
$diffMd.Add('- `batchno_serialno.vaildDate` in Word should become `validDate` or the SQL should move to `valid_date` in the new model.')
$diffMd.Add('- `station.productionline_no` in Word should align with SQL `production_line_no`.')
$diffMd.Add('- `creator_no` vs `creator_id` should be decided before ORM relationship design.')
$diffMd.Add('')
$diffMd.Add('### P2: Add high-confidence FK constraints after data validation')
$diffMd.Add('')
$diffMd.Add('Use `EWDB_WORD_INFERRED_FK_CANDIDATES_20260515.md` as the review checklist. Apply only rows marked `high` after confirming referenced values exist and target columns are unique.')
$diffMd.Add('')
$diffMd.Add('### P3: Convert polymorphic references into explicit design')
$diffMd.Add('')
$diffMd.Add('Fields that point to multiple tables should become either:')
$diffMd.Add('')
$diffMd.Add('- `ref_type` + `ref_no` without physical FK, plus application validation; or')
$diffMd.Add('- separate nullable FK columns, one per target table; or')
$diffMd.Add('- a unified item master table, which is the cleaner ERP 2.0 direction.')
$diffMd.Add('')
$diffMd.Add('## Generated Files')
$diffMd.Add('')
$diffMd.Add('- Converted SQL: `' + $OutSqlPath + '`')
$diffMd.Add('- FK candidates: `' + $OutFkPath + '`')
$diffMd.Add('- Revision report: `' + $OutDiffPath + '`')

Set-Content -LiteralPath $OutDiffPath -Value $diffMd -Encoding UTF8

Write-Output "converted_sql=$OutSqlPath"
Write-Output "fk_candidates=$OutFkPath"
Write-Output "revision_report=$OutDiffPath"
Write-Output "tables=$($docTableNames.Count)"
Write-Output "fk_candidates_count=$($fkRows.Count)"
