[CmdletBinding()]
param(
    [ValidateSet('StaticSelfTest')]
    [string] $Mode = 'StaticSelfTest'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$TargetId = 'ERP2-FM01-FUNCTIONAL-NP-001'
$Database = 'erp2_fm01_functional_np_001'
$HostName = '127.0.0.1'
$Port = 3342
$TargetRoot = 'C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\FM01_Functional_NP_Target_Binding_20261007_001'
$ForbiddenPorts = @(3341, 3344, 3345, 3306)
$SourceRoot = Join-Path (Split-Path -Parent $PSScriptRoot) 'source'

$Expected = [ordered]@{
    'fm01_org_location_0001.py' = '80CF5745CE9D8538B22EF1597CAD5CC84EB57AFD9371C30CA9F127547018AF0D'
    'fm01_org_location_0002_design_reconciliation.py' = 'B74A208D8EE1E55EEBCACE8F49011386F0FB1D18072F56CEDF879A73C45E342F'
    'fm01_org_location_0003_mutation_contract.py' = '9AD18755FB919EA5E6DD621A3DC6614891A11D6CFBD92C83190E033C183BFED0'
    'fm01_approval_audit_0004_local_persistence.py' = 'C3898F5500C554909E86D01EA370748131AC12A9433C36B141B619627C6DE94E'
}

if ($Port -ne 3342 -or $TargetId -ne 'ERP2-FM01-FUNCTIONAL-NP-001' -or $Database -ne 'erp2_fm01_functional_np_001' -or $HostName -ne '127.0.0.1') {
    throw 'STATIC_TARGET_BINDING_FAILED'
}
if ($ForbiddenPorts -contains $Port) { throw 'FORBIDDEN_PORT_BINDING_FAILED' }
if (-not (Test-Path -LiteralPath $TargetRoot -PathType Container)) { throw 'TARGET_ROOT_NOT_FOUND' }

$results = foreach ($entry in $Expected.GetEnumerator()) {
    $path = Join-Path $SourceRoot $entry.Key
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "SOURCE_MISSING=$($entry.Key)" }
    $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    if ($hash -ne $entry.Value) { throw "SOURCE_HASH_MISMATCH=$($entry.Key)" }
    [pscustomobject]@{ file=$entry.Key; sha256=$hash; status='PASS' }
}

$scriptText = Get-Content -LiteralPath $PSCommandPath -Raw
if ($scriptText -match '(?m)^\s*&?\s*(Start-Process|Stop-Process|Invoke-Sql)\b') { throw 'STATIC_FORBIDDEN_EXECUTION_PRESENT=process-or-sql-call' }
if ($scriptText -match '(?i)\\(mariadb|mariadbd)\.exe') { throw 'STATIC_FORBIDDEN_EXECUTION_PRESENT=mariadb-binary' }
if ($scriptText -match '(?i)\balembic\s+(upgrade|downgrade)\b') { throw 'STATIC_FORBIDDEN_EXECUTION_PRESENT=alembic-operation' }

[pscustomobject]@{
    mode=$Mode
    target_id=$TargetId
    database=$Database
    endpoint="$HostName`:$Port"
    source_commit='38efa0d5a45c6425cdb5139d27bdc682db5a49d1'
    source_tree='6095d409859e89889c7fd02a285fbcc648d5196a'
    source_lineage='0001->0002->0003->0004'
    source_hashes=$results
    target_contacted=$false
    database_started_or_stopped=$false
    sql_or_alembic_executed=$false
    secrets_or_dpapi_accessed=$false
    target_mutated=$false
    fm02_touched=$false
    status='PASS_WITH_CONDITIONS'
} | ConvertTo-Json -Depth 5
