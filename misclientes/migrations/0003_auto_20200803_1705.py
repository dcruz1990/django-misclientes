# Generated by Django 3.0.8 on 2020-08-03 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misclientes', '0002_auto_20200803_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='type_of_contract',
            field=models.ManyToManyField(max_length=20, to='misclientes.Type_of_Contract'),
        ),
    ]
