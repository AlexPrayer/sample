from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from transactionstorage.storage.models import Transaction


class TransactionView(APIView):
    def get(self, request):
        date_start = request.query_params.get('date_start')
        date_end = request.query_params.get('date_end')
        if date_start is None or date_end is None:
            return Response(data=[])
        data = Transaction.objects.filter(datetime__gte=date_start, datetime__lte=date_end).aggregate(Sum('amount'))
        return Response(data=data)
