from django.db.models import Sum
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from transactionstorage.storage.models import TRANSACTION_TYPES, Transaction


class RequestSerializer(serializers.Serializer):
    date_start = serializers.DateField()
    date_end = serializers.DateField()
    user_id = serializers.IntegerField()
    transaction_type = serializers.ChoiceField(choices=TRANSACTION_TYPES)


class ReponseSerializer(serializers.Serializer):
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)

    def validate_total_amount(self, value):
        if value is None:
            raise ValidationError("No data for such query params")
        return value


class TransactionView(APIView):
    serializer_class = ReponseSerializer
    request_serializer_class = RequestSerializer
    queryset = Transaction.objects.all()

    def get(self, request):
        request_serializer = RequestSerializer(data=request.query_params)
        if not request_serializer.is_valid():
            raise ValidationError("Wrong query params")

        request_data = request_serializer.data

        result = self.queryset.filter(
            user_id=request_data["user_id"],
            transaction_datetime__gte=request_data["date_start"],
            transaction_datetime__lte=request_data["date_end"],
            type=request_data["transaction_type"]
        ).aggregate(total_amount=Sum('amount'))

        serializer = self.serializer_class(data=result)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
