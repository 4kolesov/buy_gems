import csv
import io
from datetime import datetime
from decimal import Decimal

from django.db.models import Count, DecimalField, Sum
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from deals.models import Deal

@api_view(['POST'])
def process_deals_file(request):
    """Обработать файл сделок."""
    file = request.FILES.get('deals')
    if not file:
        return Response('Беда', status=status.HTTP_400_BAD_REQUEST)
    try:
        file_wrapper = io.TextIOWrapper(file, encoding='utf-8')
        reader = csv.DictReader(file_wrapper)
        for row in reader:
            customer = row['customer']
            item = row['item']
            total = float(row['total'])
            quantity = int(row['quantity'])
            date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S.%f')
            deal = Deal(
                customer=customer,
                item=item,
                total=total,
                quantity=quantity,
                date=date,
            )
            deal.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            f'Error processing deals file: {str(e)}',
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@api_view(['GET'])
def get_top_clients(request, top_count=5):
    """
    Получить количество top_count самых активных клиентов.
    По умолчанию 5.
    """
    top_clients = (
        Deal.objects.values('customer')
        .annotate(spent_money=Coalesce(Sum('total', output_field=DecimalField()), Decimal(0)))
        .order_by('-spent_money')[:top_count]
    )
    client_usernames = [client.get('customer') for client in top_clients]

    gems = (
        Deal.objects.filter(customer__in=client_usernames)
        .values('item')
        .distinct()
        .annotate(count=Count('customer'))
        .filter(count__gte=2)
        .values_list('item', flat=True)
    )

    result = []
    for client in top_clients:
        username = client['customer']
        spent_money = client['spent_money']
        client_gems = list(gems) if username in client_usernames else []
        result.append({
            'username': username,
            'spent_money': spent_money,
            'gems': client_gems,
        })

    return Response({'response': result}, status=status.HTTP_200_OK)
