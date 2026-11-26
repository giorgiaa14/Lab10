from database.DB_connect import DBConnect
from model.collegamento import Collegamento
from model.filiale import Filiale


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """

    @staticmethod
    def get_filiali() -> list[Filiale] | None:
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("errore di connessione al database.")
            return None

        result = []
        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM filiale """
        try:
            cursor.execute(query)
            for row in cursor:
                filiale = Filiale(
                    id=int(row["id"]),
                    codice=row["codice"],
                    nome=row["nome"],
                    citta=row["citta"],
                    provincia=row["provincia"],
                    latitudine=float(row["latitudine"]),
                    longitudine=float(row["longitudine"])
                )
                result.append(filiale)
        except Exception as e:
            print(f"Errore durante la query get_filiali: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_collegamenti() -> list[Collegamento] | None:
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("errore di connessione al database.")
            return None

        result = []
        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT LEAST(id_filiale_origine, id_filiale_destinazione) AS id_filiale_1,
                       GREATEST(id_filiale_origine, id_filiale_destinazione) AS id_filiale_2,
                       SUM(importo) AS somma_importi,
                       COUNT(*) AS num_bonifici
                FROM bonifico
                WHERE id_filiale_origine != id_filiale_destinazione
                GROUP BY LEAST(id_filiale_origine, id_filiale_destinazione),
                         GREATEST(id_filiale_origine, id_filiale_destinazione)
            """
        try:
            cursor.execute(query)
            for row in cursor:
                collegamento = Collegamento(
                    id_filiale_1=int(row["id_filiale_1"]),
                    id_filiale_2=int(row["id_filiale_2"]),
                    somma_importi=float(row["somma_importi"]),
                    num_bonifici=int(row["num_bonifici"])
                )
                result.append(collegamento)
        except Exception as e:
            print(f"Errore durante la query get_collegamenti: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result