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
