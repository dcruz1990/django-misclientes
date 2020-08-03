from django.contrib import admin
from misclientes.models import Cliente, Enterprise, Role, Configuracion, Type_of_Contract

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Enterprise)
admin.site.register(Role)
admin.site.register(Configuracion)
admin.site.register(Type_of_Contract)


