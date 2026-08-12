from fastapi import FastAPI, HTTPException
from database import crear_tabla, get_connection
from models import Tipo_Hurto, Hurto

app = FastAPI()

crear_tabla()

@app.get("/")
def inicio():
    return {"mensaje":"API funcionando correctamente"}

# Tipos de Hurto

@app.post("/tiposHurto")
def crear_tipo_hurto(tipo_hurto:Tipo_Hurto):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM tipos_hurto WHERE nombre = %s", (tipo_hurto.nombre,)
    )
    tipo_hurto_existente = cur.fetchone()

    if tipo_hurto_existente:
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="El tipo de hurto ya existe")

    cur.execute("INSERT INTO tipos_hurto" \
                "(nombre) VALUES(%s)" \
                "RETURNING id",
                (tipo_hurto.nombre,))
    
    new_id = cur.fetchone()["id"] #Almacenar el id generado
    conn.commit()
    cur.close()
    conn.close()
    return {"mensaje":"Tipo de hurto creado", "id":new_id}

@app.get("/tiposHurto")
def listar_tipos_hurto():

    conn = get_connection()
    cur = conn.cursor()

    tipos_hurto = cur.execute(
        "SELECT * FROM tipos_hurto"
    )

    tipos_hurto = cur.fetchall()

    cur.close()
    conn.close()
    return[dict(x) for x in tipos_hurto]

@app.get("/tiposHurto/{id}")
def buscar_tipo_hurto(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tipos_hurto WHERE id = %s", (id,))
    tipo_hurto = cur.fetchone()

    cur.close()
    conn.close()

    if tipo_hurto:
        return tipo_hurto
    raise HTTPException(status_code=404, detail="El tipo de hurto no existe")

@app.delete("/tiposHurto/{id}")
def eliminar_tipo_hurto(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tipos_hurto WHERE id = %s", (id,))
    tipo_hurto = cur.fetchone()

    if not tipo_hurto:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="El tipo de hurto no existe")

    try:
        cur.execute("DELETE FROM tipos_hurto WHERE id = %s", (id,))
        conn.commit()

    except Exception:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="No se puede eliminar el tipo de hurto porque tiene hurtos asociados")

    cur.close()
    conn.close()

    return {"mensaje": "Tipo de hurto eliminado"}


# Hurto

@app.post("/hurtos")
def crear_hurto(hurto:Hurto):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM tipos_hurto WHERE id = %s", (hurto.id_tipo_hurto,))
    tipo_hurto = cur.fetchone()
    if not tipo_hurto:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="El tipo de hurto no existe")

    cur.execute("INSERT INTO hurtos" \
                "(id_tipo_hurto,denunciante,direccion,fecha_hurto) VALUES(%s,%s,%s,%s)" \
                "RETURNING id",
                (hurto.id_tipo_hurto, hurto.denunciante, hurto.direccion, hurto.fecha_hurto))
    new_id = cur.fetchone()["id"] #Almacenar el id generado
    conn.commit()
    cur.close()
    conn.close()
    return {"mensaje":"Hurto registrado", "id":new_id}

@app.get("/hurtos")
def lista_hurtos():

    conn = get_connection()
    cur = conn.cursor()

    hurtos = cur.execute(
        "SELECT * FROM hurtos"
    )

    hurtos = cur.fetchall()

    cur.close()
    conn.close()
    return[dict(x) for x in hurtos]

@app.get("/hurtos/{id}")
def buscar_hurto(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hurtos WHERE id = %s", (id,))
    hurto = cur.fetchone()

    cur.close()
    conn.close()

    if hurto:
        return hurto
    raise HTTPException(status_code=404, detail="Hurto no encontrado")

@app.get("/tiposHurto/{id}/hurtos")
def hurtos_tipos_hurto(id: int):
    conn= get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM hurtos "
        "INNER JOIN tipos_hurto ON hurtos.id_tipo_hurto = tipos_hurto.id "
        "WHERE tipos_hurto.id = %s",
        (id,)
    )
    hurtos = cur.fetchall()
    cur.close()
    conn.close()
    return hurtos

@app.put("/hurtos/{id}")
def actualizar_hurtos(id: int, hurto:Hurto):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tipos_hurto WHERE id = %s", (hurto.id_tipo_hurto,))
    tipo_hurto = cur.fetchone()

    if not tipo_hurto:
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="El tipo de hurto no existe")

    cur.execute(
        "UPDATE hurtos SET id_tipo_hurto = %s, denunciante = %s, direccion = %s, fecha_hurto = %s WHERE id = %s",
        (hurto.id_tipo_hurto, hurto.denunciante, hurto.direccion, hurto.fecha_hurto, id)
    )

    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if affect_rows == 0:
        raise HTTPException(status_code=404, detail="Hurto no encontrado")
    return {"mensaje": "Hurto actualizado correctamente"}


@app.delete("/hurtos/{id}")
def eliminar_hurto(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM hurtos WHERE id = %s",(id,))

    conn.commit()
    cur.close()
    conn.close()

    return{"mensaje":"Hurto eliminado"}