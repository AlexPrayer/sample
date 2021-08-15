from rest_framework.generics import ListAPIView
from rest_framework.response import Response


class TransactionView(ListAPIView):
    def get_queryset(self):
        qs = super().get_queryset()

        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')

        if date_start is None or date_end is None:
            return Response(status=400, data='Not provided date_1 or date_2 arg')

        count = qs.filter(datetime__gte=date_start, datetime__lte=date_end).count()
        return count
