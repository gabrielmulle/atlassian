# Build Basic Auth header
$pair   = "NDUxxxxxQ4Olxx6xuFFKxxxxxxx"
#$bytes  = [System.Text.Encoding]::ASCII.GetBytes($pair)
#$base64 = [System.Convert]::ToBase64String($bytes)
$headers = @{
    Authorization = "Bearer $pair"
    Accept        = "application/json"
}

# Read each line from the file and call Jira API
Get-Content ".\projects.csv" | ForEach-Object {
    $line = $_.Trim()
    Write-Host "Archiving DC project ${line}: " -NoNewline

    Start-Sleep -Milliseconds 250

    try {
        # Use Invoke-WebRequest so we can easily get the HTTP status code
        $result = Invoke-WebRequest -Method Put `
            -Uri "https://instance.net/rest/api/2/project/$line/archive" `
            -Headers $headers `
            -ErrorAction Stop

        Write-Host $result.StatusCode
    }
    catch {
        Write-Host "Failed - $($_.Exception.Message)"
    }
}
