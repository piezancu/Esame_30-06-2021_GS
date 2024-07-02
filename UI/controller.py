import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view:View, model:Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.localization = None

    def creaGrafo(self, e):
        self.stampaInfoGrafo()

    def stampaInfoGrafo(self):
        self._model.creaGrafo()
        nNodi, nArchi = self._model.getInfoGraph()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente\n"
                                                      f"Il grafo contiene {nNodi} nodi e {nArchi} archi"))
        self.handleDDLocalizations()
        self._view.update_page()

    def handleStatistiche(self, e):
        vicini = self._model.getStatistiche(self.localization)
        self._view.txt_result.controls.append(ft.Text(f"Archi adiacenti a {self.localization}"))
        for arco in vicini:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} ---> {arco[1]}: {arco[2]['weight']}"))
        self._view.txt_result.controls.append(ft.Text(""))
        self._view.update_page()

    def handleRicerca(self, e):
        best_path, len_path = self._model.getBestPath(self.localization)
        self._view.txt_result.controls.append(ft.Text(f"La lunghezza del cammino di peso max è {len_path}"))
        for arco in best_path:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} ---> {arco[1]}: {arco[2]['weight']}"))
        self._view.update_page()

    def handleDDLocalizations(self):
        localizations = self._model.getLocalizations()
        for l in localizations:
            self._view.ddLocalization.options.append(
                ft.dropdown.Option(
                    data=l,
                    on_click=self.salvaLocalization,
                    text=l
                ))
        self._view.update_page()

    def salvaLocalization(self, e):
        if e.control.data is None:
            self.localization = None
        else:
            self.localization = e.control.data

