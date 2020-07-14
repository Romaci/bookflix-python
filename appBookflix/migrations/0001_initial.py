# Generated by Django 2.2.14 on 2020-07-14 17:17

import appBookflix.models
import creditcards.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='mail')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='nombre de usuario')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('confirmo', models.BooleanField(default=False)),
                ('plan', models.CharField(choices=[('free', 'free'), ('normal', 'normal'), ('premium', 'premium'), ('admin', 'admin')], default='free', max_length=8)),
                ('date_start_plan', models.DateField(blank=True, null=True)),
                ('time_pay', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Cuenta',
                'verbose_name_plural': 'Cuentas',
            },
        ),
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('apellido', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='descripcion')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha de creación')),
            ],
            options={
                'verbose_name': 'Autor',
                'verbose_name_plural': 'Autores',
            },
        ),
        migrations.CreateModel(
            name='BookByChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=16, unique=True, validators=[appBookflix.models.validateIsbnPorCapitulo, appBookflix.models.validateIsbnNum])),
                ('title', models.CharField(max_length=50, verbose_name='titulo')),
                ('cant_chapter', models.IntegerField(default=1, verbose_name='Cantidad de capitulos')),
                ('description', models.TextField(blank=True, null=True, verbose_name='descripcion')),
                ('image', models.ImageField(upload_to='portadas_libros', verbose_name='imagen')),
                ('mostrar_en_home', models.BooleanField(default=False)),
                ('on_normal', models.BooleanField(default=False, verbose_name='ver en normal')),
                ('on_premium', models.BooleanField(default=False, verbose_name='ver en premium')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Autor', verbose_name='autor')),
            ],
            options={
                'verbose_name': 'Libro por capítulo',
                'verbose_name_plural': 'Libro por capítulos',
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Ingrese el nombre del capítulo, en caso de no tenerlo, su numero de cap, esta información se mostrará al usuario', max_length=50, verbose_name='Titulo del capítulo')),
                ('number', models.IntegerField(help_text='este dato es solo para ordenar las busquedas internas, sepa que si un libro tiene dos capitulos y aquí pone 10 (en vez de 1) , no afectara al libro, pero en el orden se mostrara al final', validators=[appBookflix.models.numerolegal], verbose_name='numero de capitulo')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción del capítulo')),
                ('pdf', models.FileField(upload_to='pdf')),
                ('active', models.BooleanField(default=False, verbose_name='Activado')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.BookByChapter', verbose_name='libro')),
            ],
            options={
                'verbose_name': 'Capítulo',
                'verbose_name_plural': 'Capítulos',
                'unique_together': {('number', 'book')},
            },
        ),
        migrations.CreateModel(
            name='CommentBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_a_spoiler', models.BooleanField(default=False, verbose_name='es espoiler')),
                ('description', models.TextField(verbose_name='descripcion')),
            ],
            options={
                'verbose_name': 'Comentario libro',
                'verbose_name_plural': 'Comentarios libros',
            },
        ),
        migrations.CreateModel(
            name='CommentBookByChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_a_spoiler', models.BooleanField(default=False, verbose_name='es espoiler')),
                ('description', models.TextField(verbose_name='descripcion')),
            ],
            options={
                'verbose_name': 'Comentario libro por capítulo',
                'verbose_name_plural': 'Comentarios libros por capítulo',
            },
        ),
        migrations.CreateModel(
            name='CreditCardsUsed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', creditcards.models.CardNumberField(max_length=25, verbose_name='numero')),
                ('date_expiration', creditcards.models.CardExpiryField(verbose_name='fecha de vencimiento')),
                ('cod', creditcards.models.SecurityCodeField(max_length=4, verbose_name='codigo de seguridad')),
                ('card_name', models.CharField(max_length=50, verbose_name='nombre de tarjeta')),
                ('bank', models.CharField(max_length=50, verbose_name='banco')),
            ],
            options={
                'verbose_name': 'Tarjeta Usada',
                'verbose_name_plural': 'Tarjetas Usadas',
            },
        ),
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='descripcion')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='')),
            ],
            options={
                'verbose_name': 'Editorial',
                'verbose_name_plural': 'Editoriales',
            },
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='descripcion')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha de creación')),
            ],
            options={
                'verbose_name': 'Género',
                'verbose_name_plural': 'Géneros',
            },
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('isbn', models.CharField(default='', max_length=16, primary_key=True, serialize=False, validators=[appBookflix.models.validateIsbn, appBookflix.models.validateIsbnNum])),
                ('titulo', models.CharField(max_length=100, verbose_name='titulo')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='descripcion')),
                ('portada', models.ImageField(upload_to='portadas_libros', verbose_name='portada')),
                ('mostrar_en_home', models.BooleanField(default=False)),
                ('on_normal', models.BooleanField(default=False, verbose_name='ver en normal')),
                ('on_premium', models.BooleanField(default=False, verbose_name='ver en premium')),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdf')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Autor', verbose_name='autor')),
                ('editorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Editorial')),
                ('genero', models.ManyToManyField(to='appBookflix.Genero', verbose_name='generos')),
            ],
            options={
                'verbose_name': 'Libro',
                'verbose_name_plural': 'Libros',
            },
        ),
        migrations.CreateModel(
            name='MailQueusoPrueba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Novedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='titulo')),
                ('description', models.TextField(blank=True, null=True, verbose_name='descripcion')),
                ('mostrar_en_home', models.BooleanField(default=False)),
                ('imagen', models.ImageField(upload_to='bookflix/static/novedades', verbose_name='imagen')),
                ('video', models.URLField(blank=True, max_length=255, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='autor')),
            ],
            options={
                'verbose_name': 'Novedad',
                'verbose_name_plural': 'Novedades',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='nombre')),
                ('is_active_now', models.BooleanField(default=False, verbose_name='esta activo ahora')),
                ('hour_activation', models.DateTimeField(blank=True, null=True, verbose_name='hora de activacion')),
                ('date_of_creation', models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha de creacion')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='cuenta')),
                ('pleasures_author', models.ManyToManyField(blank=True, null=True, to='appBookflix.Autor', verbose_name='autor')),
                ('pleasures_editorial', models.ManyToManyField(blank=True, null=True, to='appBookflix.Editorial', verbose_name='editorial')),
                ('pleasures_gender', models.ManyToManyField(blank=True, null=True, to='appBookflix.Genero', verbose_name='genero')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
                'unique_together': {('name', 'account')},
            },
        ),
        migrations.CreateModel(
            name='TarjetaQueUsoPrueba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', creditcards.models.CardNumberField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Trailer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='titulo')),
                ('description', models.TextField(blank=True, null=True, verbose_name='descripcion')),
                ('mostrar_en_home', models.BooleanField(default=False)),
                ('video', models.URLField(blank=True, max_length=255, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='autor')),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Libro', verbose_name='libro')),
                ('libro_por_capitulo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appBookflix.BookByChapter', verbose_name='libro por capitulo')),
            ],
            options={
                'verbose_name': 'Trailer',
                'verbose_name_plural': 'Trailers',
            },
        ),
        migrations.CreateModel(
            name='UserSolicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_solicitud', models.CharField(max_length=6, verbose_name='tipo de solicitud')),
                ('type_of_plan', models.CharField(max_length=7, verbose_name='tipo de plan')),
                ('date_of_solicitud', models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha de solicitud')),
                ('is_accepted', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuario')),
            ],
            options={
                'verbose_name': 'Solicitud de usuario',
                'verbose_name_plural': 'Solicitudes de Usuarios',
            },
        ),
        migrations.CreateModel(
            name='UpDownTrailer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 606502, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta')),
                ('expirationl', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 606525, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja')),
                ('trailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Trailer', verbose_name='Publicacion')),
            ],
            options={
                'verbose_name': 'Programar publicación de Trailer',
                'verbose_name_plural': 'Programar publicación de Trailers',
            },
        ),
        migrations.CreateModel(
            name='UpDownNovedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 606054, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta')),
                ('expirationl', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 606077, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja')),
                ('Novedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Novedad', verbose_name='Publicacion')),
            ],
            options={
                'verbose_name': 'Programar publicación de Novedad',
                'verbose_name_plural': 'Programar publicación de Novedades',
            },
        ),
        migrations.CreateModel(
            name='UpDownChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 605510, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeAlta')),
                ('expirationl', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 605533, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='DarDeBaja')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Chapter', verbose_name='Capitulo')),
            ],
            options={
                'verbose_name': 'Programar publicación capítulo',
                'verbose_name_plural': 'Programar publicación capítulos',
            },
        ),
        migrations.CreateModel(
            name='UpDownBookByChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_normal', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 605056, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar publicación')),
                ('expiration_normal', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 605079, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar expiración')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.BookByChapter', verbose_name='libro')),
            ],
            options={
                'verbose_name': 'Programar publicación libro por capítulo',
                'verbose_name_plural': 'Programar publicación libros por capítulo',
            },
        ),
        migrations.CreateModel(
            name='UpDownBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_normal', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 604518, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar publicación')),
                ('expiration_normal', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 604551, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='programar expiración')),
                ('up_premium', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 604569, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='pasar a premium')),
                ('expiration_premium', models.DateField(default=datetime.datetime(2020, 7, 14, 17, 17, 45, 604586, tzinfo=utc), validators=[appBookflix.models.esCorrecto], verbose_name='expiracion premium')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Libro', verbose_name='libro')),
            ],
            options={
                'verbose_name': 'Programar publicación libro',
                'verbose_name_plural': 'Programar publicación libros',
            },
        ),
        migrations.CreateModel(
            name='LikeBookByChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=False, verbose_name='Puntos')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='autor')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.BookByChapter', verbose_name='libro')),
            ],
            options={
                'verbose_name': 'Me gusta libro Por Capitulo',
                'verbose_name_plural': 'Me gusta/s libros por Capitulo',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=False, verbose_name='Puntos')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='autor')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Libro', verbose_name='libro')),
            ],
            options={
                'verbose_name': 'Me gusta libro',
                'verbose_name_plural': 'Me gusta/s libros',
            },
        ),
        migrations.CreateModel(
            name='LibroPorCapituloFavorito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=16, validators=[appBookflix.models.validateIsbn, appBookflix.models.validateIsbnNum])),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appBookflix.BookByChapter', verbose_name='libro')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='perfil')),
            ],
            options={
                'verbose_name': 'Libro por capitulo favorito',
                'verbose_name_plural': 'Libros por capitulos favoritos',
            },
        ),
        migrations.CreateModel(
            name='LibroFavorito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=16, validators=[appBookflix.models.validateIsbn, appBookflix.models.validateIsbnNum])),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Libro', verbose_name='libro')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='perfil')),
            ],
            options={
                'verbose_name': 'Libro favorito',
                'verbose_name_plural': 'Libros favoritos',
            },
        ),
        migrations.CreateModel(
            name='DenunciarComentarioLibroPorCap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.CommentBookByChapter')),
            ],
        ),
        migrations.CreateModel(
            name='DenunciarComentarioLibro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.CommentBook')),
            ],
        ),
        migrations.CreateModel(
            name='CuentaqueUsoPrueba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', creditcards.models.CardNumberField(max_length=25, verbose_name='numero')),
                ('date_expiration', creditcards.models.CardExpiryField(verbose_name='fecha de vencimiento')),
                ('cod', creditcards.models.SecurityCodeField(max_length=4, verbose_name='codigo de seguridad')),
                ('card_name', models.CharField(max_length=50, verbose_name='nombre de tarjeta')),
                ('bank', models.CharField(max_length=50, verbose_name='banco')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuario')),
            ],
            options={
                'verbose_name': 'Tarjeta',
                'verbose_name_plural': 'Tarjetas',
            },
        ),
        migrations.CreateModel(
            name='CounterStates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(verbose_name='fecha de inicio')),
                ('cant_reading', models.IntegerField(default=0, verbose_name='leyendo')),
                ('cant_future_read', models.IntegerField(default=0, verbose_name='en futuras lecturas')),
                ('cant_finished', models.IntegerField(default=0, verbose_name='terminados')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Libro', verbose_name='publicacion')),
            ],
            options={
                'verbose_name': 'Estadística de libro',
                'verbose_name_plural': 'Estadísticas de libros',
            },
        ),
        migrations.AddField(
            model_name='commentbookbychapter',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='perfil'),
        ),
        migrations.AddField(
            model_name='commentbookbychapter',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.BookByChapter', verbose_name='publicacion'),
        ),
        migrations.AddField(
            model_name='commentbook',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='perfil'),
        ),
        migrations.AddField(
            model_name='commentbook',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Libro', verbose_name='publicacion'),
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
        migrations.AddField(
            model_name='bookbychapter',
            name='editorial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Editorial'),
        ),
        migrations.AddField(
            model_name='bookbychapter',
            name='genders',
            field=models.ManyToManyField(to='appBookflix.Genero', verbose_name='generos'),
        ),
        migrations.CreateModel(
            name='StateOfBookByChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='fecha')),
                ('state', models.CharField(blank=True, choices=[('reading', 'leyendo'), ('future_reading', 'futura lectura'), ('finished', 'terminado')], default='finished', max_length=16, null=True, verbose_name='estado')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.BookByChapter', verbose_name='libro')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='perfil')),
            ],
            options={
                'verbose_name': 'Estado del libro por capítulo',
                'verbose_name_plural': 'Estados de libros por capítulo',
                'unique_together': {('book', 'profile')},
            },
        ),
        migrations.CreateModel(
            name='StateOfBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='fecha')),
                ('state', models.CharField(blank=True, choices=[('reading', 'leyendo'), ('future_reading', 'futura lectura'), ('finished', 'terminado')], default='finished', max_length=16, null=True, verbose_name='estado')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Libro', verbose_name='libro')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='perfil')),
            ],
            options={
                'verbose_name': 'Estado del libro',
                'verbose_name_plural': 'Estados del libro',
                'unique_together': {('book', 'profile')},
            },
        ),
        migrations.CreateModel(
            name='LikeCommentBookByChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=False, verbose_name='me gusta')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='autor')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.CommentBookByChapter', verbose_name='comentario')),
            ],
            options={
                'verbose_name': 'Me gusta de comentario',
                'verbose_name_plural': 'Me gustas/s de comentarios',
                'unique_together': {('author', 'comment')},
            },
        ),
        migrations.CreateModel(
            name='LikeCommentBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=False, verbose_name='me gusta')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.Profile', verbose_name='autor')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBookflix.CommentBook', verbose_name='comentario')),
            ],
            options={
                'verbose_name': 'Me gusta de comentario',
                'verbose_name_plural': 'Me gustas/s de comentarios',
                'unique_together': {('author', 'comment')},
            },
        ),
    ]
