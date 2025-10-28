import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mailer.serializers import ErrorReportSerializer

load_dotenv()
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

# Create your views here.


def index(error: str) -> str:
    return f"""
    <html>
        <body>
        <h1>{error}</h1>
        </body>
    </html>
    """


def create_message(data: dict) -> EmailMessage:
    message = EmailMessage()
    message['From'] = FROM_EMAIL
    message['To'] = data['issuer']
    message['Subject'] = 'Error Report'
    message.add_alternative(index(data['error']), subtype='html')
    return message


class EmailSender(APIView):

    def post(self, request):
        serializer = ErrorReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        message = create_message(serializer.data)
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(message)
        return Response(status=status.HTTP_204_NO_CONTENT)
