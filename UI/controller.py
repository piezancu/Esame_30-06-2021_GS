import flet as ft
import networkx as nx

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.soglia = None
        self.peso_min = None
        self.peso_max = None
        self.lista_archi = None

    def handle_graph(self, e):
        graph = self._model.creaGrafo()
        self.lista_archi = self._model.getEdges()
        self.peso_min = graph[3]
        self.peso_max = graph[2]
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {graph[0]} nodi e {graph[1]} archi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha peso massimo {self.peso_max}  e peso minimo {self.peso_min}"))

        self._view.update_page()

    def setSoglia(self, e):
        self.soglia = self._view.txt_name.value

    def handle_countedges(self, e):
        try:
            soglia_float = float(self.soglia)
            min_float = float(self.peso_min)
            max_float = float(self.peso_max)
        except ValueError:
            self._view.txt_result2.controls.append(ft.Text(f"Il valore soglia deve essere un numero"))
            self._view.update_page()
            return
        somma_archi_mag = 0
        somma_archi_min = 0
        if min_float < soglia_float < max_float:
            for c1, c2, peso in self.lista_archi(data=True):
                if peso['weight'] > soglia_float:
                    somma_archi_mag += 1
                if peso['weight'] < soglia_float:
                    somma_archi_min += 1
        else:
            self._view.txt_result2.controls.append(ft.Text(f"Il valore soglia deve essere compreso tra il peso minimo e il peso massimo indicati sopra"))
            self._view.update_page()
            return
        self._view.txt_result2.controls.append(ft.Text(f"Il grafo presenta {somma_archi_min} archi con peso sotto la soglia, e {somma_archi_mag} archi con peso sopra la soglia"))
        self._view.btn_search.disabled = False
        self._view.update_page()

    def handle_search(self, e):
        try:
            soglia_float = float(self.soglia)
        except ValueError:
            self._view.txt_result3.controls.append(ft.Text("La soglia deve essere un numero"))
            return
        best_path, peso_max = self._model.getBestPath(soglia_float)
        self._view.txt_result3.controls.append(ft.Text(f"Il peso del cammino è: {peso_max}"))
        for arco in best_path:
            self._view.txt_result3.controls.append(ft.Text(
                f"{arco[0]} ----> {arco[1]}, peso = {arco[2]['weight']}"))
        self._view.update_page()
