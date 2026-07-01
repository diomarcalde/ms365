Import-Module ExchangeOnlineManagement

Connect-ExchangeOnline `
-UserPrincipalName DiegoO.Calderon@seps.gob.ec `
-DisableWAM `
-ShowBanner:$false

Get-MessageTraceV2 `
-StartDate (Get-Date).AddDays(-7) `
-EndDate (Get-Date) |
Select-Object `
    Received,
    SenderAddress,
    RecipientAddress,
    Subject,
    Status,
    MessageTraceId,
    Size |
ConvertTo-Json -Depth 5 |
Out-File C:\temp\correos.json -Encoding UTF8

Disconnect-ExchangeOnline -Confirm:$false