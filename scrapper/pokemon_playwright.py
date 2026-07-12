import os
import re
import json
import time
import random
import hashlib
import requests
from PIL import Image
from io import BytesIO
from playwright.sync_api import sync_playwright

# ==============================
# POKEDEX (GEN 1 + GEN 2)
# ==============================

POKEDEX = {
    1: "Bulbasaur", 2: "Ivysaur", 3: "Venusaur",
    4: "Charmander", 5: "Charmeleon", 6: "Charizard",
    7: "Squirtle", 8: "Wartortle", 9: "Blastoise",
    10: "Caterpie", 11: "Metapod", 12: "Butterfree",
    13: "Weedle", 14: "Kakuna", 15: "Beedrill",
    16: "Pidgey", 17: "Pidgeotto", 18: "Pidgeot",
    19: "Rattata", 20: "Raticate", 21: "Spearow",
    22: "Fearow", 23: "Ekans", 24: "Arbok",
    25: "Pikachu", 26: "Raichu", 27: "Sandshrew",
    28: "Sandslash", 29: "Nidoran♀", 30: "Nidorina", 31: "Nidoqueen",
    32: "Nidoran♂", 33: "Nidorino", 34: "Nidoking", 35: "Clefairy", 36: "Clefable",
    37: "Vulpix", 38: "Ninetales", 39: "Jigglypuff", 40: "Wigglytuff", 41: "Zubat",
    42: "Golbat", 43: "Oddish", 44: "Gloom", 45: "Vileplume", 46: "Paras", 47: "Parasect",
    48: "Venonat", 49: "Venomoth", 50: "Diglett", 51: "Dugtrio", 52: "Meowth", 53: "Persian",
    54: "Psyduck", 55: "Golduck", 56: "Mankey", 57: "Primeape", 58: "Growlithe", 59: "Arcanine",
    60: "Poliwag", 61: "Poliwhirl", 62: "Poliwrath", 63: "Abra", 64: "Kadabra", 65: "Alakazam",
    66: "Machop", 67: "Machoke", 68: "Machamp", 69: "Bellsprout", 70: "Weepinbell",
    71: "Victreebel", 72: "Tentacool", 73: "Tentacruel", 74: "Geodude", 75: "Graveler",
    76: "Golem", 77: "Ponyta", 78: "Rapidash", 79: "Slowpoke", 80: "Slowbro",
    81: "Magnemite", 82: "Magneton", 83: "Farfetch'd", 84: "Doduo", 85: "Dodrio",
    86: "Seel", 87: "Dewgong", 88: "Grimer", 89: "Muk", 90: "Shellder", 91: "Cloyster",
    92: "Gastly", 93: "Haunter", 94: "Gengar", 95: "Onix", 96: "Drowzee", 97: "Hypno",
    98: "Krabby", 99: "Kingler", 100: "Voltorb", 101: "Electrode", 102: "Exeggcute",
    103: "Exeggutor", 104: "Cubone", 105: "Marowak", 106: "Hitmonlee", 107: "Hitmonchan",
    108: "Lickitung", 109: "Koffing", 110: "Weezing", 111: "Rhyhorn", 112: "Rhydon",
    113: "Chansey", 114: "Tangela", 115: "Kangaskhan", 116: "Horsea", 117: "Seadra",
    118: "Goldeen", 119: "Seaking", 120: "Staryu", 121: "Starmie", 122: "Mr. Mime",
    123: "Scyther", 124: "Jynx", 125: "Electabuzz", 126: "Magmar", 127: "Pinsir",
    128: "Tauros", 129: "Magikarp", 130: "Gyarados", 131: "Lapras", 132: "Ditto",
    133: "Eevee", 134: "Vaporeon", 135: "Jolteon", 136: "Flareon", 137: "Porygon",
    138: "Omanyte", 139: "Omastar", 140: "Kabuto", 141: "Kabutops", 142: "Aerodactyl",
    143: "Snorlax", 144: "Articuno", 145: "Zapdos", 146: "Moltres", 147: "Dratini",
    148: "Dragonair", 149: "Dragonite", 150: "Mewtwo", 151: "Mew",
    # GEN 2
    152: "Chikorita", 153: "Bayleef", 154: "Meganium",
    155: "Cyndaquil", 156: "Quilava", 157: "Typhlosion",
    158: "Totodile", 159: "Croconaw", 160: "Feraligatr",
    161: "Sentret", 162: "Furret", 163: "Hoothoot", 164: "Noctowl",
    165: "Ledyba", 166: "Ledian", 167: "Spinarak", 168: "Ariados",
    169: "Crobat", 170: "Chinchou", 171: "Lanturn", 172: "Pichu",
    173: "Cleffa", 174: "Igglybuff", 175: "Togepi", 176: "Togetic", 177: "Natu",
    178: "Xatu", 179: "Mareep", 180: "Flaaffy", 181: "Ampharos", 182: "Bellossom",
    183: "Marill", 184: "Azumarill", 185: "Sudowoodo", 186: "Politoed", 187: "Hoppip",
    188: "Skiploom", 189: "Jumpluff", 190: "Aipom", 191: "Sunkern", 192: "Sunflora",
    193: "Yanma", 194: "Wooper", 195: "Quagsire", 196: "Espeon", 197: "Umbreon",
    198: "Murkrow", 199: "Slowking", 200: "Misdreavus", 201: "Unown", 202: "Wobbuffet",
    203: "Girafarig", 204: "Pineco", 205: "Forretress", 206: "Dunsparce", 207: "Gligar",
    208: "Steelix", 209: "Snubbull", 210: "Granbull", 211: "Qwilfish", 212: "Scizor",
    213: "Shuckle", 214: "Heracross", 215: "Sneasel", 216: "Teddiursa", 217: "Ursaring",
    218: "Slugma", 219: "Magcargo", 220: "Swinub", 221: "Piloswine", 222: "Corsola",
    223: "Remoraid", 224: "Octillery", 225: "Delibird", 226: "Mantine", 227: "Skarmory",
    228: "Houndour", 229: "Houndoom", 230: "Kingdra", 231: "Phanpy", 232: "Donphan",
    233: "Porygon2", 234: "Stantler", 235: "Smeargle", 236: "Tyrogue", 237: "Hitmontop",
    238: "Smoochum", 239: "Elekid", 240: "Magby", 241: "Miltank", 242: "Blissey",
    243: "Raikou", 244: "Entei", 245: "Suicune", 246: "Larvitar", 247: "Pupitar",
    248: "Tyranitar", 249: "Lugia", 250: "Ho-Oh", 251: "Celebi"
}

# ==============================
# CONFIGURACIÓN
# ==============================
BASE_DIR        = "dataset_pokemon_v2"
IMG_SIZE        = (224, 224)
MIN_FILE_SIZE   = 5_000
REQUEST_TIMEOUT = 8
MAX_RETRIES     = 2
SCROLL_PAUSES   = 8
MAX_IMGS_URL    = 100
PROGRESO_FILE   = "progreso.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# ==============================
# CHECKPOINT
# ==============================

def cargar_progreso() -> dict:
    if os.path.exists(PROGRESO_FILE):
        with open(PROGRESO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def guardar_progreso(progreso: dict):
    with open(PROGRESO_FILE, "w", encoding="utf-8") as f:
        json.dump(progreso, f, indent=2, ensure_ascii=False)


# ==============================
# UTILIDADES
# ==============================

def es_valida(img, size_bytes: int) -> bool:
    if getattr(img, "is_animated", False):
        return False
    if size_bytes < MIN_FILE_SIZE:
        return False
    return True


def generar_nombre(img) -> str:
    return hashlib.md5(img.tobytes()).hexdigest() + ".jpg"


# ==============================
# LIMPIEZA
# ==============================

def limpiar_dataset(folder: str) -> int:
    count = 0

    if not os.path.exists(folder):
        return 0

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        try:
            raw_size = os.path.getsize(path)

            with Image.open(path) as img:
                img.load()

                if not es_valida(img, raw_size):
                    os.remove(path)
                    continue

                img_norm = img.convert("RGB").resize(IMG_SIZE, Image.LANCZOS)
                new_name = generar_nombre(img_norm)
                new_path = os.path.join(folder, new_name)

                img_norm.save(new_path, "JPEG", quality=90)

                if path != new_path:
                    os.remove(path)

                count += 1

        except Exception:
            if os.path.exists(path):
                os.remove(path)

    return count


# ==============================
# CALENTAMIENTO
# ==============================

def calentar_browser(page):
    page.goto("https://www.google.com", wait_until="domcontentloaded")
    time.sleep(random.uniform(2, 4))

    try:
        boton = page.locator("button:has-text('Accept all'), button:has-text('Aceptar todo')")
        if boton.count() > 0:
            boton.first.click()
            time.sleep(1)
    except Exception:
        pass

    try:
        page.fill("textarea[name='q'], input[name='q']", "pokemon")
        time.sleep(random.uniform(0.5, 1))
        page.keyboard.press("Enter")
        time.sleep(random.uniform(2, 3))
    except Exception:
        pass


# ==============================
# SCRAPING CON PLAYWRIGHT
# ==============================

def obtener_urls_google(page, query: str, max_urls: int = MAX_IMGS_URL) -> list[str]:
    url_busqueda = f"https://www.google.com/search?q={requests.utils.quote(query)}&tbm=isch&hl=en"
    page.goto(url_busqueda, wait_until="domcontentloaded")
    time.sleep(random.uniform(1.5, 3))

    try:
        boton = page.locator("button:has-text('Accept all'), button:has-text('Aceptar todo')")
        if boton.count() > 0:
            boton.first.click()
            time.sleep(1)
    except Exception:
        pass

    for _ in range(SCROLL_PAUSES):
        page.keyboard.press("End")
        time.sleep(random.uniform(1.2, 2.5))

        try:
            btn_mas = page.locator("input[value='Show more results'], input[value='Mostrar más resultados']")
            if btn_mas.count() > 0:
                btn_mas.first.click()
                time.sleep(random.uniform(1, 2))
        except Exception:
            pass

    urls = page.evaluate("""
        () => {
            const results = [];
            const imgs = document.querySelectorAll('img.YQ4gaf, img.rg_i');
            imgs.forEach(img => {
                const src = img.getAttribute('src') || img.getAttribute('data-src') || '';
                if (src && !src.startsWith('data:') && !src.endsWith('.svg')) {
                    results.push(src);
                }
            });
            return results;
        }
    """)

    urls_hd = page.evaluate("""
        () => {
            const results = [];
            document.querySelectorAll('[data-ou]').forEach(el => {
                const url = el.getAttribute('data-ou');
                if (url && url.startsWith('http')) results.push(url);
            });
            return results;
        }
    """)

    todas = list(dict.fromkeys(urls_hd + urls))
    return todas[:max_urls]


def descargar_desde_urls(folder: str, urls: list[str]) -> int:
    session = requests.Session()
    session.headers.update(HEADERS)
    descargadas = 0

    for i, url in enumerate(urls):
        if not re.search(r"\.(jpg|jpeg|png|webp|gif)(\?|$)", url, re.IGNORECASE):
            if not url.startswith("http"):
                continue

        for intento in range(MAX_RETRIES):
            try:
                resp = session.get(url, timeout=REQUEST_TIMEOUT, stream=True)
                if resp.status_code != 200:
                    break

                data = resp.content
                img = Image.open(BytesIO(data))
                img.verify()
                img = Image.open(BytesIO(data))

                tmp_path = os.path.join(folder, f"tmp_{i}_{intento}.jpg")
                with open(tmp_path, "wb") as f:
                    f.write(data)

                descargadas += 1
                break

            except Exception:
                time.sleep(0.5)
                continue

    return descargadas


# ==============================
# PIPELINE PRINCIPAL
# ==============================

def construir_dataset_por_id(id_list: list, generacion: str, meta_minima: int = 300):
    base_path = os.path.join(BASE_DIR, generacion)
    progreso = cargar_progreso()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent=HEADERS["User-Agent"],
            viewport={"width": 1280, "height": 900},
            locale="en-US",
        )

        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = context.new_page()
        calentar_browser(page)

        for poke_id in id_list:
            nombre = POKEDEX[poke_id]
            clave = f"{generacion}_{poke_id}"

            # ── CHECKPOINT: saltar si ya está completo ──
            if progreso.get(clave, {}).get("completo", False):
                imgs_guardadas = progreso[clave]["imagenes"]
                print(f"  [SKIP] #{poke_id} {nombre} ya completo ({imgs_guardadas} imágenes), saltando...")
                continue

            folder = os.path.join(base_path, nombre.lower())
            os.makedirs(folder, exist_ok=True)

            queries = [
                f"{nombre} pokemon anime",
                f"{nombre} pokemon illustration",
                f"{nombre} pokemon hd",
                f"{nombre}",
                f"pokemon {nombre} official art",
                f"{nombre} pokemon fanart",
                f"{nombre} pokemon 3d render",
                f"{nombre} pokemon card",
                f"{nombre} pokemon wallpaper",
            ]

            actuales = limpiar_dataset(folder)

            for query in queries:
                print(f"  [{generacion}] #{poke_id} {nombre} | {actuales}/{meta_minima} | query: '{query}'")

                try:
                    urls = obtener_urls_google(page, query, max_urls=MAX_IMGS_URL)
                    print(f"    → {len(urls)} URLs encontradas")
                    descargar_desde_urls(folder, urls)
                    actuales = limpiar_dataset(folder)
                except Exception as e:
                    print(f"  [ERROR] Error en query '{query}': {e}")

                time.sleep(random.uniform(3, 7))

            # ── CHECKPOINT: guardar resultado ──
            estado = "[OK]" if actuales >= meta_minima else "[WARNING]"
            print(f"{estado} #{poke_id} {nombre} finalizado con {actuales} imágenes\n")

            progreso[clave] = {
                "nombre": nombre,
                "generacion": generacion,
                "imagenes": actuales,
                "completo": actuales >= meta_minima
            }
            guardar_progreso(progreso)

        browser.close()


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    gen1_ids = list(range(1, 152))
    gen2_ids = list(range(152, 252))

    construir_dataset_por_id(gen1_ids, "gen1", meta_minima=300)
    construir_dataset_por_id(gen2_ids, "gen2", meta_minima=300)