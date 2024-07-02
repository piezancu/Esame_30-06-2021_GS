import copy
import itertools

import networkx as nx
from database import DAO
class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.best_path = None
        self.peso_max = 0

    def creaGrafo(self):
        nodes = DAO.DAO.getChromosomes()
        self.graph.add_nodes_from(nodes)

        weighted_edges = DAO.DAO.getWeightedEdges()
        self.graph.add_weighted_edges_from(weighted_edges)

        # tuplelist = list(itertools.combinations(nodes, 2))
        #
        # for t in tuplelist:
        #     weightTo = DAO.DAO.getEdgeTo(t[0], t[1])
        #     weightFrom = DAO.DAO.getEdgeTo(t[1], t[0])
        #
        #     if weightTo != []:
        #         self.graph.add_edge(t[0], t[1], weight=weightTo[0])
        #     if weightFrom != []:
        #         self.graph.add_edge(t[1], t[0], weight=weightFrom[0])

        sorted_edges = sorted(self.graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        max = sorted_edges[0][2]['weight']
        min = sorted_edges[-1][2]['weight']

        return len(self.graph.nodes), len(self.graph.edges), max, min

    def getEdges(self):
        return self.graph.edges

    def getBestPath(self, soglia):
        self.best_path = []
        self.peso_max = 0

        for nodo_iniziale in self.graph.nodes:
            parziale = []
            self.ricorsione(nodo_iniziale, parziale, soglia)

        return self.best_path, self.peso_max

    def ricorsione(self, nodo_corrente, parziale, soglia):

        archi_ammissibili = self.getArchiViciniAmmiss(nodo_corrente, soglia, parziale)

        if not archi_ammissibili:
            peso_parziale = self.sommaPesi(parziale)
            if peso_parziale > self.peso_max:
                self.peso_max = peso_parziale
                self.best_path = copy.deepcopy(parziale)
                print(self.best_path)
                print(self.peso_max)

        for arco in archi_ammissibili:
            nodo_successivo = arco[1]
            parziale.append(arco)
            self.ricorsione(nodo_successivo, parziale, soglia)
            parziale.pop()

    def sommaPesi(self, parziale):
        peso_tot = 0
        for arco in parziale:
            peso_tot += arco[2]['weight']
        return peso_tot

    def getArchiViciniAmmiss(self, nodo_corrente, soglia, parziale):
        archi_vicini = self.graph.edges(nodo_corrente, data=True)
        archi_vicini_ammis = []
        for arco in archi_vicini:
            if arco[2]['weight'] > soglia and arco not in parziale:
                archi_vicini_ammis.append(arco)
        return archi_vicini_ammis

