from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from io import BytesIO
import base64

from django.conf import settings

import imgkit
import os


@api_view(["POST"])
def generate_pdf(request):
    body = request.data.get("html")
    try:
        # html_content = render_to_string("invoice_template.html", {})
        pdf_file = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(body.encode()), pdf_file)

        if pdf.err:
            print(pdf.err)
            return Response({"err": "Erreur lors de la conversion en PDF"})

        return Response(
            {"response": f"{base64.b64encode(pdf_file.getvalue()).decode('utf-8')}"}
        )

    except Exception as e:
        # Gérer les erreurs générales et loguer les détails
        return Response(
            {"err": "Une erreur s'est produite lors de la génération du PDF"}
        )


@api_view(["POST"])
def generate_image(request):
    body = request.data.get("html")
    try:
        # html_content = render_to_string("invoice_template.html", {})
        config = imgkit.config(
            wkhtmltoimage=os.path.join(settings.BASE_DIR, "wkhtmltoimage.exe"),
            xvfb="/opt/bin/xvfb-run",
        )

        image = imgkit.from_string(f"{body}", False, config=config)

        return Response({"response": f"{base64.b64encode(image).decode('utf-8')}"})

    except Exception as e:
        print(e)
        # Gérer les erreurs générales et loguer les détails
        return Response(
            {"err": "Une erreur s'est produite lors de la génération du Image"}
        )
