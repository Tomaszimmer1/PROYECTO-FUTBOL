import requests  # Importa la librería requests para hacer peticiones HTTP

# URL base de la API de football-data.org
API_BASE = "https://api.football-data.org/v4"

# Clave de autenticación para acceder a la API
API_KEY = "192c907a5470441eaa985f2ae40bddd8"

# Encabezados HTTP que incluyen el token de autenticación
HEADERS = {
    "X-Auth-Token": API_KEY
}

# Función para obtener la tabla de posiciones de una liga
def obtener_tabla_posiciones(codigo, formato="texto"):
    url = f"{API_BASE}/competitions/{codigo}/standings"  # Construye la URL de standings
    r = requests.get(url, headers=HEADERS)  # Realiza la petición GET con autenticación
    if r.status_code != 200:  # Si la respuesta no es exitosa, retorna lista vacía
        return []
    try:
        tabla = r.json()["standings"][0]["table"]  # Extrae la tabla del JSON
        if formato == "dict":  # Si se pide formato dict, devuelve lista de diccionarios
            return [
                {
                    "position": e["position"],
                    "team": e["team"]["name"],
                    "points": e["points"],
                    "playedGames": e["playedGames"],
                    "won": e["won"],
                    "draw": e["draw"],
                    "lost": e["lost"],
                    "goalsFor": e["goalsFor"],
                    "goalsAgainst": e["goalsAgainst"],
                    "goalDifference": e["goalDifference"]
                }
                for e in tabla
            ]
        else:  # Si se pide formato texto, devuelve lista de strings resumidos
            return [f"{e['position']}. {e['team']['name']} – {e['points']} pts" for e in tabla]
    except Exception as e:  # Si hay error al procesar, devuelve mensaje de error
        return [f"Error al procesar tabla: {e}"]

# Función para obtener los últimos partidos finalizados
def obtener_partidos_recientes(codigo, limit=10):
    url = f"{API_BASE}/competitions/{codigo}/matches?status=FINISHED&limit={limit}"  # URL con filtro de partidos finalizados
    r = requests.get(url, headers=HEADERS)  # Petición GET
    if r.status_code != 200:  # Si falla, devuelve error
        return [f"Error: {r.status_code}"]
    try:
        return [
            f"{m['homeTeam']['name']} {m['score']['fullTime']['home']}-{m['score']['fullTime']['away']} {m['awayTeam']['name']} ({m['utcDate'][:10]})"
            for m in r.json().get("matches", [])  # Formatea cada partido como string
        ]
    except Exception as e:
        return [f"Error al procesar partidos recientes: {e}"]

# Función para obtener los próximos partidos programados
def obtener_proximos_partidos(codigo, limit=10):
    url = f"{API_BASE}/competitions/{codigo}/matches?status=SCHEDULED&limit={limit}"  # URL con filtro de partidos programados
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return [f"Error: {r.status_code}"]
    try:
        return [
            f"{m['homeTeam']['name']} vs {m['awayTeam']['name']} ({m['utcDate'][:10]})"
            for m in r.json().get("matches", [])  # Formatea cada partido como string
        ]
    except Exception as e:
        return [f"Error al procesar próximos partidos: {e}"]

# Función para obtener los equipos participantes en una liga
def obtener_equipos_liga(codigo):
    url = f"{API_BASE}/competitions/{codigo}/teams"  # URL para obtener equipos
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return [f"Error: {r.status_code}"]
    try:
        equipos = r.json().get("teams", [])  # Extrae lista de equipos
        return [
            f"{t.get('name', 'Desconocido')} – Estadio: {t.get('venue', 'Sin estadio')}"
            for t in equipos  # Formatea cada equipo como string
        ] or ["No hay equipos disponibles."]
    except Exception as e:
        return [f"Error al procesar equipos: {e}"]

# Función para obtener información de la temporada actual
def obtener_info_temporada(codigo):
    url = f"{API_BASE}/competitions/{codigo}"  # URL para obtener info general de la competición
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return [f"Error: {r.status_code}"]
    try:
        temporada = r.json().get("currentSeason", {})  # Extrae datos de la temporada actual
        return [
            f"Inicio: {temporada.get('startDate', 'N/D')}",
            f"Fin: {temporada.get('endDate', 'N/D')}",
            f"Jornada actual: {temporada.get('currentMatchday', 'N/D')}"
        ]
    except Exception as e:
        return [f"Error al procesar temporada: {e}"]

# Función para obtener los máximos goleadores de la liga
def obtener_goleadores(codigo, limit=10):
    url = f"{API_BASE}/competitions/{codigo}/scorers?limit={limit}"  # URL para obtener goleadores
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return [f"Error: {r.status_code}"]
    try:
        data = r.json().get("scorers", [])  # Extrae lista de goleadores
        return [
            f"{s['player']['name']} ({s['team']['name']}) – {s['goals']} goles"
            for s in data  # Formatea cada goleador como string
        ] or ["No hay datos de goleadores disponibles."]
    except Exception as e:
        return [f"Error al procesar goleadores: {e}"]
