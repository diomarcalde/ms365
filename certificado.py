from reportlab.platypus import *

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.enums import TA_CENTER

from reportlab.lib.colors import navy



def generar_pdf(datos, archivo):

    estilos = getSampleStyleSheet()

    titulo = estilos["Heading1"]

    titulo.alignment = TA_CENTER

    titulo.textColor = navy

    pdf = SimpleDocTemplate(archivo)

    elementos = []

    elementos.append(

        Paragraph(

            "SUPERINTENDENCIA DE ECONOMÍA POPULAR Y SOLIDARIA",

            titulo

        )

    )

    elementos.append(

        Spacer(1,20)

    )

    elementos.append(

        Paragraph(

            "<b>CERTIFICADO DE ENVÍO DE CORREO ELECTRÓNICO</b>",

            estilos["Heading2"]

        )

    )

    texto = f"""

Se certifica que el correo electrónico con asunto:

<b>{datos['Subject']}</b>

fue enviado desde:

<b>{datos['SenderAddress']}</b>

hacia:

<b>{datos['RecipientAddress']}</b>

con fecha:

<b>{datos['Received']}</b>

Estado:

<b>{datos['Status']}</b>

Message Trace:

<b>{datos['MessageTraceId']}</b>

<br/><br/>

Este certificado acredita únicamente que el mensaje fue procesado y enviado mediante Microsoft Exchange Online.

No es posible determinar si el destinatario abrió o leyó el mensaje.

"""

    elementos.append(

        Paragraph(

            texto,

            estilos["BodyText"]

        )

    )

    pdf.build(elementos)