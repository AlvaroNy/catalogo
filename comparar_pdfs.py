# -*- coding: utf-8 -*-
"""
Compara a tabela atual do catalogo (lista P em gerar_catalogo_paula.py) com os
PDFs novos do Albatros ERP. Mostra: produtos NOVOS, REMOVIDOS e MUDANCA DE PRECO.

Uso:
    python comparar_pdfs.py "caminho/perf.pdf" "caminho/cosmeticos.pdf"
(pode passar 1 ou mais PDFs)
"""
import re, sys, importlib.util, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))

def carregar_P():
    spec = importlib.util.spec_from_file_location("g", os.path.join(BASE, "gerar_catalogo_paula.py"))
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    return g

def parse_pdf(fn):
    from pypdf import PdfReader
    d = {}
    for p in PdfReader(fn).pages:
        for ln in p.extract_text().splitlines():
            m = re.match(r"^(\d+)\s+(.*?)\s+([\d.]+,\d{2})UN\s*$", ln.strip())
            if m:
                cod = m.group(1)
                nome = m.group(2).strip()
                preco = float(m.group(3).replace(".", "").replace(",", "."))
                d[cod] = (nome, preco)
    return d

def main():
    if len(sys.argv) < 2:
        print("Uso: python comparar_pdfs.py <pdf1> [pdf2 ...]"); return
    g = carregar_P()
    cur = {p["cod"]: (p["nome"], p["preco"]) for p in g.P}
    dup = [c for c, n in Counter(p["cod"] for p in g.P).items() if n > 1]

    new = {}
    for fn in sys.argv[1:]:
        new.update(parse_pdf(fn))

    add = [c for c in new if c not in cur]
    rem = [c for c in cur if c not in new]
    chg = [(c, cur[c][1], new[c][1]) for c in new if c in cur and abs(cur[c][1] - new[c][1]) > 0.001]

    print(f"Catalogo atual: {len(cur)}  |  PDFs novos: {len(new)}  |  Duplicados: {dup or 'nenhum'}\n")
    print(f"=== NOVOS ({len(add)}) ===")
    for c in add: print(f"  {c} | {new[c][0]} | R$ {new[c][1]:.2f}")
    print(f"\n=== REMOVIDOS ({len(rem)}) ===")
    for c in rem: print(f"  {c} | {cur[c][0]}")
    print(f"\n=== MUDANCA DE PRECO ({len(chg)}) ===")
    for c, o, n in chg: print(f"  {c} | {cur[c][0]} | {o:.2f} -> {n:.2f}")

if __name__ == "__main__":
    main()
