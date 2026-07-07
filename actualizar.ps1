Import-Module ExchangeOnlineManagement

Connect-ExchangeOnline `
    -UserPrincipalName DiegoO.Calderon@seps.gob.ec `
    -DisableWAM `
    -ShowBanner:$false

$fechaInicio = (Get-Date).AddDays(-5)
$fechaFin    = Get-Date

$remitentes = @(
    "Notificaciones-INSOEPS-DNLOEPS@seps.gob.ec"
)

$resultados = @()

foreach ($remitente in $remitentes) {

    Write-Host "Consultando $remitente ..."

    $datos = Get-MessageTraceV2 `
        -StartDate $fechaInicio `
        -EndDate $fechaFin `
        -SenderAddress $remitente `
        -ResultSize 5000

    if ($datos) {
        $resultados += $datos
    }
}

$resultados |
Sort-Object Received -Descending |
Select-Object `
    MessageTraceId,
    MessageId,
    Received,
    SenderAddress,
    RecipientAddress,
    Subject,
    Status,
    Size,
    FromIP,
    ToIP |
ConvertTo-Json -Depth 5 |
Out-File "C:\temp\correos.json" -Encoding UTF8

Disconnect-ExchangeOnline -Confirm:$false

Write-Host ""
Write-Host "Total de registros: $($resultados.Count)"
Write-Host "Archivo generado: C:\temp\correos.json"