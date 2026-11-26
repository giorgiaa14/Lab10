import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_collegamenti(self, e):
        """
        Funzione che controlla prima se il valore dell'importo inserito sia valido (es. non deve essere una stringa) e
        poi popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Filiali presenti
        * Numero di Collegamenti
        * Lista di Collegamenti che superano l'importo indicato come soglia
        """
        valore_str = self._view.importo_medio_minimo.value
        if valore_str is None or valore_str.strip() == "":
            self._view.show_alert("inserire un importo medio minimo in euro.")
            return

        try:
            soglia = float(valore_str.replace(",", "."))
        except ValueError:
            self._view.show_alert("errore: inserire un valore numerico valido.")
            return

        if soglia < 0:
            self._view.show_alert("errore: inserire un importo maggiore o uguale a 0.")
            return

        # Costruzione del grafo
        self._model.costruisci_grafo(soglia)
        # Aggiornamento della ListView
        self._view.lista_visualizzazione.controls.clear()
        num_nodi = self._model.get_num_nodes()
        num_archi = self._model.get_num_edges()
        archi = self._model.get_all_edges()

        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Filiali (nodi): {num_nodi}", weight=ft.FontWeight.BOLD)
        )
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Collegamenti (archi): {num_archi}", weight=ft.FontWeight.BOLD)
        )

        for u, v, attr in archi:
            peso = attr["weight"]
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"{u} - {v} | Valore medio: €{peso:.2f}")
            )

        self._view.update()
