[CmdletBinding()]
param([Parameter(Mandatory)][string]$AuthorizationManifest)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
throw 'HOLD: restore_3342.ps1 requires a CIO-approved executor, backup hash, and exact target manifest; no live action is implemented here.'
