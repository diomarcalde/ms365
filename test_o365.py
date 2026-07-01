import subprocess

script = r"""
Import-Module 'C:\Program Files\WindowsPowerShell\Modules\ExchangeOnlineManagement\3.10.0\ExchangeOnlineManagement.psd1' -Force

Connect-ExchangeOnline -UserPrincipalName diegoo.calderon@seps.gob.ec -DisableWAM

Get-ConnectionInformation

"""

resultado = subprocess.run(
    [
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        script
    ],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

print("STDOUT")
print(resultado.stdout)

print("STDERR")
print(resultado.stderr)