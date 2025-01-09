import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Conexion a base de datos
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('PG_HOST'),
            database=os.getenv('PG_DB_NAME'),
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASSWORD'),
        )
        return conn
    except Exception as e:
        raise

# Ruta GET para senal Time to Live
@app.route(
    '/ttl', 
    methods=['GET']
)
def ttl():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Ruta POST para testear conexion a base de datos
@app.route(
    '/db_check',
    methods=['POST']
)
def db_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        results = cursor.fetchone()
        cursor.close()
        conn.close()

        return f"Conectado a PostgreSQL v{results[0]}", 200
    except Exception as e:
        return f"Sin conexion a BD: {e}", 500