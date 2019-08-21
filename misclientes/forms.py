from misclientes.models import Cliente, Enterprise, Role
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelChoiceField


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['name', 'lastname', 'idnum', 'rol', 'cogido' ]
        widgets = {
            'name': forms.TextInput(attrs={'type':'text', 'class':'validate'}),
            'idnum': forms.TextInput(attrs={'data-length': 11}),
            #'enterprise': forms.ModelChoiceField(Enterprise)
            'cogido': forms.HiddenInput()
        }

    def clean_idnum(self):
        idnum = self.cleaned_data.get("idnum")
        if len(str(idnum)) != 11:
            raise forms.ValidationError("El carnet debe tener 11 digitos")
        else:
            return idnum



WidgetTexto = forms.TextInput()	
WidgetTelefono = forms.TextInput()
		
		
class EmpresaForm(ModelForm):
    
    #persons = ModelChoiceField(queryset=Cliente.objects.filter(cogido=False) )
    class Meta:
        model = Enterprise
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
                 'persons',
		 'updated',
                             ]
     #   field_classes = {
     #       'persons': ModelChoiceField(queryset=Cliente.objects.filter(cogido=False), *args)
     #   }
        widgets = {
            'ammount_of_doubt': forms.TextInput(attrs={ 'style': 'display: none', 'class': 'validate' }),
            'nit': WidgetTexto,
            'phone': forms.TextInput(attrs={'class': 'validate' }),
            'code': forms.TextInput(attrs={'class': 'validate' }),
            'cup_account': forms.TextInput(attrs={'class': 'validate' }),
			'commercial_register_cup': forms.TextInput(attrs={'class': 'validate' }),
			'commercial_register_cuc': forms.TextInput(attrs={'class': 'validate' }),
			'enterprise_name': WidgetTexto,
			'enterprise_description': WidgetTexto,
			'address': WidgetTexto,
			'email': WidgetTexto,
			'bank': WidgetTexto,
			'bank_address': WidgetTexto,
			'cuc_account': WidgetTexto,
			'licence_to_operate_on_divisa': WidgetTexto,
			'contract': WidgetTexto,
			'cuc_account': WidgetTexto,
                   

        }

        
