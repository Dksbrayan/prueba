from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'zip', 'sb2', 'sb3'}

# Configurar la carpeta de subida y el tamaño máximo del archivo
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Función para verificar si la extensión del archivo es permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recursos')
def recursos():
    return render_template('recursos.html')

@app.route('/examen')
def examen():
    return render_template('examen.html')

@app.route('/cargar_proyecto')
def cargar_proyecto():
    return render_template('cargar_proyecto.html')

@app.route('/felicidades')
def felicidades():
    return render_template('felicidades.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica si se ha enviado un archivo
    if 'scratch-file' not in request.files:
        return redirect(url_for('cargar_proyecto', message='No se ha seleccionado ningún archivo.', type='error'))
    
    file = request.files['scratch-file']
    
    # Si el usuario no seleccionó un archivo, el campo estará vacío
    if file.filename == '':
        return redirect(url_for('cargar_proyecto', message='No se ha seleccionado ningún archivo.', type='error'))
    
    # Verificar si el archivo tiene una extensión permitida
    if file and allowed_file(file.filename):
        filename = file.filename
        # Guardar el archivo en la carpeta de subida
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('felicidades'))  # Redirigir a felicidades.html
    else:
        return redirect(url_for('cargar_proyecto', message='Tipo de archivo no permitido.', type='error'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
