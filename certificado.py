
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import cm
import os

def generar_pdf(datos, archivo):
    doc = SimpleDocTemplate(
        archivo,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    title = styles["Heading1"]
    title.alignment = TA_CENTER
    title.textColor = colors.HexColor("#003366")

    h2 = styles["Heading2"]
    h2.alignment = TA_CENTER

    normal = styles["BodyText"]
    normal.leading = 18

    elems = []

    if os.path.exists("logo_seps.png"):
        logo = Image("logo_seps.png", width=3.8*cm, height=1.8*cm)
        head = Table([[
            logo,
            Paragraph(
                "<b>SUPERINTENDENCIA DE ECONOMÍA POPULAR Y SOLIDARIA</b><br/>"
                "<font size=10></font>",
                styles["Heading3"]
            )
        ]], colWidths=[3.2*cm, 13.8*cm])
        head.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        elems.append(head)
    else:
        elems.append(Paragraph(
            "SUPERINTENDENCIA DE ECONOMÍA POPULAR Y SOLIDARIA",
            title
        ))

    elems.append(Spacer(1,0.25*cm))

    line = Table([[""]], colWidths=[16*cm])
    line.setStyle(TableStyle([
        ("LINEBELOW",(0,0),(-1,-1),2,colors.HexColor("#003366"))
    ]))
    elems.append(line)
    elems.append(Spacer(1,0.6*cm))

    estado = str(datos.get("Status","")).strip()

    if estado == "Delivered":
        encabezado = "CERTIFICADO DE ENVÍO DE CORREO ELECTRÓNICO"
        observacion = ("De acuerdo con los registros de Microsoft Exchange Online, "
                       "el mensaje fue procesado y entregado correctamente.")
    elif estado == "Failed":
        encabezado = "CERTIFICADO DEL RESULTADO DEL ENVÍO DE CORREO ELECTRÓNICO"
        observacion = ("El procesamiento del mensaje finalizó con estado FAILED, "
                       "por lo que no existe evidencia de entrega al destinatario.")
    elif estado == "GettingStatus":
        encabezado = "CERTIFICADO DEL ESTADO DEL ENVÍO DE CORREO ELECTRÓNICO"
        observacion = ("El mensaje aún se encuentra en procesamiento y no existe "
                       "un resultado definitivo.")
    else:
        encabezado = "CERTIFICADO DEL RESULTADO DEL ENVÍO DE CORREO ELECTRÓNICO"
        observacion = "Información obtenida desde Microsoft Exchange Online."

    elems.append(Paragraph(encabezado, h2))
    elems.append(Spacer(1,0.5*cm))

    texto = (
        "Se certifica que, conforme a los registros de Microsoft Exchange Online, "
        "se obtuvo el siguiente resultado para el correo electrónico:"
    )
    elems.append(Paragraph(texto, normal))
    elems.append(Spacer(1,0.4*cm))

    tabla = Table([
        ["Asunto", datos.get("Subject","")],
        ["Remitente", datos.get("SenderAddress","")],
        ["Destinatario", datos.get("RecipientAddress","")],
        ["Fecha y hora", datos.get("Received","")],
        ["Estado", estado],
        ["Message Trace ID", datos.get("MessageTraceId","")]
    ], colWidths=[4.5*cm,11.5*cm])

    tabla.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#EAF2F8")),
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("GRID",(0,0),(-1,-1),0.4,colors.grey),
        ("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),7),
    ]))
    elems.append(tabla)
    elems.append(Spacer(1,0.8*cm))

    elems.append(Paragraph("<b>Observaciones</b>", styles["Heading3"]))
    elems.append(Paragraph(observacion, normal))

    elems.append(Spacer(1,2*cm))



    doc.build(elems)
