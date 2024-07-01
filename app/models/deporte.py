from app.database import get_db

class Deporte:
    def __init__(self, id_deporte=None, nombre=None):
        self.id_deporte = id_deporte
        self.nombre = nombre

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id_deporte:
            cursor.execute("UPDATE deportes SET nombre = %s WHERE id_deporte = %s", (self.nombre, self.id_deporte))
        else:
            cursor.execute("INSERT INTO deportes (nombre) VALUES (%s)", (self.nombre,))
            self.id_deporte = cursor.lastrowid
        db.commit()
        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_deporte, nombre FROM deportes")
        rows = cursor.fetchall()
        deportes = [Deporte(id_deporte=row[0], nombre=row[1]) for row in rows]
        cursor.close()
        return deportes

    @staticmethod
    def get_by_id(id_deporte):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_deporte, nombre FROM deportes WHERE id_deporte = %s", (id_deporte,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Deporte(id_deporte=row[0], nombre=row[1])
        else:
            return None

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM deportes WHERE id_deporte = %s", (self.id_deporte,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'id_deporte': self.id_deporte,
            'nombre': self.nombre
        }

    def __str__(self):
        return f"DEPORTE: {self.id_deporte} - {self.nombre}"
