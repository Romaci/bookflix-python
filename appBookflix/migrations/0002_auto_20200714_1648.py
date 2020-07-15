# Generated by Django 3.0.7 on 2020-07-14 19:48

import appBookflix.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appBookflix', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='novedad',
            options={'verbose_name': 'Noticia', 'verbose_name_plural': 'Noticias'},
        ),
        migrations.AlterField(
            model_name='novedad',
            name='imagen',
            field=models.ImageField(upload_to='novedades', verbose_name='imagen'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='expiration_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 106937, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar expiración'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='expiration_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 106937, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion premium'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='up_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 106937, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar publicación'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='up_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 106937, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a premium'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='expiration_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 107939, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar expiración'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='up_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 107939, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar publicación'),
        ),
        migrations.AlterField(
            model_name='updownchapter',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 108939, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updownchapter',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 108939, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
        migrations.AlterField(
            model_name='updownnovedad',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 108939, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updownnovedad',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 108939, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
        migrations.AlterField(
            model_name='updowntrailer',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 109940, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updowntrailer',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 19, 48, 33, 109940, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
    ]