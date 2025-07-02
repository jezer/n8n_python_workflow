
while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git add .
    git commit -m "Automatic commit at $timestamp"
    git push
    Start-Sleep -Seconds 3600 # Sleep for 1 hour
}
