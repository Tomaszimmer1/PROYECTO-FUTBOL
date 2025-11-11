from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton,
    QTabWidget, QListWidget, QFileDialog, QMessageBox,
    QTableWidget, QTableWidgetItem, QLineEdit, QDateEdit, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
from api_futbol import (
    obtener_tabla_posiciones,
    obtener_partidos_recientes,
    obtener_proximos_partidos,
    obtener_equipos_liga,
    obtener_info_temporada,
    obtener_goleadores
)

LIGAS = {
    "PL": "Premier League",
    "PD": "La Liga",
    "SA": "Serie A",
    "BL1": "Bundesliga",
    "FL1": "Ligue 1"
}

class VentanaFutbol(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚽ Resultados de las 5 Grandes Ligas")
        self.setGeometry(100, 100, 800, 600)
        self.modo_oscuro = False
        self.aplicar_estilo()

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("Resultados de las 5 Grandes Ligas")
        titulo.setFont(QFont("Segoe UI", 20))
        layout.addWidget(titulo)

        self.selector = QComboBox()
        for codigo, nombre in LIGAS.items():
            self.selector.addItem(nombre, codigo)
        layout.addWidget(QLabel("Seleccioná una liga:"))
        layout.addWidget(self.selector)

        self.boton_cargar = QPushButton("Cargar datos")
        self.boton_cargar.clicked.connect(self.cargar_datos_liga)
        layout.addWidget(self.boton_cargar)

        self.boton_tema = QPushButton("Cambiar tema")
        self.boton_tema.clicked.connect(self.toggle_tema)
        layout.addWidget(self.boton_tema)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.tabla_tab = QTableWidget()
        self.tabla_tab.setColumnCount(10)
        self.tabla_tab.setHorizontalHeaderLabels([
            "Pos", "Equipo", "Pts", "PJ", "PG", "PE", "PP", "GF", "GC", "DIF"
        ])
        self.tabs.addTab(self.tabla_tab, "Tabla de posiciones")

        self.recientes_tab = QListWidget()
        self.tabs.addTab(self.recientes_tab, "Partidos recientes")

        filtro_layout = QHBoxLayout()
        self.equipo_input = QLineEdit()
        self.equipo_input.setPlaceholderText("Filtrar por equipo...")
        self.fecha_input = QDateEdit()
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setDate(QDate.currentDate().addDays(-30))
        self.boton_filtrar = QPushButton("Filtrar partidos")
        self.boton_filtrar.clicked.connect(self.filtrar_partidos)
        filtro_layout.addWidget(self.equipo_input)
        filtro_layout.addWidget(self.fecha_input)
        filtro_layout.addWidget(self.boton_filtrar)
        layout.addLayout(filtro_layout)

        self.proximos_tab = QListWidget()
        self.equipos_tab = QListWidget()
        self.temporada_tab = QListWidget()
        self.goleadores_tab = QListWidget()

        self.tabs.addTab(self.proximos_tab, "Próximos partidos")
        self.tabs.addTab(self.equipos_tab, "Equipos")
        self.tabs.addTab(self.temporada_tab, "Temporada")
        self.tabs.addTab(self.goleadores_tab, "Goleadores")

        self.boton_exportar_txt = QPushButton("Exportar pestaña actual a .txt")
        self.boton_exportar_txt.clicked.connect(lambda: self.exportar_tab_actual("txt"))
        layout.addWidget(self.boton_exportar_txt)

        self.boton_exportar_csv = QPushButton("Exportar pestaña actual a .csv")
        self.boton_exportar_csv.clicked.connect(lambda: self.exportar_tab_actual("csv"))
        layout.addWidget(self.boton_exportar_csv)

    def aplicar_estilo(self):
        if self.modo_oscuro:
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: #f0f0f0; font-family: 'Segoe UI'; }
                QPushButton { background-color: #444; color: white; border-radius: 5px; padding: 6px; }
                QLineEdit, QComboBox, QDateEdit {
                    background-color: #3c3c3c; color: white;
                    border: 1px solid #666; border-radius: 5px;
                }
                QListWidget, QTableWidget {
                    background-color: #3c3c3c; color: white;
                    border: 1px solid #666; border-radius: 5px;
                    selection-background-color: #555;
                    selection-color: white;
                }
                QHeaderView::section {
                    background-color: #444; color: white;
                    padding: 4px; border: 1px solid #666;
                }
                QTabBar::tab {
                    background: #444; color: white;
                    padding: 8px; border-top-left-radius: 6px; border-top-right-radius: 6px;
                    margin-right: 2px;
                }
                QTabBar::tab:selected {
                    background: #3c3c3c; font-weight: bold;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #f5f7fa; color: #333; font-family: 'Segoe UI'; }
                QPushButton { background-color: #0078d7; color: white; border-radius: 5px; padding: 6px; }
                QLineEdit, QComboBox, QDateEdit {
                    background-color: white; color: black;
                    border: 1px solid #ccc; border-radius: 5px;
                }
                QListWidget, QTableWidget {
                    background-color: white; color: black;
                    border: 1px solid #ccc; border-radius: 5px;
                    selection-background-color: #cce4ff;
                    selection-color: black;
                }
                QHeaderView::section {
                    background-color: #e0e7ef; color: black;
                    padding: 4px; border: 1px solid #ccc;
                }
                QTabBar::tab {
                    background: #e0e7ef; color: black;
                    padding: 8px; border-top-left-radius: 6px; border-top-right-radius: 6px;
                    margin-right: 2px;
                }
                QTabBar::tab:selected {
                    background: #ffffff; font-weight: bold;
                }
            """)

    def toggle_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_estilo()

    def cargar_datos_liga(self):
        codigo = self.selector.currentData()

        self.tabla_tab.setRowCount(0)
        equipos = obtener_tabla_posiciones(codigo, formato="dict")
        for fila, e in enumerate(equipos):
            self.tabla_tab.insertRow(fila)
            valores = [
                e["position"], e["team"], e["points"], e["playedGames"],
                e["won"], e["draw"], e["lost"], e["goalsFor"],
                e["goalsAgainst"], e["goalDifference"]
            ]
            for col, val in enumerate(valores):
                self.tabla_tab.setItem(fila, col, QTableWidgetItem(str(val)))

        self.partidos_recientes = obtener_partidos_recientes(codigo)
        self.recientes_tab.clear()
        for item in self.partidos_recientes:
            self.recientes_tab.addItem(item)

        self.proximos_tab.clear()
        for item in obtener_proximos_partidos(codigo):
            self.proximos_tab.addItem(item)

        self.equipos_tab.clear()
        for item in obtener_equipos_liga(codigo):
            self.equipos_tab.addItem(item)

        self.temporada_tab.clear()
        for item in obtener_info_temporada(codigo):
            self.temporada_tab.addItem(item)

        self.goleadores_tab.clear()
        for item in obtener_goleadores(codigo):
            self.goleadores_tab.addItem(item)

    def filtrar_partidos(self):
        equipo = self.equipo_input.text().strip().lower()
        fecha_min = self.fecha_input.date().toString("yyyy-MM-dd")

        filtrados = []
        for p in self.partidos_recientes:
            partes = p.lower()
            if equipo and equipo not in partes:
                continue
            if "(" in p:
                fecha = p.split("(")[-1].replace(")", "")
                if fecha < fecha_min:
                    continue
            filtrados.append(p)

        self.recientes_tab.clear()
        if filtrados:
            for item in filtrados:
                self.recientes_tab.addItem(item)
        else:
            self.recientes_tab.addItem("No se encontraron partidos.")

    def exportar_tab_actual(self, formato):
        pestaña = self.tabs.currentWidget()
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "", f"Archivos .{formato} (*.{formato})"
        )
        if not ruta:
            return
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                if isinstance(pestaña, QTableWidget):
                    filas = pestaña.rowCount()
                    columnas = pestaña.columnCount()
                    headers = [pestaña.horizontalHeaderItem(i).text() for i in range(columnas)]
                    if formato == "csv":
                        f.write(",".join(headers) + "\n")
                        for r in range(filas):
                            fila = [pestaña.item(r, c).text() if pestaña.item(r, c) else "" for c in range(columnas)]
                            f.write(",".join(fila) + "\n")
                    else:
                        f.write(" | ".join(headers) + "\n")
                        for r in range(filas):
                            fila = [pestaña.item(r, c).text() if pestaña.item(r, c) else "" for c in range(columnas)]
                            f.write(" | ".join(fila) + "\n")
                elif isinstance(pestaña, QListWidget):
                    for i in range(pestaña.count()):
                        f.write(pestaña.item(i).text() + ("\n" if formato == "txt" else ',""\n'))
            QMessageBox.information(self, "Éxito", f"Archivo guardado en:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo:\n{e}")



       
