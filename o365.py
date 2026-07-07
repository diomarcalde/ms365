import json
import os
from datetime import datetime, timedelta

JSON_FILE = r"C:\temp\correos.json"


# ==========================================================
# LECTURA DEL JSON
# ==========================================================

def _leer_json():

    if not os.path.exists(JSON_FILE):
        return []

    try:

        with open(JSON_FILE, "r", encoding="utf-8") as archivo:

            contenido = archivo.read().strip()

        if not contenido:
            return []

        datos = json.loads(contenido)

        if isinstance(datos, dict):
            return [datos]

        if isinstance(datos, list):
            return datos

        return []

    except Exception as e:

        print("Error leyendo JSON:", e)

        return []


# ==========================================================
# FECHAS
# ==========================================================

def convertir_hora_ecuador(fecha):

    if not fecha:
        return ""

    try:

        fecha = datetime.fromisoformat(
            str(fecha).replace("Z", "+00:00")
        )

        fecha = fecha - timedelta(hours=5)

        return fecha.strftime("%d/%m/%Y %H:%M:%S")

    except Exception:

        return str(fecha)


def ultima_actualizacion():

    if not os.path.exists(JSON_FILE):
        return "Sin datos"

    fecha = datetime.fromtimestamp(
        os.path.getmtime(JSON_FILE)
    )

    return fecha.strftime("%d/%m/%Y %H:%M:%S")


def total_registros():

    return len(_leer_json())


# ==========================================================
# BUSQUEDA
# ==========================================================

def buscar_correos(
        remitente="",
        destinatario="",
        asunto="",
        fecha_inicio="",
        fecha_fin="",
        estado=""
):

    datos = _leer_json()

    resultados = []

    for correo in datos:

        if remitente:

            if remitente.lower() not in correo.get(
                    "SenderAddress",
                    ""
            ).lower():
                continue

        if destinatario:

            if destinatario.lower() not in correo.get(
                    "RecipientAddress",
                    ""
            ).lower():
                continue

        if asunto:

            if asunto.lower() not in correo.get(
                    "Subject",
                    ""
            ).lower():
                continue

        if estado:

            if estado.lower() != correo.get(
                    "Status",
                    ""
            ).lower():
                continue

        fila = correo.copy()

        fila["Received"] = convertir_hora_ecuador(
            fila.get("Received")
        )

        resultados.append(fila)

    resultados.sort(

        key=lambda x: x["Received"],

        reverse=True

    )

    return resultados


# ==========================================================
# DETALLE DEL ENVIO
# ==========================================================

def obtener_por_trace(trace):

    datos = _leer_json()

    resultados = []

    for correo in datos:

        if correo.get("MessageTraceId") == trace:

            fila = correo.copy()

            fila["Received"] = convertir_hora_ecuador(

                fila.get("Received")

            )

            resultados.append(fila)

    return resultados


# ==========================================================
# CERTIFICADO INDIVIDUAL
# ==========================================================

def obtener_por_trace_y_destinatario(
        trace,
        destinatario
):

    datos = _leer_json()

    for correo in datos:

        if (

                correo.get("MessageTraceId") == trace

                and

                correo.get("RecipientAddress") == destinatario

        ):

            fila = correo.copy()

            fila["Received"] = convertir_hora_ecuador(

                fila.get("Received")

            )

            return fila

    return None


# ==========================================================
# DASHBOARD
# ==========================================================

def estadisticas():

    datos = _leer_json()

    return {

        "total": len(datos),

        "Delivered": len(

            [

                x

                for x in datos

                if x.get("Status") == "Delivered"

            ]

        ),

        "Failed": len(

            [

                x

                for x in datos

                if x.get("Status") == "Failed"

            ]

        ),

        "GettingStatus": len(

            [

                x

                for x in datos

                if x.get("Status") == "GettingStatus"

            ]

        ),

        "FilteredAsSpam": len(

            [

                x

                for x in datos

                if x.get("Status") == "FilteredAsSpam"

            ]

        )

    }