#!/usr/bin/env python3
"""Generates varied sign-in templates for the CagedDragon storefront.

Each template is a self-contained HTML file in plain CSS that reads the repo's
existing --cd-* colorway variables, and embeds the repo's 20-theme selector.
Output: templates/screen_NNN_<slug>/index.html  (+ catalog entries).
"""
import json, re, sys, os, random, html

REPO = sys.argv[1]
OUT_JSON = sys.argv[2]
START = 61

src = open(f"{REPO}/templates/screen_01_pure_minimal/index.html", encoding="utf-8").read()
i = src.index('<script id="cagedragon-colorways">')
j = src.index("</script>", i) + 9
COLORWAY = src[i:j]
PALETTES = json.loads(re.search(r"const palettes = (\[.*?\]);\n", COLORWAY, re.S).group(1))
PAL_IDS = [p["id"] for p in PALETTES]

# ---------------------------------------------------------------- industries
def ico(d):
    return f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'

INDUSTRIES = [
    dict(slug="analytics-saas", name="Analytics SaaS", brand="Quillbase", tag="Product analytics",
         h="Welcome back to Quillbase", s="Sign in to see how your product is performing today.",
         icon=ico('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'), who="your workspace"),
    dict(slug="fintech", name="Fintech", brand="Coinvale", tag="Everyday banking",
         h="Your money, one secure sign-in away", s="Check balances, send payments and track spending.",
         icon=ico('<rect x="2" y="6" width="20" height="13" rx="2"/><path d="M2 10h20M6 15h4"/>'), who="your account"),
    dict(slug="healthcare", name="Healthcare", brand="Carelane", tag="Patient portal",
         h="Access your care in one place", s="View appointments, results and messages from your care team.",
         icon=ico('<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 0 0-7.1 7.1L12 21l8.8-8.3a5 5 0 0 0 0-7.1z"/>'), who="your patient portal"),
    dict(slug="education", name="Education", brand="Lumenhall", tag="Learning campus",
         h="Pick up where you left off", s="Your courses, grades and study groups are waiting.",
         icon=ico('<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5"/>'), who="your campus"),
    dict(slug="ecommerce", name="E-commerce", brand="Cartwell", tag="Member store",
         h="Sign in to your member account", s="Track orders, save favourites and check out faster.",
         icon=ico('<path d="M5 8h14l-1 12H6z"/><path d="M9 8a3 3 0 0 1 6 0"/>'), who="your account"),
    dict(slug="travel", name="Travel", brand="Driftmap", tag="Trip planner",
         h="Your next trip starts here", s="Sign in to see saved routes, bookings and itineraries.",
         icon=ico('<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>'), who="your trips"),
    dict(slug="gaming", name="Gaming", brand="Arenaforge", tag="Esports hub",
         h="Join the match", s="Log in to queue up, track rank and meet your squad.",
         icon=ico('<rect x="2" y="7" width="20" height="11" rx="5"/><path d="M7 10.5v4M5 12.5h4M16 11h.01M18.5 14h.01"/>'), who="your player profile"),
    dict(slug="real-estate", name="Real estate", brand="Homestead Row", tag="Property finder",
         h="Find your next address", s="Sign in to see saved homes and book viewings.",
         icon=ico('<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10M10 20v-6h4v6"/>'), who="your saved homes"),
    dict(slug="restaurant", name="Food & dining", brand="Saltgrain", tag="Dining club",
         h="A table is waiting for you", s="Sign in to manage reservations and your favourite dishes.",
         icon=ico('<path d="M7 3v8M4 3v5a3 3 0 0 0 6 0V3M7 11v10M17 3c-2 2-3 5-3 8h3v10"/>'), who="your reservations"),
    dict(slug="fitness", name="Fitness", brand="Pulseform", tag="Training club",
         h="Time to train", s="Sign in to log workouts and keep your streak alive.",
         icon=ico('<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>'), who="your training log"),
    dict(slug="creative-studio", name="Creative studio", brand="Studio Mono", tag="Client portal",
         h="Review work, leave feedback", s="Sign in to your project space to see the latest drafts.",
         icon=ico('<path d="M4 20l4-1 11-11a2.1 2.1 0 0 0-3-3L5 16z"/><path d="M14 6l3 3"/>'), who="your project space"),
    dict(slug="logistics", name="Logistics", brand="Routewise", tag="Fleet & freight",
         h="Keep every shipment moving", s="Sign in to track loads, drivers and delivery windows.",
         icon=ico('<path d="M2 6h11v10H2zM13 9h5l4 4v3h-9z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>'), who="your fleet"),
    dict(slug="insurance", name="Insurance", brand="Shieldwell", tag="Policy portal",
         h="Your cover, always within reach", s="Sign in to view policies, make claims and download documents.",
         icon=ico('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>'), who="your policies"),
    dict(slug="music", name="Music streaming", brand="Soundloft", tag="Listener hub",
         h="Pick up the playlist", s="Sign in to sync your library, queue and recommendations.",
         icon=ico('<path d="M9 18V6l11-2v12"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>'), who="your library"),
    dict(slug="legal", name="Legal services", brand="Parley & Co", tag="Client portal",
         h="Your matters, securely in one place", s="Sign in to review documents, messages and billing.",
         icon=ico('<path d="M12 3v18M5 7h14M5 7l-3 8a3.5 3.5 0 0 0 6 0zM19 7l-3 8a3.5 3.5 0 0 0 6 0z"/>'), who="your client portal"),
    dict(slug="hr", name="HR & workforce", brand="Peoplehive", tag="Employee self-service",
         h="Everything about work, in one place", s="Sign in for payslips, leave requests and team updates.",
         icon=ico('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M18 14.5a6.5 6.5 0 0 1 3.5 5.5"/>'), who="your workspace"),
    dict(slug="smart-home", name="Smart home / IoT", brand="Signalnest", tag="Device control",
         h="Control your space from anywhere", s="Sign in to manage devices, scenes and schedules.",
         icon=ico('<path d="M5 12a10 10 0 0 1 14 0M8 15a6 6 0 0 1 8 0"/><circle cx="12" cy="18.5" r="1.2"/>'), who="your home"),
    dict(slug="nonprofit", name="Nonprofit", brand="Kindrise", tag="Supporter portal",
         h="Thank you for being here", s="Sign in to manage your giving and see the difference you make.",
         icon=ico('<path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10z"/>'), who="your supporter account"),
    dict(slug="agritech", name="Agritech", brand="Fieldpath", tag="Farm dashboard",
         h="Know your fields, day by day", s="Sign in to check soil, weather and crop activity.",
         icon=ico('<path d="M12 21V8M12 8c0-3 2-5 6-5 0 4-2 6-6 5zM12 13c0-3-2-5-6-5 0 4 2 6 6 5z"/>'), who="your farm"),
    dict(slug="publishing", name="News & publishing", brand="Inkwell Press", tag="Subscriber access",
         h="Read on, wherever you are", s="Sign in to your subscription to continue reading.",
         icon=ico('<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3zM9 8h6M9 12h6M9 16h4"/>'), who="your subscription"),
]

# ------------------------------------------------------------------- skins
FONTS = [
    ("Space Grotesk", "Inter", "sans-serif", "sans-serif"),
    ("Playfair Display", "Inter", "serif", "sans-serif"),
    ("DM Serif Display", "DM Sans", "serif", "sans-serif"),
    ("Sora", "Inter", "sans-serif", "sans-serif"),
    ("Fraunces", "Inter", "serif", "sans-serif"),
    ("Manrope", "Manrope", "sans-serif", "sans-serif"),
    ("Outfit", "Outfit", "sans-serif", "sans-serif"),
    ("Syne", "Inter", "sans-serif", "sans-serif"),
    ("Lora", "Inter", "serif", "sans-serif"),
    ("Bricolage Grotesque", "Inter", "sans-serif", "sans-serif"),
    ("Cormorant Garamond", "Inter", "serif", "sans-serif"),
    ("Poppins", "Poppins", "sans-serif", "sans-serif"),
    ("Plus Jakarta Sans", "Plus Jakarta Sans", "sans-serif", "sans-serif"),
    ("Archivo", "Archivo", "sans-serif", "sans-serif"),
]
RADII = [2, 6, 10, 14, 20, 28]
BORDERS = [1, 1, 1, 2]
SHADOWS = ["none", "0 1px 2px rgb(0 0 0 / .18)", "0 10px 30px rgb(0 0 0 / .22)", "0 24px 60px rgb(0 0 0 / .32)",
           "6px 6px 0 rgb(var(--cd-primary) / .9)"]
PATTERNS = ["none", "grid", "dots", "glow", "stripes", "aurora", "rings"]

def q(s): return html.escape(s, quote=True)

# ------------------------------------------------------------------ pieces
G_SVG = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>'
A_SVG = '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.61-.75 1.04-1.8.92-2.85-.9.04-2 .6-2.65 1.35-.56.64-.97 1.7-.85 2.73 1.01.08 2.04-.51 2.58-1.23z"/></svg>'
GH_SVG = '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.16 19.5c.5.1.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.15-1.1-1.46-1.1-1.46-.9-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.52 2.34 1.08 2.9.83.09-.65.35-1.08.63-1.33-2.22-.25-4.55-1.1-4.55-4.93 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02a9.5 9.5 0 0 1 5 0c1.9-1.29 2.74-1.02 2.74-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85v2.74c0 .27.18.58.69.48A10 10 0 0 0 12 2z"/></svg>'
LOCK = ico('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>')
MAIL = ico('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>')
PHONE = ico('<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>')
KEY = ico('<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M16 7l3 3"/>')
FINGER = ico('<path d="M6 11a6 6 0 0 1 12 0v3M9 20c-1-2-1-4-1-6a4 4 0 0 1 8 0c0 3 .5 5 1.5 7M12 14v3c0 2 .5 3 1 4"/>')
SHIELD = ico('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>')
EYE = ico('<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>')
ARROW = ico('<path d="M5 12h14M13 6l6 6-6 6"/>')


def field(fid, label, typ="text", ph="", icon=None, pw=False, auto=""):
    left = f'<span class="fi">{icon}</span>' if icon else ""
    right = f'<button type="button" class="eye" data-toggle="{fid}" aria-label="Show or hide password">{EYE}</button>' if pw else ""
    cls = " has-i" if icon else ""
    return (f'<div class="field"><label for="{fid}">{label}</label><div class="inp{cls}">{left}'
            f'<input id="{fid}" name="{fid}" type="{typ}" placeholder="{q(ph)}" {auto} required>{right}</div></div>')


def sso(kinds=("g", "a"), cols=2):
    m = {"g": ("Google", G_SVG), "a": ("Apple", A_SVG), "h": ("GitHub", GH_SVG)}
    items = "".join(f'<button type="button" class="btn ghost sso">{m[k][1]}<span>{m[k][0]}</span></button>' for k in kinds)
    return f'<div class="sso-row c{cols}">{items}</div>'


def divider(txt="or continue with email"):
    return f'<div class="divider"><span>{txt}</span></div>'


def pw_form(ind, btn="Sign in", who="Email", remember=True, extra=""):
    rem = ('<label class="chk"><input type="checkbox"><i></i><span>Keep me signed in</span></label>'
           '<a href="#forgot" class="lnk">Forgot password?</a>') if remember else ""
    return (f'<form class="form" onsubmit="return false">{field("em", who, "email", "name@" + ind["brand"].lower().replace(" ", "").replace("&", "") + ".com", MAIL)}'
            f'{field("pw", "Password", "password", "••••••••••", LOCK, True)}'
            f'<div class="row between">{rem}</div>{extra}'
            f'<button class="btn primary" type="submit"><span>{btn}</span>{ARROW}</button></form>')


def logo(ind, size=""):
    return f'<div class="logo {size}"><span class="mark">{ind["icon"]}</span><span class="bn">{q(ind["brand"])}</span></div>'


def foot_signup(ind, txt="New here?", link="Create an account"):
    return f'<p class="foot">{txt} <a href="#create" class="lnk">{link}</a></p>'


def qr(seed, n=25):
    rnd = random.Random(seed)
    cells = []
    def finder(ox, oy):
        for y in range(7):
            for x in range(7):
                on = x in (0, 6) or y in (0, 6) or (2 <= x <= 4 and 2 <= y <= 4)
                if on: cells.append((ox + x, oy + y))
    finder(0, 0); finder(n - 7, 0); finder(0, n - 7)
    for y in range(n):
        for x in range(n):
            if (x < 8 and y < 8) or (x >= n - 8 and y < 8) or (x < 8 and y >= n - 8): continue
            if rnd.random() < .48: cells.append((x, y))
    rects = "".join(f'<rect x="{x}" y="{y}" width="1" height="1"/>' for x, y in cells)
    return f'<svg viewBox="0 0 {n} {n}" class="qr" role="img" aria-label="Sample QR code" shape-rendering="crispEdges" fill="currentColor">{rects}</svg>'


def otp(n=6):
    return '<div class="otp" data-otp>' + "".join(
        f'<input inputmode="numeric" maxlength="1" aria-label="Digit {k + 1}" autocomplete="one-time-code">' for k in range(n)) + '</div>'

# ------------------------------------------------------------------ layouts
# Each returns inner <body> markup. Class vocabulary is defined in BASE_CSS /
# LAYOUT_CSS. Group is the storefront filter category.

def L_centered(ind):
    return f'''<main class="stage center"><section class="card narrow">
{logo(ind)}<h1>{q(ind["h"])}</h1><p class="muted">{q(ind["s"])}</p>
{sso()}{divider()}{pw_form(ind)}{foot_signup(ind)}</section></main>'''

def L_split_left(ind):
    return f'''<main class="split"><aside class="brandpane"><div class="bp-in">{logo(ind)}
<div><p class="eyebrow">{q(ind["tag"])}</p><h2>{q(ind["h"])}</h2><p class="muted">{q(ind["s"])}</p></div>
<ul class="ticks"><li>{SHIELD}<span>Encrypted end to end</span></li><li>{FINGER}<span>Passkeys supported</span></li><li>{KEY}<span>Single sign-on ready</span></li></ul></div></aside>
<section class="formpane"><div class="fp-in"><h1>Sign in</h1><p class="muted">Use your {q(ind["brand"])} credentials.</p>{sso(("g", "a", "h"), 3)}{divider()}{pw_form(ind)}{foot_signup(ind)}</div></section></main>'''

def L_split_right(ind):
    return L_split_left(ind).replace('<main class="split">', '<main class="split rev">')

def L_glass(ind):
    return f'''<main class="stage center glassy"><div class="orb o1"></div><div class="orb o2"></div><section class="card narrow glass">
{logo(ind)}<h1>{q(ind["h"])}</h1><p class="muted">{q(ind["s"])}</p>{pw_form(ind)}{divider("or")}{sso(("g", "a"), 2)}{foot_signup(ind)}</section></main>'''

def L_topnav(ind):
    return f'''<header class="topbar">{logo(ind)}<nav><a href="#help">Help</a><a href="#status">Status</a><a href="#create" class="btn ghost sm">Create account</a></nav></header>
<main class="stage left"><section class="leftcol"><p class="eyebrow">{q(ind["tag"])}</p><h1 class="big">{q(ind["h"])}</h1><p class="muted lead">{q(ind["s"])}</p>
<div class="card flat">{pw_form(ind)}{divider()}{sso(("g", "a", "h"), 3)}</div></section></main>'''

def L_rail(ind):
    return f'''<main class="railwrap"><aside class="rail"><span class="mark">{ind["icon"]}</span><span class="vert">{q(ind["brand"])} · {q(ind["tag"])}</span><span class="dot"></span></aside>
<section class="railform"><div class="fp-in"><h1>{q(ind["h"])}</h1><p class="muted">{q(ind["s"])}</p>{pw_form(ind)}{divider()}{sso()}{foot_signup(ind)}</div></section></main>'''

def L_terminal(ind):
    b = re.sub(r"[^a-z0-9]+", "-", ind["brand"].lower()).strip("-")
    return f'''<main class="stage center"><section class="term"><div class="tbar"><i></i><i></i><i></i><span>{b} — auth</span></div>
<div class="tbody"><p class="muted">$ {b} login --workspace default</p><p class="ok">✓ secure channel established</p><h1>{q(ind["h"])}</h1>
<form class="form" onsubmit="return false">{field("em", "email", "email", "you@" + b + ".dev", None)}{field("pw", "password", "password", "••••••••", None, True)}
<button class="btn primary" type="submit"><span>authenticate</span>{ARROW}</button></form>
<p class="muted">or: <a class="lnk" href="#key">use passkey</a> · <a class="lnk" href="#sso">sso</a> · <a class="lnk" href="#create">create account</a></p></div></section></main>'''

def L_editorial(ind):
    return f'''<main class="edit"><header class="ed-top"><span class="eyebrow">{q(ind["tag"])}</span><span class="muted">Vol. 01 — Member access</span></header>
<div class="ed-grid"><div class="ed-hero"><h1 class="huge">{q(ind["h"])}</h1><p class="muted lead">{q(ind["s"])}</p></div>
<section class="ed-form">{logo(ind)}{pw_form(ind)}{divider()}{sso()}{foot_signup(ind)}</section></div></main>'''

def L_bento(ind):
    return f'''<main class="bento"><div class="tile t-brand">{logo(ind)}<h2>{q(ind["h"])}</h2><p class="muted">{q(ind["s"])}</p></div>
<div class="tile t-form"><h1>Sign in</h1>{pw_form(ind)}{foot_signup(ind)}</div>
<div class="tile t-sso"><p class="eyebrow">Quick access</p>{sso(("g", "a", "h"), 1)}</div>
<div class="tile t-stat"><strong>99.99%</strong><span class="muted">uptime, last 12 months</span></div>
<div class="tile t-pass"><span class="big-ico">{FINGER}</span><p><strong>Passkeys</strong><span class="muted"> sign in with a touch</span></p></div></main>'''

def L_stacked(ind):
    return f'''<main class="stage center"><div class="stack"><div class="layer l3"></div><div class="layer l2"></div>
<section class="card narrow top">{logo(ind)}<h1>{q(ind["h"])}</h1><p class="muted">{q(ind["s"])}</p>{pw_form(ind)}{foot_signup(ind)}</section></div></main>'''

def L_wizard(ind):
    return f'''<main class="wiz"><aside class="steps"><div>{logo(ind)}</div><ol><li class="on" data-s="1"><b>1</b><span>Your email</span></li><li data-s="2"><b>2</b><span>Password</span></li><li data-s="3"><b>3</b><span>Done</span></li></ol><p class="muted">{q(ind["tag"])}</p></aside>
<section class="wizform"><div class="fp-in" data-wizard><div class="pane on" data-p="1"><h1>First, your email</h1><p class="muted">{q(ind["s"])}</p>
{field("em", "Email", "email", "name@" + ind["brand"].lower().replace(" ", "").replace("&", "") + ".com", MAIL)}<button class="btn primary" type="button" data-next>Continue {ARROW}</button></div>
<div class="pane" data-p="2"><h1>Enter your password</h1><p class="muted">Signing in to {q(ind["who"])}.</p>{field("pw", "Password", "password", "••••••••••", LOCK, True)}
<div class="row between"><button class="btn ghost" type="button" data-prev>Back</button><button class="btn primary" type="button" data-next>Sign in {ARROW}</button></div></div>
<div class="pane" data-p="3"><div class="okbig">{SHIELD}</div><h1>You're in</h1><p class="muted">Redirecting to {q(ind["who"])}…</p></div></div></section></main>'''

def L_diagonal(ind):
    return f'''<main class="diag"><div class="dg-art"><div class="dg-in">{logo(ind)}<h2>{q(ind["h"])}</h2><p class="muted">{q(ind["s"])}</p></div></div>
<section class="dg-form"><div class="fp-in">{pw_form(ind)}{divider()}{sso()}{foot_signup(ind)}</div></section></main>'''

# ---- flows
def L_magic(ind):
    return f'''<main class="stage center"><section class="card narrow">{logo(ind)}<span class="badge">{MAIL}</span><h1>Sign in with a magic link</h1>
<p class="muted">Enter your email and we'll send a one-time link to {q(ind["who"])}. No password needed.</p>
<form class="form" onsubmit="return false">{field("em", "Email", "email", "name@" + ind["brand"].lower().replace(" ", "").replace("&", "") + ".com", MAIL)}
<button class="btn primary" type="submit"><span>Email me a link</span>{ARROW}</button></form>
<p class="foot">Prefer a password? <a class="lnk" href="#pw">Use password instead</a></p></section></main>'''

def L_otp(ind):
    return f'''<main class="stage center"><section class="card narrow">{logo(ind)}<span class="badge">{PHONE}</span><h1>Enter your 6-digit code</h1>
<p class="muted">We sent a code to <b>+00 •••• ••42</b>. It expires in 10 minutes.</p>
<form class="form" onsubmit="return false">{otp()}<button class="btn primary" type="submit"><span>Verify and continue</span>{ARROW}</button></form>
<p class="foot">Didn't get it? <a class="lnk" href="#resend">Resend code</a> · <a class="lnk" href="#change">Change number</a></p></section></main>'''

def L_passkey(ind):
    return f'''<main class="stage center"><section class="card narrow center-t">{logo(ind)}<div class="bigicon">{FINGER}</div><h1>Sign in with your passkey</h1>
<p class="muted">Use your fingerprint, face or device PIN. Nothing to remember, nothing to phish.</p>
<button class="btn primary" type="button"><span>Continue with passkey</span>{ARROW}</button>{divider("other ways")}
<div class="alt"><a class="lnk" href="#pw">Password</a><a class="lnk" href="#magic">Email link</a><a class="lnk" href="#sso">SSO</a></div></section></main>'''

def L_qr(ind, seed=1):
    return f'''<main class="stage center"><section class="card wide qrcard"><div class="qr-l">{logo(ind)}<h1>Scan to sign in</h1><p class="muted">Open the {q(ind["brand"])} app, tap <b>Scan</b> and point your camera at the code.</p>
<ol class="how"><li><b>1</b> Open the app on your phone</li><li><b>2</b> Go to Settings → Devices</li><li><b>3</b> Scan this code</li></ol></div>
<div class="qr-r"><div class="qrbox">{qr(seed)}</div><a class="lnk" href="#pw">Use email instead</a></div></section></main>'''

def L_social(ind):
    return f'''<main class="stage center"><section class="card narrow">{logo(ind)}<h1>Choose how to sign in</h1><p class="muted">{q(ind["s"])}</p>
<div class="stackbtn"><button class="btn ghost sso big" type="button">{G_SVG}<span>Continue with Google</span></button><button class="btn ghost sso big" type="button">{A_SVG}<span>Continue with Apple</span></button>
<button class="btn ghost sso big" type="button">{GH_SVG}<span>Continue with GitHub</span></button><button class="btn ghost sso big" type="button">{KEY}<span>Continue with SSO</span></button></div>
<p class="foot small muted">By continuing you agree to the <a class="lnk" href="#terms">Terms</a> and <a class="lnk" href="#privacy">Privacy Policy</a>.</p></section></main>'''

def L_2fa(ind):
    return f'''<main class="stage center"><section class="card narrow">{logo(ind)}<span class="badge">{SHIELD}</span><h1>Two-step verification</h1>
<p class="muted">Open your authenticator app and enter the 6-digit code for <b>{q(ind["brand"])}</b>.</p>
<form class="form" onsubmit="return false">{otp()}<label class="chk"><input type="checkbox"><i></i><span>Trust this device for 30 days</span></label>
<button class="btn primary" type="submit"><span>Verify</span>{ARROW}</button></form><p class="foot"><a class="lnk" href="#backup">Use a backup code</a></p></section></main>'''

def L_reset(ind):
    return f'''<main class="stage center"><section class="card narrow">{logo(ind)}<span class="badge">{KEY}</span><h1>Reset your password</h1>
<p class="muted">Enter the email for {q(ind["who"])} and we'll send reset instructions.</p>
<form class="form" onsubmit="return false">{field("em", "Email", "email", "name@" + ind["brand"].lower().replace(" ", "").replace("&", "") + ".com", MAIL)}
<button class="btn primary" type="submit"><span>Send reset link</span>{ARROW}</button></form><p class="foot"><a class="lnk" href="#back">← Back to sign in</a></p></section></main>'''

def L_signup(ind):
    return f'''<main class="stage center"><section class="card narrow">{logo(ind)}<h1>Create your account</h1><p class="muted">Join {q(ind["brand"])} — it takes less than a minute.</p>
<form class="form" onsubmit="return false"><div class="two">{field("fn", "First name", "text", "Alex")}{field("ln", "Last name", "text", "Rivera")}</div>
{field("em", "Email", "email", "name@" + ind["brand"].lower().replace(" ", "").replace("&", "") + ".com", MAIL)}{field("pw", "Password", "password", "At least 10 characters", LOCK, True)}
<div class="meter"><i></i><i></i><i></i><i></i></div><label class="chk"><input type="checkbox"><i></i><span>I agree to the Terms and Privacy Policy</span></label>
<button class="btn primary" type="submit"><span>Create account</span>{ARROW}</button></form><p class="foot">Already a member? <a class="lnk" href="#in">Sign in</a></p></section></main>'''

def L_sheet(ind):
    return f'''<main class="phonewrap"><div class="phone"><div class="ph-top">{logo(ind)}<p class="muted">{q(ind["tag"])}</p><div class="ph-art">{ind["icon"]}</div></div>
<section class="sheet"><i class="grab"></i><h1>Welcome back</h1><p class="muted">{q(ind["s"])}</p>{pw_form(ind, "Sign in", "Email", False)}<p class="foot">{ "New here?" } <a class="lnk" href="#create">Create account</a></p></section></div></main>'''

def L_split_hero_form(ind):  # form over full-bleed art, form on the right in a panel
    return f'''<main class="hero"><div class="hero-art"><div class="hero-t">{logo(ind)}<h2>{q(ind["h"])}</h2></div></div>
<section class="card hero-card"><h1>Sign in</h1><p class="muted">{q(ind["s"])}</p>{pw_form(ind)}{divider()}{sso()}{foot_signup(ind)}</section></main>'''

def L_minimal_line(ind):  # underline inputs, very airy
    return f'''<main class="stage center airy"><section class="plain">{logo(ind)}<h1>{q(ind["h"])}</h1>
<form class="form line" onsubmit="return false">{field("em", "Email", "email", "name@" + ind["brand"].lower().replace(" ", "").replace("&", "") + ".com")}{field("pw", "Password", "password", "••••••••••", None, True)}
<div class="row between"><a class="lnk" href="#forgot">Forgot password?</a><button class="btn primary pill" type="submit"><span>Continue</span>{ARROW}</button></div></form>{foot_signup(ind)}</section></main>'''


def L_dual(ind):
    return f"""<main class="stage center"><div class="duo"><section class="card"><h1>Welcome back</h1><p class="muted">Sign in to {q(ind["who"])}.</p>{pw_form(ind)}</section>
<section class="card alt2"><span class="eyebrow">New to {q(ind["brand"])}?</span><h2>Create your account</h2><p class="muted">{q(ind["s"])}</p>
<ul class="ticks"><li>{SHIELD}<span>Set up in under a minute</span></li><li>{FINGER}<span>Passkeys supported</span></li><li>{KEY}<span>Cancel any time</span></li></ul>
<a class="btn ghost" href="#create"><span>Get started</span>{ARROW}</a></section></div></main>"""

def L_cover(ind):
    return f"""<main class="stage center"><section class="card narrow nopad"><div class="cover"><span class="cv-ico">{ind["icon"]}</span><span class="cv-b">{q(ind["brand"])}</span><span class="cv-t">{q(ind["tag"])}</span></div>
<div class="cv-body"><h1>{q(ind["h"])}</h1><p class="muted">{q(ind["s"])}</p>{pw_form(ind)}{foot_signup(ind)}</div></section></main>"""

def L_workspace(ind):
    dom = ind["brand"].lower().replace(" ", "").replace("&", "")
    return f"""<main class="stage center"><section class="card narrow">{logo(ind)}<h1>Find your workspace</h1><p class="muted">Enter your team's address to continue to {q(ind["who"])}.</p>
<form class="form" onsubmit="return false"><div class="field"><label for="ws">Workspace address</label><div class="ws"><input id="ws" placeholder="your-team" required><span>.{dom}.com</span></div></div>
<button class="btn primary" type="submit"><span>Continue</span>{ARROW}</button></form><p class="foot">Not sure? <a class="lnk" href="#find">Find my workspaces</a></p></section></main>"""

def L_accounts(ind):
    dom = ind["brand"].lower().replace(" ", "").replace("&", "")
    rows = [("AR", "Alex Rivera", "alex@" + dom + ".com"), ("JP", "Jordan Patel", "jordan@" + dom + ".com")]
    items = "".join(f'<button type="button" class="acct"><span class="av">{a}</span><span class="who"><b>{n}</b><small>{e}</small></span>{ARROW}</button>' for a, n, e in rows)
    return f"""<main class="stage center"><section class="card narrow">{logo(ind)}<h1>Choose an account</h1><p class="muted">to continue to {q(ind["brand"])}</p>
<div class="accts">{items}<button type="button" class="acct add"><span class="av">+</span><span class="who"><b>Use another account</b></span></button></div>
<p class="foot small muted">Only accounts used on this device are shown.</p></section></main>"""

def L_pin(ind):
    keys = "".join(f'<button type="button" data-k="{k}">{k}</button>' for k in "123456789")
    return f"""<main class="phonewrap"><div class="pinbox" data-pin>{logo(ind)}<span class="badge">{LOCK}</span><h1>Enter your PIN</h1><p class="muted">Unlock {q(ind["who"])} on this device.</p>
<div class="dots" aria-label="PIN progress"><i></i><i></i><i></i><i></i></div>
<div class="pad">{keys}<button type="button" class="soft" aria-label="Use fingerprint">{FINGER}</button><button type="button" data-k="0">0</button><button type="button" class="soft" data-k="del" aria-label="Delete">⌫</button></div>
<a class="lnk small" href="#forgot">Forgot PIN?</a></div></main>"""

def L_admin(ind):
    return f"""<main class="stage center"><section class="card narrow"><div class="envbar"><span class="envpill">● Production</span><span class="muted">Region · ap-south-1</span></div>{logo(ind)}
<h1>Administrator sign-in</h1><p class="muted">Restricted to authorised staff. Activity on this page is logged.</p>
<form class="form" onsubmit="return false">{field("org", "Organisation domain", "text", "yourcompany.com", MAIL)}<button class="btn primary" type="submit"><span>Continue with SSO</span>{ARROW}</button></form>
{divider("or")}<button class="btn ghost big" type="button" style="margin-top:18px">{KEY}<span>Use email and security key</span></button></section></main>"""

def L_testimonial(ind):
    return f"""<main class="split"><aside class="brandpane"><div class="bp-in">{logo(ind)}
<figure class="quote"><blockquote>“Replace this with a short, real customer quote about how easy {q(ind["brand"])} is to use.”</blockquote>
<figcaption><span class="av">AB</span><span><b>[Customer name]</b><small>[Role, Company]</small></span></figcaption></figure>
<p class="eyebrow">{q(ind["tag"])}</p></div></aside>
<section class="formpane"><div class="fp-in"><h1>{q(ind["h"])}</h1><p class="muted">{q(ind["s"])}</p>{pw_form(ind)}{divider()}{sso()}{foot_signup(ind)}</div></section></main>"""

def L_strip(ind):
    return f"""<main class="stripwrap"><header class="topbar flat">{logo(ind)}<a class="lnk" href="#help">Need help?</a></header>
<div class="strip-hero"><p class="eyebrow">{q(ind["tag"])}</p><h1 class="huge">{q(ind["h"])}</h1>
<form class="strip" onsubmit="return false">{field("em", "Email", "email", "name@" + ind["brand"].lower().replace(" ", "").replace("&", "") + ".com", MAIL)}{field("pw", "Password", "password", "••••••••••", LOCK, True)}
<button class="btn primary" type="submit"><span>Sign in</span>{ARROW}</button></form>
<p class="muted">{q(ind["s"])} <a class="lnk" href="#create">Create an account</a></p></div></main>"""

def L_device(ind):
    return f"""<main class="stage center"><section class="card narrow">{logo(ind)}<span class="badge">{SHIELD}</span><h1>Confirm it's you</h1><p class="muted">We noticed a sign-in to {q(ind["who"])} from a new device.</p>
<dl class="devbox"><div><dt>Device</dt><dd>Chrome on macOS</dd></div><div><dt>Location</dt><dd>Chennai, India</dd></div><div><dt>Time</dt><dd>Just now</dd></div></dl>
<div class="stackbtn"><button class="btn primary" type="button"><span>Yes, it's me</span>{ARROW}</button><button class="btn ghost" type="button">No, secure my account</button></div></section></main>"""

LAYOUTS = [
    ("Centered Card", "Visual styles", L_centered, "A focused centered card with social sign-in and a clean password form."),
    ("Left Brand Panel", "Visual styles", L_split_left, "A brand panel on the left with trust points, and the sign-in form on the right."),
    ("Right Brand Panel", "Visual styles", L_split_right, "The sign-in form on the left, with a brand panel and trust points on the right."),
    ("Glass Orbs", "Visual styles", L_glass, "A frosted glass card floating over soft glowing orbs."),
    ("Top Nav Hero", "Visual styles", L_topnav, "A top navigation bar with a large headline and a flat form card."),
    ("Vertical Rail", "Visual styles", L_rail, "A slim vertical brand rail beside a generous sign-in column."),
    ("Terminal Console", "Visual styles", L_terminal, "A command-line inspired login for developer products."),
    ("Editorial Masthead", "Visual styles", L_editorial, "A magazine-style masthead with an oversized headline and ruled form."),
    ("Bento Grid", "Visual styles", L_bento, "A modular bento layout where the form sits among trust and passkey tiles."),
    ("Stacked Layers", "Visual styles", L_stacked, "A card with offset layers behind it for a tactile, paper-stack look."),
    ("Diagonal Split", "Visual styles", L_diagonal, "A diagonal cut separates the brand art from the sign-in form."),
    ("Hero Overlay", "Visual styles", L_split_hero_form, "A full-height hero with a sign-in panel overlapping it."),
    ("Airy Underline", "Visual styles", L_minimal_line, "Ultra-minimal underline fields with plenty of whitespace."),
    ("Step by Step", "Authentication flows", L_wizard, "A guided multi-step sign-in with a progress sidebar."),
    ("Magic Link", "Authentication flows", L_magic, "Passwordless sign-in with a one-time email link."),
    ("Phone Code", "Authentication flows", L_otp, "Verify with a six-digit code sent to a phone number."),
    ("Passkey First", "Authentication flows", L_passkey, "Lead with passkeys and keep other methods one tap away."),
    ("QR Sign-in", "Authentication flows", L_qr, "Scan a QR code from the mobile app to sign in on desktop."),
    ("Social Only", "Authentication flows", L_social, "A stack of large single-tap provider buttons."),
    ("Two-Step Verify", "Authentication flows", L_2fa, "Authenticator code entry with a trust-this-device option."),
    ("Reset Password", "Authentication flows", L_reset, "A calm password reset request screen."),
    ("Create Account", "Authentication flows", L_signup, "A sign-up form with a live password strength meter."),
    ("Mobile Sheet", "Authentication flows", L_sheet, "A phone-framed screen with a bottom sheet sign-in."),
    ("Returning or New", "Visual styles", L_dual, "Two side-by-side cards: sign in for returning users, a clear invitation for new ones."),
    ("Cover Header Card", "Visual styles", L_cover, "A card topped with a branded cover band, then a compact sign-in form."),
    ("Workspace Finder", "Authentication flows", L_workspace, "Ask for the workspace address first, then continue to sign in."),
    ("Account Chooser", "Authentication flows", L_accounts, "Pick from accounts already used on this device."),
    ("PIN Pad", "Authentication flows", L_pin, "A four-digit PIN keypad with fingerprint shortcut for quick unlock."),
    ("Admin Console", "Visual styles", L_admin, "An administrator sign-in with environment badge and SSO-first flow."),
    ("Testimonial Split", "Visual styles", L_testimonial, "A customer-quote panel beside the sign-in form (placeholder quote to replace)."),
    ("Inline Strip", "Visual styles", L_strip, "A big headline with the whole sign-in on one horizontal row."),
    ("New Device Check", "Authentication flows", L_device, "Confirm a sign-in from an unrecognised device with approve and deny actions."),
]

# ------------------------------------------------------------------- css
BASE_CSS = r"""
*{box-sizing:border-box;margin:0}
:root{--bg:rgb(var(--cd-background));--sf:rgb(var(--cd-surface));--lo:rgb(var(--cd-surface-container-low));--ct:rgb(var(--cd-surface-container));
--hi:rgb(var(--cd-surface-container-high));--hx:rgb(var(--cd-surface-container-highest));--lw:rgb(var(--cd-surface-container-lowest));
--tx:rgb(var(--cd-on-surface));--tv:rgb(var(--cd-on-surface-variant));--ol:rgb(var(--cd-outline));--ov:rgb(var(--cd-outline-variant));
--pr:rgb(var(--cd-primary));--pc:rgb(var(--cd-primary-container));--op:rgb(var(--cd-on-primary));--se:rgb(var(--cd-secondary));--te:rgb(var(--cd-tertiary));
--pl:color-mix(in srgb,var(--pr) 62%,var(--tx));--pa:rgb(var(--cd-primary) / .16);--ta:rgb(var(--cd-tertiary) / .14);--sa:rgb(var(--cd-secondary) / .16);
--r:__R__px;--bw:__BW__px;--sh:__SH__;--hf:__HF__;--bf:__BF__}
html,body{min-height:100%}
body{font-family:var(--bf);background:var(--bg);color:var(--tx);-webkit-font-smoothing:antialiased;line-height:1.5;font-size:15px;position:relative;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;__PATTERN__}
main,header{position:relative;z-index:1}
html:not(.ready) *,html:not(.ready) *::before,html:not(.ready) *::after{transition:none!important}
h1,h2,.bn{font-family:var(--hf);letter-spacing:-.01em;line-height:1.12}
h1{font-size:28px;font-weight:__HW__;margin-bottom:8px}
h2{font-size:32px;font-weight:__HW__;margin:10px 0}
.big{font-size:clamp(36px,5vw,58px)}.huge{font-size:clamp(44px,7vw,92px);font-weight:__HW__}
.muted{color:var(--tv)}.lead{font-size:18px;max-width:46ch}
.eyebrow{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--pl);font-weight:700}
a{color:inherit}.lnk{color:var(--pl);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px;font-weight:600}.lnk:hover{text-decoration-thickness:2px}
.logo{display:flex;align-items:center;gap:10px;margin-bottom:22px}.logo .bn{font-weight:700;font-size:18px}
.mark{width:38px;height:38px;border-radius:calc(var(--r) * .8);background:var(--pr);color:var(--op);display:grid;place-items:center;flex:none}
.logo.lg .mark{width:48px;height:48px}
.card{background:var(--lo);border:var(--bw) solid var(--ov);border-radius:var(--r);padding:34px;box-shadow:var(--sh);width:100%}
.card.narrow{max-width:440px}.card.wide{max-width:820px}.card.flat{box-shadow:none;background:var(--ct)}
.form{display:flex;flex-direction:column;gap:16px;margin-top:22px}
.field label{display:block;font-size:12px;font-weight:600;margin-bottom:6px;color:var(--tx)}
.inp{position:relative;display:flex;align-items:center}
.inp input{width:100%;height:48px;padding:0 14px;background:var(--ct);color:var(--tx);border:var(--bw) solid var(--ol);border-radius:calc(var(--r) * .7);font:inherit;font-size:15px;outline:none;transition:border-color .15s,box-shadow .15s}
.inp input::placeholder{color:var(--tv);opacity:.85}
.inp input:focus{border-color:var(--pr);box-shadow:0 0 0 3px var(--pa)}
.inp.has-i input{padding-left:44px}.inp .fi{position:absolute;left:13px;color:var(--tv);display:grid;pointer-events:none}.inp .fi svg{width:19px;height:19px}
.inp .eye{position:absolute;right:6px;width:40px;height:40px;border:0;background:none;color:var(--ol);cursor:pointer;display:grid;place-items:center;border-radius:8px}
.inp .eye:hover{color:var(--tx)}.inp .eye svg{width:19px;height:19px}.inp:has(.eye) input{padding-right:48px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;height:48px;padding:0 20px;border-radius:calc(var(--r) * .7);font:inherit;font-weight:700;font-size:15px;cursor:pointer;border:var(--bw) solid transparent;transition:transform .12s,filter .15s,background .15s}
.btn svg{width:18px;height:18px}.btn:active{transform:translateY(1px)}
.btn.primary{background:var(--pr);color:var(--op);width:100%}.btn.primary:hover{filter:brightness(1.08)}
.btn.ghost{background:transparent;color:var(--tx);border-color:var(--ov)}.btn.ghost:hover{background:var(--ct);border-color:var(--ol)}
.btn.sm{height:38px;padding:0 14px;font-size:13px}.btn.pill{border-radius:999px;width:auto}.btn.big{width:100%;justify-content:flex-start;padding:0 18px}
.sso-row{display:grid;gap:10px;margin-top:22px}.sso-row.c1{grid-template-columns:1fr}.sso-row.c2{grid-template-columns:1fr 1fr}.sso-row.c3{grid-template-columns:repeat(3,1fr)}
.sso span{font-size:14px}.sso-row.c3 .sso span{font-size:13px}.sso-row.c3 .sso{padding:0 8px}
.divider{display:flex;align-items:center;gap:12px;margin:22px 0 0;color:var(--tv);font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.divider::before,.divider::after{content:"";height:1px;background:var(--ov);flex:1}
.row{display:flex;align-items:center;gap:12px}.row.between{justify-content:space-between}
.chk{display:flex;align-items:center;gap:9px;font-size:13px;color:var(--tv);cursor:pointer}
.chk input{position:absolute;opacity:0}.chk i{width:18px;height:18px;border:var(--bw) solid var(--ol);border-radius:5px;display:grid;place-items:center;flex:none}
.chk input:checked+i{background:var(--pr);border-color:var(--pr)}.chk input:checked+i::after{content:"";width:9px;height:5px;border-left:2px solid var(--op);border-bottom:2px solid var(--op);transform:rotate(-45deg) translate(1px,-1px)}
.chk input:focus-visible+i{box-shadow:0 0 0 3px var(--pa)}
.foot{margin-top:22px;text-align:center;font-size:14px;color:var(--tv)}.foot.small{font-size:12px}
.badge,.bigicon{display:grid;place-items:center;background:var(--pa);color:var(--pl);border-radius:calc(var(--r) * .9)}
.badge{width:48px;height:48px;margin-bottom:16px}.badge svg{width:24px;height:24px}
.bigicon{width:84px;height:84px;margin:6px auto 20px;border-radius:50%}.bigicon svg{width:40px;height:40px}
.center-t{text-align:center}.center-t .logo{justify-content:center}.center-t .btn{margin-top:22px}
.alt{display:flex;justify-content:center;gap:22px;margin-top:20px;font-size:14px}
.stage{min-height:100vh;display:flex;padding:32px 20px}.stage.center{align-items:center;justify-content:center}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.otp{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
.otp input{height:58px;text-align:center;font:700 24px var(--hf);background:var(--ct);color:var(--tx);border:var(--bw) solid var(--ov);border-radius:calc(var(--r) * .7);outline:none;min-width:0;width:100%}
.otp input:focus{border-color:var(--pr);box-shadow:0 0 0 3px var(--pa)}
.meter{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:-6px}.meter i{height:5px;border-radius:9px;background:var(--hx)}.meter i:nth-child(-n+2){background:var(--se)}
.stackbtn{display:flex;flex-direction:column;gap:10px;margin-top:24px}
.qr{width:100%;height:100%;display:block}
/* ---- layouts ---- */
.split{min-height:100vh;display:grid;grid-template-columns:1.05fr 1fr}.split.rev .brandpane{order:2}
.brandpane{background:linear-gradient(160deg,var(--pc),var(--lw) 78%);display:flex;padding:48px}
.bp-in{display:flex;flex-direction:column;justify-content:space-between;gap:36px;width:100%;max-width:520px;margin:0 auto}
.brandpane h2{font-size:clamp(30px,3.4vw,46px)}.ticks{list-style:none;padding:0;display:grid;gap:14px}
.ticks li{display:flex;align-items:center;gap:12px;color:var(--tx);font-weight:500}.ticks svg{width:20px;height:20px;color:var(--te)}
.formpane,.railform,.dg-form,.wizform{display:flex;align-items:center;justify-content:center;padding:40px 24px}
.fp-in{width:100%;max-width:410px}
.glassy .card.glass{background:rgb(var(--cd-surface) / .55);backdrop-filter:blur(22px) saturate(1.3);border-color:rgb(var(--cd-on-surface) / .14)}
.glassy{overflow:hidden}.orb{position:absolute;border-radius:50%;filter:blur(70px);opacity:.55;pointer-events:none}.o1{width:420px;height:420px;background:var(--pr);top:6%;left:12%}.o2{width:360px;height:360px;background:var(--te);bottom:4%;right:14%}
.topbar{display:flex;align-items:center;justify-content:space-between;padding:18px 40px;border-bottom:1px solid var(--ov)}.topbar .logo{margin:0}.topbar nav{display:flex;align-items:center;gap:22px;font-size:14px;color:var(--tv)}.topbar nav a{text-decoration:none}
.stage.left{min-height:calc(100vh - 75px);align-items:center}.leftcol{max-width:1080px;margin:0 auto;width:100%;display:grid;grid-template-columns:1.2fr 1fr;gap:56px;align-items:center}
.leftcol .eyebrow,.leftcol .big,.leftcol .lead{grid-column:1}.leftcol .card{grid-column:2;grid-row:1/span 3}
.railwrap{min-height:100vh;display:grid;grid-template-columns:84px 1fr}.rail{background:var(--pr);color:var(--op);display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:26px 0}
.rail .mark{background:var(--op);color:var(--pr)}.vert{writing-mode:vertical-rl;transform:rotate(180deg);font-size:12px;letter-spacing:.2em;text-transform:uppercase;font-weight:700}.rail .dot{width:10px;height:10px;border-radius:50%;background:var(--op)}
.term{width:100%;max-width:600px;background:var(--lw);border:var(--bw) solid var(--ov);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh);font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace}
.tbar{display:flex;align-items:center;gap:7px;padding:12px 16px;background:var(--ct);border-bottom:1px solid var(--ov);font-size:12px;color:var(--tv)}.tbar i{width:11px;height:11px;border-radius:50%;background:var(--ol)}.tbar i:first-child{background:var(--se)}.tbar span{margin-left:10px}
.tbody{padding:26px;display:grid;gap:12px;font-size:14px}.tbody h1{font-family:inherit;font-size:22px;margin:10px 0 0}.tbody .ok{color:var(--te)}.tbody .form{margin-top:6px}.tbody input{font-family:inherit}
.edit{min-height:100vh;padding:28px 48px 48px;max-width:1240px;margin:0 auto}.ed-top{display:flex;justify-content:space-between;border-bottom:2px solid var(--tx);padding-bottom:12px;font-size:13px}
.ed-grid{display:grid;grid-template-columns:1.4fr 1fr;gap:56px;margin-top:44px;align-items:start}.ed-hero .lead{margin-top:22px}.ed-form{border-top:var(--bw) solid var(--tx);padding-top:22px}
.bento{min-height:100vh;padding:28px;display:grid;gap:14px;max-width:1180px;margin:0 auto;grid-template-columns:repeat(4,1fr);grid-template-rows:auto auto auto;align-content:center}
.tile{background:var(--lo);border:var(--bw) solid var(--ov);border-radius:var(--r);padding:26px;box-shadow:var(--sh)}
.t-brand{grid-column:1/3;grid-row:1/3;background:linear-gradient(150deg,var(--pc),var(--lo));display:flex;flex-direction:column;justify-content:flex-end}.t-brand h2{font-size:38px}
.t-form{grid-column:3/5;grid-row:1/3}.t-sso{grid-column:1/2;grid-row:3}.t-stat{grid-column:2/3;grid-row:3;display:flex;flex-direction:column;justify-content:center}.t-stat strong{font:700 34px var(--hf);color:var(--te)}
.t-pass{grid-column:3/5;grid-row:3;display:flex;align-items:center;gap:16px;background:var(--pa)}.big-ico{width:52px;height:52px;display:grid;place-items:center;background:var(--pr);color:var(--op);border-radius:50%;flex:none}.big-ico svg{width:26px;height:26px}
.t-sso .sso-row{margin-top:10px}.t-sso .btn{height:40px;padding:0 10px}
.stack{position:relative;width:100%;max-width:440px}.layer{position:absolute;inset:0;border-radius:var(--r);border:var(--bw) solid var(--ov)}
.l3{background:var(--hx);transform:translate(26px,26px) rotate(2.2deg)}.l2{background:var(--hi);transform:translate(13px,13px) rotate(-1.4deg)}.stack .top{position:relative}
.wiz{min-height:100vh;display:grid;grid-template-columns:320px 1fr}.steps{background:var(--lw);border-right:1px solid var(--ov);padding:36px 32px;display:flex;flex-direction:column;justify-content:space-between}
.steps ol{list-style:none;padding:0;display:grid;gap:22px}.steps li{display:flex;align-items:center;gap:14px;color:var(--tv)}.steps li b{width:32px;height:32px;border-radius:50%;border:var(--bw) solid var(--ol);display:grid;place-items:center;font-size:13px}
.steps li.on{color:var(--tx);font-weight:700}.steps li.on b,.steps li.done b{background:var(--pr);border-color:var(--pr);color:var(--op)}.steps li.done{color:var(--tx)}
.pane{display:none;gap:18px;flex-direction:column}.pane.on{display:flex}.pane .btn.primary{margin-top:6px}.pane .btn.ghost{width:auto}.pane .row .btn.primary{width:auto;flex:1;margin:0}.okbig{width:72px;height:72px;border-radius:50%;background:var(--pa);color:var(--pr);display:grid;place-items:center}.okbig svg{width:36px;height:36px}
.diag{min-height:100vh;position:relative;display:grid;grid-template-columns:1fr 1fr}.dg-art{background:linear-gradient(145deg,var(--pc),var(--lw));clip-path:polygon(0 0,100% 0,82% 100%,0 100%);display:flex;align-items:center;padding:48px 14% 48px 48px;grid-column:1/2}
.dg-in{max-width:440px}.dg-in h2{font-size:clamp(30px,3.4vw,46px)}.dg-form{grid-column:2/3}
.hero{min-height:100vh;position:relative;display:flex;align-items:center;justify-content:flex-end;padding:40px 6vw}.hero-art{position:absolute;inset:0;background:radial-gradient(900px 600px at 20% 30%,var(--pc),transparent 70%),linear-gradient(160deg,var(--lw),var(--bg))}
.hero-t{position:absolute;left:6vw;top:50%;transform:translateY(-50%);max-width:480px}.hero-t h2{font-size:clamp(34px,4vw,58px)}.hero-card{position:relative;max-width:440px}
.airy .plain{width:100%;max-width:520px}.airy h1{font-size:40px;margin-bottom:6px}.form.line{gap:26px}.form.line .inp input{background:transparent;border:0;border-bottom:var(--bw) solid var(--ol);border-radius:0;padding:0 2px;height:44px}
.form.line .inp input:focus{box-shadow:none;border-bottom-color:var(--pr)}.form.line .eye{right:0}
.qrcard{display:grid;grid-template-columns:1.2fr 1fr;gap:44px;align-items:center}.how{list-style:none;padding:0;display:grid;gap:12px;margin-top:22px}.how li{display:flex;gap:12px;align-items:center;font-size:14px}.how b{width:26px;height:26px;border-radius:50%;background:var(--pa);color:var(--pr);display:grid;place-items:center;font-size:12px;flex:none}
.qr-r{display:grid;gap:16px;justify-items:center;text-align:center}.qrbox{width:100%;max-width:240px;aspect-ratio:1;padding:16px;background:#fff;color:#111;border-radius:var(--r);box-shadow:var(--sh)}
.phonewrap{min-height:100vh;display:grid;place-items:center;padding:28px}.phone{width:min(380px,100%);height:760px;max-height:calc(100vh - 56px);border-radius:44px;border:8px solid var(--hx);background:var(--lw);overflow:hidden;position:relative;box-shadow:var(--sh)}
.ph-top{padding:44px 30px;text-align:left}.ph-art{width:120px;height:120px;margin:34px auto 0;display:grid;place-items:center;background:var(--pa);color:var(--pr);border-radius:50%}.ph-art svg{width:56px;height:56px}
.sheet{position:absolute;left:0;right:0;bottom:0;background:var(--lo);border-top:1px solid var(--ov);border-radius:30px 30px 0 0;padding:14px 26px 28px;box-shadow:0 -14px 40px rgb(0 0 0 / .25)}.sheet h1{font-size:24px}.grab{display:block;width:44px;height:5px;border-radius:9px;background:var(--ol);margin:0 auto 18px;opacity:.6}
.sheet .form{gap:12px;margin-top:14px}.sheet .foot{margin-top:14px}.sheet .inp input,.sheet .btn{height:46px}
@media(max-width:860px){.stack{max-width:calc(100% - 28px);margin-right:28px}.phonewrap{padding:20px 12px}.split,.diag,.wiz{grid-template-columns:1fr}.brandpane,.dg-art{display:none}.split.rev .brandpane{order:0}.leftcol{grid-template-columns:1fr}.leftcol .card{grid-column:1;grid-row:auto}
.ed-grid,.qrcard{grid-template-columns:1fr}.bento{grid-template-columns:1fr 1fr}.t-brand,.t-form,.t-pass{grid-column:1/-1;grid-row:auto}.t-sso,.t-stat{grid-column:auto;grid-row:auto}.steps{display:none}.hero{justify-content:center}.hero-t{display:none}
.edit{padding:20px}.topbar{padding:14px 20px}.topbar nav a:not(.btn){display:none}.card{padding:26px}.sso-row.c3{grid-template-columns:1fr}.railwrap{grid-template-columns:56px 1fr}}
"""

PATTERN_CSS = {
    "none": "",
    "grid": "background-image:linear-gradient(rgb(var(--cd-outline-variant) / .35) 1px,transparent 1px),linear-gradient(90deg,rgb(var(--cd-outline-variant) / .35) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(ellipse at center,#000 30%,transparent 80%);-webkit-mask-image:radial-gradient(ellipse at center,#000 30%,transparent 80%);",
    "dots": "background-image:radial-gradient(rgb(var(--cd-outline) / .45) 1.2px,transparent 1.4px);background-size:24px 24px;mask-image:radial-gradient(ellipse at center,#000 25%,transparent 78%);-webkit-mask-image:radial-gradient(ellipse at center,#000 25%,transparent 78%);",
    "glow": "background:radial-gradient(700px 420px at 12% 8%,rgb(var(--cd-primary) / .22),transparent 70%),radial-gradient(640px 400px at 92% 96%,rgb(var(--cd-tertiary) / .18),transparent 70%);",
    "stripes": "background:repeating-linear-gradient(135deg,rgb(var(--cd-outline-variant) / .22) 0 2px,transparent 2px 22px);",
    "aurora": "background:conic-gradient(from 210deg at 70% 20%,rgb(var(--cd-primary) / .20),rgb(var(--cd-tertiary) / .16),rgb(var(--cd-secondary) / .14),rgb(var(--cd-primary) / .20));filter:blur(60px);opacity:.8;",
    "rings": "background:repeating-radial-gradient(circle at 80% 15%,transparent 0 46px,rgb(var(--cd-outline-variant) / .32) 46px 47px);",
}

JS = r"""
document.querySelectorAll('[data-toggle]').forEach(function(b){b.addEventListener('click',function(){var i=document.getElementById(b.dataset.toggle);i.type=i.type==='password'?'text':'password';});});
document.querySelectorAll('[data-otp]').forEach(function(g){var ins=g.querySelectorAll('input');ins.forEach(function(el,k){el.addEventListener('input',function(){el.value=el.value.replace(/\D/g,'');if(el.value&&ins[k+1])ins[k+1].focus();});el.addEventListener('keydown',function(e){if(e.key==='Backspace'&&!el.value&&ins[k-1])ins[k-1].focus();});el.addEventListener('paste',function(e){var t=(e.clipboardData.getData('text')||'').replace(/\D/g,'');if(!t)return;e.preventDefault();ins.forEach(function(x,n){x.value=t[n]||'';});});});});
document.querySelectorAll('[data-wizard]').forEach(function(w){var s=1,ps=w.querySelectorAll('.pane'),st=document.querySelectorAll('.steps li');function go(n){s=n;ps.forEach(function(p){p.classList.toggle('on',+p.dataset.p===n);});st.forEach(function(l){var k=+l.dataset.s;l.classList.toggle('on',k===n);l.classList.toggle('done',k<n);});}
w.querySelectorAll('[data-next]').forEach(function(b){b.addEventListener('click',function(){go(Math.min(3,s+1));});});w.querySelectorAll('[data-prev]').forEach(function(b){b.addEventListener('click',function(){go(Math.max(1,s-1));});});});
"""



EXTRA_CSS = r"""
.duo{display:grid;grid-template-columns:1fr 1fr;gap:20px;width:100%;max-width:900px}.duo .card{max-width:none}.card.alt2{background:linear-gradient(160deg,var(--pc),var(--lo));display:flex;flex-direction:column;gap:14px;justify-content:center}
.card.alt2 .ticks{margin:4px 0 8px}.card.alt2 .btn{width:100%}
.card.nopad{padding:0;overflow:hidden}.cover{position:relative;height:150px;background:linear-gradient(135deg,var(--pc),var(--lw));display:flex;flex-direction:column;justify-content:flex-end;padding:20px 28px;gap:2px}
.cv-ico{position:absolute;right:22px;top:18px;width:54px;height:54px;border-radius:calc(var(--r) * .9);background:var(--pr);color:var(--op);display:grid;place-items:center}.cv-ico svg{width:28px;height:28px}
.cv-b{font:700 22px var(--hf)}.cv-t{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--tv)}.cv-body{padding:28px 34px 34px}
.ws{display:flex;align-items:stretch;height:48px;border:var(--bw) solid var(--ol);border-radius:calc(var(--r) * .7);background:var(--ct);overflow:hidden}.ws:focus-within{border-color:var(--pr);box-shadow:0 0 0 3px var(--pa)}
.ws input{flex:1;min-width:0;border:0;background:transparent;color:var(--tx);font:inherit;padding:0 14px;outline:none}.ws input::placeholder{color:var(--tv);opacity:.85}.ws span{display:grid;place-items:center;padding:0 14px;background:var(--hi);color:var(--tv);font-size:14px;border-left:1px solid var(--ov)}
.accts{display:flex;flex-direction:column;gap:10px;margin-top:22px}.acct{display:flex;align-items:center;gap:14px;width:100%;padding:12px 14px;border:var(--bw) solid var(--ov);border-radius:calc(var(--r) * .8);background:var(--ct);color:var(--tx);font:inherit;text-align:left;cursor:pointer}
.acct:hover{border-color:var(--ol);background:var(--hi)}.acct svg{width:18px;height:18px;margin-left:auto;color:var(--tv)}.acct .who{display:flex;flex-direction:column;line-height:1.3}.acct small{color:var(--tv);font-size:12px}
.av{width:40px;height:40px;border-radius:50%;background:var(--pr);color:var(--op);display:grid;place-items:center;font:700 14px var(--bf);flex:none}.acct.add .av{background:transparent;border:var(--bw) dashed var(--ol);color:var(--tv);font-size:20px}
.pinbox{width:100%;max-width:340px;text-align:center;display:flex;flex-direction:column;align-items:center}.pinbox .logo{margin-bottom:14px}.pinbox .badge{margin-bottom:12px}
.dots{display:flex;gap:16px;margin:22px 0 26px}.dots i{width:16px;height:16px;border-radius:50%;border:2px solid var(--ol)}.dots i.on{background:var(--pr);border-color:var(--pr)}
.pad{display:grid;grid-template-columns:repeat(3,76px);gap:14px;justify-content:center;margin-bottom:22px}.pad button{height:76px;border-radius:50%;border:var(--bw) solid var(--ov);background:var(--ct);color:var(--tx);font:600 24px var(--hf);cursor:pointer;display:grid;place-items:center}
.pad button:hover{background:var(--hi);border-color:var(--ol)}.pad button:active{background:var(--pa)}.pad .soft{background:transparent;border-color:transparent;font-size:20px;color:var(--tv)}.pad .soft svg{width:26px;height:26px}.small{font-size:13px}
.envbar{display:flex;justify-content:space-between;align-items:center;font-size:12px;margin:-6px 0 20px;padding-bottom:14px;border-bottom:1px solid var(--ov)}.envpill{padding:4px 10px;border-radius:999px;background:var(--ta);color:var(--te);font-weight:700;letter-spacing:.04em}
.quote{margin:auto 0}.quote blockquote{font:600 clamp(22px,2.4vw,32px)/1.3 var(--hf);margin-bottom:24px}.quote figcaption{display:flex;align-items:center;gap:12px;font-size:14px}.quote figcaption span:last-child{display:flex;flex-direction:column;line-height:1.3}.quote small{color:var(--tv)}
.stripwrap{min-height:100vh;display:flex;flex-direction:column}.topbar.flat{border-bottom:0}.strip-hero{flex:1;display:flex;flex-direction:column;justify-content:center;gap:22px;padding:20px 48px 70px;max-width:1240px;width:100%;margin:0 auto}
.strip{display:flex;flex-wrap:wrap;align-items:flex-end;gap:14px;padding:18px;background:var(--lo);border:var(--bw) solid var(--ov);border-radius:var(--r);box-shadow:var(--sh);max-width:980px}.strip .field{flex:1 1 220px}.strip .btn.primary{width:auto;flex:0 0 auto;padding:0 28px}
.devbox{margin:22px 0;border:var(--bw) solid var(--ov);border-radius:calc(var(--r) * .8);background:var(--ct);overflow:hidden}.devbox div{display:flex;justify-content:space-between;padding:12px 16px;font-size:14px}.devbox div+div{border-top:1px solid var(--ov)}.devbox dt{color:var(--tv)}.devbox dd{margin:0;font-weight:600}
.stackbtn .btn.primary,.stackbtn .btn.ghost{width:100%}
@media(max-width:860px){.duo{grid-template-columns:1fr}.strip-hero{padding:10px 20px 50px}.cv-body{padding:24px}.pad{grid-template-columns:repeat(3,68px);gap:12px}.pad button{height:68px}}
"""
EXTRA_JS = r"""
document.querySelectorAll('[data-pin]').forEach(function(w){var v='',d=w.querySelectorAll('.dots i');function paint(){d.forEach(function(x,k){x.classList.toggle('on',k<v.length);});}w.querySelectorAll('[data-k]').forEach(function(b){b.addEventListener('click',function(){var k=b.dataset.k;if(k==='del')v=v.slice(0,-1);else if(v.length<4)v+=k;paint();});});});
"""

def build(n, li, ii):
    lname, group, fn, ldesc = LAYOUTS[li]
    ind = INDUSTRIES[ii]
    k = li * 5 + ii * 3
    heading, body, hgen, bgen = FONTS[(li * 3 + ii * 5) % len(FONTS)]
    if lname == "Terminal Console":
        heading, body, hgen, bgen = "JetBrains Mono", "JetBrains Mono", "monospace", "monospace"
    radius = RADII[(li + ii * 2) % len(RADII)]
    bw = BORDERS[(li * 2 + ii) % len(BORDERS)]
    shadow = SHADOWS[(li + ii * 3) % len(SHADOWS)]
    pattern = PATTERNS[(li * 2 + ii * 5) % len(PATTERNS)]
    palette = PAL_IDS[(n * 7 + ii) % len(PAL_IDS)]
    hw = 800 if hgen == "sans-serif" and heading in ("Archivo", "Syne", "Outfit", "Poppins") else (600 if hgen == "serif" else 700)

    fam = "&".join(f"family={f.replace(' ', '+')}:wght@400;500;600;700;800" for f in dict.fromkeys([heading, body]))
    hf = f"'{heading}',{'Georgia,serif' if hgen == 'serif' else 'system-ui,sans-serif' if hgen != 'monospace' else 'ui-monospace,Menlo,monospace'}"
    bf = f"'{body}',{'ui-monospace,Menlo,monospace' if bgen == 'monospace' else 'system-ui,-apple-system,Segoe UI,sans-serif'}"
    css = (BASE_CSS.replace("__R__", str(radius)).replace("__BW__", str(bw)).replace("__SH__", shadow)
           .replace("__HF__", hf).replace("__BF__", bf).replace("__HW__", str(hw))
           .replace("__PATTERN__", PATTERN_CSS[pattern]))
    extra_js = ""
    if li >= 23:
        css += EXTRA_CSS
        extra_js = EXTRA_JS
    cw = COLORWAY.replace("if (!palettes.some(p => p.id === selected)) selected = 'imperial-gold';",
                          f"if (!palettes.some(p => p.id === selected)) selected = '{palette}';")
    title = f"{lname} · {ind['name']}"
    page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{q(title)} — {q(ind["brand"])} sign in</title><meta name="theme-color" content="#000000">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{fam}&display=swap" rel="stylesheet">
<style>{css}</style></head>
<body>
{fn(ind)}
<script>{JS}{extra_js}</script>
{cw}
<script>requestAnimationFrame(function(){{requestAnimationFrame(function(){{document.documentElement.classList.add("ready")}})}})</script>
<script src="../../assets/cd-auth-enhance.js" defer></script>
</body></html>
'''
    num = f"{n:03d}"
    slug = re.sub(r"[^a-z0-9]+", "_", f"{lname}_{ind['slug']}".lower()).strip("_")
    return dict(id=f"screen_{num}_{slug}", title=title, group=group, description=f"{ldesc} Styled for {ind['name'].lower()} — rename {ind['brand']} to your client's brand.",
                number=num, page=page, palette=palette, featured=False)


def main():
    NL0, NI0 = 23, 12   # layouts / industries that existed in batch 1
    first = int(sys.argv[3]) if len(sys.argv) > 3 else 337
    combos = [(li, ii) for ii in range(len(INDUSTRIES)) for li in range(len(LAYOUTS)) if not (li < NL0 and ii < NI0)]
    random.Random(2027).shuffle(combos)
    out, n = [], first
    for li, ii in combos:
        t = build(n, li, ii)
        d = f"{REPO}/templates/{t['id']}"
        os.makedirs(d, exist_ok=True)
        open(f"{d}/index.html", "w", encoding="utf-8").write(t.pop("page"))
        t["preview"] = f"templates/{t['id']}/screen.png"
        t["live"] = f"templates/{t['id']}/index.html"
        out.append(t)
        n += 1
    json.dump(out, open(OUT_JSON, "w"), indent=1)
    print(len(out), "templates written, numbered", first, "to", n - 1)

main()
