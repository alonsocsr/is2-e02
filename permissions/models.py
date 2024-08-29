from django.db import models

from django.db import models
from django.contrib.auth.models import Group,Permission


class Roles(models.Model):
    
    nombre_rol=models.CharField(max_length=25,unique=True,blank=False,verbose_name='Roles del Sistema')
    
    rol_por_defecto=models.BooleanField(default=False)
    
    descripcion=models.TextField(max_length=50,blank=True)
    
    permisos=models.ManyToManyField(Permission,blank=True)
    
    
    class Meta:
        permissions= [
            ('_crear_contenido','Crear Contenido'),
            ('_visualizar_contenido','Visualizar Contenido'),
            ('_editar_contenido','Editar Contenido'),
            ('_publicar_contenido','Publicar Contenido'),
            ('_rechazar_contenido','Rechazar Contenido'),
            ('_categoria_no_moderada','Categoria No Moderada'),
            ('_inactivar_contenido','Inactivar Contenido'),
            ('_cambiar_estado_contenido','Cambiar Estado Contenido'),
            ('_crear_rol','Crear Rol'),
            ('_modificar_rol','Modificar Rol'),
            ('_asignar_rol','Asignar Rol'),
            ('_remover_rol','Modificar Rol'),
            ('_eliminar_rol','Eliminar Rol'),
            ('_crear_categoria','Crear Categoria'),
            ('_modificar_categoria','Modificar Categoria'),
            ('_eliminar_categoria','Eliminar Categoria'),
            ('_inactivar_categoria','Inactivar Categoria'),
            ('_acceder_a_categoria_paga','Acceder a Categoria Paga'),
            ('_acceder_a_categoria_free','Acceder a Categoria Free'),
            ('_editar_perfil','Editar Perfil'),
            ('_suspender_cuenta','Suspender Cuenta'),
            ('_ver_tablero_kanban','Ver Tablero Kanban'),
            ('_modificar_tablero_kanban','Modificar Tablero Kanban'),
            ('_ver_reportes_contenido','Ver Reportes de Contenido'),
            ('_ver_estadisticas_contenido','Ver Estadisticas de Contenido'),
            ('_ver_cantidad_likes','Ver Cantidad de Likes'),
            ('_ver_cantidad_dislikes','Ver Cantidad de Dislikes'),
            ('_ver_cantidad_visualizaciones','Ver Cantidad de visualizaciones'),
            ('_ver_cantidad_compartidos','Ver Cantidad de Compartidos'),
            ('_comentar_contenido','Comentar Contenido'),
            ('_eliminar_contenido','Eliminar Contenido'),
            ('_reportar_contenido','Reportar Contenido'),
            ('_compartir_contenido','Compartir Contenido'),
            ('_filtrar_por_categoria','Filtrar por Categoria'),
            ('_filtrar_por_autor','Filtrar por Autor'),
            ('_filtrar_por_tags','Filtrar por Tags'),
            ('_modificar_estado_contenido','Modificar Estado de Contenido'),
            ('_administrar_estado_contenido','Administrar Estado de Contenido'),
            ('_eliminar_estado_contenido','Eliminar Estado de Contenido'),
            ('_visualizar_versiones_contenido','Visualizar versiones de Contenido'),
            ('_restaurar_verisiones_contenido','Restaurar Versiones de Contenido'),
        ]

    def __str__(self):
        return self.nombre_rol
    
    def get_nombre_rol(self):
      return self.nombre_rol
  
  
    
    def asginar_permisos_rol(self,lista_permisos):
        """
        funcion para crear un rol o actualizarlo segun se quiera
        """
        
        """
        crear un grupo con el nombre del rol
        """

        grupo,created=Group.objects.get_or_create(name=self.nombre_rol)
        

        """
        obtener los permisos y asignarlos al grupo
        """
        permisos = Permission.objects.filter(codename__in=[perm.name for perm in lista_permisos])
        
       
        
        grupo.permissions.set(permisos)

        grupo.save()
        
        """asignar permisos a nivel modelo"""
        self.permisos.set(lista_permisos)
        self.save()
    
    def obtener_permisos(self):
        """
        Funcion que retorna los permisos asignados a un grupo
        params: el grupo
        return: lista de permisos del grupo
        """
        permisos=list(self.permisos.all())
        
        return permisos
        
    
    
        
   
        
        
        