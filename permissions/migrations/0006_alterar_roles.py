from django.db import migrations

def create_roles_and_groups(apps, schema_editor):
   
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    Roles = apps.get_model('permissions', 'Roles')  


    roles_predeterminados = [
        {
            'nombre_rol': 'Financiero',
            'rol_por_defecto': True,
            'descripcion': 'Rol para monitorear los pagos realizados en el CMS',
            'permisos': ['visualizar_contenido', 'editar_perfil', 'ver_historial_compras']
        },
     
    ]


    for rol_data in roles_predeterminados:
   
        rol, created = Roles.objects.get_or_create(
            nombre_rol=rol_data['nombre_rol'],
            rol_por_defecto=rol_data['rol_por_defecto'],
            descripcion=rol_data['descripcion'],
        )

        
        grupo, created = Group.objects.get_or_create(name=rol_data['nombre_rol'])

  
        permisos = Permission.objects.filter(codename__in=rol_data['permisos'])


        if permisos.exists():
            grupo.permissions.set(permisos)
            rol.permisos.set(permisos)      
            rol.save()
            grupo.save()
        else:
            print(f"No se encontraron permisos para {rol_data['nombre_rol']}")

class Migration(migrations.Migration):


    dependencies = [
        ('permissions', '0005_alter_roles_options'),
    ]

    operations = [
        migrations.RunPython(create_roles_and_groups),
    ]
