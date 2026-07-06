from Bd_Nutrite import bd_Nutrite
from clientes import Clientes
from articulos import Articulos
import validaciones
import mariadb
import submenus
import datetime
import mysql.connector
from tabulate import tabulate

class Ventas(bd_Nutrite):
	def __init__(self):
		super().__init__()
		self.articulos = Articulos()
		self.clientes = Clientes()
	
	#Venta sin registro enviar id cliente
	#venta con registro buscar cuil cliente
	#venta del día
	def ventaConRegistro(self):
		totalVenta = 0
		mycursor = self.mydb.cursor()
		print("-" * 65)
		print("          VENTA CLIENTE REGISTRADO")
		print("-" * 65)
		cuil = validaciones.validar_cuil()
		existeCuil = self.clientes.buscarCuil(cuil)
		if existeCuil == False:
			print("-" * 65)
			print("Lo siento.")
			print(f"El CUIL: {cuil} no se encuentra Registrado")
			print("-" * 65)
			validaciones.esperar_y_limpiar()
			submenus.submenu_ventas()
		else:
			sql = f"SELECT id_cliente, id_estado, observacion_baja FROM Clientes WHERE cuil_t_cli = '{cuil}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			id_cliente = myresultado[0]
			id_estado = myresultado[1]
			motivo = myresultado[2]
			self.clientes.mostrarDatosCli(cuil)
			print("-" * 65)
			if id_estado == 2:
				print("-" * 65)
				print("Lo siento.")
				print("El Cliente está dado de Baja.")
				print("-" * 65)
				print(f"MOTIVO BAJA: {motivo.upper()}")
				print("-" * 65)
				validaciones.esperar_y_limpiar()
				submenus.submenu_ventas()
			else:
				validaciones.esperar_y_limpiar()
				fechaSolicitud = datetime.date.today()
				horaSolicitud = datetime.datetime.now().time()
				sql = f"INSERT INTO Ventas_cli(id_cliente,fecha_venta,hora_venta, total_venta) VALUES (%d,%s,%s,%s)"
				val = [id_cliente,fechaSolicitud,horaSolicitud,totalVenta]
				hora = horaSolicitud.strftime('%H:%M:%S')
				mycursor.execute(sql, val)
				self.mydb.commit()
				self.ventas(id_cliente,fechaSolicitud,hora)
	
	#id_venta_cli INT, id_cliente, fecha_venta DATE ,hora_venta TIME, total_venta DOUBLE
	def ventaSinRegistro(self):
		id_cliente = 1
		totalVenta = 0
		mycursor = self.mydb.cursor()
		print("-" * 65)
		print("          VENTA CLIENTE SIN REGISTRAR")
		print("-" * 65)
		fechaSolicitud = datetime.date.today()
		horaSolicitud = datetime.datetime.now().time()
		sql = f"INSERT INTO Ventas_cli(id_cliente,fecha_venta,hora_venta, total_venta) VALUES (%d,%s,%s,%s)"
		val = [id_cliente,fechaSolicitud,horaSolicitud,totalVenta]
		hora = horaSolicitud.strftime('%H:%M:%S')
		mycursor.execute(sql, val)
		self.mydb.commit()
		self.ventas(id_cliente,fechaSolicitud,hora)
	
	def ventas(self, id_cliente,fechaSolicitud,hora):
		mycursor = self.mydb.cursor()
		sql = f"SELECT id_venta_cli FROM Ventas_cli WHERE id_cliente = '{id_cliente}' AND fecha_venta = '{fechaSolicitud}' AND hora_venta = '{hora}'" 
		mycursor.execute(sql)
		myresultado = mycursor.fetchone()
		id_solicitud = myresultado[0]
		ok = True
		while ok == True:
			codBarras = validaciones.validar_codBarras()
			existeCod = self.articulos.buscarCodBarras(codBarras)
			if existeCod == False:
				print("-" * 65)
				print("Lo siento.")
				print(f"El Código de Barras: {codBarras} no se encuentra Registrado")
				print("-" * 65)
				print("Vuelva a Ingresar")
			else:
				self.articulos.mostrarDatosArt(codBarras)
				sql = f"SELECT id_art,precio_art,stock_art,id_estado FROM Articulos WHERE cod_barras = '{codBarras}'"
				mycursor.execute(sql)
				myresultado = mycursor.fetchone()
				id_art = myresultado[0]
				precio_art = myresultado[1]
				stock_art = myresultado[2]
				id_estado = myresultado[3]
				if id_estado == 2:
					print("Este artículo está dado de baja.")
					print("-" * 65)
					print("          Vuelva a Ingresar")
					print("-" * 65)
				elif stock_art == 0:
					print("Lo siento. No tenemos stock de este Artículo")
					print("-" * 65)
					print("          Vuelva a Ingresar")
					print("-" * 65)
				else:
					self.cantidadPrecio(id_art,precio_art,stock_art,id_solicitud,id_cliente,fechaSolicitud,hora,codBarras)
					ok = False

	#Ventas_art(id_venta_cli INT, id_art INT,precio_uni DOUBLE, cant_venta INT, subTotal_precio DOUBLE
	def cantidadPrecio(self, id_art,precio_art,stock_art,id_solicitud, id_cliente, fechaSolicitud,hora,codBarras):
		mycursor = self.mydb.cursor()
		ok = False
		while ok == False:
			cantidad = validaciones.validar_stock("a Comprar")
			if stock_art < cantidad:
				print("Lo siento. La cantidad ingresada es Mayor al Stock Actual")
				print("-" * 65)
				print("          Vuelva a Ingresar")
				print("-" * 65)
			else:
				sub_total = precio_art * cantidad
				stockActual = stock_art - cantidad
				sql = f"SELECT nom_art, precio_art FROM Articulos WHERE cod_barras = '{codBarras}'"
				mycursor.execute(sql)
				myresultado = mycursor.fetchone()
				print("-" * 65)
				print(f"CÓDIGO BARRAS: {codBarras}")
				print(f"NOMBRE: {myresultado[0].upper()}")
				print(f"CANTIDAD A COMPRAR: {cantidad} || PRECIO POR UNIDAD: ${myresultado[1]} ")
				print("-" * 65)
				print(f"IMPORTE A ABONAR POR ESTA CANTIDAD DE ARTÍCULOS: ${sub_total}")
				print("-" * 65)
				print("           ¿Confirma este Producto y Cantidad?")
				print("-" * 65)
				respuesta = validaciones.siNo()
				if respuesta == 1:
					sql = f"INSERT INTO Ventas_art(id_venta_cli,id_art,precio_uni,cant_venta,subTotal_precio) VALUES (%d,%d,%s,%d,%s)"
					val = [id_solicitud,id_art,precio_art,cantidad,sub_total]
					mycursor.execute(sql, val)
					self.mydb.commit()
					sql = f"UPDATE Articulos SET stock_art = '{stockActual}' WHERE id_art = '{id_art}'"
					mycursor.execute(sql)
					self.mydb.commit()
				self.seguirComprando(id_cliente,fechaSolicitud,hora,id_solicitud)
				ok = True
	
	def seguirComprando(self,id_cliente,fechaSolicitud,hora,id_solicitud):
		validaciones.limpiarPantalla()
		mycursor = self.mydb.cursor()
		print("-" * 65)
		print("              ¿Desea Seguir Comprando?")
		print("-" * 65)
		respuesta = validaciones.siNo()
		if respuesta == 1:
			validaciones.limpiarPantalla()
			self.ventas(id_cliente,fechaSolicitud,hora)
		else:
			sql = f"SELECT subTotal_precio FROM Ventas_art WHERE id_venta_cli = '{id_solicitud}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchall()
			precioTotal = 0
			for tupla in myresultado:	
				sub_total = tupla[0]
				precioTotal = precioTotal + sub_total
			precioTotal = round(precioTotal, 2)
			sql = f"UPDATE Ventas_cli SET total_venta = '{precioTotal}' WHERE id_venta_cli = '{id_solicitud}'"
			mycursor.execute(sql)
			self.mydb.commit()
			self.mostrarFactura(id_solicitud, "A PAGAR")
	
	def mostrarFactura(self,id_solicitud, texto):
		mycursor = self.mydb.cursor()
		validaciones.limpiarPantalla()
		sql = f"SELECT c.cuil_t_cli, c.nom_completo,i.tipo_factura, v.fecha_venta, v.hora_venta, v.total_venta FROM Ventas_cli as v INNER JOIN Clientes as c ON v.id_cliente = c.id_cliente INNER JOIN IVA as i ON i.id_iva = c.id_iva WHERE v.id_venta_cli = '{id_solicitud}'"
		mycursor.execute(sql)
		myresultado = mycursor.fetchone()
		if myresultado is not None:
			cuil = myresultado[0]
			nomCli = myresultado[1]
			tipoFactura = myresultado[2]
			fechaVenta = myresultado[3]
			horaV = myresultado[4]
			totalV = myresultado[5]
			totalV =round(totalV, 2)
			fechaV = fechaVenta.strftime('%d/%m/%Y')
			print("-" * 100)
			print(f"                                         FACTURA N°: {id_solicitud}")
			print("-" * 100)
			print(f"                                                              FACTURA TIPO: {tipoFactura}")
			print("")
			print(f"                                                              FECHA: {fechaV} HORA: {horaV}")
			print("")
			print(f"      CUIL: {cuil}")
			print(f"   CLIENTE: {nomCli.upper()}")
			print("")
			sql = f"SELECT a.cod_barras as 'CODIGO BARRAS', a.nom_art as 'NOMBRE', v.cant_venta as 'CANTIDAD', v.precio_uni as 'PRECIO UNIDAD',v.subTotal_precio as 'SUBTOTAL $' FROM Ventas_art as v INNER JOIN Articulos as a ON v.id_art = a.id_art WHERE v.id_venta_cli = '{id_solicitud}'"
			super().mostrarTablas(sql)
			print("-" * 100)
			print(f"                                                                         | TOTAL {texto}: ${totalV}|")
			print("-" * 100)
		else:
			print("-" * 65)
			print(f"Lo siento.\nEl Número de Factura: {id_solicitud} no existe")
			print("-" * 65)
		validaciones.esperar_y_limpiar()
		submenus.submenu_ventas()
	
	def ventasDelDia(self):
		total_ventas_dia = 0
		mycursor = self.mydb.cursor()
		fechaHoy = datetime.date.today()
		sql = f"SELECT total_venta FROM Ventas_cli WHERE fecha_venta = '{fechaHoy}'"
		mycursor.execute(sql)
		myresultado = mycursor.fetchall()
		for tupla in myresultado:	
			total_venta = tupla[0]
			total_ventas_dia = total_ventas_dia + total_venta
		total_ventas_dia = round(total_ventas_dia,2)
		fechaS = fechaHoy.strftime('%d/%m/%Y')
		print("-" * 100)
		print(f"                             VENTAS DEL DÍA: {fechaS}")
		print("-" * 100)
		sql = f"SELECT c.cuil_t_cli as CUIL,c.nom_completo as 'NOMBRE COMPLETO',v.id_venta_cli as 'FACTURA N°',v.hora_venta as 'HORA', v.total_venta FROM Ventas_cli as v INNER JOIN Clientes as c ON v.id_cliente = c.id_cliente WHERE v.fecha_venta = '{fechaHoy}' ORDER BY v.hora_venta"
		super().mostrarTablas(sql)
		print("-" * 100)
		print(f"                                                                              | TOTAL: ${total_ventas_dia}|")
		print("-" * 100)	
		validaciones.esperar_y_limpiar()
		submenus.submenu_ventas()
	
	def buscarFactura(self):
		print("-" * 65)
		print("              BUSCAR FACTURA POR NÚMERO")
		print("-" * 65)
		id_factura = validaciones.validar_Factura()
		self.mostrarFactura(id_factura, "ABONADO")
