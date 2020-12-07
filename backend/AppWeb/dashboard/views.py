import json
import operator
from functools import reduce
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import localtime, now
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
from django.db.models import Sum

from core import models
from core.models import Product, Accumulate
from . import forms


@login_required
def home(request):
    if request.POST:
        product = request.POST.get('productsA')
        weight = request.POST.get('weight')
        quantity = request.POST.get('quantity')
        notes = request.POST.get('notes')
        if quantity=='':
            quantity=0
        donation = Product.objects.create(
            name=product, weight=weight, quantity=quantity, notes=notes, user= request.user)
        return redirect(reverse('dashboard:home'))

    types = models.TYPE_PRODUCT
    today = date.today()
    ropa = Product.objects.filter(created_at=today, name=1).aggregate(Sum('weight'))
    ropa = 0 if ropa['weight__sum'] == None else ropa['weight__sum']
    vivere = Product.objects.filter(created_at=today, name=2).aggregate(Sum('weight'))
    vivere = 0 if vivere['weight__sum'] == None else vivere['weight__sum']

    agricola = Product.objects.filter(created_at=today, name=3).aggregate(Sum('weight'))
    agricola = 0 if agricola['weight__sum'] == None else agricola['weight__sum']

    juguete = Product.objects.filter(created_at=today, name=4).aggregate(Sum('weight'))
    juguete = 0 if juguete['weight__sum'] == None else juguete['weight__sum']

    bicicleta = Product.objects.filter(created_at=today, name=5).aggregate(Sum('weight'))
    bicicleta = 0 if bicicleta['weight__sum'] == None else bicicleta['weight__sum']
    qbici = Product.objects.filter(created_at=today, name=5).aggregate(Sum('quantity'))
    qbici = 0 if qbici['quantity__sum'] == None else qbici['quantity__sum']
    otro = Product.objects.filter(created_at=today, name=6).aggregate(Sum('weight'))
    otro = 0 if otro['weight__sum'] == None else otro['weight__sum']

    acumm = Accumulate.objects.all().order_by('day')
    toneladas = Product.objects.all().aggregate(Sum('weight'))
    toneladas2020 = toneladas['weight__sum']
    return render(request, 'dashboard/home.html', locals())

def close_day(request):
    today = datetime.strptime(request.POST['dateC'],'%m-%d-%Y').date()

    ropa = Product.objects.filter(created_at=today, name=1).aggregate(Sum('weight'))
    ropa = 0 if ropa['weight__sum'] == None else ropa['weight__sum']
    vivere = Product.objects.filter(created_at=today, name=2).aggregate(Sum('weight'))
    vivere = 0 if vivere['weight__sum'] == None else vivere['weight__sum']

    agricola = Product.objects.filter(created_at=today, name=3).aggregate(Sum('weight'))
    agricola = 0 if agricola['weight__sum'] == None else agricola['weight__sum']

    juguete = Product.objects.filter(created_at=today, name=4).aggregate(Sum('weight'))
    juguete = 0 if juguete['weight__sum'] == None else juguete['weight__sum']

    bicicleta = Product.objects.filter(created_at=today, name=5).aggregate(Sum('weight'))
    bicicleta = 0 if bicicleta['weight__sum'] == None else bicicleta['weight__sum']

    qbici = Product.objects.filter(created_at=today, name=5).aggregate(Sum('quantity'))
    qbici = 0 if qbici['quantity__sum'] == None else qbici['quantity__sum']

    otro = Product.objects.filter(created_at=today, name=6).aggregate(Sum('weight'))
    otro = 0 if otro['weight__sum'] == None else otro['weight__sum']
    try:
        accum = Accumulate.objects.get(day=today)
        accum.day=today
        accum.clothes=ropa
        accum.viveres=vivere
        accum.agricola=agricola
        accum.toys=juguete
        accum.bicycle=bicicleta
        accum.bicycle_cant=qbici
        accum.others=otro
        accum.save()

    except Accumulate.DoesNotExist:
        accum = Accumulate.objects.create(
            day=today, clothes=ropa, viveres=vivere, agricola=agricola, 
            toys=juguete, bicycle=bicicleta, bicycle_cant=qbici, 
            others=otro)
	
    
    # if Accumulate.
    #     accum = Accumulate.objects.create(
    #         day=today, clothes=ropa, viveres=vivere, agricola=agricola, 
    #         toys=juguete, bicycle=bicicleta, bicycle_cant=qbici, 
    #         others=otro)
        
    return render(request, 'dashboard/home.html', locals())
    