from django.db.models import Sum
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from transactionstorage.storage.models import Transaction


class AggregatedAmountSerializer(serializers.Serializer):
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class TransactionView(APIView):
    serializer_class = AggregatedAmountSerializer
    queryset = Transaction.objects.all()

    def get(self, request):
        date_start = request.query_params.get('date_start')
        date_end = request.query_params.get('date_end')
        user_id = request.query_params.get('user_id')
        transaction_type = request.query_params.get('type')
        if not all(x is not None for x in [date_start, date_end, user_id, transaction_type]):
            result = self.queryset.query.set_empty()
        else:
            result = self.queryset.filter(
                user_id=user_id,
                transaction_datetime__gte=date_start,
                transaction_datetime__lte=date_end,
                type=transaction_type
            ).aggregate(total_amount=Sum('amount'))

        serializer = self.serializer_class(data=result)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
