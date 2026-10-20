Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# FM01 owner-host viability gate only. CIO's effective bounded exception permits
# Owner-host CurrentUser-DPAPI use at a separately released execution stage;
# this gate itself never starts/stops a process, invokes a MariaDB client,
# reads credentials, or queries a database.
$targetId = 'ERP2-FM01-FUNCTIONAL-NP-001'
$database = 'erp2_fm01_functional_np_001'
$hostName = '127.0.0.1'
$port = 3342
$targetRoot = 'C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\FM01_Functional_NP_Target_Binding_20261007_001'
$datadir = Join-Path $targetRoot 'data'
$runtimeRoot = 'C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Database_Runtime\ERP2-DB-RUNTIME-NP-INSTALL-001\runtime\mariadb-11.4.10-winx64'
$server = Join-Path $runtimeRoot 'bin\mariadbd.exe'
$client = Join-Path $runtimeRoot 'bin\mariadb.exe'
$dump = Join-Path $runtimeRoot 'bin\mariadb-dump.exe'
$ini = Join-Path $targetRoot 'runtime\my-erp2-fm01-functional-np-11410.ini'
$requiredSourceCommit = '38efa0d5a45c6425cdb5139d27bdc682db5a49d1'
$requiredSourceHashes = [ordered]@{
  'fm01_org_location_0001.py' = '80CF5745CE9D8538B22EF1597CAD5CC84EB57AFD9371C30CA9F127547018AF0D'
  'fm01_org_location_0002_design_reconciliation.py' = 'B74A208D8EE1E55EEBCACE8F49011386F0FB1D18072F56CEDF879A73C45E342F'
  'fm01_org_location_0003_mutation_contract.py' = '9AD18755FB919EA5E6DD621A3DC6614891A11D6CFBD92C83190E033C183BFED0'
  'fm01_approval_audit_0004_local_persistence.py' = 'C3898F5500C554909E86D01EA370748131AC12A9433C36B141B619627C6DE94E'
}

function Hold([string]$Reason) {
  Write-Output "FM01_OWNER_HOST_3342=NOT_EXECUTABLE"
  Write-Output "EXACT_REASON=$Reason"
  exit 10
}

if ($port -ne 3342) { Hold 'fixed port binding is not 3342' }
if (-not (Test-Path -LiteralPath $server -PathType Leaf)) { Hold "server binary absent: $server" }
if (-not (Test-Path -LiteralPath $client -PathType Leaf)) { Hold "client binary absent: $client" }
if (-not (Test-Path -LiteralPath $dump -PathType Leaf)) { Hold "dump binary absent: $dump" }
if (-not (Test-Path -LiteralPath $ini -PathType Leaf)) { Hold "FM01 config absent: $ini" }
if (-not (Test-Path -LiteralPath $datadir -PathType Container)) { Hold "FM01 datadir absent: $datadir" }
if ((Get-Content -LiteralPath $ini -Raw -Encoding UTF8) -notmatch '(?m)^bind-address\s*=\s*127\.0\.0\.1\s*$') { Hold "FM01 config bind-address mismatch: $ini" }
if ((Get-Content -LiteralPath $ini -Raw -Encoding UTF8) -notmatch '(?m)^port\s*=\s*3342\s*$') { Hold "FM01 config port mismatch: $ini" }
$configDatadir = (Get-Content -LiteralPath $ini -Encoding UTF8 | Where-Object { $_ -match '^datadir\s*=' } | Select-Object -First 1) -replace '^datadir\s*=\s*', ''
if ([string]::IsNullOrWhiteSpace($configDatadir) -or [IO.Path]::GetFullPath($configDatadir.Replace('/', '\\').Trim()) -ne [IO.Path]::GetFullPath($datadir)) { Hold "FM01 config datadir mismatch: $ini" }

# No credential path is accepted here. FM02 DPAPI or account material is never
# read or reused; a separately approved FM01 provider must be bound later.
Hold 'no separately approved FM01 credential provider/manifest/executor is bound; runtime invocation is prohibited'
