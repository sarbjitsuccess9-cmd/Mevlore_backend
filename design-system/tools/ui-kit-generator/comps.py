from core import *
from worlds import *
DEFS = lin('orb', [(0, '#FFFFFF'), (.4, '#BFD8FF'), (1, '#FF2EA6')], .3, .2, .8, .9) + lin('gold', [(0, '#FFF1B0'), (.5, '#D4AF37'), (1, '#8A6A12')])
def wrap(sk, w, h, body, defs=''): return svg(w, h, body, DEFS + defs)
def pad(sk): return 40 if sk.id == 'goth' else 0
def button(sk, role='primary', w=320, h=60):
    px = pad(sk); iw = w - 2 * px; uid = role[:2]
    d, b = sk.body(iw, h, role, uid)
    a = sk.amb(iw, h, role, uid)
    pr = AT('scale', '1 1;1 1;.965 .965;1 1;1 1', '3.6s', kt='0;.55;.62;.72;1', spl='0 0 1 1;.3 0 .7 1;.2 .8 .2 1;0 0 1 1') if role == 'primary' else ''
    inner = '<g transform="translate(%s,0)">%s%s</g>' % (px, b, a)
    wings = (sk.wings_btn(w, h) if px else '')
    return wrap(sk, w, h, '<g transform="translate(%s,%s)"><g>%s<g transform="translate(%s,%s)">%s%s</g></g></g>' % (w / 2, h / 2, pr, -w / 2, -h / 2, wings, inner), d)
if __name__ == '__main__':
    import sys, os
    from playwright.sync_api import sync_playwright
    os.makedirs('t', exist_ok=True); h = '<body style="margin:0;background:#9aa;font:11px sans-serif">'
    for sk in SKINS:
        h += '<div style="display:flex;gap:8px;padding:6px;background:%s;margin:2px;align-items:center"><b style="width:80px;color:#888">%s</b>' % (sk.P['bg'], sk.id)
        for role in ('primary', 'ghost', 'tonal'): h += button(sk, role)
        h += '</div>'
    open('t/b.html', 'w').write(h)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1160, 'height': 900}); pg.goto('file:///home/claude/kit/t/b.html'); pg.wait_for_timeout(1500); pg.screenshot(path='t/b.png', full_page=True); b.close()
