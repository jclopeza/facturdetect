from facturas.models import Invoice
from rest_framework import serializers

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        # Podríamos haber utilizado lo siguiente
        # fields = '__all__'
        fields = [
            'author',
            'created_at',
            'updated_at',
            'pdf_file_name',
            'n_pages',
            'company',
            'power_contracted',
            'duration',
            'power_price',
            'total_energy_consumed',
            'total_energy_consumed_p1',
            'total_energy_consumed_p2',
            'energy_price',
            'energy_price_p1',
            'energy_price_p2',
            'equipment_rental',
            'electricity_tax_percentage',
            'electricity_tax',
            'energy_cost',
            'energy_cost_p1',
            'energy_cost_p2',
            'power_cost',
            'iva_percentage',
            'iva_tax',
            'tax_base',
            'total_invoice',
        ]
