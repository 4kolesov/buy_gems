from api.views import get_top_clients, process_deals_file
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('v1/upload/', process_deals_file, name='file-upload'),
    path('v1/data/', get_top_clients, name='processed-data'),
]
