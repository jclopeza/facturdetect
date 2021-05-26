from django.urls import path
from .views import FacturaListView, FacturaUpdateView, FacturaDetailView, FacturaDeleteView, FacturaCreateView

urlpatterns = [
    path('<int:pk>/edit/', FacturaUpdateView.as_view(), name='factura_edit'),
    path('<int:pk>/', FacturaDetailView.as_view(), name='factura_detail'),
    path('<int:pk>/delete/', FacturaDeleteView.as_view(), name='factura_delete'),
    path('new/', FacturaCreateView.as_view(), name='factura_new'),
    path('', FacturaListView.as_view(), name='factura_list'),
]
