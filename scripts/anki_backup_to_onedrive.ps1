# Back up an Anki profile's media and latest collection backup to a local folder.
# The historical filename is retained for existing scheduled tasks.
param(
    [string]$ProfilePath = (Join-Path $env:APPDATA "Anki2\User 1"),
    [string]$Destination = "C:\AnkiBackup"
)

$ErrorActionPreference = "Stop"
$media = Join-Path $ProfilePath "collection.media"
$backups = Join-Path $ProfilePath "backups"
$mediaDestination = Join-Path $Destination "collection.media"
$backupDestination = Join-Path $Destination "backups"

if (-not (Test-Path -LiteralPath $media -PathType Container)) {
    throw "Anki media folder not found: $media"
}

New-Item -ItemType Directory -Force -Path $mediaDestination, $backupDestination | Out-Null

Write-Output "Copying media to $mediaDestination"
& robocopy $media $mediaDestination /E /R:2 /W:5 /NFL /NDL /NP | Out-Null
if ($LASTEXITCODE -ge 8) {
    throw "Media backup failed (robocopy exit code $LASTEXITCODE)."
}

if (Test-Path -LiteralPath $backups -PathType Container) {
    $latest = Get-ChildItem -LiteralPath $backups -Filter "*.colpkg" -File |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latest) {
        Copy-Item -LiteralPath $latest.FullName -Destination $backupDestination -Force
        Write-Output "Copied collection backup: $($latest.Name)"
    } else {
        Write-Output "No .colpkg backup was found."
    }
} else {
    Write-Output "No Anki backup folder was found at $backups."
}

Write-Output "Backup complete: $Destination"
