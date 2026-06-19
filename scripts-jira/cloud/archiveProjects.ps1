# Build Basic Auth header
$pair   = "ATATT3xFfGF0KKKxxxxxzPxxxxxxx"
#$bytes  = [System.Text.Encoding]::ASCII.GetBytes($pair)
#$base64 = [System.Convert]::ToBase64String($bytes)
$headers = @{
    Authorization = "mulleg@example.com:$pair"
    Accept        = "application/json"
}

# Read each line from the file and call Jira API
Get-Content ".\projects.csv" | ForEach-Object {
    $line = $_.Trim()
    Write-Host "Archiving cloud project ${line}: " -NoNewline

    Start-Sleep -Milliseconds 250

    try {
        # Use Invoke-WebRequest so we can easily get the HTTP status code
        $result = Invoke-WebRequest -Method Post `
            -Uri "https://nw-test.atlassian.net/rest/api/3/project/$line/archive" `
            -Headers $headers `
            -ErrorAction Stop

        Write-Host $result.StatusCode
    }
    catch {
        Write-Host "Failed - $($_.Exception.Message)"
    }
}
