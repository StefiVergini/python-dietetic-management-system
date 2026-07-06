from Bd_Nutrite import bd_Nutrite
from proveedores import Proveedores
from articulos import Articulos
import validaciones
import mariadb
import submenus
import datetime
import mysql.connector
from tabulate import tabulate
#pip install mysql-connector-python
#pip install tabulate

class PedidoDevo(bd_Nutrite):
	def __init__(self):
		super().__init__()
		self.proveedor = Proveedores()
		self.articulos = Articulos()
	
	def buscarId_Solicitud(self, id_solicitud):
		encontrado = False
		mycursor = self.mydb.cursor()
		sql = "SELECT id_solicitud FROM Solicitudes"
		mycursor.execute(sql)
		myresultado = mycursor.fetchall()
		for tupla in myresultado:	
			id_sol = tupla[0]
			if id_solicitud == id_sol:
				encontrado = True
				break		
		return encontrado	
	
	def mostrarPedido(self,id_solicitud, id_prov, fechaSolicitud, hora, texto):
		mycursor = self.mydb.cursor()
		sql = f"SELECT nombre_empresa,cuit_pro FROM Proveedores WHERE id_proveedor = '{id_prov}'"
		mycursor.execute(sql)
		myresultado = mycursor.fetchone()
		fechaFormat = fechaSolicitud.strftime('%d/%m/%Y')
		print("-" * 70)
		print(f"|                         SOLICITUD N°: {id_solicitud}")
		print("-" * 70)
		print(f"|   FECHA: {fechaFormat}                      HORA: {hora}")
		print("|")
		print(f"|   EMPRESA: {myresultado[0].upper()}")
		print(f"|   CUIT: {myresultado[1]}")
		sql = f"SELECT a.cod_barras as 'CODIGO BARRAS', a.nom_art as 'NOMBRE - DESCRIPCION', s.cant_art as 'CANTIDAD {texto}' FROM Solicitud_Descripcion as s INNER JOIN Articulos as a ON s.id_art = a.id_art WHERE id_solicitud = '{id_solicitud}'"
		super().mostrarTablas(sql)
		
	def nuevoPedido(self):
		print("-" * 65)
		print("                   NUEVO PEDIDO")
		print("-" * 65)
		cuit = self.proveedor.provNoEncontrado()
		if cuit:
			mycursor = self.mydb.cursor()
			sql = f"SELECT id_proveedor, id_estado, motivo_baja FROM Proveedores WHERE cuit_pro = '{cuit}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			id_prov = myresultado[0]
			id_estado = myresultado[1]
			motivo = myresultado[2]
			self.proveedor.mostrarDatosProv(cuit)
			print("-" * 65)
			if id_estado == 2:
				print("-" * 65)
				print("Error. El Proveedor está dado de Baja.")
				print(f"MOTIVO: {motivo.upper()}")
				print("-" * 65)
				validaciones.esperar_y_limpiar()
				submenus.submenu_proveedor()
			else:
				fechaSolicitud = datetime.date.today()
				horaSolicitud = datetime.datetime.now().time()
				sql = f"INSERT INTO Solicitudes(id_proveedor,fecha_solicitud,hora_solicitud ,tipo_solicitud,estado_solicitud) VALUES (%d,%s,%s,%s,%s)"
				val = [id_prov,fechaSolicitud,horaSolicitud,'P','A']
				hora = horaSolicitud.strftime('%H:%M:%S')
				mycursor.execute(sql, val)
				self.mydb.commit()
				validaciones.esperar_y_limpiar()
				self.artNuevoPedido(id_prov,fechaSolicitud,hora)
		else:
			validaciones.esperar_y_limpiar()
			submenus.submenu_proveedor()
		
	def artNuevoPedido (self,id_prov,fechaSolicitud,hora):
		print("-" * 65)
		print("              ARTÍCULOS - PEDIDO")
		print("-" * 65)
		ok = True
		contador = 0
		mycursor = self.mydb.cursor()
		sql = f"SELECT id_solicitud FROM Solicitudes WHERE id_proveedor = '{id_prov}' AND fecha_solicitud = '{fechaSolicitud}' AND hora_solicitud = '{hora}'" 
		mycursor.execute(sql)
		myresultado = mycursor.fetchone()
		id_solicitud = myresultado[0]
		while ok == True:
			codBarras = self.articulos.artNoEncontrado()
			if codBarras:
				sql = f"SELECT id_art, id_proveedor, id_estado, motivo_baja FROM Articulos WHERE cod_barras = '{codBarras}'" 
				mycursor.execute(sql)
				myresultado = mycursor.fetchone()
				id_art = myresultado[0]
				provBase = myresultado[1]
				estadoArt = myresultado[2]
				motivo = myresultado[3]
				mostrarArt = self.articulos.mostrarDatosArt(codBarras)
				sql = f"SELECT id_art, id_solicitud, cant_art FROM Solicitud_Descripcion WHERE id_art = '{id_art}' AND id_solicitud = '{id_solicitud}' " 
				mycursor.execute(sql)
				myresultado = mycursor.fetchone()
				if myresultado is not None:
					print("-" * 65)
					print("  Este Artículo ya fue Ingresado en el mismo pedido")
					print("          No puede volver a ingresarlo")
					#desea modificar el dato ingresado?
					print("-" * 65)
				elif id_prov != provBase:
					print("  Error. Este artículo es de un Proveedor distinto.")
					print("-" * 65)
					print("             Vuelva a Ingresar")
					print("-" * 65)
				elif estadoArt != 1:
					print("  Error. Este artículo no se encuentra Activo.")
					print("-" * 65)
					print(f" MOTIVO: {motivo.upper()}")
					print("-" * 65)
					print("          Vuelva a Ingresar")
					print("-" * 65)
				else:
					stock = validaciones.validar_stock("a Pedir")
					print("-" * 65)
					print("    ¿Confirma el ingreso de los datos?")
					print("-" * 65)
					confirmacion = validaciones.siNo()
					if confirmacion == 1:
						sql = f"INSERT INTO Solicitud_Descripcion(id_solicitud,id_art,cant_art) VALUES (%d,%d,%d)"
						val = [id_solicitud,id_art,stock]
						mycursor.execute(sql, val)
						self.mydb.commit()
						contador = contador + 1
					validaciones.limpiarPantalla()
					print("-" * 65)
					print("  ¿Desea Agregar más Artículos al Pedido?")
					print("-" * 65)
					nro = validaciones.siNo()
					if nro == 1:
						validaciones.limpiarPantalla()
					elif nro == 2 and contador == 0:
						validaciones.limpiarPantalla()
						print("-" * 65)
						print("  ERROR.\nEl pedido debe tener por lo menos un artículo.")
						print("-" * 65)
						print("             Vuelva a Ingresar")
						print("-" * 65)
					else:
						validaciones.limpiarPantalla()
						print("-" * 70)
						print("                     PEDIDO GENERADO CON ÉXITO")
						print("-" * 70)
						mostrar = self.mostrarPedido(id_solicitud, id_prov, fechaSolicitud, hora, "PEDIDA")
						validaciones.esperar_y_limpiar()
						submenus.submenu_proveedor()
						ok = False
						
							
	def devolucionArt(self):
		print("-" * 65)
		print("                  PEDIDO DEVOLUCIÓN")
		print("-" * 65)
		mycursor = self.mydb.cursor()
		codBarras = self.articulos.artNoEncontrado()
		if codBarras:
			sql = f"SELECT a.id_art, a.id_proveedor, a.stock_art, p.nombre_empresa, p.id_estado, a.id_estado FROM Articulos as a INNER JOIN Proveedores as p ON a.id_proveedor = p.id_proveedor WHERE cod_barras = '{codBarras}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			self.articulos.mostrarDatosArt(codBarras)
			id_art = myresultado[0]
			id_prov = myresultado[1]
			stock_art = myresultado[2]
			nomEmpresa = myresultado[3]
			estadoProv = myresultado[4]
			estadoArt = myresultado[5]
			if stock_art == 0:
				print("-" * 65)	
				print("  Error. No se registra Stock del Artículo.")
				print("-" * 65)
			elif estadoProv != 1:
				print("-" * 65)	
				print("  Error. El Estado del Proveedor es Baja.")
				print("  Tiene que estar en estado Activo, para generar la devolución.")
				print("-" * 65)
			else:			
				motivo = validaciones.motivoDevolucion()
				fechaSolicitud = datetime.date.today()
				horaSolicitud = datetime.datetime.now().time()
				hora = horaSolicitud.strftime('%H:%M:%S')
				sql = f"INSERT INTO Solicitudes(id_proveedor,fecha_solicitud,hora_solicitud ,tipo_solicitud,estado_solicitud, observaciones) VALUES (%d,%s,%s,%s,%s,%s)"
				val = [id_prov,fechaSolicitud,horaSolicitud,'D','A', motivo]
				mycursor.execute(sql, val)
				self.mydb.commit()
				while True:
					stock = validaciones.validar_stock("a Devolver")
					if stock > stock_art:
						print("  Error. La cantidad ingresada es mayor a la existente.")
						print("-" * 65)
						print("          Vuelva a Ingresar")
						print("-" * 65)
					else:
						break
				sql = f"SELECT id_solicitud FROM Solicitudes WHERE id_proveedor = '{id_prov}' AND fecha_solicitud = '{fechaSolicitud}' AND hora_solicitud = '{hora}'" 
				mycursor.execute(sql)
				myresultado = mycursor.fetchone()
				id_solicitud = myresultado[0]
				sql = f"INSERT INTO Solicitud_Descripcion(id_solicitud,id_art,cant_art) VALUES (%d,%d,%d)"
				val = [id_solicitud,id_art,stock]
				mycursor.execute(sql, val)
				self.mydb.commit()
				updateStock = stock_art - stock
				sql = f"UPDATE Articulos SET stock_art = '{updateStock}' WHERE id_art = '{id_art}'"
				mycursor.execute(sql)
				self.mydb.commit()	
				print("-" * 65)
				validaciones.esperar_y_limpiar()
				print("-" * 70)
				print("                              PEDIDO DEVOLUCIÓN")
				print("-" * 70)
				mostrar = self.mostrarPedido(id_solicitud, id_prov, fechaSolicitud, hora , "A DEVOLVER")
			
		validaciones.esperar_y_limpiar()
		submenus.submenu_proveedor()
			
	def registrarDevolucion(self):
		mycursor = self.mydb.cursor()
		print("-" * 65)
		print("              REGISTRAR DEVOLUCIÓN")
		print("-" * 65)
		id_solicitud = validaciones.validar_idSolicitud()
		existeId = self.buscarId_Solicitud(id_solicitud)
		if existeId == False:
			print("-" * 65)
			print("Lo siento.")
			print(f"El N° de Solicitud: {id_solicitud} no se encuentra Registrado")
			print("-" * 65)
		else:
			mycursor = self.mydb.cursor()
			sql = f"SELECT estado_solicitud, tipo_solicitud FROM Solicitudes WHERE id_solicitud = '{id_solicitud}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			estado = myresultado[0]
			tipo_solicitud = myresultado[1]
			if estado == 'F' and tipo_solicitud == 'D':
				print("-" * 65)
				print(f"Error. El N° de Solicitud: {id_solicitud}")
				print("Ya se Registró la Devolución")
				print("-" * 65)
			elif tipo_solicitud == 'P':
				print("-" * 65)
				print(f"Error. El N° de Solicitud: {id_solicitud}")
				print("No es una Devolución, es un Pedido")
				print("-" * 65)
			else:
				fechaRegistro = datetime.date.today()
				horaRegistro = datetime.datetime.now().time()
				horaR = horaRegistro.strftime('%H:%M:%S')
				fechaR = fechaRegistro.strftime('%d/%m/%Y')
				fec_horaR =f"{fechaR} {horaR}".center(30)
				sql = f"UPDATE Solicitudes SET fecha_deIngreso = '{fechaRegistro}', hora_deIngreso = '{horaRegistro}', estado_solicitud = 'F' WHERE id_solicitud = '{id_solicitud}'"
				mycursor.execute(sql)
				self.mydb.commit()	
				sql = f"SELECT s.id_solicitud, p.cuit_pro, sd.cant_art, a.nom_art, a.cod_barras, p.nombre_empresa, s.fecha_solicitud, s.hora_solicitud, s.observaciones FROM Solicitudes as s INNER JOIN Proveedores as p ON s.id_proveedor = p.id_proveedor INNER JOIN Solicitud_Descripcion as sd ON s.id_solicitud = sd.id_solicitud INNER JOIN Articulos as a ON sd.id_art = a.id_art WHERE s.id_solicitud = '{id_solicitud}'"
				mycursor.execute(sql)
				myresultado = mycursor.fetchone()
				cant_art = myresultado[2]
				fechaSolicitud = myresultado[6]
				horaSolicitud = myresultado[7]
				fechaS = fechaSolicitud.strftime('%d/%m/%Y')
				fec_horaS =f"{fechaS} {horaSolicitud}".center(30)
				sql = f"UPDATE Solicitud_Descripcion SET cant_deIngreso = '{cant_art}' WHERE id_solicitud = '{id_solicitud}'"
				mycursor.execute(sql)
				self.mydb.commit()
				id_solicitud = str(id_solicitud)
				cant_art = str(cant_art)
				print("-" * 65)
				print("         DEVOLUCIÓN REGISTRADA CON ÉXITO")
				print("-" * 65)
				print("    N° SOLICITUD:         ", id_solicitud.center(30))
				print("    Código de Barras:     ", myresultado[4].center(30))
				print("    Nombre - Descripción: ", myresultado[3].center(30).upper())
				print("    Cantidad Devuelta:    ", cant_art.center(30))
				print("    CUIT PROVEEDOR:       ", myresultado[1].center(30))
				print("    Nombre Empresa:       ", myresultado[5].center(30).title())
				print("    Fecha Solicitud:      ", fec_horaS)
				print("    Fecha Devolución:     ", fec_horaR)
				print("    Observaciones:        ", myresultado[8].center(30).upper())
				print("    Estado Solucitud:     ", "FINALIZADO".center(30))
				print("-" * 65)
		
		validaciones.esperar_y_limpiar()
		submenus.submenu_proveedor()
				
	def registrarReposicion(self):
		mycursor = self.mydb.cursor()
		print("-" * 65)
		print("             REGISTRAR REPOSICIÓN")
		print("-" * 65)
		id_solicitud = validaciones.validar_idSolicitud()
		existeId = self.buscarId_Solicitud(id_solicitud)
		if existeId == False:
			print("-" * 65)
			print("Lo siento.")
			print(f"El N° de Solicitud: {id_solicitud} no se encuentra Registrado")
			print("-" * 65)
			validaciones.esperar_y_limpiar()
			submenus.submenu_articulos()
		else:
			sql = f"SELECT estado_solicitud, tipo_solicitud FROM Solicitudes WHERE id_solicitud = '{id_solicitud}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			estado = myresultado[0]
			tipo_solicitud = myresultado[1]
			if estado == 'F' and tipo_solicitud == 'P':
				print("-" * 65)
				print(f"Error. El N° de Solicitud: {id_solicitud}")
				print("Ya se Registró la Reposición")
				print("-" * 65)
				validaciones.esperar_y_limpiar()
				submenus.submenu_articulos()
			elif tipo_solicitud == 'D':
				print("-" * 65)
				print(f"Error. El N° de Solicitud: {id_solicitud}")
				print("No es un Pedido, es una Devolución")
				print("-" * 65)
				validaciones.esperar_y_limpiar()
				submenus.submenu_articulos()
			else:		
				fechaRegistro = datetime.date.today()
				horaRegistro = datetime.datetime.now().time()
				sql = f"UPDATE Solicitudes SET fecha_deIngreso = '{fechaRegistro}', hora_deIngreso = '{horaRegistro}', estado_solicitud = 'F' WHERE id_solicitud = '{id_solicitud}'"
				mycursor.execute(sql)
				self.mydb.commit()
				self.stockIngresado(id_solicitud)
				
	def stockIngresado(self, id_solicitud):
		mycursor = self.mydb.cursor()
		sql = f"SELECT a.cod_barras, a.nom_art,s.cant_art, a.stock_art, a.id_art FROM Solicitud_Descripcion as s INNER JOIN Articulos as a ON a.id_art = s.id_art WHERE s.id_solicitud = '{id_solicitud}'"
		mycursor.execute(sql)
		myresultado = mycursor.fetchall()
		for row in myresultado:
			print("-" * 65)
			print("            INGRESAR CANTIDAD")
			print("-" * 65)
			print("-" * 65)
			print(f"Código Barras: {row[0]}\nNombre: {row[1].upper()}\nCantidad Pedida: {row[2]}")
			print("-" * 65)
			codBarras = row[0]
			stockPedido = row[2]
			stockEnTienda = row[3]
			id_articulo = row[4]
			while True:
				stock = validaciones.validar_stock("que Ingresa")
				if stock > stockPedido:
					print("Error. Ingresó una cantidad mayor a la Pedida.")
					print("-" * 65)
					print("          Vuelva a Ingresar")
					print("-" * 65)
				else:
					sql = f"UPDATE Solicitud_Descripcion SET cant_deIngreso = '{stock}' WHERE id_solicitud = '{id_solicitud}' AND id_art = '{id_articulo}'"
					mycursor.execute(sql)
					self.mydb.commit()
					stockEnTienda = stockEnTienda + stock
					sql = f"UPDATE Articulos SET stock_art = '{stockEnTienda}' WHERE cod_barras = '{codBarras}'"
					mycursor.execute(sql)
					self.mydb.commit()
					validaciones.limpiarPantalla()
					break
		sql = f"SELECT a.cod_barras,a.nom_art,a.precio_art, s.id_art FROM Solicitud_Descripcion as s INNER JOIN Articulos as a ON a.id_art = s.id_art WHERE s.id_solicitud = '{id_solicitud}'"
		mycursor.execute(sql)
		myresultado = mycursor.fetchall()
		for row in myresultado:
			valido = 0
			print("-" * 65)
			print("            INGRESAR PRECIO")
			print("-" * 65)
			print("-" * 65)
			print(f"Código Barras: {row[0]}\nNombre: {row[1].upper()}\nPrecio: ${row[2]}")
			print("-" * 65)
			codBarras = row[0]
			precio_art = row[2]
			id_articulo = row[3]
			nombre = row[1]
			print("-" * 65)
			print("IMPORTANTE: ")
			print("           SI NO DESEA MODIFICAR EL PRECIO ")
			print("            APRIETE EL NÚMERO: 0 Y ENTER")
			print("-" * 65)
			while valido == 0:
				precioActual = validaciones.validarPrecio("modi")
				if precio_art == 0 and stock != 0 and precioActual == 0:
					print("Error. El Precio del Artículo no puede ser $0.")
					print("-" * 65)
					print("          Vuelva a Ingresar")
					print("-" * 65)
				else:
					if precioActual == 0 and precio_art != 0:
						print("-" * 65)
						print("Queda registrado el Precio Anterior")
						print("-" * 65)
						sql = f"UPDATE Articulos SET precio_art = '{precio_art}' WHERE cod_barras = '{codBarras}'"
						mycursor.execute(sql)
						self.mydb.commit()
						valido = 1
					else:
						sql = f"UPDATE Articulos SET precio_art = '{precioActual}' WHERE cod_barras = '{codBarras}'"
						mycursor.execute(sql)
						self.mydb.commit()
						valido = 1
					
		validaciones.limpiarPantalla()
		self.mostrarReposicion(id_solicitud)
	
	def mostrarReposicion(self,id_solicitud):
		mycursor = self.mydb.cursor()
		sql = f"SELECT p.cuit_pro, p.nombre_empresa, s.fecha_solicitud, s.hora_solicitud, s.fecha_deIngreso, s.hora_deIngreso FROM Solicitudes as s INNER JOIN Proveedores as p ON s.id_proveedor = p.id_proveedor WHERE id_solicitud = '{id_solicitud}'"
		mycursor.execute(sql)
		myresultado = mycursor.fetchone()
		cuit = myresultado[0]
		nomEmpresa = myresultado[1]
		fechaSol = myresultado[2]
		horaSol = myresultado[3]
		fechaIn = myresultado[4]
		horaIn = myresultado[5]
		fechaS = fechaSol.strftime('%d/%m/%Y')
		fechaI = fechaIn.strftime('%d/%m/%Y')
		print("-" * 120)
		print("                               REPOSICIÓN REGISTRADA CON ÉXITO")
		print("-" * 120)
		print("-" * 120)
		print(f"                                     SOLICITUD N°: {id_solicitud}")
		print("-" * 120)
		print(f"  FECHA PEDIDO: {fechaS}                                         HORA: {horaSol}")
		print("")
		print(f" EMPRESA: {myresultado[1].upper()}")
		print(f" CUIT: {myresultado[0]}")
		print("")
		print(f" FECHA INGRESO: {fechaI}                                         HORA: {horaIn}")
		sql = f"SELECT a.cod_barras as 'CODIGO BARRAS', a.nom_art as 'NOMBRE - DESCRIPCION', sd.cant_art as 'CANT. PEDIDA',sd.cant_deIngreso as 'CANT. INGRESA', a.stock_art as 'STOCK TOTAL', a.precio_art as 'PRECIO' FROM Solicitud_Descripcion as sd INNER JOIN Articulos as a ON sd.id_art = a.id_art WHERE sd.id_solicitud = '{id_solicitud}'"
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.submenu_articulos()
		
	
	#despues agregarle la cantidad que ingreso realmente, en un for que muestre cuanto se habia pedido 
	
	#Solicitudes(id_solicitud INT , id_proveedor INT, fecha_solicitud DATE ,hora_solicitud TIME,
	#fecha_deIngreso DATE ,hora_deIngreso TIME,tipo_solicitud ,estado_solicitud observaciones
	#Solicitud_Descripcion(id_solicitud INT NOT NULL, id_art INT,cant_art INT ,cant_deIngreso INT


	#fechaSolicitud = datetime.date.today()
	#fechaSolicitud = datetime.datetime.strftime(fechaSolicitud, '%d/%m/%Y')
	#hora_actual = datetime.datetime.now().time()
	#fecha_actual = datetime.date.today()
	#hora = hora_actual.strftime('%H:%M:%S')
	#hora_minutos = hora_actual.strftime('%H:%M')
	
