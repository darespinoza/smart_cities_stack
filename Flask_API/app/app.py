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

# Función para crear tabla destino en base de datos
def create_table():
    try:
        # Establecer la conexion y crear cursor
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Crear la tabla
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS smart_cties_register (
            id SERIAL PRIMARY KEY,
            node_id VARCHAR(100),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sensor_id VARCHAR(100),
            value NUMERIC
        );
        '''
        cursor.execute(create_table_query)
        
        # Persistir cambios
        conn.commit()
        return "Tabla creada correctamente."
    except Exception as error:
        return f"Error creando la tabla: {error}"
    finally:
        # Cerrar la conexión y el cursor
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Función para crear tabla destino en base de datos
def create_temp_view():
    try:
        # Establecer la conexion y crear cursor
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Crear la tabla
        create_view_query = '''
        CREATE OR REPLACE VIEW temperatura_diaria AS
        SELECT DATE_TRUNC('day', scr."timestamp") AS timestamp_day,
            node_id,
            avg(value) AS avg_temperatura,
            max(value) AS max_temperatura,
            min(value) AS min_temperatura
        FROM smart_cties_register scr
        WHERE sensor_id = 'TEMP'
        GROUP BY node_id, timestamp_day;
        '''
        cursor.execute(create_view_query)
        
        # Persistir cambios
        conn.commit()
        return "Vista creada correctamente."
    except Exception as error:
        return f"Error creando la vista: {error}"
    finally:
        # Cerrar la conexión y el cursor
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Función para insertar datos en la tabla
def insert_data(node_id, timestamp,sensor_id, value):
    try:
        # Establecer la conexion y crear cursor
        conn = get_db_connection()
        cursor = conn.cursor()

        # Preparar query para insertar datos
        insert_query = "INSERT INTO smart_cties_register (node_id, timestamp, sensor_id, value) VALUES (%s, %s, %s, %s) RETURNING id;"
        cursor.execute(insert_query, (node_id, timestamp, sensor_id, value,))
        conn.commit()

        inserted_id = cursor.fetchone()[0]
        return inserted_id

    except Exception as error:
        print (f"Error insertando datos: {error}")
        return None
    finally:
        # Cerrar conexion y cursor
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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
        # Conectarse a base de datos
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
        # Crear tabla al inicio de la app
        create_table()
        # Crear vistas
        create_temp_view()
        
        # Obtener los datos JSON del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se hayan proporcionado campos necesarios
        if 'node_id' not in data and 'timestamp' not in data and 'sensor_id' not in data and 'value' not in data:
            return jsonify({"error": "Campos faltantes"}), 400

        # Obtener datos 
        node_id = data['node_id']
        timestamp = data['timestamp']
        sensor_id = data['sensor_id']
        value = float(data['value'])

        # Insertar los datos en la tabla
        inserted_id = insert_data(node_id, timestamp, sensor_id, value)

        # Verificar si se insertaron datos
        if inserted_id:
            return jsonify({"message": "Datos insertados correctamente", "id": inserted_id}), 201
        else:
            return jsonify({"error": "Error al insertar datos"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
