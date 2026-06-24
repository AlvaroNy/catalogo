# -*- coding: utf-8 -*-
"""
Le urls.json = { "<codigo>": ["<url_pagina_ou_imagem>", ...], ... }
Para cada codigo sem imagem ainda, tenta cada url:
  - se for pagina: extrai og:image / twitter:image / link image_src
  - baixa a imagem (com Referer), valida, redimensiona p/ 440px e salva img/<cod>.jpg
Uso:  python harvest.py            (processa todos do urls.json que ainda faltam)
      python harvest.py 38 117     (so esses codigos)
      python harvest.py --force    (rebaixa mesmo os que ja tem)
"""
import os, io, re, sys, json, html, requests
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
os.makedirs(IMG, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

def has_img(cod):
    return any(os.path.exists(os.path.join(IMG, f"{cod}.{e}")) for e in ("jpg","jpeg","png","webp"))

def og_from_page(url):
    try:
        r = requests.get(url, headers={"User-Agent":UA,"Accept-Language":"en-US,en;q=0.9"}, timeout=20)
    except Exception as e:
        return None, f"pgerr {e}"
    if r.status_code != 200:
        return None, f"pg {r.status_code}"
    t = r.text
    pats = [
        r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image',
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)',
        r'<link[^>]+rel=["\']image_src["\'][^>]+href=["\']([^"\']+)',
    ]
    for p in pats:
        m = re.search(p, t, re.I)
        if m:
            return html.unescape(m.group(1)), "ok"
    return None, "no-og"

def download_img(img_url, referer):
    h = {"User-Agent":UA, "Referer":referer, "Accept":"image/avif,image/webp,image/*,*/*"}
    if img_url.startswith("//"): img_url = "https:" + img_url
    try:
        r = requests.get(img_url, headers=h, timeout=20)
    except Exception as e:
        return None, f"dlerr {e}"
    if r.status_code != 200:
        return None, f"dl {r.status_code}"
    if "image" not in r.headers.get("content-type","") and not re.search(r'\.(jpe?g|png|webp)', img_url, re.I):
        return None, "not-image"
    return r.content, "ok"

def save(cod, content):
    try:
        im = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception as e:
        return False, f"badimg {e}"
    if min(im.size) < 120:   # muito pequena, provavelmente icone/logo
        return False, f"small {im.size}"
    im.thumbnail((440, 440))
    bg = Image.new("RGB", im.size, (255,255,255))
    bg.paste(im)
    bg.save(os.path.join(IMG, f"{cod}.jpg"), "JPEG", quality=80, optimize=True)
    return True, f"{im.size}"

def process(cod, urls):
    for u in urls:
        u = u.strip()
        if not u: continue
        if re.search(r'\.(jpe?g|png|webp)(\?|$)', u, re.I):  # ja eh imagem direta
            content, st = download_img(u, u)
            ref = u
        else:
            img_url, st = og_from_page(u)
            if not img_url:
                print(f"   - {u[:50]} -> {st}"); continue
            content, st = download_img(img_url, u)
            ref = u
        if not content:
            print(f"   - {u[:50]} -> {st}"); continue
        ok, info = save(cod, content)
        if ok:
            print(f"   OK {cod} <- {u[:50]} ({info})"); return True
        else:
            print(f"   - {u[:50]} -> {info}")
    return False

def main():
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv
    with open(os.path.join(BASE, "urls.json"), encoding="utf-8") as f:
        data = json.load(f)
    todo = args if args else list(data.keys())
    done = fail = skip = 0
    for cod in todo:
        if cod not in data:
            print(f"!! {cod} nao esta no urls.json"); continue
        if has_img(cod) and not force:
            skip += 1; continue
        print(f"[{cod}]")
        if process(cod, data[cod]): done += 1
        else: fail += 1; print(f"   xx FALHOU {cod}")
    print(f"\n== ok:{done}  falhou:{fail}  ja-tinha:{skip} ==")

if __name__ == "__main__":
    main()
