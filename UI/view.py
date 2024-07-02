import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None

        # graphical elements
        self._title = None

        self.ddLocalization = None
        self.btn_statistiche = None

        self.btn_ricerca_cammino = None

        self.txt_result = None



    def load_interface(self):
        # title
        self._title = ft.Text("Esame 30/06/2021 - Genes", color="blue", size=24)
        self._page.controls.append(self._title)

        #row1
        self.btn_crea_grafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.creaGrafo)
        self.ddLocalization = ft.Dropdown(label="Localizzazione",
                                         width=400)
        self.btn_statistiche = ft.ElevatedButton(text="Statistiche", on_click=self._controller.handleStatistiche)
        row1 = ft.Row([
                        self.btn_crea_grafo,
                        self.ddLocalization,
                        self.btn_statistiche],
                        alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        #ROW 2
        self.btn_ricerca_cammino = ft.ElevatedButton(text="Ricerca Cammino", width=500, on_click=self._controller.handleRicerca)
        row2 = ft.Row([self.btn_ricerca_cammino],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
