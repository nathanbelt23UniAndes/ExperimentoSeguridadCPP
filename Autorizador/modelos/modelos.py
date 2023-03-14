from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from enum import IntEnum

db = SQLAlchemy()

class Roles(IntEnum):
    VENDEDOR  = 1
    COMPRADOR  = 2
    ADMINISTRADOR  = 3
    REPARTIDOR = 4
    
    @staticmethod
    def fetch_values():
        return [c.value for c in Roles]
    
class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    rol = db.Column(db.Enum(Roles))

class UsuarioSchema(SQLAlchemyAutoSchema):
    rol = EnumADiccionario(attribute=("rol"))
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        
    id = fields.String()

