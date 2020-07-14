# Generated by Django 3.0.7 on 2020-07-13 23:59

import appBookflix.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appBookflix', '0006_auto_20200713_1557'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='updownbook',
            options={'verbose_name': 'Programar publicación libro', 'verbose_name_plural': 'Programar publicación libros'},
        ),
        migrations.AlterModelOptions(
            name='updownbookbychapter',
            options={'verbose_name': 'Programar publicación libro por capítulo', 'verbose_name_plural': 'Programar publicación libros por capítulo'},
        ),
        migrations.AlterModelOptions(
            name='updownchapter',
            options={'verbose_name': 'Programar publicación capítulo', 'verbose_name_plural': 'Programar publicación capítulos'},
        ),
        migrations.AlterModelOptions(
            name='updownnovedad',
            options={'verbose_name': 'Programar publicación de Novedad', 'verbose_name_plural': 'Programar publicación de Novedades'},
        ),
        migrations.AlterModelOptions(
            name='updowntrailer',
            options={'verbose_name': 'Programar publicación de Trailer', 'verbose_name_plural': 'Programar publicación de Trailers'},
        ),
        migrations.RemoveField(
            model_name='updownbookbychapter',
            name='expiration_premium',
        ),
        migrations.RemoveField(
            model_name='updownbookbychapter',
            name='up_premium',
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='expiration_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar expiración'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='expiration_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion premium'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='up_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar publicación'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='up_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a premium'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='expiration_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar expiración'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='up_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar publicación'),
        ),
        migrations.AlterField(
            model_name='updownchapter',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updownchapter',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
        migrations.AlterField(
            model_name='updownnovedad',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updownnovedad',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
        migrations.AlterField(
            model_name='updowntrailer',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updowntrailer',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 13, 23, 59, 19, 614468, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
    ]