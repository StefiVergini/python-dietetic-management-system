import mariadb
import mysql.connector
from tabulate import tabulate
# importa la libreria

#-----------Conectarse con la Base de Datos--------------
class bd_Nutrite():
	
	_conexion = None
	
	@classmethod
	def get_conexion(cls):
		if cls._conexion is None:
			  # Si no hay una conexión existente, crea una nueva
			  cls._conexion = mariadb.connect(host="127.0.0.1",user="root",database = "NUTRITE_DIETETICA")
		return cls._conexion
			
	def __init__(self):
		self.mydb = self.get_conexion()
		self.mydb.database = "NUTRITE_DIETETICA"
	

	def crearTabla(self):
		mycursor = self.mydb.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS IVA(id_iva INT NOT NULL AUTO_INCREMENT, condicion_iva VARCHAR(60) NOT NULL, tipo_factura VARCHAR(1) NOT NULL,PRIMARY KEY(id_iva))")
		mycursor = self.mydb.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS Estado(id_estado INT NOT NULL AUTO_INCREMENT, tipo_estado VARCHAR(60) NOT NULL, PRIMARY KEY(id_estado))")
		mycursor = self.mydb.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS Categoria_Art(id_categoria INT NOT NULL AUTO_INCREMENT, categoria_art VARCHAR(100) NOT NULL, PRIMARY KEY(id_categoria))")
		mycursor = self.mydb.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS Clientes(id_cliente INT NOT NULL AUTO_INCREMENT,cuil_t_cli VARCHAR(11) NOT NULL,nom_completo VARCHAR(255) NOT NULL,tel_cli VARCHAR(20) NOT NULL,dir_cli VARCHAR(255) NOT NULL,mail_cli VARCHAR(255) NOT NULL, id_iva INT NOT NULL, id_estado INT NOT NULL,observacion_baja VARCHAR(255), PRIMARY KEY(id_cliente), FOREIGN KEY (id_iva) REFERENCES IVA(id_iva), FOREIGN KEY (id_estado) REFERENCES Estado(id_estado))")
		mycursor = self.mydb.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS Proveedores(id_proveedor INT NOT NULL AUTO_INCREMENT,cuit_pro VARCHAR(11) NOT NULL, nombre_empresa VARCHAR(255) NOT NULL, dir_pro VARCHAR(255) NOT NULL, tel_pro VARCHAR(20) NOT NULL, mail_pro VARCHAR(255) NOT NULL, id_iva INT NOT NULL, id_estado INT NOT NULL, motivo_baja VARCHAR(255),PRIMARY KEY(id_proveedor), FOREIGN KEY (id_iva) REFERENCES IVA(id_iva), FOREIGN KEY (id_estado) REFERENCES Estado(id_estado))")
		mycursor = self.mydb.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS Articulos(id_art INT NOT NULL AUTO_INCREMENT,cod_barras VARCHAR(30) NOT NULL, nom_art VARCHAR(255) NOT NULL,cant_producto DOUBLE NOT NULL ,tipo_medida VARCHAR(5) NOT NULL, id_categoria INT NOT NULL, precio_art DOUBLE NOT NULL, stock_art INT NOT NULL, motivo_baja VARCHAR(255), id_proveedor INT NOT NULL, id_estado INT NOT NULL, PRIMARY KEY(id_art), FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor), FOREIGN KEY (id_estado) REFERENCES Estado(id_estado), FOREIGN KEY (id_categoria) REFERENCES Categoria_Art(id_categoria))")
		mycursor = self.mydb.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS Solicitudes(id_solicitud INT NOT NULL AUTO_INCREMENT, id_proveedor INT NOT NULL, fecha_solicitud DATE ,hora_solicitud TIME,fecha_deIngreso DATE ,hora_deIngreso TIME,tipo_solicitud VARCHAR(60) NOT NULL, estado_solicitud VARCHAR(60) NOT NULL, observaciones VARCHAR(255), PRIMARY KEY(id_solicitud), FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor))")
		mycursor = self.mydb.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS Solicitud_Descripcion(id_solicitud INT NOT NULL, id_art INT NOT NULL,cant_art INT NOT NULL,cant_deIngreso INT, FOREIGN KEY (id_solicitud) REFERENCES Solicitudes(id_solicitud), FOREIGN KEY (id_art) REFERENCES Articulos(id_art))")
		mycursor = self.mydb.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS Ventas_cli(id_venta_cli INT NOT NULL AUTO_INCREMENT, id_cliente INT NOT NULL, fecha_venta DATE ,hora_venta TIME, total_venta DOUBLE, PRIMARY KEY(id_venta_cli), FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente))")
		mycursor = self.mydb.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS Ventas_art(id_venta_cli INT NOT NULL, id_art INT NOT NULL,precio_uni DOUBLE NOT NULL, cant_venta INT NOT NULL, subTotal_precio DOUBLE NOT NULL, FOREIGN KEY (id_venta_cli) REFERENCES Ventas_cli(id_venta_cli), FOREIGN KEY (id_art) REFERENCES Articulos(id_art))")
		
	def insertarDatos(self):
		#insertar datos tabla IVA
		mycursor = self.mydb.cursor()
		sql = "INSERT IGNORE INTO IVA(id_iva, condicion_iva, tipo_factura) VALUES (%d,%s, %s)"
		val = [
		(1,'Consumidor Final','B'),
		(2,'Responsable Inscripto', 'A'),
		(3,'Sujeto Exento', 'B'),
		]
		mycursor.executemany(sql, val)
		self.mydb.commit()
		#insertar datos tabla Estado
		mycursor = self.mydb.cursor()
		sql = "INSERT IGNORE INTO Estado(id_estado, tipo_estado) VALUES (%d,%s)"
		val = [
		(1,'ACTIVO'),
		(2,'BAJA'),
		]
		mycursor.executemany(sql, val)
		self.mydb.commit()
		#insertar datos tabla Categoria_Art
		mycursor = self.mydb.cursor()
		sql = "INSERT IGNORE INTO Categoria_Art(id_categoria, categoria_art) VALUES (%d,%s)"
		val = [
		(1,'ACEITES Y ACEITUNAS'),
		(2,'AZUCAR'),
		(3,'BEBIDAS'),
		(4,'CEREALES'),
		(5,'CEREALES PROCESADOS'),
		(6,'CHOCOLATES Y CACAOS'),
		(7,'DULCES'),
		(8,'ESPECIAS'),
		(9,'FIDEOS Y PASTAS'),
		(10,'FRUTAS DESHIDRATADAS'),
		(11,'FRUTOS SECOS'),
		(12,'GALLETITAS Y TOSTADAS'),
		(13,'GELATINA'),
		(14,'HARINAS Y FECULAS'),
		(15,'HIERBAS E INFUSIONES'),
		(16,'LEGUMBRES Y POROTOS'),
		(17,'MIXES'),
		(18,'REPOSTERIA'),
		(19,'SALSAS Y ADEREZOS'),
		(20,'SEMILLAS'),
		(21,'SNACKS'),
		(22,'UNTABLES'),
		(23,'VARIOS'),
		(24,'VERDURAS DESHIDRATADAS'),
		]
		mycursor.executemany(sql, val)
		self.mydb.commit()
		#insertar datos tabla clientes		
		mycursor = self.mydb.cursor()
		#(id_cliente ,cuil_t_cli VARCHAR(11) NOT NULL,nom_completo,tel_cli,dir_cli,mail_cli , id_iva 
		sql = "INSERT IGNORE INTO Clientes(id_cliente,cuil_t_cli ,nom_completo, tel_cli, dir_cli,mail_cli,id_iva, id_estado) VALUES (%d,%s,%s,%s,%s,%s,%d,%d)"
		val = [
		(1,'00000000000','Consumidor Final','00000000','Dietetica Nutrite 00','nutrite@dieteticanutrite.com',1,1),
		(2,'27372179991','stefania vergini','1164777337', 'calle falsa 123','stefanialvergini@gmail.com',1,1),
		(3,'23102222229','ernesto sabato','44441111','av. rivadavia 5501','ernesabato@gmail.com',2,1),
		(4,'25195622237','federico garcia lorca','1162627733','niceto vega 1502','felorca@hotmail.com',1,1),
		(5,'21145025032','luis alberto spinetta','43813909','mario bravo 1318','spinettajade@gmail.com',1,1),
		(6,'30344000346','universidad de buenos aires','46335555','av. diaz velez 2331','administracionuba@uba.bue.ar',3,1),
		(7,'20115698745','susana gimenez','42228873','jufre 980','soysusi@yahoo.com.ar',1,1),
		(8,'27434050593','moria casan','44287752','fitz roy 1493','laonemoria@gmail.com',1,1),
		(9,'25289270557','eric clapton','43835596','bonpland 1322','claptoneric@hotmail.com',1,1),
		]
		mycursor.executemany(sql, val)
		self.mydb.commit()
		#insertar datos tabla Proveedores
		mycursor = self.mydb.cursor()
		sql = "INSERT IGNORE INTO Proveedores(id_proveedor,cuit_pro, nombre_empresa, tel_pro, dir_pro, mail_pro, id_iva, id_estado) VALUES (%d,%s,%s,%s,%s,%s,%d,%d)"
		val = [
		(1,'60666555991','campo claro','43328118','av. cordoba 5666 caba','ventas@campoclaro.com',2,1),
		(2,'40333111556','esquina de las flores','1126996411', 'chile 1242 lanus','ventas@esquinadelasflores.com.ar',2,1),
		(3,'23102222229','sabores andinos','21099447','av. independencia 2231 caba','ventas@saboresandinos.com',2,1),
		(4,'25195622237','sudamerik argentina','47197600','martín fierro 980 escobar','ventas@sudamerikargentina.com.ar',2,1),
		]
		mycursor.executemany(sql, val)
		self.mydb.commit()
		#insertar datos tabla Articulos
		#Articulos(id_art,cod_barras, sku_del_prov, nom_art, categoria_art, precio_art, cant_art, tipo_cant, id_proveedor")
		mycursor = self.mydb.cursor()
		sql = "INSERT IGNORE INTO Articulos(id_art,cod_barras, nom_art,cant_producto,tipo_medida,id_categoria, precio_art, stock_art, id_proveedor, id_estado) VALUES (%d,%s,%s,%s,%s,%d,%s,%d,%d,%d)"
		val = [
		(1,'7790150350171', 'ACEITE OLIVA EXTRA VIRGEN ARECO', '250', 'ML',1, '3650.33', 10,4,1),
		(2,'7790150350172','ACEITE OLIVA EXTRA VIRGEN ARECO', '500', 'ML',1, '6150.00', 15,4,1),
		(3,'7790150350173','ACEITE DE COCO NATURAL ENTRENUTS','360','GR',1, '2700.00', 20,3,1),
		(4,'7790150350174','ARROZ YAMANI INTEGRAL','1', 'KG',4, '1415.00', 50,1,1),
		(5,'7790150350175','ARROZ YAMANI BLANCO', '1', 'KG', 4, '1560.00', 40,1,1),
		(6,'7790150350176','GRANOLA HIGOS TURCOS Y NUECES','1','KG',5, '3790.00', 10,2,1),
		(7,'7790150350177','GRANOLA MANI C/PASAS','1','KG',5, '2950.00', 5,4,1),
		(8,'7790150350178', 'GRANOLA CRUJIENTE C/PASAS','1','KG', 5, '3375.00', 2,3,1),
		(9,'7790150350179', 'GRANOLA AVENA CACAO Y MASCABO','1','KG',5, '3165.00', 1,2,1),
		(10,'7790150350180','GRANOLA AVENA MASCABO Y MIEL','1','KG',5, '2950.00', 4,1,1),
		(11,'7790150350181','PASAS DE UVA JUMBO MOROCHAS','1','KG',10, '4900.00', 10,2,1),
		(12,'7790150350182','PASAS DE UVA RUBIA 1° S/S','1','KG', 10, '6810.00', 5,1,1),
		(13,'7790150350183','PASAS DE UVA FLAME','1','KG',10, '3890.00', 0,4,1),
		(14,'7790150350184','CASTAÑAS DE CAJU W3 NATURAL','1','KG',11, '13895.00', 5,2,1),
		(15,'7790150350185','CASTAÑAS DE CAJU W3 NATURAL','500','GR',11, '6990.00', 10, 1,1),
		(16,'7790150350186','ALMENDRAS NON PAREIL 32/34','500','GR',11, '7965.00', 6,1,1),
		(17,'7790150350187','AVELLANAS MEDIANAS','500','GR',11, '5570.00', 10,2,1),
		(18,'7790150350188','ALMENDRAS NON PAREIL 27/30','1','KG',11, '14555.00', 2,4,1),
		(19,'7790150350189','NUECES MARIPOSAS EXTRA LIGHT','500','GR',11, '6540.00', 10,3,1),
		(20,'7790150350190','PISTACHOS C/CASCARA TOST Y SAL','500','GR',11, '9680.00', 6,2,1),
		(21,'7790150350191','HARINA TRIGO SARRACENO','1','KG',14, '2700.00', 20,1,1),
		(22,'7790150350192','HARINA TRIGO SARRACENO','500','GR',14, '765.00', 10,3,1),
		(23,'7790150350193','FECULA DE MAIZ','1','KG',14, '1605.00', 15,1,1),
		(24,'7790150350194','FECULA DE MANDIOCA','1','KG',14, '3610.00', 15,1,1),
		(25,'7790150350195','HARINA DE TRIGO INTEGRAL','1','KG',14, '1580.00', 30,1,1),
		(26,'7790150350196','HARINA DE TRIGO INTEGRAL','1','KG',14, '1375.00', 40,3,1),
		(27,'7790150350197','FARIÑA DE MANDIOCA','1' ,'KG',14, '5055.00', 20,3,1),
		(28,'7790150350198','HARINA DE TRIGO INTEGRAL','1','KG',14, '1400.00', 20,2,1),
		(29,'7790150350199','POROTOS NEGROS','1','KG',16, '1875.00', 10,4,1),
		(30,'7790150350200','POROTOS PALLARES GRANDE','500','GR',16, '2180.00', 15,3,1),
		(31,'7790150350201','POROTOS COLORADOS','1','KG',16, '1005.00', 10,4,1),
		(32,'7790150350202','POROTOS MUNG','1','KG',16, '1490.00', 0,4,1),
		(33,'7790150350203','GARBANZOS SECOS 6MM','1','KG',16, '2200.00', 20,2,1),
		(34,'7790150350204','LENTEJONES','500','GR',16, '1585.00', 40,2,1),
		(35,'7790150350205','POROTOS ALUBIA','1','KG',16, '2420.00', 15,3,1),
		(36,'7790150350206','POROTOS COLORADOS DARK','1','KG',16, '1950.00', 10,4,1),
		(37,'7790150350207','SEMILLA DE ZAPALLO','500','GR',20, '5400.00', 10,2,1),
		(38,'7790150350208','SEMILLA DE CHIA','1','KG',20, '1350.00', 30,3,1),
		(39,'7790150350209','SEMILLA DE SESAMO NEGRO','500','GR',20, '3795.00', 10,4,1),
		(40,'7790150350210','SEMILLA DE LINO','1','KG',20, '5630.00', 10,3,1),
		(41,'7790150350211','SEMILLA DE SESAMO BLANCO','500','GR',20, '4405.00', 9,2,1),
		]
		mycursor.executemany(sql, val)
		self.mydb.commit()
		
	def mostrarTablas(self, sql):
		mycursor = self.mydb.cursor()
		mycursor.execute(sql)
		rows = mycursor.fetchall()
		column_names = [desc[0].upper() for desc in mycursor.description]
		rows = [[str(cell).upper() for cell in row] for row in rows]
		if not rows:
			print("-" * 100)
			print("                Lo siento.")
			print("        No hay datos para mostrar.")
			print("-" * 100)	
		else:
			table = tabulate(rows, headers=column_names, tablefmt="grid", colalign=("center",))
			print(table)
		
	def cerrarBD(self):
		self.mydb.close()     # cerrar conexion cuando terminamos
