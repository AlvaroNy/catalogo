# Catálogo Alvaro Nayder — Guia do Projeto

Catálogo digital de **perfumes & cosméticos (atacado)** com carrinho de pedidos
que fecha pelo WhatsApp. Gerado a partir das tabelas de preço em PDF do
**Albatros ERP** e publicado como site estático no GitHub Pages.

🔗 **Site no ar:** https://alvarony.github.io/catalogo/
📦 **Repositório:** https://github.com/AlvaroNy/catalogo

---

## 1. O que tem neste repositório

| Arquivo | O que é |
|---|---|
| `index.html` | **O catálogo publicado** (gerado automaticamente — não editar à mão) |
| `img/*.webp` | Fotos dos produtos (uma por código, + `DB.webp` = frasco dos contratipos) |
| `gerar_catalogo_paula.py` | **O gerador.** Contém os dados dos produtos (lista `P`) + o layout/HTML |
| `harvest.py` | Baixa fotos novas da web (busca `og:image` e salva em `img/`) |
| `comparar_pdfs.py` | Compara a tabela atual com PDFs novos (novos / removidos / preço) |
| `build.py` | Converte imagens p/ WebP, regenera o `index.html` e checa fotos faltando |
| `requirements.txt` | Bibliotecas Python necessárias |
| `.nojekyll` | Faz o GitHub Pages servir a pasta `img/` sem processamento |

> O **único arquivo de dados** que se edita é o `gerar_catalogo_paula.py`
> (lista `P` e os dados de contato no topo). O `index.html` é sempre gerado.

---

## 2. Pré-requisitos (qualquer computador: Windows, Mac ou Linux)

1. **Git** — https://git-scm.com
2. **GitHub CLI (`gh`)** — https://cli.github.com (para publicar; opcional, dá p/ usar `git` puro)
3. **Python 3.10+** — https://python.org

Instalar as bibliotecas (uma vez):
```bash
pip install -r requirements.txt
```

---

## 3. Primeira vez em uma máquina nova

```bash
git clone https://github.com/AlvaroNy/catalogo.git
cd catalogo
pip install -r requirements.txt
```
Pronto. Tudo que é necessário (gerador, imagens, scripts) já vem no clone.

Para **autenticar** o envio ao GitHub (uma vez por máquina):
```bash
gh auth login        # escolha GitHub.com / HTTPS / login no navegador
```

---

## 4. Atualizar o catálogo com uma tabela nova (rotina)

Quando chegarem os PDFs novos do Albatros (ex.: `perf 30-06.pdf` e `cosmeticos 30-06.pdf`):

### Passo 1 — Ver o que mudou
```bash
python comparar_pdfs.py "perf 30-06.pdf" "cosmeticos 30-06.pdf"
```
Mostra os produtos **NOVOS**, **REMOVIDOS** e com **mudança de preço**.

### Passo 2 — Editar os dados
Abra `gerar_catalogo_paula.py` e ajuste a lista **`P`** (cada produto é uma linha):

```python
add("CODIGO", "Nome de exibição", PRECO, "categoria", "texto de busca da imagem", eq="insp. X", badge="Novo")
```
- **Adicionar** produto novo → nova linha `add(...)` na categoria certa.
- **Remover** → apague a linha daquele código.
- **Mudar preço** → troque o número.
- **Contratipos Dream Brand** ficam no bloco `db(codigo, numero, "Referencia", preco)` (usam a mesma foto `DB.webp`).

Categorias disponíveis (campo 4): `perf_import`, `perf_arabe`, `perf_tester`,
`contratipo`, `arabic_insp`, `cosm_base`, `cosm_vs_lot`, `cosm_vs_spl`,
`cosm_nac`, `cosm_mist`, `cosm_cabelo`, `cosm_corpo`.

### Passo 3 — Buscar as fotos dos produtos novos
Crie um arquivo `urls.json` com os códigos novos e 1–3 links de **páginas de
loja** (de onde a foto será extraída via `og:image`). Lojas que costumam funcionar:
`justmylook`, `caretobeauty`, `intenseoud`, `perfumania`, `fragranceoutlet`,
`lojas Shopify` em geral.
```json
{
  "999": ["https://loja.com/produto-x", "https://outraloja.com/produto-x"],
  "888": ["https://loja.com/produto-y"]
}
```
Rode:
```bash
python harvest.py
```
Ele baixa, recorta e salva em `img/<codigo>.jpg`. Confira as imagens; se vier
errada (logo/banner), troque a URL e rode de novo. Produtos que compartilham
frasco (ex.: contratipos) não precisam de foto — usam `img/DB.webp`.

### Passo 4 — Gerar e conferir
```bash
python build.py
```
Converte tudo p/ WebP, gera o `index.html` e avisa se algum produto ficou sem foto.
Para pré-visualizar localmente:
```bash
python -m http.server 8531
# abra http://localhost:8531 no navegador
```

### Passo 5 — Publicar
```bash
git add -A
git commit -m "Atualiza catalogo DD-MM"
git push
```
O GitHub Pages reconstrói sozinho em ~1–3 minutos (às vezes um pouco mais).
O link continua o mesmo — quem já tem, vê a versão nova automaticamente.

---

## 5. Mudar dados de contato / marca

No topo do `gerar_catalogo_paula.py`:
```python
MARCA      = "Alvaro Nayder"
SUBTITULO  = "Perfumes & Cosméticos importados · Atacado"
WHATSAPP   = "5537991716781"      # só números: 55 + DDD + número
WHATSAPP_F = "(37) 99171-6781"    # como aparece escrito
INSTAGRAM  = "seu_instagram"      # sem @  (TROCAR pelo @ real)
ENDERECO   = "Rua Tupis, 174 - Moema"
REFERENCIA = "Tabela de Atacado · Junho/2026"
```
Depois rode `python build.py` e publique (passo 5).

---

## 6. Recursos do catálogo (já prontos)

- **Carrinho**: cliente toca em **+ Adicionar**, ajusta quantidade, e o pedido
  fica salvo no aparelho (não some ao recarregar).
- **Fechar Pedido**: pede o **nome do cliente** e abre o WhatsApp já com a lista
  no formato `#código - Nome - Valor` + **Total** (título `*Pedido - <nome>*`).
- **Cards / Lista**: botão no topo alterna a visualização.
- **Categorias retráteis**: toque no título recolhe/expande.
- **Busca** por nome, marca ou código.
- **Performance**: imagens WebP externas com *lazy-load* (página inicial leve).

---

## 7. Detalhes técnicos úteis

- **`EMBED_IMAGES`** (no gerador): `False` = imagens externas `img/*.webp` (site leve, padrão).
  `True` = embute tudo em base64 e gera **um único arquivo HTML** (bom para enviar
  offline por WhatsApp, mas pesado ~3 MB). Depois de mudar, rode `python build.py`.
- **Selo "Novo"**: passe `badge="Novo"` no `add(...)`. Outros: `"Kit"`, `"Combo"`, `"Tester"`, `"Emb. nova"`.
- **Equivalência** (contratipo/clone): `eq="insp. One Million"` aparece em itálico no card.
- **Frasco compartilhado**: contratipos (`contratipo`) e `arabic_insp` caem em `img/DB.webp`
  automaticamente (ver `CAT_FALLBACK` no gerador).
- O `harvest.py` ignora imagens muito pequenas/largas (provável logo) — se algo
  falhar, basta outra URL no `urls.json`.

---

## 8. Resolução de problemas

- **Build do GitHub Pages demorando**: normal até ~1–3 min; ocasionalmente mais
  (lentidão do GitHub). Veja o status em *Settings → Pages* no repositório.
- **Produto sem foto**: aparece um placeholder com a inicial. Procure outra URL e
  rode `harvest.py` de novo, ou copie uma foto parecida: `cp img/<similar>.jpg img/<codigo>.jpg` e `python build.py`.
- **`gh` não autenticado**: rode `gh auth login`, ou use `git push` com usuário/senha (token) do GitHub.
- **Imagem veio errada (logo da loja)**: troque a URL no `urls.json` (prefira páginas
  de produto de lojas Shopify) e rode `harvest.py` novamente.

---

*Projeto mantido por Alvaro Nayder. Estrutura e automação documentadas para
continuidade em qualquer máquina.*
