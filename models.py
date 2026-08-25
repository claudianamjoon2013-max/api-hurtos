from pydantic import BaseModel

class UsuarioRegistro(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TipoHurtoSchema(BaseModel):
    nombre_hurto: str

class HurtoSchema(BaseModel):
    idtipohurto: int
    direccion: str
    fecha_hurto: str