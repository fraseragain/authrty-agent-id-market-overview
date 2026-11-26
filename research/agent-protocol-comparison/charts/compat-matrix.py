"""Render the protocol compatibility matrix as HTML (for headless-Chrome PNG export).

Usage: python3 compat-matrix.py ../compatibility.json <out-dir>
  compatibility-matrix.html  one triangle, each pair once: fill = seen together in the wild,
                             overlapping circles = a spec defines the join, one circle = mentioned only,
                             ≈ = same job, numbered badge = note
  compat-list.html           every pair with any evidence, ranked by evidence (working view)
"""
import json, sys, html, os

C = json.load(open(sys.argv[1]))
OUT = sys.argv[2]

INK, INK2, MUTED = '#0b0b0b', '#52514e', '#898781'
SURF, PLANE, GRID, AXIS = '#fcfcfb', '#f9f9f7', '#e1e0d9', '#c3c2b7'
ABSENT = '#f0efec'
# one hue, light -> dark
WILD = {'none': (ABSENT, INK), 'code': ('#fad7c2', INK), 'announced': ('#f08a55', INK), 'live': ('#b8471b', '#fff')}
WILD_LABEL = {'live': 'Live', 'announced': 'Announced, preview or pilot', 'code': 'Code only', 'none': 'Not seen'}
WRANK = {'live': 3, 'announced': 2, 'code': 1, 'none': 0}
SRANK = {'defined': 2, 'mentioned': 1, 'none': 0}
FONT = 'system-ui,-apple-system,"Segoe UI",sans-serif'

NAMES = {'ACP': 'ACP (OpenAI, Stripe)', 'UCP': 'UCP', 'AP2': 'AP2', 'VI': 'Verifiable Intent',
         'TAP': 'Visa TAP', 'x402': 'x402', 'MPP': 'MPP', 'PAP': 'PAP (Poppy) 1.0', 'MCP': 'MCP',
         'A2A': 'A2A', 'WebBotAuth': 'Web Bot Auth', 'ERC8004': 'ERC-8004', 'x401': 'x401', 'KYA-OS': 'KYA-OS'}
GROUPS = [('Agent identity and access', ['WebBotAuth', 'TAP', 'KYA-OS', 'PAP', 'x401']),
          ('Agent transport', ['MCP', 'A2A']),
          ('Mandates and checkout', ['AP2', 'VI', 'UCP', 'ACP']),
          ('Payment rails', ['x402', 'MPP', 'ERC8004'])]
ORDER = [p for _, ps in GROUPS for p in ps]
GROUP_OF = {p: g for g, ps in GROUPS for p in ps}

JOIN = {frozenset((j['a'], j['b'])): j for j in C['joins']}
WILDP = {frozenset((w['a'], w['b'])): w for w in C['wild']}
ALT = {frozenset(p) for p in C['alternatives']['pairs']}


def spec(pair):
    j = JOIN.get(pair)
    return (j['level'] if j else 'none'), (j.get('note') if j else None), j


def wild(pair):
    w = WILDP.get(pair)
    return (w['level'] if w else 'none'), w


def glyph(cx, cy, lvl, col=INK, r=8):
    """Joined = two overlapping rings with the overlap filled (a Venn); mentioned = one ring. Same circle throughout, always black."""
    col = INK
    # same circle (radius r, stroke 1.8) for every mark
    ring = f'fill="none" stroke="{col}" stroke-width="1.8"'
    if lvl == 'defined':
        d = r * 0.62
        h = (r * r - d * d) ** 0.5
        lens = (f'M{cx:.2f},{cy-h:.2f} A{r},{r} 0 0 1 {cx:.2f},{cy+h:.2f} '
                f'A{r},{r} 0 0 1 {cx:.2f},{cy-h:.2f} Z')
        return (f'<path d="{lens}" fill="{col}"/>'
                f'<circle cx="{cx-d}" cy="{cy}" r="{r}" {ring}/>'
                f'<circle cx="{cx+d}" cy="{cy}" r="{r}" {ring}/>')
    if lvl == 'mentioned':
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" {ring}/>'
    return ''


def badge(x, y, n):
    return (f'<circle cx="{x}" cy="{y}" r="8" fill="{SURF}" stroke="{INK}" stroke-width="1.2"/>'
            f'<text x="{x}" y="{y+3.6}" font-size="10" font-weight="650" fill="{INK}" text-anchor="middle">{n}</text>')


def page(title, sub, body, w, src):
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>
html,body{{margin:0;background:{PLANE}}}
body{{width:{w}px;font-family:{FONT};color:{INK}}}
.card{{margin:16px;background:{SURF};border:1px solid rgba(11,11,11,.10);border-radius:12px;padding:28px 32px 22px}}
h1{{font-size:24px;font-weight:650;margin:0 0 6px;letter-spacing:-.01em}}
.sub{{font-size:14px;color:{INK2};margin:0 0 18px;line-height:1.45;max-width:{w-140}px}}
.src{{font-size:11.5px;color:{MUTED};margin-top:14px;line-height:1.4}}
.kicker{{font-size:12px;letter-spacing:.04em;color:{MUTED};margin:0 0 8px;text-transform:uppercase}}
svg text{{font-family:{FONT}}}
table{{border-collapse:collapse;width:100%;font-size:13px;line-height:1.4;color:{INK2}}}
th{{text-align:left;font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;color:{MUTED};font-weight:500;padding:0 10px 6px 0;border-bottom:1px solid {AXIS}}}
td{{padding:6px 10px 6px 0;border-bottom:1px solid {GRID};vertical-align:top}}
tr.tier td{{border-bottom:none;padding:16px 0 4px;font-size:13px;font-weight:650;color:{INK}}}
.pair{{color:{INK};font-weight:600;white-space:nowrap}}
.chip{{display:inline-block;min-width:16px;height:16px;border-radius:4px;vertical-align:-3px;margin-right:6px}}
</style></head><body><div class="card"><h1>{html.escape(title)}</h1><p class="sub">{sub}</p>{body}<div class="src">{html.escape(src)}</div></div><script>document.body.setAttribute('data-h',Math.ceil(document.querySelector('.card').getBoundingClientRect().bottom+16))</script></body></html>'''


def notes_block(nums=None):
    items = ''.join(f'<div style="break-inside:avoid;margin:0 0 9px;display:flex;gap:8px"><span style="flex:none;width:18px;height:18px;border-radius:50%;border:1.2px solid {INK};font-size:10.5px;font-weight:650;color:{INK};display:flex;align-items:center;justify-content:center">{k}</span><span>{html.escape(v)}</span></div>'
                    for k, v in sorted(C['notes'].items(), key=lambda kv: int(kv[0])))
    return (f'<div style="margin-top:18px;padding-top:14px;border-top:1px solid {GRID};font-size:13px;line-height:1.45;color:{INK2}">'
            f'<div class="kicker">Numbered notes: possible gaps or friction</div>'
            f'<div style="column-count:2;column-gap:36px">{items}</div></div>')


SRC = ('Source: Authrty analysis of primary specifications, 26 Nov 2026. In the wild: live pairs checked against vendor pages on 26 Nov 2026; '
       'code = GitHub package manifests, 25 Nov 2026 (noisy, unfiltered). Per-pair evidence in research/agent-protocol-comparison/compatibility.json and compatibility.md.')


# ---------- view 1: one triangle ----------
def triangle():
    LW, CW, TOP = 170, 56, 34
    rows, cols = ORDER[1:], ORDER[:-1]
    n = len(rows)
    W = LW + CW * n + 10
    H = TOP + CW * n + 125
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    # row group brackets on the left
    for gname, ps in GROUPS:
        rs = [rows.index(p) for p in ps if p in rows]
        y0, y1 = TOP + CW * rs[0] + 3, TOP + CW * (rs[-1] + 1) - 3
        s.append(f'<line x1="4" x2="4" y1="{y0}" y2="{y1}" stroke="{AXIS}" stroke-width="2"/>')
    # group names along the diagonal steps
    for gname, ps in GROUPS:
        if ps[0] not in cols:
            continue
        c = cols.index(ps[0])
        x, y = LW + CW * c + 4, TOP + CW * c - 8
        s.append(f'<text x="{x}" y="{y}" font-size="11.5" font-weight="600" fill="{INK2}">{html.escape(gname)}</text>')
    for i, p in enumerate(rows):
        s.append(f'<text x="14" y="{TOP + CW*i + CW/2 + 5}" font-size="14" fill="{INK}">{html.escape(NAMES[p])}</text>')
    for j, p in enumerate(cols):
        x = LW + CW * j + CW / 2
        s.append(f'<text transform="translate({x-4},{TOP + CW*n + 10}) rotate(50)" font-size="13" font-weight="600" fill="{INK}">{html.escape(NAMES[p])}</text>')
    # group separators inside the triangle
    bounds = []
    k = 0
    for _, ps in GROUPS[:-1]:
        k += len(ps)
        bounds.append(k)
    for b in bounds:
        # vertical line after column index b-1, horizontal line before row index b-1
        x = LW + CW * b
        s.append(f'<line x1="{x}" x2="{x}" y1="{TOP + CW*(b-1)}" y2="{TOP + CW*n}" stroke="{AXIS}" stroke-width="1.5"/>')
        y = TOP + CW * (b - 1)
        s.append(f'<line x1="{LW}" x2="{LW + CW*b}" y1="{y}" y2="{y}" stroke="{AXIS}" stroke-width="1.5"/>')
    for i, a in enumerate(rows):
        for j, b in enumerate(cols):
            if j > i:
                continue
            x, y = LW + CW * j, TOP + CW * i
            pair = frozenset((a, b))
            wl, _ = wild(pair)
            sl, note, jn = spec(pair)
            if pair in JOIN and JOIN[pair].get('note') is None:
                note = None
            fill, tc = WILD[wl]
            s.append(f'<rect x="{x+1.5}" y="{y+1.5}" width="{CW-3}" height="{CW-3}" rx="4" fill="{fill}"/>')
            s.append(glyph(x + CW / 2, y + CW / 2, sl, tc))
            if pair in ALT:
                s.append(f'<text x="{x+7}" y="{y+CW-8}" font-size="15" font-weight="700" fill="{INK}">≈</text>')
            if note:
                s.append(badge(x + CW - 10, y + 10, note))
    s.append('</svg>')
    return ''.join(s), W, H


def tri_legend():
    def row(sw, label):
        return f'<div style="display:flex;align-items:center;gap:10px;margin:0 0 8px">{sw}<span>{label}</span></div>'

    def cell(fill, inner=''):
        return f'<svg width="34" height="34" style="flex:none"><rect x="0.5" y="0.5" width="33" height="33" rx="4" fill="{fill}"/>{inner}</svg>'
    fill_rows = ''.join(row(cell(WILD[k][0]), t) for k, t in [
        ('live', '<b style="color:#0b0b0b">Live</b>: we found a generally available product that appears to run both in one flow (vendor pages, 26 Nov)'),
        ('announced', '<b style="color:#0b0b0b">Announced</b>: documented, preview or pilot; we could not confirm general availability'),
        ('code', '<b style="color:#0b0b0b">Code only</b>: both appear in at least one package file on GitHub'),
        ('none', '<b style="color:#0b0b0b">Not seen</b>: none found in our search')])
    glyph_rows = (row(cell(ABSENT, glyph(17, 17, 'defined', INK)), '<b style="color:#0b0b0b">Joined</b> (overlapping circles): at least one spec describes how the two combine (core, extension, binding, SHOULD or MAY)')
                  + row(cell(ABSENT, glyph(17, 17, 'mentioned', INK)), '<b style="color:#0b0b0b">Mentioned</b> (one circle): referenced, proposed or given as an example, without a described join')
                  + row(cell(ABSENT), 'No mark: we found no reference in either spec'))
    other = (row(cell(ABSENT, f'<text x="7" y="26" font-size="15" font-weight="700" fill="{INK}">≈</text>'), '<b style="color:#0b0b0b">Same job</b>: largely overlapping roles, so a product would usually choose one')
             + row(cell(ABSENT, badge(24, 10, 'n')), 'Numbered note below: a possible gap or point of friction'))
    read = (f'<div style="margin-top:16px;padding:12px 14px;background:{PLANE};border-radius:8px">'
            f'<div class="kicker">How to read it</div>'
            f'<div style="display:flex;align-items:center;gap:10px;margin:0 0 6px">{cell(WILD["live"][0], glyph(17,17,"defined"))}<span>Dark with overlapping circles: specified, and seen in use</span></div>'
            f'<div style="display:flex;align-items:center;gap:10px">{cell(ABSENT, glyph(17,17,"defined",INK))}<span>Pale with overlapping circles: specified, but we found no use yet</span></div></div>')
    return (f'<div style="font-size:13px;line-height:1.4;color:{INK2};width:420px">'
            f'<div class="kicker">Fill: seen together in the wild?</div>{fill_rows}'
            f'<div class="kicker" style="margin-top:14px">Mark: what do the specs describe?</div>{glyph_rows}'
            f'<div class="kicker" style="margin-top:14px">Also</div>{other}{read}</div>')


# ---------- view 3: ranked list ----------
def ranked():
    pairs = set(JOIN) | set(WILDP) | ALT | {frozenset((j['a'], j['b'])) for j in C['joins'] if j.get('note')}
    rows = []
    for p in pairs:
        a, b = sorted(p, key=ORDER.index)
        wl, w = wild(p)
        sl, note, jn = spec(p)
        rows.append(dict(a=a, b=b, wl=wl, w=w, sl=sl, jn=jn, note=note, alt=p in ALT))
    # order: wild tier, then spec level, then data order within the wild list
    worder = {frozenset((w['a'], w['b'])): k for k, w in enumerate(C['wild'])}
    rows.sort(key=lambda r: (-WRANK[r['wl']], -SRANK[r['sl']], worder.get(frozenset((r['a'], r['b'])), 999), ORDER.index(r['a']), ORDER.index(r['b'])))
    SPEC_TXT = {'defined': 'Joined', 'mentioned': 'Mentioned', 'none': '—'}
    out = [f'<table><colgroup><col style="width:250px"><col style="width:125px"><col style="width:330px"><col><col style="width:44px"></colgroup>'
           f'<tr><th>Pair</th><th>Spec</th><th>What the specs say</th><th>Where it is seen</th><th>Note</th></tr>']
    tier = None
    counts = {}
    for r in rows:
        counts[r['wl']] = counts.get(r['wl'], 0) + 1
    for r in rows:
        if r['wl'] != tier:
            tier = r['wl']
            fill = WILD[tier][0]
            label = WILD_LABEL[tier] if tier != 'none' else 'Not seen in the wild (spec link only, or same job)'
            out.append(f'<tr class="tier"><td colspan="5"><span class="chip" style="background:{fill};{"border:1px solid "+AXIS if tier=="none" else ""}"></span>{html.escape(label)} · {counts[tier]}</td></tr>')
        g = glyph(9, 8, r['sl'], INK, r=5)
        spec_cell = f'<svg width="20" height="16" style="vertical-align:-3px;margin-right:6px">{g}</svg>{SPEC_TXT[r["sl"]]}' if r['sl'] != 'none' else f'<span style="color:{MUTED}">Not mentioned</span>'
        spec_basis = html.escape(r['jn']['basis']) if r['jn'] and r['jn'].get('basis') and r['sl'] != 'none' else ''
        where = html.escape(r['w']['basis']) if r['w'] else f'<span style="color:{MUTED}">—</span>'
        alt = f' <span title="same job" style="color:{INK2};font-weight:700">≈ same job</span>' if r['alt'] else ''
        note = badge_html(r['note']) if r['note'] else ''
        out.append(f'<tr><td><span class="pair">{html.escape(NAMES[r["a"]])} + {html.escape(NAMES[r["b"]])}</span>{alt}</td>'
                   f'<td style="white-space:nowrap;color:{INK}">{spec_cell}</td><td>{spec_basis}</td><td>{where}</td><td>{note}</td></tr>')
    out.append('</table>')
    return ''.join(out), len(rows)


def badge_html(n):
    return (f'<span style="display:inline-flex;width:18px;height:18px;border-radius:50%;border:1.2px solid {INK};font-size:10.5px;'
            f'font-weight:650;color:{INK};align-items:center;justify-content:center">{n}</span>')


os.makedirs(OUT, exist_ok=True)
sizes = {}

svg, w, h = triangle()
body = f'<div style="display:flex;gap:40px;align-items:flex-start">{svg}<div style="padding-top:30px">{tri_legend()}</div></div>{notes_block()}'
W = w + 40 + 420 + 100
sub = ('Fourteen agent protocols, each pair once. The fill shows whether we found the pair used together; overlapping circles mean a specification describes how they combine; one circle means a spec only references the other. '
       'In our review, only four pairs appear to run together in a generally available product, and three of those are also joined in a spec.')
open(os.path.join(OUT, 'compatibility-matrix.html'), 'w').write(page('Which agent protocols appear to fit together?', sub, body, W, SRC))
sizes['compatibility-matrix'] = [W, h]

table, nrows = ranked()
W2 = 1500
sub2 = (f'The {nrows} of 91 protocol pairs with any evidence, strongest first. Ranked by whether the pair is seen together in the wild, then by what the specifications define. '
        'The other pairs are neither mentioned in either spec nor seen together.')
open(os.path.join(OUT, 'compat-list.html'), 'w').write(page('Agent protocol pairs, ranked by evidence', sub2, table + notes_block(), W2, SRC))
sizes['compat-list'] = [W2, 0]

json.dump(sizes, open(os.path.join(OUT, 'compat-sizes.json'), 'w'))  # distinct from make-charts.py's sizes.json
print(sizes, nrows)
