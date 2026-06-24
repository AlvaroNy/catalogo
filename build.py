# -*- coding: utf-8 -*-
"""
Build do catalogo:
  1) converte qualquer img/*.jpg|jpeg|png novo para .webp (quality 80)
  2) roda o gerador (gera catalogo.html)
  3) copia catalogo.html -> index.html (arquivo servido pelo GitHub Pages)
  4) garante o arquivo .nojekyll
  5) avisa se algum produto ficou sem foto

Uso:  python build.py
Depois: git add -A && git commit -m "..." && git push   (o GitHub Pages publica sozinho)
"""
import os, glob, importlib.util, shutil
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")

def to_webp():
    n = 0
    for f in glob.glob(os.path.join(IMG, "*")):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            out = os.path.splitext(f)[0] + ".webp"
            Image.open(f).convert("RGB").save(out, "WEBP", quality=80, method=6)
            n += 1
    print(f"WebP: {n} imagem(ns) convertida(s).")

def gerar():
    spec = importlib.util.spec_from_file_location("g", os.path.join(BASE, "gerar_catalogo_paula.py"))
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    faltam = [p["cod"] for p in g.P if not g.img_data(p["cod"], p["cat"])]
    return len(g.P), faltam

def main():
    to_webp()
    total, faltam = gerar()
    shutil.copy2(os.path.join(BASE, "catalogo.html"), os.path.join(BASE, "index.html"))
    open(os.path.join(BASE, ".nojekyll"), "w").close()
    print(f"OK -> index.html gerado ({total} produtos).")
    if faltam:
        print(f"ATENCAO: {len(faltam)} sem foto -> {faltam} (use harvest.py para buscar)")
    else:
        print("Todos os produtos com foto.")

if __name__ == "__main__":
    main()
