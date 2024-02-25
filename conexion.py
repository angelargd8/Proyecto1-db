import psycopg2


def conexiones():
    try:
        conexion= psycopg2.connect(
            host = "localhost",
            database = "Proyecto1",
            user = "postgres",
            password = "123456", # francis123
            port = "5432" #SELECT * FROM pg_settings WHERE name = 'port';
        )
        print("conexion exitosa")
        return conexion

    except Exception as e:
        print(e)
        print("error en la conexion")
        return None