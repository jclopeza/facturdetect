from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Factura

class FacturaListView(LoginRequiredMixin, ListView):
    model = Factura
    template_name = 'factura_list.html'

class FacturaDetailView(LoginRequiredMixin, DetailView):
    model = Factura
    template_name = 'factura_detail.html'

class FacturaUpdateView(LoginRequiredMixin, UpdateView):
    model = Factura
    template_name = 'factura_edit.html'
    fields = (
        'numero_factura',
        'periodo_de_facturacion',
        'fecha_de_emision',
        'contrato',
        'inicio_contrato',
        'fin_contrato',
    )

class FacturaDeleteView(LoginRequiredMixin, DeleteView):
    model = Factura
    template_name = 'factura_delete.html'
    success_url = reverse_lazy('home')

class FacturaCreateView(LoginRequiredMixin, CreateView):
    model = Factura
    template_name = 'factura_new.html'
    fields = (
        'numero_factura',
        'periodo_de_facturacion',
        'fecha_de_emision',
        'contrato',
        'inicio_contrato',
        'fin_contrato',
    )
