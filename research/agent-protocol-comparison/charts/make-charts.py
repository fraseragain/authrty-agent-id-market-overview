"""Render the agent protocol comparison charts as HTML (for headless-Chrome PNG export)."""
import json, math, sys, html, os

SRC = sys.argv[1]   # scores.json
OUT = sys.argv[2]   # output dir
d = json.load(open(SRC))
S, P = d['rubric_scores'], d['chain_scores']

# Authrty brand palette (authrty.ai): navy #0D1421, indigo #3E42B6, lavender #B9BBF8, text #50565D, font Inter
INK, INK2, MUTED = '#0D1421', '#50565D', '#7B7F88'
SURF, PLANE, GRID, AXIS = '#FFFFFF', '#F7F7FA', '#E6E6EC', '#C9CAD6'
BLUE, ORANGE = '#3E42B6', '#0D1421'  # totals and Harvey balls in indigo; adoption bars in navy
ABSENT, PARTIAL, MET = '#F0F0F4', '#B9BBF8', '#3E42B6'
FONT = 'Inter,system-ui,-apple-system,"Segoe UI",sans-serif'
FONT_LINK = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;650;700&display=block" rel="stylesheet">'

NAMES = {'ACP': 'ACP (OpenAI, Stripe)', 'UCP': 'UCP', 'AP2': 'AP2', 'VI': 'Verifiable Intent',
         'TAP': 'Visa TAP', 'x402': 'x402', 'MPP': 'MPP', 'PAP': 'PAP (Poppy) 1.0', 'MCP': 'MCP',
         'A2A': 'A2A', 'WebBotAuth': 'Web Bot Auth', 'ERC8004': 'ERC-8004', 'x401': 'x401', 'KYA-OS': 'KYA-OS'}
ORDER = ['ACP', 'UCP', 'AP2', 'VI', 'TAP', 'x402', 'MPP', 'PAP', 'MCP', 'A2A', 'WebBotAuth', 'ERC8004', 'x401', 'KYA-OS']
SOURCE = 'Source: Authrty analysis of primary specifications, 25 Nov 2026. Rubric, citations and data in research/agent-protocol-comparison/.'


def page(title, sub, body, w, h, src=SOURCE):
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONT_LINK}<title>{html.escape(title)}</title><style>
html,body{{margin:0;background:{PLANE}}}
body{{width:{w}px;font-family:{FONT};color:{INK}}}
.card{{margin:16px;background:{SURF};border:1px solid rgba(13,20,33,.10);border-radius:12px;padding:28px 32px 22px}}
h1{{font-size:24px;font-weight:650;margin:0 0 6px;letter-spacing:-.01em}}
.sub{{font-size:14px;color:{INK2};margin:0 0 18px;line-height:1.45;max-width:{w-120}px}}
.src{{font-size:11.5px;color:{MUTED};margin-top:14px;line-height:1.4}}
svg text{{font-family:{FONT}}}
</style></head><body><div class="card"><h1>{html.escape(title)}</h1><p class="sub">{sub}</p>{body}<div class="src">{html.escape(src)}</div></div><script>document.body.setAttribute('data-h',Math.ceil(document.querySelector('.card').getBoundingClientRect().bottom+16))</script></body></html>''', w, h


def ball(cx, cy, r, frac, col):
    """Harvey ball: outline ring plus a clockwise wedge from 12 o'clock."""
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SURF}" stroke="{col}" stroke-width="2"/>'
    frac = max(0, min(1, frac))
    if frac >= 0.999:
        out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>'
    elif frac > 0:
        a = 2 * math.pi * frac
        x, y = cx + r * math.sin(a), cy - r * math.cos(a)
        large = 1 if frac > 0.5 else 0
        out += f'<path d="M{cx},{cy} L{cx},{cy-r} A{r},{r} 0 {large} 1 {x:.2f},{y:.2f} Z" fill="{col}"/>'
    return out


def fmt(v):
    return ('%g' % v) if v != int(v) else str(int(v))


# ---------- Chart 1: Harvey balls on four headings (amended criteria) ----------
CREDIT = "Harvey-ball format and the four headings inspired by OneID's protocol coverage chart (LinkedIn, 11 Nov 2026)."


def chart1():
    dims = ['Identity', 'Authentication', 'Authorisation', 'Accountability']
    rows = []
    for p in ORDER:
        s = dict(S[p]); s.update(I1=P[p]['I1p'], I2=P[p]['I2p'], A2=P[p]['A2p'])
        rows.append((p, [sum(s[k + str(i)] for i in range(1, 5)) for k in 'IAZC']))
    rows.sort(key=lambda r_: (-sum(r_[1]), NAMES[r_[0]]))
    LW, GW, RH, TOP = 220, 200, 46, 78
    W = LW + GW * 4
    H = TOP + RH * len(rows) + 10
    r = 14
    svg = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    lx = 0
    for frac, lab in ((0, '0'), (.25, '1'), (.5, '2'), (.75, '3'), (1, '4 of 4')):
        svg.append(ball(lx + r, 16, r - 2, frac, BLUE) + f'<text x="{lx+2*r+6}" y="21" font-size="13.5" fill="{INK}">{lab}</text>')
        lx += 70 if frac < 1 else 0
    svg.append(f'<text x="{W}" y="21" font-size="13" fill="{INK2}" text-anchor="end">Half-steps appear as partial wedges</text>')
    for i, dn in enumerate(dims):
        x = LW + GW * i + GW / 2
        svg.append(f'<text x="{x}" y="{TOP-14}" font-size="14" font-weight="600" fill="{INK}" text-anchor="middle">{dn}</text>')
    svg.append(f'<line x1="0" x2="{W}" y1="{TOP-4}" y2="{TOP-4}" stroke="{AXIS}"/>')
    for j, (p, ours) in enumerate(rows):
        y = TOP + RH * j + RH / 2
        if j % 2 == 0:
            svg.append(f'<rect x="0" y="{TOP+RH*j}" width="{W}" height="{RH}" fill="{PLANE}"/>')
        svg.append(f'<text x="8" y="{y+5}" font-size="14.5" fill="{INK}">{html.escape(NAMES[p])}</text>')
        for i in range(4):
            gx = LW + GW * i + GW / 2
            svg.append(ball(gx - 12, y, r, ours[i] / 4, BLUE))
            svg.append(f'<text x="{gx+10}" y="{y+5}" font-size="13.5" fill="{INK2}" style="font-variant-numeric:tabular-nums">{fmt(ours[i])}</text>')
    svg.append('</svg>')
    sub = ('Each protocol scored 0 to 4 on four headings, using a published 16-criterion rubric applied to the protocol\'s own specification. '
           'Principal and operator must be identifiable, not just named, and the agent\'s key must be tied to an accountable party and checkable later. ' + CREDIT)
    return page('Agent protocols on four headings, scored from the specifications', sub, ''.join(svg), W + 100, H + 196)


# ---------- Charts 2 and 3: chain heat-maps ----------
LINKS = [('L1', 'Principal', 'identity'), ('L2', 'Operator', 'identity'), ('L3', 'Agent key', 'binding'),
         ('L4', 'Delegation', ''), ('L5', 'Session', 'authentication'), ('L6', 'Action within', 'the grant'),
         ('L7', 'Evidence', ''), ('L8', 'Redress', ''), ('L9', 'Trust', 'anchor'), ('L10', 'Continuity', '')]
GROUPS = [('Who is behind it', 0, 3), ('What it may do', 3, 6), ('Proof, redress and trust', 6, 9), ('Joined up', 9, 10)]


def heat(rows, title, sub, best_row=False, label_w=250, extra=150, ghost_legend=False, adopt=None, src=None, key=None):
    CW, RH, TOP = 92, 40, 104
    CHW, TW = 0, 150  # the chain (weakest-link) column is not shown
    AW = 660 if adopt else 0
    W = label_w + CW * 10 + 14 + TW + AW
    H = TOP + RH * (len(rows) + (1 if best_row else 0)) + (30 if adopt else 14)
    fill = {0: ABSENT, 1: PARTIAL, 2: MET}
    tcol = {0: MUTED, 1: INK, 2: '#ffffff'}
    word = {0: 'absent', 1: 'partial', 2: 'met'}
    svg = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    # legend
    lx = 0
    for v in (2, 1, 0):
        svg.append(f'<rect x="{lx}" y="4" width="22" height="16" rx="3" fill="{fill[v]}" stroke="rgba(13,20,33,.10)"/>'
                   f'<text x="{lx+30}" y="17" font-size="13.5" fill="{INK}">{v} = {word[v]}</text>')
        lx += 120
    if ghost_legend:
        svg.append(f'<rect x="{lx}" y="4" width="22" height="16" rx="3" fill="{PARTIAL}" fill-opacity=".45" stroke="{MET}" stroke-dasharray="4 3"/>'
                   f'<text x="{lx+30}" y="17" font-size="13.5" fill="{INK}">if joined as proposed (no spec defines the join)</text>')
    # group headers
    for gname, a, b in GROUPS:
        x0, x1 = label_w + CW * a + 3, label_w + CW * b - 3
        svg.append(f'<line x1="{x0}" x2="{x1}" y1="{TOP-62}" y2="{TOP-62}" stroke="{AXIS}" stroke-width="2"/>'
                   f'<text x="{(x0+x1)/2}" y="{TOP-68}" font-size="12.5" font-weight="600" fill="{INK2}" text-anchor="middle">{gname}</text>')
    for i, (code, l1, l2) in enumerate(LINKS):
        x = label_w + CW * i + CW / 2
        svg.append(f'<text x="{x}" y="{TOP-40}" font-size="12" fill="{MUTED}" text-anchor="middle">{code}</text>'
                   f'<text x="{x}" y="{TOP-24}" font-size="13" font-weight="600" fill="{INK}" text-anchor="middle">{l1}</text>'
                   f'<text x="{x}" y="{TOP-9}" font-size="13" font-weight="600" fill="{INK}" text-anchor="middle">{l2}</text>')
    xc = label_w + CW * 10 + 14
    xt = xc
    svg.append(f'<text x="{xt}" y="{TOP-24}" font-size="13" font-weight="650" fill="{INK}">Total</text>'
               f'<text x="{xt}" y="{TOP-9}" font-size="12" fill="{MUTED}">out of 20</text>')
    xa = xt + TW + 10
    BW, DO = 240, 325  # bar width; x offset of the downloads column
    if adopt:
        svg.append(f'<line x1="{xa-8}" x2="{xa-8}" y1="{TOP-40}" y2="{TOP+RH*len(rows)}" stroke="{GRID}"/>'
                   f'<text x="{xa}" y="{TOP-40}" font-size="12" fill="{MUTED}">ADOPTION ({"shared log scale, 1 to 1 billion" if MODE == "log" else "linear, share of the largest"})</text>'
                   f'<text x="{xa}" y="{TOP-24}" font-size="13" font-weight="650" fill="{INK}">GitHub stars</text>'
                   f'<text x="{xa}" y="{TOP-9}" font-size="12" fill="{MUTED}">main repo</text>'
                   f'<text x="{xa+DO}" y="{TOP-24}" font-size="13" font-weight="650" fill="{INK}">Downloads</text>'
                   f'<text x="{xa+DO}" y="{TOP-9}" font-size="12" fill="{MUTED}">official packages, 4 weeks</text>')
    tracks = []  # adoption tracks sit under the gridlines; bars sit over them
    allrows = list(rows)
    if best_row:
        allrows.append(('Best on the link', [max(r[1][i] for r in rows if not r[0].startswith('↳')) for i in range(10)], None))
    for j, (name, vals, note) in enumerate(allrows):
        y = TOP + RH * j
        is_best = best_row and j == len(allrows) - 1
        if is_best:
            svg.append(f'<line x1="0" x2="{label_w+CW*10}" y1="{y+2}" y2="{y+2}" stroke="{AXIS}"/>')
            y += 6
        svg.append(f'<text x="6" y="{y+RH/2+5}" font-size="14.5" font-weight="{650 if is_best else 400}" fill="{INK}">{html.escape(name)}</text>')
        if note:
            svg.append(f'<text x="6" y="{y+RH/2+19}" font-size="11" fill="{MUTED}">{html.escape(note)}</text>')
        ghost = name.startswith('↳ if joined')
        for i, v in enumerate(vals):
            x = label_w + CW * i
            if ghost:
                svg.append(f'<rect x="{x+2}" y="{y+2}" width="{CW-4}" height="{RH-4}" rx="4" fill="{fill[v]}" fill-opacity=".45" stroke="{MET if v else AXIS}" stroke-width="1.5" stroke-dasharray="4 3"/>'
                           f'<text x="{x+CW/2}" y="{y+RH/2+5}" font-size="14" font-weight="600" fill="{INK if v else MUTED}" text-anchor="middle">{v}</text>')
            else:
                svg.append(f'<rect x="{x+1}" y="{y+1}" width="{CW-2}" height="{RH-2}" rx="4" fill="{fill[v]}"/>'
                           f'<text x="{x+CW/2}" y="{y+RH/2+5}" font-size="14" font-weight="600" fill="{tcol[v]}" text-anchor="middle">{v}</text>')
        if is_best:
            continue
        tot = sum(vals)
        bw = (TW - 34) * tot / 20
        svg.append(f'<rect x="{xt}" y="{y+RH/2-7}" width="{TW-34}" height="14" rx="4" fill="{ABSENT}"/>'
                   f'<rect x="{xt}" y="{y+RH/2-7}" width="{bw:.1f}" height="14" rx="4" fill="{BLUE}" fill-opacity="{.45 if ghost else 1}"/>'
                   f'<text x="{xt+TW-28}" y="{y+RH/2+5}" font-size="13.5" fill="{INK}" style="font-variant-numeric:tabular-nums">{tot}</text>')
        a = adopt.get(name) if adopt else None
        if a is not None:
            for off, v, col in ((0, a['stars'], 'stars'), (DO, a['dl'], 'dl')):
                x0 = xa + off
                if v:
                    bw = max(3, BW * (math.log10(v) / 9 if MODE == 'log' else v / max(q[col] for q in adopt.values())))
                    tracks.append(f'<rect x="{x0}" y="{y+RH/2-7}" width="{BW}" height="14" rx="4" fill="{ABSENT}"/>')
                    svg.append(f'<rect x="{x0}" y="{y+RH/2-7}" width="{bw:.1f}" height="14" rx="4" fill="{ORANGE}"/>'
                               f'<text x="{x0+BW+6}" y="{y+RH/2+5}" font-size="13.5" fill="{INK}" style="font-variant-numeric:tabular-nums">{human(v)}</text>')
                else:
                    svg.append(f'<text x="{x0}" y="{y+RH/2+5}" font-size="12.5" fill="{MUTED}">no official package</text>')
    if adopt:
        yb = TOP + RH * len(rows)
        LAB = ['1', '10', '100', '1k', '10k', '100k', '1M', '10M', '100M', '1B']
        ticks = [(t, LAB[t]) for t in range(10)] if MODE == 'log' else [(0, '0'), (.5, '50%'), (1, '100%')]
        grid = []
        for off in (0, DO):
            for t, lab in ticks:
                major = MODE != 'log' or t % 3 == 0
                x = xa + off + BW * (t / 9 if MODE == 'log' else t)
                grid.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{TOP}" y2="{yb+4}" stroke="{AXIS if major else GRID}" stroke-opacity="{.9 if major else 1}" stroke-dasharray="{"2 3" if major else "1 4"}"/>')
                svg.append(f'<text x="{x:.1f}" y="{yb+17}" font-size="{11 if major else 9}" fill="{MUTED}" fill-opacity="{1 if major else .8}" text-anchor="middle">{lab}</text>')
        svg[1:1] = tracks + grid
    svg.append('</svg>')
    if key:
        svg.append(key_html(key))
    return page(title, sub, ''.join(svg), W + 100, H + extra, src or 'Source: Authrty analysis of primary specifications, 25 Nov 2026, with independent review. Rubric, per-link citations and data in research/agent-protocol-comparison/.')


def chart2():
    L = ['L%d' % i for i in range(1, 11)]
    rows = sorted(((NAMES[p], [P[p][l] for l in L], None) for p in ORDER), key=lambda r: (-sum(r[1]), -min(r[1])))
    sub = ('Ten links an auditor or a court would need to follow, from the person behind an agent to the money that moved. '
           '2 = met in the core spec, 1 = partial or optional, 0 = absent. Scored from each protocol\'s specification and checked by an independent reviewer. '
           'No protocol has a complete chain; seven links are never fully met by any of them.')
    return heat(rows, 'No agent protocol yet gives a complete chain of accountability', sub)


def chart3():
    st = d['chain_stacks']
    defs = [('AP2 + UCP (+ Verifiable Intent)', ['AP2', 'UCP'], 'AP2+VI+UCP', 'Normative join via UCP\'s AP2 Mandates extension'),
            ('PAP + UCP + Web Bot Auth', ['PAP', 'UCP', 'WebBotAuth'], 'PAP+UCP+WebBotAuth', 'Documented join; no principal-signed grant'),
            ('KYA-OS + MCP', ['KYA-OS', 'MCP'], 'KYA-OS+MCP', 'Tool calls, not purchases'),
            ('x402 + ERC-8004', ['x402', 'ERC8004'], 'x402+ERC8004', 'Joined only by an optional transaction hash'),
            ('Visa TAP + Web Bot Auth', ['TAP'], 'TAP+WebBotAuth', 'Join not defined: TAP\'s own scores'),
            ('ACP + Stripe payment tokens', ['ACP'], 'ACP+SPT', 'ACP\'s own scores')]
    rows = []
    for name, mem, key, note in defs:
        v = [max(P[m]['L%d' % i] for m in mem) for i in range(1, 10)] + [st[key]['L10']]
        rows.append((name, v, note))
    rows.sort(key=lambda r: (-sum(r[1]), -min(r[1])))
    sub = ('The same ten links for protocols as they are deployed together. Links 1–9 take the best member\'s score (an upper bound); '
           'continuity is scored across the joins. Stacking does not close the gaps: the members share them.')
    return heat(rows, 'Combining protocols does not complete the chain', sub, best_row=False, label_w=300, extra=118)



G = json.load(open(sys.argv[3]))
TR = json.load(open(sys.argv[4]))['protocols']
def human(v):
    for div, suf in ((1e6, 'M'), (1e3, 'k')):
        if v >= div:
            return ('%.1f' % (v / div)).rstrip('0').rstrip('.') + suf
    return str(int(v))
AP = {NAMES[k]: {'stars': TR[k]['stars'], 'dl': sum(TR[k]['downloads'].values())} for k in ORDER}
ASRC = ('Link scores: Authrty analysis of primary specifications, 25 Nov 2026, with independent review. '
        'Adoption: GitHub stars on each protocol\'s main repository, 25 Nov 2026 (MPP: the mppx SDK; Web Bot Auth: Cloudflare\'s implementation). '
        'Downloads of packages published by each protocol\'s maintainers on npm, PyPI and crates.io, 19 Oct to 15 Nov 2026; third-party packages excluded. '
        'Downloads include CI and dependency installs, not just users. Package list and notes in research/agent-protocol-comparison/adoption.json.')
MODE = 'log'  # adoption bars: one log scale, 1 to 1 billion, shared by stars and downloads
ALEG = ('<br><b>Navy bars show adoption</b>: GitHub stars and recent downloads, both on one log scale from 1 to 1 billion, so bar lengths compare across the two columns.'
        if MODE == 'log' else
        ' <b>Navy bars show adoption</b>: GitHub stars and recent downloads, each as a linear share of the largest value in its column (A2A for stars, MCP for downloads).')
GP, ST = G['general_protocols'], G['stacks']
L = ['L%d' % i for i in range(1, 11)]
SRC2 = 'Source: Authrty analysis of primary specifications, 25 Nov 2026, with independent review. Rubrics, per-link citations and data in research/agent-protocol-comparison/.'
STACKS = ["PAP + Web Bot Auth", "KYA-OS + MCP", "x402 + ERC-8004",
          "Visa TAP + Web Bot Auth", "ACP + Stripe payment tokens", "Web Bot Auth + PAP + KYA-OS",
          "Web Bot Auth + PAP + AP2", "Web Bot Auth + PAP + KYA-OS + AP2",
          "x402 + MCP", "MCP + A2A", "x402 + MPP + MCP", "UCP + AP2 over MCP/A2A", "PAP + Web Bot Auth (+ UCP, MCP)"]


NOTES = {"AP2 + UCP (+ Verifiable Intent)": "Joined by UCP's AP2 Mandates extension",
         "PAP + UCP + Web Bot Auth": "Documented join; no principal-signed grant",
         "PAP + Web Bot Auth": "Documented join; Web Bot Auth adds no link",
         "KYA-OS + MCP": "Joined by a draft, optional MCP extension",
         "x402 + ERC-8004": "Joined only by an optional transaction hash",
         "Visa TAP + Web Bot Auth": "Join not defined: TAP's own scores",
         "ACP + Stripe payment tokens": "ACP's own scores",
         "Web Bot Auth + PAP + KYA-OS": "Only PAP + Web Bot Auth is documented",
         "Web Bot Auth + PAP + AP2": "AP2 join only proposed (PAP issue #61)",
         "Web Bot Auth + PAP + KYA-OS + AP2": "Only PAP + Web Bot Auth is documented",
         "x402 + MCP": "Payer wallet not tied to the MCP caller",
         "MCP + A2A": "No grant passes between agents",
         "x402 + MPP + MCP": "One payment path per request",
         "UCP + AP2 over MCP/A2A": "As Google and Shopify describe it",
         "PAP + Web Bot Auth (+ UCP, MCP)": "As specified in PAP 1.0"}


def stack_rows(kind):
    rows = []
    for n in STACKS:
        s_ = ST[n]
        rows.append((n, s_[kind]['today'], NOTES[n]))
    rows.sort(key=lambda r: (-sum(r[1]), -min(r[1])))
    out = []
    for r in rows:
        out.append(r)
        ad = ST[r[0]][kind].get('as_deployed')
        if ad:
            out.append(('↳ as deployed (Shopify, Muse)', ad, 'Shopify poppy.json v0.4, UCP only'))
        ij = ST[r[0]][kind].get('if_joined')
        if ij:
            out.append(('↳ if joined as proposed', ij, None))
    return out


def pay_protocols():
    rows = sorted(((NAMES[p], [P[p][l] for l in L], None) for p in ORDER), key=lambda r: (-sum(r[1]), -min(r[1])))
    sub = ('Ten links an auditor or a court would need to follow, from the person behind an agent to the money that moved. '
           '2 = met in the core spec, 1 = partial or optional, 0 = absent. Scored from each protocol\'s specification and checked by an independent reviewer.')
    return heat(rows, 'Payments: the most-downloaded protocols do not complete the chain', sub + ALEG, adopt=AP, src=ASRC, key=KEY_PAY + KEY_SUM + KEY_ADOPT)


def gen_protocols():
    rows = sorted(((NAMES[p], [GP[p][l] for l in L], None) for p in ORDER), key=lambda r: (-sum(r[1]), -min(r[1])))
    sub = ('The same ten links for actions other than buying: reading data, messaging, changing an account, accepting terms, instructing another agent. '
           'Payment-only grants, receipts and chargebacks earn nothing here. 2 = met in the core spec, 1 = partial or optional, 0 = absent.')
    return heat(rows, 'Beyond payments: the most-downloaded protocols do not complete the chain', sub + ALEG, adopt=AP, src=ASRC, key=KEY_GEN + KEY_SUM + KEY_ADOPT)


def pay_stacks():
    sub = ('Protocols as deployed together, for purchases. A stack takes a member\'s score only where a spec defines the join; '
           'dashed rows show the upper bound if the members were joined as proposed. No spec defines those joins today.')
    return heat(stack_rows('purchase'), 'Payments: combining protocols does not complete the chain', sub, best_row=False, label_w=340, extra=118, ghost_legend=True, key=KEY_PAY + KEY_SUM)


def gen_stacks():
    sub = ('The same stacks for actions other than buying. Dashed rows show the upper bound if the members were joined as proposed; '
           'no spec defines those joins today.')
    return heat(stack_rows('general'), 'Beyond payments: stacks of agent protocols', sub, best_row=False, label_w=340, extra=118, ghost_legend=True, key=KEY_GEN + KEY_SUM)


SCORE = ('Each link scores 2 when every test is met by the core specification (a MUST dependency on an external standard counts), '
         '1 when only some tests are met or a test is met only through an optional extension or a SHOULD/MAY, and 0 when no test is met '
         'or the spec leaves it to another party without saying how. A 0 on any link means the chain is not complete.')
KEY_PAY = [
    ('L1 Principal identity', 'The person or organisation the agent acts for can be identified (by the counterparty, or by a named party on request), is verified by a third party, and that verifier is named and accountable under a trust framework. A self-asserted name or email does not count.'),
    ('L2 Operator identity', 'The company running the agent is identifiable in the same way and verified by an accountable third party. A bare domain with no attestation of who controls it is partial.'),
    ('L3 Agent key binding', 'An accountable party, not the agent itself, states that the agent\'s signing key belongs to the operator or principal, and the key\'s validity (rotation, revocation, expiry) can be checked as at the time of use, including later.'),
    ('L4 Delegation', 'An explicit grant states what the agent may do, carries limits (amount, payee, time window, scope), is signed by the principal\'s own key or authenticator, and expires or can be revoked. A token a platform issues on the principal\'s behalf is partial.'),
    ('L5 Session authentication', 'Each request or session proves possession of the agent\'s key and is protected against replay, and human consent is captured with an assurance level when the grant is made or before a high-risk action.'),
    ('L6 Action within the grant', 'The transaction references the grant it relies on, and the counterparty can check before acting that it falls within the grant\'s limits.'),
    ('L7 Evidence', 'A record of the action is signed by an identifiable, accountable party, carries a time a third party can rely on, and can be re-verified later.'),
    ('L8 Redress', 'Liability is allocated between named roles, and there is a dispute or refund path in the protocol or in a named rulebook (such as card-scheme rules) with the protocol\'s evidence mapped to it. A rulebook without that mapping is partial.'),
    ('L9 Trust anchor', 'A registry, trust list or governance framework says which issuers, operators or agents are trusted, and the credentials and keys the chain relies on can be checked for revocation or status.'),
    ('L10 Continuity', 'The same principal appears in the identity, the grant and the action record, and each artefact cryptographically references the one before it: grant to identity, action to grant, record to action.'),
]
_GEN = {
    'L4 Delegation': 'An explicit grant states what the agent may do, can limit the operation, resource, data scope, recipient, count or rate and time window, is signed by the principal\'s own key or authenticator, and expires or can be revoked. Amount and payee limits alone are partial.',
    'L5 Session authentication': 'Each request or session proves possession of the agent\'s key and is protected against replay, and the protocol defines a human step-up, with an assurance level, before high-risk actions of any kind. Payment-only step-up (such as 3-D Secure) is partial.',
    'L6 Action within the grant': 'Every action, not only payments, references the grant it relies on, and the counterparty can check before acting that this operation on this resource falls within the grant. A scope-only check is partial.',
    'L7 Evidence': 'A signed record states what was done, to which resource and with what inputs; the counterparty\'s response is also signed; the record carries a time a third party can rely on and can be re-verified later.',
    'L8 Redress': 'Responsibility for an unauthorised or mistaken action, including harm that is not monetary (data disclosed, message sent, account changed), is allocated between named roles, and there is a path to contest, reverse or remedy it. Chargebacks alone score 0.',
}
KEY_GEN = [(k, _GEN.get(k, v)) for k, v in KEY_PAY]
KEY_SUM = [
    ('Total', 'The sum of the ten link scores, out of 20. It shows breadth of coverage, not whether the chain holds: a protocol can score well and still have a 0.'),
]
KEY_ADOPT = [
    ('GitHub stars', 'Stars on the protocol\'s main GitHub repository on 25 Nov 2026. A measure of developer attention, not of use.'),
    ('Downloads', 'Installs from 19 Oct to 15 Nov 2026 of packages published by the protocol\'s maintainers on npm, PyPI and crates.io, including automated installs. "No official package" means the maintainers publish none; third-party packages are not counted.'),
]


def key_html(items):
    cells = ''.join(f'<div style="break-inside:avoid;margin:0 0 9px"><b style="color:{INK}">{html.escape(a)}.</b> {html.escape(b)}</div>' for a, b in items)
    return (f'<div style="margin-top:18px;padding-top:14px;border-top:1px solid {GRID};font-size:13px;line-height:1.45;color:{INK2}">'
            f'<div style="font-size:12px;letter-spacing:.04em;color:{MUTED};margin-bottom:8px">WHAT EACH COLUMN MEANS</div>'
            f'<div style="margin-bottom:10px">{html.escape(SCORE)}</div>'
            f'<div style="column-count:2;column-gap:36px">{cells}</div></div>')


CLASSES = [('A', 'Read or', 'retrieve data'), ('B', 'Communicate', 'on their behalf'), ('C', 'Change an', 'account'),
           ('D', 'Legally', 'significant act'), ('E', 'Pay', ''), ('F', 'Instruct', 'another agent')]


def coverage():
    order = sorted(ORDER, key=lambda p: (-sum({'yes': 2, 'partial': 1}.get(GP[p]['classes'][c], 0) for c in 'ABCDEF'), NAMES[p]))
    LW, CW, RH, TOP = 250, 132, 40, 76
    W = LW + CW * 6
    H = TOP + RH * (len(order) + 1) + 14
    fill = {'yes': MET, 'partial': PARTIAL, 'no': ABSENT}
    tc = {'yes': '#ffffff', 'partial': INK, 'no': MUTED}
    svg = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    lx = 0
    for k, lab in (('yes', 'defined in the spec'), ('partial', 'generic hook only'), ('no', 'not covered')):
        svg.append(f'<rect x="{lx}" y="4" width="22" height="16" rx="3" fill="{fill[k]}" stroke="rgba(13,20,33,.10)"/>'
                   f'<text x="{lx+30}" y="17" font-size="13.5" fill="{INK}">{lab}</text>')
        lx += 200
    for i, (c, a, b) in enumerate(CLASSES):
        x = LW + CW * i + CW / 2
        svg.append(f'<text x="{x}" y="{TOP-24}" font-size="13" font-weight="600" fill="{INK}" text-anchor="middle">{a}</text>'
                   f'<text x="{x}" y="{TOP-9}" font-size="13" font-weight="600" fill="{INK}" text-anchor="middle">{b}</text>')
    word = {'yes': 'defined', 'partial': 'hook', 'no': '—'}
    for j, p in enumerate(order):
        y = TOP + RH * j
        svg.append(f'<text x="6" y="{y+RH/2+5}" font-size="14.5" fill="{INK}">{html.escape(NAMES[p])}</text>')
        for i, (c, _, _) in enumerate(CLASSES):
            v = GP[p]['classes'][c]
            x = LW + CW * i
            svg.append(f'<rect x="{x+1}" y="{y+1}" width="{CW-2}" height="{RH-2}" rx="4" fill="{fill[v]}"/>'
                       f'<text x="{x+CW/2}" y="{y+RH/2+5}" font-size="13.5" font-weight="600" fill="{tc[v]}" text-anchor="middle">{word[v]}</text>')
    y = TOP + RH * len(order) + 6
    svg.append(f'<line x1="0" x2="{W}" y1="{y-2}" y2="{y-2}" stroke="{AXIS}"/>'
               f'<text x="6" y="{y+RH/2+5}" font-size="14.5" font-weight="650" fill="{INK}">Protocols defining it</text>')
    for i, (c, _, _) in enumerate(CLASSES):
        n = sum(GP[p]['classes'][c] == 'yes' for p in ORDER)
        svg.append(f'<text x="{LW+CW*i+CW/2}" y="{y+RH/2+5}" font-size="14.5" font-weight="650" fill="{INK}" text-anchor="middle">{n} of {len(ORDER)}</text>')
    svg.append('</svg>')
    sub = ('Which kinds of action each protocol\'s grant and evidence can express. "Defined" means the spec names the scope, operation or constraint for it; '
           '"hook" means only a free-form scope, tool name or custom type exists, with no agreed meaning.')
    return page('What can an agent be authorised to do?', sub, ''.join(svg), W + 100, H + 150, SRC2)


os.makedirs(OUT, exist_ok=True)
sizes = {}
for name, fn in [('payments-1-four-headings', chart1), ('payments-2-chain-by-protocol', pay_protocols), ('payments-3-chain-by-stack', pay_stacks),
                 ('non-payments-1-action-coverage', coverage), ('non-payments-2-chain-by-protocol', gen_protocols), ('non-payments-3-chain-by-stack', gen_stacks)]:
    doc, w, h = fn()
    open(os.path.join(OUT, name + '.html'), 'w').write(doc)
    sizes[name] = (w, h)
json.dump(sizes, open(os.path.join(OUT, 'sizes.json'), 'w'))
print(sizes)
