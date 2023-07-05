from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, HttpResponse, get_list_or_404, get_object_or_404
from app.models import client,Paciente
from django.contrib.auth.models import User
from app.models import Paciente, client, Product, Citas, UserInformation
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout
import datetime
from pathlib import Path
from docxtpl import DocxTemplate
from django.core import serializers

from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Importar el rest FRAMEWORK

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

@csrf_exempt
def index(request):
    data = json.loads(request.body)
    user_code = data['code']

    # Realiza la consulta de la base de datos
    paciente = Paciente.objects.filter(cliente__codigo=user_code)
    productos = Product.objects.filter(Q(promocionar_a__codigo=user_code) & Q(activa=True)).order_by("-updated_at")

    pacientes_serializer = PacienteSerializer(paciente, many=True)
    pacientes_data = pacientes_serializer.data

    productos_serializer = ProductSerializer(productos, many=True)
    productos_data = productos_serializer.data

    veterinario = User.objects.filter(client__codigo=user_code).first()
    veterinario_info = UserInformation.objects.filter(user=veterinario).first()

    if not veterinario or not veterinario_info:
        response_data = {
                'msg': "Su veterinario no ha configurado su cuenta.",
        }
        return JsonResponse(response_data, status=400)
    if paciente:
        response_data = {
                'msg': "OK",
                'pacientes': pacientes_data,
                "productos_5": productos_data[0:5],
                'productos': productos_data,
                "id_vet": veterinario.id,
                "lat": veterinario_info.lat ,
                "lon": veterinario_info.lon,
                "nombre_clinica": veterinario_info.nombre_clinica
        }
        return JsonResponse(response_data, status=200)
    else:
            # Devuelve una respuesta con estado 400 si no hay productos
        response_data = {
                'msg': "Su veterinario no ha registrado sus mascotas.",
        }
    return JsonResponse(response_data, status=400)
    # except:
    #     response_data = {
    #        'msg': "Ha ocurrido un error",
    #     }
    #     return JsonResponse(response_data, status=400)

@csrf_exempt
def descargar(request):
    
    user = request.GET.get('code')
    paciente_id = request.GET.get('paciente')

    
    if paciente_id:
        paciente = Paciente.objects.filter(id=paciente_id).all()
        citas = Citas.objects.filter(paciente=paciente[0]).order_by("-fecha_cita").all()
    
    else:
        paciente = get_list_or_404(Paciente, cliente__codigo=user) 

        citas = Citas.objects.filter(paciente__cliente__codigo=user).order_by("-fecha_cita").all()
    
    

    base_dir = Path(__file__).parent
    word_template_path = base_dir / "docxmedia/pacientetemplate.docx"
    today = datetime.date.today()
    doc = DocxTemplate(word_template_path)
    context = {
        "DATE": today,
        "pacientes": paciente,
        "citas": citas
    }

    for p in paciente:
        print(p.citas.all())
    doc.render(context)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=paciente.docx'
    doc.save(response)

    return response