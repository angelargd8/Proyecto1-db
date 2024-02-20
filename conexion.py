import psycopg2


def conexiones():
    try:
        conexion= psycopg2.connect(
            host = "localhost",
            database = "prueba1",
            user = "postgres",
            password = "123456",
            port = "5432" #SELECT * FROM pg_settings WHERE name = 'port';
        )
        print("conexion exitosa")

    except Exception as e:
        print(e)
        print("error en la conexion")