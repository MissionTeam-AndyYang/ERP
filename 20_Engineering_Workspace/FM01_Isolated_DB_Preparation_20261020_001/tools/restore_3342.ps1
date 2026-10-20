[CmdletBinding()]
param([Parameter(Mandatory)][string]$AuthorizationManifest,[Parameter(Mandatory)][string]$BackupHash)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
throw 'HOLD: pinned verified FM01 runtime adapter and authenticated manifest gate are not installed; no live action performed.'
