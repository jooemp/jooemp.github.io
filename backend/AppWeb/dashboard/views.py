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
from datetime import date
from django.db.models import Sum

from core import models
from core.models import Product
from . import forms


@login_required
def home(request):
    if request.POST:
        product = request.POST.get('productsA')
        weight = request.POST.get('weight')
        notes = request.POST.get('notes')
        donation = Product.objects.create(
            name=product, weight=weight, notes=notes, user= request.user)
        
        return redirect(reverse('dashboard:home'))

    types = models.TYPE_PRODUCT
    today = date.today()
    donations = Product.objects.filter(created_at=today).aggregate(Sum('weight'))
    donation = donations['weight__sum']
    return render(request, 'dashboard/home.html', locals())

