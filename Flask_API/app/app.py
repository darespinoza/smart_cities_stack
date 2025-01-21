import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

# Conexion a base de datos
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('PG_HOST'),
            port=os.getenv('PG_PORT'),
            database=os.getenv('PG_DB_NAME'),
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASSWORD'),
        )
        return conn
    except Exception as e:
        raise

# Función para crear la tabla
def create_table():
    try:
        # Establecer la conexión con la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        # Crear la tabla
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS smart_cties_register (
            id SERIAL PRIMARY KEY,
            node_id VARCHAR(100),
            timestamp_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sensor_id VARCHAR(100),
            value NUMERIC
        );
        '''
        cursor.execute(create_table_query)
        # Persistir cambios
        conn.commit()
        return "Tabla 'my_table' creada correctamente."
    except Exception as error:
        return f"Error creando la tabla: {error}"
    finally:
        # Cerrar la conexión y el cursor
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Función para insertar datos en la tabla
def insert_data(node_id, timestamp,sensor_id, value):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        insert_query = "INSERT INTO smart_cties_register (node_id, timestamp_db, sensor_id, value) VALUES (%s, %s, %s, %s) RETURNING id;"
        cursor.execute(insert_query, (node_id, timestamp, sensor_id, value,))
        connection.commit()

        inserted_id = cursor.fetchone()[0]
        return inserted_id

    except Exception as error:
        print(f"Error insertando datos: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Ruta GET para senal Time to Live
@app.route(
    '/ttl', 
    methods=['GET']
)
def ttl():
    return jsonify({"status": "OK"}), 200

# Ruta POST para testear conexion a base de datos
@app.route(
    '/db_check',
    methods=['POST']
)
def db_check():
    try:
        # Conectarse a la base de datos
        conn = get_db_connection()
        # Crear un cursor
        cursor = conn.cursor()
        # Ejecutar la consulta de version
        cursor.execute("SELECT version();")
        results = cursor.fetchone()
        
        return f"Conectado a PostgreSQL v{results[0]}", 200
    except Exception as e:
        return f"Sin conexion a BD: {e}", 500
    finally:
        # Cerrar la conexión y el cursor
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route(
    '/add_data', 
    methods=['POST']
)
def add_data():
    try:
        # Obtener los datos JSON del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se hayan proporcionado campos necesarios
        if 'node_id' not in data and 'timestamp' not in data and 'sensor_id' not in data and 'value' not in data:
            return jsonify({"error": "Campos faltantes"}), 400

        node_id = data['node_id']
        timestamp = data['timestamp']
        sensor_id = data['sensor_id']
        value = float(data['value'])

        # Insertar los datos en la tabla
        inserted_id = insert_data(node_id, timestamp, sensor_id, value)

        if inserted_id:
            return jsonify({"message": "Datos insertados correctamente", "id": inserted_id}), 201
        else:
            return jsonify({"error": "Error al insertar datos"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
