$lastGitCommandDateString = Get-Content -Path "C:\source\IATextHelp\n8n_python_workflow\commands\lastGitCommand.md" | Out-String
$lastGitCommandDate = [datetime]::ParseExact($lastGitCommandDateString.Trim(), "yyyy-MM-dd HH:mm:ss", $null)
$currentDate = Get-Date

if ($currentDate -ge $lastGitCommandDate) {
    git pull
    git add .
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "Automatic sync and commit at $timestamp"
    git push

    # Update lastGitCommand.md with current time + 2 hours
    $newExecutionDate = (Get-Date).AddHours(2).ToString("yyyy-MM-dd HH:mm:ss")
    Set-Content -Path "C:\source\IATextHelp\n8n_python_workflow\commands\lastGitCommand.md" -Value $newExecutionDate
    Write-Host "Updated lastGitCommand.md with next execution time: $newExecutionDate"
} else {
    Write-Host "Execution date in lastGitCommand.md has not yet been reached. Not executing git commands."
}