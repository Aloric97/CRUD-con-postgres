"""
    Conexión a PostgreSQL con Python
    Ejemplo de CRUD evitando inyecciones SQL

"""
import email
from multiprocessing import Value
import time
from turtle import delay
from pandas import options
import psycopg2
from os import system


#CRUD CON CLASES

def create_user(cursor,conexion):
    """A) CREAR USUARIO"""

    username= input("ingrese nombre de usuario:")
    password=input("ingrese contrasenia:")
    email=input("ingrese el correo:")

    query= "INSERT INTO users (username, password, email) VALUES(%s, %s, %s)"
    values=(username, password,email)

    cursor.execute(query,values)
    conexion.commit()
    print("\n################################\n")
    print("\nUsuario creado")


def list_user(cursor,conexion):
    """B) LISTAR USUARIO"""
    query ="SELECT id,username,email FROM users"
    cursor.execute(query)
    print("\n################################\n")
    print("\nListado de usuarios:\n")
    print("  ID- NOMBRE- EMAIL ")

    for id,username,email in cursor.fetchall():
        print("[",id,username,email,"]")

def update_user(cursor,conexion):
    """C) ACTUALIZAR USUARIO"""
    id= input("ingrese el id del usuario que desea actualizar:")
    query = "SELECT id from users WHERE id =%s"
    cursor.execute(query,(id,))
    user = cursor.fetchone()

    if user:
        opc={
            '1':"nombre",
            '2':"contraseña",
            '3':"email",
            '4':"SALIR"
        }

        print("cual campo quiere actualizar?")
        print(opc)
        rta=input("opcion:")
        if rta =='1':
            username= input("ingrese nombre de usuario:")
            query = "UPDATE users SET username= %s WHERE id=%s"

            values=(username,id)
            cursor.execute(query,values)
            conexion.commit()
            print(f"Su nuevo nombre de usuario es:{username}")
        elif rta =='2':   
            password= input("ingrese nombre de usuario:")
            query = "UPDATE users SET password= %s WHERE id=%s"

            values=(password,id)
            cursor.execute(query,values)
            conexion.commit()
            print(f"Su nuevo password:{password}")
        elif rta =='3':
            email=input("ingrese el correo:")
            query = "UPDATE users SET email= %s WHERE id=%s"

            values=(email,id)
            cursor.execute(query,values)
            conexion.commit()
            print(f"Su nuevo email es:{email}")
        else:
            print("ACTUALIZACION CANCELADA")
            print("VOLVIENDO AL MENÚ PRINCIPAL...")
            time.sleep(3)
            system("cls")
            
    else:
        print("No se encuentra el id del usuario")


def delete_user(cursor,conexion):
    """D) ELIMINAR USUARIO"""

    id= input("ingrese el id del usuario que desea eliminar:")

    query = "SELECT id from users WHERE id =%s"
    cursor.execute(query,(id,))

    user = cursor.fetchone()
    if user:
        query= "DELETE FROM users WHERE id=%s"
        cursor.execute(query,(5,))
        conexion.commit()
        print("\n################################\n")
        print("Usuario eliminado")
    else:
        print("\n################################\n")
        print("el id del usuario no se encuentra")

    
    

def user_exists(function):

    def wrapper(conexion,cursor):
        id= input("ingrese el id del usuario que desea actualizar:")
        query = "SELECT id from users WHERE id =%s"
        cursor.execute(query,(id,))
        
        user = cursor.fetchone()
        if user:
            function(id,conexion,cursor)
        else:
            print("no existe usuario con ese id, intenta de nuevo")
    return wrapper

def default(*args):
    print("\n################################\n")
    print("\nla opcion elegida no es valida")


#CREACION DE UNA TABLA
USERS_TABLE = """ CREATE TABLE IF NOT EXISTS users(
    id SERIAL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP            


)"""


if __name__ == '__main__':

    options={
        'a':create_user,
        'b':list_user,
        'c':update_user,
        'd':delete_user

    }

    print("La conexion ha sido exitosa")
    try:
        credenciales = {
            "dbname": "proyecto_python",
            "user": "postgres",
            "password": "123456",
            "host": "localhost",
            "port": 5432
        }
        conexion = psycopg2.connect(**credenciales)

        print("\n################################\n")
        with conexion.cursor() as cursor:
            cursor.execute(USERS_TABLE)
            while True:

                for functions in options.values():
                    print(functions.__doc__)

                print("quit para salir")

                option=input("seleciona una opcion valida:")
                if option=="quit" or option=="q":
                    conexion.close()
                    print("BASE DE DATOS CERRADA...")
                    break
                
                functions= options.get(option,default)
                functions(cursor,conexion)
                print("\n################################\n")
            

        


    except psycopg2.OperationalError as e:
        print("Ocurrió un error al conectar a PostgreSQL: ")
        print(e)
