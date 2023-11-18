from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import psycopg2
import getpass

app = Flask(__name__)
CORS(app)

# PostgreSQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'paul',
    'password': 'password',
    'port': '54321',
    'database': 'postgres'
}

def execute_query(query, values=None):
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

@app.route("/add", methods=['POST'])  # Use POST method for adding a student
def add_car():
    data = request.get_json()
    make = data['make']
    model = data['model']
    query = "INSERT INTO car(make, model) VALUES (%s, %s)"
    values = (make, model)
    execute_query(query, values)
    return jsonify({"Result": "Success"})
    
@app.route("/delete", methods=['POST'])
def delete_car():
    data = request.get_json()
    model = data['model']
    query = "Delete from car where model = %s"
    values = (model, )
    execute_query(query, values)
    return jsonify({"Result": "Success"})

@app.route("/update", methods=['POST'])
def update_car():
    data = request.get_json()
    old_model = data['old_model']
    new_model = data['new_model']
    query = "UPDATE car SET model = %s WHERE model = %s"
    values = (old_model, new_model)
    execute_query(query, values)
    return jsonify({"Result": "Success"})

@app.route("/")  # Default - Show Data
def read_car():
    query = "SELECT * FROM car"
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        Cars = [{'make': row[1], 'model': row[2]} for row in results]
        response = {'Results': Cars, 'count': len(Cars)}
        return jsonify(response)
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
