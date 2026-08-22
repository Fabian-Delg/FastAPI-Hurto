from pydantic import BaseModel

class Tipo_Hurto(BaseModel):
    nombre:str

class Hurto(BaseModel):
    id_tipo_hurto:int
    denunciante:str
    direccion:str
    fecha_hurto:str

class UsuarioRegistro(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str