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
    total_registros,
    obtener_por_trace,
    obtener_por_trace_y_destinatario,
    estadisticas
)

app = FastAPI()

POWERSHELL = r"C:\Program Files\PowerShell\7\pwsh.exe"

SCRIPT = r"C:\Users\docalderon\PycharmProjects\ms365\actualizar.ps1"

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
            "registros_cargados": total_registros(),
            "stats": estadisticas()
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
            "registros_cargados": total_registros(),
            "stats": estadisticas()
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
    correos=obtener_por_trace(traceid)
    if not correos:
        return {"mensaje":"Correo no encontrado"}
    return {
        "trace":traceid,
        "total_destinatarios":len(correos),
        "remitente":correos[0]["SenderAddress"],
        "asunto":correos[0]["Subject"],
        "fecha":correos[0]["Received"],
        "destinatarios":correos
    }


@app.get("/certificado/{traceid}/{destinatario}")
async def certificado(traceid:str,destinatario:str):
    correo=obtener_por_trace_y_destinatario(traceid,destinatario)
    if correo is None:
        return {"mensaje":"Correo no encontrado"}
    archivo=os.path.join(tempfile.gettempdir(),f"certificado_{traceid}.pdf")
    generar_pdf(correo,archivo)
    return FileResponse(archivo,media_type="application/pdf",filename=f"Certificado_{traceid}.pdf")

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )