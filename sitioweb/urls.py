from django.urls import path
from . import  views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("",views.inicio, name=("inicio")),
    path("nosotros/",views.nosotros, name=("nosotros")),
    path("productos/",views.productos, name=("productos")),
    path("contactos/",views.contactos, name=("contactos")),
    path("carrito/",views.carrito, name=("carrito")),
    path('Cliente/',views.registrarCliente, name='paginaRegistroCliente'),
    path('login/',views.vistaLogin, name='paginaLogin'),
    path('nuevo-cliente/',views.crearUsuario, name='PaginaNuevoCliente'),
    path('logout/',views.salirUsuario, name='SalirCliente'),
    path('mi-dashboard/',views.cuentaCliente, name='cuentaCliente'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
