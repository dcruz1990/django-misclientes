# Generated by Django 3.0.8 on 2020-07-02 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre del Cliente')),
                ('lastname', models.CharField(max_length=50, null=True, verbose_name='Apellidos')),
                ('idnum', models.IntegerField(null=True, unique=True, verbose_name='Carnet de Identidad')),
                ('cogido', models.BooleanField(default=False)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['idnum'],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enterprise_name', models.CharField(max_length=100, verbose_name='Nombre de la Empresa')),
                ('enterprise_description', models.CharField(default='Ingrese la descripción de la empresa o algún comentario...', max_length=100, null=True, verbose_name='Descripción')),
                ('has_doubt', models.BooleanField(default=False, verbose_name='Tiene deudas?')),
                ('ammount_of_doubt', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('address', models.CharField(max_length=200, null=True, verbose_name='Domicilio Legal')),
                ('phone', models.IntegerField(null=True, verbose_name='Número de Teléfono')),
                ('email', models.EmailField(default='email@empresa.cu', max_length=254)),
                ('code', models.CharField(max_length=15, null=True, verbose_name='Codigo')),
                ('nit', models.PositiveIntegerField(null=True, verbose_name='NIT')),
                ('bank', models.CharField(max_length=200, null=True, verbose_name='Banco en el que opera')),
                ('bank_address', models.CharField(max_length=200, null=True, verbose_name='Direccion del Banco')),
                ('cup_account', models.IntegerField(null=True, verbose_name='Cuenta en Moneda Nacional')),
                ('cuc_account', models.IntegerField(null=True, verbose_name='Cuenta en CUC')),
                ('commercial_register_cup', models.IntegerField(null=True, verbose_name='Registro Comercial en CUP')),
                ('commercial_register_cuc', models.IntegerField(null=True, verbose_name='Registro Comercial en CUC')),
                ('licence_to_operate_on_divisa', models.CharField(max_length=20, null=True, verbose_name='Licencia para Operar en Divisa')),
                ('contract', models.IntegerField(default=0, verbose_name='Número de Contrato')),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('emailed', models.BooleanField(default=False)),
                ('updated', models.BooleanField(default=False, verbose_name='Actualizado?')),
                ('signed', models.DateField(null=True)),
                ('expire_on', models.DateField(null=True)),
                ('type_of_contract', models.CharField(choices=[('Suministros', 'Suministros'), ('Compraventa CUC', 'Compraventa CUC'), ('Compraventa CUP', 'Compraventa CUP')], max_length=20, null=True)),
                ('persons', models.ManyToManyField(limit_choices_to={'cogido': False}, related_name='enterprise', to='misclientes.Cliente')),
            ],
            options={
                'verbose_name_plural': 'Empresas',
                'ordering': ['-contract'],
                'permissions': (('cambiar_enterprise', 'Puede Editar Empresas'),),
                'get_latest_by': ['contract'],
            },
        ),
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enterprise_ordering_by', models.CharField(choices=[('code', 'Codigo REUP'), ('last_update', 'Fecha de actualizacion'), ('enterprise_name', 'Nombre del Cliente'), ('nit', 'NIT')], default='last_update', max_length=30)),
                ('persons_ordering_by', models.CharField(choices=[('lastname', 'Apellidos'), ('idnum', 'Carnet de Identidad'), ('name', 'Nombre')], default='idnum', max_length=50)),
                ('app_color_theme', models.CharField(choices=[('blue', 'Azul'), ('black', 'Negro'), ('green', 'Verde'), ('purple', 'Violeta'), ('red', 'Rojo'), ('yellow', 'Amarillo')], default='indigo', max_length=10)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='rol',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='misclientes.Role'),
        ),
    ]
