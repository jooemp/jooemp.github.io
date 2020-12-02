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

from core import models
from . import forms


@login_required
def home(request):
    types = models.TYPE_PRODUCT
    return render(request, 'dashboard/home.html', locals())

