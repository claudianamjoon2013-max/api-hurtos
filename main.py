from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import database
from models import TipoHurtoSchema, HurtoSchema, UsuarioRegistro, Token
from auth import (
    hashear_password, 
    verificar_password, 
    crear_token, 
    obtener_usuario_actual
)

app = FastAPI()

database.crear_tablas()

@app.get("/")
def inicio():
    return {"mensaje": "API de Hurtos"}


@app.post("/registro")
def registrar_usuario(usuario: UsuarioRegistro):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        password_hash = hashear_password(usuario.password)
        cursor.execute(
            "INSERT INTO usuarios_app (username, password_hash) VALUES (%s, %s) RETURNING id, username;",
            (usuario.username, password_hash)
        )
        nuevo_usuario = cursor.fetchone()
        conn.commit()
        cursor.close()
        return {"mensaje": "Usuario registrado con éxito", "usuario": nuevo_usuario}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="El usuario ya existe o hubo un error.")
    finally:
        conn.close()

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios_app WHERE username = %s;", (form_data.username,))
        usuario = cursor.fetchone()
        cursor.close()
    finally:
        conn.close()

    if not usuario or not verificar_password(form_data.password, usuario["password_hash"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token = crear_token({"sub": usuario["username"], "id": usuario["id"]})
    return {"access_token": token, "token_type": "bearer"}




@app.get("/tipo-hurto/")
def obtener_tipos_hurto():
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_hurto;")
        return cursor.fetchall()
    finally:
        conn.close()

@app.get("/tipo-hurto/{id}")
def obtener_tipo_hurto_por_id(id: int):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_hurto WHERE id_tipohurto = %s;", (id,))
        tipo_hurto = cursor.fetchone()
        
        if not tipo_hurto:
            raise HTTPException(status_code=404, detail="Tipo de hurto no encontrado")
            
        return tipo_hurto
    finally:
        conn.close()

@app.post("/tipo-hurto/")
def crear_tipo_hurto(datos: TipoHurtoSchema, usuario: dict = Depends(obtener_usuario_actual)):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tipo_hurto (nombre_hurto) VALUES (%s) RETURNING *;",
            (datos.nombre_hurto,)
        )
        nuevo_tipo = cursor.fetchone()
        conn.commit()
        return nuevo_tipo
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/tipo-hurto/{id}")
def actualizar_tipo_hurto(id: int, datos: TipoHurtoSchema, usuario: dict = Depends(obtener_usuario_actual)):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tipo_hurto SET nombre_hurto = %s WHERE id_tipohurto = %s RETURNING *;",
            (datos.nombre_hurto, id)
        )
        tipo_actualizado = cursor.fetchone()
        if not tipo_actualizado:
            raise HTTPException(status_code=404, detail="Tipo de hurto no encontrado")
        conn.commit()
        return {"mensaje": "Tipo de hurto actualizado", "datos": tipo_actualizado}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/tipo-hurto/{id}")
def eliminar_tipo_hurto(id: int, usuario: dict = Depends(obtener_usuario_actual)):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipo_hurto WHERE id_tipohurto = %s RETURNING *;", (id,))
        tipo_eliminado = cursor.fetchone()
        if not tipo_eliminado:
            raise HTTPException(status_code=404, detail="Tipo de hurto no encontrado")
        conn.commit()
        return {"mensaje": "Tipo de hurto eliminado", "datos": tipo_eliminado}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="No se puede eliminar porque está asociado a registros de hurtos")
    finally:
        conn.close()




@app.get("/hurto/")
def obtener_hurtos():
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hurto;")
        return cursor.fetchall()
    finally:
        conn.close()

@app.get("/hurto/{id}")
def obtener_hurto_por_id(id: int):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hurto WHERE id = %s;", (id,))
        hurto = cursor.fetchone()
        
        if not hurto:
            raise HTTPException(status_code=404, detail="Registro de hurto no encontrado")
            
        return hurto
    finally:
        conn.close()

@app.post("/hurto/")
def registrar_hurto(datos: HurtoSchema, usuario: dict = Depends(obtener_usuario_actual)):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO hurto (idtipohurto, direccion, fecha_hurto)
            VALUES (%s, %s, %s)
            RETURNING *;
            """,
            (datos.idtipohurto, datos.direccion, str(datos.fecha_hurto))
        )
        nuevo_hurto = cursor.fetchone()
        conn.commit()
        return nuevo_hurto
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/hurto/{id}")
def actualizar_hurto(id: int, datos: HurtoSchema, usuario: dict = Depends(obtener_usuario_actual)):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE hurto 
            SET idtipohurto = %s, direccion = %s, fecha_hurto = %s 
            WHERE id = %s 
            RETURNING *;
            """,
            (datos.idtipohurto, datos.direccion, str(datos.fecha_hurto), id)
        )
        hurto_actualizado = cursor.fetchone()
        if not hurto_actualizado:
            raise HTTPException(status_code=404, detail="Registro de hurto no encontrado")
        conn.commit()
        return {"mensaje": "Hurto actualizado", "datos": hurto_actualizado}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/hurto/{id}")
def eliminar_hurto(id: int, usuario: dict = Depends(obtener_usuario_actual)):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hurto WHERE id = %s RETURNING *;", (id,))
        hurto_eliminado = cursor.fetchone()
        if not hurto_eliminado:
            raise HTTPException(status_code=404, detail="Registro de hurto no encontrado")
        conn.commit()
        return {"mensaje": "Hurto eliminado", "datos": hurto_eliminado}
    finally:
        conn.close()