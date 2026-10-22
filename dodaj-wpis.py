#!/usr/bin/env python3
# dodaj-wpis.py — publikuje notkę .md na blogu pochmurny.net
#
# Użycie:
#   python3 dodaj-wpis.py wpisy/moj-notka.md [--no-git]
#
# Wymagane linie na początku pliku .md:
#   # Tytuł wpisu
#   data: 2026-10-22
#   tagi: devops, linux
#   lead: Jedno zdanie do listy na blogu.
#
# Reszta pliku to zwykły Markdown (## nagłówki, - listy, ``` kod, **pogrubienie**).
# Skrypt: generuje wpis-<slug>.html (wg szablonu wpis.html), dodaje wiersz na górę
# listy w blog.html, liczy czas czytania i (bez --no-git) komituje + puszuje.
import sys, re, html, datetime, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = ROOT / "wpis.html"
BLOG = ROOT / "blog.html"


def slugify(t):
    import unicodedata
    t = t.replace("ł", "l").replace("Ł", "L")
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def inline(s):
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\\2">\\1</a>', s)
    return s


def md2html(md):
    out, para, in_code, in_ul = [], [], False, False

    def flush():
        nonlocal para
        if para:
            out.append("<p>" + " ".join(inline(x) for x in para) + "</p>")
            para = []

    def closeul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    for line in md.splitlines():
        if line.startswith("```"):
            flush(); closeul()
            out.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(line)); continue
        if not line.strip():
            flush(); closeul(); continue
        if line.startswith("### "):
            flush(); closeul(); out.append("<h3>" + inline(line[4:]) + "</h3>")
        elif line.startswith("## "):
            flush(); closeul(); out.append("<h2>" + inline(line[3:]) + "</h2>")
        elif line.startswith("> "):
            flush(); closeul(); out.append("<blockquote><p>" + inline(line[2:]) + "</p></blockquote>")
        elif line.startswith("- "):
            flush()
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append("<li>" + inline(line[2:]) + "</li>")
        else:
            closeul(); para.append(line.strip())
    flush(); closeul()
    if in_code:
        out.append("</code></pre>")
    return "\n      ".join(out)


def parse(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"# (.+?)\n", raw)
    if not m:
        sys.exit(f"PLIK {path}: brak tytułu w pierwszej linii (wymagane '# Tytuł')")
    title, rest = m.group(1).strip(), raw[m.end():]

    def field(name, txt):
        f = re.search(rf"^{name}:\s*(.+)$", txt, re.M)
        return f.group(1).strip() if f else ""

    data, tagi, lead = field("data", rest), field("tagi", rest), field("lead", rest)
    if not (data and tagi and lead):
        sys.exit(f"PLIK {path}: brak linii 'data:', 'tagi:' lub 'lead:'")
    body = re.sub(r"^(data|tagi|lead):\s*.+$", "", rest, flags=re.M).strip()
    return title, data, tagi, lead, body


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    git = "--no-git" not in sys.argv
    if not args:
        sys.exit("Użycie: python3 dodaj-wpis.py wpisy/notka.md [--no-git]")
    src = pathlib.Path(args[0]).expanduser().resolve()
    title, data, tagi, lead, body = parse(src)

    dt = datetime.datetime.strptime(data, "%Y-%m-%d")
    when = dt.strftime("%d.%m.%Y")
    words = len(re.sub(r"[#*`\[\]()>\-]", " ", body).split())
    mins = max(1, round(words / 200))
    tags = [t.strip() for t in tagi.split(",") if t.strip()]
    slug = slugify(title)
    fname = f"wpis-{slug}.html"
    desc = html.escape(re.sub(r"\s+", " ", lead), quote=True)

    page = TEMPLATE.read_text(encoding="utf-8")
    page = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} — pochmurny.net</title>",
                  page, count=1, flags=re.S)
    page = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">',
                  page, count=1, flags=re.S)
    page = re.sub(r"<h1>.*?</h1>", f"<h1>{html.escape(title)}</h1>", page, count=1, flags=re.S)
    meta = ('<div class="meta">\n'
            f'      <span><b>{when}</b></span>\n'
            f'      <span>{mins} MIN CZYTANIA</span>\n'
            f'      <span>{html.escape(" · ".join(t.upper() for t in tags))}</span>\n'
            '    </div>')
    page = re.sub(r'<div class="meta">.*?</div>', meta, page, count=1, flags=re.S)
    page = re.sub(r'<div class="prose">.*?\n    </div>',
                  '<div class="prose">\n      ' + md2html(body) + '\n    </div>',
                  page, count=1, flags=re.S)
    page = re.sub(r"\s*<nav class=\"post-nav\">.*?</nav>", "", page, count=1, flags=re.S)
    (ROOT / fname).write_text(page, encoding="utf-8")

    row = (f'      <a class="row" href="{fname}">\n'
           f'        <div class="when">{when}</div>\n'
           f'        <div class="main">\n'
           f'          <h3>{html.escape(title)}</h3>\n'
           f'          <p>{html.escape(lead)}</p>\n'
           f'          <div class="tags">'
           + "".join(f'<span class="tag-pill">{html.escape(t)}</span>' for t in tags)
           + '</div>\n'
           f'        </div>\n'
           f'        <div class="go">{mins} MIN →</div>\n'
           f'      </a>\n\n')
    blog = BLOG.read_text(encoding="utf-8")
    blog = blog.replace('<div class="rows">\n', '<div class="rows">\n' + row, 1)
    n = len(re.findall(r'<a class="row"', blog))
    blog = re.sub(r"// \d+ wpis", f"// {n:02d} wpis", blog, count=1)
    BLOG.write_text(blog, encoding="utf-8")

    print(f"OK: {fname}  (wierszy na blogu: {n})")
    if git:
        for f in (fname, "blog.html", str(src.relative_to(ROOT)) if src.is_relative_to(ROOT) else str(src)):
            subprocess.run(["git", "add", f], check=True, cwd=ROOT)
        subprocess.run(["git", "commit", "-m", f"wpis: {title}"], check=True, cwd=ROOT)
        subprocess.run(["git", "push"], check=True, cwd=ROOT)
        print("zpushowane — blog zaktualizuje się na https://pochmurny.net/blog.html za ~1 min")


if __name__ == "__main__":
    main()
