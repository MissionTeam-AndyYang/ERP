[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidateSet('TargetCheck','SafeStart','BackupRecoveryCheck','Migrations0001To0004','IdentityPreflight','DbTests','EvidenceExport','GracefulStop')]
    [string] $Stage,
    [switch] $ConfirmHumanExecution,
    [string] $ExecutionReleaseArtifact,
    [string] $BackupPath,
    [string] $EvidencePath,
    [string] $TestCommand
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$TargetId = 'ERP2-FM01-FUNCTIONAL-NP-001'
$Database = 'erp2_fm01_functional_np_001'
$HostName = '127.0.0.1'
$Port = 3342
$Root = Split-Path -Parent $PSScriptRoot
$WorkspaceRoot = 'C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace'
$TargetRoot = Join-Path $WorkspaceRoot 'FM01_Functional_NP_Target_Binding_20261007_001'
$RuntimeBin = Join-Path $WorkspaceRoot 'Database_Runtime\ERP2-DB-RUNTIME-NP-INSTALL-001\runtime\mariadb-11.4.10-winx64\bin'
$Server = Join-Path $RuntimeBin 'mariadbd.exe'
$Client = Join-Path $RuntimeBin 'mariadb.exe'
$Dump = Join-Path $RuntimeBin 'mariadb-dump.exe'
$Admin = Join-Path $RuntimeBin 'mariadb-admin.exe'
$Config = Join-Path $TargetRoot 'runtime\my-erp2-fm01-functional-np-11410.ini'
$DataDir = Join-Path $TargetRoot 'data'
$ExpectedConfigHash = 'D386B8D32CC2897D1C1DBEB0CC9DB62BDA365072F3434B6EDF5146506AE61A3D'
$SourceDir = Join-Path $Root 'source'
$ExpectedSourceHashes = [ordered]@{
    'fm01_org_location_0001.py' = '80CF5745CE9D8538B22EF1597CAD5CC84EB57AFD9371C30CA9F127547018AF0D'
    'fm01_org_location_0002_design_reconciliation.py' = 'B74A208D8EE1E55EEBCACE8F49011386F0FB1D18072F56CEDF879A73C45E342F'
    'fm01_org_location_0003_mutation_contract.py' = '9AD18755FB919EA5E6DD621A3DC6614891A11D6CFBD92C83190E033C183BFED0'
    'fm01_approval_audit_0004_local_persistence.py' = 'C3898F5500C554909E86D01EA370748131AC12A9433C36B141B619627C6DE94'
}
$MutationStages = @('SafeStart','BackupRecoveryCheck','Migrations0001To0004','IdentityPreflight','DbTests','EvidenceExport','GracefulStop')
$RuntimeSecretPath = Join-Path $TargetRoot 'secrets\fm01-runtime-route-c-20261007-001.secret.dpapi'
$DefaultRootSecretPath = Join-Path $TargetRoot 'secrets\np-functional-root-route-c-20261007-001.secret.dpapi'

function Hold([string] $Reason) {
    Write-Output "FM01_STAGE=$Stage"
    Write-Output 'RESULT=NOT_TO_EXECUTE'
    Write-Output "EXACT_REASON=$Reason"
    exit 10
}

function Assert-ExactBindings {
    if ($TargetId -ne 'ERP2-FM01-FUNCTIONAL-NP-001' -or $Database -ne 'erp2_fm01_functional_np_001' -or $HostName -ne '127.0.0.1' -or $Port -ne 3342) { Hold 'fixed target binding mismatch' }
    foreach ($p in @($Server,$Client,$Dump,$Admin,$Config,$DataDir)) {
        if (-not (Test-Path -LiteralPath $p)) { Hold "approved path absent: $p" }
    }
    $configHash = (Get-FileHash -LiteralPath $Config -Algorithm SHA256).Hash
    if ($configHash.ToUpperInvariant() -ne $ExpectedConfigHash.ToUpperInvariant()) { Hold "launch config hash mismatch: $Config" }
    $text = Get-Content -LiteralPath $Config -Raw -Encoding UTF8
    if ($text -notmatch '(?m)^bind-address\s*=\s*127\.0\.0\.1\s*$' -or $text -notmatch '(?m)^port\s*=\s*3342\s*$') { Hold 'launch config bind/port mismatch' }
    $configuredData = (Get-Content -LiteralPath $Config -Encoding UTF8 | Where-Object { $_ -match '^datadir\s*=' } | Select-Object -First 1) -replace '^datadir\s*=\s*',''
    if ([string]::IsNullOrWhiteSpace($configuredData) -or [IO.Path]::GetFullPath($configuredData.Replace('/','\').Trim()) -ne [IO.Path]::GetFullPath($DataDir)) { Hold 'launch config datadir mismatch' }
    $sourceChecks = @(
        @('fm01_org_location_0001.py','80CF5745CE9D8538B22EF1597CAD5CC84EB57AFD9371C30CA9F127547018AF0D'),
        @('fm01_org_location_0002_design_reconciliation.py','B74A208D8EE1E55EEBCACE8F49011386F0FB1D18072F56CEDF879A73C45E342F'),
        @('fm01_org_location_0003_mutation_contract.py','9AD18755FB919EA5E6DD621A3DC6614891A11D6CFBD92C83190E033C183BFED0'),
        @('fm01_approval_audit_0004_local_persistence.py','C3898F5500C554909E86D01EA370748131AC12A9433C36B141B619627C6DE94E')
    )
    foreach ($sourceCheck in $sourceChecks) {
        $sourceName = [string]$sourceCheck[0]
        $sourcePath = Join-Path $SourceDir $sourceName
        if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) { Hold "migration source absent: $sourcePath" }
        $actualSourceHash = [string](Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
        $expectedSourceHash = [string]$sourceCheck[1]
        if ($actualSourceHash.ToUpperInvariant() -ne $expectedSourceHash.ToUpperInvariant()) { Hold "migration source hash mismatch: $sourcePath" }
    }
}

function Assert-ExecutionRelease {
    if (-not $ConfirmHumanExecution) { Hold 'side-effecting stage requires explicit -ConfirmHumanExecution' }
    if ([string]::IsNullOrWhiteSpace($ExecutionReleaseArtifact)) { Hold 'a real execution-release artifact path is required; boolean release tokens are not accepted' }
    if (-not (Test-Path -LiteralPath $ExecutionReleaseArtifact -PathType Leaf)) { Hold "execution-release artifact not found: $ExecutionReleaseArtifact" }
    $release = Get-Content -LiteralPath $ExecutionReleaseArtifact -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($release.target_id -ne $TargetId -or $release.database -ne $Database -or $release.host -ne $HostName -or [int]$release.port -ne $Port) { Hold 'execution-release artifact target mismatch' }
    if (-not ($release.allowed_stages -is [array]) -or @($release.allowed_stages) -notcontains $Stage) { Hold 'execution-release stage allowlist does not contain requested stage' }
    if ([string]::IsNullOrWhiteSpace([string]$release.owner_identity)) { Hold 'execution-release owner identity missing' }
    $currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
    if ([string]$release.owner_identity -ne $currentIdentity) { Hold "execution-release owner identity does not match current Owner-host identity: $currentIdentity" }
    if ([string]::IsNullOrWhiteSpace([string]$release.nonce)) { Hold 'execution-release one-time nonce missing' }
    if ($release.expires_at -and ([datetime]$release.expires_at) -le (Get-Date).ToUniversalTime()) { Hold 'execution-release artifact expired' }
    $consumedRoot = Join-Path $TargetRoot 'evidence\release-consumption'
    New-Item -ItemType Directory -Path $consumedRoot -Force | Out-Null
    $noncePath = Join-Path $consumedRoot (($release.nonce -replace '[^A-Za-z0-9_.-]','_') + '.consumed')
    $stream = [IO.File]::Open($noncePath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { [Text.Encoding]::UTF8.GetBytes("stage=$Stage`nowner=$($release.owner_identity)`nconsumed_at=$((Get-Date).ToUniversalTime().ToString('o'))`n") | ForEach-Object { $stream.WriteByte($_) } }
    finally { $stream.Dispose() }
}

function Get-TargetProcess {
    try {
        @(
            Get-CimInstance Win32_Process -Filter "Name='mariadbd.exe'" -ErrorAction Stop |
                Where-Object { $_.CommandLine -and $_.CommandLine -like "*my-erp2-fm01-functional-np-11410.ini*" }
        )
    } catch { Hold 'process identity query unavailable; target check is indeterminate' }
}

function Assert-ProcessIdentity($Process, [string] $Context) {
    if ($null -eq $Process -or @($Process).Count -ne 1) { Hold "$Context requires exactly one identified FM01 process" }
    $item = @($Process)[0]
    if (-not $item.CommandLine -or $item.CommandLine -notlike "*--defaults-file=$Config*") { Hold "$Context process command line is not bound to the approved config" }
    if ($item.ExecutablePath -and [IO.Path]::GetFullPath($item.ExecutablePath) -ne [IO.Path]::GetFullPath($Server)) { Hold "$Context executable path mismatch" }
    return $item
}

function Assert-ListenerProcessMatch($Process, $Listener, [string] $Context) {
    $item = Assert-ProcessIdentity $Process $Context
    if ($null -eq $Listener -or @($Listener).Count -ne 1) { Hold "$Context requires exactly one listener" }
    if ([int]@($Listener)[0].OwningProcess -ne [int]$item.ProcessId) { Hold "$Context listener owning PID mismatch" }
    return $item
}

function Get-TargetListener {
    try { @(Get-NetTCPConnection -LocalAddress $HostName -LocalPort $Port -State Listen -ErrorAction Stop) }
    catch { Hold 'listener identity query unavailable; target check is indeterminate' }
}

function Read-DpapiSecret([string] $Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "approved target credential file not found: $Path" }
    $secure = (Get-Content -LiteralPath $Path -Raw).Trim() | ConvertTo-SecureString
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}

function Invoke-ChildWithRedactedFailure([string] $FilePath, [string[]] $ArgumentList, [hashtable] $Environment) {
    $previous = $env:FM01_RUNTIME_PASSWORD
    try {
        if ($Environment.ContainsKey('FM01_RUNTIME_PASSWORD')) { $env:FM01_RUNTIME_PASSWORD = $Environment['FM01_RUNTIME_PASSWORD'] }
        $output = @(& $FilePath @ArgumentList 2>&1)
        $code = $LASTEXITCODE
    } finally { $env:FM01_RUNTIME_PASSWORD = $previous }
    if ($code -ne 0) {
        $redacted = (($output | ForEach-Object { ([string]$_) -replace '(?i)(password|secret|token|credential|private[_-]?key)\s*[=:].*$', '$1=[REDACTED]' }) -join "`n")
        Hold ("child operation failed: " + $redacted)
    }
    return $output
}

function Invoke-ReadOnlySql([string] $Sql, [string] $Password) {
    if ($Sql -match '\b(INSERT|UPDATE|DELETE|ALTER|CREATE|DROP|TRUNCATE|GRANT|REVOKE|SHUTDOWN|SET\s+GLOBAL)\b') { Hold 'read-only SQL contract violated' }
    $previous = $env:MYSQL_PWD; $env:MYSQL_PWD = $Password
    try { $output = @($Sql | & $Client --protocol=tcp --host=$HostName --port=$Port --user='fm01_runtime' --database=$Database --batch --raw --skip-column-names --connect-timeout=5 2>&1); $code=$LASTEXITCODE }
    finally { $env:MYSQL_PWD = $previous }
    if ($code -ne 0) { Hold 'read-only DB test failed; no retry attempted' }
    return @($output | ForEach-Object { ([string]$_) -replace '(?i)(password|secret|token|private[_-]?key)\s*[=:].*$', '$1=[REDACTED]' })
}

Assert-ExactBindings
if ($Stage -eq 'TargetCheck') {
    $listener = @(Get-TargetListener); $process = @(Get-TargetProcess)
    if ($listener.Count -gt 0 -and $process.Count -ne 1) { Hold 'listener exists without exactly one positively identified FM01 process' }
    if ($listener.Count -eq 1 -and $process.Count -eq 1) { Assert-ListenerProcessMatch $process $listener 'target check' | Out-Null }
    Write-Output "FM01_STAGE=$Stage"; Write-Output 'RESULT=TARGET_CHECK_PASS'; Write-Output "TARGET_ID=$TargetId"; Write-Output "DATABASE=$Database"; Write-Output "ENDPOINT=$HostName`:$Port"; Write-Output "CONFIG_SHA256=$ExpectedConfigHash"; Write-Output 'SOURCE_LINEAGE=0001->0002->0003->0004'; Write-Output "LISTENING=$($listener.Count -gt 0)"; Write-Output 'SECRET_VALUES_EXPOSED=false'; Write-Output 'LIVE_OPERATION_INVOKED=false'; exit 0
}

if ($Stage -eq 'Migrations0001To0004') { $migrationRunner = Join-Path $Root 'tools\fm01_3342_runner.py'; if (-not (Test-Path -LiteralPath $migrationRunner -PathType Leaf)) { Hold 'FM01 migration runner is absent' } }
if ($Stage -eq 'Migrations0001To0004') { Hold 'CIO Owner-host exception does not authenticate an ordinary JSON release for live migration; authenticated release evidence is required' }
if ($Stage -eq 'DbTests') { Hold 'FM01 design test catalogue exists, but no approved executable DB test runner is present; case IDs remain NOT_RUN and no DB TEST PASS is claimed' }
Assert-ExecutionRelease

switch ($Stage) {
    'SafeStart' {
        if ((Get-TargetListener).Count -gt 0 -or (Get-TargetProcess).Count -gt 0) { Hold 'target already present; refusing duplicate start' }
        $proc = Start-Process -FilePath $Server -ArgumentList @("--defaults-file=$Config") -PassThru -WindowStyle Hidden
        Start-Sleep -Seconds 3
        Assert-ListenerProcessMatch @(Get-TargetProcess) @(Get-TargetListener) 'safe start' | Out-Null
        Write-Output "FM01_STAGE=$Stage"; Write-Output "RESULT=STARTED_PID_$($proc.Id)"; Write-Output 'SECRET_VALUES_EXPOSED=false'; exit 0
    }
    'BackupRecoveryCheck' {
        if ([string]::IsNullOrWhiteSpace($BackupPath)) { Hold 'BackupRecoveryCheck requires explicit backup path' }
        $resolvedBackup = [IO.Path]::GetFullPath($BackupPath)
        $approvedBackupRoot = [IO.Path]::GetFullPath((Join-Path $TargetRoot 'backups'))
        if (-not $resolvedBackup.StartsWith($approvedBackupRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { Hold 'backup path is outside the exact FM01 backup root' }
        $dir = Split-Path -Parent $resolvedBackup; if (-not (Test-Path -LiteralPath $dir -PathType Container)) { Hold 'backup parent directory absent' }
        if (Test-Path -LiteralPath $resolvedBackup) { Hold 'backup output already exists; refusing overwrite' }
        Assert-ListenerProcessMatch @(Get-TargetProcess) @(Get-TargetListener) 'backup preflight' | Out-Null
        $password = Read-DpapiSecret $DefaultRootSecretPath
        try { $previous=$env:MYSQL_PWD; $env:MYSQL_PWD=$password; & $Dump --protocol=tcp --host=$HostName --port=$Port --user='np-functional-root' --database=$Database --single-transaction --routines --triggers --result-file=$resolvedBackup 2>$null; if ($LASTEXITCODE -ne 0) { Hold 'backup command failed' } }
        finally { $env:MYSQL_PWD=$previous; $password=$null }
        if (-not (Test-Path -LiteralPath $resolvedBackup -PathType Leaf) -or (Get-Item -LiteralPath $resolvedBackup).Length -le 0) { Hold 'backup output is missing or empty' }
        $backupHash=(Get-FileHash -LiteralPath $resolvedBackup -Algorithm SHA256).Hash
        if ([string]::IsNullOrWhiteSpace($backupHash)) { Hold 'backup hash readback failed' }
        Assert-ListenerProcessMatch @(Get-TargetProcess) @(Get-TargetListener) 'backup postflight' | Out-Null
        Write-Output "FM01_STAGE=$Stage"; Write-Output "RESULT=BACKUP_CREATED"; Write-Output "BACKUP_SHA256=$backupHash"; Write-Output 'SECRET_VALUES_EXPOSED=false'; exit 0
    }
    'Migrations0001To0004' {
        $python = Join-Path $WorkspaceRoot 'G1P313\python-3.13.14\python.exe'
        if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { Hold 'approved Python runtime absent for FM01 migration runner' }
        $runner = Join-Path $Root 'tools\migrate_3342.py'
        $password = Read-DpapiSecret $RuntimeSecretPath
        try { $result = Invoke-ChildWithRedactedFailure $python @($runner,'--source-dir',$SourceDir,'--datadir',$DataDir,'--execute','--credential-path',$RuntimeSecretPath) @{ 'FM01_RUNTIME_PASSWORD' = $password } }
        finally { $password = $null }
        Write-Output "FM01_STAGE=$Stage"; Write-Output ($result | Out-String).Trim(); Write-Output 'SECRET_VALUES_EXPOSED=false'; exit 0
    }
    'IdentityPreflight' {
        $password=Read-DpapiSecret $RuntimeSecretPath
        try { $out=Invoke-ReadOnlySql 'SELECT DATABASE(),@@port,@@datadir; SELECT CURRENT_USER();' $password }
        finally { $password=$null }
        $listener=@(Get-TargetListener); $process=@(Get-TargetProcess)
        if($listener.Count -ne 1 -or $process.Count -ne 1 -or [int]$listener[0].OwningProcess -ne [int]$process[0].ProcessId){Hold 'identity preflight listener/process PID mismatch'}
        if(($out -join "`n") -notmatch [regex]::Escape($Database) -or ($out -join "`n") -notmatch '(?m)^3342$' -or ($out -join "`n") -notmatch [regex]::Escape($DataDir.Replace('\','/'))){Hold 'identity SQL did not prove exact database/port/datadir'}
        Write-Output "FM01_STAGE=$Stage"; Write-Output 'RESULT=IDENTITY_PREFLIGHT_PASS'; Write-Output 'OUTPUT_REDACTED=true'; Write-Output 'SECRET_VALUES_EXPOSED=false'; exit 0
    }
    'EvidenceExport' {
        if ([string]::IsNullOrWhiteSpace($EvidencePath)) { Hold 'EvidenceExport requires explicit evidence path' }
        $resolvedEvidence = [IO.Path]::GetFullPath($EvidencePath); $approvedEvidenceRoot=[IO.Path]::GetFullPath((Join-Path $TargetRoot 'evidence'))
        if (-not $resolvedEvidence.StartsWith($approvedEvidenceRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { Hold 'evidence path is outside the exact FM01 evidence root' }
        $evidence=@('target_id='+$TargetId,'database='+$Database,'endpoint='+$HostName+':'+$Port,'config_sha256='+$ExpectedConfigHash,'source_lineage=0001->0002->0003->0004','secret_values_exposed=false','live_operation_invoked=false','stage_outcome=EVIDENCE_EXPORT_ONLY')
        if (Test-Path -LiteralPath $resolvedEvidence) { Hold 'evidence path already exists; refusing overwrite' }
        $evidence += 'stage=EvidenceExport'
        $evidence += ('operator_identity=' + [Security.Principal.WindowsIdentity]::GetCurrent().Name)
        $evidence += ('approval_ref=' + (Split-Path -Leaf $ExecutionReleaseArtifact))
        $evidence += ('timestamp_utc=' + (Get-Date).ToUniversalTime().ToString('o'))
        $evidence += 'cleanup_state=NOT_APPLICABLE_PREP_ONLY'
        Set-Content -LiteralPath $resolvedEvidence -Value $evidence -Encoding UTF8
        Write-Output "FM01_STAGE=$Stage"; Write-Output 'RESULT=EVIDENCE_EXPORTED'; Write-Output "EVIDENCE_SHA256=$((Get-FileHash -LiteralPath $resolvedEvidence -Algorithm SHA256).Hash)"; exit 0
    }
    'GracefulStop' {
        if ((Get-TargetProcess).Count -ne 1 -or (Get-TargetListener).Count -ne 1) { Hold 'safe stop requires exactly one identified FM01 process and listener' }
        $expectedPid=[int](Get-TargetListener | Select-Object -First 1).OwningProcess
        $identifiedPid=[int](Get-TargetProcess | Select-Object -First 1).ProcessId
        if($expectedPid -ne $identifiedPid){Hold 'safe-stop owning PID does not match approved FM01 process'}
        $password=Read-DpapiSecret $DefaultRootSecretPath
        try { $previous=$env:MYSQL_PWD; $env:MYSQL_PWD=$password; 'shutdown' | & $Admin --protocol=tcp --host=$HostName --port=$Port --user='np-functional-root' --database=$Database --connect-timeout=5 2>$null; if($LASTEXITCODE -ne 0){Hold 'graceful shutdown failed'} }
        finally { $env:MYSQL_PWD=$previous; $password=$null }
        $deadline=(Get-Date).AddSeconds(30); do { Start-Sleep -Seconds 1 } while ((Get-Date) -lt $deadline -and ((Get-TargetProcess).Count -ne 0 -or (Get-TargetListener).Count -ne 0)); if((Get-TargetProcess).Count -ne 0 -or (Get-TargetListener).Count -ne 0){Hold 'safe-stop bounded wait expired; no force termination attempted'}
        Write-Output "FM01_STAGE=$Stage"; Write-Output 'RESULT=GRACEFUL_STOP_VERIFIED'; Write-Output 'SECRET_VALUES_EXPOSED=false'; exit 0
    }
}
