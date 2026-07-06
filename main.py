#HACER TODOS LOS IMPORTSSSSSS
from Bd_Nutrite import bd_Nutrite
import mariadb
import submenus
import validaciones
#AGREGAR LIMPIAR PANTALLA AL PRINCIPIO(?)

def display_menu():
	print('''
****************************************************************************************
**--------------------------- ** BIENVENIDO A DIETETICA ** ---------------------------**
**--------------------------- **        NUTRITE         ** ---------------------------**
****************************************************************************************

				----  SELECCIONE  ----
					   
				1 - GESTIÓN PROVEEDORES
				2 - GESTIÓN CLIENTES
				3 - GESTIÓN ARTÍCULOS
				4 - GESTIÓN VENTAS
							
				0 - SALIR
    ''')

def get_user_choice():
	valido = 0
	while valido == 0:
		try:
			numIngresado = int(input("- Ingrese opción: "))
			return numIngresado
			valido = 1
		except ValueError:
			print("-" * 65)
			print("Error. Debe ingresar un valor numérico.")
			print("-" * 65)
               
def main():
	valido = 0
	mydb = mariadb.connect(host="127.0.0.1", user="root", autocommit=True)
	mycursor = mydb.cursor()
	mycursor.execute("CREATE DATABASE IF NOT EXISTS NUTRITE_DIETETICA")
	
	bd = bd_Nutrite()
	bd.crearTabla()
	bd.insertarDatos()
	
	while valido == 0:
		display_menu()
		user_choice = get_user_choice()
		if user_choice == 1:
			validaciones.limpiarPantalla()
			submenus.submenu_proveedor()
			valido = 1
		elif user_choice == 2:
			validaciones.limpiarPantalla()
			submenus.submenu_clientes()
			valido = 1
		elif user_choice == 3:
			validaciones.limpiarPantalla()
			submenus.submenu_articulos()
			valido = 1
		elif user_choice == 4:
			validaciones.limpiarPantalla()
			submenus.submenu_ventas()
			valido = 1
		elif user_choice == 0:
			print("**********************************  HASTA LUEGO  ************************************")
			bd.cerrarBD()
			del bd
			validaciones.limpiarPantalla()
			valido = 1
		else:
			print("-" * 65)
			print("Error. Debe ingresar un número entre las opciones.")
			print("-" * 65)

if __name__ == "__main__":
	main()
