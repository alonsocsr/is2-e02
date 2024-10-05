from django.db import models

from django.db import models
from django.contrib.auth.models import Group,Permission


class Roles(models.Model):
    """
    Modelo que representa los roles en el sistema, cada uno de los cuales puede tener permisos asociados.

    :cvar nombre_rol: CharField - Nombre representativo del rol. Ejemplo: 'Editor'.
    :cvar rol_por_defecto: BooleanField - Indica si el rol es un rol por defecto. El valor por defecto es ``False``.
    :cvar descripcion: TextField - Descripción de lo que representa el rol. Ejemplo: 'Rol encargado de la edición de contenidos dentro del sistema'.
    :cvar permisos: ManyToManyField - Permisos asociados al rol. Este campo es opcional y permite definir múltiples permisos que el rol puede tener.
    """
    nombre_rol=models.CharField(max_length=25,unique=True,blank=False,verbose_name='Roles del Sistema')
    
    rol_por_defecto=models.BooleanField(default=False)
    
    descripcion=models.TextField(max_length=50,blank=True)
    
    permisos=models.ManyToManyField(Permission,blank=True)
    
    
    class Meta:
        permissions= [
            ('crear_contenido','Crear Contenido'),
            ('visualizar_contenido','Visualizar Contenido'),
            ('editar_contenido','Editar Contenido'),
            ('publicar_contenido','Publicar Contenido'),
            ('rechazar_contenido','Rechazar Contenido'),
            ('categoria_no_moderada','Categoria No Moderada'),
            ('inactivar_contenido','Inactivar Contenido'),
            ('cambiar_estado_contenido','Cambiar Estado Contenido'),
            ('crear_rol','Crear Rol'),
            ('modificar_rol','Modificar Rol'),
            ('asignar_rol','Asignar Rol'),
            ('remover_rol','Modificar Rol'),
            ('eliminar_rol','Eliminar Rol'),
            ('crear_categoria','Crear Categoria'),
            ('modificar_categoria','Modificar Categoria'),
            ('eliminar_categoria','Eliminar Categoria'),
            ('inactivar_categoria','Inactivar Categoria'),
            ('acceder_a_categoria_paga','Acceder a Categoria Paga'),
            ('acceder_a_categoria_free','Acceder a Categoria Free'),
            ('editar_perfil','Editar Perfil'),
            ('suspender_cuenta','Suspender Cuenta'),
            ('ver_tablero_kanban','Ver Tablero Kanban'),
            ('modificar_tablero_kanban','Modificar Tablero Kanban'),
            ('ver_reportes_contenido','Ver Reportes de Contenido'),
            ('ver_estadisticas_contenido','Ver Estadisticas de Contenido'),
            ('ver_cantidad_likes','Ver Cantidad de Likes'),
            ('ver_cantidad_dislikes','Ver Cantidad de Dislikes'),
            ('ver_cantidad_visualizaciones','Ver Cantidad de visualizaciones'),
            ('ver_cantidad_compartidos','Ver Cantidad de Compartidos'),
            ('comentar_contenido','Comentar Contenido'),
            ('eliminar_contenido','Eliminar Contenido'),
            ('reportar_contenido','Reportar Contenido'),
            ('compartir_contenido','Compartir Contenido'),
            ('filtrar_por_categoria','Filtrar por Categoria'),
            ('filtrar_por_autor','Filtrar por Autor'),
            ('filtrar_por_tags','Filtrar por Tags'),
            ('modificar_estado_contenido','Modificar Estado de Contenido'),
            ('administrar_estado_contenido','Administrar Estado de Contenido'),
            ('eliminar_estado_contenido','Eliminar Estado de Contenido'),
            ('visualizar_versiones_contenido','Visualizar versiones de Contenido'),
            ('restaurar_verisiones_contenido','Restaurar Versiones de Contenido'),
            
        ]
        default_permissions = ()

    def __str__(self):
        """
        Retorna una representación en cadena del rol, que es su nombre.
        
        :return: str - El nombre del rol.
        """
        return self.nombre_rol
    
    def get_nombre_rol(self):
        """
        Retorna el nombre del rol.
        
        :return: str - El nombre del rol.
        """
        return self.nombre_rol
  
  
    
    def asginar_permisos_rol(self,lista_permisos):
        """
        Asigna permisos al rol y al grupo asociado con el mismo nombre. Si el grupo no existe, se crea uno nuevo.

        :param lista_permisos: QuerySet - Lista de permisos a ser asignados al rol.
        """
        grupo,created=Group.objects.get_or_create(name=self.nombre_rol)
        

        #obtener los permisos y asignarlos al grupo
    
        
        grupo.permissions.set(lista_permisos)

        grupo.save()
        
        #asignar permisos a nivel modelo
        self.permisos.set(lista_permisos)
        self.save()
    
    def obtener_permisos(self):
        """
        Retorna los permisos asignados al rol.

        :return: list - Lista de permisos del rol.
        """
        permisos=list(self.permisos.all())
        
        return permisos
        
    
    
        
   
        
        
        