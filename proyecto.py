from conexion import conexiones
import psycopg2

conexion= conexiones()
#uso de cursor
cursor= conexion.cursor()

#queries sql
sql='SELECT * FROM teams'
#con lo que se ejecutan las consultas
cursor.execute(sql)
#mostrar el resultado
registro= cursor.fetchall() 

print(registro)
#cerrando la conexión a la base de datos
cursor.close()
conexion.close()
