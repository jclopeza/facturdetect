from django.urls import path
from .views import FacturaListView, FacturaUpdateView, FacturaDetailView, FacturaDeleteView, FacturaCreateView, factura_pdf_upload, factura_pdf_upload_pdfplumber

urlpatterns = [
    path('<int:pk>/edit/', FacturaUpdateView.as_view(), name='factura_edit'),
    path('<int:pk>/', FacturaDetailView.as_view(), name='factura_detail'),
    path('<int:pk>/delete/', FacturaDeleteView.as_view(), name='factura_delete'),
    path('new/', FacturaCreateView.as_view(), name='factura_new'),
    path('factura_pdf_upload/', factura_pdf_upload, name='factura_pdf_upload'),
    path('factura_pdf_upload_pdfplumber/', factura_pdf_upload_pdfplumber, name='factura_pdf_upload_pdfplumber'),
    path('', FacturaListView.as_view(), name='factura_list'),
]
