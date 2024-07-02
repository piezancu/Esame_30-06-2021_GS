import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.localizations = DAO.getAllLocalizations()
        self._graph.add_nodes_from(self.localizations)

        self.best_path = []
        self.peso_max = 0

    def creaGrafo(self):
        weighted_edges = DAO.getWeightedEdges()
        self._graph.add_weighted_edges_from(weighted_edges)

    def getInfoGraph(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getLocalizations(self):
        return self.localizations

    def getStatistiche(self, l1):
        # comp_conn = nx.node_connected_component(self._graph, l1)
        return self._graph.edges(l1, data=True)

    def getBestPath(self, l1):
        self.best_path = []
        self.peso_max = 0
        parz_nodi = [l1]
        self.ricorsione(l1, [], parz_nodi)

        return self.best_path, self.peso_max

    def ricorsione(self, nodo_corrente, parziale, parz_nodi):

        if parziale:
            peso_parziale = self.sommaPesi(parziale)
            if peso_parziale > self.peso_max:
                self.peso_max = peso_parziale
                self.best_path = copy.deepcopy(parziale)
                print(self.best_path)
                print(parz_nodi)
                print(self.peso_max)
                return

        for arco in self._graph.edges(nodo_corrente, data=True):
            nodo_successivo = arco[1]
            if nodo_successivo not in parz_nodi:
                parziale.append(arco)
                parz_nodi.append(nodo_successivo)
                self.ricorsione(nodo_successivo, parziale, parz_nodi)
                parz_nodi.pop()
                parziale.pop()

    def sommaPesi(self, parziale):
        peso = 0
        for arco in parziale:
            peso += arco[2]['weight']
        return peso


