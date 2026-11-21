from comps2 import *
import io, cairosvg
from PIL import Image
import numpy as np
# glyph parts: (kind, d, anim)  kind: 's' stroke / 'f' fill-region (active) ; anim: None|(type,pivot,amp)
G = {
 'home': dict(fill='M5.5 10.2 12 4.6l6.5 5.6v10.3h-5v-5.5h-3v5.5h-5Z', parts=[('M3 11.5 12 3.8l9 7.7', ('ty', 0, -1.4)), ('M5.5 10v10.5h5v-6h3v6h5V10', None), ('M16.5 7.5V4.5h2.2v5', None)], acc=[('M11 14.5h2', None)]),
 'discover': dict(fill='M12 3a9 9 0 1 0 .01 0Z', parts=[('M12 3a9 9 0 1 0 .01 0Z', None), ('M12 3v1.6M12 19.4V21M3 12h1.6M19.4 12H21', None)], needle=('M15.8 8.2 13.6 13.6 8.2 15.8 10.4 10.4Z', ('rot', (12, 12), 40))),
 'videos': dict(fill='M3.5 6.5h17v11h-17Z', parts=[('M3.5 9a2.5 2.5 0 0 1 2.5-2.5h12A2.5 2.5 0 0 1 20.5 9v6a2.5 2.5 0 0 1-2.5 2.5H6A2.5 2.5 0 0 1 3.5 15Z', None)], needle=('M10.2 9.6v4.8l4.2-2.4Z', ('pulse', (12.2, 12), 1.25))),
 'elite': dict(fill='M3.5 8.5 8 12.2l4-6.7 4 6.7 4.5-3.7-1.8 10H5.3Z', parts=[('M3.5 8.5 8 12.2l4-6.7 4 6.7 4.5-3.7-1.8 10H5.3Z', ('ty', 0, -1.2)), ('M6 15.6h12', None)], acc=[('M12 9.4l.9 1.3-.9 1.3-.9-1.3Z', ('pulse', (12, 10.7), 1.5))]),
 'bag': dict(fill='M5.2 8h13.6l-1 12.5H6.2Z', parts=[('M5.2 8h13.6l-1 12.5H6.2Z', None)], needle=('M9 8V6.6a3 3 0 0 1 6 0V8', ('rot', (12, 8), 9))),
 'heart': dict(fill='M12 20C5.5 15.4 3.5 11.8 3.5 9A4.4 4.4 0 0 1 12 7.2 4.4 4.4 0 0 1 20.5 9c0 2.8-2 6.4-8.5 11Z', parts=[('M12 20C5.5 15.4 3.5 11.8 3.5 9A4.4 4.4 0 0 1 12 7.2 4.4 4.4 0 0 1 20.5 9c0 2.8-2 6.4-8.5 11Z', ('pulse', (12, 13), 1.16))], acc=[]),
 'search': dict(fill='M10.5 4a6.5 6.5 0 1 0 .01 0Z', parts=[('M10.5 4a6.5 6.5 0 1 0 .01 0Z', None)], needle=('M15.3 15.3 20.5 20.5', ('rot', (10.5, 10.5), 12))),
 'profile': dict(fill='M4.5 20.5c1-4.2 4-6 7.5-6s6.5 1.8 7.5 6Z', parts=[('M12 4a4 4 0 1 0 .01 0Z', ('ty', 0, -1.3)), ('M4.5 20.5c1-4.2 4-6 7.5-6s6.5 1.8 7.5 6', None)], acc=[]),
 'filter': dict(fill=None, parts=[('M4 7h16M4 12h16M4 17h16', None)], knobs=[(8, 7, 7), (15, 12, -6), (10, 17, 6)]),
 'bell': dict(fill='M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15Z', parts=[('M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15Z', ('rot', (12, 4), 10))], needle=('M10 21a2 2 0 0 0 4 0', ('ty', 0, 1))),
}
ICON_STYLE = {  # sw, cap, join, idle color, act color
 'goth': (1.5, 'square', 'miter'), 'coquette': (1.6, 'round', 'round'), 'y2k': (1.8, 'round', 'round'), 'streetwear': (2.3, 'square', 'miter'), 'k-fashion': (1.2, 'butt', 'miter'),
 'quiet-luxury': (1.1, 'butt', 'miter'), 'pixel': (2, 'square', 'miter'), 'minimal': (1.5, 'round', 'round'), 'grunge': (1.7, 'square', 'bevel'), 'old-money': (1.2, 'butt', 'round'), 'casual': (2, 'round', 'round'), 'party-wear': (1.5, 'round', 'round')}
def motion(content, a, dur='2.8s', begin='0s'):
    if not a: return content
    t, pv, amp = a
    if t == 'ty': return '<g>%s%s</g>' % (AT('translate', '0 0;0 %s;0 0;0 0' % amp, dur, begin, kt='0;.12;.26;1', spl='.3 1.5 .5 1;.4 0 .6 1;0 0 1 1'), content)
    if t == 'rot':
        x, y = pv; return '<g transform="translate(%s,%s)"><g>%s<g transform="translate(%s,%s)">%s</g></g></g>' % (x, y, AT('rotate', '0;%s;%s;%s;0;0' % (amp, -amp, amp / 2), dur, begin, kt='0;.1;.2;.3;.38;1', spl=S(5, '.4 0 .6 1')), -x, -y, content)
    if t == 'pulse':
        x, y = pv; return '<g transform="translate(%s,%s)"><g>%s<g transform="translate(%s,%s)">%s</g></g></g>' % (x, y, AT('scale', '1;%s;.94;1;1' % amp, dur, begin, kt='0;.12;.24;.36;1', spl=S(4, '.4 0 .6 1')), -x, -y, content)
    return content
def glyph_svg(sk, name, active, px=False):
    P = sk.P; g = G[name]; sw, cap, join = ICON_STYLE[sk.id]; col = P['acc'] if active else (P['ink2'] if sk.id not in ('old-money',) else P['acc2'])
    if sk.id == 'party-wear' and active: col = 'url(#gold)'
    if sk.id == 'y2k' and active: col = '#FF7BC8'
    st = 'stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="%s"' % (col, sw, cap, join)
    o = ''
    fillc = P['acc'] if sk.id != 'party-wear' else '#D4AF37'
    if active and g.get('fill'): o += '<path d="%s" fill="%s" fill-opacity="%s"/>' % (g['fill'], fillc, .25 if sk.id not in ('pixel', 'streetwear') else .5)
    stroke_parts = ''
    for d, a in g['parts']: stroke_parts += motion('<path d="%s" %s fill="none"/>' % (d, st), a if active else None)
    if 'needle' in g:
        d, a = g['needle']; stroke_parts += motion('<path d="%s" %s fill="%s"/>' % (d, st, col if name in ('discover', 'videos') and active else 'none'), a if active else None)
    for d, a in g.get('acc', []): stroke_parts += motion('<path d="%s" fill="%s"/>' % (d, col if active else 'none'), a if active else None) if active else ''
    if 'knobs' in g:
        for cx, cy, dx in g['knobs']:
            kn = '<circle cx="%s" cy="%s" r="2.2" %s fill="%s"/>' % (cx, cy, st, P['bg'] if not active else P['surf'])
            stroke_parts += ('<g>%s%s</g>' % (AT('translate', '0 0;%s 0;0 0;0 0' % dx, '2.8s', kt='0;.2;.45;1', spl=S(3, '.4 0 .2 1')), kn)) if active else kn
    o += stroke_parts
    if active:  # world-specific accent decoration
        if sk.id == 'goth': o += '<g transform="translate(19.5,4)"><path d="M0 -2.4 1.6 0 0 2.4 -1.6 0Z" fill="#FF7A8A">%s</path></g>' % A('opacity', '1;.2;1', '2s')
        if sk.id == 'coquette': o += '<g transform="translate(19.5,4.5) scale(.34)">%s</g>' % ''.join(['<path d="M0 0C-12 -10 -17 -1 -13 6C-9 13 -3 7 0 0Z" fill="#E8A5BA"/><path d="M0 0C12 -10 17 -1 13 6C9 13 3 7 0 0Z" fill="#E8A5BA"/><circle r="3.6" fill="#D96588"/>'])
        if sk.id == 'y2k': o += '<g transform="translate(20,4)"><path d="%s" fill="#fff">%s%s</path></g>' % (star4(0, 0, 3.4), AT('scale', '.4;1.2;.4', '1.6s', spl=S(2, EASE)), '')
        if sk.id == 'streetwear': o += '<rect x="5" y="22.3" width="14" height="2" fill="#F97316"><animate attributeName="width" values="0;14;14;0" dur="2.8s" keyTimes="0;.2;.8;1" repeatCount="indefinite"/></rect>'
        if sk.id == 'k-fashion': o += '<path d="M2 5V2h3M22 5V2h-3M2 19v3h3M22 19v3h-3" stroke="#4F6D8A" stroke-width=".9"/>'
        if sk.id == 'quiet-luxury': o += '<path d="M12 22.2l.9-.9-.9-.9-.9.9Z" fill="#B48811"/>'
        if sk.id == 'minimal': o += '<circle cx="12" cy="22.4" r="1" fill="#18181B"/>'
        if sk.id == 'grunge': o += '<path d="M3 22.5l18-.6" stroke="#D97706" stroke-width="1.2" stroke-dasharray="4 2"/>'
        if sk.id == 'old-money': o += '<path d="M7 22.4h10" stroke="#B08D3C" stroke-width=".8"/><circle cx="12" cy="22.4" r="1.1" fill="#B08D3C"/>'
        if sk.id == 'casual': o += '<path d="M19 3.5c2 0 3 1 3 3-2 0-3-1-3-3Z" fill="#10B981">%s</path>' % AT('rotate', '-10 19 6;10 19 6;-10 19 6', '2s', spl=S(2, EASE))
        if sk.id == 'party-wear': o += '<g transform="translate(19.5,4.5)"><path d="%s" fill="#FFF1B0">%s</path></g>' % (star4(0, 0, 3.4), AT('scale', '.3;1.1;.3', '1.8s', spl=S(2, EASE)))
    if sk.id == 'streetwear' and active:  # hard offset shadow
        o = '<g transform="translate(1.2,1.2)" opacity=".9" style="filter:none"><g stroke-opacity="1">%s</g></g>' % o.replace(col, '#38BDF8') + o
    return o
def pixel_icon(sk, name, active):
    """rasterise glyph to 16px grid -> merged rects, stepped bob when active"""
    P = sk.P; g = G[name]; o = ''
    parts = ''.join('<path d="%s" stroke="#000" stroke-width="2.6" stroke-linecap="square" stroke-linejoin="miter" fill="none"/>' % d for d, _ in g['parts'])
    if 'needle' in g: parts += '<path d="%s" stroke="#000" stroke-width="2.6" fill="#000"/>' % g['needle'][0]
    if 'knobs' in g: parts += ''.join('<circle cx="%s" cy="%s" r="2.2" fill="#000"/>' % (a, b) for a, b, _ in g['knobs'])
    png = cairosvg.svg2png(bytestring=('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48">%s</svg>' % parts).encode()); im = Image.open(io.BytesIO(png)).convert('RGBA').resize((16, 16), Image.BOX)
    a = np.asarray(im)[:, :, 3] > 90
    fillm = None
    if active and g.get('fill'):
        png = cairosvg.svg2png(bytestring=('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48"><path d="%s" fill="#000"/></svg>' % g['fill']).encode()); fillm = np.asarray(Image.open(io.BytesIO(png)).convert('RGBA').resize((16, 16), Image.BOX))[:, :, 3] > 90
    s = 1.5; rects = ''
    def mk(mask, col):
        out = ''
        for y in range(16):
            x = 0
            while x < 16:
                if mask[y, x]:
                    x2 = x
                    while x2 + 1 < 16 and mask[y, x2 + 1]: x2 += 1
                    out += 'M%s %sh%sv%sh-%sz' % (f(x * s), f(y * s), f((x2 - x + 1) * s + .02), f(s + .02), f((x2 - x + 1) * s + .02)); x = x2 + 1
                else: x += 1
        return '<path d="%s" fill="%s"/>' % (out, col)
    col = P['acc'] if active else P['ink2']
    o = ''
    if fillm is not None: o += mk(fillm & ~a, mixc(P['acc'], P['bg'], .55))
    sh = mk(np.roll(a, 1, 0) & ~a, '#0A0620') if active else ''
    body = sh + mk(a, col)
    if active: body = '<g>%s%s</g>' % (AT('translate', '0 0;0 -1.5;0 0;0 0', '1.6s', kt='0;.25;.5;1', mode='discrete'), body)
    return o + body
ICON_NAMES = list(G)
def icon(sk, name, active):
    inner = pixel_icon(sk, name, active) if sk.id == 'pixel' else glyph_svg(sk, name, active)
    return wrap(sk, 24, 24, inner)
if __name__ == '__main__':
    import os, sys
    from playwright.sync_api import sync_playwright
    os.makedirs('t/i', exist_ok=True); h = '<body style="margin:0;background:#888;font:10px sans-serif">'
    for sk in SKINS:
        h += '<div style="display:flex;gap:6px;padding:6px;background:%s;margin:2px;align-items:center"><b style="width:70px;color:#999">%s</b>' % (sk.P['bg'], sk.id)
        for n in ICON_NAMES:
            for ac in (False, True):
                p = 't/i/%s_%s_%s.svg' % (sk.id, n, ac); open(p, 'w').write(icon(sk, n, ac)); h += '<img src="i/%s_%s_%s.svg" width="48" height="48">' % (sk.id, n, ac)
        h += '</div>'
    open('t/i.html', 'w').write(h)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 700}); pg.goto('file:///home/claude/kit/t/i.html'); pg.wait_for_timeout(1200); pg.screenshot(path='t/i.png', full_page=True); b.close()
