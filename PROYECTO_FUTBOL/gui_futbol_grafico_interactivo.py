# Importa los widgets necesarios para construir la interfaz gráfica
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton,
    QTabWidget, QListWidget, QTableWidget, QTableWidgetItem,
    QFileDialog, QApplication
)

# Importa clase para personalizar fuentes
from PyQt5.QtGui import QFont

# Importa el canvas para incrustar gráficos de matplotlib en PyQt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Importa la clase Figure para crear gráficos
from matplotlib.figure import Figure

# Importa módulo del sistema para acceder a argumentos y cerrar la app
import sys

# Diccionario con códigos de liga y sus nombres legibles
LIGAS = {
    "PL": "Premier League",
    "PD": "La Liga",
    "SA": "Serie A",
    "BL1": "Bundesliga",
    "FL1": "Ligue 1"
}

# Diccionario con datos ficticios de goles por equipo en cada liga
GOLES_LIGA = {
    "PL": {"Manchester City": 38, "Liverpool": 34, "Arsenal": 32, "Chelsea": 27},
    "PD": {"Real Madrid": 36, "Barcelona": 33, "Atlético": 30, "Girona": 28},
    "SA": {"Inter": 35, "Juventus": 31, "Milan": 29, "Napoli": 26},
    "BL1": {"Bayern": 37, "Leverkusen": 34, "Dortmund": 30, "Leipzig": 27},
    "FL1": {"PSG": 36, "Monaco": 32, "Lille": 29, "Nice": 25}
}

# Clase principal de la ventana
class VentanaFutbol(QWidget):
    def __init__(self):
        super().__init__()  # Inicializa la clase base QWidget
        self.setWindowTitle("⚽ Goles por Liga - Interactivo")  # Título de la ventana
        self.setGeometry(100, 100, 900, 600)  # Posición y tamaño inicial

        layout = QVBoxLayout()  # Layout vertical principal
        self.setLayout(layout)  # Asigna el layout a la ventana

        titulo = QLabel("Gráfico de Goles por Liga")  # Etiqueta de título
        titulo.setFont(QFont("Segoe UI", 20))  # Fuente personalizada
        layout.addWidget(titulo)  # Agrega el título al layout

        self.selector = QComboBox()  # Combo para seleccionar liga
        for codigo, nombre in LIGAS.items():
            self.selector.addItem(nombre, codigo)  # Agrega cada liga al combo
        layout.addWidget(QLabel("Seleccioná una liga:"))  # Etiqueta descriptiva
        layout.addWidget(self.selector)  # Agrega el combo al layout

        self.boton_grafico = QPushButton("Mostrar gráfico")  # Botón para generar gráfico
        self.boton_grafico.clicked.connect(self.actualizar_grafico)  # Conecta evento click
        layout.addWidget(self.boton_grafico)

        self.boton_exportar = QPushButton("Exportar gráfico como imagen")  # Botón para exportar gráfico
        self.boton_exportar.clicked.connect(self.exportar_grafico)
        layout.addWidget(self.boton_exportar)

        self.tabs = QTabWidget()  # Contenedor de pestañas
        layout.addWidget(self.tabs)

        self.grafico_tab = QWidget()  # Pestaña para el gráfico
        self.grafico_layout = QVBoxLayout()  # Layout vertical para el gráfico
        self.grafico_tab.setLayout(self.grafico_layout)
        self.tabs.addTab(self.grafico_tab, "Gráfico")  # Agrega la pestaña al tab

        self.canvas = None  # Inicializa el canvas del gráfico como vacío

    # Método para actualizar el gráfico según la liga seleccionada
    def actualizar_grafico(self):
        liga = self.selector.currentData()  # Obtiene el código de liga seleccionado
        goles = GOLES_LIGA.get(liga, {})  # Obtiene los goles por equipo
        equipos = list(goles.keys())  # Lista de equipos
        valores = list(goles.values())  # Lista de goles

        fig = Figure(figsize=(6, 4))  # Crea una figura de matplotlib
        ax = fig.add_subplot(111)  # Agrega un subplot (gráfico de barras)
        barras = ax.bar(equipos, valores, color="#0078d7", edgecolor="black")  # Dibuja las barras

        # Agrega etiquetas de goles encima de cada barra
        for barra, gol in zip(barras, valores):
            ax.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + 0.5,
                    str(gol), ha='center', va='bottom', fontsize=9)

        ax.set_title(f"Goles a favor - {LIGAS[liga]}", fontsize=12)  # Título del gráfico
        ax.set_ylabel("Goles")  # Etiqueta del eje Y
        ax.set_xticks(range(len(equipos)))  # Posiciones de las etiquetas X
        ax.set_xticklabels(equipos, rotation=45, ha='right')  # Nombres de equipos rotados
        ax.grid(axis='y', linestyle='--', alpha=0.5)  # Líneas de guía en eje Y
        fig.tight_layout()  # Ajusta el layout del gráfico

        # Elimina cualquier gráfico anterior del layout
        for i in reversed(range(self.grafico_layout.count())):
            widget = self.grafico_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.canvas = FigureCanvas(fig)  # Crea el canvas con el nuevo gráfico
        self.grafico_layout.addWidget(self.canvas)  # Agrega el canvas al layout

    # Método para exportar el gráfico como imagen PNG
    def exportar_grafico(self):
        if self.canvas:  # Verifica si hay un gráfico generado
            ruta, _ = QFileDialog.getSaveFileName(
                self, "Guardar gráfico", "grafico_goles.png", "Imagen PNG (*.png)"
            )  # Abre diálogo para guardar archivo
            if ruta:
                self.canvas.figure.savefig(ruta)  # Guarda el gráfico como imagen
        else:
            print("No hay gráfico para exportar.")  # Mensaje si no hay gráfico

# Punto de entrada principal de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Crea la aplicación PyQt5
    ventana = VentanaFutbol()  # Crea la ventana principal
    ventana.show()  # Muestra la ventana
    sys.exit(app.exec_())  # Ejecuta el loop de eventos y cierra al salir
