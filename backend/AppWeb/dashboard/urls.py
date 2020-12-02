from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('search-patient/<str:pattern>', views.search_patient, name='search_patient'),
    path('search-patient-advanced/<int:speciality_id>', views.search_patient_advanced, name='search-patient-advanced'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('edit-patient/<int:id>/', views.edit_patient, name='edit_patient'),
    path('update-patient/<int:id>/', views.update_patient, name='update_patient'),
    path('add-attention/<int:patient_id>/', views.add_attention, name='add_attention'),
    path('edit-attention/<int:patient_id>/<int:id>/', views.update_attention, name='update_attention'),
]
