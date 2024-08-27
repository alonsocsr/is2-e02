# Generated by Django 5.1 on 2024-08-24 23:52

from django.db import migrations, models

    
class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_rol', models.CharField(max_length=25, unique=True, verbose_name='Roles del Sistema')),
                ('rol_por_defecto', models.BooleanField(default=False)),
                ('descripcion', models.TextField(blank=True, max_length=50)),
                ('permisos', models.ManyToManyField(blank=True, to='auth.permission')),
            ],
            options={
                'permissions': [('crear_contenido', 'Crear Contenido'), ('visualizar_contenido', 'Visualizar Contenido'), ('editar_contenido', 'Editar Contenido'), ('publicar_contenido', 'Publicar Contenido'), ('rechazar_contenido', 'Rechazar Contenido'), ('categoria_no_moderada', 'Categoria No Moderada'), ('inactivar_contenido', 'Inactivar Contenido'), ('cambiar_estado_contenido', 'Cambiar Estado Contenido'), ('crear_rol', 'Crear Rol'), ('modificar_rol', 'Modificar Rol'), ('asignar_rol', 'Asignar Rol'), ('remover_rol', 'Modificar Rol'), ('eliminar_rol', 'Eliminar Rol'), ('crear_categoria', 'Crear Categoria'), ('modificar_categoria', 'Modificar Categoria'), ('eliminar_categoria', 'Eliminar Categoria'), ('inactivar_categoria', 'Inactivar Categoria'), ('acceder_a_categoria_paga', 'Acceder a Categoria Paga'), ('acceder_a_categoria_free', 'Acceder a Categoria Free'), ('editar_perfil', 'Editar Perfil'), ('suspender_cuenta', 'Suspender Cuenta'), ('ver_tablero_kanban', 'Ver Tablero Kanban'), ('modificar_tablero_kanban', 'Modificar Tablero Kanban'), ('ver_reportes_contenido', 'Ver Reportes de Contenido'), ('ver_estadisticas_contenido', 'Ver Estadisticas de Contenido'), ('ver_cantidad_likes', 'Ver Cantidad de Likes'), ('ver_cantidad_dislikes', 'Ver Cantidad de Dislikes'), ('ver_cantidad_visualizaciones', 'Ver Cantidad de visualizaciones'), ('ver_cantidad_compartidos', 'Ver Cantidad de Compartidos'), ('comentar_contenido', 'Comentar Contenido'), ('eliminar_contenido', 'Eliminar Contenido'), ('reportar_contenido', 'Reportar Contenido'), ('compartir_contenido', 'Compartir Contenido'), ('filtrar_por_categoria', 'Filtrar por Categoria'), ('filtrar_por_autor', 'Filtrar por Autor'), ('filtrar_por_tags', 'Filtrar por Tags'), ('modificar_estado_contenido', 'Modificar Estado de Contenido'), ('administrar_estado_contenido', 'Administrar Estado de Contenido'), ('eliminar_estado_contenido', 'Eliminar Estado de Contenido'), ('visualizar_versiones_contenido', 'Visualizar versiones de Contenido'), ('restaurar_verisiones_contenido', 'Restaurar Versiones de Contenido')],
            },
        ),
    ]