from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/vortexsound"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    birthdate = db.Column(db.String(10))  # Puedes ajustar el tipo de datos según tus necesidades
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, firstname, lastname, birthdate, email):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.email = email

with app.app_context():
    db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "firstname", "lastname", "birthdate", "email")

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

# Endpoint para obtener todos los usuarios
@app.route("/usuarios", methods=["GET"])
def get_Usuarios():
    all_usuarios = Usuario.query.all()
    result = usuarios_schema.dump(all_usuarios)
    return jsonify(result)

# Endpoint para obtener un usuario específico por ID
@app.route("/usuarios/<id>", methods=["GET"])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    return usuario_schema.jsonify(usuario)

# Endpoint para eliminar un usuario por ID
@app.route("/usuarios/<id>", methods=["DELETE"])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return usuario_schema.jsonify(usuario)

# Endpoint para crear un nuevo usuario
@app.route("/usuarios", methods=["POST"])
def create_usuario():
    username = request.json["username"]
    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    birthdate = request.json["birthdate"]
    email = request.json["email"]
    
    new_usuario = Usuario(username, firstname, lastname, birthdate, email)
    db.session.add(new_usuario)
    db.session.commit()
    return usuario_schema.jsonify(new_usuario)

# Endpoint para actualizar un usuario por ID
@app.route("/usuarios/<id>", methods=["PUT"])
def update_usuario(id):
    usuario = Usuario.query.get(id)

    usuario.username = request.json["username"]
    usuario.firstname = request.json["firstname"]
    usuario.lastname = request.json["lastname"]
    usuario.birthdate = request.json["birthdate"]
    usuario.email = request.json["email"]

    db.session.commit()
    return usuario_schema.jsonify(usuario)

if __name__ == "__main__":
    app.run(debug=True, port=5000)