#!/usr/bin/env python3
"""The Marketing School: content build script.

  python3 scripts/build.py page content/learn/<slug>.json   # render one article from its spec
  python3 scripts/build.py index                            # rebuild hubs, sitemap, footer, nav, llms.txt

A spec is JSON:
{
  "section": "learn" | "guide",     # learn -> /learn/<slug>, guide -> /<slug>
  "slug": "google-ads-negative-keywords",
  "title": "Google Ads Negative Keywords: A Beginner's Guide",   # <title>, before " | The Marketing School"
  "description": "One or two sentences for meta description (under 160 chars).",
  "h1": "Page H1",
  "eyebrow": "Learn · Google Ads",
  "crumb": "Short breadcrumb label",
  "lede": "Intro paragraph under the H1 (plain text or simple inline HTML).",
  "card": "One-line summary for the hub card.",
  "date": "2026-11-28",
  "body_html": "<div class=\"tldr\">...</div><section><h2>..</h2><p>..</p></section> ...",
  "faqs": [{"q": "...", "a": "..."}],
  "related": [{"href": "/learn/...", "text": "..."}]
}
Learn pages get an email signup box. Guide pages get the account review offer box.
After adding a spec, add its slug to content/registry.json, then run `page` and `index`.
"""
import datetime, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.themarketingschool.com"
REG = os.path.join(ROOT, "content", "registry.json")

NAV = """<nav>
  <a class="nav-logo" href="/">The Marketing School</a>
  <ul class="nav-links">
    <li><a href="/#process">How it works</a></li>
    <li><a href="/#pricing">Services</a></li>
    <li><a href="/learn">Learn</a></li>
    <li><a href="/guides">Guides</a></li>
    <li><a href="/#about">About</a></li>
    <li class="nav-cta-wrap"><a href="/contact" class="nav-cta"><span class="lg">Free Account Review</span><span class="sm">Book a Review</span></a></li>
    <li class="nav-cta-wrap nav-toggle-wrap"><button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></li>
  </ul>
</nav>
<div class="mobile-menu" id="mobile-menu">
  <a href="/#process">How it works</a>
  <a href="/#pricing">Services</a>
  <a href="/done-for-you-ads">Done-for-you ads</a>
  <a href="/learn">Learn ads (free)</a>
  <a href="/guides">Guides</a>
  <a href="/#about">About</a>
  <a href="/contact">Contact</a>
</div>
<div class="menu-backdrop"></div>"""

FOOTER_TOP = """<footer>
  <div class="footer-logo">The Marketing School<small>Done-for-you ads. AI built in.</small></div>
  <ul class="footer-links">
    <li><a href="/contact">Free account review</a></li>
    <li><a href="/#pricing">Services</a></li>
    <li><a href="/learn">Learn</a></li>
    <li><a href="/guides">Guides</a></li>
    <li><a href="/#about">About</a></li>
    <li><a href="/contact">Contact</a></li>
    <li><a href="/privacy">Privacy</a></li>
    <li><a href="/terms">Terms</a></li>
  </ul>
  <span class="footer-copy">© 2026 The Marketing School</span>
"""

SERVICES = [("/ai-ads-management", "AI-powered ads management"), ("/google-ads-management", "Google Ads management"),
            ("/meta-ads-management", "Meta ads management"), ("/tiktok-ads-management", "TikTok ads management"),
            ("/linkedin-ads-management", "LinkedIn ads management")]

OFFER_BOX = """<div class="offer-box">
  <p class="offer-kicker">Done-For-You Ads</p>
  <h2>Rather have someone run this for you?</h2>
  <p>We build your ads with AI and run them on 1 or 2 platforms (Google, Meta, TikTok, LinkedIn), install AI in your ad accounts to find wasted spend, write ads, and report results, and send you a monthly results report. Built for businesses spending under $10k a month on ads.</p>
  <p><a class="btn" href="/contact" data-cta-plan="review">Book a free account review</a></p>
  <p class="offer-guarantee"><strong>If you're not getting better results in 90 days, we'll refund our fee.</strong> <span>Refund covers our fee only. Ad spend paid to Google, Meta, and other platforms isn't refundable.</span></p>
  <p class="offer-small">Spending $30k+ a month? <a href="/contact" data-cta-plan="allin">Book a free account review</a></p>
</div>"""

SIGNUP_BOX = """<div class="learn-signup" id="signup">
  <h2>Get the next guide by email</h2>
  <p>New ads tutorials every week, written by Evan Baker (20+ years running paid media). Free. Unsubscribe any time.</p>
  <form class="ls-form" novalidate>
    <input type="text" name="name" placeholder="First name" autocomplete="given-name" aria-label="First name">
    <input type="email" name="email" placeholder="Email" autocomplete="email" aria-label="Email" required>
    <input type="text" name="company" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <button class="btn" type="submit">Send me guides</button>
  </form>
  <p class="ls-fine">See our <a href="/privacy" style="color:#C9D3E0">privacy policy</a>.</p>
</div>"""


def esc(s):
    return html.escape(s, quote=True)


def url_for(section, slug):
    return f"{SITE}/learn/{slug}" if section == "learn" else f"{SITE}/{slug}"


def head(title, desc, url, ld):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="The Marketing School">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0A2342">
<script>window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};</script>
<script defer src="/_vercel/insights/script.js"></script>
<script src="/lead-config.js"></script>
<script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="font" type="font/woff2" crossorigin href="https://fonts.gstatic.com/s/archivo/v25/k3kQo8UDI-1M0wlSfdnoLg.woff2">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/site.css">
</head>
<body>
{NAV}
"""


TAIL = """
<script>
document.querySelectorAll('[data-cta-plan]').forEach(function(a){
  a.addEventListener('click',function(){ try{ window.va&&window.va('event',{name:'package_cta_click',data:{plan:a.getAttribute('data-cta-plan'),location:location.pathname}}); }catch(e){} });
});
</script>
<script src="/site.js"></script>
</body>
</html>
"""


def footer_groups(reg):
    def items(pairs):
        return "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in pairs)
    guides = [("/" + s, page_meta("guide", s)["crumb"]) for s in reg["guides"][:6]] + [("/guides", "All guides →")]
    learn = [("/learn/" + s, page_meta("learn", s)["crumb"]) for s in reg["learn"][:6]] + [("/learn", "All tutorials →")]
    return ("  <!-- footer-groups:start -->\n  <div class=\"footer-groups\">\n"
            f"    <div class=\"footer-group\"><h4>Done-for-you ads</h4><ul>{items(SERVICES)}</ul></div>\n"
            f"    <div class=\"footer-group\"><h4>Guides</h4><ul>{items(guides)}</ul></div>\n"
            f"    <div class=\"footer-group\"><h4>Learn ads</h4><ul>{items(learn)}</ul></div>\n"
            "  </div>\n  <!-- footer-groups:end -->\n</footer>")


def file_for(section, slug):
    return os.path.join(ROOT, "learn", slug + ".html") if section == "learn" else os.path.join(ROOT, slug + ".html")


def page_meta(section, slug):
    """Read title, description, crumb, eyebrow, card from a built page (works for old hand-built pages too)."""
    s = open(file_for(section, slug), encoding="utf-8").read()
    def grab(pat, default=""):
        m = re.search(pat, s, re.S)
        return html.unescape(re.sub(r"<[^>]+>", "", m.group(1)).strip()) if m else default
    title = grab(r"<title>(.*?)</title>").replace(" | The Marketing School", "")
    desc = grab(r'<meta name="description" content="(.*?)"')
    crumb = grab(r'class="crumbs".*?<span>([^<]*)</span>\s*</div>') or title
    eyebrow = grab(r'<div class="eyebrow">(.*?)</div>')
    card = grab(r'<meta name="tms:card" content="(.*?)"') or desc
    date = grab(r'<meta name="tms:date" content="(.*?)"', "2026-11-22")
    return dict(title=title, desc=desc, crumb=crumb, eyebrow=eyebrow, card=card, date=date)


def render_page(spec):
    sec, slug = spec["section"], spec["slug"]
    url = url_for(sec, slug)
    title = spec["title"] + " | The Marketing School"
    crumbs = [("Home", SITE + "/")]
    if sec == "learn":
        crumbs.append(("Learn", SITE + "/learn"))
    else:
        crumbs.append(("Guides", SITE + "/guides"))
    crumbs.append((spec["crumb"], url))
    graph = [
        {"@type": "Article", "@id": url + "#article", "headline": spec["h1"], "description": spec["description"],
         "url": url, "datePublished": spec["date"], "dateModified": spec.get("updated", spec["date"]),
         "author": {"@type": "Person", "name": "Evan Baker", "url": "https://www.linkedin.com/in/evanabaker/"},
         "publisher": {"@id": SITE + "/#org"}, "image": SITE + "/og-image.png",
         "isPartOf": {"@type": "WebSite", "@id": SITE + "/#website", "name": "The Marketing School", "url": SITE + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
    ]
    if spec.get("faqs"):
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", f["a"])}}
            for f in spec["faqs"]]})
    graph.append({"@type": "Organization", "@id": SITE + "/#org", "name": "The Marketing School", "url": SITE + "/",
                  "logo": SITE + "/apple-touch-icon.png"})
    out = head(title, spec["description"], url, {"@context": "https://schema.org", "@graph": graph})
    out = out.replace("</head>", f'<meta name="tms:card" content="{esc(spec.get("card", spec["description"]))}">\n'
                                 f'<meta name="tms:date" content="{spec["date"]}">\n</head>')
    crumb_html = " <span aria-hidden=\"true\">/</span> ".join(
        [f'<a href="{u.replace(SITE, "") or "/"}">{esc(n)}</a>' for n, u in crumbs[:-1]] + [f"<span>{esc(spec['crumb'])}</span>"])
    cta = ('<a class="btn" href="#signup">Get free guides by email</a>' if sec == "learn"
           else '<a class="btn" href="/contact" data-cta-plan="review">Book a free account review</a>')
    out += f"""
<header class="page-hero"><div class="page-hero-inner">
  <div class="crumbs" role="navigation" aria-label="Breadcrumb">{crumb_html}</div>
  <div class="eyebrow">{esc(spec["eyebrow"])}</div>
  <h1>{esc(spec["h1"])}</h1>
  <p class="lede">{spec["lede"]}</p>
  <div class="hero-ctas">{cta}</div>
</div></header>
<main class="wrap article">
<p class="byline">By Evan Baker · Updated {datetime.date.fromisoformat(spec.get("updated", spec["date"])).strftime("%b %-d, %Y")}</p>
{spec["body_html"]}
{SIGNUP_BOX if sec == "learn" else OFFER_BOX}
"""
    if sec == "learn":
        out += '<p class="offer-small">Running ads for a business and want a second set of eyes? <a href="/contact" data-cta-plan="review">Book a free account review</a>.</p>\n'
    if spec.get("faqs"):
        out += '  <section class="faq-block" id="faq">\n    <h2>Questions, answered</h2>\n'
        for f in spec["faqs"]:
            out += f'    <details class="faq-d"><summary>{esc(f["q"])}</summary><p>{f["a"]}</p></details>\n'
        out += "  </section>\n"
    rel = "".join(f'<li><a href="{r["href"]}">{esc(r["text"])}</a></li>' for r in spec.get("related", []))
    out += f'  <aside class="related" aria-label="Related pages"><h2>Keep reading</h2><ul>{rel}</ul></aside>\n</main>\n\n'
    out += FOOTER_TOP + footer_groups(load_reg()) + TAIL
    path = file_for(sec, slug)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(out)
    print("wrote", os.path.relpath(path, ROOT))


def load_reg():
    reg = json.load(open(REG, encoding="utf-8"))
    for k, sec in (("learn", "learn"), ("guides", "guide")):
        reg[k] = [s for s in reg[k] if os.path.exists(file_for(sec, s))]
    return reg


def render_hub(kind, reg):
    if kind == "learn":
        slug, h1, crumb = "learn", "Learn to run ads that make money", "Learn"
        title = "Learn Google, Meta and TikTok Ads (Free Guides)"
        desc = "Free, practical tutorials on running Google Ads, Meta ads, TikTok ads, tracking, and ad copy, from someone who has managed $200M+ in ad spend."
        lede = "Free, practical tutorials for running paid ads yourself: Google, Meta, TikTok, LinkedIn, tracking, and copy. Written by Evan Baker, who has managed $200M+ in ad spend over 20+ years. New guides every week."
        items = [("/learn/" + s, page_meta("learn", s)) for s in reg["learn"]]
        extra = SIGNUP_BOX
        cta = '<a class="btn" href="#signup">Get free guides by email</a>'
    else:
        slug, h1, crumb = "guides", "Guides for business owners buying ads", "Guides"
        title = "Guides: Hiring an Ad Agency, Costs, and AI Ads"
        desc = "Straight answers on hiring an ad agency, what it costs, and how AI fits into running Google and Meta ads."
        lede = "Straight answers for business owners deciding how to get ads run: hire, learn, or mix both. If you'd rather talk it through, book a free account review and we'll look at your accounts with you."
        items = [("/" + s, page_meta("guide", s)) for s in reg["guides"]]
        extra = OFFER_BOX
        cta = '<a class="btn" href="/contact" data-cta-plan="review">Book a free account review</a>'
    url = f"{SITE}/{slug}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#webpage", "name": title, "url": url, "description": desc,
         "isPartOf": {"@type": "WebSite", "@id": SITE + "/#website", "name": "The Marketing School", "url": SITE + "/"},
         "publisher": {"@id": SITE + "/#org"}},
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + h, "name": m["title"]} for i, (h, m) in enumerate(items)]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]},
        {"@type": "Organization", "@id": SITE + "/#org", "name": "The Marketing School", "url": SITE + "/", "logo": SITE + "/apple-touch-icon.png"}]}
    out = head(title + " | The Marketing School", desc, url, ld)
    cards = "".join(
        f'<li><a href="{h}"><span class="k">{esc(m["eyebrow"].replace("Learn · ", "").replace("Guide · ", ""))}</span>'
        f'<span class="t">{esc(m["crumb"][:1].upper() + m["crumb"][1:])}</span><span class="d">{esc(m["card"])}</span></a></li>'
        for h, m in items)
    out += f"""
<header class="page-hero"><div class="page-hero-inner">
  <div class="crumbs" role="navigation" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <span>{crumb}</span></div>
  <div class="eyebrow">{crumb}</div>
  <h1>{esc(h1)}</h1>
  <p class="lede">{esc(lede)}</p>
  <div class="hero-ctas">{cta}</div>
</div></header>
<main class="wrap article">
  <section>
    <h2>{"All tutorials" if kind == "learn" else "All guides"}</h2>
    <ul class="hub-grid">{cards}</ul>
  </section>
{extra}
</main>

"""
    out += FOOTER_TOP + footer_groups(reg) + TAIL
    path = os.path.join(ROOT, "learn", "index.html") if kind == "learn" else os.path.join(ROOT, "guides.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(out)
    print("wrote", os.path.relpath(path, ROOT))


def all_pages():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if not d.startswith(".") and d not in ("scripts", "content", "images", "node_modules")]
        for f in fn:
            if f.endswith(".html"):
                out.append(os.path.join(dp, f))
    return sorted(out)


def path_to_url(p):
    rel = os.path.relpath(p, ROOT).replace(os.sep, "/")[:-5]
    if rel == "index":
        return SITE + "/"
    if rel.endswith("/index"):
        rel = rel[:-6]
    return f"{SITE}/{rel}"


def rebuild_index():
    reg = load_reg()
    render_hub("learn", reg)
    render_hub("guide", reg)
    fg = footer_groups(reg)
    nav_learn = '<li><a href="/learn">Learn</a></li>'
    for p in all_pages():
        s = open(p, encoding="utf-8").read()
        o = s
        # footer groups (managed block)
        s = re.sub(r"\s*(<!-- footer-groups:start -->\s*)?<div class=\"footer-groups\">.*?</div>\s*</div>\s*(<!-- footer-groups:end -->\s*)?</footer>",
                   "\n" + fg, s, count=1, flags=re.S)
        # footer links: add Learn + Guides after Services
        if 'href="/learn">Learn</a></li>' not in s.split("<footer>")[-1]:
            s = re.sub(r'(<ul class="footer-links">.*?<li><a href="[^"]*#pricing">Services</a></li>)',
                       r'\1\n    <li><a href="/learn">Learn</a></li>\n    <li><a href="/guides">Guides</a></li>', s, count=1, flags=re.S)
        # top nav: add Learn after Services (replace AI Implementation/FAQ entries? keep existing, just insert)
        if nav_learn not in s:
            s = re.sub(r'(<ul class="nav-links">.*?<li><a href="[^"]*#pricing">Services</a></li>)', r'\1\n    ' + nav_learn, s, count=1, flags=re.S)
        if '<a href="/learn">Learn ads (free)</a>' not in s:
            s = re.sub(r'(<div class="mobile-menu" id="mobile-menu">.*?)(\n  <a href="[^"]*#about">About</a>)',
                       r'\1\n  <a href="/learn">Learn ads (free)</a>\n  <a href="/guides">Guides</a>\2', s, count=1, flags=re.S)
        if s != o:
            open(p, "w", encoding="utf-8").write(s)
    # sitemap
    rows = []
    for p in all_pages():
        u = path_to_url(p)
        s = open(p, encoding="utf-8").read()
        m = re.search(r'<meta name="tms:date" content="(.*?)"', s)
        rows.append(f"  <url><loc>{u}</loc><lastmod>{m.group(1) if m else '2026-11-28'}</lastmod></url>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")
    # llms.txt managed sections
    llms_p = os.path.join(ROOT, "llms.txt")
    llms = open(llms_p, encoding="utf-8").read()
    block = "## Learn (free tutorials)\n- Hub: " + SITE + "/learn\n" + "".join(
        f"- {page_meta('learn', s)['title']}: {SITE}/learn/{s}\n" for s in reg["learn"])
    block += "\n## Guides\n- Hub: " + SITE + "/guides\n" + "".join(
        f"- {page_meta('guide', s)['title']}: {SITE}/{s}\n" for s in reg["guides"])
    block = "<!-- content:start -->\n" + block + "<!-- content:end -->\n"
    if "<!-- content:start -->" in llms:
        llms = re.sub(r"<!-- content:start -->.*?<!-- content:end -->\n", block, llms, flags=re.S)
    else:
        llms = llms.replace("## Contact", block + "\n## Contact")
    open(llms_p, "w", encoding="utf-8").write(llms)
    print("rebuilt hubs, footer/nav on", len(all_pages()), "pages, sitemap, llms.txt")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "page":
        for f in sys.argv[2:]:
            render_page(json.load(open(f, encoding="utf-8")))
    elif len(sys.argv) == 2 and sys.argv[1] == "index":
        rebuild_index()
    else:
        print(__doc__)
