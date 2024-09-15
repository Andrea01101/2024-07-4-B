from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def buildGraph(self, y: int, s: str):
        self._grafo.clear()
        sight = DAO.get_all_nodes(y, s)
        self._grafo.add_nodes_from(sight)

        self._idMap = {}
        for n in self._grafo.nodes:
            self._idMap[n.id] = n

        connessioni = DAO.get_all_edges(y, s, self._idMap)
        for c in connessioni:
            s1 = c.s1
            s2 = c.s2
            if s1.distance_HV(s2) < 100:
                self._grafo.add_edge(s1, s2)

    def connesse(self):
        conn = list(nx.connected_components(self._grafo))
        lun = len(conn)
        conn.sort(key=lambda x: len(x), reverse=True)
        return lun, conn[0]

    def getYears(self):
        return DAO.getAllYears()

    def getState(self, y: int):
        return DAO.getAllStates(y)

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
