from rest_framework import serializers

from mailer.models import ErrorReport


class ErrorReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ErrorReport
        fields = '__all__'
