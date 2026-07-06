from Bd_Nutrite import bd_Nutrite
from articulos import Articulos
import validaciones
import mariadb
import submenus


class Proveedores(bd_Nutrite):
	def __init__(self):
		super().__init__()
		
	#FALTA REPOSICIÓN PROVEEDOR
	#DEVOLUCIÓN DE ARTÍCULOS
	
	def mostrarDatosProv(self,cuit):
		mycursor = self.mydb.cursor()
		sql = f"SELECT p.id_proveedor,p.cuit_pro, p.nombre_empresa, p.tel_pro, p.dir_pro, p.mail_pro, i.condicion_iva, e.tipo_estado FROM Proveedores as p INNER JOIN IVA as i ON p.id_iva = i.id_iva INNER JOIN Estado as e ON p.id_estado = e.id_estado WHERE cuit_pro = {cuit}"
		mycursor.execute(sql)
		myresultado = mycursor.fetchone()
		print("-" * 65)
		print("                   DATOS DEL PROVEEDOR: ")
		print("-" * 65)
		id_prov = myresultado[0]
		id_prov = str(id_prov)
		print("    |  ID - Proveedor:   ", id_prov.center(30), " | ")
		print("    |  CUIT:             ", myresultado[1].center(30), " | ")
		print("    |  Nombre Empresa:   ", myresultado[2].center(30).title(), " | ")
		print("    |  Teléfono:         ", myresultado[3].center(30), " | ")
		print("    |  Dirección:        ", myresultado[4].center(30).title(), " | ")
		print("    |  Mail:             ", myresultado[5].center(30), " | ")
		print("    |  Situación IVA:    ", myresultado[6].center(30), " | ")
		print("    |  Estado Proveedor: ", myresultado[7].center(30), " | ")
		
	def buscarCuit(self, cuit_user):
		encontrado = False
		mycursor = self.mydb.cursor()
		sql = "SELECT cuit_pro FROM Proveedores"
		mycursor.execute(sql)
		myresultado = mycursor.fetchall()
		for tupla in myresultado:	
			cuit = tupla[0]
			if cuit_user == cuit:
				encontrado = True
				break
		return encontrado
	
	def provNoEncontrado(self):
		cuit = validaciones.validar_cuit()
		existeCuit = self.buscarCuit(cuit)
		if existeCuit == False:
			print("-" * 65)
			print("Lo siento.")
			print(f"El CUIT: {cuit} no se encuentra Registrado")
			print("-" * 65)
		else:
			return cuit
		
	def registroProveedor(self):
		cuit = validaciones.validar_cuit()
		existeCuit = self.buscarCuit(cuit)
		if existeCuit == True:
			print("-" * 65)
			print("                      Lo siento.")
			print("      No se puede agregar este CUIT ya está registrado")
			print("-" * 65)
			self.mostrarDatosProv(cuit)
			print("-" * 65)
			validaciones.esperar_y_limpiar()
			submenus.submenu_proveedor()	
		else:
			print("-" * 65)
			print("                NUEVO PROVEEDOR")
			print("-" * 65)
			nomEmpresa = validaciones.validar_nomEmpresa()
			direccion = validaciones.validar_dirProveedor()
			telefono = validaciones.validarTelefonoCliente()
			mail = validaciones.mail()
			iva = validaciones.validarIva()
			self.nuevoProveedor(cuit, nomEmpresa,direccion,telefono, mail, iva)
	
	def checkProv_Articulo(self):
		art = Articulos()
		cuit = validaciones.validar_cuit()
		existeCuit = self.buscarCuit(cuit)
		if existeCuit == False:
			print("-" * 65)
			print("                      Lo siento.")
			print("             Este CUIT NO está registrado")
			print("-" * 65)
			print("         ¿Desea Agregar un Nuevo Proveedor?")
			print("-" * 65)
			nro = validaciones.siNo()
			if nro == 1:
				nomEmpresa = validaciones.validar_nomEmpresa()
				direccion = validaciones.validar_dirProveedor()
				telefono = validaciones.validarTelefonoCliente()
				mail = validaciones.mail()
				iva = validaciones.validarIva()
				self.nuevoProveedor(cuit, nomEmpresa,direccion,telefono, mail, iva, "art")
			else:
				validaciones.limpiarPantalla()
				submenus.submenu_articulos()	
		else:
			validaciones.limpiarPantalla()
			print("-" * 65)
			print("            NUEVO ARTÍCULO")
			print("-" * 65)
			art.registroArticulo(cuit)
			del art
			
	
	def nuevoProveedor(self, cuit, nomEmpresa, direccion, telefono, mail,iva, parametro = ""):
		sql = "INSERT INTO Proveedores(cuit_pro, nombre_empresa, tel_pro, dir_pro, mail_pro, id_iva, id_estado) VALUES (%s,%s,%s,%s,%s,%d,%d)"
		val = [cuit,nomEmpresa, telefono,direccion, mail, iva, 1]
		mycursor = self.mydb.cursor()
		mycursor.execute(sql, val)
		self.mydb.commit()
		print("-" * 65)
		print("           Proveedor Agregado con Éxito!")
		print("-" * 65)
		self.mostrarDatosProv(cuit)
		print("-" * 65)
		validaciones.esperar_y_limpiar()
		if parametro == "art":
			art = Articulos()
			art.registroArticulo(cuit)
			del art
		else:
			submenus.submenu_proveedor()
	
	def modificarProveedor(self):
		acc = 0
		cuit = self.provNoEncontrado()
		if cuit:
			print("-" * 65)
			self.mostrarDatosProv(cuit)
			print("-" * 65)
			mycursor = self.mydb.cursor()
			sql = f"SELECT nombre_empresa, tel_pro, dir_pro, mail_pro, id_iva, id_estado FROM Proveedores WHERE cuit_pro = {cuit}"
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
				nomEmpresa = validaciones.validar_nomEmpresa("modi")
				telefono = validaciones.validarTelefonoCliente("modi")
				direccion = validaciones.validar_dirProveedor("modi")
				mail = validaciones.mail("modi")
				iva = validaciones.validarIva("modi")
				if nomEmpresa != '0' and nomEmpresa != nomAnterior:
					sql = f"UPDATE Proveedores SET nombre_empresa = '{nomEmpresa}' WHERE cuit_pro = '{cuit}'"
					mycursor.execute(sql)
					self.mydb.commit()
					acc += 1
				if telefono != '0' and telefono != telAnterior:
					sql = f"UPDATE Proveedores SET tel_pro = '{telefono}' WHERE cuit_pro = '{cuit}'"
					mycursor.execute(sql)
					self.mydb.commit()	
					acc +=1
				if direccion != '0' and direccion != dirAnterior:
					sql = f"UPDATE Proveedores SET dir_pro = '{direccion}' WHERE cuit_pro = '{cuit}'"
					mycursor.execute(sql)
					self.mydb.commit()
					acc += 1
				if mail != '0' and mail != mailAnterior:
					sql = f"UPDATE Proveedores SET mail_pro = '{mail}' WHERE cuit_pro = '{cuit}'"
					mycursor.execute(sql)
					self.mydb.commit()
					acc += 1
				if iva != 0 and iva != ivaAnterior:
					sql = f"UPDATE Proveedores SET id_iva = '{iva}' WHERE cuit_pro = '{cuit}'"
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
					print("         Proveedor Modificado con Éxito!")
					print("-" * 65)
					self.mostrarDatosProv(cuit)
					print("-" * 65)
		validaciones.esperar_y_limpiar()
		submenus.submenu_proveedor()
		
	def check_bajaProveedor(self):
		cuit = self.provNoEncontrado()
		if cuit:
			mycursor = self.mydb.cursor()
			sql = f"SELECT id_estado, id_proveedor FROM Proveedores WHERE cuit_pro = {cuit}"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			idEstado = myresultado[0]
			id_prov = myresultado[1]

			eliminarProveedor = 2
			if idEstado == eliminarProveedor:
				print("-" * 65)
				print("  Lo siento. No se puede dar de Baja a este Proveedor")
				print("               Ya está dado de Baja")
				print("-" * 65)
				print("-" * 65)
				self.mostrarDatosProv(cuit)
				print("-" * 65)
			else:
				sql = f"SELECT estado_solicitud FROM Solicitudes WHERE id_proveedor = {id_prov}"
				mycursor.execute(sql)
				myresultado_solicitudes = mycursor.fetchall()
				hay_solicitudes_pendientes = any(row[0] == 'A' for row in myresultado_solicitudes)
				if hay_solicitudes_pendientes:
					print("-" * 65)
					print("  Lo siento. No se puede dar de Baja a este Proveedor")
					print("      Hay Pedido o Devolución Pendiente.")
					print("-" * 65)
					sql_solicitudes = f"SELECT s.id_solicitud as 'REMITO N°', p.cuit_pro as 'CUIT',s.fecha_solicitud as 'FECHA', s.hora_solicitud as 'HORA', s.tipo_solicitud as 'TIPO' FROM Solicitudes as s INNER JOIN Proveedores as p ON s.id_proveedor = p.id_proveedor WHERE s.id_proveedor = '{id_prov}' AND s.estado_solicitud = 'A'" 
					super().mostrarTablas(sql_solicitudes)
				else:
					self.mostrarDatosProv(cuit)
					print("-" * 65)
					print("-" * 65)
					print("    ¿Está seguro de dar de Baja a este Proveedor?")
					advertencia =  validaciones.siNo()
					print("-" * 65)
					if advertencia == 1:
						self.bajaProveedor(cuit,eliminarProveedor)
					elif advertencia == 2:
						validaciones.limpiarPantalla()
						print("-" * 65)
						print("       ELIGIÓ NO DAR DE BAJA AL PROVEEDOR")
						print("-" * 65)
		validaciones.esperar_y_limpiar()
		submenus.submenu_proveedor()
			
	def bajaProveedor(self,cuit,eliminarProveedor):
		motivo = validaciones.motivoBaja()
		mycursor = self.mydb.cursor()
		sql = f"UPDATE Proveedores SET id_estado = '{eliminarProveedor}', motivo_baja = '{motivo}' WHERE cuit_pro = '{cuit}'"
		mycursor.execute(sql)
		self.mydb.commit()
		validaciones.limpiarPantalla()
		print("-" * 65)
		print("          Proveedor dado de Baja")
		print("-" * 65)
		self.mostrarDatosProv(cuit)
		print("-" * 65)
		print(f"         MOTIVO BAJA: {motivo.upper()}")
		print("-" * 65)

	def reactivarProveedor(self):
		reactivarProv = 1
		cuit = self.provNoEncontrado()
		if cuit:
			mycursor = self.mydb.cursor()
			sql = f"SELECT id_estado, id_proveedor, motivo_baja FROM Proveedores WHERE cuit_pro = '{cuit}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			idEstado = myresultado[0]
			id_proveedor = myresultado[1]
			motivo = myresultado[2]
			if idEstado == reactivarProv:
				print("-" * 65)
				print("   Lo siento. No se puede Reactivar esta Cuenta")
				print("                Ya está Activa")
				print("-" * 65)
				self.mostrarDatosProv(cuit)
				print("-" * 65)
			else:
				self.mostrarDatosProv(cuit)
				print("-" * 65)
				print(" |  MOTIVO BAJA: ", motivo.upper() ," | ")
				print("-" * 65)
				print("-" * 65)
				print("    ¿Está seguro de Reactivar al Proveedor?")
				advertencia = validaciones.siNo()
				print("-" * 65)
				if advertencia == 1:
					mycursor = self.mydb.cursor()
					sql = f"UPDATE Proveedores SET id_estado = '{reactivarProv}', motivo_baja = NULL WHERE cuit_pro = '{cuit}'"
					mycursor.execute(sql)
					self.mydb.commit()
					validaciones.limpiarPantalla()
					print("-" * 65)
					print("                    CUENTA REACTIVADA")
					print("-" * 65)
					self.mostrarDatosProv(cuit)
					print("-" * 65)
				elif advertencia == 2:
					validaciones.limpiarPantalla()
					print("-" * 65)
					print("             ELIGIÓ NO REACTIVAR LA CUENTA")
					print("-" * 65)
		validaciones.esperar_y_limpiar()
		submenus.submenu_proveedor()
		
	def verProveedores(self):
		print("-" * 140)
		print("                                 VER TODOS LOS PROVEEDORES")
		print("-" * 140)
		mycursor = self.mydb.cursor()
		sql = f"SELECT p.id_proveedor as ID ,p.cuit_pro as CUIT, p.nombre_empresa as EMPRESA, p.tel_pro as TELEFONO, p.dir_pro as DIRECCION, p.mail_pro as EMAIL, i.condicion_iva as 'CONDICION IVA', e.tipo_estado as ESTADO FROM Proveedores as p INNER JOIN IVA as i ON p.id_iva = i.id_iva INNER JOIN Estado as e ON p.id_estado = e.id_estado"
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_proveedores()
		
	def verProveedoresBaja(self):
		id_estado = 2
		print("-" * 100)
		print("                                VER PROVEEDORES DE BAJA")
		print("-" * 100)
		mycursor = self.mydb.cursor()
		sql = f"SELECT p.id_proveedor as ID,p.cuit_pro as CUIT, p.nombre_empresa as EMPRESA, p.tel_pro as TELEFONO, p.dir_pro as DIRECCION, p.mail_pro as EMAIL, i.condicion_iva 'CONDICION IVA', p.motivo_baja as 'MOTIVO BAJA' FROM Proveedores as p INNER JOIN IVA as i ON p.id_iva = i.id_iva WHERE p.id_estado = '{id_estado}'"
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_proveedores()
		
	def verBajoStock(self):
		mycursor = self.mydb.cursor()
		maximo = 4
		minimo = 0		
		print("-" * 100)
		print("                                 BAJO  STOCK")
		print("-" * 100)
		sql = f"SELECT p.cuit_pro as CUIT, p.nombre_empresa as EMPRESA, a.cod_barras as 'CODIGO BARRAS', a.nom_art as NOMBRE, a.stock_art as 'STOCK' FROM Proveedores as p INNER JOIN Articulos as a ON p.id_proveedor = a.id_proveedor WHERE a.stock_art < '{maximo}' AND a.stock_art > '{minimo}'"
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_proveedores()
	
	def proveedorPorNombre(self):
		print("-" * 65)
		print("        CONSULTAR PROVEEDORES POR NOMBRE")
		print("-" * 65)
		nombre = validaciones.consultar_por_nombre("Proveedor")
		sql = f"SELECT  p.id_proveedor as ID ,p.cuit_pro as CUIT, p.nombre_empresa as EMPRESA, p.tel_pro as TELEFONO, p.dir_pro as DIRECCION, p.mail_pro as EMAIL, i.condicion_iva as 'CONDICION IVA', e.tipo_estado as ESTADO FROM Proveedores as p INNER JOIN IVA as i ON p.id_iva = i.id_iva INNER JOIN Estado as e ON p.id_estado = e.id_estado WHERE p.nombre_empresa LIKE '%"+nombre+"%'"
		print("-" * 130)
		print(f"                                                           PROVEEDORES QUE CONTENGAN '{nombre.upper()}'")
		print("-" * 130)
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_proveedores()
