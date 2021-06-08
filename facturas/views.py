import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.forms import ModelForm
from pdf2image import convert_from_bytes
from datetime import datetime
from utilities.proccess_pdf_files import proccess_invoice_electric


from .forms import UploadFileForm
from .models import Factura, Invoice
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
            print(values_found)
            factura_form = FacturaForm(initial=values_found)
            print("Formulario creado")
            return render(request, 'factura_new.html', {'form': factura_form})
    else:
        form = UploadFileForm()
    return render(request, 'factura_pdf_upload.html', {'form': form})


def factura_pdf_upload_pdfplumber(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            target_dir = 'media'
            file = request.FILES['file']
            current_time_str = datetime.now().strftime("%Y%m%d-%H%M%S.%f")
            file_name = f'{current_time_str}.pdf'
            with open(f'{target_dir}/{file_name}', 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            miInvoice = proccess_invoice_electric(f'{target_dir}/{file_name}')
            # Ahora debemos insertar los datos calculados en BDD
            # p1 = Editor(nombre='Addison­Wesley', domicilio='75 Arlington Street',
            # ... ciudad='Boston', estado='MA', pais='U.S.A.',
            # ... website='http://www.apress.com/')
            # p1.save()
            record = Invoice(
                author=request.user,
                pdf_file_name=file_name,
                n_pages=miInvoice.n_pages,
                company=miInvoice.company,
                power_contracted=miInvoice.power_contracted,
                duration=miInvoice.duration,
                power_price=miInvoice.power_price,
                total_energy_consumed=miInvoice.total_energy_consumed,
                total_energy_consumed_p1=miInvoice.total_energy_consumed_p1,
                total_energy_consumed_p2=miInvoice.total_energy_consumed_p2,
                energy_price=miInvoice.energy_price,
                energy_price_p1=miInvoice.energy_price_p1,
                energy_price_p2=miInvoice.energy_price_p2,
                equipment_rental=miInvoice.equipment_rental,
                electricity_tax_percentage=miInvoice.electricity_tax_percentage,
                electricity_tax=miInvoice.electricity_tax,
                energy_cost=miInvoice.energy_cost,
                energy_cost_p1=miInvoice.energy_cost_p1,
                energy_cost_p2=miInvoice.energy_cost_p2,
                power_cost=miInvoice.power_cost,
                iva_percentage=miInvoice.iva_percentage,
                iva_tax=miInvoice.iva_tax,
                tax_base=miInvoice.tax_base,
                total_invoice=miInvoice.total_invoice
            )
            record.save()
            # Pasamos la factura a objeto json
            miInvoiceJsonStr = json.dumps(record.__dict__)
            print(miInvoiceJsonStr)

            print("YA HEMOS GANADO UNA NUEVA BATALLA!!!!!!!!!")
    else:
        form = UploadFileForm()
    return render(request, 'factura_pdf_upload_pdfplumber.html', {'form': form})
