$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git add .
git commit -m "Automatic commit at $timestamp"
git push