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

from core.models import Patient, Attention, Speciality
from . import forms


@login_required
def home(request):
    specialities = Speciality.objects.all()
    return render(request, 'dashboard/home.html', locals())


@login_required
def add_patient(request):
    if request.method == 'POST':
        form = forms.PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, _('Patient created successfully.'))
            return redirect(reverse('dashboard:add_attention', kwargs={'patient_id': patient.id}))
    else:
        form = forms.PatientForm()
    return render(request, 'dashboard/form.html', locals())


@login_required
def update_patient(request, id):
    patient = get_object_or_404(Patient, pk=id)
    if request.method == 'POST':
        form = forms.PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, _('Patient updated successfully.'))
            return redirect(reverse('dashboard:home'))
    else:
        form = forms.PatientForm(instance=patient)
    return render(request, 'dashboard/formUpdate.html', locals())


@login_required
def add_attention(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = forms.AttentionForm(request.POST)
        if form.is_valid():
            attention = form.save(commit=False)
            attention.patient = patient
            attention.save()
            messages.success(request, _('Attention created successfully.'))
            return redirect(reverse('dashboard:home'))
    else:
        form = forms.AttentionForm()
    return render(request, 'dashboard/formAddAttention.html', locals())


@login_required
def update_attention(request, patient_id, id):
    patient = get_object_or_404(Patient, pk=patient_id)
    attention = get_object_or_404(Attention, pk=id)
    speciality = attention.speciality
    if request.method == 'POST':
        form = forms.AttentionUpdateForm(request.POST, instance=attention)
        if form.is_valid():
            attention = form.save(commit=False)
            attention.state = 'A'
            attention.save()
            messages.success(request, _('Attention updated successfully.'))
            return redirect(reverse('dashboard:home'))
    else:
        form = forms.AttentionUpdateForm(instance=attention)
    return render(request, 'dashboard/formUpdate.html', locals())


@login_required
def edit_patient(request, id):
    patient = get_object_or_404(Patient, pk=id)
    if request.method == 'POST':
        form = forms.PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, _('Patient updated successfuly'))
            return redirect(reverse('dashboard:home'))
    else:
        form = forms.PatientForm(instance=patient)
    return render(request, 'dashboard/form.html', locals())


@csrf_exempt
@login_required
def search_patient(request, pattern):
    parts = pattern.split()
    if len(parts) is 1:
        patients = Patient.objects.filter(
            Q(dni__contains=pattern) | Q(first_name__icontains=pattern) | Q(last_name__icontains=pattern))
    else:
        condition1 = reduce(operator.or_, [Q(first_name__icontains=s) for s in parts])
        condition2 = reduce(operator.or_, [Q(last_name__icontains=s) for s in parts])
        patients = Patient.objects.filter(
            Q(condition1) |
            Q(condition2))

    ids = list()
    for p in patients:
        ids.append(p.id)

    attentions = Attention.objects.select_related('speciality', 'patient').filter(patient__in=ids).order_by('id')
    parsed_data = []
    for p in patients:
        p.attentions = []
        for a in attentions:
            if p.id is a.patient.id:
                local_date = localtime(a.created_at)
                p.attentions.append({
                    'id': a.id,
                    'speciality': a.speciality.name,
                    'datetime': local_date.strftime("%d-%m %H:%M"),
                    'time': local_date.strftime("%H:%M")
                })
        parsed_data.append({
            'id': p.id,
            'first_name': p.first_name,
            'last_name': p.last_name,
            'dni': p.dni,
            'attentions': p.attentions
        })

    qs_json = json.dumps(parsed_data)
    return HttpResponse(qs_json, content_type='application/json')


@csrf_exempt
@login_required
def search_patient_advanced(request, speciality_id):
    speciality = get_object_or_404(Speciality, pk=speciality_id)
    today = now().today()
    attentions = Attention.objects.select_related('speciality', 'patient').filter(
        speciality=speciality,
        created_at__day=today.day,
        created_at__month=today.month,
        created_at__year=today.year,
        state='W')
    parsed_data = []
    for a in attentions:
        local_date = localtime(a.created_at)
        parsed_data.append({
            'id': a.patient.id,
            'first_name': a.patient.first_name,
            'last_name': a.patient.last_name,
            'dni': a.patient.dni,
            'attentions': [
                {
                    'id': a.id,
                    'speciality': speciality.name,
                    'datetime': local_date.strftime("%d-%m %H:%M"),
                    'time': local_date.strftime("%H:%M")
                }
            ]
        })

    qs_json = json.dumps(parsed_data)
    return HttpResponse(qs_json, content_type='application/json')
