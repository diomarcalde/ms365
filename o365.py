import json
import os
from datetime import datetime, timedelta

JSON_FILE = r"C:\temp\correos.json"


def convertir_hora_ecuador(fecha_utc):

    try:

        fecha = datetime.fromisoformat(
            fecha_utc.replace("Z", "+00:00")
        )

        fecha_ec = fecha - timedelta(hours=5)

        return fecha_ec.strftime(
            "%d/%m/%Y %H:%M:%S"
        )

    except:

        return fecha_utc


def ultima_actualizacion():

    if not os.path.exists(JSON_FILE):
        return "Sin datos"

    fecha = datetime.fromtimestamp(
        os.path.getmtime(JSON_FILE)
    )

    return fecha.strftime(
        "%d/%m/%Y %H:%M:%S"
    )


def total_registros():

    if not os.path.exists(JSON_FILE):
        return 0

    with open(
            JSON_FILE,
            "r",
            encoding="utf-8"
    ) as archivo:

        datos = json.load(archivo)

    if isinstance(datos, dict):
        return 1

    return len(datos)


def buscar_correos(
        remitente,
        destinatario,
        asunto,
        fecha_inicio,
        fecha_fin):

    if not os.path.exists(JSON_FILE):
        return []

    try:

        with open(
                JSON_FILE,
                "r",
                encoding="utf-8"
        ) as archivo:

            datos = json.load(archivo)

        if isinstance(datos, dict):
            datos = [datos]

        resultados = []

        for correo in datos:

            sender = str(
                correo.get(
                    "SenderAddress",
                    ""
                )
            )

            recipient = str(
                correo.get(
                    "RecipientAddress",
                    ""
                )
            )

            subject = str(
                correo.get(
                    "Subject",
                    ""
                )
            )

            if remitente:

                if remitente.lower() not in sender.lower():
                    continue

            if destinatario:

                if destinatario.lower() not in recipient.lower():
                    continue

            if asunto:

                if asunto.lower() not in subject.lower():
                    continue

            correo["Received"] = convertir_hora_ecuador(
                str(
                    correo.get(
                        "Received",
                        ""
                    )
                )
            )

            resultados.append(correo)

        return resultados

    except Exception as e:

        print(e)

        return []