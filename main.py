from fastapi import FastAPI
from fastapi import Request
from fastapi import Form

from fastapi.responses import HTMLResponse

from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse

import subprocess
import tempfile
import os

from certificado import generar_pdf

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from o365 import (
    buscar_correos,
    ultima_actualizacion,
    total_registros
)

app = FastAPI()

POWERSHELL = r"C:\Program Files\PowerShell\7\pwsh.exe"

SCRIPT = r"C:\Users\docalderon\PycharmProjects\tracking365-demo\actualizar.ps1"

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "resultados": [],
            "total": 0,
            "remitente": "",
            "destinatario": "",
            "asunto": "",
            "fecha_inicio": "",
            "fecha_fin": "",
            "ultima_actualizacion": ultima_actualizacion(),
            "registros_cargados": total_registros()
        }
    )


@app.post("/buscar", response_class=HTMLResponse)
async def buscar(
        request: Request,
        remitente: str = Form(""),
        destinatario: str = Form(""),
        asunto: str = Form(""),
        fecha_inicio: str = Form(""),
        fecha_fin: str = Form("")
):

    resultados = buscar_correos(
        remitente,
        destinatario,
        asunto,
        fecha_inicio,
        fecha_fin
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "resultados": resultados,
            "total": len(resultados),
            "remitente": remitente,
            "destinatario": destinatario,
            "asunto": asunto,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "ultima_actualizacion": ultima_actualizacion(),
            "registros_cargados": total_registros()
        }
    )
@app.post("/actualizar")
async def actualizar():

    subprocess.run(

        [
            POWERSHELL,
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            SCRIPT
        ]

    )

    return RedirectResponse(

        "/",

        status_code=303

    )


@app.get("/detalle/{traceid}")
async def detalle(traceid: str):

    resultados = buscar_correos(

        "", "", "", "", ""

    )

    for correo in resultados:

        if correo["MessageTraceId"] == traceid:

            return correo

    return {

        "mensaje": "Correo no encontrado"

    }


@app.get("/certificado/{traceid}")
async def certificado(traceid: str):

    resultados = buscar_correos(

        "", "", "", "", ""

    )

    for correo in resultados:

        if correo["MessageTraceId"] == traceid:

            archivo = os.path.join(

                tempfile.gettempdir(),

                f"certificado_{traceid}.pdf"

            )

            generar_pdf(

                correo,

                archivo

            )

            return FileResponse(

                archivo,

                media_type="application/pdf",

                filename=f"Certificado_{traceid}.pdf"

            )

    return {

        "mensaje": "Correo no encontrado"

    }

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )