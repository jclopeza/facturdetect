from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms import ModelForm
from pdf2image import convert_from_bytes
from datetime import datetime


from .forms import UploadFileForm
from .models import Factura
from aws.functions import upload_file_to_s3, detect_text

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


def handle_factura_pdf_uploaded(file):
    current_time_str = datetime.now().strftime("%Y%m%d-%H%M%S.%f")
    images = convert_from_bytes(file.read())
    for idx, image in enumerate(images, start=1):
        img_name_s3 = f'{current_time_str}-{idx}.jpg'
        img_name = f'media/{img_name_s3}'
        image.save(img_name, 'JPEG')
        # Ahora subimos la imagen a S3
        upload_file_to_s3(img_name, 'facturdetect-collection', object_name=img_name_s3)
    return current_time_str, len(images)


class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        fields = ['numero_factura', 'periodo_de_facturacion', 'fecha_de_emision', 'contrato', 'inicio_contrato', 'fin_contrato']


def factura_pdf_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            img_prefix, img_num = handle_factura_pdf_uploaded(request.FILES['file'])
            print(f"Prefijo imagenes = {img_prefix}, Total de imagenes = {img_num}")
            values_found = detect_text(img_prefix, img_num, 'facturdetect-collection')
            #print(values_found)
            factura_form = FacturaForm(initial=values_found)
            return render(request, 'factura_new.html', {'form': factura_form})
    else:
        form = UploadFileForm()
    return render(request, 'factura_pdf_upload.html', {'form': form})
