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
    weight = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Peso")
    notes = models.CharField(max_length=255, null="true", verbose_name="Observaciones")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null="True")

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    