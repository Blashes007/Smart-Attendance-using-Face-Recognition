from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', selected_date='', no_data=False)

@app.route('/attendance', methods=['POST'])
def attendance():
    selected_date = request.form.get('selected_date')
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, time FROM attendance WHERE date = ?", (formatted_date,))
    attendance_data = cursor.fetchall()

    conn.close()

    if not attendance_data:
        return render_template('index.html', selected_date=selected_date, no_data=True)
    
    return render_template('index.html', selected_date=selected_date, attendance_data=attendance_data)

@app.route('/delete', methods=['POST'])
def delete():
    selected_date = request.form.get('selected_date')
    name = request.form.get('name')
    time = request.form.get('time')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM attendance WHERE date = ? AND name = ? AND time = ?", (selected_date, name, time))
    conn.commit()

    cursor.execute("SELECT name, time FROM attendance WHERE date = ?", (selected_date,))
    attendance_data = cursor.fetchall()

    conn.close()

    if not attendance_data:
        return render_template('index.html', selected_date=selected_date, no_data=True)
    
    return render_template('index.html', selected_date=selected_date, attendance_data=attendance_data)

@app.route('/take_attendance', methods=['POST'])
def take_attendance():
    try:
        subprocess.Popen(['python', 'attendance_taker.py'])
        message = 'Attendance taking process started.'
    except Exception as e:
        message = f'Error: {str(e)}'

    return render_template('index.html', message=message)
@app.route('/get_faces', methods=['POST'])
def get_faces():
    try:
        subprocess.Popen(['python', 'get_faces_from_camera_tkinter.py'])
        message = 'recording faces'
    except Exception as e:
        message = f'Error: {str(e)}'

    return render_template('index.html', message=message)

@app.route('/feature_extraction', methods=['POST'])
def feature_extraction():
    try:
        subprocess.Popen(['python', 'features_extraction_to_csv.py'])
        message = 'extracting features of  faces'
    except Exception as e:
        message = f'Error: {str(e)}'

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
