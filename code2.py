from flask import Flask, render_template, jsonify
import pyodbc
import os
import logging
from dotenv import load_dotenv

app = Flask(__name__)

# Load biến môi trường từ tập tin .env
load_dotenv()

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chuỗi kết nối tới SQL Server
connection_string = os.getenv('DB_CONNECTION_STRING')

if not connection_string:
    logger.error("Database connection string is not set. Please set the DB_CONNECTION_STRING environment variable.")
else:
    logger.info(f"Database connection string: {connection_string}")

# Kết nối tới SQL Server
def get_db_connection():
    if not connection_string:
        raise ValueError("Database connection string is not set.")
    return pyodbc.connect(connection_string)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM AirQuality")
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return jsonify(data)
    except Exception as e:
        logger.error(f"Error occurred while fetching data: {str(e)}")
        return jsonify({"error": str(e)})

@app.route('/inde')
def show_table():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM AirQuality")
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return render_template('inde.html', columns=columns, data=data)
    except Exception as e:
        logger.error(f"Error occurred while fetching data: {str(e)}")
        return jsonify({"error": str(e)})

@app.route('/chart')
def show_chart():
    return render_template('chart.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8800)
