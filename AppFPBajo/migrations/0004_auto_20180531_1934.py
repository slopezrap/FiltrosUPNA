# Generated by Django 2.0.4 on 2018-05-31 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFPBajo', '0003_filtro_butterworth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelofpbajo',
            name='imagePlantilla',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Imagen Plantilla'),
        ),
    ]