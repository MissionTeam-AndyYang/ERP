param(
  [string]$InputPath = "docs/database/EWDB_20260517.sql",
  [string]$OutputPath = "docs/database/EWDB_20260517_UNIQUE_KEY_FIXED.sql",
  [string]$ReportPath = "docs/database/EWDB_20260517_UNIQUE_KEY_FIX_REPORT.md"
)

$ErrorActionPreference = "Stop"

function Normalize-KeyName($tableName) {
  return ("uq_${tableName}_composite" -replace '[^A-Za-z0-9_]', '_')
}

function Get-KeyColumns($uniqueLine) {
  $cols = New-Object System.Collections.Generic.List[string]
  if ($uniqueLine -match 'UNIQUE KEY\s+`[^`]+`\s+\((.+)\)') {
    $raw = $Matches[1]
    foreach ($part in ($raw -split ',')) {
      $col = $part.Trim()
      if ($col -match '`([^`]+)`') {
        $cols.Add($Matches[1])
      }
    }
  }
  return @($cols)
}

function Make-NotNull($line) {
  if ($line -match '^\s*`([^`]+)`\s+') {
    $line = $line -replace '\s+DEFAULT\s+NULL\b', ' DEFAULT NULL'
    $line = $line -replace '\s+NULL\b', ' NOT NULL'
  }
  return $line
}

function Recomma($lines) {
  $clean = New-Object System.Collections.Generic.List[string]
  foreach ($line in $lines) {
    if ($line.Trim().Length -eq 0) { continue }
    $clean.Add($line.TrimEnd().TrimEnd(','))
  }

  $out = New-Object System.Collections.Generic.List[string]
  for ($i = 0; $i -lt $clean.Count; $i++) {
    $suffix = if ($i -lt $clean.Count - 1) { "," } else { "" }
    $out.Add($clean[$i] + $suffix)
  }
  return @($out)
}

$sql = Get-Content -Raw -Encoding UTF8 $InputPath
$tablePattern = '(?s)CREATE TABLE IF NOT EXISTS `([^`]+)` \((.*?)\) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;'
$matches = [regex]::Matches($sql, $tablePattern)

$reportRows = New-Object System.Collections.Generic.List[object]
$rewritten = New-Object System.Text.StringBuilder
$lastIndex = 0

foreach ($match in $matches) {
  $tableName = $match.Groups[1].Value
  $body = $match.Groups[2].Value

  [void]$rewritten.Append($sql.Substring($lastIndex, $match.Index - $lastIndex))

  $lines = @($body -split "`r?`n" | Where-Object { $_.Trim().Length -gt 0 })
  $uniqueLines = @($lines | Where-Object { $_ -match '^\s*UNIQUE KEY\s+' })
  $uniqueCols = New-Object System.Collections.Generic.List[string]

  foreach ($uniqueLine in $uniqueLines) {
    foreach ($col in (Get-KeyColumns $uniqueLine)) {
      if (-not $uniqueCols.Contains($col)) {
        $uniqueCols.Add($col)
      }
    }
  }

  $newLines = New-Object System.Collections.Generic.List[string]
  $primaryKeyIndex = -1

  foreach ($line in $lines) {
    if ($line -match '^\s*UNIQUE KEY\s+') { continue }

    $newLine = $line
    if ($newLine -match '^\s*`([^`]+)`\s+') {
      $colName = $Matches[1]
      if ($uniqueCols.Contains($colName)) {
        $newLine = Make-NotNull $newLine
      }
    }

    $newLines.Add($newLine)
  }

  for ($i = 0; $i -lt $newLines.Count; $i++) {
    if ($newLines[$i] -match '^\s*PRIMARY KEY\s+') {
      $primaryKeyIndex = $i
      break
    }
  }

  $newUniqueKey = $null
  if ($uniqueCols.Count -gt 0) {
    $keyCols = (@($uniqueCols) | ForEach-Object { "``$_``" }) -join ", "
    $newUniqueKey = "  UNIQUE KEY ``$(Normalize-KeyName $tableName)`` ($keyCols)"

    if ($primaryKeyIndex -ge 0) {
      $newLines.Insert($primaryKeyIndex + 1, $newUniqueKey)
    } else {
      $newLines.Add($newUniqueKey)
    }
  }

  $finalLines = Recomma $newLines
  [void]$rewritten.Append("CREATE TABLE IF NOT EXISTS ``$tableName`` (`r`n")
  [void]$rewritten.Append(($finalLines -join "`r`n"))
  [void]$rewritten.Append("`r`n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")

  $reportRows.Add([pscustomobject]@{
    Table = $tableName
    OriginalUniqueKeyCount = $uniqueLines.Count
    NewUniqueKeyCount = $(if ($uniqueCols.Count -gt 0) { 1 } else { 0 })
    CompositeColumns = (@($uniqueCols) -join ", ")
  })

  $lastIndex = $match.Index + $match.Length
}

[void]$rewritten.Append($sql.Substring($lastIndex))
Set-Content -LiteralPath $OutputPath -Value $rewritten.ToString() -Encoding UTF8

$md = New-Object System.Collections.Generic.List[string]
$md.Add("# EWDB 20260517 UNIQUE KEY Fix Report")
$md.Add("")
$md.Add("日期：2026-05-17")
$md.Add("")
$md.Add("## Rule")
$md.Add("")
$md.Add("- 每個資料表最多保留一組 `UNIQUE KEY`。")
$md.Add("- 若原始資料表有多組 `UNIQUE KEY`，合併為一組多欄位 composite unique key。")
$md.Add("- 所有出現在 `UNIQUE KEY` 內的欄位均改為 `NOT NULL`。")
$md.Add("")
$md.Add("## Output")
$md.Add("")
$md.Add('- Input: `' + $InputPath + '`')
$md.Add('- Output: `' + $OutputPath + '`')
$md.Add("")
$md.Add("## Summary")
$md.Add("")
$md.Add("- Tables scanned: $($reportRows.Count)")
$md.Add("- Tables with unique key: $(($reportRows | Where-Object { $_.NewUniqueKeyCount -eq 1 }).Count)")
$md.Add("- Tables without unique key: $(($reportRows | Where-Object { $_.NewUniqueKeyCount -eq 0 }).Count)")
$md.Add("- Tables originally having multiple unique keys: $(($reportRows | Where-Object { $_.OriginalUniqueKeyCount -gt 1 }).Count)")
$md.Add("")
$md.Add("## Table Detail")
$md.Add("")
$md.Add("| Table | Original UNIQUE KEY count | New UNIQUE KEY count | Composite columns |")
$md.Add("|---|---:|---:|---|")
foreach ($row in ($reportRows | Sort-Object Table)) {
  $cols = if ($row.CompositeColumns) { $row.CompositeColumns } else { "" }
  $md.Add('| `' + $row.Table + '` | ' + $row.OriginalUniqueKeyCount + ' | ' + $row.NewUniqueKeyCount + ' | ' + $cols + ' |')
}

Set-Content -LiteralPath $ReportPath -Value $md -Encoding UTF8

Write-Output "output=$OutputPath"
Write-Output "report=$ReportPath"
Write-Output "tables=$($reportRows.Count)"
Write-Output "multi_unique_before=$(($reportRows | Where-Object { $_.OriginalUniqueKeyCount -gt 1 }).Count)"
