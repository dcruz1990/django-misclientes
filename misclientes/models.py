####################################################################
#                MisClientes V 0.0.1                               #
#      By: Luis Miguel Pozo González luis.pozo@nauta.cu            #
#          Dennis Quesada Cruz       dcruz@pescatun.alinet.cu      #
####################################################################

from django.db import models
from django.urls import reverse
from django.utils.timezone import datetime
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template
from django.contrib.auth.models import User


class Configuracion(models.Model):
    ENTERPRISE_CODE = 'code'
    ENTERPRISE_NIT = 'nit'
    ENTERPRISE_LAST_UPDATE = 'last_update'
    ENTERPRISE_NAME = 'enterprise_name'
    ENTERPRISE_ORDERING_CHOICES = (
        (ENTERPRISE_CODE, 'Codigo REUP'),
        (ENTERPRISE_LAST_UPDATE, 'Fecha de actualizacion'),
        (ENTERPRISE_NAME, 'Nombre del Cliente'),
        (ENTERPRISE_NIT, 'NIT'),
    )
    PERSONS_IDNUM = 'idnum'
    PERSONS_NAME = 'name'
    PERSON_LASTNAME = 'lastname'
    PERSON_ORDERING_CHOICES = (
        (PERSON_LASTNAME, 'Apellidos'),
        (PERSONS_IDNUM, 'Carnet de Identidad'),
        (PERSONS_NAME, 'Nombre')
    )
    THEME_INDIGO = 'indigo'
    THEME_PURPLE = 'purple'
    THEME_BLUE = 'blue'
    THEME_DARK = 'black'
    THEME_RED = 'red'
    THEME_YELLOW = 'yellow'
    THEME_GREEN = 'green'
    THEME_CHOICES = (
        (THEME_BLUE, 'Azul'),
        (THEME_DARK, 'Negro'),
        (THEME_GREEN, 'Verde'),
        (THEME_PURPLE, 'Violeta'),
        (THEME_RED, 'Rojo'),
        (THEME_YELLOW, 'Amarillo')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, unique=True)
    enterprise_ordering_by = models.CharField(max_length=30, choices=ENTERPRISE_ORDERING_CHOICES, default=ENTERPRISE_LAST_UPDATE)
    persons_ordering_by = models.CharField(max_length=50, default=PERSONS_IDNUM, choices=PERSON_ORDERING_CHOICES)
    app_color_theme = models.CharField(max_length=10, default=THEME_INDIGO, choices=THEME_CHOICES)

    def __str__(self):
        return str(self.user) + " Cliente por: " + str(self.enterprise_ordering_by) + " Personas por: " + str(self.persons_ordering_by)


class Cliente(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre del Cliente")
    lastname = models.CharField(max_length=50, null=True, verbose_name="Apellidos")
    idnum = models.IntegerField(null=True, verbose_name="Carnet de Identidad", unique=True)
    cogido = models.BooleanField(default=False)
    #Hasta que tengamos pillow
    #signature = models.ImageField(null=True)
    # face = models.ImageField()
    rol = models.ForeignKey('Role', on_delete=models.CASCADE, default=1)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
      return str(self.name) + str(self.lastname) + " " + str(self.rol)

    class Meta:
      ordering = ['idnum']


class Enterprise(models.Model):

  tipo_contratos = (
     ('Suministros', 'Suministros'),
     ('Compraventa CUC', 'Compraventa CUC'),
     ('Compraventa CUP', 'Compraventa CUP'),
  ) 

  enterprise_name = models.CharField(max_length=100, verbose_name='Nombre de la Empresa')
  enterprise_description = models.CharField(max_length=100, null=True, default="Ingrese la descripción de la empresa"
                                                                                 " o algún comentario...",
                                                                                 verbose_name="Descripción")
  has_doubt = models.BooleanField(default=False, verbose_name='Tiene deudas?')
  ammount_of_doubt = models.DecimalField(null=True,decimal_places=2,max_digits=10,default=0)
    # client = models.ManyToManyField(Cliente)
  #  pic = models.ImageField(null=True, blank=True)
  address = models.CharField(null=True, max_length=200, verbose_name='Domicilio Legal')
  phone = models.IntegerField(null=True, verbose_name='Número de Teléfono')
  email = models.EmailField(default="email@empresa.cu",)
  code = models.CharField(null=True, verbose_name='Codigo',max_length=15)
  nit = models.PositiveIntegerField(null=True, verbose_name='NIT')
  bank = models.CharField(null=True, max_length=200, verbose_name='Banco en el que opera')
  bank_address = models.CharField(null=True, max_length=200, verbose_name='Direccion del Banco')
  cup_account = models.IntegerField(null=True, verbose_name='Cuenta en Moneda Nacional')
  cuc_account = models.IntegerField(null=True, verbose_name='Cuenta en CUC')
  commercial_register_cup = models.IntegerField(null=True, verbose_name='Registro Comercial en CUP')
  commercial_register_cuc = models.IntegerField(null=True, verbose_name='Registro Comercial en CUC')
  licence_to_operate_on_divisa = models.CharField(null=True, max_length=20, verbose_name='Licencia para Operar en Divisa')
  contract = models.IntegerField(default=0, verbose_name="Número de Contrato")
  persons = models.ManyToManyField(Cliente, related_name="enterprise",limit_choices_to={'cogido': False})
  last_update = models.DateTimeField(auto_now=True)
  emailed = models.BooleanField(default=False)
  updated = models.BooleanField(default=False, verbose_name="Actualizado?")
  signed = models.DateField(null=True)
  expire_on = models.DateField(null=True)
  type_of_contract = models.CharField(max_length=20, null=True, choices=tipo_contratos)


  def __str__(self):
    return self.enterprise_name

  def save(self, *args, **kwargs):
    self.expire_on = self.signed + timedelta(days=365)
    should_send_email = False
    if self.pk:
      deuda_actual = Enterprise.objects.get(pk=self.pk).ammount_of_doubt
      if self.has_doubt:
        if self.ammount_of_doubt != deuda_actual:
          should_send_email = True
    else:
      should_send_email = self.has_doubt

    if should_send_email:
        mensaje = mensaje = """Hola """ + self.enterprise_name + """este es un mensaje automatico generado por
        la app MisClientes V0.1.\n
        -------------------------------------------------------------
        Se ha insertado una cuenta por pagar envejecida a nuestra Empresa: $""" + str(self.ammount_of_doubt) +""" moneda total.
        Por favor pongase en contacto con nuestro Dpto. Economico en 31 34 30 52 ext 138.
	Por favor, no responda este correo, el mismo es generado por una computadora.
        """
        send_mail("Notificacion", mensaje, "misclientes@pescatun.alinet.cu", [self.email], fail_silently=True)
        self.emailed = True
    super(Enterprise, self).save(*args, **kwargs)

  class Meta:
    ordering = ['-contract']
    verbose_name_plural = "Empresas"
    permissions = (
      ("cambiar_enterprise", "Puede Editar Empresas",),
   )
    get_latest_by = ['contract']

class Role(models.Model):
    rol = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.rol





