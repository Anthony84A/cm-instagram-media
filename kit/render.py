"""Gabarits Instagram d'Anthony Arniaud -> JPEG 1080x1350.
Usage : python3 render.py spec.json sortie/
spec.json = liste de slides : {"type": "cover|tip|realisation|cta", ...champs}
"""
import json, sys, base64, html, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FONTS = ROOT / "node_modules/@fontsource"

def font(face, path, weight):
    b64 = base64.b64encode((FONTS / path).read_bytes()).decode()
    return f"@font-face{{font-family:'{face}';font-weight:{weight};src:url(data:font/woff2;base64,{b64}) format('woff2');}}"

FONT_CSS = "".join([
    font("Poppins", "poppins/files/poppins-latin-600-normal.woff2", 600),
    font("Poppins", "poppins/files/poppins-latin-700-normal.woff2", 700),
    font("Inter", "inter/files/inter-latin-400-normal.woff2", 400),
    font("Inter", "inter/files/inter-latin-500-normal.woff2", 500),
    font("JetBrains Mono", "jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2", 400),
    font("JetBrains Mono", "jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2", 500),
])

CSS = """
:root{--void:#0d1220;--surface:#161f33;--surface2:#1c2740;--ink:#f3f5f9;--dim:#98a2b8;--soft:#6f7b93;
--cyan:#62e1e9;--blue:#0652e9;--blue-soft:#3d7dff;--line:hsla(0,0%,100%,.09);--line-strong:hsla(0,0%,100%,.18)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:var(--void);color:var(--ink);font-family:Inter,sans-serif;overflow:hidden;position:relative}
.bg{position:absolute;inset:0;background:
 radial-gradient(900px 600px at 85% -10%,rgba(6,82,233,.35),transparent 60%),
 radial-gradient(700px 500px at -10% 110%,rgba(98,225,233,.16),transparent 60%);}
.grid{position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
 background-size:60px 60px;mask-image:radial-gradient(ellipse at center,#000 30%,transparent 80%);opacity:.6}
.wrap{position:relative;height:100%;padding:96px 90px 80px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:18px;font-family:'JetBrains Mono';font-size:24px;color:var(--dim)}
.logo{font-family:Poppins;font-weight:700;font-size:30px;color:var(--void);background:var(--cyan);border-radius:12px;padding:6px 14px;letter-spacing:-1px}
.tag{font-family:'JetBrains Mono';font-size:28px;color:var(--cyan)}
h1{font-family:Poppins;font-weight:700;font-size:92px;line-height:1.05;letter-spacing:-2px}
h2{font-family:Poppins;font-weight:700;font-size:70px;line-height:1.08;letter-spacing:-1.5px}
.hl{background:linear-gradient(90deg,var(--blue-soft),var(--cyan));-webkit-background-clip:text;color:transparent}
p{font-size:38px;line-height:1.45;color:var(--dim)}
p strong{color:var(--ink);font-weight:500}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-family:'JetBrains Mono';font-size:24px;color:var(--soft);
 border-top:1px solid var(--line-strong);padding-top:30px}
.swipe{color:var(--cyan)}
.num{font-family:Poppins;font-weight:700;font-size:200px;line-height:1;color:transparent;-webkit-text-stroke:3px var(--cyan);opacity:.9}
.card{background:var(--surface);border:1px solid var(--line-strong);border-radius:28px;padding:44px}
.btn{display:inline-block;background:var(--blue);color:#fff;font-family:Poppins;font-weight:600;font-size:38px;padding:30px 56px;border-radius:999px}
.browser{border-radius:24px;overflow:hidden;border:1px solid var(--line-strong);box-shadow:0 40px 80px rgba(0,0,0,.5)}
.bar{background:var(--surface2);height:56px;display:flex;align-items:center;gap:12px;padding:0 24px}
.dot{width:16px;height:16px;border-radius:50%;background:var(--soft)}
.url{margin-left:20px;font-family:'JetBrains Mono';font-size:22px;color:var(--dim)}
.browser img{display:block;width:100%}
.chips{display:flex;gap:14px;flex-wrap:wrap}
.chip{font-family:'JetBrains Mono';font-size:24px;color:var(--cyan);background:rgba(98,225,233,.1);border:1px solid rgba(98,225,233,.25);padding:10px 20px;border-radius:999px}
"""

e = html.escape
def rich(t):  # **gras** et [[surligné]]
    import re
    t = re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", t)
    for a, b in ((" €", "\u00a0€"), (" ?", "\u00a0?"), (" :", "\u00a0:"), (" !", "\u00a0!"), ("« ", "«\u00a0"), (" »", "\u00a0»"), ("dès ", "dès\u00a0")):
        t = t.replace(a, b)
    t = e(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"\[\[(.+?)\]\]", r'<span class="hl">\1</span>', t)

def foot(s, i, n):
    right = '<span class="swipe">Glissez →</span>' if i < n else "anthonyarniaud.fr"
    return f'<div class="foot"><span>{i}/{n}</span>{right}</div>' if n > 1 else f'<div class="foot"><span>anthonyarniaud.fr</span><span>Vaucluse · Luberon</span></div>'

LOGO = base64.b64encode((ROOT / "logo.png").read_bytes()).decode()
BRAND = f'<div class="brand"><img src="data:image/png;base64,{LOGO}" style="height:92px;mix-blend-mode:lighten"></div>'

def slide(s, i, n):
    t = s["type"]
    if t == "cover":
        body = f'''{BRAND}<div style="margin-top:auto;margin-bottom:auto">
<div class="tag">&lt;{e(s.get("tag","conseil"))} /&gt;</div><h1 style="margin-top:36px">{rich(s["title"])}</h1>
<p style="margin-top:44px">{rich(s.get("subtitle",""))}</p></div>'''
    elif t == "tip":
        body = f'''{BRAND}<div style="margin-top:auto;margin-bottom:auto"><div class="num">{e(str(s["num"]))}</div>
<h2 style="margin-top:20px">{rich(s["title"])}</h2><p style="margin-top:40px">{rich(s["text"])}</p></div>'''
    elif t == "realisation":
        img = base64.b64encode((ROOT / s["image"]).read_bytes()).decode()
        chips = "".join(f'<span class="chip">{e(c)}</span>' for c in s.get("chips", []))
        body = f'''{BRAND}<div class="tag" style="margin-top:70px">&lt;réalisation /&gt;</div>
<h2 style="margin-top:24px">{rich(s["title"])}</h2>
<div class="browser" style="margin-top:50px"><div class="bar"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="url">{e(s["url"])}</span></div>
<img src="data:image/jpeg;base64,{img}"></div>
<p style="margin-top:44px">{rich(s.get("text",""))}</p><div class="chips" style="margin-top:30px">{chips}</div>'''
    elif t == "cta":
        body = f'''{BRAND}<div style="margin-top:auto;margin-bottom:auto"><h2>{rich(s["title"])}</h2>
<p style="margin-top:40px">{rich(s["text"])}</p><div style="margin-top:70px"><span class="btn">{e(s.get("button","Demander un devis"))}</span></div>
<p style="margin-top:40px;font-family:'JetBrains Mono';font-size:28px;color:var(--cyan)">{e(s.get("note","Réponse sous 24 h · lien en bio"))}</p></div>'''
    else:
        raise ValueError(t)
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}{CSS}</style></head><body><div class="bg"></div><div class="grid"></div><div class="wrap">{body}{foot(s,i,n)}</div></body></html>'

def main(spec_path, out_dir):
    slides = json.loads(pathlib.Path(spec_path).read_text())
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        import os
        exe = "/usr/bin/google-chrome"
        b = p.chromium.launch(executable_path=exe) if os.path.exists(exe) else p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(slides, 1):
            pg.set_content(slide(s, i, len(slides)), wait_until="load")
            pg.evaluate("document.fonts.ready")
            f = out / f"{i:02d}-{s['type']}.jpg"
            pg.screenshot(path=str(f), type="jpeg", quality=92)
            print(f)
        b.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
