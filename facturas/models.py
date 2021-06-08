from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Factura(models.Model):
    numero_factura = models.CharField(max_length=255)
    periodo_de_facturacion = models.CharField(max_length=255)
    fecha_de_emision = models.CharField(max_length=255)
    contrato = models.CharField(max_length=255)
    inicio_contrato = models.CharField(max_length=255)
    fin_contrato = models.CharField(max_length=255)

    def __str__(self):
        return self.numero_factura
    
    def get_absolute_url(self):
        return reverse('factura_detail', args=[str(self.id)])


class Invoice(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pdf_file_name = models.CharField(max_length=250)
    n_pages = models.PositiveSmallIntegerField()
    company = models.CharField(max_length=3)
    power_contracted = models.FloatField(null=True)
    duration = models.PositiveSmallIntegerField(null=True)
    power_price = models.FloatField(null=True)
    total_energy_consumed = models.FloatField(null=True)
    total_energy_consumed_p1 = models.FloatField(null=True)
    total_energy_consumed_p2 = models.FloatField(null=True)
    energy_price = models.FloatField(null=True)
    energy_price_p1 = models.FloatField(null=True)
    energy_price_p2 = models.FloatField(null=True)
    equipment_rental = models.FloatField(null=True)
    electricity_tax_percentage = models.FloatField(null=True)
    electricity_tax = models.FloatField(null=True)
    energy_cost = models.FloatField(null=True)
    energy_cost_p1 = models.FloatField(null=True)
    energy_cost_p2 = models.FloatField(null=True)
    power_cost = models.FloatField(null=True)
    iva_percentage = models.PositiveSmallIntegerField(null=True)
    iva_tax = models.FloatField(null=True)
    tax_base = models.FloatField(null=True)
    total_invoice = models.FloatField(null=True)

    def __str__(self):
        return f"{self.id}-{self.company} {self.total_invoice} €"
    
    def get_absolute_url(self):
        return reverse('invoice_detail', args=[str(self.id)])
