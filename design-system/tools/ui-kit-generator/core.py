import math, random
def f(v): return ('%.2f' % v).rstrip('0').rstrip('.')
def A(attr, vals, dur, begin='0s', kt=None, spl=None, mode=None, rep='indefinite', tgt=None, fill=None):
    s = '<animate attributeName="%s" values="%s" dur="%s" begin="%s" repeatCount="%s"' % (attr, vals, dur, begin, rep)
    if kt: s += ' keyTimes="%s"' % kt
    if mode: s += ' calcMode="%s"' % mode
    if spl: s += ' calcMode="spline" keySplines="%s"' % spl
    if fill: s += ' fill="freeze"'
    return s + '/>'
def AT(typ, vals, dur, begin='0s', kt=None, spl=None, mode=None, rep='indefinite', additive=None):
    s = '<animateTransform attributeName="transform" type="%s" values="%s" dur="%s" begin="%s" repeatCount="%s"' % (typ, vals, dur, begin, rep)
    if kt: s += ' keyTimes="%s"' % kt
    if mode: s += ' calcMode="%s"' % mode
    if spl: s += ' calcMode="spline" keySplines="%s"' % spl
    if additive: s += ' additive="sum"'
    return s + '/>'
EASE = '.4 0 .2 1'
def S(n, spl): return ';'.join([spl] * n)
def rr(x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    return 'M%s %sH%sA%s %s 0 0 1 %s %sV%sA%s %s 0 0 1 %s %sH%sA%s %s 0 0 1 %s %sV%sA%s %s 0 0 1 %s %sZ' % tuple(map(f, (x + r, y, x + w - r, r, r, x + w, y + r, y + h - r, r, r, x + w - r, y + h, x + r, r, r, x, y + h - r, y + r, r, r, x + r, y)))
def poly(pts): return 'M' + 'L'.join('%s %s' % (f(a), f(b)) for a, b in pts) + 'Z'
def chamfer(x, y, w, h, c): return poly([(x + c, y), (x + w - c, y), (x + w, y + c), (x + w, y + h - c), (x + w - c, y + h), (x + c, y + h), (x, y + h - c), (x, y + c)])
def star4(cx, cy, r, k=.22):
    return poly([(cx, cy - r), (cx + r * k, cy - r * k), (cx + r, cy), (cx + r * k, cy + r * k), (cx, cy + r), (cx - r * k, cy - -r * k), (cx - r, cy), (cx - r * k, cy - r * k)])
def mixc(a, b, t):
    A_ = [int(a[i:i + 2], 16) for i in (1, 3, 5)]; B_ = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02X%02X%02X' % tuple(round(A_[i] + (B_[i] - A_[i]) * t) for i in range(3))
def svg(w, h, body, defs=''):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" fill="none">%s%s</svg>' % (w, h, w, h, ('<defs>%s</defs>' % defs) if defs else '', body)
def lin(id_, stops, x1=0, y1=0, x2=0, y2=1):
    return '<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s">%s</linearGradient>' % (id_, x1, y1, x2, y2, ''.join('<stop offset="%s" stop-color="%s"%s/>' % (o, c, (' stop-opacity="%s"' % a) if a is not None else '') for o, c, *r in stops for a in [r[0] if r else None]))
def sweep(w, h, clip_d, dur='3.2s', col='#FFFFFF', op=.55, wid=26, begin='0s', id_='clp'):
    """diagonal shine band sweeping across, clipped to shape"""
    return ('<clipPath id="%s"><path d="%s"/></clipPath><g clip-path="url(#%s)"><g opacity="%s"><path d="M0 %s L%s %s L%s %s L%s %sZ" fill="%s" transform="translate(-60,0)">%s</path></g></g>' %
            (id_, clip_d, id_, op, f(h), f(wid), f(h), f(wid + 10), 0, 10, 0, col,
             AT('translate', '-60 0;-60 0;%s 0;%s 0' % (f(w + 60), f(w + 60)), dur, begin, kt='0;.35;.7;1', spl='0 0 1 1;.4 0 .2 1;0 0 1 1', additive=None)))
