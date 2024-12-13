from django.contrib import admin

#para registrar mi base de datos en el administrador
from .models import Producto, Pedido,DetallePedido,Carrito, Cliente,Inicio,FormularioContacto,ContactoSitio,Nosotros,Testimonio
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Carrito)
admin.site.register(DetallePedido)
admin.site.register(Cliente)
admin.site.register(Inicio)
admin.site.register(FormularioContacto)
admin.site.register(ContactoSitio)
admin.site.register(Nosotros)
admin.site.register(Testimonio)


# Register your models here.
