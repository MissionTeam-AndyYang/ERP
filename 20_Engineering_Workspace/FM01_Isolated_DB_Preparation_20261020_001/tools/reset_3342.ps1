[CmdletBinding()]
param([Parameter(Mandatory)][string]$AuthorizationManifest,[switch]$ConfirmReset)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
if (-not $ConfirmReset) { throw 'HOLD: explicit ConfirmReset is required; no live action performed.' }
throw 'HOLD: pinned verified FM01 runtime adapter and authenticated manifest gate are not installed; no live action performed.'
