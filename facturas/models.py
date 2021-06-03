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
    company = models.CharField(max_length=250)
    total_amount = models.FloatField(default=60.72)
    total_energy = models.FloatField(default=34.55)
    total_power = models.FloatField(default=12.48)
    total_services = models.FloatField(default=0.75)
    total_taxes = models.FloatField(default=12.94)
    total_energy_consumed = models.FloatField(default=193.0)
    energy_price = models.FloatField(default=0.179017)
    energy_cost = models.FloatField(default=34.55)
    power_contracted = models.FloatField(default=3.3)
    duration = models.PositiveSmallIntegerField(default=28)
    power_price = models.FloatField(default=0.135031)
    power_cost = models.FloatField(default=12.48)
    equipment_rental = models.FloatField(default=0.75)
    electricity_tax_percentage = models.FloatField(default=5.11269632)
    electricity_tax = models.FloatField(default=5.11)
    iva_tax = models.FloatField(default=10.54)

    def __str__(self):
        return f"{self.id}-{self.company} {self.total_amount} €"
    
    def get_absolute_url(self):
        return reverse('invoice_detail', args=[str(self.id)])
