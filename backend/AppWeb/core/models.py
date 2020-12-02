import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

SEX_CHOICES = [
    ('M', _('male')),
    ('F', _('female'))
]
STATE_CHOICES = [
    ('W', _('waiting')),
    ('A', _('attended'))
]
DISTRICT_CHOICES = [
    ('aqp-1', 'ALTO SELVA ALEGRE'),
    ('aqp-2', 'AREQUIPA'),
    ('aqp-3', 'CAYMA'),
    ('aqp-4', 'CERRO COLORADO'),
    ('aqp-5', 'CHARACATO'),
    ('aqp-6', 'CHIGUATA'),
    ('aqp-7', 'JACOBO HUNTER'),
    ('aqp-8', 'JOSE LUIS BUSTAMANTE Y RIVERO'),
    ('aqp-9', 'LA JOYA'),
    ('aqp-10', 'MARIANO MELGAR'),
    ('aqp-11', 'MIRAFLORES'),
    ('aqp-12', 'MOLLEBAYA'),
    ('aqp-13', 'PAUCARPATA'),
    ('aqp-14', 'POCSI'),
    ('aqp-15', 'POLOBAYA'),
    ('aqp-16', 'QUEQUEÑA'),
    ('aqp-17', 'SABANDIA'),
    ('aqp-18', 'SACHACA'),
    ('aqp-19', 'SAN JUAN DE SIGUAS'),
    ('aqp-20', 'SANTA ISABEL DE SIGUAS'),
    ('aqp-21', 'SANTA RITA DE SIHUAS'),
    ('aqp-22', 'SOCABAYA'),
    ('aqp-23', 'TIABAYA'),
    ('aqp-24', 'UCHUMAYO'),
    ('aqp-25', 'VITOR'),
    ('aqp-26', 'YANAHUARA'),
    ('aqp-27', 'YARABAMBA'),
    ('aqp-28', 'YURA')
]


TYPE_PRODUCT = (
    (1, 'Ropa'),
    (2, 'Víveres no Perecibles'),
    (3, 'Agrícola'),
    (4, 'Juguetes'),
    (5, 'Bicicletas'),
    (6, 'Otros'),
)

class Product(models.Model):
    name = models.IntegerField('Producto', choices=TYPE_PRODUCT, default=6)
    weight = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name="Peso")
    notes = models.CharField(max_length=255, verbose_name="Observaciones")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null="True")

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Patient(models.Model):
    dni = models.CharField(_("dni"), max_length=10)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    district = models.CharField(_("district"), choices=DISTRICT_CHOICES, max_length=6, blank=True, null=True)
    date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)
    sex = models.CharField(_("sex"), max_length=1, choices=SEX_CHOICES, blank=True, null=True)
    weight = models.CharField(_("weight"), blank=True, null=True, max_length=10)
    stature = models.CharField(_("stature"), blank=True, null=True, max_length=10)
    blood_pressure = models.CharField(_("blood pressure"), blank=True, null=True, max_length=10)
    allergic = models.TextField(_("allergic"), blank=True, null=True)
    notes = models.TextField(_("notes"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username's name."""
        return f'{self.first_name} {self.last_name}'

    def age(self):
        if self.date_of_birth:
            my_birth = self.date_of_birth
            today = datetime.date.today()
            my_age = (today.year - my_birth.year) - int((today.month, today.day) < (my_birth.month, my_birth.day))
        else:
            my_age = 0
        return my_age

    class Meta:
        verbose_name = _('patient')
        verbose_name_plural = _('patients')


class Speciality(models.Model):
    name = models.CharField(_("name"), max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('speciality')
        verbose_name_plural = _('specialities')
        ordering = ['name']


class Attention(models.Model):
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    state = models.CharField(_("state"), choices=STATE_CHOICES, max_length=1, default='W')
    doctor = models.CharField(_("doctor"), max_length=50, blank=True, null=True)
    diagnostic = models.TextField(_("diagnostic"), blank=True, null=True)
    treatment = models.TextField(_("treatment"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.first_name + ' ' + self.patient.last_name

    class Meta:
        verbose_name = _('attention')
        verbose_name_plural = _('attentions')
