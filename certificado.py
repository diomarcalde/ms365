from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generar_pdf(datos, salida):
    s = getSampleStyleSheet()
    d = SimpleDocTemplate(salida)
    texto = (
        "CERTIFICADO<br/><br/>"
        f"Asunto: {datos.get('Subject','')}<br/>"
        f"Remitente: {datos.get('SenderAddress','')}<br/>"
        f"Destinatario: {datos.get('RecipientAddress','')}<br/>"
        f"Fecha: {datos.get('Received','')}<br/>"
        f"Estado: {datos.get('Status','')}<br/><br/>"
        "Se certifica que el correo fue enviado y no puede determinarse si fue leído."
    )
    d.build([Paragraph(texto, s['BodyText'])])