# ANKI_BACKUP_TO_ONEDRIVE.PS1
# Mirrors the Anki media folder and the most recent database backup, since
# Anki's own automatic backups only protect the card database
# (collection.anki2) -- they do NOT include media at all (verified: a
# .colpkg backup's "media" entry is a 9-byte empty placeholder). Without
# this, the ~10,500 images/audio files in this collection have zero
# off-disk protection.
#
# NOTE: this was originally set up to mirror into OneDrive, but the full
# 6GB media folder blew straight through Carter's OneDrive quota within
# minutes of being created and knocked OneDrive out of sync entirely. It
# now mirrors to a plain local folder (C:\AnkiBackup) instead -- this still
# protects against accidental in-app deletion/corruption, just not a full
# disk failure. Revisit if a cloud destination with more room becomes
# available (a paid OneDrive/Google Drive tier, an external drive, etc).
#
# Run manually any time with:  powershell -File anki_backup_to_onedrive.ps1
# Or let the scheduled task (set up alongside this script) run it daily.

$ErrorActionPreference = "Stop"

$src_media   = "$env:APPDATA\Anki2\User 1\collection.media"
$src_backups = "$env:APPDATA\Anki2\User 1\backups"
$dest        = "C:\AnkiBackup"

New-Item -ItemType Directory -Force -Path $dest | Out-Null
New-Item -ItemType Directory -Force -Path "$dest\collection.media" | Out-Null
New-Item -ItemType Directory -Force -Path "$dest\backups" | Out-Null

Write-Output "Mirroring collection.media -> $dest\collection.media ..."
robocopy $src_media "$dest\collection.media" /MIR /R:2 /W:5 /NFL /NDL /NP | Out-Null
Write-Output "  robocopy exit code: $LASTEXITCODE (0-7 are all success codes)"

$latest = Get-ChildItem $src_backups -Filter "*.colpkg" -ErrorAction SilentlyContinue |
          Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($latest) {
    Copy-Item $latest.FullName -Destination "$dest\backups\$($latest.Name)" -Force
    Write-Output "Copied latest collection backup: $($latest.Name)"
    # keep only the 3 newest copies in the OneDrive mirror, no need to pile these up
    Get-ChildItem "$dest\backups" -Filter "*.colpkg" |
        Sort-Object LastWriteTime -Descending | Select-Object -Skip 3 |
        Remove-Item -Force
} else {
    Write-Output "No .colpkg backup found to copy."
}

Write-Output "Done. $(Get-Date)"
