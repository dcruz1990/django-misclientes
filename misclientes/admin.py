from django.contrib import admin
from misclientes.models import Cliente, Enterprise, Role, Configuracion

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Enterprise)
admin.site.register(Role)
admin.site.register(Configuracion)


