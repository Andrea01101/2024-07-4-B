import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        if self._view.ddyear.value is None:
            self._view.txt_result1.controls.append(ft.Text("Inserire anno"))
            self._view.update_page()
            return
        if self._view.ddstate.value is None or self._view.ddstate.value == "":
            self._view.txt_result1.controls.append(ft.Text("Inserire stato"))
            self._view.update_page()
            return
        y = self._view.ddyear.value
        s = self._view.ddstate.value
        self._model.buildGraph(y, s)
        self._view.txt_result1.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero vertici: {self._model.getNumNodes()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero archi: {self._model.getNumEdges()}"))
        lung, lista = self._model.connesse()
        self._view.txt_result1.controls.append(ft.Text(f"Numero componenti connesse: {lung}"))
        for c in lista:
            self._view.txt_result1.controls.append(ft.Text(c))

        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDD(self):
        years = self._model.getYears()
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(y))
        self._view.update_page()

    def handle_genera_stati(self, e):
        self._view.ddstate.options.clear()
        self._view.ddstate.value = None
        y = int(self._view.ddyear.value)
        states = self._model.getState(y)
        for s in states:
            self._view.ddstate.options.append(ft.dropdown.Option(key=s.id, text=s.name))
        self._view.update_page()

