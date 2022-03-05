import psycopg2

#Variable de entorno
from decouple import config

#ELIMINACION DE UNA TABLA
#DROP_TABLE_USERS="DROP TABLE IF EXISTS users"

#CREACION DE UNA TABLA
USERS_TABLE = """ CREATE TABLE IF NOT EXISTS users(
    id SERIAL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP            


)"""

multi_user=[
    ("leandro2", "12345", "leandro.tombetta97@gmail.com"),
    ("leandro3", "12345", "leandro.tombetta107@gmail.com"),
    ("leandro4", "12345", "leandro.tombetta117@gmail.com"),
    ("leandro5", "12345", "leandro.tombetta127@gmail.com")

]

if __name__=='__main__':

    try:
        connect = psycopg2.connect("dbname=pythondb user='postgres' password='123456' host='localhost' port='5432' ")


        with connect.cursor() as cursor:
            print('conexion realizada de forma exitosa')
            #cursor.execute(USERS_TABLE)
            #cursor.execute(DROP_TABLE_USERS)

            #INSERTAR REGISTRO
            query= "INSERT INTO users (username, password, email) VALUES(%s, %s, %s)"
            values=("leandro", "12345", "leandro.tombetta87@gmail.com")

            cursor.execute(query,values)
            connect.commit()
        #----------------------------------------------------------------------
            #INSERTAR MULTIPLES REGISTROS
            #for user in multi_user:
                #cursor.execute(query,user)
            #connect.commit()

            #SEGUNDA FORMA
            #cursor.executemany(quert,multi_user)
        #-----------------------------------------------------------------------

            #OBTENER REGISTROS
            query ="SELECT id FROM users"
            rows= cursor.execute(query)
            print('cantidad de registro:')
            print(rows)
            
            for user in cursor.fetchall():
                print(user)

            
            #OTRA FORMA
            #print('-----')
            #for user in cursor.fetchmany(3):
                #print(user)
        #----------------------------------------------------------------------

            #ACTUALIZAR REGISTROS
            #query = "UPDATE users SET username =%s WHERE id= %s"
            #values =("cambiouser",3)
            #cursor.execute(query,values)
            #connect.commit()
        #----------------------------------------------------------------------

            #ELIMINAR REGISTROS

            #query= "DELETE FROM users WHERE id=%s"
            #cursor.execute(query,(5,))
            #connect.commit()

    except Exception as error:

        print('no fue posible realizar la conexion')
        print(error)

    #Para ahorrar espacio en la memoria, es de buena practica cerrarlo    
    finally:
        print("La conexion finalizada exitosamente")
        connect.close()

        