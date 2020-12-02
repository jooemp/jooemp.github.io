from django.contrib import admin
from . import models

admin.site.register(models.Speciality)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'created_at')
    list_filter = (
        ('created_at', admin.DateFieldListFilter),
    )

class AttentionAdmin(admin.ModelAdmin):
    list_display = ('dni', 'patient', 'state', 'speciality', 'doctor', 'diagnostic', 'treatment', 'created_at')
    list_filter = (
        ('created_at', admin.DateFieldListFilter),
    )

    def dni(self, obj):
        return obj.patient.dni
   
admin.site.register(models.Attention, AttentionAdmin)
admin.site.register(models.Patient, PatientAdmin)