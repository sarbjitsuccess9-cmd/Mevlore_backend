from comps import *
def star5(cx, cy, R, r=None):
    r = r or R * .45; pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr_ = R if k % 2 == 0 else r; pts.append((cx + rr_ * math.cos(a), cy + rr_ * math.sin(a)))
    return poly(pts)
def edge(sk, kind, w, y):
    """top-edge polyline (list of pts)  -> path 'M..L..' open"""
    pts = [(0, y)]
    if kind == 'arches':
        n = int(w / 26); st = w / n
        d = 'M0 %s' % f(y + 10) + ''.join('Q%s %s %s %s' % (f(k * st + st / 2), f(y - 12), f((k + 1) * st), f(y + 10)) for k in range(n)); return d
    if kind == 'scallop':
        n = int(w / 18); st = w / n; return 'M0 %s' % f(y + 6) + ''.join('a%s %s 0 0 1 %s 0' % (f(st / 2), f(st / 2 * .7), f(st)) for _ in range(n))
    if kind == 'steps':
        d = 'M0 %s' % f(y + 8); x = 0
        while x < w: d += 'H%sV%sH%sV%s' % (f(x + 16), f(y), f(x + 24), f(y + 8)) if False else 'V%sH%sV%sH%s' % (f(y), f(x + 12), f(y + 8), f(x + 24)); x += 24
        return d
    if kind == 'torn':
        rnd = random.Random(5); d = 'M0 %s' % f(y + 2)
        for k in range(int(w / 8) + 1): d += 'L%s %s' % (f(k * 8), f(y + rnd.uniform(-3, 3) + (3 if k % 2 else 0)))
        return d
    return 'M0 %sH%s' % (f(y), f(w))
EDGE = {'goth': 'arches', 'coquette': 'scallop', 'pixel': 'steps', 'grunge': 'torn'}
def bar_style(sk, w, h, uid='n'):
    P = sk.P; k = EDGE.get(sk.id, 'line'); y = 12 if k != 'line' else 1
    e = edge(sk, k, w, y); fillc = P['surf']; d = ''
    body = '<path d="%s V%s H0 Z" fill="%s"/>' % (e, h, fillc)
    if sk.id == 'y2k': body += '<path d="%s" stroke="url(#yb)" stroke-width="2"/><path d="M0 %sH%s" stroke="#FF2EA6" stroke-opacity=".25" stroke-width="6"/>' % (e, y + 3, w); d += lin('yb', [(0, '#38BDF8'), (.5, '#FF2EA6'), (1, '#38BDF8')], 0, 0, 1, 0)
    elif sk.id == 'streetwear': body += '<g><clipPath id="hz"><rect x="0" y="0" width="%s" height="8"/></clipPath><g clip-path="url(#hz)"><g>%s%s</g></g></g>' % (w, ''.join('<path d="M%s 0h8l-8 8h-8z" fill="#F97316"/>' % (x * 16) for x in range(-1, int(w / 16) + 2)), AT('translate', '0 0;16 0', '1.2s', mode='linear'))
    elif sk.id == 'quiet-luxury': body += '<path d="M0 4H%s" stroke="#B48811" stroke-width=".8"/><path d="M0 1H%s" stroke="#1C1917" stroke-width=".8"/>' % (w, w)
    elif sk.id == 'old-money': body += '<path d="M0 1H%s" stroke="#B08D3C" stroke-width="1.2"/><path d="M0 5H%s" stroke="#B08D3C" stroke-width=".7" stroke-dasharray="2 3"/>' % (w, w)
    elif sk.id == 'party-wear': body += '<path d="M0 1H%s" stroke="url(#gold)" stroke-width="2"/>' % w + sweep(w, 6, 'M0 0H%s V6H0Z' % w, '3s', '#fff', .9, 40, id_='nbs')
    elif sk.id == 'pixel': body += '<path d="%s" stroke="#FFD23F" stroke-width="3"/>' % e + '<path d="M0 %sH%s" stroke="#0A0620" stroke-width="4"/>' % (h - 2, w)
    elif sk.id == 'goth': body += '<path d="%s" stroke="#C02638" stroke-width="1.4"/>' % e + ''.join('<path d="M%s %sl2.5 3.5l-2.5 3.5l-2.5 -3.5z" fill="#C02638" transform="translate(0,-4)"/>' % (x * 78 + 39, y - 4) for x in range(5))
    elif sk.id == 'coquette': body += '<path d="%s" stroke="#D96588" stroke-width="1.4"/>' % e
    elif sk.id == 'grunge': body += '<path d="%s" stroke="#D97706" stroke-width="1.2"/>' % e
    elif sk.id == 'casual': body = '<path d="M0 %sV14Q0 0 14 0H%sQ%s 0 %s 14V%sZ" fill="#fff"/><path d="M0 0.8Q0 .8 14 .8H%s" stroke="#E2E8F0"/>' % (h, w - 14, w, w, h, w - 14)
    elif sk.id == 'k-fashion': body += '<path d="M0 .5H%s" stroke="#D6DCE8"/>' % w + ''.join('<path d="M%s 0v6" stroke="#4F6D8A" stroke-width="1"/>' % (x * 78 + 39) for x in range(5))
    else: body += '<path d="%s" stroke="%s" stroke-width="1"/>' % (e, P['bd'])
    return d, body
def navbar(sk, variant='classic', w=390):
    P = sk.P
    if variant == 'classic':
        h = 76; d, b = bar_style(sk, w, h); return wrap(sk, w, h, b, d)
    if variant == 'floating':
        h = 96; iw = w - 28; dd, b = sk.body(iw, 64, 'card', 'f'); sh = '<ellipse cx="%s" cy="%s" rx="%s" ry="6" fill="#000" opacity=".28"><animate attributeName="opacity" values=".28;.2;.28" dur="3s" repeatCount="indefinite"/></ellipse>' % (w / 2, 86, iw / 2 - 18)
        return wrap(sk, w, h, sh + '<g transform="translate(14,14)"><g><animateTransform attributeName="transform" type="translate" values="0 0;0 -2;0 0" dur="3.6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines="%s;%s"/>%s</g></g>' % (EASE, EASE, b), dd)
    h = 88; d, b = bar_style(sk, w, h); cx = w / 2
    ring = '<circle cx="%s" cy="14" r="34" fill="%s" opacity="1"/><circle cx="%s" cy="14" r="34" stroke="%s" stroke-width="1.2"/>' % (cx, P['bg'], cx, P['bd'])
    fab = '<g transform="translate(%s,16)"><circle r="26" stroke="%s" stroke-width="2" opacity=".5">%s%s</circle><g transform="scale(1.9)">%s</g></g>' % (cx, P['acc'], A('r', '26;38', '2s'), A('opacity', '.6;0', '2s'), sk.thumb(0, 0, 8))
    return wrap(sk, w, h, b + ring + fab, d)
def indicator(sk, variant='top'):
    P = sk.P
    if variant == 'top':
        w, h = 78, 14; body = '<path d="M6 7H%s" stroke="%s" stroke-width="1.4" stroke-linecap="round" opacity=".6"/>' % (w - 6, P['acc']) + '<g transform="translate(%s,7)">%s</g>' % (w / 2, '<g>' + AT('scale', '0 0;1 1;1 1', '3s', kt='0;.18;1', spl='.3 1.5 .5 1;0 0 1 1') + sk.thumb(0, 0, 4.5, False) + '</g>')
        return wrap(sk, w, h, body)
    if variant == 'pill':
        w, h = 64, 36; d, b = sk.body(w, h, 'tonal', 'i'); return wrap(sk, w, h, '<g transform="translate(%s,%s)"><g>%s<g transform="translate(%s,%s)">%s</g></g></g>' % (w / 2, h / 2, AT('scale', '.4 .6;1.06 1.06;1 1;1 1', '3s', kt='0;.14;.24;1', spl='.2 1.3 .4 1;.3 0 .6 1;0 0 1 1'), -w / 2, -h / 2, b), d)
    w, h = 40, 40; body = '<circle cx="20" cy="20" r="14" stroke="%s" stroke-width="1.4" opacity=".6"><animate attributeName="r" values="12;19" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="2s" repeatCount="indefinite"/></circle>' % P['acc'] + sk.motif(20, 20, .9)
    return wrap(sk, w, h, body)
def track(sk, x0, x1, y, hgt=6):
    P = sk.P; d = sk.path(x1 - x0, hgt, 0)
    return '<g transform="translate(%s,%s)"><path d="%s" fill="%s"/></g>' % (f(x0), f(y - hgt / 2), d, P['bd'] if not sk.dark else mixc(P['bd'], P['bg'], .2))
def slider(sk, variant='a', w=320):
    P = sk.P; x0, x1 = 14, w - 14; L = x1 - x0
    kt = '0;.5;1'; sp = S(2, '.45 0 .25 1')
    if variant == 'a':
        h = 44; y = 22; clip = '<clipPath id="sl"><rect x="%s" y="0" width="%s" height="%s"><animate attributeName="width" values="%s;%s;%s" dur="4s" repeatCount="indefinite" keyTimes="%s" calcMode="spline" keySplines="%s"/></rect></clipPath>' % (x0, L * .2, h, f(L * .2), f(L * .72), f(L * .2), kt, sp)
        fillb = '<g clip-path="url(#sl)"><g transform="translate(%s,%s)"><path d="%s" fill="%s"/></g></g>' % (x0, y - 3, sk.path(L, 6, 0), P['acc'])
        th = '<g transform="translate(%s,%s)"><animateTransform attributeName="transform" type="translate" values="%s %s;%s %s;%s %s" dur="4s" repeatCount="indefinite" keyTimes="%s" calcMode="spline" keySplines="%s"/>%s</g>' % (0, 0, f(x0 + L * .2), y, f(x0 + L * .72), y, f(x0 + L * .2), y, kt, sp, sk.thumb(0, 0, 9))
        return wrap(sk, w, h, track(sk, x0, x1, y) + fillb + th, clip)
    if variant == 'b':
        h = 70; y = 46; a, b = .22, .7; clip = '<clipPath id="sl"><rect y="0" height="%s"><animate attributeName="x" values="%s;%s;%s" dur="4.4s" repeatCount="indefinite" keyTimes="%s" calcMode="spline" keySplines="%s"/><animate attributeName="width" values="%s;%s;%s" dur="4.4s" repeatCount="indefinite" keyTimes="%s" calcMode="spline" keySplines="%s"/></rect></clipPath>' % (h, f(x0 + L * .22), f(x0 + L * .34), f(x0 + L * .22), kt, sp, f(L * .48), f(L * .5), f(L * .48), kt, sp)
        fillb = '<g clip-path="url(#sl)"><g transform="translate(%s,%s)"><path d="%s" fill="%s"/></g></g>' % (x0, y - 3, sk.path(L, 6, 0), P['acc'])
        def th(xa, xb, lab):
            bub = '<g transform="translate(0,-26)"><path d="M-17 -9H17V9H4L0 15L-4 9H-17Z" fill="%s" stroke="%s" stroke-width="1"/><rect x="-9" y="-2" width="18" height="3" rx="1.5" fill="%s" opacity=".7"/></g>' % (P['surf'], P['acc'], P['ink'] if sk.dark else P['ink'])
            return '<g><animateTransform attributeName="transform" type="translate" values="%s %s;%s %s;%s %s" dur="4.4s" repeatCount="indefinite" keyTimes="%s" calcMode="spline" keySplines="%s"/>%s%s</g>' % (f(x0 + L * xa), y, f(x0 + L * xb), y, f(x0 + L * xa), y, kt, sp, bub, sk.thumb(0, 0, 8.5))
        return wrap(sk, w, h, track(sk, x0, x1, y) + fillb + th(.22, .34, 'a') + th(.70, .84, 'b'), clip)
    h = 52; y = 24; n = 5; steps = [x0 + L * k / (n - 1) for k in range(n)]
    tk = ''.join('<path d="M%s %sv%s" stroke="%s" stroke-width="1.4" opacity=".6"/>' % (f(x), y + 8, 6, P['acc2']) for x in steps) + ''.join('<g transform="translate(%s,%s)">%s</g>' % (f(x), y, '<circle r="3" fill="%s"/>' % P['bd']) for x in steps)
    vals = ';'.join('%s %s' % (f(steps[i]), y) for i in (0, 1, 1, 3, 3, 4, 4, 2, 2, 0)); kts = ';'.join(f(k / 9) for k in range(10))
    th = '<g><animateTransform attributeName="transform" type="translate" values="%s" dur="7s" repeatCount="indefinite" keyTimes="%s" calcMode="spline" keySplines="%s"/>%s</g>' % (vals, kts, S(9, '.5 0 .2 1.2'), sk.thumb(0, 0, 9))
    return wrap(sk, w, h, track(sk, x0, x1, y) + tk + th)
def pip(sk, cx, cy, r, on):
    P = sk.P; c = P['acc'] if on else P['bd'] if not sk.dark else mixc(P['bd'], '#ffffff', .15)
    if sk.id == 'goth': return '<path d="M%s %sL%s %sL%s %sL%s %sZ" fill="%s"/>' % (f(cx), f(cy - r - 1), f(cx + r), f(cy), f(cx), f(cy + r + 1), f(cx - r), f(cy), c)
    if sk.id == 'coquette': return '<path d="M%s %sC%s %s %s %s %s %sC%s %s %s %s %s %sC%s %s %s %s %s %sZ" fill="%s"/>' % (f(cx), f(cy + r), f(cx - r * 1.6), f(cy), f(cx - r), f(cy - r * 1.2), f(cx), f(cy - r * .4), f(cx + r), f(cy - r * 1.2), f(cx + r * 1.6), f(cy), f(cx), f(cy + r), f(cx), f(cy), f(cx), f(cy), f(cx), f(cy), c)
    if sk.id in ('pixel', 'streetwear', 'grunge'): return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(cx - r), f(cy - r), f(2 * r), f(2 * r), c)
    if sk.id in ('quiet-luxury', 'old-money', 'k-fashion'): return '<path d="M%s %sL%s %sL%s %sL%s %sZ" fill="%s"/>' % (f(cx), f(cy - r - 1), f(cx + r), f(cy), f(cx), f(cy + r + 1), f(cx - r), f(cy), c) if sk.id != 'k-fashion' else '<circle cx="%s" cy="%s" r="%s" %s/>' % (f(cx), f(cy), f(r), ('fill="%s"' % c) if on else 'stroke="%s" stroke-width="1.2"' % P['acc2'])
    if sk.id in ('y2k', 'party-wear'): return '<path d="%s" fill="%s"/>' % (star4(cx, cy, r * 1.5, .3), c)
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), c)
def pager(sk, variant='dots'):
    P = sk.P
    if variant == 'dots':
        w, h, n, gap = 132, 24, 5, 24; xs = [14 + k * gap for k in range(n)]; body = ''.join(pip(sk, x, 12, 4, False) for x in xs)
        vals = ';'.join('%s 12' % x for x in xs + xs[-2::-1][:3]); 
        seq = xs + xs[-2:0:-1]; vals = ';'.join('%s 12' % f(x) for x in seq) + ';%s 12' % f(xs[0]); kt = ';'.join(f(k / len(seq)) for k in range(len(seq) + 1))
        body += '<g><animateTransform attributeName="transform" type="translate" values="%s" dur="6s" repeatCount="indefinite" keyTimes="%s" calcMode="spline" keySplines="%s"/>%s<g>%s</g></g>' % (vals, kt, S(len(seq), '.5 0 .2 1'), pip(sk, 0, 0, 5.2, True), '')
        return wrap(sk, w, h, body)
    if variant == 'line':
        w, h, n = 180, 16, 4; sw_ = (w - 3 * 6) / n; body = ''
        for k in range(n):
            x = k * (sw_ + 6); body += '<g transform="translate(%s,6)"><path d="%s" fill="%s"/><clipPath id="p%s"><rect width="%s" height="4"><animate attributeName="width" values="0;0;%s;%s" dur="8s" begin="%ss" repeatCount="indefinite" keyTimes="0;.0001;.2;1" calcMode="linear"/></rect></clipPath></g>' % (f(x), sk.path(sw_, 4, 0), P['bd'], k, f(sw_), f(sw_), k * 0) if False else '<g transform="translate(%s,6)"><path d="%s" fill="%s"/><clipPath id="p%s"><rect width="0" height="4"><animate attributeName="width" values="0;0;%s;%s;0" dur="8s" repeatCount="indefinite" keyTimes="%s"/></rect></clipPath><g clip-path="url(#p%s)"><path d="%s" fill="%s"/></g></g>' % (f(x), sk.path(sw_, 4, 0), P['bd'], k, f(sw_), f(sw_), ';'.join(f(v) for v in (0, k * .25, k * .25 + .2, .999 if k == 3 else .999, 1)) if False else '0;%s;%s;.99;1' % (f(k * .22), f(k * .22 + .22)), k, sk.path(sw_, 4, 0), P['acc'])
        return wrap(sk, w, h, body)
    w, h = 120, 36; body = sk.motif(18, 18, .9) + '<g>%s</g>' % ''.join('<path d="M%s 18H%s" stroke="%s" stroke-width="1.4" stroke-linecap="round" stroke-dasharray="2 6" opacity=".7"/>' % (36, 108, P['acc']) for _ in [0])
    body += '<g transform="translate(108,18)"><g>%s%s</g></g>' % (AT('translate', '0 0;-72 0;-72 0;0 0', '4s', kt='0;.45;.55;1', spl='.5 0 .2 1;0 0 1 1;.5 0 .2 1'), sk.thumb(0, 0, 5))
    return wrap(sk, w, h, body)
def loader(sk, variant='spin'):
    P = sk.P
    if variant == 'spin':
        w = h = 72; n = 10; o = ''
        for k in range(n):
            a = 2 * math.pi * k / n; x = 36 + 24 * math.cos(a); y = 36 + 24 * math.sin(a)
            o += '<g opacity=".15">%s%s</g>' % (A('opacity', '1;.12', '1.2s', begin='%ss' % f(-1.2 * (n - k) / n) if False else '%ss' % f(1.2 * k / n)), pip(sk, x, y, 3.2, True))
        return wrap(sk, w, h, o + sk.motif(36, 36, 1.1))
    if variant == 'bar':
        w, h = 220, 24; d = sk.path(w - 4, 12, 0); cp = '<clipPath id="lb"><path d="%s"/></clipPath>' % d
        o = '<g transform="translate(2,6)"><path d="%s" fill="%s"/><g clip-path="url(#lb)"><rect width="0" height="12" fill="%s"><animate attributeName="width" values="0;%s;%s" dur="3s" repeatCount="indefinite" keyTimes="0;.85;1" calcMode="spline" keySplines="%s;0 0 1 1"/></rect><g opacity=".5">%s</g></g></g>' % (d, P['bd'], P['acc'], w - 4, w - 4, EASE, '<rect x="-40" width="30" height="12" fill="#fff" transform="skewX(-20)">%s</rect>' % A('x', '-40;%s' % (w + 20), '1.2s'))
        return wrap(sk, w, h, o, cp)
    w, h = 240, 150; bl = mixc(P['bd'], P['bg'], .35); o = '<rect width="240" height="110" rx="%s" fill="%s"/><rect y="122" width="150" height="10" rx="5" fill="%s"/><rect y="138" width="90" height="8" rx="4" fill="%s"/>' % (min(sk.r, 12), bl, bl, bl)
    o += '<clipPath id="sk"><rect width="240" height="150"/></clipPath><g clip-path="url(#sk)"><rect x="-80" width="70" height="150" fill="#fff" opacity="%s" transform="skewX(-18)">%s</rect></g>' % (.5 if not sk.dark else .1, A('x', '-80;300', '1.6s'))
    return wrap(sk, w, h, o)
def toggle(sk):
    P = sk.P; w, h = 72, 40; d = sk.path(w, h, 1); off = mixc(P['bd'], P['bg'], .3) if sk.dark else P['bd']
    track_ = '<path d="%s" fill="%s"/><path d="%s" fill="%s" opacity="0">%s</path><path d="%s" stroke="%s" stroke-width="1.2" opacity=".6"/>' % (d, off, d, P['acc'], A('opacity', '0;0;1;1;0', '4s', kt='0;.15;.3;.7;.85' if False else '0;.2;.35;.7;.85'), d, P['bd'] if not sk.dark else P['acc2'])
    kn = '<g><animateTransform attributeName="transform" type="translate" values="%s 20;%s 20;%s 20;%s 20;%s 20" dur="4s" repeatCount="indefinite" keyTimes="0;.2;.35;.7;.85" calcMode="spline" keySplines="0 0 1 1;.3 1.4 .5 1;0 0 1 1;.3 1.4 .5 1"/>%s</g>' % (22, 22, 50, 50, 22, sk.thumb(0, 0, 11))
    return wrap(sk, w, h, track_ + kn)
def checkbox(sk, radio=False):
    P = sk.P; w = h = 36; d = '<circle cx="18" cy="18" r="13"/>' if radio else '<path d="%s"/>' % sk.path(28, 28, 0)
    box = ('<g transform="translate(4,4)">' if not radio else '<g>') + d.replace('/>', ' stroke="%s" stroke-width="1.6" fill="none"/>' % P['acc2']) + '</g>'
    fillbox = d.replace('/>', ' fill="%s"/>' % P['acc'])
    fb = ('<g transform="translate(4,4)">' if not radio else '<g>') + fillbox + '</g>'
    if radio: mark = '<circle cx="18" cy="18" r="5" fill="%s"><animate attributeName="r" values="0;0;6.5;5;5;0" dur="3.6s" keyTimes="0;.2;.3;.35;.8;.9" repeatCount="indefinite"/></circle>' % P['acc']; return wrap(sk, w, h, box + mark)
    chk = '<path d="M11 18.5l5 5 9-11" stroke="%s" stroke-width="3" stroke-linecap="square" stroke-linejoin="miter" stroke-dasharray="26" stroke-dashoffset="26"><animate attributeName="stroke-dashoffset" values="26;26;0;0;26" dur="3.6s" keyTimes="0;.2;.35;.8;.9" repeatCount="indefinite"/></path>' % (P['bg'] if not sk.dark else '#0b0b0b' if sk.id not in ('goth',) else '#fff')
    return wrap(sk, w, h, box + '<g opacity="0">%s%s</g>' % (A('opacity', '0;0;1;1;0', '3.6s', kt='0;.2;.3;.8;.9'), fb) + chk)
def chip(sk, selected=False):
    P = sk.P; w, h = 116, 40; role = 'primary' if selected else 'ghost'; d, b = sk.body(w, h, 'tonal', 'c'); d2, b2 = sk.body(w, h, 'primary', 'c2')
    clip = '<clipPath id="ch"><path d="%s"/></clipPath>' % sk.path(w, h, 1)
    o = '<g>%s</g><g opacity="0">%s%s</g>' % (b if not sk.id == 'streetwear' else b, A('opacity', '0;0;1;1;0', '4s', kt='0;.2;.28;.8;.9'), b2)
    return wrap(sk, w, h, o + '<g transform="translate(%s,%s)">%s</g>' % (w - 22, h / 2, '<g opacity="0">%s%s</g>' % (A('opacity', '0;0;1;1;0', '4s', kt='0;.25;.3;.8;.9'), '<path d="M-5 0l3.5 3.5 6.5 -7" stroke="%s" stroke-width="2" stroke-linecap="square"/>' % (P['bg'] if not sk.dark else '#111'))), d + d2)
def badge(sk, kind='sale'):
    P = sk.P
    if kind == 'count':
        w = h = 28; o = '<circle cx="14" cy="14" r="9" stroke="%s" stroke-width="1.4"><animate attributeName="r" values="9;14" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="1.6s" repeatCount="indefinite"/></circle>' % P['acc'] + '<g transform="translate(14,14)"><g>%s%s</g></g>' % (AT('scale', '1;1.14;1', '1.6s', spl=S(2, EASE)), pip(sk, 0, 0, 9, True) if sk.id not in ('pixel', 'streetwear', 'grunge') else '<rect x="-9" y="-9" width="18" height="18" fill="%s"/>' % P['acc'])
        return wrap(sk, w, h, o)
    if kind == 'new':
        w, h = 72, 28; d, b = sk.body(w, h, 'primary', 'n'); return wrap(sk, w, h, '<g transform="translate(%s,%s)"><g>%s<g transform="translate(%s,%s)">%s</g></g></g>' % (w / 2, h / 2, AT('rotate', '-3;3;-3', '3s', spl=S(2, EASE)), -w / 2, -h / 2, b), d)
    w = h = 84; pts = []
    for k in range(24):
        a = 2 * math.pi * k / 24; r_ = 40 if k % 2 == 0 else 34; pts.append((42 + r_ * math.cos(a), 42 + r_ * math.sin(a)))
    o = '<g transform="translate(42,42)"><g>%s<g transform="translate(-42,-42)"><path d="%s" fill="%s"/><path d="%s" stroke="%s" stroke-width="1" stroke-dasharray="2 3" opacity=".7"/></g></g></g>' % (AT('rotate', '0;360', '16s'), poly(pts), P['acc'], 'M42 12a30 30 0 1 0 .01 0Z', '#fff' if sk.id != 'minimal' else '#fff') + '<g transform="translate(42,42)"><g>%s%s</g></g>' % (AT('scale', '1;1.1;1', '1.4s', spl=S(2, EASE)), '<rect x="-20" y="-3" width="40" height="6" rx="3" fill="#fff" opacity=".9"/><rect x="-12" y="-13" width="24" height="5" rx="2.5" fill="#fff" opacity=".7"/><rect x="-14" y="8" width="28" height="5" rx="2.5" fill="#fff" opacity=".7"/>')
    return wrap(sk, w, h, o)
def toast(sk):
    P = sk.P; w, h = 360, 76; d, b = sk.body(w - 16, 56, 'card', 't')
    ic = '<g transform="translate(34,28)"><circle r="14" fill="%s"/><path d="M-6 0l4 4 8 -9" stroke="%s" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="20" stroke-dashoffset="20">%s</path></g>' % (P['acc'], '#fff' if sk.id not in ('pixel', 'party-wear', 'quiet-luxury') else '#111', A('stroke-dashoffset', '20;20;0;0;20', '5s', kt='0;.18;.3;.85;1'))
    bars = '<rect x="62" y="17" width="140" height="7" rx="3.5" fill="%s" opacity=".85"/><rect x="62" y="31" width="200" height="6" rx="3" fill="%s" opacity=".45"/>' % (P['ink'], P['ink2'])
    anim = AT('translate', '0 40;0 0;0 0;0 -10', '5s', kt='0;.12;.85;1', spl='.2 1.2 .4 1;0 0 1 1;.5 0 1 1') ; op = A('opacity', '0;1;1;0', '5s', kt='0;.1;.85;1')
    return wrap(sk, w, h, '<g>%s%s<g transform="translate(8,10)">%s%s%s</g></g>' % (anim, op, b, ic, bars), d)
def divider(sk, variant='a'):
    P = sk.P; w, h = 320, 24
    if variant == 'a':
        o = '<path d="M8 12H%s M%s 12H%s" stroke="%s" stroke-width="1.2" stroke-linecap="round" opacity=".8"/>' % (w / 2 - 22, w / 2 + 22, w - 8, P['acc'] if sk.id not in ('minimal',) else P['acc2']) + sk.motif(w / 2, 12, .9)
        return wrap(sk, w, h, o)
    n = 17; o = ''.join('<g transform="translate(%s,12)">%s</g>' % (f(10 + k * 18.5), '<g>%s%s</g>' % (A('opacity', '.25;1;.25', '2.4s', begin='%ss' % f(k * .14)), pip(sk, 0, 0, 2.6, True))) for k in range(n))
    return wrap(sk, w, h, o)
def rating(sk):
    P = sk.P; w, h = 132, 28; o = ''
    for k in range(5):
        x = 14 + k * 26; base = '<path d="%s" stroke="%s" stroke-width="1.2" opacity=".6"/>' % (star5(x, 14, 10), P['acc2'])
        fl = '<path d="%s" fill="%s" opacity="0">%s</path>' % (star5(x, 14, 10), P['acc'], A('opacity', '0;0;1;1;0', '4.5s', kt='0;%s;%s;.85;.95' % (f(.05 + k * .1), f(.14 + k * .1))))
        sc = '<g transform="translate(%s,14)"><g>%s<g transform="translate(%s,-14)">%s</g></g></g>' % (x, AT('scale', '1;1;1.35;1;1', '4.5s', kt='0;%s;%s;%s;1' % (f(.05 + k * .1), f(.1 + k * .1), f(.16 + k * .1))), -x, base + fl)
        o += sc
    return wrap(sk, w, h, o)
def search(sk):
    P = sk.P; w, h = 340, 52; d, b = sk.body(w, h, 'ghost', 's')
    ic = '<g transform="translate(26,26)"><g>%s<circle cx="-1" cy="-1" r="6" stroke="%s" stroke-width="2"/><path d="M3.5 3.5L8 8" stroke="%s" stroke-width="2" stroke-linecap="round"/></g></g>' % (AT('rotate', '0;-14;0;0', '3s', kt='0;.1;.2;1'), P['acc'], P['acc'])
    ph = '<rect x="50" y="22" width="0" height="8" rx="4" fill="%s" opacity=".5"><animate attributeName="width" values="0;0;150;150;0" dur="5s" keyTimes="0;.1;.55;.9;1" repeatCount="indefinite"/></rect>' % P['ink2'] + '<rect x="50" y="19" width="2" height="14" fill="%s"><animate attributeName="x" values="50;50;200;200;50" dur="5s" keyTimes="0;.1;.55;.9;1" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0;1" dur=".9s" repeatCount="indefinite"/></rect>' % P['acc']
    return wrap(sk, w, h, b + ic + ph, d)
def stepper(sk):
    P = sk.P; w, h = 132, 44; d, b = sk.body(w, h, 'ghost', 'q')
    pm = '<path d="M16 22H28" stroke="%s" stroke-width="2.2" stroke-linecap="round"/><path d="M104 22H116M110 16V28" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>' % (P['acc'], P['acc'])
    num = '<g transform="translate(66,22)"><g>%s<rect x="-4" y="-9" width="8" height="18" rx="2" fill="%s"/></g></g>' % (AT('translate', '0 14;0 0;0 0;0 -14', '3s', kt='0;.15;.85;1', spl='.2 1 .4 1;0 0 1 1;.6 0 1 1'), P['ink'])
    return wrap(sk, w, h, b + '<g>%s%s</g>' % (AT('scale', '1;1;1.2;1', '3s', kt='0;.7;.78;1'), '') + pm + num, d)
def price_tag(sk):
    P = sk.P; w, h = 104, 40; d, b = sk.body(w, h, 'primary', 'p'); hole = '<circle cx="14" cy="20" r="3.5" fill="%s"/>' % P['bg']
    return wrap(sk, w, h, '<g transform="translate(%s,%s)"><g>%s<g transform="translate(%s,%s)">%s%s<rect x="28" y="16" width="60" height="8" rx="4" fill="%s" opacity=".85"/></g></g></g>' % (w / 2, h / 2, AT('rotate', '-2;2;-2', '3.4s', spl=S(2, EASE)), -w / 2, -h / 2, b, hole, '#fff' if not (sk.id in ('quiet-luxury', 'pixel', 'party-wear', 'old-money', 'minimal', 'k-fashion')) else '#fff'), d)
def fab(sk):
    P = sk.P; w = h = 76; body = '<circle cx="38" cy="38" r="26" stroke="%s" stroke-width="2"><animate attributeName="r" values="26;37" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;0" dur="2s" repeatCount="indefinite"/></circle>' % P['acc']
    body += '<g transform="translate(38,38)"><g>%s<g transform="scale(2.1)">%s</g></g></g>' % (AT('scale', '1;1.06;1', '2s', spl=S(2, EASE)), sk.thumb(0, 0, 11, False))
    body += '<g transform="translate(38,39)"><path d="M-6 -4h12l-1 10h-10zM-3 -4v-1.5a3 3 0 0 1 6 0v1.5" stroke="%s" stroke-width="1.8" stroke-linejoin="round" fill="none"/></g>' % ('#fff' if sk.id in ('goth', 'y2k', 'streetwear', 'coquette', 'casual', 'minimal', 'grunge', 'old-money') else '#111')
    return wrap(sk, w, h, body)
def card(sk, variant='a'):
    P = sk.P; w, h = (200, 260)
    d, b = sk.body(w, h, 'card', 'cd'); o = b
    if variant == 'b':
        o += '<g transform="translate(%s,%s)">%s</g>' % (w - 62, 14, '<g>%s%s</g>' % (A('opacity', '.8;1;.8', '2s'), sk.body(50, 20, 'primary', 'ct')[1]))
        d += sk.body(50, 20, 'primary', 'ct')[0]
    o += '<g transform="translate(18,%s)"><rect width="%s" height="%s" rx="%s" fill="%s" opacity=".5"/></g>' % (h - 44, w - 36, 8, 4, P['bd'])
    return wrap(sk, w, h, o, d)
COMPONENTS = [('button', lambda s: button(s, 'primary')), ('button_ghost', lambda s: button(s, 'ghost')), ('button_tonal', lambda s: button(s, 'tonal')),
    ('button_compact', lambda s: button(s, 'primary', 150, 44)), ('fab', fab), ('navbar', lambda s: navbar(s, 'classic')), ('navbar_floating', lambda s: navbar(s, 'floating')), ('navbar_dock', lambda s: navbar(s, 'dock')),
    ('nav_indicator', lambda s: indicator(s, 'top')), ('nav_indicator_pill', lambda s: indicator(s, 'pill')), ('nav_indicator_pulse', lambda s: indicator(s, 'pulse')),
    ('slider', lambda s: slider(s, 'a')), ('slider_range', lambda s: slider(s, 'b')), ('slider_steps', lambda s: slider(s, 'c')),
    ('pager', lambda s: pager(s, 'dots')), ('pager_line', lambda s: pager(s, 'line')), ('pager_motif', lambda s: pager(s, 'motif')),
    ('loader', lambda s: loader(s, 'spin')), ('loader_bar', lambda s: loader(s, 'bar')), ('loader_skeleton', lambda s: loader(s, 'skel')),
    ('toggle', toggle), ('checkbox', checkbox), ('radio', lambda s: checkbox(s, True)), ('chip', chip), ('badge_count', lambda s: badge(s, 'count')), ('badge_new', lambda s: badge(s, 'new')), ('badge_sale', lambda s: badge(s, 'sale')),
    ('toast', toast), ('divider', lambda s: divider(s, 'a')), ('divider_dots', lambda s: divider(s, 'b')), ('rating', rating), ('search_bar', search), ('stepper', stepper), ('price_tag', price_tag),
    ('card_frame', lambda s: card(s, 'a')), ('card_frame_tag', lambda s: card(s, 'b'))]
if __name__ == '__main__':
    import os, sys
    from playwright.sync_api import sync_playwright
    only = sys.argv[1].split(',') if len(sys.argv) > 1 else None; skins = [s for s in SKINS if (not only or s.id in only)]
    os.makedirs('t/f', exist_ok=True); h = '<body style="margin:0;background:#888;font:10px sans-serif">'
    for sk in skins:
        h += '<div style="display:flex;flex-wrap:wrap;gap:10px;padding:8px;background:%s;margin:2px;align-items:center"><b style="width:70px;color:#999">%s</b>' % (sk.P['bg'], sk.id)
        for n, fn in COMPONENTS:
            try: s = fn(sk)
            except Exception as e: print('ERR', sk.id, n, repr(e)); continue
            p = 't/f/%s_%s.svg' % (sk.id, n); open(p, 'w').write(s); h += '<img src="f/%s_%s.svg">' % (sk.id, n)
        h += '</div>'
    open('t/c.html', 'w').write(h)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); pg.goto('file:///home/claude/kit/t/c.html'); pg.wait_for_timeout(1800); pg.screenshot(path='t/c.png', full_page=True); b.close()
