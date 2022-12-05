####################################################################
#                MisClientes V 0.0.1                               #
#      By: Luis Miguel Pozo González luis.pozo@nauta.cu            #
#          Dennis Quesada Cruz       dcruz@pescatun.alinet.cu      #
#                                                                  #   
#   Thanks to Ozkar L. Garcell , Guillermo Roig, Feliz Pupo,       #
#   Franger Rodolfo Cuevas, and all the @DjangoCuba members on     # 
#          Telegram                                                #
####################################################################

from django.http import HttpResponse, JsonResponse, HttpRequest
from .models import Cliente, Enterprise, Configuracion, Type_of_Contract
from django.views.generic import DetailView, ListView, FormView
from .forms import ClienteForm, EmpresaForm
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.views import generic
from django.views.generic import View
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views import View
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.utils.timezone import datetime

from django.db.models import Max

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

#from .utils import render_to_pdf
# Create your views here.

from django.utils import decorators



#Vista de Indice ok ayuda

@login_required
def index(request):
    if request.method == 'POST':
        criterio = request.POST['empresa']
        enter = Enterprise.objects.filter(enterprise_name__contains=criterio)
       # personas = Enterprise.objects.get(persons__name__contains=criterio)
        gente = Cliente.objects.filter(name__contains=criterio)
        #Cliente.objects.filter(name__contains=s)
        carnet = Cliente.objects.filter(idnum__contains=criterio)
        code = Enterprise.objects.filter(code__contains=criterio)
        if enter.count() == 0 and carnet.count() == 0 and code.count() ==0 and gente.count() == 0:
            err = True
            return render(request, 'results.html', {'err': err, 'criterio': criterio})
        else:
            return render(request, 'results.html', {'cliente': enter, 'carnets': carnet, 'nit': code, 'gente': gente})
    else:
        ultimo_no_contrato = Enterprise.objects.all().aggregate(Max('contract'))
        total_clientes = Enterprise.objects.all().count()
        total_personas = Cliente.objects.all().count()
        resultado = False
        return render(request, 'index.html', {'result': resultado , 'total': total_clientes, 'personas': total_personas ,'ultimocontrato': ultimo_no_contrato})

# Devuelve un listado con todos los clientes, con paginacion incluida. Ayuda OK		
@method_decorator(login_required, name='dispatch')
class ListaClientesView(generic.ListView):
    template_name = 'empresas.html'
    context_object_name = 'clients_list'
    paginate_by = 10
    
    def get_queryset(self):
        return Enterprise.objects.all()


#Añade personas a los Clientes.
@permission_required('misclientes.add_cliente')
@login_required
def addclient(request):
    form = ClienteForm()
    if request.method == 'POST':
        micliente = ClienteForm(request.POST)
        if micliente.is_valid():
            try:
                micliente.save()
                HttpResponseRedirect('/clientes')
            except IntegrityError:
                error = "Error: Ya existe el carnet"
                return JsonResponse(error, status=400)
                
#Añade nuevos Clientes
@permission_required('misclientes.add_cliente')
@login_required	
def addempresa(request):
    form = EmpresaForm()
    cliform = ClienteForm()
    if request.method == 'POST':
        empresa = EmpresaForm(request.POST)
        if empresa.is_valid():
            nuevaempresa = empresa.save()
            nuevaempresa.persons.update(cogido=True)
            return HttpResponseRedirect('/index/')
        else:
            return render(request, 'addempresa.html', { 'form': empresa })
    else:
        return render(request, 'addempresa.html', { 'clienteform': cliform, 'form': form})

#Borra un Cliente y las personas asociadas		
@permission_required('misclientes.del_cliente')
@login_required		
def deletemodel(request, id):
    b=Enterprise.objects.get( id = id )
    c = b.persons.all()
    c.delete()
    b.delete()
    return HttpResponseRedirect('/clientes/')

#Borra un cliente determinado desde la vista de Detalles del Cliente.
@method_decorator(login_required, name='dispatch')
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "persondelete.html"
    
    def get_success_url(self):
        return reverse('client-detail', kwargs={'pk': self.request.GET.get('redirect_to')})

#Crea un cliente nuevo desde la vista de Detalles del Cliente. Ayuda ok
class ClienteCreateView(CreateView):
    model = Cliente
    template_name = "createperson.html"
    fields = ['name','lastname','idnum','rol']
    
    def form_valid(self, form) :
        empresa = Enterprise.objects.get(pk=self.kwargs['pk'])
        name = form.cleaned_data.get('name')
        lastname = form.cleaned_data.get('lastname')
        idnum = form.cleaned_data.get('idnum')
        role = form.cleaned_data.get('rol')
        nuevocliente = Cliente(name=name,lastname=lastname,idnum=idnum,rol=role)
        nuevocliente.cogido = True
        nuevocliente.save()
        empresa.persons.add(nuevocliente)
        return redirect(self.get_success_url())


    def get_success_url(self):
        return reverse('client-detail', kwargs={'pk': self.request.GET.get('redirect_to')})
      
#Añade personas desde la vista de crear Clientes.    
@method_decorator(login_required, name='dispatch')
class AddPersonaView(FormView):
    form_class = ClienteForm
    template_name = 'addempresa.html'
    success_url = '/addclientes/'

    def form_invalid(self, form):
        response = super(AddPersonaView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AddPersonaView, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            data = {
                'message': "Satisfactoriamente subida"
            }
            return JsonResponse(data)
        else:
            return response

#Detalles de los Clientes
@method_decorator(login_required, name='dispatch')	
class ClienteDetailView(DetailView):
   template_name='cliente_detail.html'
   queryset = Enterprise.objects.all()
   
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = Enterprise.objects.get(pk=self.kwargs['pk'])
        context['personas'] = cliente.persons.all()
        context['tipo_de_contrato'] = cliente.type_of_contract.all()
        return context

#Edita un Cliente		
@method_decorator(login_required, name='dispatch')	  
class EnterpriseUpdate(UpdateView):
    template_name = 'enterprise_update_form.html'
    fields = [
    'enterprise_name',
    'enterprise_description',
    'has_doubt',
    'ammount_of_doubt',
    'address',
    'phone',
    'email',
    'code',
    'nit',
    'bank',
    'bank_address',
    'cup_account',
    'cuc_account',
    'commercial_register_cup',
    'commercial_register_cuc',
    'licence_to_operate_on_divisa',
    'contract',
    'updated',
    'signed',
    'type_of_contract'
    ]
    model= Enterprise
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('client-detail', kwargs={'pk': self.request.GET.get('return_to_enterprise')})


#Edita una persona	  
@method_decorator(login_required, name='dispatch')	  
class ClienteUpdate(UpdateView):
    template_name = 'cliente_update_form.html'
    model = Cliente
    form_class = ClienteForm
    template_name_suffix = '_update_form'  
    
    def get_success_url(self):
        return reverse('client-detail', kwargs={'pk': self.request.GET.get('redirect_to')})


#Detalles de los contratos expirados
@method_decorator(login_required, name='dispatch')	
class ExpiredContracts(generic.ListView):
    template_name = 'expiredContracts.html'
    context_object_name = 'expired_list'
    paginate_by = 10
    
    def get_queryset(self):
        return Enterprise.objects.filter(expire_on__year=datetime.now().year)

#Exporta a pdf la ficha de cliente    
@login_required
def printToPDF(request, pk):
    enterprise = get_object_or_404(Enterprise, pk=pk)
    personas = enterprise.persons.all()
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "attach; filename={name}-ficha-de-cliente.pdf".format(
        name=enterprise.enterprise_name
    )
    html = render_to_string("fichapdf.html", {
        'empresa': enterprise,
        'personas': personas,
    })
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response

#Exporta a pdf todos los clientes
@login_required
def printClientList(request):
    enterprise = Enterprise.objects.all().order_by('contract')
    total_clientes = enterprise.count()
    fecha = datetime.today()
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "attach; filename=Lista-fichas-de-clientes-todos.pdf"
    html = render_to_string("listapdf.html", {
        'empresas': enterprise,
        'fecha': fecha,
        'total': total_clientes,
        
    })
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response

@login_required
def printBuyersList(request):
    enterprise = Enterprise.objects.all().order_by('contract')
    total_clientes = enterprise.count()
    fecha = datetime.today()
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "attach; filename=Lista-fichas-de-compradores-todos.pdf"
    html = render_to_string("listapdfBuyers.html", {
        'empresas': enterprise,
        'fecha': fecha,
        'total': total_clientes,
        
    })
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response



