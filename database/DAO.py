from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct  year(s.datetime) as y
                       from sighting s
                       order by y"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["y"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllStates(year: int):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s2.*
                       from sighting s, state s2 
                        where s2.id = s.state and year(s.`datetime`) = %s
                        order by s2.Name """
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_nodes(y: int, s: str):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                       from sighting s 
                       where year(s.`datetime`) = %s and s.state = %s"""
            cursor.execute(query, (y, s))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_edges(y: int, s: str, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.id as s1id, s2.id as s2id
                       from sighting s, sighting s2 
                       where year(s2.`datetime`) = year(s.`datetime`) and year(s.`datetime`) = %s
                       and s.state = s2.state and s.state = %s and s.shape = s2.shape 
                       and s.id < s2.id"""
            cursor.execute(query, (y, s))

            for row in cursor:
                result.append(Connessione(idMap[row["s1id"]],
                                          idMap[row["s2id"]]))
            cursor.close()
            cnx.close()
        return result
