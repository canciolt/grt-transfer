# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 17:39
from __future__ import unicode_literals

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
            name='Camion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.IntegerField(unique=True, verbose_name='n\xfamero')),
                ('marca', models.CharField(max_length=50, verbose_name='marca')),
                ('modelo', models.IntegerField(verbose_name='modelo')),
                ('serie', models.CharField(max_length=18, unique=True, verbose_name='serie')),
                ('millaje', models.IntegerField(default=0, verbose_name='millaje')),
                ('placa', models.CharField(max_length=8, unique=True, verbose_name='placa')),
                ('tag', models.IntegerField(help_text='N\xfamero de serie Tarjeta de cruze (Ida)', verbose_name='TAG')),
                ('decal', models.IntegerField(help_text='N\xfamero de serie Tarjeta de cruze (Regreso)', verbose_name='DECAL')),
                ('estado', models.CharField(choices=[('0', 'Libre'), ('1', 'Ocupado'), ('2', 'Arrendado')], default=0, help_text='Seleccione el estado (Libre-Ocupado)', max_length=2, verbose_name='estado')),
                ('circulacion', models.CharField(max_length=20, verbose_name='circulaci\xf3n')),
                ('expira_circulacion', models.DateField(verbose_name='vencimiento de circulaci\xf3n')),
            ],
            options={
                'verbose_name': 'Camion',
                'verbose_name_plural': 'Camiones',
            },
        ),
        migrations.CreateModel(
            name='Flujo_Trabajo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('ip', models.GenericIPAddressField()),
                ('modulo', models.CharField(max_length=250)),
                ('navegador', models.CharField(max_length=250)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inspeccion_Camion_US',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('inspeccion', models.CharField(max_length=20, verbose_name='inspecci\xf3n')),
                ('expira', models.DateField(unique=True, verbose_name='vencimiento de inspecci\xf3n')),
                ('camion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Camion')),
            ],
        ),
        migrations.CreateModel(
            name='Multas_Camion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_multa', models.DateTimeField(verbose_name='fecha de multa')),
                ('numero', models.IntegerField(unique=True, verbose_name='n\xfamero de multa')),
                ('importe', models.FloatField(verbose_name='importe de multa')),
                ('descripcion', models.TextField(verbose_name='Motivo de la multa')),
                ('expira', models.DateField(verbose_name='Vigencia de la Multa')),
                ('grua', models.CharField(blank=True, max_length=25, verbose_name='grua')),
                ('importe_grua', models.FloatField(default=0, verbose_name='importe de grua')),
                ('estado', models.BooleanField(choices=[(0, 'Pendiente de pago'), (1, 'Pagado')], default=0, verbose_name='estado de la multa')),
                ('camion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Camion', verbose_name='camion')),
            ],
        ),
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, verbose_name='nombre')),
                ('direccion', models.CharField(max_length=50, verbose_name='direcci\xf3n')),
                ('colonia', models.CharField(choices=[('150 Aniversario', '150 Aniversario'), ('Primero de Mayo', 'Primero de Mayo'), ('20 de Noviembre', '20 de Noviembre'), ('Agronomos', 'Agronomos'), ('Alfonso Gutierrez', 'Alfonso Gutierrez'), ('Alianza Para La Produccion', 'Alianza Para La Produccion'), ('Alijadores', 'Alijadores'), ('Altavista', 'Altavista'), ('America 1', 'America 1'), ('America 2', 'America 2'), ('America 3', 'America 3'), ('America 4', 'America 4'), ('America 5', 'America 5'), ('America 6', 'America 6'), ('America 7', 'America 7'), ('America 8', 'America 8'), ('America 9', 'America 9'), ('America 10', 'America 10'), ('America 11', 'America 11'), ('America 12', 'America 12'), ('Americo Villarreal Guerra', 'Americo Villarreal Guerra'), ('Ampliaci\xf3n Tercer Milenio', 'Ampliaci\xf3n Tercer Milenio'), ('Anahuac', 'Anahuac'), ('Anahuac Sur', 'Anahuac Sur'), ('Anexo Reforma Urbana', 'Anexo Reforma Urbana'), ('Arturo Cortes Villada', 'Arturo Cortes Villada'), ('Ayuntamiento 77', 'Ayuntamiento 77'), ('Balcones del Boulevard', 'Balcones del Boulevard'), ('Balcones del Valle', 'Balcones del Valle'), ('Bellavista', 'Bellavista'), ('Bertha de Avellano', 'Bertha de Avellano'), ('Blanca Navidad', 'Blanca Navidad'), ('Bonanza', 'Bonanza'), ('Bosques del Sur', 'Bosques del Sur'), ('Buenavista', 'Buenavista'), ('Buenos Aires', 'Buenos Aires'), ('Burocratas', 'Burocratas'), ('Campesina', 'Campesina'), ('Campestre', 'Campestre'), ('Candelario Perales', 'Candelario Perales'), ('Carlos Benjamin Galvan Maytorera', 'Carlos Benjamin Galvan Maytorera'), ('Casa Linda', 'Casa Linda'), ('Central 2000', 'Central 2000'), ('Central de Carga', 'Central de Carga'), ('Centro Comercial Reforma', 'Centro Comercial Reforma'), ('Cereso', 'Cereso'), ('Claudette', 'Claudette'), ('Club Campestre Ribera del Bravo', 'Club Campestre Ribera del Bravo'), ('Club de Leones', 'Club de Leones'), ('Cnop', 'Cnop'), ('Colinas Del Sur Oriente', 'Colinas Del Sur Oriente'), ('Colinas Del Sur Poniente', 'Colinas Del Sur Poniente'), ('Colinas de San Javier', 'Colinas de San Javier'), ('Colorines', 'Colorines'), ('Concordia', 'Concordia'), ('Constitucional', 'Constitucional'), ('Cuartel Militar Macario Zamora', 'Cuartel Militar Macario Zamora'), ('Daniel Covarrubias', 'Daniel Covarrubias'), ('Del Maestro', 'Del Maestro'), ('Del Valle', 'Del Valle'), ('Don Ramon Salcido', 'Don Ramon Salcido'), ('Eden Country Villas', 'Eden Country Villas'), ('El Bayito', 'El Bayito'), ('El Campanario', 'El Campanario'), ('El Caporal', 'El Caporal'), ('El Capulin', 'El Capulin'), ('El Caracol', 'El Caracol'), ('El Cortijo', 'El Cortijo'), ('Electricistas', 'Electricistas'), ('El Ed\xe9n', 'El Ed\xe9n'), ('El Frances y Buenos Aires', 'El Frances y Buenos Aires'), ('El Nogal', 'El Nogal'), ('El Pedregal Residencial', 'El Pedregal Residencial'), ('El Progreso', 'El Progreso'), ('El Remolino', 'El Remolino'), ('El Rio', 'El Rio'), ('El Triunfo', 'El Triunfo'), ('Emiliano Zapata', 'Emiliano Zapata'), ('Endulzadora PEMEX', 'Endulzadora PEMEX'), ('Enrique Cardenas Gonzalez', 'Enrique Cardenas Gonzalez'), ('Ferrocarril', 'Ferrocarril'), ('Ferrocarrilera', 'Ferrocarrilera'), ('FOVISSSTE Benito Juarez', 'FOVISSSTE Benito Juarez'), ('FOVISSSTE Las Alazanas', 'FOVISSSTE Las Alazanas'), ('Francisco Villa', 'Francisco Villa'), ('Francisco Villa 2', 'Francisco Villa 2'), ('Gilberto Montemayor Quintanilla', 'Gilberto Montemayor Quintanilla'), ('Gonzalez', 'Gonzalez'), ('Gran Boulevard', 'Gran Boulevard'), ('Granjas Economicas 1', 'Granjas Economicas 1'), ('Granjas Economicas 2', 'Granjas Economicas 2'), ('Granjas Guzman', 'Granjas Guzman'), ('Granjas Regina', 'Granjas Regina'), ('Granjas Trevino', 'Granjas Trevino'), ('Guerrero', 'Guerrero'), ('Guerreros Del Sol', 'Guerreros Del Sol'), ('Hacienda de La Concordia', 'Hacienda de La Concordia'), ('Hacienda J. Longoria', 'Hacienda J. Longoria'), ('Haciendas de San Agustin', 'Haciendas de San Agustin'), ('Hidalgo', 'Hidalgo'), ('Hipodromo', 'Hipodromo'), ('Independencia', 'Independencia'), ('INFONAVIT Benito Juarez', 'INFONAVIT Benito Juarez'), ('INFONAVIT Fundadores', 'INFONAVIT Fundadores'), ('Insurgentes', 'Insurgentes'), ('Itavu', 'Itavu'), ('Jardan', 'Jardan'), ('Jardines de la Hacienda', 'Jardines de la Hacienda'), ('Jardan Juvencia', 'Jardan Juvencia'), ('Jesus Garcia', 'Jesus Garcia'), ('Juarez', 'Juarez'), ('Junta Federal de Mejoras Materiales', 'Junta Federal de Mejoras Materiales'), ('La Concordia', 'La Concordia'), ('La Cruz', 'La Cruz'), ('La Esperanza', 'La Esperanza'), ('La Fe', 'La Fe'), ('Lagos', 'Lagos'), ('La Joya', 'La Joya'), ('La Paz', 'La Paz'), ('Las Alamedas', 'Las Alamedas'), ('Las Alazanas', 'Las Alazanas'), ('La Sandia', 'La Sandia'), ('Las Arboledas', 'Las Arboledas'), ('Las Cumbres', 'Las Cumbres'), ('Las Flores', 'Las Flores'), ('Las Lomas', 'Las Lomas'), ('Las Piedritas', 'Las Piedritas'), ('Las Torres', 'Las Torres'), ('Las Vi\xf1as', 'Las Vi\xf1as'), ('Lic. Daniel Hernandez Isais', 'Lic. Daniel Hernandez Isais'), ('Lic. Luis Donaldo Colosio', 'Lic. Luis Donaldo Colosio'), ('Loma Bonita', 'Loma Bonita'), ('Lomas del Poniente', 'Lomas del Poniente'), ('Lomas Del Popo', 'Lomas Del Popo'), ('Lomas Del Rey', 'Lomas Del Rey'), ('Lomas Del Rio', 'Lomas Del Rio'), ('Lomas del Rosario', 'Lomas del Rosario'), ('Los Agaves', 'Los Agaves'), ('Los Alamos', 'Los Alamos'), ('Los Angeles', 'Los Angeles'), ('Los Arcos', 'Los Arcos'), ('Los Artistas', 'Los Artistas'), ('Los Aztecas', 'Los Aztecas'), ('Los Cantaros', 'Los Cantaros'), ('Los Cerezos', 'Los Cerezos'), ('Los Ciruelos', 'Los Ciruelos'), ('Los Encinos', 'Los Encinos'), ('Los Fresnos', 'Los Fresnos'), ('Los Garza', 'Los Garza'), ('Los Olivos', 'Los Olivos'), ('Los Presidentes', 'Los Presidentes'), ('Los Sanchez', 'Los Sanchez'), ('Los Virreyes', 'Los Virreyes'), ('Maclovio Herrera', 'Maclovio Herrera'), ('Madero', 'Madero'), ('Manuel Cavazos Lerma', 'Manuel Cavazos Lerma'), ('Manuel Martinez Mendez', 'Manuel Martinez Mendez'), ('Maria Del Pilar Martinez Munoz', 'Maria Del Pilar Martinez Munoz'), ('Maria Luisa', 'Maria Luisa'), ('Matamoros', 'Matamoros'), ('Mexico', 'Mexico'), ('Dr Mier', 'Dr Mier'), ('Miguel Aleman', 'Miguel Aleman'), ('Militar', 'Militar'), ('Mirador', 'Mirador'), ('Mision de San Mauricio', 'Mision de San Mauricio'), ('Morelos', 'Morelos'), ('Naciones Unidas', 'Naciones Unidas'), ('Nueva Era', 'Nueva Era'), ('Nueva Espana', 'Nueva Espana'), ('Nueva Victoria', 'Nueva Victoria'), ('Centro', 'Centro'), ('Quetzalcoatl', 'Quetzalcoatl'), ('Nuevo Milenio', 'Nuevo Milenio'), ('Ojo Caliente', 'Ojo Caliente'), ('Othon Chavez', 'Othon Chavez'), ('Palacios', 'Palacios'), ('Palmares', 'Palmares'), ('2 Laredos', '2 Laredos'), ('FINSA', 'FINSA'), ('Longoria', 'Longoria'), ('Oradel', 'Oradel'), ('Rio Bravo', 'Rio Bravo'), ('Rio Grande', 'Rio Grande'), ('Americas', 'Americas'), ('Pavorreales', 'Pavorreales'), ('Pedregal', 'Pedregal'), ('Pe\xf1a Benavides', 'Pe\xf1a Benavides'), ('Postal', 'Postal'), ('Praderas del Mezquital', 'Praderas del Mezquital'), ('Privanzas Sector Alameda', 'Privanzas Sector Alameda'), ('Recinto Fiscal', 'Recinto Fiscal'), ('Reforma Urbana', 'Reforma Urbana'), ('Reservas Territoriales', 'Reservas Territoriales'), ('Residencial Longoria', 'Residencial Longoria'), ('Riberas del Bravo', 'Riberas del Bravo'), ('Roma', 'Roma'), ('Rosita', 'Rosita'), ('San Andres', 'San Andres'), ('Saneva', 'Saneva'), ('San Jose', 'San Jose'), ('San Patricio', 'San Patricio'), ('San Rafael', 'San Rafael'), ('Santa Anita', 'Santa Anita'), ('Santa Cecilia', 'Santa Cecilia'), ('Santa Elena', 'Santa Elena'), ('Santa Martha', 'Santa Martha'), ('Santiago M. Belden', 'Santiago M. Belden'), ('Sistema de Agua y Saneamiento', 'Sistema de Agua y Saneamiento'), ('Sistema Merlin', 'Sistema Merlin'), ('Solidaridad', 'Solidaridad'), ('SUTERM I', 'SUTERM I'), ('SUTERM II', 'SUTERM II'), ('Tamaulipas', 'Tamaulipas'), ('Tercer Milenio', 'Tercer Milenio'), ('Tinajitas', 'Tinajitas'), ('Toboganes', 'Toboganes'), ('Tulipanes', 'Tulipanes'), ('Unidad Nacional', 'Unidad Nacional'), ('Union', 'Union'), ('Union Del Recuerdo', 'Union Del Recuerdo'), ('Valle Dorado', 'Valle Dorado'), ('Valle Elizondo', 'Valle Elizondo'), ('Valle Real', 'Valle Real'), ('Valles de Anahuac', 'Valles de Anahuac'), ('Valles del Paraiso', 'Valles del Paraiso'), ('Vamos Tamaulipas', 'Vamos Tamaulipas'), ('Vamos Tamaulipas', 'Vamos Tamaulipas'), ('Vicente Mendoza', 'Vicente Mendoza'), ('Victoria', 'Victoria'), ('Villa Del Lago', 'Villa Del Lago'), ('Villas de la Concordia', 'Villas de la Concordia'), ('Villas de La Fe', 'Villas de La Fe'), ('Villas del Oradel', 'Villas del Oradel'), ('Villas del Progreso', 'Villas del Progreso'), ('Villas Del Sol', 'Villas Del Sol'), ('Villas de San Francisco', 'Villas de San Francisco'), ('Villas de San Miguel', 'Villas de San Miguel'), ('Vista Hermosa', 'Vista Hermosa'), ('Viveros', 'Viveros'), ('Viviendas Unidas', 'Viviendas Unidas'), ('Voluntad y Trabajo', 'Voluntad y Trabajo'), ('Zaragoza', 'Zaragoza'), ('Zona de Tolerancia', 'Zona de Tolerancia')], max_length=20, verbose_name='colonia')),
                ('ciudad', models.CharField(max_length=20, verbose_name='ciudad')),
                ('pasaporte', models.CharField(max_length=15, verbose_name='pasaporte')),
                ('telefono', models.CharField(blank=True, max_length=10, verbose_name='tel\xe9fono')),
                ('radio', models.CharField(blank=True, max_length=12, verbose_name='radio')),
                ('celular', models.CharField(blank=True, max_length=10, verbose_name='celular')),
                ('estatus', models.BooleanField(default=True, verbose_name='estado')),
                ('nss', models.CharField(max_length=30, verbose_name='seguro social')),
                ('curp', models.CharField(max_length=30, verbose_name='CURP')),
                ('rfc', models.CharField(max_length=30, verbose_name='registro de contribuyentes')),
                ('visa', models.CharField(max_length=15, verbose_name='visa')),
                ('visa_expira', models.DateField(verbose_name='vencimiento de visa')),
                ('fast', models.CharField(max_length=15, verbose_name='cruse FAST')),
                ('fast_expira', models.DateField(verbose_name='vencimiento de FAST')),
                ('licencia', models.CharField(max_length=25, verbose_name='licencia')),
                ('licencia_expira', models.DateField(verbose_name='vencimiento de licencia')),
                ('medico', models.CharField(max_length=25, verbose_name='seguro medico')),
                ('medico_expira', models.DateField(verbose_name='vencimiento de seguro medico')),
                ('camion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.Camion')),
            ],
        ),
        migrations.CreateModel(
            name='Orden_Reparacion_Camion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=255, verbose_name='descripcion')),
                ('tipo', models.CharField(choices=[('P', 'Cambio de Pieza'), ('MO', 'Mano de obra')], max_length=2, verbose_name='tipo de Reparacion')),
                ('cantidad', models.IntegerField(verbose_name='cantida')),
                ('provedor', models.CharField(max_length=150, verbose_name='provedor')),
                ('factura', models.CharField(max_length=17, verbose_name='factura')),
                ('costo_r_mx', models.FloatField(verbose_name='Costo MX')),
                ('costo_r_usd', models.FloatField(verbose_name='Costo US')),
                ('tipo_pago', models.CharField(choices=[('E', 'Efectivo'), ('CH', 'Cheque')], max_length=2, verbose_name='tipo de pago')),
            ],
        ),
        migrations.CreateModel(
            name='Reparacion_Camion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateTimeField(verbose_name='fecha de inicio')),
                ('fecha_fin', models.DateTimeField(verbose_name='fecha de terminaci\xf3n')),
                ('rotura', models.CharField(max_length=255, verbose_name='rotura')),
                ('costo_usd', models.FloatField(verbose_name='costo USD')),
                ('costo_mx', models.FloatField(verbose_name='costo MX')),
                ('estado', models.BooleanField(default=False, help_text='Seleccione el estado (Iniciada-Terminada)', verbose_name='estado reparaci\xf3n')),
                ('detecto_fecha', models.DateTimeField(verbose_name='fecha de detecci\xf3n')),
                ('supervisor_fecha', models.DateTimeField(verbose_name='fecha de supervici\xf3n')),
                ('autorizo_fecha', models.DateTimeField(verbose_name='fecha de autorizaci\xf3n')),
                ('autorizo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='autorizo_user', to=settings.AUTH_USER_MODEL, verbose_name='Autorizo')),
                ('camion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Camion', verbose_name='camion')),
                ('detecto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system.Operador', verbose_name='Detector de rotura')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supervisor_user', to=settings.AUTH_USER_MODEL, verbose_name='Supervisor')),
            ],
        ),
        migrations.CreateModel(
            name='Seguromx_Camion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('seguromx', models.CharField(max_length=20, verbose_name='seguro MX')),
                ('expira_seguromx', models.DateField(verbose_name='vencimiento de seguro MX')),
                ('camion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='smx_camion', to='system.Camion')),
            ],
        ),
        migrations.CreateModel(
            name='Segurous_Camion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('segurous', models.CharField(max_length=20, verbose_name='seguro US')),
                ('expira_segurous', models.DateField(verbose_name='vencimiento de seguro US')),
                ('camion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sus_camion', to='system.Camion')),
            ],
        ),
        migrations.CreateModel(
            name='Ubicacion_Camion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ubicacion', models.CharField(max_length=10)),
                ('fecha', models.DateTimeField()),
                ('camion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uc_camion', to='system.Camion')),
            ],
        ),
        migrations.CreateModel(
            name='Verificacion_Camion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('verificacion', models.CharField(max_length=20, verbose_name='verificaci\xf3n')),
                ('expira', models.DateField(unique=True, verbose_name='vencimiento de verificaci\xf3n')),
                ('camion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Camion')),
            ],
            options={
                'verbose_name': 'verificaci\xf3n camion',
                'verbose_name_plural': 'verificaci\xf3n camion',
            },
        ),
        migrations.AddField(
            model_name='orden_reparacion_camion',
            name='reparacion_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Reparacion_Camion', verbose_name='reparaci\xf3n ID'),
        ),
    ]