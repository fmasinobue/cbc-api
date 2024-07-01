import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from app.models.socio import Socio
from app.models.deporte import Deporte
from app.database import init_app, init_db

d = os.path.dirname(__file__)
os.chdir(d)

# Configuración inicial
app = Flask(__name__)
CORS(app)
init_app(app)


# Ruta para inicializar la base de datos
@app.route('/init-db')
def init_db_route():
    init_db()
    return "Base de datos inicializada correctamente."

# Ruta principal
@app.route('/')
def principal():
    return "¡Hola! Esta es la API para gestionar socios y deportes."

### Gestión de Socios ###

# Crear un socio
@app.route('/socios', methods=['POST'])
def create_socio():
    data = request.json
    nuevo_socio = Socio(nombre=data['nombre'], apellido=data['apellido'], federado=data['federado'], edad=data['edad'])
    nuevo_socio.save()

    # Asociar los deportes al socio en la tabla socios_deportes
    deportes = data.get('deportes', [])  # Lista de IDs de deportes que practica el socio
    for deporte_id in deportes:
        nuevo_socio.add_deporte(deporte_id)
    return jsonify({'message': 'Socio creado correctamente'}), 201

# Obtener todos los socios
@app.route('/socios', methods=['GET'])
def get_all_socios():
    socios = Socio.get_all()
    return jsonify([socio.serialize() for socio in socios])

# Obtener un socio por su ID
@app.route('/socios/<int:id_socio>', methods=['GET'])
def get_by_id_socio(id_socio):
    socio = Socio.get_by_id(id_socio)
    if socio:
        return jsonify(socio.serialize())
    else:
        return jsonify({'message': 'Socio no encontrado'}), 404

# Eliminar un socio por su ID
@app.route('/socios/<int:id_socio>', methods=['DELETE'])
def delete_socio(id_socio):
    socio = Socio.get_by_id(id_socio)
    if not socio:
        return jsonify({'message': 'Socio no encontrado'}), 404
    socio.delete()
    return jsonify({'message': 'El socio fue eliminado correctamente'})

# Actualizar un socio por su ID
@app.route('/socios/<int:id_socio>', methods=['PUT'])
def update_socio(id_socio):
    socio = Socio.get_by_id(id_socio)
    if not socio:
        return jsonify({'message': 'Socio no encontrado'}), 404
    data = request.json
    socio.nombre = data.get('nombre', socio.nombre)
    socio.apellido = data.get('apellido', socio.apellido)
    socio.federado = data.get('federado', socio.federado)
    socio.edad = data.get('edad', socio.edad)
    socio.save()
    return jsonify({'message': 'Socio actualizado correctamente'})

### Gestión de Deportes ###

# Crear un deporte
@app.route('/deportes', methods=['POST'])
def create_deporte():
    data = request.json
    nuevo_deporte = Deporte(nombre=data['nombre'])
    nuevo_deporte.save()
    return jsonify({'message': 'Deporte creado correctamente'}), 201

# Obtener todos los deportes
@app.route('/deportes', methods=['GET'])
def get_all_deportes():
    deportes = Deporte.get_all()
    return jsonify([deporte.serialize() for deporte in deportes])

# Obtener un deporte por su ID
@app.route('/deportes/<int:id_deporte>', methods=['GET'])
def get_by_id_deporte(id_deporte):
    deporte = Deporte.get_by_id(id_deporte)
    if deporte:
        return jsonify(deporte.serialize())
    else:
        return jsonify({'message': 'Deporte no encontrado'}), 404

# Eliminar un deporte por su ID
@app.route('/deportes/<int:id_deporte>', methods=['DELETE'])
def delete_deporte(id_deporte):
    deporte = Deporte.get_by_id(id_deporte)
    if not deporte:
        return jsonify({'message': 'Deporte no encontrado'}), 404
    deporte.delete()
    return jsonify({'message': 'El deporte fue eliminado correctamente'})

# Actualizar un deporte por su ID
@app.route('/deportes/<int:id_deporte>', methods=['PUT'])
def update_deporte(id_deporte):
    deporte = Deporte.get_by_id(id_deporte)
    if not deporte:
        return jsonify({'message': 'Deporte no encontrado'}), 404
    data = request.json
    deporte.nombre = data.get('nombre', deporte.nombre)
    deporte.save()
    return jsonify({'message': 'Deporte actualizado correctamente'})

# Ejecutar la aplicación si este archivo es el punto de entrada principal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
