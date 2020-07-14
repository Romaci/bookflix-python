# Generated by Django 3.0.7 on 2020-07-11 20:30

import appBookflix.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appBookflix', '0003_auto_20200711_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updownbook',
            name='expiration_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 984163, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion normal'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='expiration_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 984163, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion premium'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='up_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 984163, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a normal'),
        ),
        migrations.AlterField(
            model_name='updownbook',
            name='up_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 984163, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a premium'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='expiration_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 984163, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion normal'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='expiration_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 984163, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion premium'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='up_normal',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 984163, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a normal'),
        ),
        migrations.AlterField(
            model_name='updownbookbychapter',
            name='up_premium',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 984163, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a premium'),
        ),
        migrations.AlterField(
            model_name='updownchapter',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 984163, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updownchapter',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 984163, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
        migrations.AlterField(
            model_name='updownnovedad',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 994373, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updownnovedad',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 994355, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
        migrations.AlterField(
            model_name='updowntrailer',
            name='expirationl',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 994373, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja'),
        ),
        migrations.AlterField(
            model_name='updowntrailer',
            name='up',
            field=models.DateField(default=datetime.datetime(2020, 7, 11, 20, 30, 53, 994373, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta'),
        ),
        migrations.CreateModel(
            name='CapituloFavorito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo_capitulo', models.CharField(max_length=50, verbose_name='titulo')),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appBookflix.BookByChapter', verbose_name='libro')),
                ('capitulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Chapter')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='perfil')),
            ],
            options={
                'verbose_name': 'Capitulo Leyéndose',
                'verbose_name_plural': 'Capitulos Leyéndose',
            },
        ),
    ]