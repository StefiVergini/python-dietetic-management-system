from main import *
from validaciones import *
from Bd_Nutrite import bd_Nutrite
from clientes import Clientes
from proveedores import Proveedores
from articulos import Articulos
from pedidoDevo import PedidoDevo
from ventas import Ventas

def salir():
	bd = bd_Nutrite()
	bd.cerrarBD()
	del bd
	print("**********************************  HASTA LUEGO  ************************************")
	limpiarPantalla()

#OPCION 1 MENU PRINCIPAL
def submenu_proveedor():
	proveedor = Proveedores()
	pedido = PedidoDevo()
	print('''
		---------------------------------------------
		|      ****  GESTIÓN PROVEEDORES  ****      |
		---------------------------------------------
					
			   ----  SELECCIONE  ----
				           
			2 - CONSULTAS PROVEEDORES
			3 - ALTA PROVEEDOR
			4 - MODIFICACIÓN PROVEEDOR
			5 - BAJA O REACTIVAR CUENTA PROVEEDOR
			6 - PEDIDO DE REPOSICIÓN ARTÍCULOS
			7 - PEDIDO DE DEVOLUCIÓN DE ARTÍCULO
			8 - REGISTRAR DEVOLUCIÓN DE ARTÍCULO
			
			1 - VOLVER AL MENÚ PRINCIPAL
			0 - SALIR
	''')
	
	valido = 0
	while valido == 0:
		try:
			numIngresado = int(input("- Ingrese opción: "))
		except ValueError:
			print("Error. Debe ingresar un número entre las opciones")
		else:
			if numIngresado < 0 or numIngresado > 8:
				print("-" * 65)
				print("Error", "\n", "Debe ingresar una opción correcta.")
				print("-" * 65)
			elif numIngresado == 1:
				del proveedor
				limpiarPantalla()
				main()
				valido = 1
			elif numIngresado == 2:
				limpiarPantalla()
				consulta_proveedores()
				valido = 1
			elif numIngresado == 3:
				limpiarPantalla()
				proveedor.registroProveedor()
				valido = 1
			elif numIngresado == 4:
				limpiarPantalla()
				proveedor.modificarProveedor()
				valido = 1
			elif numIngresado == 5:
				op5Prov()
				valido = 1
			elif numIngresado == 6:
				limpiarPantalla()
				pedido.nuevoPedido()
				valido = 1
			elif numIngresado == 7:
				limpiarPantalla()
				pedido.devolucionArt()
				valido = 1
			elif numIngresado == 8:
				limpiarPantalla()
				pedido.registrarDevolucion()
				valido = 1
			elif numIngresado == 0:
				del proveedor
				del pedido
				salir()
				valido = 1


#OPCION 2 MENU PRINCIPAL
def submenu_clientes():
	cliente = Clientes()
	print('''
		---------------------------------------------
		|        ****  GESTIÓN CLIENTES  ****       |
		---------------------------------------------
					
			   ----  SELECCIONE  ----
				           
			2 - CONSULTAS CLIENTE
			3 - ALTA CLIENTE
			4 - MODIFICACIÓN CLIENTE
			5 - BAJA O REACTIVAR CUENTA CLIENTE
			
			1 - VOLVER AL MENÚ PRINCIPAL
			0 - SALIR
	''')
	valido = 0
	while valido == 0:
		try:
			numIngresado = int(input("- Ingrese opción: "))
		except ValueError:
			print("Error. Debe ingresar un número entre las opciones")
		else:
			if numIngresado < 0 or numIngresado > 5:
				print("-" * 65)
				print("Error", "\n", "Debe ingresar una opción correcta.")
				print("-" * 65)
			elif numIngresado == 1:
				del cliente
				limpiarPantalla()
				main()
				valido = 1
			elif numIngresado == 2:
				limpiarPantalla()
				consulta_clientes()
				valido = 1
			elif numIngresado == 3:
				limpiarPantalla()
				cliente.registroCliente()
				valido = 1
			elif numIngresado == 4:
				limpiarPantalla()
				cliente.modificarCliente()
				valido = 1
			elif numIngresado == 5:
				op5Clientes()
				valido = 1
			elif numIngresado == 0:
				del cliente
				salir()
				valido = 1

#OPCION 3 MENU PRINCIPAL
def submenu_articulos():
	art = Articulos()
	pro = Proveedores()
	pedido = PedidoDevo()
	print('''
		---------------------------------------------
		|       ****  GESTIÓN ARTÍCULOS  ****       |
		---------------------------------------------
					
			   ----  SELECCIONE  ----
				           
			2 - CONSULTAS ARTÍCULO
			3 - ALTA ARTÍCULO
			4 - MODIFICACIÓN ARTÍCULO
			5 - BAJA O REACTIVAR ARTÍCULO
			6 - REPOSICIÓN ARTÍCULOS
			7 - ARTÍCULOS SIN STOCK
			
			1 - VOLVER AL MENÚ PRINCIPAL
			0 - SALIR
	''')
	valido = 0
	while valido == 0:
		try:
			numIngresado = int(input("- Ingrese opción: "))
		except ValueError:
			print("Error. Debe ingresar un número entre las opciones")
		else:
			if numIngresado < 0 or numIngresado > 7:
				print("-" * 65)
				print("Error", "\n", "Debe ingresar una opción correcta.")
				print("-" * 65)
			elif numIngresado == 1:
				del pro
				del art
				limpiarPantalla()
				main()
				valido = 1
			elif numIngresado == 2:
				limpiarPantalla()
				consulta_articulos()
				valido = 1
			elif numIngresado == 3:
				pro.checkProv_Articulo()
				limpiarPantalla()
				valido = 1
			elif numIngresado == 4:
				art. modificarArticulo()
				limpiarPantalla()
				valido = 1
			elif numIngresado == 5:
				op5Art()
				valido = 1
			elif numIngresado == 6:
				limpiarPantalla()
				pedido.registrarReposicion()
				valido = 1
			elif numIngresado == 7:
				limpiarPantalla()
				art.artSinStock()
				valido = 1
			elif numIngresado == 0:
				del pedido
				del pro
				del art
				salir()
				valido = 1


#OPCION 4 MENU PRINCIPAL
def submenu_ventas():
	venta = Ventas()
	print('''
		---------------------------------------------
		|        ****  GESTIÓN VENTAS  ****         |
		---------------------------------------------
					
			   ----  SELECCIONE  ----
				           
			2 - VENTA CLIENTE SIN REGISTRAR
			3 - VENTA CLIENTE REGISTRADO
			4 - VENTAS DEL DÍA
			5 - BUSCAR UNA FACTURA POR NÚMERO
			
			1 - VOLVER AL MENÚ PRINCIPAL
			0 - SALIR
	''')
	valido = 0
	while valido == 0:
		try:
			numIngresado = int(input("- Ingrese opción: "))
		except ValueError:
			print("Error. Debe ingresar un número entre las opciones")
		else:
			if numIngresado < 0 or numIngresado > 5:
				print("-" * 65)
				print("Error", "\n", "Debe ingresar una opción correcta.")
				print("-" * 65)
			elif numIngresado == 1:
				limpiarPantalla()
				main()
				valido = 1
			elif numIngresado == 2:
				limpiarPantalla()
				venta.ventaSinRegistro()
				valido = 1
			elif numIngresado == 3:
				limpiarPantalla()
				venta.ventaConRegistro()
				valido = 1
			elif numIngresado == 4:
				limpiarPantalla()
				venta.ventasDelDia()
				valido = 1
			elif numIngresado == 5:
				limpiarPantalla()
				venta.buscarFactura()
				valido = 1
			elif numIngresado == 0:
				del venta
				salir()
				valido = 1

def op5Clientes():
	cliente = Clientes()
	print('''
		Ingrese el Número:
		
		1 - REACTIVAR CLIENTE
		2 - DAR DE BAJA CLIENTE
	
		0 - Volver a Gestión Clientes
			''')
	print("-" * 57)
	ok = True
	while ok == True:
		try:
			nro = int(input("Ingrese opción: "))
		except ValueError:
			print("Error. Debe ingresar un valor numérico")
		else:
			if nro < 0 or nro > 2:
				print("-" * 65)
				print("Error", "\n", "Debe ingresar una opción correcta.")
				print("-" * 65)
			elif nro == 1:
				limpiarPantalla()
				cliente.reactivarCliente()
				ok = False
			elif nro == 2:
				limpiarPantalla()
				cliente.checkBajaCliente()
				ok = False
			elif nro == 0:
				limpiarPantalla()
				submenu_clientes()
				ok = False

def op5Prov():
	prov = Proveedores()
	print('''
		Ingrese el Número:
		
		1 - REACTIVAR PROVEEDOR
		2 - DAR DE BAJA PROVEEDOR
	
		0 - Volver a Gestión Proveedor
			''')
	print("-" * 57)
	ok = True
	while ok == True:
		try:
			nro = int(input("Ingrese opción: "))
		except ValueError:
			print("Error. Debe ingresar un valor numérico")
		else:
			if nro < 0 or nro > 2:
				print("-" * 65)
				print("Error", "\n", "Debe ingresar una opción correcta.")
				print("-" * 65)
			elif nro == 1:
				limpiarPantalla()
				prov.reactivarProveedor()
				ok = False
			elif nro == 2:
				limpiarPantalla()
				prov.check_bajaProveedor()
				ok = False
			elif nro == 0:
				limpiarPantalla()
				submenu_proveedor()
				ok = False

def op5Art():
	art = Articulos()
	print('''
		Ingrese el Número:
		
		1 - REACTIVAR ARTÍCULO
		2 - DAR DE BAJA ARTÍCULO
	
		0 - Volver a Gestión Artículos
			''')
	print("-" * 57)
	ok = True
	while ok == True:
		try:
			nro = int(input("Ingrese opción: "))
		except ValueError:
			print("Error. Debe ingresar un valor numérico")
		else:
			if nro < 0 or nro > 2:
				print("-" * 65)
				print("Error", "\n", "Debe ingresar una opción correcta.")
				print("-" * 65)
			elif nro == 1:
				limpiarPantalla()
				art.reactivarArt()
				ok = False
			elif nro == 2:
				limpiarPantalla()
				art.checkBajaArt()
				ok = False
			elif nro == 0:
				limpiarPantalla()
				submenu_articulos()
				ok = False
				
def consulta_proveedores():
	prov = Proveedores()
	print('''
		---------------------------------------------
		|      ****  CONSULTA PROVEEDORES  ****     |
		---------------------------------------------
					
			   ----  SELECCIONE  ----
				           
			2 - CONSULTAR PROVEEDOR POR NOMBRE
			3 - VER TODOS LOS PROVEEDORES
			4 - VER PROVEEDORES BAJA
			5 - VER ARTÍCULOS CON STOCK 
			    MENOR A 4 Y MAYOR A 0
			
			1 - VOLVER MENÚ GESTIÓN PROVEEDOR
			0 - SALIR
	''')
	valido = 0
	while valido == 0:
		try:
			numIngresado = int(input("- Ingrese opción: "))
		except ValueError:
			print("Error. Debe ingresar un número entre las opciones")
		else:
			if numIngresado < 0 or numIngresado > 5:
				print("-" * 65)
				print("Error", "\n", "Debe ingresar una opción correcta.")
				print("-" * 65)
			elif numIngresado == 1:
				del prov
				limpiarPantalla()
				submenu_proveedor()
				valido = 1
			elif numIngresado == 2:
				limpiarPantalla()
				prov.proveedorPorNombre()
				valido = 1
			elif numIngresado == 3:
				limpiarPantalla()
				prov.verProveedores()
				valido = 1
			elif numIngresado == 4:
				limpiarPantalla()
				prov.verProveedoresBaja()
				valido = 1
			elif numIngresado == 5:
				limpiarPantalla()
				prov.verBajoStock()
				valido = 1

			elif numIngresado == 0:
				del prov
				salir()
				valido = 1

def consulta_clientes():
	cliente = Clientes()
	print('''
		---------------------------------------------
		|       ****  CONSULTA CLIENTES  ****       |
		---------------------------------------------
					
			   ----  SELECCIONE  ----
				           
			2 - CONSULTAR CLIENTE POR NOMBRE
			3 - VER TODOS LOS CLIENTES
			4 - VER CLIENTES BAJA
			5 - VER VENTAS POR CLIENTE
			
			1 - VOLVER MENÚ GESTIÓN CLIENTES
			0 - SALIR
	''')
	valido = 0
	while valido == 0:
		try:
			numIngresado = int(input("- Ingrese opción: "))
		except ValueError:
			print("Error. Debe ingresar un número entre las opciones")
		else:
			if numIngresado < 0 or numIngresado > 5:
				print("-" * 65)
				print("Error", "\n", "Debe ingresar una opción correcta.")
				print("-" * 65)
			elif numIngresado == 1:
				del cliente
				limpiarPantalla()
				submenu_clientes()
				valido = 1
			elif numIngresado == 2:
				limpiarPantalla()
				cliente.clientePorNombre()
				valido = 1
			elif numIngresado == 3:
				limpiarPantalla()
				cliente.verClientes()
				valido = 1
			elif numIngresado == 4:
				limpiarPantalla()
				cliente.verClientesBaja()
				valido = 1
			elif numIngresado == 5:
				limpiarPantalla()
				cliente.verVentasCliente()
				valido = 1

			elif numIngresado == 0:
				del cliente
				salir()
				valido = 1
				
def consulta_articulos():
	art = Articulos()
	print('''
		---------------------------------------------
		|       ****  CONSULTA ARTICULOS  ****       |
		---------------------------------------------
					
			   ----  SELECCIONE  ----
				           
			2 - CONSULTAR ARTÍCULOS POR NOMBRE
			3 - VER TODOS LOS ARTICULOS
			4 - VER ARTICULOS BAJA
			5 - VER ARTICULOS POR PROVEEDOR
			
			1 - VOLVER MENÚ GESTIÓN ARTICULOS
			0 - SALIR
	''')
	valido = 0
	while valido == 0:
		try:
			numIngresado = int(input("- Ingrese opción: "))
		except ValueError:
			print("Error. Debe ingresar un número entre las opciones")
		else:
			if numIngresado < 0 or numIngresado > 5:
				print("-" * 65)
				print("Error", "\n", "Debe ingresar una opción correcta.")
				print("-" * 65)
			elif numIngresado == 1:
				del art
				limpiarPantalla()
				submenu_articulos()
				valido = 1
			elif numIngresado == 2:
				limpiarPantalla()
				art.artPorNombre()
				valido = 1
			elif numIngresado == 3:
				limpiarPantalla()
				art.verArticulos()
				valido = 1
			elif numIngresado == 4:
				limpiarPantalla()
				art.verArticulosBaja()
				valido = 1
			elif numIngresado == 5:
				limpiarPantalla()
				art.verArticulosXProv()
				valido = 1

			elif numIngresado == 0:
				del art
				salir()
				valido = 1
