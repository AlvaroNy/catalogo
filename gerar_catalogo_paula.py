# -*- coding: utf-8 -*-
"""
Gerador do catalogo visual Paula Fernanda (Perfumes & Cosmeticos - Atacado).
Le as fotos de img/<codigo>.jpg (se existirem), embute em base64 e gera um
unico arquivo HTML autossuficiente (catalogo.html), pronto p/ WhatsApp/celular.
Rode:  python gerar_catalogo_paula.py
"""
import os, io, base64, html, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, "img")
SAIDA = os.path.join(BASE, "catalogo.html")

# ----------------------------------------------------------------------------
# DADOS DE CONTATO  ->  EDITE AQUI (deixei placeholders; troque pelos reais)
# ----------------------------------------------------------------------------
MARCA      = "Alvaro Nayder"
SUBTITULO  = "Perfumes & Cosméticos importados · Atacado"
WHATSAPP   = "5537991716781"          # so numeros, com 55 + DDD. ex: 5511999998888
WHATSAPP_F = "(37) 99171-6781"        # como aparece escrito
INSTAGRAM  = "seu_instagram"          # sem @  -> TROCAR pelo @ real
ENDERECO   = "Rua Tupis, 174 - Moema"
REFERENCIA = "Tabela de Atacado · Junho/2026"
# Data da ultima atualizacao de PRODUTOS/PRECOS (formato DD/MM/AAAA).
# >>> SO TROQUE quando mudar produto ou preco. Melhorias no site NAO contam. <<<
ATUALIZADO = "24/06/2026"

# ----------------------------------------------------------------------------
# CATEGORIAS (ordem de exibicao)
# ----------------------------------------------------------------------------
CATEGORIAS = [
    ("perf_import",  "Perfumes importados",        "ti-flask",          "card"),
    ("perf_arabe",   "Perfumes árabes",            "ti-moon-stars",     "card"),
    ("perf_tester",  "Testers",                    "ti-test-pipe",      "card"),
    ("contratipo",   "Contratipos Dream Brand 25ml","ti-droplet-half",  "lista"),
    ("arabic_insp",  "Inspirações Arabic 25ml",    "ti-droplet",        "lista"),
    ("cosm_base",    "Bases",                      "ti-palette",        "card"),
    ("cosm_vs_lot",  "Hidratantes Victoria's Secret","ti-bottle",       "card"),
    ("cosm_vs_spl",  "Body Splash Victoria's Secret","ti-spray",        "card"),
    ("cosm_nac",     "Cremes & Splash nacionais",  "ti-droplet",        "card"),
    ("cosm_mist",    "Body Mist Maison",           "ti-air-balloon",    "card"),
    ("cosm_cabelo",  "Cabelo & Tratamento",        "ti-wind",           "card"),
    ("cosm_corpo",   "Corpo & Skincare",           "ti-leaf",           "card"),
]

# ----------------------------------------------------------------------------
# PRODUTOS  (codigo, nome, preco, categoria, query_imagem, equivalencia, badge)
# ----------------------------------------------------------------------------
P = []
def add(cod, nome, preco, cat, q="", eq="", badge=""):
    P.append(dict(cod=cod, nome=nome, preco=preco, cat=cat, q=q or nome, eq=eq, badge=badge))

# --- Perfumes importados ---
add("142", "Animale For Men 100ml EDT",              175.50, "perf_import", "Animale for men eau de toilette 100ml")
add("905", "Antonio Banderas The Secret Golden Men 200ml EDT", 170.10, "perf_import", "Antonio Banderas The Golden Secret men eau de toilette 200ml")
add("2",   "Azzaro Pour Homme 100ml EDT",            230.40, "perf_import", "Azzaro Pour Homme 100ml eau de toilette")
add("2103","CH La Bomba 80ml EDP",                   570.60, "perf_import", "Carolina Herrera CH La Bomba 80ml eau de parfum")
add("22",  "CH 212 NYC Men 100ml EDT",               380.70, "perf_import", "Carolina Herrera 212 NYC Men 100ml eau de toilette")
add("23",  "CH 212 Sexy Men 100ml EDT",              400.50, "perf_import", "Carolina Herrera 212 Sexy Men 100ml")
add("26",  "CH 212 VIP Femme 80ml EDP",              470.70, "perf_import", "Carolina Herrera 212 VIP women eau de parfum 80ml")
add("717", "CH 212 VIP Black Men 100ml",             415.80, "perf_import", "Carolina Herrera 212 VIP Black Men 100ml")
add("24",  "CH 212 VIP Men 100ml EDT",               405.00, "perf_import", "Carolina Herrera 212 VIP Men 100ml")
add("27",  "CH 212 VIP Rose 80ml EDP",               470.70, "perf_import", "Carolina Herrera 212 VIP Rose 80ml eau de parfum")
add("255", "Chloé by Chloé 100ml EDP",               540.90, "perf_import", "Chloe by Chloe 100ml eau de parfum")
add("20",  "CK Euphoria Fem 100ml EDP",              320.40, "perf_import", "Calvin Klein Euphoria 100ml eau de parfum")
add("21",  "CK Euphoria Men 100ml EDT",              240.30, "perf_import", "Calvin Klein Euphoria Men 100ml eau de toilette", badge="Novo")
add("48",  "Dolce & Gabbana Light Blue 100ml EDT",   399.60, "perf_import", "Dolce Gabbana Light Blue pour femme 100ml eau de toilette", badge="Novo")
add("44",  "Dior J'adore 100ml EDP",                 650.70, "perf_import", "Dior J'adore eau de parfum 100ml")
add("1989","Dolce & Gabbana K Men - Kit 100ml + gel + pós barba", 460.80, "perf_import", "Dolce Gabbana K King men eau de parfum 100ml", badge="Kit")
add("52",  "Ferrari Black 125ml EDT",                150.30, "perf_import", "Ferrari Black 125ml eau de toilette")
add("248", "Gabriela Sabatini Fem 60ml EDT",         90.00, "perf_import", "Gabriela Sabatini eau de toilette 60ml", badge="Novo")
add("527", "Jean Paul Gaultier Scandal Fem 80ml EDP",495.90, "perf_import", "Jean Paul Gaultier Scandal pour femme eau de parfum 80ml")
add("68",  "Joop! Homme 125ml EDT",                  165.60, "perf_import", "Joop Homme 125ml eau de toilette", badge="Novo")
add("132", "Lancôme La Vie Est Belle 100ml EDP",     535.50, "perf_import", "Lancome La Vie Est Belle 100ml eau de parfum")
add("70",  "Marina de Bourbon Rouge Royal 100ml EDP",209.70, "perf_import", "Marina de Bourbon Rouge Royal 100ml")
add("567", "Marina de Bourbon Royal Diamond 100ml EDP",210.60, "perf_import", "Princesse Marina de Bourbon Royal Diamond 100ml")
add("113", "Paco Rabanne Olympéa 80ml EDP",          460.80, "perf_import", "Paco Rabanne Olympea 80ml eau de parfum", badge="Novo")
add("80",  "Paco Rabanne Invictus 100ml EDT",        380.70, "perf_import", "Paco Rabanne Invictus 100ml eau de toilette")
add("1635","Paco Rabanne Invictus Victory Elixir Parfum Intense 100ml", 490.50, "perf_import", "Paco Rabanne Invictus Victory Elixir 100ml")
add("78",  "Paco Rabanne Lady Million 80ml EDP",     450.90, "perf_import", "Paco Rabanne Lady Million 80ml eau de parfum")
add("74",  "Paco Rabanne One Million 100ml EDT",     380.70, "perf_import", "Paco Rabanne One Million 100ml eau de toilette")
add("233", "Silver Scent Intense Masculino 100ml EDT",165.60, "perf_import", "Jacques Bogart Silver Scent Intense 100ml eau de toilette")
add("127", "Silver Scent Tradicional 100ml EDT",     150.30, "perf_import", "Jacques Bogart Silver Scent 100ml eau de toilette")
add("136", "Thierry Mugler Angel Feminino 100ml EDP",550.80, "perf_import", "Thierry Mugler Angel pour femme eau de parfum 100ml")
add("177", "UDV For Men Black 100ml EDT",            85.50, "perf_import", "Ulric de Varens UDV pour homme black 100ml", badge="Novo")
add("1482","Versace Dylan Turquoise Fem 100ml",      450.90, "perf_import", "Versace Dylan Turquoise pour femme eau de parfum 100ml")
add("811", "Versace Pour Homme 100ml EDT",           370.80, "perf_import", "Versace Pour Homme 100ml eau de toilette", badge="Novo")

# --- Testers ---
add("1118","Tester Dolce & Gabbana Light Blue Fem 100ml", 305.10, "perf_tester", "Dolce Gabbana Light Blue pour femme eau de toilette 100ml", badge="Tester")

# --- Perfumes arabes ---
add("1150","Al Haramain L'Aventure Men EDP 100ml",   240.30, "perf_arabe", "Al Haramain L'Aventure men eau de parfum 100ml")
add("1855","Al Wataniah Shagaf Al Ward EDP Fem 100ml",135.00, "perf_arabe", "Al Wataniah Shagaf Al Ward 100ml")
add("1733","Al Wataniah Ameerati Fem EDP 100ml",     125.10, "perf_arabe", "Al Wataniah Ameerati 100ml")
add("1734","Al Wataniah Durrat Al Aroos EDP 85ml",   129.60, "perf_arabe", "Al Wataniah Durrat Al Aroos 85ml")
add("1149","Armaf Club de Nuit Intense Men EDT 105ml",230.40, "perf_arabe", "Armaf Club de Nuit Intense Man 105ml eau de toilette", badge="Novo")
add("1988","Armaf Club de Nuit Woman 100ml",         220.50, "perf_arabe", "Armaf Club de Nuit Woman 100ml")
add("2219","Asdaaf Ameerat Al Arab Vermelho EDP 100ml",129.60, "perf_arabe", "Asdaaf Ameerat Al Arab red eau de parfum 100ml", badge="Novo")
add("2077","French Avenue Liquid Brun EDP 100ml",    260.10, "perf_arabe", "French Avenue Liquid Brun eau de parfum 100ml", badge="Novo")
add("2179","French Avenue Vulcan Feu EDP 100ml",     285.30, "perf_arabe", "French Avenue Vulcan Feu eau de parfum 100ml")
add("2037","Hawas Black EDP 100ml (Rasasi)",         205.20, "perf_arabe", "Rasasi Hawas Black for him eau de parfum 100ml")
add("1937","Lattafa Asad Bourbon EDP 100ml",         190.80, "perf_arabe", "Lattafa Asad Bourbon 100ml eau de parfum")
add("1794","Lattafa Asad Elixir Men EDP 100ml",      230.40, "perf_arabe", "Lattafa Asad Elixir 100ml eau de parfum", badge="Novo")
add("1756","Lattafa Asad Men EDP 100ml",             170.10, "perf_arabe", "Lattafa Asad 100ml eau de parfum")
add("2246","Lattafa Asad - Kit 4 x 25ml",            260.10, "perf_arabe", "Lattafa Asad discovery set 4 x 25ml", badge="Kit")
add("2070","Lattafa Atheeri EDP 100ml",              350.10, "perf_arabe", "Lattafa Atheeri 100ml eau de parfum")
add("2237","Lattafa Confidential Gold EDP 100ml",    149.40, "perf_arabe", "Lattafa Confidential Gold eau de parfum 100ml", eq="insp. Tiziana Kirke")
add("1837","Lattafa Fakhar Black EDP 100ml",         170.10, "perf_arabe", "Lattafa Fakhar Black 100ml")
add("1870","Lattafa Fakhar Gold EDP 100ml",          160.20, "perf_arabe", "Lattafa Fakhar Gold men 100ml eau de parfum", badge="Novo")
add("1891","Lattafa Fakhar Fem EDP 100ml (rosa)",    210.60, "perf_arabe", "Lattafa Fakhar Lattafa for women 100ml rose")
add("1852","Lattafa Haya Fem EDP 100ml",             185.40, "perf_arabe", "Lattafa Haya 100ml eau de parfum", eq="insp. Prada Paradoxe", badge="Novo")
add("1929","Lattafa Musamman White EDP 100ml",       265.50, "perf_arabe", "Lattafa Musamman White eau de parfum 100ml")
add("2197","Lattafa Queen of Arabia EDP 100ml",      330.30, "perf_arabe", "Lattafa Queen of Arabia eau de parfum 100ml")
add("1707","Lattafa Tharwah Gold EDP 100ml",         290.70, "perf_arabe", "Lattafa Tharwah Gold 100ml")
add("1812","Lattafa Yara EDP 100ml (rosa)",          150.30, "perf_arabe", "Lattafa Yara 100ml eau de parfum pink", badge="Novo")
add("1962","Lattafa Yara - Kit 4 x 25ml",            215.10, "perf_arabe", "Lattafa Yara discovery set 4 x 25ml", badge="Kit")
add("1586","Maison Alhambra Delilah EDP 100ml",      180.00, "perf_arabe", "Maison Alhambra Delilah pour femme eau de parfum 100ml", eq="insp. Delina")
add("1991","Maison Alhambra Delilah Blanc EDP 100ml",190.80, "perf_arabe", "Maison Alhambra Delilah Blanc 100ml")
add("2036","Maison Alhambra Athenas EDP 100ml",      200.70, "perf_arabe", "Maison Alhambra Athenas 100ml")
add("2005","Maison Alhambra Alpine Homme Sport EDP 100ml", 140.40, "perf_arabe", "Maison Alhambra Alpine Homme Sport 100ml", eq="insp. Allure Sport")
add("1892","Maison Alhambra Leonie Fem EDP 100ml",   155.70, "perf_arabe", "Maison Alhambra Leonie 100ml", eq="insp. Libre")
add("2235","Maison Alhambra Papillon D'Or EDP 100ml",255.60, "perf_arabe", "Maison Alhambra Papillon D'Or 100ml eau de parfum", eq="insp. CH La Bomba", badge="Novo")
add("2114","Maison Alhambra Perseus Exclusif EDP 100ml",130.50, "perf_arabe", "Maison Alhambra Perseus 100ml eau de parfum", badge="Novo")
add("1964","Maison Alhambra Philos Pura EDP 100ml",  140.40, "perf_arabe", "Maison Alhambra Philos Pura 100ml eau de parfum", badge="Novo")
add("1890","Maison Alhambra Salvo Men EDP 100ml",    135.00, "perf_arabe", "Maison Alhambra Salvo 100ml", eq="insp. Sauvage")
add("1651","Maison Alhambra So Candid Pour Femme EDP 100ml", 135.00, "perf_arabe", "Maison Alhambra So Candid 100ml")
add("680", "NB Master of Pink Gold 100ml",           89.10, "perf_arabe", "New Brand Master pink gold 100ml eau de parfum", eq="insp. Olympéa", badge="Novo")
add("1650","Orientica Royal Amber EDP 80ml",         370.80, "perf_arabe", "Orientica Royal Amber eau de parfum 80ml")
add("2236","Sabah Al Ward Garden of Eden EDP 100ml", 250.20, "perf_arabe", "Sabah Al Ward Garden of Eden 100ml")

# --- Inspiracoes Arabic 25ml ---
add("2093","Arabic 25ml — inspiração Sabah",         50.40, "arabic_insp", "perfume 25ml arabic", eq="insp. Sabah")
add("1969","Arabic 25ml — Fakhar Rose",              50.40, "arabic_insp", "perfume 25ml arabic", eq="insp. Fakhar Rose")
add("2039","Arabic 25ml — Tharwad Gold",             50.40, "arabic_insp", "perfume 25ml arabic", eq="insp. Tharwad Gold")
add("1970","Arabic 25ml — Yara Rosa",                48.60, "arabic_insp", "perfume 25ml arabic", eq="insp. Yara Rosa")

# --- Contratipos Dream Brand 25ml ---
def db(cod, num, ref, preco):
    add(cod, f"Dream Brand {num} — {ref}", preco, "contratipo", "Dream Brand perfume 25ml", eq=f"insp. {ref}")
db("1109","005","One Million",40.50); db("1111","008","212 VIP Men",40.50); db("1265","009","212 VIP Fem",45.00)
db("1114","012","La Vie Est Belle",40.50); db("1780","014","Miss Dior Blooming",45.00); db("1219","015","Miss Dior",45.00)
db("1110","021","Coco Mademoiselle",40.50); db("1415","022","Decadence",45.00); db("1363","027","Hypnotic Poison",43.20)
db("1290","034","VIP Rose",40.50); db("1220","039","Chanel Chance",45.00); db("1291","043","Alien",40.50)
db("1322","055","Black Opium",45.90); db("1266","060","Narciso For Her",45.00); db("1267","063","Armani Si",45.00)
db("1107","069","La Nuit Trésor",45.00); db("1228","070","Bleu de Chanel",40.50); db("1108","087","Olympéa",40.50)
db("1229","097","Euphoria Fem",45.00); db("1256","100","Sauvage",45.00); db("1318","102","212 NYC Men",45.00)
db("1293","105","Lady Million",45.00); db("1112","126","Good Girl",58.50); db("1328","136","Scandal",43.20)
db("1547","151","Delina",45.00); db("1294","156","212 Sexy Men",45.00); db("1269","164","Armani Code Men",45.00)
db("1270","168","Angel EDP",45.00); db("1380","171","Jean Paul Classique Fem",45.00); db("1943","176","Issey Miyake Fem",45.00)
db("1414","181","Bad Boy",58.50); db("1446","214","Invictus Black",45.00); db("2097","225","Victoria Bombshell",45.00)
db("1419","238","Idôle",45.00); db("1423","240","212 NYC Fem",45.00); db("1451","265","Versace Dylan Fem",49.50)
db("1554","294","L'Interdit Rouge",45.00); db("2018","295","Ariana Grande Cloud",45.00); db("1503","296","Phantom",45.00)
db("2134","323","Le Male Elixir",45.00); db("1718","324","La Belle",40.50); db("2135","325","Le Male Le Parfum",45.00)
db("1604","340","212 Heroes Fem",45.90); db("1605","347","212 Heroes Men",45.00); db("2242","348","Delina La Rosée",45.00)
db("1592","351","Dylan Turquoise",45.00); db("2159","356","J'adore L'Or",45.00); db("1639","361","Libre Intense",45.00)
db("1624","365","Fame",45.00); db("1973","367","Valaya",45.00); db("1848","370","Versace Purple",53.00)
db("1906","382","L'Interdit",45.00); db("1878","387","Azzaro Wanted Parfum",45.00); db("1974","391","Valentino Born in Roma",45.00)
db("1819","415","Fame Parfum (preto)",47.70); db("2063","435","Burberry Goddess",45.00); db("2127","445","Prada Paradoxe",45.00)
db("1532","106","Versace Pour Homme",45.00)

# --- Bases ---
add("509", "Base Milani Nº 03",  79.20, "cosm_base", "Milani foundation bottle")

# --- Hidratantes Victoria's Secret ---
add("898", "Body Lotion VS Aqua Kiss (emb. nova)",         105.30, "cosm_vs_lot", "Victoria's Secret Aqua Kiss body lotion", badge="Emb. nova")
add("99",  "Body Lotion VS Coconut Passion",               105.30, "cosm_vs_lot", "Victoria's Secret Coconut Passion body lotion")
add("95",  "Body Lotion VS Love Spell 236ml",              105.30, "cosm_vs_lot", "Victoria's Secret Love Spell body lotion")
add("96",  "Body Lotion VS Pure Seduction",                105.30, "cosm_vs_lot", "Victoria's Secret Pure Seduction body lotion")
add("1593","Body Lotion VS Velvet Petals 236ml",           105.30, "cosm_vs_lot", "Victoria's Secret Velvet Petals body lotion")

# --- Body Splash Victoria's Secret ---
add("786", "Body Splash VS Aqua Kiss",                     105.30, "cosm_vs_spl", "Victoria's Secret Aqua Kiss fragrance mist")
add("250", "Body Splash VS Amber Romance",                 105.30, "cosm_vs_spl", "Victoria's Secret Amber Romance fragrance mist")
add("977", "Body Splash VS Bare Vanilla",                  110.70, "cosm_vs_spl", "Victoria's Secret Bare Vanilla fragrance mist")
add("251", "Body Splash VS Bare Vanilla Shimmer",          110.70, "cosm_vs_spl", "Victoria's Secret Bare Vanilla Shimmer fragrance mist")
add("380", "Body Splash VS Coconut Passion",               105.30, "cosm_vs_spl", "Victoria's Secret Coconut Passion fragrance mist")
add("1376","Body Splash VS Coconut Passion Shimmer",       105.30, "cosm_vs_spl", "Victoria's Secret Coconut Passion Shimmer fragrance mist")
add("1622","Body Splash VS Midnight Bloom",                105.30, "cosm_vs_spl", "Victoria's Secret Midnight Bloom fragrance mist")
add("234", "Body Splash VS Love Spell",                    105.30, "cosm_vs_spl", "Victoria's Secret Love Spell fragrance mist")
add("252", "Body Splash VS Pure Seduction",                105.30, "cosm_vs_spl", "Victoria's Secret Pure Seduction fragrance mist")
add("1016","Body Splash VS Romantic",                      105.30, "cosm_vs_spl", "Victoria's Secret Romantic fragrance mist")
add("488", "Body Splash VS Rush",                          105.30, "cosm_vs_spl", "Victoria's Secret Rush fragrance mist")
add("1054","Body Splash VS Temptation",                    105.30, "cosm_vs_spl", "Victoria's Secret Temptation fragrance mist")
add("1803","Body Splash VS Velvet Petals Shimmer",         110.70, "cosm_vs_spl", "Victoria's Secret Velvet Petals Shimmer fragrance mist")

# --- Cremes & Splash nacionais ---
add("1253","Creme Dream Brand 168 Angel 200ml",            39.60, "cosm_nac", "creme hidratante corporal", eq="insp. Angel")
add("1897","Isabelle Creme Angel 200ml",                   59.40, "cosm_nac", "creme hidratante corporal", eq="insp. Angel")
add("2055","Isabelle Creme La Vie 200ml",                  59.40, "cosm_nac", "creme hidratante corporal", eq="insp. La Vie Est Belle")
add("2203","Isabelle Splash La Vie 300ml",                 65.70, "cosm_nac", "body splash", eq="insp. La Vie Est Belle")
add("1385","Ciclo Creme La Vida",                          28.80, "cosm_nac", "Ciclo La Vida creme hidratante corporal")
add("1828","Ciclo Splash La Vida",                         32.85, "cosm_nac", "Ciclo La Vida body splash colonia")

# --- Body Mist Maison ---
add("2204","Maison Alhambra Body Mist Delilah 250ml",      65.70, "cosm_mist", "Maison Alhambra Delilah body mist", eq="insp. Delina")
add("2215","Maison Alhambra Body Mist Pink Eclipse 250ml", 65.70, "cosm_mist", "Maison Alhambra Pink Eclipse body mist", eq="insp. Paradoxe")

# --- Cabelo & Tratamento ---
add("1019","Joico Color Therapy Máscara 500g",             240.30, "cosm_cabelo", "Joico K-Pak Color Therapy mask 500ml")
add("196", "Joico Moisture Recovery Máscara 500ml",        144.00, "cosm_cabelo", "Joico Moisture Recovery hydration mask 500ml")
add("851", "Joico Moisture Recovery Combo Shampoo + Cond. 1L", 266.40, "cosm_cabelo", "Joico Moisture Recovery shampoo conditioner liter", badge="Combo")
add("112", "Revlon Uniq One Leave-in (vermelho) trad.",    69.30, "cosm_cabelo", "Revlon Uniq One leave-in 150ml")

# --- Corpo & Skincare ---
add("1103","St. Ives Creme Corporal Colágeno & Elastina 532ml", 45.00, "cosm_corpo", "St Ives Collagen Elastin body lotion 532ml")

# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s

# categorias que compartilham a mesma foto de frasco (contratipos 25ml)
CAT_FALLBACK = {"contratipo": "DB", "arabic_insp": "DB"}

# False = imagens WebP externas (site leve, lazy-load) | True = base64 embutido (HTML unico)
EMBED_IMAGES = False
IMG_EXTS = ("webp", "jpg", "jpeg", "png")

def _find(cod):
    for ext in IMG_EXTS:
        p = os.path.join(IMG_DIR, f"{cod}.{ext}")
        if os.path.exists(p):
            return cod, ext, p
    return None, None, None

def img_data(cod, cat=None):
    rc, ext, p = _find(cod)
    if p is None and cat in CAT_FALLBACK:
        rc, ext, p = _find(CAT_FALLBACK[cat])
    if p is None:
        return None
    if EMBED_IMAGES:
        with open(p, "rb") as f:
            b = f.read()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        return f"data:image/{mime};base64,{base64.b64encode(b).decode()}"
    return f"img/{rc}.{ext}"

def wa_link(prod):
    msg = f"Olá! Tenho interesse no produto {prod['cod']} - {prod['nome']} ({brl(prod['preco'])}). Está disponível?"
    return f"https://wa.me/{WHATSAPP}?text={html.escape(msg.replace(' ', '%20').replace(chr(10),''))}"

def esc(s): return html.escape(str(s))

# ----------------------------------------------------------------------------
# RENDER
# ----------------------------------------------------------------------------
total = len(P)
com_foto = sum(1 for p in P if img_data(p["cod"], p["cat"]))
menor = min(p["preco"] for p in P)

def data_attrs(p):
    return (f'data-cod="{esc(p["cod"])}" data-nome="{esc(p["nome"])}" data-preco="{p["preco"]:.2f}" '
            f'data-n="{esc(p["nome"].lower())} {esc(p["eq"].lower())} {p["cod"]}"')

def add_ctrl(mini=False):
    cls = "addwrap mini" if mini else "addwrap"
    lbl = "" if mini else "<span>Adicionar</span>"
    return (f'<div class="{cls}">'
            f'<button class="addbtn" type="button" data-add><i class="ti ti-plus"></i>{lbl}</button>'
            f'<div class="qtybox"><button type="button" data-dec aria-label="menos"><i class="ti ti-minus"></i></button>'
            f'<span data-qty>1</span>'
            f'<button type="button" data-inc aria-label="mais"><i class="ti ti-plus"></i></button></div>'
            f'</div>')

def card_html(p):
    src = img_data(p["cod"], p["cat"])
    if src:
        media = f'<img loading="lazy" decoding="async" src="{src}" alt="{esc(p["nome"])}">'
    else:
        ini = esc(p["nome"][:1].upper())
        media = f'<div class="ph"><span>{ini}</span></div>'
    badge = f'<span class="badge">{esc(p["badge"])}</span>' if p["badge"] else ""
    eq = f'<p class="eq">{esc(p["eq"])}</p>' if p["eq"] else ""
    return f'''<article class="card" {data_attrs(p)}>
      <div class="media">{media}{badge}</div>
      <div class="info">
        <p class="nome">{esc(p['nome'])}</p>{eq}
        <div class="row"><span class="cod">#{esc(p['cod'])}</span><span class="preco">{brl(p['preco'])}</span></div>
        {add_ctrl(False)}
      </div>
    </article>'''

def lista_html(p):
    src = img_data(p["cod"], p["cat"])
    thumb = f'<img loading="lazy" decoding="async" src="{src}" alt="{esc(p["nome"])}">' if src else '<i class="ti ti-droplet"></i>'
    eq = f'<span class="leq">{esc(p["eq"])}</span>' if p["eq"] else ""
    return f'''<div class="li" {data_attrs(p)}>
      <span class="lthumb">{thumb}</span>
      <span class="lname">{esc(p['nome'])}{eq}<span class="lcod">#{esc(p['cod'])}</span></span>
      <span class="lpreco">{brl(p['preco'])}</span>
      {add_ctrl(True)}
    </div>'''

secoes = []
nav = []
for key, titulo, icon, modo in CATEGORIAS:
    itens = [p for p in P if p["cat"] == key]
    if not itens: continue
    nav.append(f'<a href="#{key}"><i class="ti {icon}"></i>{esc(titulo)} <b>{len(itens)}</b></a>')
    if modo == "lista":
        corpo = '<div class="lista">' + "".join(lista_html(p) for p in itens) + '</div>'
    else:
        corpo = '<div class="grid">' + "".join(card_html(p) for p in itens) + '</div>'
    secoes.append(f'''<section id="{key}">
      <h2 class="sec-h"><i class="ti {icon}"></i>{esc(titulo)}<span class="qt">{len(itens)} itens</span><i class="ti ti-chevron-down chev"></i></h2>
      <div class="sec-body">{corpo}</div>
    </section>''')

HTML = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(MARCA)} — Catálogo</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.7.0/dist/tabler-icons.min.css" rel="stylesheet">
<style>
:root{{--bg:#fbf7f4;--ink:#2a1720;--wine:#5c1a32;--wine2:#7a2444;--rose:#b9456b;--rose-l:#f4dbe4;--gold:#c79a3e;--card:#fff;--line:#ecdfe4;--mut:#6e555d}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--ink);line-height:1.45}}
img{{display:block;width:100%;height:100%;object-fit:contain}}
a{{text-decoration:none;color:inherit}}
.wrap{{max-width:860px;margin:0 auto;padding:0 14px 60px}}

/* CAPA */
.capa{{background:linear-gradient(160deg,#5c1a32,#7a2444 60%,#9c2f54);color:#fff;text-align:center;padding:46px 20px 40px;border-radius:0 0 26px 26px;position:relative;overflow:hidden}}
.capa::after{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 80% -10%,rgba(255,255,255,.18),transparent 45%)}}
.logo{{font-family:Georgia,'Times New Roman',serif;font-size:13px;letter-spacing:7px;color:var(--gold);text-transform:uppercase}}
.capa h1{{font-family:Georgia,serif;font-size:40px;font-weight:600;margin:8px 0 4px;letter-spacing:.5px}}
.capa .sub{{color:#f3c9d6;font-size:14px;max-width:430px;margin:6px auto 0}}
.capa .selo{{display:inline-block;margin-top:18px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.35);color:#fff;font-size:12px;letter-spacing:1px;padding:7px 16px;border-radius:30px}}
.capa .atualizado{{margin-top:8px;color:rgba(255,255,255,.78);font-size:11px;letter-spacing:.5px}}
.capa .atualizado i{{font-size:12px;vertical-align:-1px;margin-right:4px}}
.stats{{display:flex;gap:10px;justify-content:center;margin-top:20px;flex-wrap:wrap}}
.stats div{{background:rgba(0,0,0,.18);border-radius:12px;padding:8px 14px;min-width:84px}}
.stats b{{display:block;font-size:20px;font-family:Georgia,serif}}
.stats span{{font-size:11px;color:#f0c2d0}}

/* BUSCA + NAV */
.tools{{position:sticky;top:0;z-index:20;background:var(--bg);padding:12px 0 8px;margin-top:6px}}
.search{{display:flex;align-items:center;gap:8px;background:#fff;border:1px solid var(--line);border-radius:30px;padding:10px 16px;box-shadow:0 2px 10px rgba(92,26,50,.06)}}
.search i{{color:var(--rose)}}
.search input{{border:0;outline:0;flex:1;font-size:15px;background:transparent;color:var(--ink)}}
.nav{{display:flex;gap:8px;overflow-x:auto;padding:10px 0 2px;-webkit-overflow-scrolling:touch}}
.nav a{{white-space:nowrap;font-size:12.5px;color:var(--wine);background:#fff;border:1px solid var(--line);padding:7px 13px;border-radius:30px;display:flex;align-items:center;gap:6px}}
.nav a b{{background:var(--rose-l);color:var(--wine2);border-radius:20px;padding:1px 7px;font-size:11px}}
.nav a i{{color:var(--rose)}}

/* SECOES */
section{{margin-top:26px;scroll-margin-top:118px}}
h2{{display:flex;align-items:center;gap:10px;font-family:Georgia,serif;font-size:21px;color:var(--wine);font-weight:600;padding-bottom:8px;border-bottom:2px solid var(--rose-l)}}
h2 i{{color:var(--rose)}}
h2 .qt{{margin-left:auto;font-family:'Segoe UI',sans-serif;font-size:12px;font-weight:400;color:var(--mut)}}

/* GRID CARDS */
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(158px,1fr));gap:12px;margin-top:14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;transition:.15s;box-shadow:0 2px 8px rgba(92,26,50,.05)}}
.card:hover{{transform:translateY(-3px);box-shadow:0 8px 20px rgba(92,26,50,.13)}}
.media{{position:relative;height:150px;background:#fff;padding:12px;border-bottom:1px solid var(--line)}}
.ph{{display:flex;align-items:center;justify-content:center;height:100%;background:linear-gradient(135deg,#f7e9ee,#fbf3f6);border-radius:10px}}
.ph span{{font-family:Georgia,serif;font-size:40px;color:var(--rose);opacity:.55}}
.badge{{position:absolute;top:8px;left:8px;background:var(--gold);color:#3a2a05;font-size:10px;font-weight:700;letter-spacing:.4px;padding:3px 9px;border-radius:20px;text-transform:uppercase}}
.info{{padding:11px 12px 13px;display:flex;flex-direction:column;gap:5px;flex:1}}
.nome{{font-size:13.5px;font-weight:600;line-height:1.25;min-height:34px}}
.eq{{font-size:11.5px;color:var(--rose);font-style:italic}}
.row{{display:flex;align-items:baseline;justify-content:space-between;margin-top:auto;gap:6px}}
.cod{{font-size:11px;color:var(--mut)}}
.preco{{font-family:Georgia,serif;font-size:18px;font-weight:700;color:var(--wine)}}
/* ADICIONAR / STEPPER */
.addwrap{{margin-top:4px}}
.addbtn{{display:flex;width:100%;align-items:center;justify-content:center;gap:6px;background:#25d366;color:#063b1c;font-size:12.5px;font-weight:600;padding:11px 8px;min-height:44px;border:0;border-radius:9px;cursor:pointer;transition:.12s}}
.addbtn:hover{{background:#1fc25b}}
.addbtn i{{font-size:16px}}
.qtybox{{display:none;align-items:center;justify-content:space-between;gap:6px;background:#eaf7ee;border:1px solid #bfe6cb;border-radius:9px;padding:4px;margin-top:4px}}
.qtybox button{{width:40px;height:40px;border:0;border-radius:7px;background:#25d366;color:#063b1c;font-size:16px;display:flex;align-items:center;justify-content:center;cursor:pointer}}
.qtybox button:hover{{background:#1fc25b}}
.qtybox [data-qty]{{font-weight:700;color:#0a3a1c;min-width:22px;text-align:center;font-size:15px}}
.incart .addbtn{{display:none}}
.incart .qtybox{{display:flex}}
.incart.card{{outline:2px solid #25d366;outline-offset:-2px}}
.incart.li{{border-color:#25d366;background:#f4fcf6}}
/* controle compacto (listas / contratipos) */
.addwrap.mini{{margin:0;flex:none}}
.addwrap.mini .addbtn{{width:44px;min-height:44px;padding:0;font-size:0}}
.addwrap.mini .addbtn i{{font-size:18px}}
.addwrap.mini .qtybox{{margin:0;padding:3px}}
.addwrap.mini .qtybox button{{width:38px;height:38px;font-size:15px}}
.addwrap.mini .qtybox [data-qty]{{min-width:18px;font-size:13px}}

/* LISTA (contratipos) */
.lista{{display:grid;grid-template-columns:1fr;gap:8px;margin-top:14px}}
@media(min-width:560px){{.lista{{grid-template-columns:1fr 1fr}}}}
.li{{display:flex;align-items:center;gap:11px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px 12px;transition:.12s}}
.li:hover{{border-color:var(--rose);background:#fffafc}}
.lthumb{{width:40px;height:40px;flex:none;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#f7e9ee,#fbf3f6);border-radius:8px;color:var(--rose);font-size:18px;overflow:hidden}}
.lname{{flex:1;font-size:13px;font-weight:600;line-height:1.2;display:flex;flex-direction:column;gap:1px}}
.leq{{font-size:11px;color:var(--rose);font-style:italic;font-weight:400}}
.lcod{{font-size:10.5px;color:var(--mut);font-weight:400}}
.lpreco{{font-family:Georgia,serif;font-size:15.5px;font-weight:700;color:var(--wine);white-space:nowrap}}

.empty{{text-align:center;color:var(--mut);padding:40px 0;font-size:15px;display:none}}

/* RODAPE */
footer{{background:var(--wine);color:#fff;border-radius:22px;margin-top:42px;padding:30px 22px;text-align:center}}
footer h3{{font-family:Georgia,serif;font-size:24px;color:#fff;margin-bottom:4px}}
footer .fsub{{color:#f0c2d0;font-size:13px;margin-bottom:18px}}
.fcontacts{{display:flex;flex-direction:column;gap:11px;max-width:340px;margin:0 auto}}
.fcontacts a,.fcontacts div{{display:flex;align-items:center;gap:11px;justify-content:center;color:#fff;font-size:14px;background:rgba(255,255,255,.1);border-radius:11px;padding:11px 14px}}
.fcontacts i{{color:var(--gold);font-size:18px}}
.fbtn{{background:#25d366!important;color:#063b1c!important;font-weight:700!important;margin-top:4px}}
.note{{margin-top:18px;color:#e7aebf;font-size:11px;line-height:1.5}}
.top{{position:fixed;right:16px;bottom:16px;z-index:30;background:var(--wine);color:#fff;width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,.25);font-size:20px}}
body.has-cart .top{{bottom:80px}}

/* ACORDEAO */
.sec-h{{cursor:pointer;user-select:none}}
.chev{{margin-left:10px;color:var(--rose);font-size:18px;transition:transform .2s}}
.collapsed .chev{{transform:rotate(-90deg)}}
.collapsed .sec-body{{display:none}}
.searching .sec-body{{display:block!important}}

/* ALTERNAR VISUALIZACAO */
.viewtoggle{{display:flex;gap:0;background:#fff;border:1px solid var(--line);border-radius:30px;padding:3px;margin-top:10px;width:fit-content}}
.viewtoggle button{{border:0;background:transparent;color:var(--mut);font-size:12.5px;font-weight:600;padding:7px 15px;border-radius:30px;display:flex;align-items:center;gap:6px;cursor:pointer}}
.viewtoggle button.active{{background:var(--wine);color:#fff}}
.viewtoggle i{{font-size:16px}}

/* MODO LISTA (cards viram linhas) */
.listview .grid{{grid-template-columns:1fr;gap:8px}}
@media(min-width:560px){{.listview .grid{{grid-template-columns:1fr 1fr}}}}
.listview .card{{flex-direction:row;align-items:center;border-radius:12px;padding:6px 10px 6px 6px;box-shadow:none}}
.listview .card:hover{{transform:none;box-shadow:0 2px 8px rgba(92,26,50,.08)}}
.listview .media{{width:46px;height:46px;flex:none;padding:3px;border:0;border-radius:8px}}
.listview .badge{{display:none}}
.listview .info{{flex-direction:row;align-items:center;gap:10px;padding:0 0 0 10px}}
.listview .nome{{min-height:0;font-size:13px;flex:1}}
.listview .eq{{display:none}}
.listview .row{{flex:none;margin:0;flex-direction:column;align-items:flex-end;gap:0}}
.listview .cod{{display:none}}
.listview .preco{{font-size:15.5px}}
.listview .addwrap{{margin:0;flex:none}}
.listview .addbtn{{width:44px;min-height:44px;padding:0;font-size:0}}
.listview .addbtn i{{font-size:18px}}
.listview .addbtn span{{display:none}}
.listview .qtybox{{margin:0;padding:3px}}
.listview .qtybox button{{width:38px;height:38px;font-size:15px}}
.listview .qtybox [data-qty]{{min-width:18px;font-size:13px}}

/* BARRA + PAINEL DO CARRINHO */
.cartbar{{position:fixed;left:0;right:0;bottom:0;z-index:40;background:#fff;border-top:1px solid var(--line);box-shadow:0 -4px 16px rgba(92,26,50,.14)}}
.cartbar[hidden]{{display:none}}
.cb-inner{{max-width:860px;margin:0 auto;display:flex;gap:10px;align-items:center;padding:10px 14px}}
.cart-info{{flex:1;text-align:left;background:transparent;border:0;color:var(--wine);font-weight:600;font-size:13px;display:flex;align-items:center;gap:7px;cursor:pointer}}
.cart-info .ci-ic{{position:relative;font-size:22px;color:var(--rose)}}
.cart-info b{{font-family:Georgia,serif;font-size:17px}}
.cart-go{{background:#25d366;color:#063b1c;border:0;border-radius:11px;font-size:14px;font-weight:700;padding:12px 16px;display:flex;align-items:center;gap:7px;cursor:pointer}}
.cart-go:hover{{background:#1fc25b}}
.cart-go i{{font-size:18px}}
.overlay{{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:44;opacity:0;pointer-events:none;transition:.25s}}
.overlay.show{{opacity:1;pointer-events:auto}}
.cartpanel{{position:fixed;left:0;right:0;bottom:0;z-index:45;background:#fff;border-radius:18px 18px 0 0;box-shadow:0 -8px 30px rgba(0,0,0,.28);max-width:860px;margin:0 auto;max-height:78vh;display:flex;flex-direction:column;transform:translateY(110%);transition:transform .25s}}
.cartpanel.open{{transform:translateY(0)}}
.cp-head{{display:flex;align-items:center;justify-content:space-between;padding:16px 18px 12px;border-bottom:1px solid var(--line);cursor:pointer}}
.cp-head h4{{font-family:Georgia,serif;font-size:19px;color:var(--wine);font-weight:600}}
.cp-x{{background:transparent;border:0;font-size:24px;color:var(--mut);cursor:pointer;line-height:1}}
.cp-list{{overflow-y:auto;padding:4px 16px}}
.cp-empty{{text-align:center;color:var(--mut);padding:30px 0;font-size:14px}}
.cp-row{{display:flex;align-items:center;gap:10px;padding:11px 0;border-bottom:1px solid #f3eaee}}
.cp-n{{flex:1;font-size:13px;font-weight:600;line-height:1.25}}
.cp-n small{{display:block;color:var(--mut);font-weight:400;font-size:11px}}
.cp-line{{font-family:Georgia,serif;font-weight:700;color:var(--wine);font-size:14px;white-space:nowrap}}
.cp-rem{{background:transparent;border:0;color:#c0394b;font-size:18px;cursor:pointer;padding:4px}}
.cp-foot{{padding:14px 18px 18px;border-top:1px solid var(--line);background:#fff}}
.cp-total{{display:flex;justify-content:space-between;align-items:baseline;font-size:15px;margin-bottom:12px;color:var(--ink)}}
.cp-total b{{font-family:Georgia,serif;font-size:22px;color:var(--wine)}}
.cp-nome{{width:100%;border:1px solid var(--line);border-radius:11px;padding:12px 14px;font-size:15px;color:var(--ink);outline:none;margin-bottom:10px;font-family:inherit}}
.cp-nome::placeholder{{color:var(--mut)}}
.cp-nome:focus{{border-color:var(--rose)}}
.cp-nome.err{{border-color:#e24b4a;background:#fdeceb}}
.cp-go{{width:100%;background:#25d366;color:#063b1c;border:0;border-radius:12px;font-size:15px;font-weight:700;padding:14px;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer}}
.cp-go:hover{{background:#1fc25b}}
.cp-go i{{font-size:19px}}
.cp-safe{{margin:10px 0 0;text-align:center;font-size:12px;color:var(--mut);line-height:1.55}}
.cp-safe i{{color:#25d366;font-size:14px;vertical-align:-2px;margin-right:4px}}
.cp-clear{{display:block;margin:10px auto 0;background:transparent;border:0;color:var(--mut);font-size:12px;text-decoration:underline;cursor:pointer}}
</style>
</head>
<body>
<div class="capa">
  <div class="logo">Distribuidora</div>
  <h1>{esc(MARCA)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <div class="selo">{esc(REFERENCIA)}</div>
  <div class="atualizado"><i class="ti ti-calendar-check"></i>Atualizado em {esc(ATUALIZADO)}</div>
  <div class="stats">
    <div><b>{total}</b><span>produtos</span></div>
    <div><b>{brl(menor).replace('R$ ','R$')}</b><span>a partir de</span></div>
    <div><b>100%</b><span>originais</span></div>
  </div>
</div>

<div class="wrap">
  <div class="tools">
    <label class="search"><i class="ti ti-search"></i><input id="q" type="search" placeholder="Buscar produto, marca ou código..."></label>
    <div class="viewtoggle">
      <button id="vCards" class="active" type="button"><i class="ti ti-layout-grid"></i> Cards</button>
      <button id="vList" type="button"><i class="ti ti-list"></i> Lista</button>
    </div>
  </div>

  <p class="empty" id="empty">Nenhum produto encontrado. Tente outro termo.</p>

  {''.join(secoes)}

  <footer>
    <h3>{esc(MARCA)}</h3>
    <p class="fsub">Faça seu pedido pelo WhatsApp · atacado e revenda</p>
    <div class="fcontacts">
      <a class="fbtn" href="https://wa.me/{WHATSAPP}" target="_blank"><i class="ti ti-brand-whatsapp"></i> {esc(WHATSAPP_F)}</a>
      <a href="https://instagram.com/{esc(INSTAGRAM)}" target="_blank"><i class="ti ti-brand-instagram"></i> @{esc(INSTAGRAM)}</a>
      <div><i class="ti ti-map-pin"></i> {esc(ENDERECO)}</div>
    </div>
    <p class="note">Imagens meramente ilustrativas. Preços de atacado sujeitos a alteração sem aviso prévio. {esc(REFERENCIA)}.</p>
  </footer>
</div>
<a href="#" class="top" aria-label="Voltar ao topo"><i class="ti ti-arrow-up"></i></a>

<div class="cartbar" id="cartbar" hidden><div class="cb-inner">
  <button class="cart-info" id="cInfo" type="button"><i class="ti ti-shopping-cart ci-ic"></i><span><b id="cCount">0</b> itens · <span id="cTotal">R$ 0,00</span></span></button>
  <button class="cart-go" id="cGo" type="button">Fechar Pedido <i class="ti ti-brand-whatsapp"></i></button>
</div></div>

<div class="overlay" id="overlay"></div>
<div class="cartpanel" id="cartpanel">
  <div class="cp-head" id="cpHead"><h4>Seu pedido</h4><button class="cp-x" id="cpClose" type="button">&times;</button></div>
  <div class="cp-list" id="cpList"></div>
  <div class="cp-foot">
    <div class="cp-total"><span>Total do pedido</span><b id="cpTotal">R$ 0,00</b></div>
    <input id="cpNome" class="cp-nome" type="text" placeholder="Seu nome (para identificar o pedido)" autocomplete="name">
    <button class="cp-go" id="cpGo" type="button"><i class="ti ti-brand-whatsapp"></i> Fechar Pedido no WhatsApp</button>
    <p class="cp-safe"><i class="ti ti-lock"></i> Abre o WhatsApp com seu pedido pronto.<br>Você confirma tudo na conversa.</p>
    <button class="cp-clear" id="cpClear" type="button">Limpar pedido</button>
  </div>
</div>

<script>
const WA="{WHATSAPP}", MARCA_PED="{MARCA}";
const BRL=new Intl.NumberFormat('pt-BR',{{style:'currency',currency:'BRL'}});
const fmt=v=>BRL.format(v);
const wrap=document.querySelector('.wrap');

const q=document.getElementById('q'),empty=document.getElementById('empty');
const items=[...document.querySelectorAll('[data-n]')],secs=[...document.querySelectorAll('section')];
q.addEventListener('input',()=>{{
  const t=q.value.toLowerCase().trim();let any=false;
  wrap.classList.toggle('searching', !!t);
  items.forEach(el=>{{const m=!t||el.dataset.n.includes(t);el.style.display=m?'':'none';if(m)any=true;}});
  secs.forEach(s=>{{const vis=[...s.querySelectorAll('[data-n]')].some(e=>e.style.display!=='none');s.style.display=vis?'':'none';}});
  empty.style.display=any?'none':'block';
}});

document.querySelectorAll('.sec-h').forEach(h=>h.addEventListener('click',()=>h.closest('section').classList.toggle('collapsed')));

const vC=document.getElementById('vCards'),vL=document.getElementById('vList');
vC.onclick=()=>{{wrap.classList.remove('listview');vC.classList.add('active');vL.classList.remove('active');}};
vL.onclick=()=>{{wrap.classList.add('listview');vL.classList.add('active');vC.classList.remove('active');}};

const cart={{}};
const LS='pedido_alvaro_v1';
function save(){{try{{localStorage.setItem(LS,JSON.stringify(cart));}}catch(e){{}}}}
const bar=document.getElementById('cartbar'),panel=document.getElementById('cartpanel'),overlay=document.getElementById('overlay');
const cCount=document.getElementById('cCount'),cTotal=document.getElementById('cTotal'),cpList=document.getElementById('cpList'),cpTotal=document.getElementById('cpTotal');

function syncItem(cod){{
  document.querySelectorAll('[data-cod="'+cod+'"]').forEach(el=>{{
    if(!el.classList.contains('card')&&!el.classList.contains('li'))return;
    const qy=cart[cod]?cart[cod].qty:0;
    el.classList.toggle('incart', qy>0);
    const s=el.querySelector('[data-qty]'); if(s)s.textContent=qy||1;
  }});
}}
function addItem(el){{
  const cod=el.dataset.cod;
  if(cart[cod])cart[cod].qty++;
  else cart[cod]={{nome:el.dataset.nome,preco:parseFloat(el.dataset.preco),qty:1}};
  syncItem(cod);render();
}}
function chg(cod,d){{
  if(!cart[cod])return;
  cart[cod].qty+=d;
  if(cart[cod].qty<=0)delete cart[cod];
  syncItem(cod);render();
}}
function totals(){{let n=0,t=0;for(const k in cart){{n+=cart[k].qty;t+=cart[k].qty*cart[k].preco;}}return{{n:n,t:t}};}}
function render(){{
  save();
  const tt=totals();
  cCount.textContent=tt.n;cTotal.textContent=fmt(tt.t);
  bar.hidden=tt.n===0;document.body.classList.toggle('has-cart',tt.n>0);
  if(tt.n===0)closePanel();
  cpTotal.textContent=fmt(tt.t);
  const ks=Object.keys(cart);
  cpList.innerHTML=ks.length?ks.map(cod=>{{const it=cart[cod];const line=it.qty*it.preco;
    return '<div class="cp-row" data-cod="'+cod+'"><div class="cp-n">'+it.nome+'<small>#'+cod+' · '+fmt(it.preco)+(it.qty>1?' · '+it.qty+'x':'')+'</small></div>'+
      '<div class="qtybox" style="display:flex"><button type="button" data-dec><i class="ti ti-minus"></i></button><span>'+it.qty+'</span><button type="button" data-inc><i class="ti ti-plus"></i></button></div>'+
      '<span class="cp-line">'+fmt(line)+'</span><button class="cp-rem" type="button" data-rem aria-label="remover"><i class="ti ti-trash"></i></button></div>';
  }}).join(''):'<p class="cp-empty">Seu pedido está vazio. Toque em + Adicionar nos produtos.</p>';
}}
function openPanel(){{if(Object.keys(cart).length){{panel.classList.add('open');overlay.classList.add('show');}}}}
function closePanel(){{panel.classList.remove('open');overlay.classList.remove('show');}}

document.addEventListener('click',e=>{{
  const add=e.target.closest('[data-add]'),inc=e.target.closest('[data-inc]'),dec=e.target.closest('[data-dec]'),rem=e.target.closest('[data-rem]');
  if(add){{addItem(add.closest('[data-cod]'));}}
  else if(inc){{chg(inc.closest('[data-cod]').dataset.cod,1);}}
  else if(dec){{chg(dec.closest('[data-cod]').dataset.cod,-1);}}
  else if(rem){{const cod=rem.closest('[data-cod]').dataset.cod;delete cart[cod];syncItem(cod);render();}}
}});
document.getElementById('cInfo').onclick=()=>{{panel.classList.contains('open')?closePanel():openPanel();}};
document.getElementById('cpHead').onclick=closePanel;
overlay.onclick=closePanel;
document.getElementById('cpClear').onclick=()=>{{const ks=Object.keys(cart);ks.forEach(c=>delete cart[c]);ks.forEach(syncItem);render();}};

const cpNome=document.getElementById('cpNome');
cpNome.addEventListener('input',()=>cpNome.classList.remove('err'));
function fechar(){{
  const ks=Object.keys(cart);if(!ks.length)return;
  const nome=cpNome.value.trim();
  if(!nome){{openPanel();cpNome.classList.add('err');cpNome.placeholder='Por favor, digite seu nome';cpNome.focus();return;}}
  const lines=ks.map(cod=>{{const it=cart[cod];const line=it.qty*it.preco;
    const qx=it.qty>1?' ('+it.qty+'x '+fmt(it.preco)+')':'';
    return '#'+cod+' - '+it.nome+qx+' - '+fmt(line);}});
  const tt=totals();
  const msg='*Pedido - '+nome+'*\\n\\n'+lines.join('\\n')+'\\n\\n*Total: '+fmt(tt.t)+'*';
  window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(msg),'_blank');
}}
document.getElementById('cGo').onclick=()=>{{openPanel();setTimeout(()=>cpNome.focus(),250);}};
document.getElementById('cpGo').onclick=fechar;

/* restaura pedido salvo (nao perde ao recarregar) */
(function restore(){{try{{const s=JSON.parse(localStorage.getItem(LS)||'{{}}');for(const k in s)cart[k]=s[k];}}catch(e){{}}Object.keys(cart).forEach(syncItem);render();}})();
</script>
</body>
</html>'''

with open(SAIDA, "w", encoding="utf-8") as f:
    f.write(HTML)

kb = os.path.getsize(SAIDA) / 1024
print(f"OK -> {SAIDA}")
print(f"   {total} produtos | {com_foto} com foto | {total-com_foto} sem foto | {kb:.0f} KB")
