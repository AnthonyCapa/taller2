from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Configuración de la conexión a la base de datos Access
connection = pyodbc.connect(
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\PC 1\Downloads\taller\Nueva carpeta\TaskDB.accdb;'
)

cursor = connection.cursor()

# Ruta principal para mostrar tareas
@app.route('/')
def index():
    cursor.execute('SELECT * FROM taskDB')
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

# Ruta para agregar una nueva tarea
@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    cursor.execute('INSERT INTO TaskDB (Descripcion, Estado) VALUES (?, ?)', (task_name, False))
    connection.commit()
    return redirect(url_for('index'))

# Ruta para marcar una tarea como hecha 
# ...

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    cursor.execute('SELECT Estado FROM taskDB WHERE Id = ?', (task_id,))
    task = cursor.fetchone()
    if task:
        new_done = not task[0]
        cursor.execute('UPDATE taskDB SET Estado = ? WHERE Id = ?', (new_done, task_id))
        connection.commit()
    return redirect(url_for('index'))

#ruta para eliminar una tarea

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    cursor.execute('DELETE FROM taskDB WHERE Id = ?', (task_id,))
    connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
