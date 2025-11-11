import sys  # Importa el módulo 'sys', que permite acceder a parámetros del sistema, como los argumentos pasados al script.

from PyQt5.QtWidgets import QApplication  # Importa la clase QApplication, necesaria para iniciar cualquier aplicación PyQt5.

from gui_futbol import VentanaFutbol  # Importa la clase VentanaFutbol desde el archivo 'gui_futbol.py', que define la interfaz principal.

if __name__ == "__main__":  # Verifica si este archivo se está ejecutando directamente (no importado como módulo).
    app = QApplication(sys.argv)  # Crea una instancia de la aplicación PyQt5, pasando los argumentos del sistema (por si hay flags como -style).
    ventana = VentanaFutbol()  # Crea una instancia de la ventana principal de la app, definida en gui_futbol.py.
    ventana.show()  # Muestra la ventana en pantalla.
    sys.exit(app.exec_())  # Ejecuta el loop principal de eventos de la app y sale del programa cuando se cierra la ventana.
