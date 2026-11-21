import sys; sys.path.insert(0, '/home/claude/work/lt')
from icons import *
from engine import glyph_run
FD = '/home/claude/kit/fonts/'
_tc = {}
def txt(s, font, size, x, y, fill='#fff', anchor='l', track=0, stroke=None, sw=0, op=None, extra=''):
    k = (s, font, size, track)
    if k not in _tc: _tc[k] = glyph_run(s, FD + font + '.ttf', size, track)
    run, wd = _tc[k]; x0 = x - (wd / 2 if anchor == 'm' else wd if anchor == 'r' else 0)
    d = ''.join('<path transform="translate(%s,%s)" d="%s"/>' % (f(x0 + g['x']), f(y), g['d']) for g in run)
    a = 'fill="%s"' % fill if fill else 'fill="none"'
    if stroke: a += ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (stroke, sw)
    if op is not None: a += ' opacity="%s"' % op
    return '<g %s %s>%s</g>' % (a, extra, d), wd
def T(*a, **k): return txt(*a, **k)[0]
D = 12  # loop seconds for entrance choreography
def enter(content, i, kind='up', hold=True):
    t0 = (.12 + .09 * i) / D; t1 = t0 + .55 / D; kt = '0;%s;%s;.93;1' % (f(t0), f(t1)); sp = '0 0 1 1;.16 1 .3 1;0 0 1 1;.5 0 1 1'
    tr = {'up': ('0 26;0 26;0 0;0 0;0 -4', 'translate'), 'left': ('-40 0;-40 0;0 0;0 0;-10 0', 'translate'), 'right': ('40 0;40 0;0 0;0 0;10 0', 'translate'), 'zoom': ('.86;.86;1;1;1.02', 'scale')}[kind]
    if kind == 'zoom': return '<g opacity="0">%s<g>%s%s</g></g>' % (A('opacity', '0;0;1;1;0', '%ss' % D, kt=kt, spl=sp), AT(tr[1], tr[0], '%ss' % D, kt=kt, spl=sp), content)
    return '<g opacity="0">%s<g>%s%s</g></g>' % (A('opacity', '0;0;1;1;0', '%ss' % D, kt=kt, spl=sp), AT(tr[1], tr[0], '%ss' % D, kt=kt, spl=sp), content)
def glow_stroke(d, col, w0=14, op0=.5, n=5, extra=''):
    return ''.join('<path d="%s" stroke="%s" stroke-width="%s" stroke-opacity="%s" fill="none" %s/>' % (d, col, f(w0 * (1 - i / n) + 1), f(op0 * (i + 1) / n / 2.2), extra) for i in range(n))
def pulse(attr, a, b, dur, begin='0s'): return A(attr, '%s;%s;%s' % (a, b, a), dur, begin, spl=S(2, EASE))
def scan(w, h, col='#fff', op=.07, dur='6s', gap=4):
    return '<pattern id="scp" width="%s" height="%s" patternUnits="userSpaceOnUse"><rect width="%s" height="1.4" fill="%s" opacity="%s"/>%s</pattern><rect width="%s" height="%s" fill="url(#scp)"/>' % (w, gap, w, col, op, AT('translate', '0 0;0 %s' % gap, dur, mode='linear') .replace('attributeName="transform"', 'attributeName="patternTransform"'), w, h)
def particles(n, w, h, col, seed, r0=1, r1=2.6, up=True, dur0=5, dur1=11, op=.9, shape='c'):
    rnd = random.Random(seed); o = ''
    for i in range(n):
        x = rnd.uniform(0, w); y0 = h + 10; y1 = rnd.uniform(-20, h * .5); r = rnd.uniform(r0, r1); du = rnd.uniform(dur0, dur1); b = -rnd.uniform(0, du); sw = rnd.uniform(-18, 18)
        shp = '<circle r="%s" fill="%s"/>' % (f(r), col) if shape == 'c' else '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(-r), f(-r), f(2 * r), f(2 * r), col) if shape == 's' else shape
        o += '<g opacity="0">%s<g>%s%s</g></g>' % (A('opacity', '0;%s;%s;0' % (op, op), '%ss' % f(du), '%ss' % f(b), kt='0;.15;.8;1'), AT('translate', '%s %s;%s %s' % (f(x), f(y0 if up else -10), f(x + sw), f(y1 if up else h + 10)), '%ss' % f(du), '%ss' % f(b), mode='linear'), shp)
    return o
def noise(w, h, col, n, seed, op=.4, r=.8):
    rnd = random.Random(seed); return '<g opacity="%s" fill="%s">%s</g>' % (op, col, ''.join('<circle cx="%s" cy="%s" r="%s"/>' % (f(rnd.uniform(0, w)), f(rnd.uniform(0, h)), f(rnd.uniform(.3, r))) for _ in range(n)))
def rope_ring(cx, cy, r, amp, k, col, sw, phase=0):
    pts1 = []; pts2 = []
    for i in range(0, 361, 4):
        a = math.radians(i); m = r + amp * math.sin(k * a + phase); m2 = r - amp * math.sin(k * a + phase)
        pts1.append((cx + m * math.cos(a), cy + m * math.sin(a))); pts2.append((cx + m2 * math.cos(a), cy + m2 * math.sin(a)))
    mk = lambda p: 'M' + 'L'.join('%s %s' % (f(a), f(b)) for a, b in p) + 'Z'
    return '<path d="%s" stroke="%s" stroke-width="%s" fill="none"/><path d="%s" stroke="%s" stroke-width="%s" fill="none" opacity=".75"/>' % (mk(pts1), col, sw, mk(pts2), col, sw)
RAVEN = 'M10 170C4 140 14 108 40 88C50 60 70 38 98 34C112 32 124 38 132 48L172 60L136 66C134 74 128 82 122 88C136 104 142 134 130 158C120 176 100 190 80 196L120 236L58 214L18 238Z'
def raven(x, y, s, eye='#FF4D5E', anim=True):
    return '<g transform="translate(%s,%s) scale(%s)"><path d="%s" fill="#050304"/><path d="M40 92C58 80 74 82 88 96M30 120C60 112 88 120 104 142M34 150C58 146 80 154 92 172" stroke="#2A1218" stroke-width="2.4" stroke-linecap="round" fill="none"/><circle cx="120" cy="52" r="4" fill="%s">%s</circle><path d="M140 56L170 60L140 62Z" fill="#14090C"/></g>' % (f(x), f(y), s, RAVEN, eye, A('opacity', '1;1;.15;1;1', '4.2s', kt='0;.7;.74;.78;1') if anim else '')
def pxrows(rows, pal, u, x=0, y=0):
    out = {}
    for j, row in enumerate(rows):
        i = 0
        while i < len(row):
            c = row[i]
            if c == '.': i += 1; continue
            k = i
            while k + 1 < len(row) and row[k + 1] == c: k += 1
            out.setdefault(c, []).append('M%s %sh%sv%sh-%sz' % (f(x + i * u), f(y + j * u), f((k - i + 1) * u), f(u), f((k - i + 1) * u))); i = k + 1
    return ''.join('<path d="%s" fill="%s"/>' % (''.join(v), pal[c]) for c, v in out.items())
