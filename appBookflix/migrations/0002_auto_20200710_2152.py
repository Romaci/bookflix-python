# Generated by Django 2.2.14 on 2020-07-10 21:52

import appBookflix.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appBookflix', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updownbook',
            name='expiration_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 658585, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion normal'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='expiration_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 658621, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion premium'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='up_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 658552, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a normal'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='up_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 658604, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a premium'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='expiration_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 659095, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion normal'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='expiration_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 659133, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion premium'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='up_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 659072, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a normal'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='up_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 659116, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a premium'),
        ),
        migrations.AlterField(
            model_name='updownchapter',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 659625, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updownchapter',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 659600, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
        migrations.AlterField(
            model_name='updownnovedad',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 660081, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updownnovedad',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 660058, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
        migrations.AlterField(
            model_name='updowntrailer',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 660530, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updowntrailer',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 21, 52, 16, 660507, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
    ]
