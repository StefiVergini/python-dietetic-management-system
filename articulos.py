from Bd_Nutrite import bd_Nutrite
import validaciones
import mariadb
import submenus
#PRECIO SE PIDE EN EL ALTA O CUANDO INGRESA EL PEDIDO?

class Articulos(bd_Nutrite):
	def __init__(self):
		super().__init__()
	
	#FALTA CONSULTA QUIERO SABER QUE PIDE EXACTAMENTE 
		
	def mostrarDatosArt(self,codBarras):
		mycursor = self.mydb.cursor()
		sql = f"SELECT a.id_art, a.cod_barras, c.categoria_art,a.nom_art, a.cant_producto, a.tipo_medida, a.precio_art, a.stock_art,p.nombre_empresa,p.cuit_pro, e.tipo_estado FROM Articulos as a INNER JOIN Categoria_art as c ON a.id_categoria = c.id_categoria INNER JOIN Proveedores as p ON a.id_proveedor = p.id_proveedor INNER JOIN Estado as e ON a.id_estado = e.id_estado WHERE cod_barras = {codBarras}"
		mycursor.execute(sql)
		myresultado = mycursor.fetchone()
		print("-" * 65)
		print("                DATOS DEL ARTÍCULO: ")
		print("-" * 65)
		id_art = str(myresultado[0])
		precio= str(myresultado[6])
		stock = str(myresultado[7])
		unidad_de_venta = f"{myresultado[4]} {myresultado[5].lower()}".center(30)
		print("  |  ID - Artículo:        ", id_art.center(30),"|".center(10))
		print("  |  Código de Barras:     ", myresultado[1].center(30),"|".center(10))
		print("  |  Categoría:            ", myresultado[2].center(30).title(),"|".center(10))
		print("     Nombre - Descripción: ", myresultado[3].center(30).upper())
		print("     Unidad de Venta:      ", unidad_de_venta)
		print(f"     Precio:                            ${precio.ljust(30)}")
		print("     Stock Disponible:     ",stock.center(30))
		print("  |  Empresa Proveedor:    ", myresultado[8].center(30).title(),"|".center(10))
		print("  |  CUIT Proveedor:       ", myresultado[9].center(30),"|".center(10))
		print("  |  Estado Artículo:      ", myresultado[10].center(30),"|".center(10))
		print("-" * 65)
		
	def buscarCodBarras(self, codBarras):
		encontrado = False
		mycursor = self.mydb.cursor()
		sql = "SELECT cod_barras FROM Articulos"
		mycursor.execute(sql)
		myresultado = mycursor.fetchall()
		for tupla in myresultado:	
			codigo = tupla[0]
			if codBarras == codigo:
				encontrado = True
				break
		return encontrado

	def artNoEncontrado(self):
		cod = validaciones.validar_codBarras()
		existeCod = self.buscarCodBarras(cod)
		if existeCod == False:
			print("-" * 65)
			print("Lo siento.")
			print(f"El Código de Barras: {cod} no se encuentra Registrado")
			print("-" * 65)
		else:
			return cod
		
	def registroArticulo(self, cuitProv):
		cod = validaciones.validar_codBarras()
		existeCod = self.buscarCodBarras(cod)
		if existeCod == True:
			print("-" * 65)
			print("                      Lo siento.")
			print("  No se puede agregar este Artículo ya está registrado")
			print("-" * 65)
			self.mostrarDatosArt(cod)
			print("-" * 65)
			validaciones.esperar_y_limpiar()
			submenus.submenu_articulos()	
		else:
			print("-" * 65)
			print("                      NUEVO ARTÍCULO")
			print("-" * 65)
			nomArt = validaciones.validar_NombreArt()
			medida = validaciones.validar_medida()
			cant_produc = validaciones.validar_cantProducto()
			self.mostrarCategorias()
			id_categoria = validaciones.validar_categoria()
			mycursor = self.mydb.cursor()
			sql = f"SELECT id_proveedor FROM Proveedores WHERE cuit_pro = '{cuitProv}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			id_prov = myresultado[0]
			self.nuevoArticulo(cod, nomArt,cant_produc,medida, id_categoria,id_prov)
	
	#id_art,cod_barras, nom_art,cant_producto,tipo_medida,id_categoria, precio_art, stock_art, id_proveedor, id_estado
	def nuevoArticulo(self,codBarras, nomArt,cant_produc,medida, id_cagoria,id_prov):
		sql = "INSERT INTO Articulos(cod_barras, nom_art,cant_producto,tipo_medida,id_categoria, precio_art, stock_art, id_proveedor, id_estado) VALUES (%s,%s,%s,%s,%d,%s,%d,%d,%d)"
		val = [codBarras, nomArt,cant_produc,medida, id_cagoria,'0',0,id_prov,1]
		mycursor = self.mydb.cursor()
		mycursor.execute(sql, val)
		self.mydb.commit()
		validaciones.limpiarPantalla()
		print("-" * 65)
		print("                  Artículo Agregado con Éxito!")
		print("-" * 65)
		self.mostrarDatosArt(codBarras)
		print("-" * 65)
		validaciones.esperar_y_limpiar()
		submenus.submenu_articulos()	
	
	def mostrarCategorias(self):
		mycursor = self.mydb.cursor()
		sql = "SELECT id_categoria, categoria_art FROM Categoria_Art"
		mycursor.execute(sql)
		myresultado = mycursor.fetchall()
		print("-" * 65)
		print("          NRO CATEGORIA    |        CATEGORIAS      ")
		print("-" * 65)
		for tupla in myresultado:
			id_cat = tupla[0]
			categoria = tupla[1]
			print("         -  ",id_cat,"         ",categoria.center(30))
		print("-" * 65)
		
	def modificarArticulo(self):
		acc = 0
		cod = self.artNoEncontrado()
		if cod:
			validaciones.limpiarPantalla()
			print("-" * 65)
			self.mostrarDatosArt(cod)
			print("-" * 65)
			mycursor = self.mydb.cursor()
			sql = f"SELECT id_categoria,nom_art,tipo_medida,cant_producto, precio_art,stock_art,id_estado FROM Articulos WHERE cod_barras = {cod}"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			id_catAnterior = myresultado[0]
			nomAnterior = myresultado[1]
			tipoMedidaAnterior = myresultado[2]
			cant_productAnterior = myresultado[3]
			precioAnterior = myresultado[4]
			stock = myresultado[5]
			id_estado = myresultado[6]
			if id_estado != 1:
				print("-" * 65)
				print("    Lo siento. El artículo está dado de baja")
				print("        Debe reactivarlo para modificarlo")
				print("-" * 65)
			else:
				print("-" * 65)
				print("IMPORTANTE: ")
				print("           SI NO DESEA MODIFICAR UN DATO ")
				print("            APRIETE EL NÚMERO: 0 Y ENTER")
				print("-" * 65)
				nomArt = validaciones.validar_NombreArt("modi")
				medida = validaciones.validar_medida("modi")
				cant_produc = validaciones.validar_cantProducto("modi")
				self.mostrarCategorias()
				id_categoria = validaciones.validar_categoria("modi")
				if nomArt != '0' and nomArt != nomAnterior:
					sql = f"UPDATE Articulos SET nom_art = '{nomArt}' WHERE cod_barras = '{cod}'"
					mycursor.execute(sql)
					self.mydb.commit()
					acc += 1
				if medida != 0 and medida != tipoMedidaAnterior:
					sql = f"UPDATE Articulos SET tipo_medida = '{medida}' WHERE cod_barras = '{cod}'"
					mycursor.execute(sql)
					self.mydb.commit()	
					acc +=1
				if cant_produc != 0 and cant_produc != cant_productAnterior:
					sql = f"UPDATE Articulos SET cant_producto = '{cant_produc}' WHERE cod_barras = '{cod}'"
					mycursor.execute(sql)
					self.mydb.commit()
					acc += 1
				if id_categoria != 0 and id_categoria != id_catAnterior:
					sql = f"UPDATE Articulos SET id_categoria = '{id_categoria}' WHERE cod_barras = '{cod}'"
					mycursor.execute(sql)
					self.mydb.commit()
					acc += 1
				if stock != 0:
					precio = validaciones.validarPrecio("modi")
					if precio != 0 and precio != precioAnterior:
						sql = f"UPDATE Articulos SET precio_art = '{precio}' WHERE cod_barras = '{cod}'"
						mycursor.execute(sql)
						self.mydb.commit()
						acc += 1
				validaciones.limpiarPantalla()
				if acc == 0:
					print("-" * 65)
					print("             NO REALIZÓ NINGUNA MODIFICACIÓN")
					print("-" * 65)
				else:
					print("-" * 65)
					print("              Artículo Modificado con Éxito!")
					print("-" * 65)
					self.mostrarDatosArt(cod)
					print("-" * 65)
		validaciones.esperar_y_limpiar()
		submenus.submenu_articulos()
		
	def checkBajaArt(self):
		cod = self.artNoEncontrado()
		if cod:
			mycursor = self.mydb.cursor()
			sql = f"SELECT id_estado, id_art, stock_art FROM Articulos WHERE cod_barras = '{cod}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			idEstado = myresultado[0]
			id_art = myresultado[1]
			stock = myresultado[2]
			bajaArt = 2
			if idEstado == bajaArt:
				print("-" * 65)
				print("Lo siento. No se puede dar de Baja a este Artículo")
				print("            Ya está dado de Baja")
				print("-" * 65)
				self.mostrarDatosArt(cod)
			elif stock != 0:
				self.mostrarDatosArt(cod)
				print("-" * 65)
				print("Lo siento. No se puede dar de Baja a este Artículo")
				print("El Stock es Mayor a 0. No debe haber Stock para Vender")
				print("-" * 65)
			else:
				self.mostrarDatosArt(cod)
				print("-" * 65)
				print("    ¿Está seguro de dar de Baja a este Artículo?")
				advertencia = validaciones.siNo()
				print("-" * 65)
				if advertencia == 1:
					baja = self.bajaArt(cod,bajaArt)
				elif advertencia == 2:
					validaciones.limpiarPantalla()
					print("    ELIGIÓ NO DAR DE BAJA EL ARTÍCULO")
					print("-" * 65)

		validaciones.esperar_y_limpiar()
		submenus.submenu_articulos()
	
	
	def bajaArt(self,cod,bajaArt):
		motivo = validaciones.motivoBaja()
		mycursor = self.mydb.cursor()
		sql = f"UPDATE Articulos SET id_estado = '{bajaArt}', motivo_baja = '{motivo}' WHERE cod_barras = '{cod}'"
		mycursor.execute(sql)
		self.mydb.commit()
		validaciones.limpiarPantalla()
		print("-" * 65)
		print("            Artículo dado de Baja")
		print("-" * 65)
		self.mostrarDatosArt(cod)
		print("-" * 65)
		print(f"       MOTIVO BAJA: {motivo.upper()}")
		print("-" * 65)
			
	def reactivarArt(self):
		reactivarArt = 1
		cod = self.artNoEncontrado()
		if cod:
			mycursor = self.mydb.cursor()
			sql = f"SELECT id_estado, id_art, motivo_baja FROM Articulos WHERE cod_barras = '{cod}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			idEstado = myresultado[0]
			id_art = myresultado[1]
			motivo = myresultado[2]
			if idEstado == reactivarArt:
				print("-" * 65)
				print("Lo siento. No se puede Reactivar este Artículo")
				print("               Ya está Activo")
				print("-" * 65)
				self.mostrarDatosArt(cod)
				print("-" * 65)
			else:
				self.mostrarDatosArt(cod)
				print("-" * 65)
				print("MOTIVO BAJA: ", motivo.upper())
				print("-" * 65)
				print("-" * 65)
				print("   ¿Está seguro de Reactivar este Artículo?")
				advertencia = validaciones.siNo()
				print("-" * 65)
				if advertencia == 1:
					mycursor = self.mydb.cursor()
					sql = f"UPDATE Articulos SET id_estado = '{reactivarArt}', motivo_baja = NULL WHERE cod_barras = '{cod}'"
					mycursor.execute(sql)
					self.mydb.commit()
					validaciones.limpiarPantalla()
					print("-" * 65)
					print("                   ARTÍCULO REACTIVADO")
					print("-" * 65)
					self.mostrarDatosArt(cod)
				elif advertencia == 2:
					validaciones.limpiarPantalla()
					print("-" * 65)
					print("      ELIGIÓ NO REACTIVAR EL ARTÍCULO")
					print("-" * 65)
						
		validaciones.esperar_y_limpiar()
		submenus.submenu_articulos()

	def artSinStock(self):
		stock = 0
		id_estado = 1
		print("-" * 135)
		print("                                ARTÍCULOS SIN STOCK - ACTIVOS")
		print("-" * 135)
		mycursor = self.mydb.cursor()
		sql = f"SELECT a.cod_barras as 'CODIGO BARRAS',a.nom_art as 'NOMBRE - DESCRIPCION',c.categoria_art as 'CATEGORÍA', a.cant_producto as 'CANTIDAD', a.tipo_medida as 'MEDIDA',p.nombre_empresa as 'EMPRESA',p.cuit_pro as 'CUIT' FROM Articulos as a INNER JOIN Categoria_art as c ON a.id_categoria = c.id_categoria INNER JOIN Proveedores as p ON a.id_proveedor = p.id_proveedor WHERE a.stock_art = '{stock}' AND a.id_estado = '{id_estado}' ORDER BY p.nombre_empresa"
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.submenu_articulos()
	
	def verArticulos(self):
		print("-" * 140)
		print("                                   VER TODOS LOS ARTICULOS")
		print("-" * 140)
		mycursor = self.mydb.cursor()
		sql = f"SELECT a.cod_barras as 'CODIGO BARRAS',a.nom_art as 'NOMBRE', c.categoria_art as CATEGORIA,a.cant_producto CANTIDAD, a.tipo_medida as MEDIDA, a.precio_art as PRECIO, a.stock_art as STOCK, p.nombre_empresa as EMPRESA ,p.cuit_pro as CUIT ,e.tipo_estado as ESTADO FROM Articulos as a INNER JOIN Categoria_art as c ON a.id_categoria = c.id_categoria INNER JOIN Proveedores as p ON a.id_proveedor = p.id_proveedor INNER JOIN Estado as e ON a.id_estado = e.id_estado ORDER BY a.id_art"
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_articulos()
		
	def verArticulosBaja(self):
		id_estado = 2
		print("-" * 100)
		print("                                   VER ARTICULOS DE BAJA")
		print("-" * 100)
		mycursor = self.mydb.cursor()
		id_estado = 2
		sql = f"SELECT a.id_art as ID, a.cod_barras as 'CODIGO BARRAS',a.nom_art as 'NOMBRE', c.categoria_art as CATEGORIA,a.cant_producto CANTIDAD, a.tipo_medida as MEDIDA, a.precio_art as PRECIO, a.stock_art as STOCK, p.nombre_empresa as EMPRESA ,p.cuit_pro as CUIT FROM Articulos as a INNER JOIN Categoria_art as c ON a.id_categoria = c.id_categoria INNER JOIN Proveedores as p ON a.id_proveedor = p.id_proveedor WHERE a.id_estado = '{id_estado}'"
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_articulos()
		
	def verArticulosXProv(self):
		mycursor = self.mydb.cursor()
		cuit = validaciones.validar_cuit()
		sql = f"SELECT cuit_pro FROM Proveedores WHERE cuit_pro= '{cuit}'"
		mycursor.execute(sql)
		myresultado = mycursor.fetchall()
		encontrado = False
		for tupla in myresultado:	
			cuitBase = tupla[0]
			if cuit == cuitBase:
				encontrado = True
				break
		if encontrado == False:
			print("-" * 65)
			print("Lo siento.")
			print(f"El CUIT: {cuit} no se encuentra Registrado")
			print("-" * 65)
		else:
			estado = 1
			mycursor = self.mydb.cursor()
			sql = f"SELECT id_proveedor FROM Proveedores WHERE cuit_pro= '{cuit}'"
			mycursor.execute(sql)
			myresultado = mycursor.fetchone()
			id_proveedor = myresultado[0]	
			print("-" * 100)
			print("                          ARTICULOS ACTIVOS POR PROVEEDOR")
			print("-" * 100)
			sql = f"SELECT a.id_art as ID, a.cod_barras as 'CODIGO BARRAS',a.nom_art as 'NOMBRE', c.categoria_art as CATEGORIA,a.cant_producto as CANTIDAD, a.tipo_medida as MEDIDA, a.precio_art as PRECIO, a.stock_art as STOCK FROM Articulos as a INNER JOIN Categoria_art as c ON a.id_categoria = c.id_categoria WHERE a.id_proveedor = '{id_proveedor}' AND a.id_estado = '{estado}'"
			super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_articulos()

	def artPorNombre(self):
		print("-" * 65)
		print("                        CONSULTAR ARTÍCULOS POR NOMBRE")
		print("-" * 65)
		nombre = validaciones.consultar_por_nombre("Artículo")
		sql = f"SELECT a.id_art as ID, a.cod_barras as 'CODIGO BARRAS',a.nom_art as 'NOMBRE', c.categoria_art as CATEGORIA,a.cant_producto as CANTIDAD, a.tipo_medida as MEDIDA, a.precio_art as PRECIO, a.stock_art as STOCK, e.tipo_estado as ESTADO FROM Articulos as a INNER JOIN Categoria_art as c ON a.id_categoria = c.id_categoria INNER JOIN Estado as e ON a.id_estado = e.id_estado WHERE a.nom_art LIKE '%"+nombre+"%'"
		print("-" * 100)
		print(f"                                ARTÍCULOS QUE CONTENGAN '{nombre.upper()}'")
		print("-" * 100)
		super().mostrarTablas(sql)
		validaciones.esperar_y_limpiar()
		submenus.consulta_articulos()
