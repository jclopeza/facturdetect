from facturas.models import Invoice
from rest_framework import viewsets
from rest_framework import permissions
from quickstart.serializers import InvoiceSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows invoices to be viewed or edited.
    """
    queryset = Invoice.objects.all().order_by('created_at')
    serializer_class = InvoiceSerializer
    # permission_classes = [permissions.IsAuthenticated]
