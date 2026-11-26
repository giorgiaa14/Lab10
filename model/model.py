from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutte le Filiali (i nodi) presenti e filtrando i Collegamenti con
        importo medio per bonifico >= threshold (euro)
        """
        self.G.clear()
        self._nodes = DAO.get_filiali()
        if self._nodes is None:
            return
        # inserisco tutte le filiali come nodi del grafo
        self.G.add_nodes_from(self._nodes)
        # Mappa ID -> oggetto Filiale per costruire gli archi tra oggetti
        id_map = {f.id: f for f in self._nodes}
        self._edges = DAO.get_collegamenti()
        if self._edges is None:
            return

        for c in self._edges:
            importo_medio = c.valore
            if importo_medio >= threshold:
                u = id_map[c.id_filiale_1]
                v = id_map[c.id_filiale_2]
                self.G.add_edge(u, v, weight=importo_medio)

    def get_num_edges(self):
        """
        Restituisce il numero di Collegamenti (edges) del grafo
        :return: numero di edges del grafo
        """
        return len(self.G.edges)

    def get_num_nodes(self):
        """
        Restituisce il numero di Filiali (nodi) del grafo
        :return: numero di nodi del grafo
        """
        return len(self.G.nodes)

    def get_all_edges(self):
        """
        Restituisce tutti i Collegamenti (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        return list(self.G.edges(data=True))
