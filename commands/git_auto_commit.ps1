$lastGitCommandDateString = Get-Content -Path "C:\source\IATextHelp\n8n_python_workflow\lastGitCommand.md" | Out-String
$lastGitCommandDate = [datetime]::ParseExact($lastGitCommandDateString.Trim(), "yyyy-MM-dd HH:mm:ss", $null)
$currentDate = Get-Date

if ($currentDate -lt $lastGitCommandDate) {
    git pull
    git add .
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "Automatic sync and commit at $timestamp"
    git push
} else {
    Write-Host "Execution date in lastGitCommand.md has passed. Not executing git commands."
}