from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from .models import Cliente,Inicio,FormularioContacto,ContactoSitio,Nosotros,Testimonio
from django.contrib import messages
from .models import Carrito, Pedido, DetallePedido
from django.contrib.auth.decorators import login_required

from .models import Producto
# from django.contrib.auth.decorators import de
# Create your views here.

def inicio(request):
    context = {
        'inicio': Inicio.objects.all(),
        'formulario_contacto': FormularioContacto.objects.all(),
        'contacto_sitio': ContactoSitio.objects.first(),
        'cliente': Cliente.objects.all(),
        'nosotros': Nosotros.objects.first(),
        'testimonio': Testimonio.objects.all(),
        'productos': Producto.objects.all()[:9]  # Get the first 3 products
    }
    return render(request, "index.html", context)
def nosotros(request):
    nosotros = Nosotros.objects.first()  # Assuming you have only one Nosotros object
    testimonios = Testimonio.objects.all()
    cotacto_sitio = ContactoSitio.objects.first()
    return render(request, "nosotros.html", {'nosotros': nosotros, 'testimonios': testimonios, 'contacto_sitio': cotacto_sitio})

@login_required
def productos(request):
    cotacto_sitio = ContactoSitio.objects.first()
    nosotros = Nosotros.objects.first()
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))

        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para agregar productos al carrito.')
            return redirect('login')  # Asegúrate de que la URL 'login' esté configurada

        producto = Producto.objects.get(id=producto_id)

        # Añadir producto al carrito
        carrito_item, created = Carrito.objects.get_or_create(
            usuario=request.user,
            producto=producto,
            defaults={'cantidad': cantidad}
        )

        if not created:
            # Si el ítem ya está en el carrito, actualizar la cantidad
            carrito_item.cantidad += cantidad
            carrito_item.save()

        return redirect('carrito')  # Asegúrate de que la URL 'carrito' esté configurada

    listarProducto = Producto.objects.all()
    return render(request, "productos.html", {'productos': listarProducto , 'contacto_sitio': cotacto_sitio , 'nosotros': nosotros})


def contactos(request):
    cotacto_sitio_yo = ContactoSitio.objects.first()
    nosotros = Nosotros.objects.first()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        mensaje = request.POST.get('mensaje')
        FormularioContacto.objects.create(nombre=nombre, correo=correo, mensaje=mensaje)
        return redirect('contactos')  # Redirect after successful form submission

    contacto_sitio = ContactoSitio.objects.first()  # Assuming you have only one ContactoSitio object
    return render(request, "contactos.html", {'contacto_sitio': contacto_sitio, 'cotacto_sitio_yo': cotacto_sitio_yo, 'nosotros': nosotros})


@login_required
def carrito(request):
    
    usuario = request.user

    # Obtenemos los elementos del carrito del usuario
    carrito_items = Carrito.objects.filter(usuario=usuario)
    
    # Creamos una lista para almacenar los elementos del carrito junto con el total por item
    carrito_con_totales = []
    total_carrito = 0

    for item in carrito_items:
        total_item = item.producto.precio * item.cantidad
        total_carrito += total_item
        carrito_con_totales.append({
            'item': item,
            'total_item': total_item
        })
    
    if request.method == 'POST':
        direccion_envio = request.POST.get('direccion_envio')
        metodo_pago = request.POST.get('metodo_pago')
        
        # Verificamos que los campos obligatorios estén presentes
        if not direccion_envio or not metodo_pago:
            messages.error(request, 'Por favor, complete todos los campos.')
            return redirect('carrito')  # Asegúrate de que la URL 'carrito' esté configurada

        # Creamos el pedido
        pedido = Pedido.objects.create(
            usuario=usuario,
            total=total_carrito,
            direccion_envio=direccion_envio,
            metodo_pago=metodo_pago
        )

        # Creamos los detalles del pedido
        for item in carrito_items:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio=item.producto.precio
            )
        
        # Eliminamos los elementos del carrito después de crear el pedido
        carrito_items.delete()
        
        messages.success(request, 'Compra realizada con éxito.')
        return redirect('inicio')  # Asegúrate de que la URL 'inicio' esté configurada
    context = {
        'carrito': carrito_con_totales,
        'total': total_carrito,
        'contacto_sitio': ContactoSitio.objects.first(),
        'inicio': Inicio.objects.all(),
        'formulario_contacto': FormularioContacto.objects.all(),
        'contacto_sitio': ContactoSitio.objects.first(),
        'cliente': Cliente.objects.all(),
        'nosotros': Nosotros.objects.first(),
        'testimonio': Testimonio.objects.all(),
        'productos': Producto.objects.all()[:9]  # Get the first 3 products
    }

    return render(request, 'carrito.html', context)



@login_required
def dashword(request):
    return render(request,'dashword.html')

def vistaLogin(request):
    context = {
        'inicio': Inicio.objects.all(),
        'formulario_contacto': FormularioContacto.objects.all(),
        'contacto_sitio': ContactoSitio.objects.first(),
        'cliente': Cliente.objects.all(),
        'nosotros': Nosotros.objects.first(),
        'testimonio': Testimonio.objects.all(),
        'productos': Producto.objects.all()[:9]  # Get the first 3 products
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('cuentaCliente')
        else:
            messages.error(request, 'Datos incorrectos. Por favor, intente nuevamente.')
            return redirect('paginaLogin')

    return render(request, "login.html" , context)

def crearUsuario(request):
    context = {
        'inicio': Inicio.objects.all(),
        'formulario_contacto': FormularioContacto.objects.all(),
        'contacto_sitio': ContactoSitio.objects.first(),
        'cliente': Cliente.objects.all(),
        'nosotros': Nosotros.objects.first(),
        'testimonio': Testimonio.objects.all(),
        'productos': Producto.objects.all()[:9]  # Get the first 3 products
    }
    if request.method == "POST":
        formUsuario = request.POST.get("nuevoCliente")
        formPassword = request.POST.get("nuevaClave")
        
        if formUsuario and formPassword:
            try:
                # Crear un nuevo usuario
                insertarCliente = User.objects.create_user(username=formUsuario, password=formPassword)
                login(request, insertarCliente)
                messages.success(request, 'Registro exitoso. Bienvenido!')
                return redirect('cuentaCliente')
            except Exception as e:
                # Manejar cualquier excepción (por ejemplo, nombre de usuario ya existe)
                messages.error(request, 'Error al registrar el usuario. Por favor, intente nuevamente.')
                return redirect('paginaRegistroCliente')
        else:
            messages.error(request, 'Por favor, complete todos los campos.')
            return redirect('paginaRegistroCliente')

    return render(request, "registrar.html" , context)


@login_required
def salirUsuario(request):
    logout(request)
    context = {
        'inicio': Inicio.objects.all(),
        'formulario_contacto': FormularioContacto.objects.all(),
        'contacto_sitio': ContactoSitio.objects.first(),
        'cliente': Cliente.objects.all(),
        'nosotros': Nosotros.objects.first(),
        'testimonio': Testimonio.objects.all(),
        'productos': Producto.objects.all()[:9]  # Get the first 3 products
    }
    return render(request, "index.html", context)

@login_required
def cuentaCliente(request):
   context = {
        'inicio': Inicio.objects.all(),
        'formulario_contacto': FormularioContacto.objects.all(),
        'contacto_sitio': ContactoSitio.objects.first(),
        'cliente': Cliente.objects.all(),
        'cliente': Cliente.objects.first(),
        'nosotros': Nosotros.objects.first(),
        'testimonio': Testimonio.objects.all(),
        'productos': Producto.objects.all()[:9]  # Get the first 3 products
    }
   return render(request, 'dashboard.html' ,context)

@login_required
def registrarCliente(request):
    context = {
        'inicio': Inicio.objects.all(),
        'formulario_contacto': FormularioContacto.objects.all(),
        'contacto_sitio': ContactoSitio.objects.first(),
        'cliente': Cliente.objects.all(),
        'nosotros': Nosotros.objects.first(),
        'testimonio': Testimonio.objects.all(),
        'productos': Producto.objects.all()[:9]
    }
    if request.method == "POST":
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        direccion = request.POST.get('direccion')

        if nombres and apellidos and dni and telefono and fecha_nacimiento and direccion:
            try:
                insertarRegistro = Cliente(
                    usuario=request.user,
                    nombres=nombres,
                    apellidos=apellidos,
                    dni=dni,
                    telefono=telefono,
                    fecha_nacimiento=fecha_nacimiento,
                    direccion=direccion
                )
                insertarRegistro.save()
                messages.success(request, 'Registro de cliente exitoso.')
                return redirect('cuentaCliente')
            except Exception as e:
                messages.error(request, 'Error al registrar el cliente. Por favor, intente nuevamente.')
                return redirect('paginaRegistroCliente')
        else:
            messages.error(request, 'Por favor, complete todos los campos.')
            return redirect('paginaRegistroCliente')

    return render(request, "cliente.html", context)
