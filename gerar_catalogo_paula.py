# -*- coding: utf-8 -*-
"""
Gerador do catalogo visual Paula Fernanda (Perfumes & Cosmeticos - Atacado).
Le as fotos de img/<codigo>.jpg (se existirem), embute em base64 e gera um
unico arquivo HTML autossuficiente (catalogo.html), pronto p/ WhatsApp/celular.
Rode:  python gerar_catalogo_paula.py
"""
import os, io, base64, html, datetime, json, unicodedata

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
REFERENCIA = "Tabela de Atacado · 13/07/2026"
# Data da ultima atualizacao de PRODUTOS/PRECOS (formato DD/MM/AAAA).
# >>> SO TROQUE quando mudar produto ou preco. Melhorias no site NAO contam. <<<
ATUALIZADO = "24/06/2026"

# ----------------------------------------------------------------------------
# CATEGORIAS (ordem de exibicao)
# ----------------------------------------------------------------------------
CATEGORIAS = [
    ("promo",        "Promoção da Copa",           "ti-ball-football",  "card"),
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
    ("acess_vela",   "Velas Perfumadas",           "ti-flame",          "card"),
    ("acess_corpo",  "Géis & Hidratantes",         "ti-bath",           "card"),
    ("acess_bolsa",  "Necessaires & Bolsas",       "ti-briefcase",      "card"),
]

# ----------------------------------------------------------------------------
# PRODUTOS  (codigo, nome, preco, categoria, query_imagem, equivalencia, badge)
# ----------------------------------------------------------------------------
P = []
def add(cod, nome, preco, cat, q="", eq="", badge="", de=0):
    # de = preco "de" (antigo). Se de > preco, vira oferta (mostra riscado + % off).
    P.append(dict(cod=cod, nome=nome, preco=preco, cat=cat, q=q or nome, eq=eq, badge=badge, de=de))

# --- PROMOCAO DA COPA (estoque limitado) ---
add("CP1", "Bad Boy Cobalt 150ml EDP",                 499.00, "promo", "Carolina Herrera Bad Boy Cobalt 150ml eau de parfum", de=570.00)
add("CP2", "Bad Boy Le Parfum 50ml",                   299.00, "promo", "Carolina Herrera Bad Boy Le Parfum 50ml", de=360.00)
add("CP3", "Bad Boy Sparkling Ice 100ml",              350.00, "promo", "Carolina Herrera Bad Boy Sparkling Ice 100ml", de=410.00)
add("CP4", "Black XS Men 50ml EDT",                    259.00, "promo", "Paco Rabanne Black XS for him 50ml eau de toilette", de=299.00)
add("CP5", "Jean Paul Gaultier Divine Le Parfum 100ml",499.00, "promo", "Jean Paul Gaultier Divine Le Parfum 100ml", de=590.00)
add("CP6", "Good Girl Légère 80ml EDP",                430.00, "promo", "Carolina Herrera Good Girl Legere 80ml eau de parfum", de=510.00)
add("CP7", "Good Girl Sparkling Ice 80ml EDP",         430.00, "promo", "Carolina Herrera Good Girl 80ml eau de parfum", eq="mesmo cheiro do tradicional · edição colecionador", de=500.00)
add("CP8", "One Million 200ml EDT",                    480.00, "promo", "Paco Rabanne One Million 200ml eau de toilette", de=520.00)
add("CP9", "Armani Si Intense 100ml EDP",              490.00, "promo", "Giorgio Armani Si Intense 100ml eau de parfum", de=560.00)
add("CP10","Good Girl Very Glam 30ml EDP",             259.00, "promo", "Carolina Herrera Good Girl Very Glam 30ml eau de parfum", de=299.00)

# --- Perfumes importados ---
add("142", "Animale For Men 100ml EDT",              175.50, "perf_import", "Animale for men eau de toilette 100ml")
add("2",   "Azzaro Pour Homme 100ml EDT",            230.40, "perf_import", "Azzaro Pour Homme 100ml eau de toilette")
add("22",  "CH 212 NYC Men 100ml EDT",               380.70, "perf_import", "Carolina Herrera 212 NYC Men 100ml eau de toilette")
add("48",  "Dolce & Gabbana Light Blue Fem 100ml EDT",399.60, "perf_import", "Dolce Gabbana Light Blue pour femme 100ml eau de toilette")
add("52",  "Ferrari Black 125ml EDT",                150.30, "perf_import", "Ferrari Black 125ml eau de toilette")
add("248", "Gabriela Sabatini Fem 60ml EDT",         90.00, "perf_import", "Gabriela Sabatini eau de toilette 60ml")
add("74",  "Paco Rabanne One Million 100ml EDT",     380.70, "perf_import", "Paco Rabanne One Million 100ml eau de toilette")
add("674", "UDV For Men Cinza 100ml EDT",            74.70, "perf_import", "Ulric de Varens UDV pour homme grey 100ml", badge="Novo")
add("38",  "Chanel Coco Mademoiselle 100ml EDP",     950.40, "perf_import", "Chanel Coco Mademoiselle 100ml eau de parfum", badge="Novo")
add("2103","CH La Bomba 80ml EDP",                   570.60, "perf_import", "Carolina Herrera CH La Bomba 80ml eau de parfum")
add("23",  "CH 212 Sexy Men 100ml EDT",              400.50, "perf_import", "Carolina Herrera 212 Sexy Men 100ml")
add("26",  "CH 212 VIP Femme 80ml EDP",              470.70, "perf_import", "Carolina Herrera 212 VIP women eau de parfum 80ml")
add("717", "CH 212 VIP Black Men 100ml",             415.80, "perf_import", "Carolina Herrera 212 VIP Black Men 100ml")
add("24",  "CH 212 VIP Men 100ml EDT",               405.00, "perf_import", "Carolina Herrera 212 VIP Men 100ml")
add("20",  "CK Euphoria Fem 100ml EDP",              320.40, "perf_import", "Calvin Klein Euphoria 100ml eau de parfum")
add("21",  "CK Euphoria Men 100ml EDT",              240.30, "perf_import", "Calvin Klein Euphoria Men 100ml eau de toilette", badge="Novo")
add("44",  "Dior J'adore 100ml EDP",                 650.70, "perf_import", "Dior J'adore eau de parfum 100ml")
add("1989","Dolce & Gabbana K Men - Kit 100ml + gel + pós barba", 460.80, "perf_import", "Dolce Gabbana K King men eau de parfum 100ml", badge="Kit")
add("68",  "Joop! Homme 125ml EDT",                  165.60, "perf_import", "Joop Homme 125ml eau de toilette", badge="Novo")
add("132", "Lancôme La Vie Est Belle 100ml EDP",     535.50, "perf_import", "Lancome La Vie Est Belle 100ml eau de parfum")
add("70",  "Marina de Bourbon Rouge Royal 100ml EDP",209.70, "perf_import", "Marina de Bourbon Rouge Royal 100ml")
add("567", "Marina de Bourbon Royal Diamond 100ml EDP",210.60, "perf_import", "Princesse Marina de Bourbon Royal Diamond 100ml")
add("113", "Paco Rabanne Olympéa 80ml EDP",          460.80, "perf_import", "Paco Rabanne Olympea 80ml eau de parfum", badge="Novo")
add("80",  "Paco Rabanne Invictus 100ml EDT",        380.70, "perf_import", "Paco Rabanne Invictus 100ml eau de toilette")
add("78",  "Paco Rabanne Lady Million 80ml EDP",     450.90, "perf_import", "Paco Rabanne Lady Million 80ml eau de parfum")
add("233", "Silver Scent Intense Masculino 100ml EDT",165.60, "perf_import", "Jacques Bogart Silver Scent Intense 100ml eau de toilette")
add("127", "Silver Scent Tradicional 100ml EDT",     150.30, "perf_import", "Jacques Bogart Silver Scent 100ml eau de toilette")
add("136", "Thierry Mugler Angel Feminino 100ml EDP",550.80, "perf_import", "Thierry Mugler Angel pour femme eau de parfum 100ml")
add("1482","Versace Dylan Turquoise Fem 100ml",      450.90, "perf_import", "Versace Dylan Turquoise pour femme eau de parfum 100ml")
add("811", "Versace Pour Homme 100ml EDT",           370.80, "perf_import", "Versace Pour Homme 100ml eau de toilette", badge="Novo")

# --- Testers ---
add("1118","Tester Dolce & Gabbana Light Blue Fem 100ml", 305.10, "perf_tester", "Dolce Gabbana Light Blue pour femme eau de toilette 100ml", badge="Tester")

# --- Perfumes arabes ---
add("1821","Al Haramain Amber Oud Gold EDP 120ml",   330.30, "perf_arabe", "Al Haramain Amber Oud Gold Edition eau de parfum 120ml", badge="Novo")
add("2146","Al Wataniah Durrat Love EDP 100ml",      195.30, "perf_arabe", "Al Wataniah Durrat Al Aroos Love eau de parfum 100ml", badge="Novo")
add("1855","Al Wataniah Shagaf Al Ward EDP Fem 100ml",135.00,"perf_arabe", "Al Wataniah Shagaf Al Ward 100ml")
add("1676","Al Wataniah Sabah Al Ward EDP Fem 100ml",115.20, "perf_arabe", "Al Wataniah Sabah Al Ward eau de parfum 100ml", badge="Novo")
add("2193","Lattafa Afeef EDP 100ml",                390.60, "perf_arabe", "Lattafa Afeef eau de parfum 100ml", badge="Novo")
add("1937","Lattafa Asad Bourbon EDP 100ml",         190.80, "perf_arabe", "Lattafa Asad Bourbon 100ml eau de parfum")
add("2246","Lattafa Asad - Kit 4 x 25ml",            260.10, "perf_arabe", "Lattafa Asad discovery set 4 x 25ml", badge="Kit")
add("2245","Lattafa Dalal EDP 100ml",                280.80, "perf_arabe", "Lattafa Dalal eau de parfum 100ml", eq="lembra Lady Million", badge="Novo")
add("1962","Lattafa Yara - Kit 4 x 25ml",            215.10, "perf_arabe", "Lattafa Yara discovery set 4 x 25ml", badge="Kit")
add("1812","Lattafa Yara EDP 100ml (rosa)",          145.80, "perf_arabe", "Lattafa Yara 100ml eau de parfum pink")
add("1150","Al Haramain L'Aventure Men EDP 100ml",   240.30, "perf_arabe", "Al Haramain L'Aventure men eau de parfum 100ml")
add("1734","Al Wataniah Durrat Al Aroos EDP 85ml",   129.60, "perf_arabe", "Al Wataniah Durrat Al Aroos 85ml")
add("2219","Asdaaf Ameerat Al Arab Vermelho EDP 100ml",129.60, "perf_arabe", "Asdaaf Ameerat Al Arab red eau de parfum 100ml", badge="Novo")
add("2077","French Avenue Liquid Brun EDP 100ml",    260.10, "perf_arabe", "French Avenue Liquid Brun eau de parfum 100ml", badge="Novo")
add("2179","French Avenue Vulcan Feu EDP 100ml",     285.30, "perf_arabe", "French Avenue Vulcan Feu eau de parfum 100ml")
add("1794","Lattafa Asad Elixir Men EDP 100ml",      230.40, "perf_arabe", "Lattafa Asad Elixir 100ml eau de parfum", badge="Novo")
add("1756","Lattafa Asad Men EDP 100ml",             170.10, "perf_arabe", "Lattafa Asad 100ml eau de parfum")
add("2070","Lattafa Atheeri EDP 100ml",              350.10, "perf_arabe", "Lattafa Atheeri 100ml eau de parfum")
add("2237","Lattafa Confidential Gold EDP 100ml",    149.40, "perf_arabe", "Lattafa Confidential Gold eau de parfum 100ml", eq="insp. Tiziana Kirke")
add("1837","Lattafa Fakhar Black EDP 100ml",         170.10, "perf_arabe", "Lattafa Fakhar Black 100ml")
add("1870","Lattafa Fakhar Gold EDP 100ml",          160.20, "perf_arabe", "Lattafa Fakhar Gold men 100ml eau de parfum", badge="Novo")
add("1891","Lattafa Fakhar Fem EDP 100ml (rosa)",    210.60, "perf_arabe", "Lattafa Fakhar Lattafa for women 100ml rose")
add("1852","Lattafa Haya Fem EDP 100ml",             185.40, "perf_arabe", "Lattafa Haya 100ml eau de parfum", eq="insp. Prada Paradoxe", badge="Novo")
add("1929","Lattafa Musamman White EDP 100ml",       265.50, "perf_arabe", "Lattafa Musamman White eau de parfum 100ml")
add("1707","Lattafa Tharwah Gold EDP 100ml",         290.70, "perf_arabe", "Lattafa Tharwah Gold 100ml")
add("1586","Maison Alhambra Delilah EDP 100ml",      180.00, "perf_arabe", "Maison Alhambra Delilah pour femme eau de parfum 100ml", eq="insp. Delina")
add("2036","Maison Alhambra Athenas EDP 100ml",      200.70, "perf_arabe", "Maison Alhambra Athenas 100ml")
add("2005","Maison Alhambra Alpine Homme Sport EDP 100ml", 140.40, "perf_arabe", "Maison Alhambra Alpine Homme Sport 100ml", eq="insp. Allure Sport")
add("1964","Maison Alhambra Philos Pura EDP 100ml",  140.40, "perf_arabe", "Maison Alhambra Philos Pura 100ml eau de parfum", badge="Novo")
add("2006","Maison Maître de Blue EDP 100ml",        140.40, "perf_arabe", "Maison Alhambra Maitre de Blue eau de parfum 100ml", eq="insp. Bleu de Chanel", badge="Novo")
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
db("1322","055","Black Opium",45.90); db("1267","063","Armani Si",45.00)
db("1108","087","Olympéa",40.50)
db("1229","097","Euphoria Fem",45.00); db("1256","100","Sauvage",45.00); db("1318","102","212 NYC Men",45.00)
db("1293","105","Lady Million",45.00); db("1328","136","Scandal",43.20)
db("1547","151","Delina",45.00); db("1294","156","212 Sexy Men",45.00); db("1269","164","Armani Code Men",45.00)
db("1380","171","Jean Paul Classique Fem",45.00); db("1943","176","Issey Miyake Fem",45.00)
db("1414","181","Bad Boy",58.50); db("1446","214","Invictus Black",45.00); db("2097","225","Victoria Bombshell",45.00)
db("1419","238","Idôle",45.00); db("1423","240","212 NYC Fem",45.00); db("1451","265","Versace Dylan Fem",49.50)
db("1554","294","L'Interdit Rouge",45.00); db("2018","295","Ariana Grande Cloud",45.00); db("1503","296","Phantom",45.00)
db("2134","323","Le Male Elixir",45.00); db("1718","324","La Belle",40.50); db("2135","325","Le Male Le Parfum",45.00)
db("1605","347","212 Heroes Men",45.00); db("2242","348","Delina La Rosée",45.00)
db("1592","351","Dylan Turquoise",45.00)
db("1624","365","Fame",45.00); db("1973","367","Valaya",45.00); db("1848","370","Versace Purple",53.00)
db("1906","382","L'Interdit",45.00); db("1878","387","Azzaro Wanted Parfum",45.00); db("1974","391","Valentino Born in Roma",45.00)
db("1819","415","Fame Parfum (preto)",47.70); db("2063","435","Burberry Goddess",45.00)
db("1532","106","Versace Pour Homme",45.00)
db("1268","093","Light Blue Fem",45.00); db("1116","116","Invictus",45.00); db("1875","234","Petit et Mamans (infantil)",45.00)
db("1674","336","My Way Intense",45.00)

# --- Bases ---

# --- Hidratantes Victoria's Secret ---
add("1903","Body Lotion VS Bare Vanilla Shimmer",         110.70, "cosm_vs_lot", "Victoria's Secret Bare Vanilla Shimmer body lotion", badge="Novo")
add("1802","Body Lotion VS Velvet Petals Shimmer",        107.00, "cosm_vs_lot", "Victoria's Secret Velvet Petals Shimmer body lotion", badge="Novo")
add("898", "Body Lotion VS Aqua Kiss (emb. nova)",         105.30, "cosm_vs_lot", "Victoria's Secret Aqua Kiss body lotion", badge="Emb. nova")
add("95",  "Body Lotion VS Love Spell 236ml",              105.30, "cosm_vs_lot", "Victoria's Secret Love Spell body lotion")
add("1593","Body Lotion VS Velvet Petals 236ml",           105.30, "cosm_vs_lot", "Victoria's Secret Velvet Petals body lotion")
add("1621","Body Lotion VS Midnight Bloom",                105.30, "cosm_vs_lot", "Victoria's Secret Midnight Bloom body lotion", badge="Novo")
add("139", "Body Lotion VS Romantic 236ml (emb. nova)",    105.30, "cosm_vs_lot", "Victoria's Secret Romantic body lotion", badge="Emb. nova")

# --- Body Splash Victoria's Secret ---
add("977", "Body Splash VS Bare Vanilla",                  105.30, "cosm_vs_spl", "Victoria's Secret Bare Vanilla fragrance mist")
add("251", "Body Splash VS Bare Vanilla Shimmer",          110.70, "cosm_vs_spl", "Victoria's Secret Bare Vanilla Shimmer fragrance mist")
add("1518","Body Splash VS Velvet Petals",                 105.30, "cosm_vs_spl", "Victoria's Secret Velvet Petals fragrance mist", badge="Novo")
add("1803","Body Splash VS Velvet Petals Shimmer",         110.70, "cosm_vs_spl", "Victoria's Secret Velvet Petals Shimmer fragrance mist")
add("1376","Body Splash VS Coconut Passion Shimmer",       105.30, "cosm_vs_spl", "Victoria's Secret Coconut Passion Shimmer fragrance mist")
add("1622","Body Splash VS Midnight Bloom",                105.30, "cosm_vs_spl", "Victoria's Secret Midnight Bloom fragrance mist")
add("234", "Body Splash VS Love Spell",                    105.30, "cosm_vs_spl", "Victoria's Secret Love Spell fragrance mist")
add("252", "Body Splash VS Pure Seduction",                105.30, "cosm_vs_spl", "Victoria's Secret Pure Seduction fragrance mist")
add("859", "Body Splash VS Pure Seduction Shimmer",        105.30, "cosm_vs_spl", "Victoria's Secret Pure Seduction Shimmer fragrance mist", badge="Novo")
add("488", "Body Splash VS Rush",                          105.30, "cosm_vs_spl", "Victoria's Secret Rush fragrance mist")

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

# --- Corpo & Skincare ---
add("1103","St. Ives Creme Corporal Colágeno & Elastina 532ml", 45.00, "cosm_corpo", "St Ives Collagen Elastin body lotion 532ml")

# ============================================================================
# ACESSORIOS & BRINDES DE MARCA (fotos proprias em img/B##)
# ============================================================================
# --- Velas Perfumadas ---
add("B01","Vela Perfumada Marc Jacobs Perfect 70g",        90.00, "acess_vela", "vela", badge="Consultar")
add("B02","Vela Perfumada Burberry Goddess 70g",          100.00, "acess_vela", "vela", badge="Consultar")

# --- Geis & Hidratantes ---
add("B12","Gel de Banho Jo Malone 30ml",                   89.00, "acess_corpo", "gel", badge="Consultar")
add("B13","Gel de Banho Lancôme La Vie Est Belle 50ml",    79.00, "acess_corpo", "gel", badge="Consultar")
add("B14","Gel de Banho Montblanc Legend 100ml",           75.00, "acess_corpo", "gel", badge="Consultar")
add("B15","Gel de Banho JPG Le Male Elixir 75ml",          75.00, "acess_corpo", "gel", badge="Consultar")
add("B16","Hidratante JPG Scandal Elixir Fem 75ml",        89.00, "acess_corpo", "hidratante", badge="Consultar")
add("B17","Hidratante JPG Scandal Absolu 75ml",            89.00, "acess_corpo", "hidratante", badge="Consultar")
add("B18","Hidratante Coach Gold 100ml",                   89.00, "acess_corpo", "hidratante", badge="Consultar")
add("B19","Hidratante Lacoste L.12.12 Rose 100ml",         89.00, "acess_corpo", "hidratante", badge="Consultar")
add("B20","Hidratante Coach Dreams Moonlight 100ml",       89.00, "acess_corpo", "hidratante", badge="Consultar")
add("B21","Hidratante JPG Classique 75ml",                 89.00, "acess_corpo", "hidratante", badge="Consultar")
add("B22","Hidratante Montblanc Signature 100ml",          89.00, "acess_corpo", "hidratante", badge="Consultar")

# --- Necessaires & Bolsas ---
add("B03","Carteira Chloé (tam. M)",                       65.00, "acess_bolsa", "carteira", badge="Consultar")
add("B04","Porta Níquel Chloé (tam. P)",                   39.00, "acess_bolsa", "porta niquel", badge="Consultar")
add("B05","Necessaire Chloé (tam. M)",                     85.00, "acess_bolsa", "necessaire", badge="Consultar")
add("B06","Necessaire Armani (preta)",                     99.00, "acess_bolsa", "necessaire", badge="Consultar")
add("B07","Necessaire Carolina Herrera Cinza",             79.00, "acess_bolsa", "necessaire", badge="Consultar")
add("B08","Necessaire Carolina Herrera Pied de Poule",     85.00, "acess_bolsa", "necessaire", badge="Consultar")
add("B09","Bolsa Carolina Herrera",                        99.00, "acess_bolsa", "bolsa", badge="Consultar")
add("B10","Frasqueira Marc Jacobs",                        89.00, "acess_bolsa", "frasqueira", badge="Consultar")
add("B11","Bolsa Jean Paul Gaultier Vermelha (tam. M)",   110.00, "acess_bolsa", "bolsa", badge="Consultar")
add("B23","Necessaire Carolina Herrera Good Girl Rosa",   119.00, "acess_bolsa", "necessaire", badge="Consultar")

# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s

# categorias que compartilham a mesma foto de frasco (contratipos 25ml)
CAT_FALLBACK = {"contratipo": "DB", "arabic_insp": "DB"}

# produtos cuja foto e de outra versao/linha -> marca "Foto ilustrativa" no card
FOTO_ILUSTRATIVA = {"1903", "2146"}

# ----------------------------------------------------------------------------
# EM FALTA — arquivo historico: produtos que JA tivemos no catalogo, com o
# ULTIMO preco de referencia. PADRAO: ao desabilitar um produto, mova-o pra ca
# com o ultimo valor. (codigo, nome, ultimo_preco, categoria_original_p/_foto)
# Itens que voltarem a ficar ativos sao ignorados automaticamente (ver P_FALTA).
# ----------------------------------------------------------------------------
EM_FALTA = [
    ("1733","Al Wataniah Ameerati Fem EDP 100ml",125.10,"perf_arabe"),
    ("2107","Al Wataniah Sabah Sugar EDP 100ml",130.50,"perf_arabe"),
    ("905","Antonio Banderas The Secret Golden Men 200ml EDT",170.10,"perf_import"),
    ("1149","Armaf Club de Nuit Intense Men EDT 105ml",230.40,"perf_arabe"),
    ("1988","Armaf Club de Nuit Woman 100ml",220.50,"perf_arabe"),
    ("509","Base Milani Nº 03",79.20,"cosm_base"),
    ("1015","Body Lotion VS Bare Vanilla",110.70,"cosm_vs_lot"),
    ("99","Body Lotion VS Coconut Passion",105.30,"cosm_vs_lot"),
    ("96","Body Lotion VS Pure Seduction",105.30,"cosm_vs_lot"),
    ("250","Body Splash VS Amber Romance",105.30,"cosm_vs_spl"),
    ("786","Body Splash VS Aqua Kiss",105.30,"cosm_vs_spl"),
    ("380","Body Splash VS Coconut Passion",105.30,"cosm_vs_spl"),
    ("1016","Body Splash VS Romantic",105.30,"cosm_vs_spl"),
    ("1054","Body Splash VS Temptation",105.30,"cosm_vs_spl"),
    ("27","CH 212 VIP Rose 80ml EDP",470.70,"perf_import"),
    ("32","Chanel Allure Homme Sport 100ml EDT",740.70,"perf_import"),
    ("255","Chloé by Chloé 100ml EDP",540.90,"perf_import"),
    ("1266","Dream Brand 060 — Narciso For Her",45.00,"contratipo"),
    ("1107","Dream Brand 069 — La Nuit Trésor",45.00,"contratipo"),
    ("1228","Dream Brand 070 — Bleu de Chanel",40.50,"contratipo"),
    ("1112","Dream Brand 126 — Good Girl",58.50,"contratipo"),
    ("1270","Dream Brand 168 — Angel EDP",45.00,"contratipo"),
    ("2126","Dream Brand 303 — Devotion D&G",45.00,"contratipo"),
    ("1604","Dream Brand 340 — 212 Heroes Fem",45.90,"contratipo"),
    ("2159","Dream Brand 356 — J'adore L'Or",45.00,"contratipo"),
    ("1639","Dream Brand 361 — Libre Intense",45.00,"contratipo"),
    ("2127","Dream Brand 445 — Prada Paradoxe",45.00,"contratipo"),
    ("2037","Hawas Black EDP 100ml (Rasasi)",205.20,"perf_arabe"),
    ("527","Jean Paul Gaultier Scandal Fem 80ml EDP",495.90,"perf_import"),
    ("1019","Joico Color Therapy Máscara 500g",240.30,"cosm_cabelo"),
    ("851","Joico Moisture Recovery Combo Shampoo + Cond. 1L",266.40,"cosm_cabelo"),
    ("196","Joico Moisture Recovery Máscara 500ml",144.00,"cosm_cabelo"),
    ("2197","Lattafa Queen of Arabia EDP 100ml",330.30,"perf_arabe"),
    ("1991","Maison Alhambra Delilah Blanc EDP 100ml",190.80,"perf_arabe"),
    ("1892","Maison Alhambra Leonie Fem EDP 100ml",155.70,"perf_arabe"),
    ("2235","Maison Alhambra Papillon D'Or EDP 100ml",255.60,"perf_arabe"),
    ("2114","Maison Alhambra Perseus Exclusif EDP 100ml",130.50,"perf_arabe"),
    ("1890","Maison Alhambra Salvo Men EDP 100ml",135.00,"perf_arabe"),
    ("1635","Paco Rabanne Invictus Victory Elixir Parfum Intense 100ml",490.50,"perf_import"),
    ("112","Revlon Uniq One Leave-in (vermelho) trad.",69.30,"cosm_cabelo"),
    ("133","Thierry Mugler Angel Body Lotion 200ml",370.80,"cosm_corpo"),
    ("177","UDV For Men Black 100ml EDT",85.50,"perf_import"),
]

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
# FICHAS DOS PERFUMES  (detalhes exibidos no lightbox pelo botao "Detalhes")
#   genero      : "Masculino" | "Feminino" | "Unissex"
#   fragancia   : 1-3 de  Doce, Frutado, Floral, Cítrico, Fresco, Especiado,
#                         Amadeirado, Oriental/Âmbar, Aromático, Almiscarado
#   intensidade : "Leve" | "Médio" | "Marcante"
#   ideal       : 1-3 de  Dia a dia, Trabalho, Noite, Datas especiais
#   publico     : 1-2 de  Jovens, Adultos, Maduros, Versátil
# Contratipos/arabes "inspirados" herdam a ficha do original pelo eq= (ver FICHAS_REF).
# ----------------------------------------------------------------------------
def ficha(genero, fragancia, intensidade, ideal, publico):
    return dict(genero=genero, fragancia=fragancia, intensidade=intensidade,
                ideal=ideal, publico=publico)

# categorias que exibem ficha (so perfumes; cosmeticos ficam sem)
PERF_CATS = {"perf_import", "perf_arabe", "perf_tester", "arabic_insp", "contratipo", "promo"}

# fichas nomeadas (reaproveitadas por codigo direto E como referencia p/ clones)
_f_coco   = ficha("Feminino",  ["Floral","Cítrico","Amadeirado"], "Marcante", ["Dia a dia","Trabalho","Datas especiais"], ["Jovens","Adultos"])
_f_lvb    = ficha("Feminino",  ["Doce","Floral","Frutado"],       "Marcante", ["Dia a dia","Datas especiais"],            ["Jovens","Adultos"])
_f_lady   = ficha("Feminino",  ["Doce","Floral","Frutado"],       "Marcante", ["Noite","Datas especiais"],                ["Jovens","Adultos"])
_f_scandal= ficha("Feminino",  ["Doce","Floral"],                 "Marcante", ["Noite","Datas especiais"],                ["Jovens","Adultos"])
_f_vph    = ficha("Masculino", ["Cítrico","Aromático","Amadeirado"], "Médio", ["Dia a dia","Trabalho"],                   ["Versátil"])
_f_delina = ficha("Feminino",  ["Floral","Frutado","Almiscarado"],"Médio",    ["Dia a dia","Datas especiais"],            ["Jovens","Adultos"])
_f_bleu   = ficha("Masculino", ["Amadeirado","Aromático","Cítrico"],"Médio",  ["Dia a dia","Trabalho","Noite"],           ["Adultos","Maduros"])

# fichas por CODIGO (perfumes reais do catalogo)
FICHAS = {
    "38":   _f_coco,
    "32":   ficha("Masculino", ["Cítrico","Amadeirado","Aromático"], "Médio",   ["Dia a dia","Trabalho"],          ["Jovens","Adultos"]),
    "44":   ficha("Feminino",  ["Floral","Frutado"],                 "Médio",   ["Dia a dia","Trabalho","Datas especiais"], ["Adultos","Maduros"]),
    "132":  _f_lvb,
    "80":   ficha("Masculino", ["Fresco","Cítrico","Amadeirado"],    "Médio",   ["Dia a dia","Trabalho"],          ["Jovens"]),
    "78":   _f_lady,
    "527":  _f_scandal,
    "811":  _f_vph,
    "1756": ficha("Masculino", ["Especiado","Doce","Amadeirado"],    "Marcante",["Noite","Datas especiais"],       ["Jovens","Adultos"]),
    "1586": _f_delina,
    "1149": ficha("Masculino", ["Frutado","Amadeirado","Cítrico"],   "Marcante",["Dia a dia","Noite"],             ["Jovens","Adultos"]),
    "2006": _f_bleu,
}

# fichas por REFERENCIA/INSPIRACAO (clones herdam via eq="insp. <ref>")
FICHAS_REF = {
    "coco mademoiselle":  _f_coco,
    "la vie est belle":   _f_lvb,
    "lady million":       _f_lady,
    "scandal":            _f_scandal,
    "versace pour homme": _f_vph,
    "delina":             _f_delina,
    "bleu de chanel":     _f_bleu,
    "one million":  ficha("Masculino", ["Especiado","Doce","Amadeirado"], "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "olympea":      ficha("Feminino",  ["Doce","Floral","Oriental/Âmbar"], "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "good girl":    ficha("Feminino",  ["Doce","Floral","Amadeirado"],     "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "sauvage":      ficha("Masculino", ["Fresco","Especiado","Amadeirado"],"Marcante", ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "212 vip men":  ficha("Masculino", ["Especiado","Amadeirado"],         "Médio",    ["Noite","Datas especiais"], ["Jovens"]),
    "bad boy":      ficha("Masculino", ["Especiado","Amadeirado","Doce"],  "Médio",    ["Dia a dia","Noite"],       ["Jovens"]),
    "prada paradoxe": ficha("Feminino",["Floral","Oriental/Âmbar"],        "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
}

# ---- Preenchimento em massa (referencias p/ os contratipos/arabes inspirados) ----
FICHAS_REF.update({
    "212 vip fem":      ficha("Feminino",  ["Doce","Floral","Frutado"],          "Marcante", ["Noite","Datas especiais"], ["Jovens"]),
    "vip rose":         ficha("Feminino",  ["Floral","Frutado","Doce"],          "Médio",    ["Dia a dia","Noite"],       ["Jovens"]),
    "212 nyc men":      ficha("Masculino", ["Amadeirado","Aromático","Especiado"],"Médio",   ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "212 nyc fem":      ficha("Feminino",  ["Floral","Amadeirado"],              "Médio",    ["Dia a dia","Noite"],       ["Adultos"]),
    "212 sexy men":     ficha("Masculino", ["Especiado","Amadeirado","Doce"],    "Médio",    ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "212 heroes men":   ficha("Masculino", ["Fresco","Aromático","Amadeirado"],  "Médio",    ["Dia a dia","Trabalho"],    ["Jovens"]),
    "miss dior blooming":ficha("Feminino", ["Floral","Frutado","Cítrico"],       "Leve",     ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "miss dior":        ficha("Feminino",  ["Floral","Frutado"],                 "Médio",    ["Dia a dia","Datas especiais"], ["Adultos"]),
    "decadence":        ficha("Feminino",  ["Amadeirado","Floral","Oriental/Âmbar"],"Marcante",["Noite","Datas especiais"],["Adultos"]),
    "hypnotic poison":  ficha("Feminino",  ["Doce","Amadeirado","Oriental/Âmbar"],"Marcante", ["Noite","Datas especiais"], ["Adultos","Maduros"]),
    "chanel chance":    ficha("Feminino",  ["Floral","Cítrico","Amadeirado"],    "Médio",    ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "alien":            ficha("Feminino",  ["Floral","Oriental/Âmbar","Amadeirado"],"Marcante",["Noite","Datas especiais"],["Adultos","Maduros"]),
    "black opium":      ficha("Feminino",  ["Doce","Especiado","Amadeirado"],    "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "narciso for her":  ficha("Feminino",  ["Almiscarado","Floral","Amadeirado"],"Médio",    ["Dia a dia","Noite"],       ["Adultos"]),
    "armani si":        ficha("Feminino",  ["Frutado","Floral","Amadeirado"],    "Marcante", ["Noite","Datas especiais"], ["Adultos"]),
    "la nuit tresor":   ficha("Feminino",  ["Doce","Floral","Oriental/Âmbar"],   "Marcante", ["Noite","Datas especiais"], ["Adultos"]),
    "euphoria fem":     ficha("Feminino",  ["Frutado","Oriental/Âmbar","Amadeirado"],"Marcante",["Noite","Datas especiais"],["Adultos"]),
    "armani code men":  ficha("Masculino", ["Aromático","Amadeirado","Doce"],    "Médio",    ["Noite","Datas especiais"], ["Adultos"]),
    "jean paul classique fem": ficha("Feminino",["Floral","Oriental/Âmbar","Doce"],"Marcante",["Noite","Datas especiais"],["Adultos","Maduros"]),
    "issey miyake fem": ficha("Feminino",  ["Floral","Fresco","Cítrico"],        "Leve",     ["Dia a dia","Trabalho"],    ["Adultos"]),
    "invictus":         ficha("Masculino", ["Fresco","Cítrico","Amadeirado"],    "Médio",    ["Dia a dia","Trabalho"],    ["Jovens"]),
    "invictus black":   ficha("Masculino", ["Amadeirado","Especiado","Fresco"],  "Marcante", ["Noite","Datas especiais"], ["Jovens"]),
    "victoria bombshell":ficha("Feminino", ["Frutado","Floral"],                 "Médio",    ["Dia a dia","Noite"],       ["Jovens"]),
    "idole":            ficha("Feminino",  ["Floral","Almiscarado","Cítrico"],   "Médio",    ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "versace dylan fem":ficha("Feminino",  ["Frutado","Floral","Almiscarado"],   "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "dylan turquoise":  ficha("Feminino",  ["Cítrico","Frutado","Fresco"],       "Leve",     ["Dia a dia","Trabalho"],    ["Jovens"]),
    "versace purple":   ficha("Feminino",  ["Floral","Frutado"],                 "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "l interdit rouge": ficha("Feminino",  ["Especiado","Floral","Amadeirado"],  "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "l interdit":       ficha("Feminino",  ["Floral","Amadeirado"],              "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "ariana grande cloud": ficha("Feminino",["Doce","Frutado","Amadeirado"],     "Médio",    ["Dia a dia","Noite"],       ["Jovens"]),
    "phantom":          ficha("Masculino", ["Fresco","Cítrico","Aromático"],     "Médio",    ["Dia a dia","Trabalho"],    ["Jovens"]),
    "le male elixir":   ficha("Masculino", ["Doce","Especiado","Oriental/Âmbar"],"Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "le male le parfum":ficha("Masculino", ["Oriental/Âmbar","Especiado","Doce"],"Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "la belle":         ficha("Feminino",  ["Doce","Amadeirado"],                "Marcante", ["Noite","Datas especiais"], ["Jovens"]),
    "j adore l or":     ficha("Feminino",  ["Floral","Doce"],                    "Marcante", ["Noite","Datas especiais"], ["Adultos","Maduros"]),
    "libre":            ficha("Feminino",  ["Floral","Aromático","Oriental/Âmbar"],"Marcante",["Noite","Datas especiais"],["Jovens","Adultos"]),
    "libre intense":    ficha("Feminino",  ["Floral","Aromático","Oriental/Âmbar"],"Marcante",["Noite","Datas especiais"],["Jovens","Adultos"]),
    "fame":             ficha("Feminino",  ["Floral","Frutado","Amadeirado"],    "Médio",    ["Dia a dia","Noite"],       ["Jovens"]),
    "fame parfum preto":ficha("Feminino",  ["Floral","Doce","Amadeirado"],       "Marcante", ["Noite","Datas especiais"], ["Jovens"]),
    "valaya":           ficha("Feminino",  ["Almiscarado","Floral","Frutado"],   "Médio",    ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "azzaro wanted parfum": ficha("Masculino",["Especiado","Amadeirado","Doce"], "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "valentino born in roma": ficha("Feminino",["Floral","Amadeirado","Doce"],   "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "burberry goddess": ficha("Feminino",  ["Doce","Aromático","Amadeirado"],    "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "light blue fem":   ficha("Feminino",  ["Cítrico","Frutado","Fresco"],       "Leve",     ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "petit et mamans":  ficha("Unissex",   ["Cítrico","Floral","Fresco"],        "Leve",     ["Dia a dia"],               ["Jovens"]),
    "devotion":         ficha("Feminino",  ["Doce","Cítrico","Amadeirado"],      "Marcante", ["Noite","Datas especiais"], ["Jovens"]),
    "my way":           ficha("Feminino",  ["Floral","Almiscarado","Doce"],      "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "ch la bomba":      ficha("Feminino",  ["Doce","Frutado","Floral"],          "Marcante", ["Noite","Datas especiais"], ["Jovens"]),
    "allure sport":     ficha("Masculino", ["Cítrico","Amadeirado","Aromático"], "Médio",    ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "sabah":            ficha("Feminino",  ["Frutado","Floral","Doce"],          "Médio",    ["Dia a dia","Noite"],       ["Jovens"]),
    "fakhar rose":      ficha("Feminino",  ["Floral","Frutado","Doce"],          "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "tharwad gold":     ficha("Feminino",  ["Floral","Doce","Aromático"],        "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "yara rosa":        ficha("Feminino",  ["Doce","Floral","Amadeirado"],       "Marcante", ["Dia a dia","Noite"],       ["Jovens"]),
})

# ---- Perfumes diretos (sem eq de inspiracao) ----
FICHAS.update({
    # importados
    "2103": FICHAS_REF["ch la bomba"],
    "23":   FICHAS_REF["212 sexy men"],
    "26":   FICHAS_REF["212 vip fem"],
    "717":  ficha("Masculino", ["Especiado","Amadeirado","Oriental/Âmbar"], "Marcante", ["Noite","Datas especiais"], ["Jovens"]),
    "24":   ficha("Masculino", ["Especiado","Amadeirado"],                  "Médio",    ["Noite","Datas especiais"], ["Jovens"]),
    "27":   FICHAS_REF["vip rose"],
    "20":   FICHAS_REF["euphoria fem"],
    "21":   ficha("Masculino", ["Amadeirado","Especiado"],                  "Marcante", ["Noite","Datas especiais"], ["Adultos"]),
    "1989": ficha("Masculino", ["Cítrico","Aromático","Amadeirado"],        "Médio",    ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "68":   ficha("Masculino", ["Doce","Especiado","Oriental/Âmbar"],       "Marcante", ["Noite","Datas especiais"], ["Adultos","Maduros"]),
    "70":   ficha("Feminino",  ["Frutado","Floral"],                        "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "567":  ficha("Feminino",  ["Floral","Frutado","Almiscarado"],          "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "113":  FICHAS_REF["olympea"],
    "233":  ficha("Masculino", ["Aromático","Amadeirado","Fresco"],         "Marcante", ["Noite","Trabalho"],        ["Jovens","Adultos"]),
    "127":  ficha("Masculino", ["Aromático","Cítrico","Amadeirado"],        "Médio",    ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "136":  ficha("Feminino",  ["Doce","Amadeirado","Oriental/Âmbar"],      "Marcante", ["Noite","Datas especiais"], ["Adultos","Maduros"]),
    "1482": FICHAS_REF["dylan turquoise"],
    # arabes
    "1150": ficha("Masculino", ["Cítrico","Amadeirado","Frutado"],          "Marcante", ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "1734": ficha("Feminino",  ["Especiado","Oriental/Âmbar","Doce"],       "Marcante", ["Noite","Datas especiais"], ["Adultos"]),
    "2107": FICHAS_REF["sabah"],
    "1988": ficha("Feminino",  ["Frutado","Floral","Amadeirado"],           "Marcante", ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "2219": ficha("Feminino",  ["Frutado","Floral","Doce"],                 "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "2077": ficha("Masculino", ["Especiado","Doce","Amadeirado"],           "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "2179": ficha("Unissex",   ["Frutado","Doce","Amadeirado"],             "Médio",    ["Dia a dia","Noite"],       ["Jovens"]),
    "1794": ficha("Masculino", ["Especiado","Doce","Amadeirado"],           "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "2070": ficha("Feminino",  ["Floral","Doce","Fresco"],                  "Médio",    ["Dia a dia","Noite"],       ["Jovens"]),
    "2237": ficha("Unissex",   ["Frutado","Doce","Almiscarado"],            "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "1837": ficha("Masculino", ["Aromático","Amadeirado","Frutado"],        "Marcante", ["Noite","Trabalho"],        ["Jovens","Adultos"]),
    "1870": ficha("Unissex",   ["Doce","Amadeirado","Oriental/Âmbar"],      "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "1891": FICHAS_REF["fakhar rose"],
    "1929": ficha("Unissex",   ["Floral","Amadeirado","Especiado"],         "Médio",    ["Dia a dia","Noite"],       ["Adultos"]),
    "1707": FICHAS_REF["tharwad gold"],
    "1991": ficha("Feminino",  ["Floral","Almiscarado","Frutado"],          "Médio",    ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "2036": ficha("Feminino",  ["Floral","Amadeirado","Doce"],              "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "1964": ficha("Masculino", ["Fresco","Aromático","Amadeirado"],         "Médio",    ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "1651": ficha("Feminino",  ["Floral","Doce"],                           "Marcante", ["Noite","Datas especiais"], ["Adultos"]),
    "1650": ficha("Unissex",   ["Doce","Oriental/Âmbar","Frutado"],         "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "2236": ficha("Unissex",   ["Floral","Fresco","Doce"],                  "Leve",     ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    # promocao da copa
    "CP1":  ficha("Masculino", ["Aromático","Amadeirado","Fresco"],         "Médio",    ["Dia a dia","Noite"],       ["Jovens"]),
    "CP2":  ficha("Masculino", ["Especiado","Doce","Amadeirado"],           "Marcante", ["Noite","Datas especiais"], ["Jovens"]),
    "CP3":  ficha("Masculino", ["Fresco","Especiado","Amadeirado"],         "Médio",    ["Dia a dia","Noite"],       ["Jovens"]),
    "CP4":  ficha("Masculino", ["Especiado","Amadeirado","Doce"],           "Médio",    ["Noite","Datas especiais"], ["Jovens"]),
    "CP5":  ficha("Feminino",  ["Doce","Floral"],                           "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "CP6":  ficha("Feminino",  ["Doce","Floral","Amadeirado"],              "Médio",    ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "CP7":  FICHAS_REF["good girl"],
    "CP8":  FICHAS_REF["one million"],
    "CP9":  FICHAS_REF["armani si"],
    "CP10": ficha("Feminino",  ["Doce","Floral","Amadeirado"],              "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
})

# ---- Fichas dos itens da tabela 13-07 (novos + reentradas) ----
FICHAS.update({
    "142":  ficha("Masculino", ["Especiado","Amadeirado","Oriental/Âmbar"], "Marcante", ["Noite","Datas especiais"], ["Adultos","Maduros"]),
    "2":    ficha("Masculino", ["Aromático","Amadeirado","Cítrico"],        "Marcante", ["Noite","Trabalho"],        ["Adultos","Maduros"]),
    "22":   FICHAS_REF["212 nyc men"],
    "48":   FICHAS_REF["light blue fem"],
    "52":   ficha("Masculino", ["Aromático","Amadeirado","Cítrico"],        "Médio",    ["Dia a dia","Trabalho"],    ["Jovens","Adultos"]),
    "248":  ficha("Feminino",  ["Floral","Amadeirado"],                     "Médio",    ["Dia a dia","Noite"],       ["Adultos","Maduros"]),
    "74":   FICHAS_REF["one million"],
    "674":  ficha("Masculino", ["Aromático","Cítrico","Amadeirado"],        "Médio",    ["Dia a dia","Trabalho"],    ["Jovens"]),
    "1118": FICHAS_REF["light blue fem"],
    "1821": ficha("Unissex",   ["Doce","Oriental/Âmbar","Amadeirado"],      "Marcante", ["Noite","Datas especiais"], ["Adultos"]),
    "2146": ficha("Feminino",  ["Especiado","Oriental/Âmbar","Doce"],       "Marcante", ["Noite","Datas especiais"], ["Adultos"]),
    "1855": ficha("Feminino",  ["Floral","Amadeirado","Doce"],              "Médio",    ["Dia a dia","Noite"],       ["Adultos"]),
    "1676": FICHAS_REF["sabah"],
    "2193": ficha("Unissex",   ["Frutado","Floral","Doce"],                 "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "1937": ficha("Masculino", ["Especiado","Doce","Amadeirado"],          "Marcante", ["Noite","Datas especiais"], ["Jovens","Adultos"]),
    "2246": FICHAS["1756"],
    "2245": ficha("Feminino",  ["Frutado","Floral","Doce"],                 "Marcante", ["Dia a dia","Noite"],       ["Jovens","Adultos"]),
    "1962": FICHAS_REF["yara rosa"],
    "1812": FICHAS_REF["yara rosa"],
})

def _norm(s):
    s = (s or "").lower().replace("insp.", " ").replace("mesmo cheiro do tradicional", " ")
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = "".join(ch if (ch.isalnum() or ch == " ") else " " for ch in s)
    return " ".join(s.split())

def detalhe(p):
    """Retorna a ficha do produto (direta por codigo ou herdada por inspiracao), ou None."""
    if p["cat"] not in PERF_CATS:
        return None
    if p["cod"] in FICHAS:
        return FICHAS[p["cod"]]
    if p["eq"]:
        ref = _norm(p["eq"])
        if ref in FICHAS_REF:
            return FICHAS_REF[ref]
        for k, v in FICHAS_REF.items():   # match parcial (eq pode ter texto extra)
            if k in ref:
                return v
    return None

# ----------------------------------------------------------------------------
# RENDER
# ----------------------------------------------------------------------------
total = len(P)
com_foto = sum(1 for p in P if img_data(p["cod"], p["cat"]))
menor = min(p["preco"] for p in P)

# mapa codigo -> ficha (so quem tem), enviado ao JS p/ montar o cartao "Detalhes"
det_map = {}
for p in P:
    d = detalhe(p)
    if d:
        det_map[p["cod"]] = {"g": d["genero"], "fr": d["fragancia"],
                             "in": d["intensidade"], "id": d["ideal"], "pu": d["publico"]}
det_json = json.dumps(det_map, ensure_ascii=False)
com_ficha = len(det_map)

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

def is_promo(p):
    return p["de"] and p["de"] > p["preco"]

def price_html(p):
    if is_promo(p):
        return (f'<span class="precobox"><span class="preco-de">{brl(p["de"])}</span>'
                f'<span class="preco preco-promo">{brl(p["preco"])}</span></span>')
    return f'<span class="preco">{brl(p["preco"])}</span>'

def card_html(p):
    src = img_data(p["cod"], p["cat"])
    if src:
        media = f'<img loading="lazy" decoding="async" src="{src}" alt="{esc(p["nome"])}">'
    else:
        ini = esc(p["nome"][:1].upper())
        media = f'<div class="ph"><span>{ini}</span></div>'
    if is_promo(p):
        pct = round((1 - p["preco"] / p["de"]) * 100)
        badge = f'<span class="badge badge-off">-{pct}%</span>'
    elif p["badge"]:
        badge = f'<span class="badge">{esc(p["badge"])}</span>'
    else:
        badge = ""
    ilustr = '<span class="ilustr"><i class="ti ti-photo"></i> Ilustrativa</span>' if p["cod"] in FOTO_ILUSTRATIVA else ""
    cls = "card promo" if is_promo(p) else "card"
    eq = f'<p class="eq">{esc(p["eq"])}</p>' if p["eq"] else ""
    return f'''<article class="{cls}" {data_attrs(p)}>
      <div class="media">{media}{badge}{ilustr}</div>
      <div class="info">
        <p class="nome">{esc(p['nome'])}</p>{eq}
        <div class="row"><span class="cod">#{esc(p['cod'])}</span>{price_html(p)}</div>
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
      <span class="lpreco">{price_html(p)}</span>
      {add_ctrl(True)}
    </div>'''

def emfalta_html(p):
    if p["src"]:
        media = f'<img loading="lazy" decoding="async" src="{p["src"]}" alt="{esc(p["nome"])}">'
    else:
        media = f'<div class="ph"><span>{esc(p["nome"][:1].upper())}</span></div>'
    dn = esc(p["nome"].lower()) + " " + esc(p["cod"])
    return f'''<article class="card offcard" data-n="{dn}">
      <div class="offmedia">{media}<span class="offtag"><i class="ti ti-ban"></i> Em falta</span></div>
      <div class="info">
        <p class="nome">{esc(p["nome"])}</p>
        <div class="row"><span class="cod">#{esc(p["cod"])}</span><span class="preco-old">últ. {brl(p["preco"])}</span></div>
      </div>
    </article>'''

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
    nota = ('<p class="sec-note"><i class="ti ti-clock-hour-4"></i>Estoque limitado — aproveite enquanto durar!</p>'
            if key == "promo" else "")
    secoes.append(f'''<section id="{key}">
      <h2 class="sec-h"><i class="ti {icon}"></i>{esc(titulo)}<span class="qt">{len(itens)} itens</span><i class="ti ti-chevron-down chev"></i></h2>
      {nota}
      <div class="sec-body">{corpo}</div>
    </section>''')

# --- Em Falta (arquivo historico: ultimo preco de referencia) ---
_ativos = {p["cod"] for p in P}
P_FALTA = [dict(cod=c, nome=n, preco=pr, src=img_data(c, cat0))
           for (c, n, pr, cat0) in EM_FALTA if c not in _ativos]
if P_FALTA:
    corpo_f = '<div class="grid">' + "".join(emfalta_html(p) for p in P_FALTA) + '</div>'
    nav.append(f'<a href="#emfalta"><i class="ti ti-ban"></i>Em Falta <b>{len(P_FALTA)}</b></a>')
    secoes.append(f'''<section id="emfalta" class="sec-falta collapsed">
      <h2 class="sec-h"><i class="ti ti-ban"></i>Em Falta<span class="qt">{len(P_FALTA)} itens</span><i class="ti ti-chevron-down chev"></i></h2>
      <p class="sec-note"><i class="ti ti-info-circle"></i>Produtos que já tivemos — referência de último preço. Indisponíveis no momento.</p>
      <div class="sec-body">{corpo_f}</div>
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
.ilustr{{position:absolute;bottom:6px;left:6px;background:rgba(0,0,0,.5);color:#fff;font-size:9px;padding:2px 6px;border-radius:6px;display:inline-flex;align-items:center;gap:3px;line-height:1.3;letter-spacing:.2px}}
.ilustr i{{font-size:10px}}
/* categoria Em Falta (arquivo historico, foto p&b) */
.offcard{{opacity:.94}}
.offmedia{{position:relative;height:150px;background:#fff;padding:12px;border-bottom:1px solid var(--line)}}
.offmedia img{{filter:grayscale(1);opacity:.68}}
.offtag{{position:absolute;top:8px;left:8px;background:rgba(0,0,0,.62);color:#fff;font-size:10px;padding:2px 8px;border-radius:6px;display:inline-flex;align-items:center;gap:4px;letter-spacing:.3px}}
.offtag i{{font-size:11px}}
.preco-old{{color:var(--mut);font-size:13px;font-weight:600}}
.sec-falta .sec-h,.sec-falta .sec-h i,.sec-falta .sec-note,.sec-falta .sec-note i{{color:var(--mut)}}
.nav a[href="#emfalta"]{{color:var(--mut)}}
.ph{{display:flex;align-items:center;justify-content:center;height:100%;background:linear-gradient(135deg,#f7e9ee,#fbf3f6);border-radius:10px}}
.ph span{{font-family:Georgia,serif;font-size:40px;color:var(--rose);opacity:.55}}
.badge{{position:absolute;top:8px;left:8px;background:var(--gold);color:#3a2a05;font-size:10px;font-weight:700;letter-spacing:.4px;padding:3px 9px;border-radius:20px;text-transform:uppercase}}
.info{{padding:11px 12px 13px;display:flex;flex-direction:column;gap:5px;flex:1}}
.nome{{font-size:13.5px;font-weight:600;line-height:1.25;min-height:34px}}
.eq{{font-size:11.5px;color:var(--rose);font-style:italic}}
.row{{display:flex;align-items:baseline;justify-content:space-between;margin-top:auto;gap:6px}}
.cod{{font-size:11px;color:var(--mut)}}
.preco{{font-family:Georgia,serif;font-size:18px;font-weight:700;color:var(--wine)}}
/* PROMOCAO DA COPA */
.sec-note{{display:flex;align-items:center;gap:6px;font-size:12.5px;color:#d0341b;font-weight:600;margin-top:8px}}
.sec-note i{{font-size:15px}}
#promo h2{{color:#0b6b35;border-bottom-color:#d8edcf}}
#promo h2 i{{color:#0b8a3e}}
#promo .card{{border:2px solid var(--gold);background:linear-gradient(180deg,#fffdf5,#fff);box-shadow:0 4px 14px rgba(199,154,62,.22)}}
#promo .card:hover{{box-shadow:0 10px 24px rgba(199,154,62,.32)}}
.precobox{{display:inline-flex;flex-direction:column;align-items:flex-end;line-height:1.05}}
.preco-de{{font-family:'Segoe UI',sans-serif;font-size:12px;color:var(--mut);text-decoration:line-through}}
.preco-promo{{color:#0b8a3e}}
.badge-off{{background:#e0322a;color:#fff;font-size:11px}}
.nav a[href="#promo"]{{background:linear-gradient(135deg,#fff6e0,#ffe6bd);border-color:var(--gold);color:#8a5a00;font-weight:700}}
.nav a[href="#promo"] i{{color:#d68a00}}
.nav a[href="#promo"] b{{background:#ffe1b0;color:#8a5a00}}
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

/* LIGHTBOX (toque na foto -> tela cheia + zoom estilo galeria) */
.media img,.lthumb img{{cursor:zoom-in}}
.lb{{position:fixed;inset:0;z-index:200;background:rgba(16,6,11,.96);display:none;align-items:center;justify-content:center;overflow:hidden;touch-action:none;-webkit-user-select:none;user-select:none}}
.lb.open{{display:flex}}
.lb img{{max-width:100vw;max-height:100vh;width:auto;height:auto;object-fit:contain;transform-origin:0 0;-webkit-user-drag:none}}
.lb.zoomed img{{cursor:grab}}
.lb-x{{position:absolute;top:14px;right:16px;z-index:6;width:44px;height:44px;border:0;border-radius:50%;background:rgba(0,0,0,.45);color:#fff;font-size:24px;line-height:1;display:flex;align-items:center;justify-content:center;cursor:pointer}}
.lb-hint{{position:absolute;bottom:18px;left:0;right:0;text-align:center;color:rgba(255,255,255,.65);font-size:12px;pointer-events:none;transition:opacity .4s}}
.lb.zoomed .lb-hint{{opacity:0}}
/* cartao de detalhes do perfume */
.lb-det{{position:absolute;bottom:16px;left:50%;transform:translateX(-50%);z-index:4;border:1px solid var(--gold);border-radius:999px;background:rgba(0,0,0,.4);color:#fff;font-size:14px;padding:9px 18px;display:none;align-items:center;gap:7px;cursor:pointer;white-space:nowrap}}
.lb.has-ficha .lb-det{{display:flex}}
.lb.zoomed .lb-det{{opacity:0;pointer-events:none}}
.lb-dots{{position:absolute;bottom:60px;left:0;right:0;display:none;justify-content:center;gap:7px;z-index:4}}
.lb.has-ficha:not(.zoomed) .lb-dots{{display:flex}}
.lb-dots span{{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.35)}}
.lb-dots span.on{{background:#fff}}
.lb-card{{position:absolute;inset:0;padding:64px 16px 88px;display:none;overflow:auto;z-index:3}}
.lb.showcard .lb-card{{display:block}}
.lb.showcard img{{visibility:hidden}}
.lb.showcard .lb-hint{{opacity:0}}
.fcard{{background:#fff;border-radius:14px;padding:18px 16px;max-width:360px;margin:0 auto}}
.fcard h3{{font-family:Georgia,serif;font-size:19px;color:var(--ink);margin:0 0 2px;font-weight:600;line-height:1.25}}
.fcard .fsub{{font-size:12px;color:var(--mut);margin:0 0 14px}}
.ffld{{display:flex;flex-direction:column;gap:6px;margin-bottom:13px}}
.ffld:last-child{{margin-bottom:0}}
.flbl{{font-size:12px;color:#a06a2a;font-weight:600;display:flex;align-items:center;gap:6px}}
.flbl i{{font-size:15px}}
.fchips{{display:flex;flex-wrap:wrap;gap:6px}}
.fchips span{{font-size:13px;background:var(--rose-l);color:var(--wine);padding:4px 11px;border-radius:999px}}
.fchips span.cg{{background:var(--wine);color:#fff}}
.fchips span.ci{{background:#f3e3bf;color:#8a5a00}}
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

<div class="lb" id="lb">
  <button class="lb-x" id="lbX" type="button" aria-label="Fechar">&times;</button>
  <img id="lbImg" src="" alt="" draggable="false">
  <div class="lb-card" id="lbCard"></div>
  <div class="lb-hint">Pinça ou toque duplo para dar zoom</div>
  <div class="lb-dots"><span id="lbDot0" class="on"></span><span id="lbDot1"></span></div>
  <button class="lb-det" id="lbDet" type="button"><i class="ti ti-info-circle"></i> Detalhes</button>
</div>

<script>
const WA="{WHATSAPP}", MARCA_PED="{MARCA}";
const DET={det_json};
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

/* LIGHTBOX estilo galeria: toque na foto abre; pinca/toque-duplo da zoom (centrado),
   arrasta com limites; fecha SO no X. */
const lb=document.getElementById('lb'),lbImg=document.getElementById('lbImg'),lbX=document.getElementById('lbX');
const lbCard=document.getElementById('lbCard'),lbDet=document.getElementById('lbDet');
const lbDot0=document.getElementById('lbDot0'),lbDot1=document.getElementById('lbDot1');
const MINS=1,MAXS=4,DTS=2.6;
let s=1,tx=0,ty=0,base=null,curCod=null;
const FLAB={{g:'Gênero',fr:'Fragância',in:'Intensidade',id:'Ideal para',pu:'Público'}};
const FICO={{g:'ti-venus',fr:'ti-flask',in:'ti-flame',id:'ti-clock-hour-3',pu:'ti-users'}};
function esc2(t){{return String(t).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));}}
function chips(arr,cls){{return arr.map(v=>'<span'+(cls?' class="'+cls+'"':'')+'>'+esc2(v)+'</span>').join('');}}
function buildCard(cod,nome){{
  const d=DET[cod]; if(!d)return false;
  const gico=d.g==='Feminino'?'ti-venus':d.g==='Masculino'?'ti-mars':'ti-gender-bigender';
  let h='<div class="fcard"><h3>'+esc2(nome||'')+'</h3><p class="fsub">#'+esc2(cod)+'</p>';
  h+='<div class="ffld"><span class="flbl"><i class="ti '+gico+'"></i> Gênero</span><div class="fchips">'+chips([d.g],'cg')+'</div></div>';
  h+='<div class="ffld"><span class="flbl"><i class="ti ti-flask"></i> Fragância</span><div class="fchips">'+chips(d.fr)+'</div></div>';
  h+='<div class="ffld"><span class="flbl"><i class="ti ti-flame"></i> Intensidade</span><div class="fchips">'+chips([d.in],'ci')+'</div></div>';
  h+='<div class="ffld"><span class="flbl"><i class="ti ti-clock-hour-3"></i> Ideal para</span><div class="fchips">'+chips(d.id)+'</div></div>';
  h+='<div class="ffld"><span class="flbl"><i class="ti ti-users"></i> Público</span><div class="fchips">'+chips(d.pu)+'</div></div>';
  h+='</div>';
  lbCard.innerHTML=h; return true;
}}
function showCard(on){{
  lb.classList.toggle('showcard',on);
  lbDot0.classList.toggle('on',!on);lbDot1.classList.toggle('on',on);
  lbDet.innerHTML=on?'<i class="ti ti-photo"></i> Foto':'<i class="ti ti-info-circle"></i> Detalhes';
  if(on){{s=1;tx=0;ty=0;applyT(false);}}
}}
function applyT(anim){{lbImg.style.transition=anim?'transform .26s cubic-bezier(.22,.61,.36,1)':'none';lbImg.style.transform='translate('+tx+'px,'+ty+'px) scale('+s+')';lb.classList.toggle('zoomed',s>1.01);}}
function ensureBase(){{const r=lbImg.getBoundingClientRect();base={{l:r.left-tx,t:r.top-ty,w:r.width/s,h:r.height/s}};}}
function clampT(){{
  const W=innerWidth,H=innerHeight,rw=base.w*s,rh=base.h*s;
  tx=rw<=W?(W-rw)/2-base.l:Math.min(-base.l,Math.max(W-rw-base.l,tx));
  ty=rh<=H?(H-rh)/2-base.t:Math.min(-base.t,Math.max(H-rh-base.t,ty));
}}
function zoomAt(px,py,ns){{
  ns=Math.min(MAXS,Math.max(MINS,ns));
  const cx=(px-base.l-tx)/s,cy=(py-base.t-ty)/s;
  s=ns;tx=px-base.l-cx*s;ty=py-base.t-cy*s;
}}
function openLB(src,alt,cod){{
  s=1;tx=0;ty=0;base=null;lbImg.alt=alt||'';curCod=cod||null;
  lbImg.style.transition='none';lbImg.style.transform='';
  lbImg.src=src;
  const temFicha=cod&&buildCard(cod,alt);
  lb.classList.remove('zoomed','showcard');
  lb.classList.toggle('has-ficha',!!temFicha);
  showCard(false);
  lb.classList.add('open');document.body.style.overflow='hidden';
  const init=()=>{{ensureBase();applyT(false);}};
  if(lbImg.complete&&lbImg.naturalWidth)requestAnimationFrame(init);else lbImg.onload=()=>requestAnimationFrame(init);
}}
function closeLB(){{lb.classList.remove('open','zoomed','showcard','has-ficha');document.body.style.overflow='';s=1;tx=0;ty=0;base=null;curCod=null;}}
function dist(t){{return Math.hypot(t[0].clientX-t[1].clientX,t[0].clientY-t[1].clientY);}}
function mid(t){{return{{x:(t[0].clientX+t[1].clientX)/2,y:(t[0].clientY+t[1].clientY)/2}};}}

document.addEventListener('click',e=>{{
  const im=e.target.closest('.media img,.lthumb img');
  if(im){{e.preventDefault();const c=im.closest('[data-cod]');openLB(im.currentSrc||im.src,im.alt,c&&c.dataset.cod);}}
}});
lbX.onclick=e=>{{e.stopPropagation();closeLB();}};
lbDet.onclick=e=>{{e.stopPropagation();showCard(!lb.classList.contains('showcard'));}};

/* --- toque --- */
let pinch=false,panT=false,sStart=1,dStart=0,plx=0,ply=0,lastTap=0;
lb.addEventListener('touchstart',e=>{{
  if(lb.classList.contains('showcard'))return;
  if(!base)ensureBase();
  if(e.touches.length===2){{pinch=true;panT=false;sStart=s;dStart=dist(e.touches);applyT(false);}}
  else if(e.touches.length===1){{
    const now=e.timeStamp,t=e.touches[0];
    if(now-lastTap<300){{
      e.preventDefault();lastTap=0;
      if(s>1.01){{s=1;}}else zoomAt(t.clientX,t.clientY,DTS);
      clampT();applyT(true);
    }}else{{lastTap=now;panT=true;plx=t.clientX;ply=t.clientY;applyT(false);}}
  }}
}},{{passive:false}});
lb.addEventListener('touchmove',e=>{{
  if(lb.classList.contains('showcard'))return;
  if(pinch&&e.touches.length===2){{
    e.preventDefault();const m=mid(e.touches);
    zoomAt(m.x,m.y,sStart*dist(e.touches)/dStart);applyT(false);
  }}else if(panT&&e.touches.length===1&&s>1){{
    e.preventDefault();const t=e.touches[0];
    tx+=t.clientX-plx;ty+=t.clientY-ply;plx=t.clientX;ply=t.clientY;applyT(false);
  }}
}},{{passive:false}});
lb.addEventListener('touchend',e=>{{
  if(e.touches.length===0){{pinch=false;panT=false;if(base){{clampT();applyT(true);}}}}
  else if(e.touches.length===1&&pinch){{pinch=false;panT=true;plx=e.touches[0].clientX;ply=e.touches[0].clientY;}}
}});

/* --- desktop --- */
lb.addEventListener('dblclick',e=>{{if(lb.classList.contains('showcard'))return;if(!base)ensureBase();if(s>1.01){{s=1;}}else zoomAt(e.clientX,e.clientY,DTS);clampT();applyT(true);}});
lb.addEventListener('wheel',e=>{{if(lb.classList.contains('showcard'))return;e.preventDefault();if(!base)ensureBase();zoomAt(e.clientX,e.clientY,s*(e.deltaY<0?1.18:.85));clampT();applyT(false);}},{{passive:false}});
let md=false,mlx=0,mly=0;
lb.addEventListener('mousedown',e=>{{if(lb.classList.contains('showcard'))return;if(s>1){{md=true;mlx=e.clientX;mly=e.clientY;applyT(false);e.preventDefault();}}}});
addEventListener('mousemove',e=>{{if(md){{tx+=e.clientX-mlx;ty+=e.clientY-mly;mlx=e.clientX;mly=e.clientY;applyT(false);}}}});
addEventListener('mouseup',()=>{{if(md){{md=false;clampT();applyT(true);}}}});
addEventListener('resize',()=>{{if(lb.classList.contains('open')){{base=null;s=1;tx=0;ty=0;requestAnimationFrame(()=>{{ensureBase();applyT(false);}});}}}});

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
