from django.db import models
from django.contrib.auth.models import User

# Modelo para registrar información general
class Registro(models.Model):
    nombre = models.CharField(max_length=200)
    correo = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    fecha = models.DateField()
    contenido = models.TextField()

    def __str__(self):
        return self.nombre

# Modelo para información adicional del cliente
class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.RESTRICT)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    dni = models.CharField(max_length=15)
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(null=True)
    direccion = models.TextField()

    def __str__(self):
        return self.usuario.username

# Modelos para productos y pedidos
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, null=True, blank=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADO_OPCIONES = [
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='procesando')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    direccion_envio = models.TextField()
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f'Pedido {self.id} - {self.usuario.username}'

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad}'


#Inicio --------------------------------------------------------------------------------------------
class Inicio(models.Model):
    imagenFondo = models.ImageField(upload_to='inicio/', null=True, blank=True)
    imagenQuienesSomos = models.ImageField(upload_to='inicioQuienesSomos/', null=True, blank=True)
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200)
    contenido = models.TextField()
    tituloProductos = models.CharField(max_length=200)

#formularioContacto
class FormularioContacto(models.Model):
    nombre = models.CharField(max_length=200)
    correo = models.CharField(max_length=200)
    mensaje = models.TextField()

#ContactoSitio 
class ContactoSitio(models.Model):
    lugar = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    horario_atencion = models.CharField(max_length=200)
    mapaurl = models.URLField(max_length=200, blank=True)
    facebook_url = models.URLField(max_length=200, blank=True)
    instagram_url = models.URLField(max_length=200, blank=True)
    twitter_url = models.URLField(max_length=200, blank=True)
    whatsapp_url = models.URLField(max_length=200, blank=True)

#Nosotros----------------------------------------------------------------------------------------------------
class Nosotros(models.Model):
    logo = models.ImageField(upload_to='nosotros/', null=True, blank=True)
    tituloElBorrachoFiel = models.CharField(max_length=200)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagenNosotros = models.ImageField(upload_to='nosotros/', null=True, blank=True)
    valores = models.TextField()
    equipo = models.TextField()

#textimonio 
class Testimonio(models.Model):
    contenido = models.TextField()
    nombrepersona = models.CharField(max_length=200)


