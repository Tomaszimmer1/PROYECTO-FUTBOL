from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton,
    QTabWidget, QListWidget, QTableWidget, QTableWidgetItem,
    QApplication
)
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys

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
        self.setWindowTitle("⚽ Resultados y Goles por Liga")
        self.setGeometry(100, 100, 900, 600)
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
        self.tabla_tab.setColumnCount(3)
        self.tabla_tab.setHorizontalHeaderLabels(["Equipo", "PJ", "Pts"])
        self.tabs.addTab(self.tabla_tab, "Tabla de posiciones")

        self.recientes_tab = QListWidget()
        self.tabs.addTab(self.recientes_tab, "Partidos recientes")

        self.grafico_tab = QWidget()
        self.grafico_layout = QVBoxLayout()
        self.grafico_tab.setLayout(self.grafico_layout)
        self.tabs.addTab(self.grafico_tab, "Gráfico de goles")

    def aplicar_estilo(self):
        if self.modo_oscuro:
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: #f0f0f0; font-family: 'Segoe UI'; }
                QPushButton { background-color: #444; color: white; border-radius: 5px; padding: 6px; }
                QComboBox {
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
                QComboBox {
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

        datos_tabla = {
            "PL": [("Manchester City", 38), ("Liverpool", 34), ("Arsenal", 32), ("Chelsea", 27)],
            "PD": [("Real Madrid", 36), ("Barcelona", 33), ("Atlético", 30), ("Girona", 28)],
            "SA": [("Inter", 35), ("Juventus", 31), ("Milan", 29), ("Napoli", 26)],
            "BL1": [("Bayern", 37), ("Leverkusen", 34), ("Dortmund", 30), ("Leipzig", 27)],
            "FL1": [("PSG", 36), ("Monaco", 32), ("Lille", 29), ("Nice", 25)]
        }

        partidos = {
            "PL": ["Arsenal 2-1 Chelsea", "Liverpool 3-0 Man City"],
            "PD": ["Barcelona 1-1 Girona", "Real Madrid 2-0 Atlético"],
            "SA": ["Inter 2-2 Napoli", "Juventus 1-0 Milan"],
            "BL1": ["Bayern 3-1 Dortmund", "Leipzig 2-2 Leverkusen"],
            "FL1": ["PSG 4-0 Nice", "Monaco 2-1 Lille"]
        }

        self.tabla_tab.setRowCount(0)
        for i, (equipo, puntos) in enumerate(datos_tabla.get(codigo, [])):
            self.tabla_tab.insertRow(i)
            self.tabla_tab.setItem(i, 0, QTableWidgetItem(equipo))
            self.tabla_tab.setItem(i, 1, QTableWidgetItem(str(10 + i)))  # PJ ficticio
            self.tabla_tab.setItem(i, 2, QTableWidgetItem(str(puntos)))

        self.recientes_tab.clear()
        for partido in partidos.get(codigo, []):
            self.recientes_tab.addItem(partido)

        self.mostrar_grafico_goles(codigo)

    def mostrar_grafico_goles(self, liga):
        datos_ficticios = {
            "PL": {"Manchester City": 38, "Liverpool": 34, "Arsenal": 32, "Chelsea": 27},
            "PD": {"Real Madrid": 36, "Barcelona": 33, "Atlético": 30, "Girona": 28},
            "SA": {"Inter": 35, "Juventus": 31, "Milan": 29, "Napoli": 26},
            "BL1": {"Bayern": 37, "Leverkusen": 34, "Dortmund": 30, "Leipzig": 27},
            "FL1": {"PSG": 36, "Monaco": 32, "Lille": 29, "Nice": 25}
        }

        goles = datos_ficticios.get(liga, {})
        equipos = list(goles.keys())
        valores = list(goles.values())

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        barras = ax.bar(equipos, valores, color="#0078d7", edgecolor="black")

        for barra, gol in zip(barras, valores):
            ax.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + 0.5,
                    str(gol), ha='center', va='bottom', fontsize=9)

        ax.set_title(f"Goles a favor - {LIGAS[liga]}", fontsize=12)
        ax.set_ylabel("Goles")
        ax.set_xticks(range(len(equipos)))
        ax.set_xticklabels(equipos, rotation=45, ha='right')
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        fig.tight_layout()

        # Limpiar gráfico anterior si existe
        for i in reversed(range(self.grafico_layout.count())):
            widget = self.grafico_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        canvas = FigureCanvas(fig)
        self.grafico_layout.addWidget(canvas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaFutbol()
    ventana.show()
    sys.exit(app.exec_())
