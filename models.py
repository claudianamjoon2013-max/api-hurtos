from pydantic import BaseModel

#
class TipoHurtoSchema(BaseModel):
    nombre_hurto: str


class HurtoSchema(BaseModel):
    idtipohurto: int
    direccion: str
    fecha_hurto: str