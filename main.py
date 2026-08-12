from fastapi import FastAPI, HTTPException
import database
from models import TipoHurtoSchema, HurtoSchema

app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "API de Hurtos"}



@app.post("/tipo-hurto/")
def crear_tipo_hurto(datos: TipoHurtoSchema):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tipo_hurto (nombre_hurto) VALUES (%s) RETURNING *;",
            (datos.nombre_hurto,)
        )
        nuevo_tipo = cursor.fetchone()
        conn.commit()
        cursor.close()
        return nuevo_tipo
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.get("/tipo-hurto/")
def obtener_tipos_hurto():
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_hurto;")
        tipos = cursor.fetchall()
        cursor.close()
        return tipos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.put("/tipo-hurto/{id_tipohurto}")
def actualizar_tipo_hurto(id_tipohurto: int, datos: TipoHurtoSchema):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tipo_hurto SET nombre_hurto = %s WHERE id_tipohurto = %s RETURNING *;",
            (datos.nombre_hurto, id_tipohurto)
        )
        tipo_actualizado = cursor.fetchone()
        
        if not tipo_actualizado:
            raise HTTPException(status_code=404, detail="Tipo de hurto no encontrado")
            
        conn.commit()
        cursor.close()
        return tipo_actualizado
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.delete("/tipo-hurto/{id_tipohurto}")
def eliminar_tipo_hurto(id_tipohurto: int):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tipo_hurto WHERE id_tipohurto = %s RETURNING *;",
            (id_tipohurto,)
        )
        tipo_eliminado = cursor.fetchone()
        
        if not tipo_eliminado:
            raise HTTPException(status_code=404, detail="Tipo de hurto no encontrado")
            
        conn.commit()
        cursor.close()
        return {"mensaje": "Tipo de hurto eliminado", "datos": tipo_eliminado}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()




@app.post("/hurto/")
def registrar_hurto(datos: HurtoSchema):
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
        cursor.close()
        return nuevo_hurto
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.get("/hurto/")
def obtener_hurtos():
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hurto;")
        hurtos = cursor.fetchall()
        cursor.close()
        return hurtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.put("/hurto/{id}")
def actualizar_hurto(id: int, datos: HurtoSchema):
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
        cursor.close()
        return hurto_actualizado
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.delete("/hurto/{id}")
def eliminar_hurto(id: int):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM hurto WHERE id = %s RETURNING *;",
            (id,)
        )
        hurto_eliminado = cursor.fetchone()
        
        if not hurto_eliminado:
            raise HTTPException(status_code=404, detail="Registro de hurto no encontrado")
            
        conn.commit()
        cursor.close()
        return {"mensaje": "Hurto eliminado", "datos": hurto_eliminado}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()