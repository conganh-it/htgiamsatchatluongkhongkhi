from flask import Flask, render_template, jsonify, request
import logging

from code2 import get_db_connection

app = Flask(__name__)

# Assuming get_db_connection is defined somewhere
# Define your logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('air_quality.html')

@app.route('/air_quality')
def air_quality():
    return render_template('air_quality.html')

@app.route('/air_qualitydata')
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

@app.route('/air_qualityinde')
def show_table():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM AirQuality")
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return render_template('table.html', columns=columns, data=data)
    except Exception as e:
        logger.error(f"Error occurred while fetching data: {str(e)}")
        return jsonify({"error": str(e)})

@app.route('/air_qualitychart')
def show_chart():
    return render_template('chart.html')

if __name__ == '__main__':
    app.run(debug=True)
