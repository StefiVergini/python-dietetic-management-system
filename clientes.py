from Bd_Nutrite import bd_Nutrite
import validaciones
import mariadb
import submenus


class Clientes(bd_Nutrite):
	def __init__(self):
		super().__init__()
	
	#FALTA CONSULTA QUIERO SABER QUE PIDE EXACTAMENTE 
	def mostrarDatosCli(self,cuil):
		mycursor = self.mydb.cursor()
		sql = f"SELECT c.id_cliente,c.cuil_t_cli ,c.nom_completo, c.tel_cli, c.dir_cli,c.mail_cli,i.condicion_iva, e.tipo_estado FROM Clientes as c INNER JOIN IVA as i ON c.id_iva = i.id_iva INNER JOIN Estado as e ON c.id_estado = e.id_estado WHERE cuil_t_cli = {cuil}"
		mycursor.execute(sql)
		myresultado = mycursor.fetchone()
		print("-" * 65)
		print("                        DATOS DEL CLIENTE: ")
		print("-" * 65)
		id_cliente = myresultado[0]
		id_cliente = str(id_cliente)
		print("    |  ID - Cliente:     ", id_cliente.center(30), " | ")
		print("    |  CUIL:             ", myresultado[1].center(30), " | ")
		print("    |  Nombre Completo:  ", myresultado[2].center(30).title(), " | ")
		print("    |  Teléfono:         ", myresultado[3].center(30), " | ")
		print("    |  Dirección:        ", myresultado[4].center(30).title(), " | ")
		print("    |  Mail:             ", myresultado[5].center(30), " | ")
		print("    |  Situación IVA:    ", myresultado[6].center(30), " | ")
		print("    |  Estado Cliente:   ", myresultado[7].center(30), " | ")
		
	def buscarCuil(self, cuil_user):
		encontrado = False
		mycursor = self.mydb.cursor()
		sql = "SELECT cuil_t_cli FROM Clientes"
		mycursor.execute(sql)
		myresultado = mycursor.fetchall()
		for tupla in myresultado:	
			cuil = tupla[0]
			if cuil_user == cuil:
				encontrado = True
				break
		return encontrado
		
	def clienteNoEncontrado(self):
		cuil = validaciones.validar_cuil()
		existeCuil = self.buscarCuil(cuil)
		if existeCuil == False:
			print("-" * 65)
			print("Lo siento.")
			print(f"El CUIL: {cuil} no se encuentra Registrado")
			print("-" * 65)
		else:
			return cuil
			
	def registroCliente(self):
		cuil = validaciones.validar_cuil()
		existeCuil = self.buscarCuil(cuil)
		if existeCuil == True:
			print("-" * 65)
			print("                      Lo siento.")
			print("      No se puede agregar este CUIL ya está registrado")
			print("-" * 65)
			self.mostrarDatosCli(cuil)
			print("-" * 65)
			validaciones.esperar_y_limpiar()
			submenus.submenu_clientes()	
		else:
			print("-" * 65)
			print("                  NUEVO CLIENTE")
			print("-" * 65)
			nomCompleto = validaciones.validarNombreCliente()
			direccion = validaciones.validarDireccion()
			telefono = validaciones.validarTelefonoCliente()
			mail = validaciones.mail()
			iva = validaciones.validarIva()
			self.nuevoCliente(cuil, nomCompleto,direccion,telefono, mail, iva)
	
	def nuevoCliente(self, cuil, nomCompleto, direccion, telefono, mail,iva):
		sql = "INSERT INTO Clientes(cuil_t_cli ,nom_completo, tel_cli, dir_cli,mail_cli,id_iva, id_estado) VALUES (%s,%s,%s,%s,%s,%d,%d)"
		val = [cuil,nomCompleto, telefono,direccion, mail, iva, 1]
		mycursor = self.mydb.cursor()
		mycursor.execute(sql, val)
		self.mydb.commit()
		validaciones.limpiarPantalla()
		print("-" * 65)
		print("             Cliente Agregado con Éxito!")
		print("-" * 65)
		self.mostrarDatosCli(cuil)
		print("-" * 65)
		validaciones.esperar_y_limpiar()
		submenus.submenu_clientes()	
	
	def modificarCliente(self):
		acc = 0
		cuil = self.clienteNoEncontrado()
		if cuil:
			if cuil == '00000000000':
				print("-" * 65)
				print("Lo siento.")
				print(f"El CUIL: {cuil} es nuestro Cliente Genérico")
				print("No se puede Modificar")
				print("-" * 65)
				self.mostrarDatosCli(cuil)
				print("-" * 65)
			else:
				print("-" * 65)
				self.mostrarDatosCli(cuil)
				print("-" * 65)
				mycursor = self.mydb.cursor()
				sql = f"SELECT nom_completo, tel_cli, dir_cli,mail_cli,id_iva, id_estado FROM Clientes WHERE cuil_t_cli = {cuil}"
				mycursor.execute(sql)
				myresultado = mycursor.fetchone()
				nomAnterior = myresultado[0]
				telAnterior = myresultado[1]
				dirAnterior = myresultado[2]
				mailAnterior = myresultado[3]
				ivaAnterior = myresultado[4]
				id_estado = myresultado[5]
				if id_estado != 1:
					print("-" * 65)
					print("    Lo siento. El cliente está dado de baja")
					print("        Debe reactivarlo para modificarlo")
					print("-" * 65)
				else:
					print("-" * 65)
					print("IMPORTANTE: ")
					print("           SI NO DESEA MODIFICAR UN DATO ")
					print("            APRIETE EL NÚMERO: 0 Y ENTER")
					print("-" * 65)
					nomCompleto = validaciones.validarNombreCliente("modi")
					telefono = validaciones.validarTelefonoCliente("modi")
					direccion = validaciones.validarDireccion("modi")
					mail = validaciones.mail("modi")
					iva = validaciones.validarIva("modi")
					
					if nomCompleto != '0' and nomCompleto != nomAnterior:
						sql = f"UPDATE Clientes SET nom_completo = '{nomCompleto}' WHERE cuil_t_cli = '{cuil}'"
						mycursor.execute(sql)
						self.mydb.commit()
						acc += 1
					if telefono != '0' and telefono != telAnterior:
						sql = f"UPDATE Clientes SET tel_cli = '{telefono}' WHERE cuil_t_cli = '{cuil}'"
						mycursor.execute(sql)
						self.mydb.commit()	
						acc +=1
					if direccion != '0' and direccion != dirAnterior:
						sql = f"UPDATE Clientes SET dir_cli = '{direccion}' WHERE cuil_t_cli = '{cuil}'"
						mycursor.execute(sql)
						self.mydb.commit()
						acc += 1
					if mail != '0' and mail != mailAnterior:
						sql = f"UPDATE Clientes SET mail_cli = '{mail}' WHERE cuil_t_cli = '{cuil}'"
						mycursor.execute(sql)
						self.mydb.commit()
						acc += 1
					if iva != 0 and iva != ivaAnterior:
						sql = f"UPDATE Clientes SET id_iva = '{iva}' WHERE cuil_t_cli = '{cuil}'"
						mycursor.execute(sql)
						self.mydb.commit()
						acc += 1
					if acc == 0:
						validaciones.limpiarPantalla()
						print("-" * 65)
						print("          NO REALIZÓ NINGUNA MODIFICACIÓN")
						print("-" * 65)
					else:
						validaciones.limpiarPantalla()
						print("-" * 65)
						print("           Cliente Modificado con Éxito!")
						print("-" * 65)
						self.mostrarDatosCli(cuil)
						print("-" * 65)
		validaciones.esperar_y_limpiar()
		submenus.submenu_clientes()
		
	def checkBajaCliente(self):
		cuil = self.clienteNoEncontrado()
		if cuil:
			if cuil == '00000000000':
				print("-" * 65)
				print("Lo siento.")
				print(f"El CUIL: {cuil} es nuestro Cliente Genérico")
				print("No se puede dar de Baja")
				print("-" * 65)
				self.mostrarDatosCli(cuil)
				print("-" * 65)
			else:
				mycursor = self.mydb.cursor()
				sql = f"SELECT id_estado, id_cliente FROM Clientes WHERE cuil_t_cli = {cuil}"
				mycursor.execute(sql)
				myresultado = mycursor.fetchone()
				idEstado = myresultado[0]
				id_cliente = myresultado[1]
				eliminarCliente = 2
				if idEstado == eliminarCliente:
					print("-" * 65)
					print("Lo siento. No se puede dar de Baja a este Cliente")
					print("            Ya está dado de Baja")
					print("-" * 65)
					print("-" * 65)
					self.mostrarDatosCli(cuil)
					print("-" * 65)
				else:
					self.mostrarDatosCli(cuil)
					print("-" * 65)
					print("-" * 65)
				print("      ¿Está seguro de dar de Baja a este Cliente?")
				advertencia = validaciones.siNo()
				print("-" * 65)
				if advertencia == 1:
					baja = self.bajaCliente(cuil,eliminarCliente)
				elif advertencia == 2:
					validaciones.limpiarPantalla()
					print("-" * 65)
					print("       ELIGIÓ NO DAR DE BAJA AL CLIENTE")
					print("-" * 65)
							
		validaciones.esperar_y_limpiar()
		submenus.submenu_clientes()
	
	
	def bajaCliente(self,cuil,eliminarCliente):
		motivo = validaciones.motivoBaja()
		mycursor = self.mydb.cursor()
		sql = f"UPDATE Clientes SET id_estado = '{eliminarCliente}', observacion_baja = '{motivo}' WHERE cuil_t_cli = '{cuil}'"
		mycursor.execute(sql)
		self.mydb.commit()
		validaciones.limpiarPantalla()
		print("-" * 65)
		print("               Cliente dado de Baja")
		print("-" * 65)
		self.mostrarDatosCli(cuil)
		print("-" * 65)
		print(f"         MOTIVO BAJA: {motivo.upper()}")
		print("-" * 65)
			
	def reactivarCliente(self):
		reactivarCliente = 1
		cuil = self.clienteNoEncontrado()
		if cuil:
			mycursor = self.mydb.cursor()
			sql = f"SELECT id_estado, id_cliente, observacion_baja FROM Clientes WHERE cuil_t_cli = '{cuil}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			idEstado = myresultado[0]
			id_cliente = myresultado[1]
			motivo = myresultado[2]
			if idEstado == reactivarCliente:
				print("-" * 65)
				print("Lo siento. No se puede Reactivar esta Cuenta")
				print("               Ya está Activa")
				print("-" * 65)
				self.mostrarDatosCli(cuil)
				print("-" * 65)
			else:
				self.mostrarDatosCli(cuil)
				print("-" * 65)
				print(" |  MOTIVO BAJA: ", motivo.upper() ," | ")
				print("-" * 65)
				print("-" * 65)
				print("    ¿Está seguro de Reactivar al Cliente?")
				advertencia = validaciones.siNo()
				if advertencia == 1:
					mycursor = self.mydb.cursor()
					sql = f"UPDATE Clientes SET id_estado = '{reactivarCliente}',observacion_baja = NULL WHERE cuil_t_cli = '{cuil}'"
					mycursor.execute(sql)
					self.mydb.commit()
					print("-" * 65)
					print("               CUENTA REACTIVADA")
					print("-" * 65)
					self.mostrarDatosCli(cuil)
					print("-" * 65)
				elif advertencia == 2:
					print("-" * 65)
					print("       ELIGIÓ NO REACTIVAR LA CUENTA")
					print("-" * 65)
				
		validaciones.esperar_y_limpiar()
		submenus.submenu_clientes()
	
	def verClientes(self):
		print("-" * 140)
		print("                                             VER TODOS LOS CLIENTES")
		print("-" * 140)
		mycursor = self.mydb.cursor()
		sql = f"SELECT c.id_cliente,c.cuil_t_cli ,c.nom_completo, c.tel_cli, c.dir_cli,c.mail_cli,i.condicion_iva, e.tipo_estado FROM Clientes as c INNER JOIN IVA as i ON c.id_iva = i.id_iva INNER JOIN Estado as e ON c.id_estado = e.id_estado"
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_clientes()
		
	def verClientesBaja(self):
		id_estado = 2
		print("-" * 100)
		print("                                       VER CLIENTES DE BAJA")
		print("-" * 100)
		mycursor = self.mydb.cursor()
		sql = f"SELECT c.id_cliente as ID,c.cuil_t_cli as CUIL,c.nom_completo as 'NOMBRE COMPLETO', c.tel_cli as TELEFONO, c.dir_cli as DIRECCION,c.mail_cli,i.condicion_iva as 'CONDICION IVA', c.observacion_baja as 'MOTIVO' FROM Clientes as c INNER JOIN IVA as i ON c.id_iva = i.id_iva WHERE c.id_estado = '{id_estado}'"
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_clientes()
		
	def verVentasCliente(self):
		cuil = self.clienteNoEncontrado()
		if cuil:
			mycursor = self.mydb.cursor()
			sql = f"SELECT id_cliente FROM Clientes WHERE cuil_t_cli = '{cuil}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			id_cliente = myresultado[0]
			print("-" * 90)
			print("                                   VER VENTAS POR CLIENTE")
			print("-" * 90)
			mycursor = self.mydb.cursor()
			sql = f"SELECT c.cuil_t_cli as CUIL ,c.nom_completo as NOMBRE, s.id_venta_cli as 'FACTURA N°', s.fecha_venta as FECHA, s.hora_venta as HORA, s.total_venta as 'TOTAL ABONADO' FROM Clientes as c INNER JOIN Ventas_cli as s ON c.id_cliente = s.id_cliente WHERE s.id_cliente = '{id_cliente}'"
			super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_clientes()
		
	def clientePorNombre(self):
		print("-" * 65)
		print("        CONSULTAR CLIENTES POR NOMBRE")
		print("-" * 65)
		nombre = validaciones.consultar_por_nombre("Cliente")
		sql = f"SELECT c.id_cliente as ID,c.cuil_t_cli as CUIL,c.nom_completo as 'NOMBRE COMPLETO', c.tel_cli as TELEFONO, c.dir_cli as DIRECCION ,c.mail_cli as EMAIL,i.condicion_iva as 'CONDICION IVA', e.tipo_estado as 'ESTADO' FROM Clientes as c INNER JOIN IVA as i ON c.id_iva = i.id_iva INNER JOIN Estado as e ON c.id_estado = e.id_estado WHERE c.nom_completo LIKE '%"+nombre+"%'"
		print("-" * 100)
		print(f"                             CLIENTES QUE CONTENGAN '{nombre.upper()}'")
		print("-" * 100)
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_clientes()
