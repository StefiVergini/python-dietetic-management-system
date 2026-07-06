from Bd_Nutrite import bd_Nutrite
import platform
import os
import time
import re
#import math
#import datetime
#---------------------------------- VALIDACIONES GENERALES --------------------------------------
def limpiarPantalla():
    time.sleep(1)

    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def teclaContinuar():
	ok = True
	while ok == True:
		continuar = input("Presione ENTER para Continuar: ")
		if continuar == "":
			ok = False

def esperar_y_limpiar():
	teclaContinuar()
	limpiarPantalla()
	
def siNo():
	ok = True
	print('''
	Ingrese el Número:
		1  -  SI
		2  -  NO
	''')
	print("-" * 65)
	while ok == True:
		try:
			nro = int(input("Ingrese opción: "))
			print("-" * 65)
		except ValueError:
			print("Error. Debe ingresar un número.")
		else:
			if nro < 1 or nro > 2:
				print("Error. Debe elegir un número entre las opciones")
			else:
				ok = False
	return nro
	
def motivoBaja():
	ok = True
	while ok == True:
			motivo = input("Ingrese el motivo de la Baja: ")
			if motivo == '' or motivo == ' ':
				print("-" * 65)
				print("Error. Debe ingresar algún motivo de la Baja")
				print("-" * 65)
			else:
				ok = False
	return motivo
#---------------------------------- VALIDACIONES CLIENTES ---------------------------------------
def validar_cuil():
	valido = 0
	while valido == 0:
		print("-" * 65)
		cuil=(input("Ingrese el CUIL o CUIT solo números: "))
		print("-" * 65)
		if cuil.isdigit() and (len(cuil) == 11 or cuil == "00000000000"):
			valido = 1
		else:
			print("-" * 65)
			print("Error. El N° de CUIL O CUIT debe tener 11 dígitos")
			print("-" * 65)
			
	return cuil
				
def validarNombreCliente(parametro = ""):
	ok=False	
	while ok == False:
		print("-" * 65)
		nomCompleto = input("Ingrese Nombre y Apellido del cliente: ").lower()
		print("-" * 65)
		if parametro == "modi" and nomCompleto == '0':
			ok = True
		elif len(nomCompleto) < 6:
			print("-" * 65)
			print("Lo siento." ,"\n", "Ingresó un Nombre Completo con menos de 6 caracteres.")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		elif not ' ' in nomCompleto:
			print("-" * 65)
			print("Lo siento." ,"\n","Ingresó 1 sola palabra, mínimo tienen que ser 2.")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		elif any(map(str.isdigit, nomCompleto)) == True:
			print("-" * 65)
			print("Error. El Nombre no puede contener números.")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)	
		else:
			ok = True
	return nomCompleto

def validarDireccion(parametro = ""):	
	ok=False 			
	while ok == False:
		print("-" * 65)
		direccion = input("Ingrese Dirección del cliente: ").lower()
		print("-" * 65)
		if parametro == "modi" and direccion == '0':
			ok = True
		elif len(direccion) < 4:
			print("-" * 65)
			print("Error. La dirección debe tener mínimo 4 caracteres")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		elif not ' ' in direccion:
			print("-" * 65)
			print("Lo siento." ,"\n","Ingresó 1 sola palabra, tiene que colocar la calle y el número.")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		elif any(map(str.isdigit, direccion)) == False:
			print("-" * 65)
			print("Error. La dirección debe tener algún número.")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		else:
			ok = True
	return direccion

def validarTelefonoCliente(parametro = ""):	
	ok=True
	while ok == True:
		try:
			print("-" * 65)
			telefono = int(input("Ingrese número de Teléfono: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Debe ingresar solo números")
			print("-" * 65)
		else:
			telefono = str(telefono)
			if parametro == "modi" and telefono == '0':
				ok = False
			elif len(telefono) < 8 or len(telefono) > 12:
				print("-" * 65)
				print("Error. Los teléfonos tienen mínimo 8 dígitos y máximo 12 dígitos")
				print("Por favor, vuelva a ingresar")
				print("-" * 65)
			else:
				ok = False
	return telefono
	
def validar_email(email):
	# Patrón de expresión regular para validar un correo electrónico
	patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

	
	# Utilizar re.match para validar el correo electrónico
	if re.match(patron, email):
		return True
	else:
		return False
		
def mail(parametro = ""):
	ok=True
	while ok == True:
		print("-" * 65)
		email = (input("Ingrese el Mail: "))
		print("-" * 65)
		if parametro == "modi" and email == '0':
			ok = False
		elif validar_email(email):
			ok = False
		else:
			print(f"{email} no es una dirección de correo electrónico válida.")
			print("Por favor, vuelva a ingresar")

	return email

def validarIva(parametro = ""):
	print('''
		Condición Frente al IVA: 
		
		1 - Consumidor Final
		2 - Responsable Inscripto
		3 - Sujeto Exento
	''')
	ok=True
	while ok == True:
		try:
			print("-" * 65)
			iva = int(input("Ingrese número del tipo de IVA: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Debe ingresar solo números")
			print("-" * 65)
		else:
			if parametro == "modi" and iva == 0:
				ok = False
			elif iva < 1 or iva > 3:
				print("-" * 65)
				print("Error. Debe ingresar un Número entre las opciones")
				print("Por favor, vuelva a ingresar")
				print("-" * 65)
			else:
				ok = False
	return iva
	
#--------------------------------------VALIDACIONES PROVEEDOR-----------------------------------------------

def validar_cuit():
	valido = 0
	while valido == 0:
		try:
			print("-" * 65)
			cuit=int(input("Ingrese el CUIT del Proveedor: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Error. Debe ingresar valores numéricos")
			print("-" * 65)
		else:
			cuit = str(cuit)
			if len(cuit) != 11:
				print("-" * 65)
				print("Error. El N° de D.N.I. debe tener 11 dígitos")
				print("-" * 65)
			else:
				valido = 1

	return cuit
def validar_nomEmpresa(parametro = ""):
	ok=False	
	while ok == False:
		print("-" * 65)
		nomEmpresa = input("Ingrese Nombre de la Empresa del Proveedor: ").lower()
		print("-" * 65)
		if parametro == "modi" and nomEmpresa == '0':
			ok = True
		elif len(nomEmpresa) < 2:
			print("-" * 65)
			print("Lo siento." ,"\n", "Ingresó un Nombre  con menos de 2 caracteres.")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		else:
			ok = True
	return nomEmpresa
	
def validar_dirProveedor(parametro = ""):
	ok=False 			
	while ok == False:
		print("-" * 65)
		dirProv = input("Ingrese Dirección del Proveedor\nCALLE - NÚMERO - LOCALIDAD:  ").lower()
		print("-" * 65)
		if parametro == "modi" and dirProv == '0':
			ok = True
		elif len(dirProv) < 4:
			print("-" * 65)
			print("Error. La dirección debe tener mínimo 4 caracteres")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		elif not ' ' in dirProv:
			print("-" * 65)
			print("Lo siento." ,"\n","Ingresó 1 sola palabra, tiene que colocar la Calle, el Número y la Localidad.")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		elif any(map(str.isdigit, dirProv)) == False:
			print("-" * 65)
			print("Error. La dirección debe tener algún número.")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		elif dirProv.count(' ') < 2:
			print("-" * 65)
			print("Lo siento.\nMínimo tiene que haber 2 espacios.")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		else:
			ok = True		
	return dirProv

#------------------------------------------------------------------------------------------------
#---------------------------------- VALIDACIONES ARTICULOS --------------------------------------
def validar_codBarras():
	valido = 0
	while valido == 0:
		try:
			print("-" * 65)
			codBarras = int(input("Ingrese el Código de Barras del Artículo: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Error, debe ingresar sólo valores numéricos")
			print("-" * 65)
		else:
			#maximo de caracteres
			codBarras = str(codBarras)
			if len(codBarras) < 10 or len(codBarras) > 20:
				print("-" * 65)
				print("Error.","\n", "El Código de Barras debe tener mínimo 10 números y máximo 20")
				print("-" * 65)
			else:
				valido = 1
	return codBarras

def validar_NombreArt(parametro = ""):
	ok=False 			
	while ok == False:
		print("-" * 65)
		nomArt = input("Ingrese NOMBRE ARTÍCULO - DESCRIPCIÓN  - MARCA (de tener):\n ").upper()
		print("-" * 65)
		if parametro == "modi" and nomArt == '0':
			ok = True
		elif len(nomArt) < 4:
			print("-" * 65)
			print("Error. El artículo debe tener mínimo 4 caracteres")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		elif not ' ' in nomArt:
			print("-" * 65)
			print("Lo siento." ,"\n","Ingresó 1 sola palabra, debe agregar mínimo el Nombre y la Descripción")
			print("Por favor, vuelva a ingresar")
			print("-" * 65)
		else:
			ok = True		
	return nomArt

def validar_medida(parametro = ""):
	#ML CM3 LITRO GR KG
	print('''
		Unidad de Medida del Artículo: 
		
		1 - Mililitro (ml.)
		2 - Centímetro cúbico (cc.)
		3 - Litro (l.)
		4 - Kilogramo (kg.)
		5 - Gramo (gr.)
	''')
	medidas = ('ML','CC','L','KG','GR')
	valido = 0
	while valido == 0:
		try:
			print("-" * 65)
			tipo_medida=int(input("Ingrese el Número: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Error. Debe ingresar valores numéricos")
			print("-" * 65)
		else:
			if parametro == "modi" and tipo_medida == 0:
				valido = 1
			elif tipo_medida < 1 or tipo_medida > 5:
				print("-" * 65)
				print("Error. Debe ingresar un Número entre las opciones")
				print("-" * 65)
			else:
				tipo_medida = tipo_medida - 1
				valido = 1
	
	return medidas[tipo_medida]
	
def validar_cantProducto(parametro = ""):
	valido = 0
	while valido == 0:
		try:
			print("-" * 65)
			cant_produc=float(input("Ingrese el peso o volumen del Artículo: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Error. Debe ingresar valores numéricos enteros o con decimales")
			print("-" * 65)
		else:
			if parametro == "modi" and cant_produc == 0:
				valido = 1
			elif cant_produc < 0  or cant_produc == 0:
				print("-" * 65)
				print("Error. La cantidad no puede ser inferior o igual a cero")
				print("-" * 65)
			else:
				cant_produc = str(cant_produc)
				limpiarPantalla()
				valido = 1
	return cant_produc
	
def validar_categoria(parametro = ""):
	valido = 0
	while valido == 0:
		try:
			print("-" * 65)
			id_cat=int(input("Ingrese el N° de Categoría del Artículo: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Error. Debe ingresar valores numéricos")
			print("-" * 65)
		else:
			if parametro == "modi" and id_cat == 0:
				valido = 1
			elif id_cat < 1 or id_cat > 24:
				print("-" * 65)
				print("Error. Debe ingresar un Número entre las opciones")
				print("-" * 65)
			else:
				limpiarPantalla()
				valido = 1
	return id_cat

def validarPrecio(parametro = ""):
	valido = 0
	while valido == 0:
		try:
			print("-" * 65)
			precio=float(input("Ingrese el Precio de Venta del Artículo: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Error. Debe ingresar valores numéricos enteros o con decimales")
			print("-" * 65)
		else:
			if parametro == "modi" and precio == 0:
				valido = 1
			elif precio < 0  or precio == 0:
				print("-" * 65)
				print("Error. El Precio no puede ser inferior o igual a cero")
				print("-" * 65)
			else:
				precio = str(precio)
				limpiarPantalla()
				valido = 1
	return precio
	
def validar_stock(texto):
	#texto que ingresa  o texto que egresa cuando hay una venta
	ok=False
	while ok == False:
		try:
			print("-" * 65)
			stock=int(input(f"Ingrese la Cantidad del Producto {texto}: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Error. Debe ingresar valores numéricos enteros")
			print("-" * 65)
		else:
			if texto == "que Ingresa" and stock == 0:
				ok = True
			elif stock < 0 or stock == 0:
				print("-" * 65)
				print("Error. La cantidad no puede ser inferior o igual a cero")
				print("-" * 65)
			else:
				ok = True
	return stock
	
def motivoDevolucion():
	ok = True
	while ok == True:
			motivo = input("Ingrese el motivo de la Devolución: ")
			if motivo == '' or motivo == ' ':
				print("Error. Debe ingresar algún motivo.")
			else:
				ok = False
	return motivo

def validar_idSolicitud():
	ok=False
	while ok == False:
		try:
			print("-" * 65)
			id_solicitud=int(input("Ingrese el Número de Solicitud: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Error. Debe ingresar valores numéricos enteros")
			print("-" * 65)
		else:
			if id_solicitud < 0:
				print("-" * 65)
				print("Error. El Número de Solicitud no puede ser inferior cero")
				print("-" * 65)
			else:
				ok = True
	return id_solicitud

def consultar_por_nombre(texto):
	ok = True
	while ok == True:
			nombre = input(f"Ingrese el Nombre del {texto}: ")
			if nombre == '' or nombre == ' ':
				print("Error. Debe ingresar algún caracter.")
			else:
				ok = False
	return nombre

def validar_Factura():
	ok=False
	while ok == False:
		try:
			print("-" * 65)
			factura=int(input("Ingrese el Número de Factura: "))
			print("-" * 65)
		except ValueError:
			print("-" * 65)
			print("Error. Debe ingresar valores numéricos enteros")
			print("-" * 65)
		else:
			if factura < 0:
				print("-" * 65)
				print("Error. El Número de Solicitud no puede ser inferior cero")
				print("-" * 65)
			else:
				ok = True
	return factura
