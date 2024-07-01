from app.database import get_db

class Socio:
    def __init__(self, id_socio=None, nombre=None, apellido=None, federado=False, edad=None, deportes=[]):
        self.id_socio = id_socio
        self.nombre = nombre
        self.apellido = apellido
        self.federado = federado
        self.edad = edad
        self.deportes = deportes

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id_socio:
            cursor.execute("""
                UPDATE socios SET nombre = %s, apellido = %s, federado = %s, edad = %s
                WHERE id_socio = %s
            """, (self.nombre, self.apellido, self.federado, self.edad, self.id_socio))
        else:
            cursor.execute("""
                INSERT INTO socios (nombre, apellido, federado, edad) VALUES (%s, %s, %s, %s)
            """, (self.nombre, self.apellido, self.federado, self.edad))
            self.id_socio = cursor.lastrowid
        db.commit()
        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_socio, nombre, apellido, federado, edad FROM socios")
        rows = cursor.fetchall()

        socios = []
        for row in rows:
            socio = Socio(id_socio=row[0], nombre=row[1], apellido=row[2], federado=row[3], edad=row[4])
            socio.deportes = Socio.get_deportes_of_socio(socio.id_socio)
            socios.append(socio)

        cursor.close()
        return socios

    @staticmethod
    def get_by_id(id_socio):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_socio, nombre, apellido, federado, edad FROM socios WHERE id_socio = %s", (id_socio,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            socio = Socio(id_socio=row[0], nombre=row[1], apellido=row[2], federado=row[3], edad=row[4])
            socio.deportes = Socio.get_deportes_of_socio(id_socio)
            return socio
        else:
            return None

    @staticmethod
    def get_deportes_of_socio(id_socio):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT d.id_deporte, d.nombre
            FROM socios_deportes sd
            JOIN deportes d ON sd.id_deporte = d.id_deporte
            WHERE sd.id_socio = %s
        """, (id_socio,))
        deportes = cursor.fetchall()
        cursor.close()
        return deportes

    def add_deporte(self, id_deporte):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO socios_deportes (id_socio, id_deporte) VALUES (%s, %s)", (self.id_socio, id_deporte))
        db.commit()
        cursor.close()

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM socios WHERE id_socio = %s", (self.id_socio,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'id_socio': self.id_socio,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'federado': self.federado,
            'edad': self.edad,
            'deportes': [{'id_deporte': dep[0], 'nombre': dep[1]} for dep in self.deportes]
        }

    def __str__(self):
        return f"SOCIO: {self.id_socio} - {self.nombre} {self.apellido}"

