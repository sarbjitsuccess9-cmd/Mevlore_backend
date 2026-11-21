from lay_core import *
W, H = 390, 844
RED = '#E11D48'; RED2 = '#C41E3A'; DK = '#0A0709'
def status(col='#E7E5E4', font='rajdhani'):
    return T('9:41', font, 15, 22, 30, col) + '<g fill="%s"><rect x="318" y="21" width="3" height="5" rx="1"/><rect x="323" y="18" width="3" height="8" rx="1"/><rect x="328" y="15" width="3" height="11" rx="1"/><rect x="345" y="17" width="22" height="10" rx="3" fill="none" stroke="%s"/><rect x="347" y="19" width="13" height="6" rx="1.5"/></g>' % (col, col)
def goth_bg():
    o = '<defs>%s%s</defs>' % (lin('gbg', [(0, '#0C080A'), (1, '#050304')]), '<radialGradient id="gglow"><stop offset="0" stop-color="#E11D48" stop-opacity=".55"/><stop offset=".5" stop-color="#8A1030" stop-opacity=".2"/><stop offset="1" stop-color="#8A1030" stop-opacity="0"/></radialGradient>')
    o += '<rect width="390" height="844" fill="url(#gbg)"/>'
    o += '<ellipse cx="200" cy="200" rx="300" ry="260" fill="url(#gglow)">%s%s</ellipse>' % (pulse('rx', 280, 320, '6s'), pulse('opacity', .75, 1, '6s'))
    o += '<g opacity=".5"><ellipse cx="60" cy="700" rx="220" ry="40" fill="#E11D48" opacity=".08">%s</ellipse><ellipse cx="330" cy="520" rx="200" ry="34" fill="#E11D48" opacity=".06">%s</ellipse></g>' % (AT('translate', '-40 0;60 0;-40 0', '14s', spl=S(2, EASE)), AT('translate', '40 0;-60 0;40 0', '17s', spl=S(2, EASE)))
    o += particles(22, 390, 844, '#FF5C74', 4, .6, 1.8, True, 6, 13, .8)
    return o
def goth_hero():
    o = '<defs>%s%s</defs>' % ('<radialGradient id="moon" cx=".45" cy=".4"><stop offset="0" stop-color="#D42A48"/><stop offset=".6" stop-color="#A81830"/><stop offset="1" stop-color="#5A0C1A"/></radialGradient>', '<radialGradient id="halo"><stop offset="0" stop-color="#E11D48" stop-opacity=".6"/><stop offset="1" stop-color="#E11D48" stop-opacity="0"/></radialGradient>')
    cx, cy = 205, 195
    o += '<circle cx="%s" cy="%s" r="190" fill="url(#halo)">%s</circle>' % (cx, cy, pulse('r', 175, 200, '5s'))
    o += '<circle cx="%s" cy="%s" r="104" fill="url(#moon)"/>' % (cx, cy)
    # moon texture: grunge blotches
    o += '<clipPath id="mc"><circle cx="%s" cy="%s" r="104"/></clipPath><g clip-path="url(#mc)">%s<g opacity=".25">%s</g><g>%s<path d="M80 140L330 100L330 160L80 220Z" fill="#fff" opacity=".07"/></g></g>' % (cx, cy, noise(390, 400, '#4A0A18', 260, 9, .55, 2.2), ''.join('<path d="M%s %sl%s %sl%s %s" stroke="#fff" stroke-width="1"/>' % (150 + i * 9, 120 + (i * 37) % 60, 20, 8, -14, 22) for i in range(14)), AT('translate', '-120 0;160 0', '9s', mode='linear'))
    # rope rings
    o += '<g transform="translate(%s,%s)"><g>%s%s</g></g>' % (cx, cy, AT('rotate', '0;360', '70s', mode='linear'), rope_ring(0, 0, 128, 7, 14, '#7A2234', 5) + rope_ring(0, 0, 128, 7, 14, '#C23A52', 1.2, .6))
    o += '<g transform="translate(%s,%s)"><g>%s%s</g></g>' % (cx, cy, AT('rotate', '360;0', '90s', mode='linear'), rope_ring(0, 0, 150, 6, 20, '#4D1523', 4) + '<circle r="162" stroke="#6E1B2E" stroke-width="1.2" stroke-dasharray="3 9" fill="none"/>')
    o += '<circle cx="%s" cy="%s" r="112" stroke="#E11D48" stroke-opacity=".5" stroke-width="1.4" fill="none">%s</circle>' % (cx, cy, pulse('stroke-opacity', .25, .8, '3.4s'))
    o += '<g>%s%s</g>' % (AT('translate', '0 0;0 -3;0 0', '4.5s', spl=S(2, EASE)), raven(160, 110, .95))
    # flying drips / rune ticks
    for i in range(12):
        a = math.radians(i * 30 + 15); o += '<path d="M%s %sl%s %s" stroke="#E11D48" stroke-width="2" opacity=".7">%s</path>' % (f(cx + 172 * math.cos(a)), f(cy + 172 * math.sin(a)), f(7 * math.cos(a)), f(7 * math.sin(a)), A('opacity', '.1;.9;.1', '3s', '%ss' % f(i * .25)))
    return o
def goth_titles():
    o = ''
    o += '<g>%s%s</g>' % (T('FIVE ZERO', 'oswald', 14, 38, 392, '#F5F5F4', track=6), '<path d="M148 387H%s" stroke="#F5F5F4" stroke-width="1" stroke-opacity=".7"><animate attributeName="d" values="M148 387H148;M148 387H236;M148 387H236;M148 387H148" dur="%ss" keyTimes="0;.12;.93;1" repeatCount="indefinite"/></path>' % (236, D))
    ol = T('SUNDAY', 'bebas-neue', 104, 34, 466, None, stroke='#FFFFFF', sw=1.1, op=.38)
    o += '<g>%s%s%s</g>' % (ol, '<g transform="translate(2,0)" opacity="0">%s%s</g>' % (A('opacity', '0;0;.6;0;0', '5s', kt='0;.55;.57;.6;1', mode='linear'), T('SUNDAY', 'bebas-neue', 104, 34, 466, None, stroke='#E11D48', sw=1.4)), AT('translate', '0 0;0 0;-2 1;2 -1;0 0;0 0', '5s', kt='0;.54;.56;.58;.6;1', mode='discrete'))
    o += T('SUNDAY', 'oswald', 30, 62, 446, RED, track=15)
    sc = T('Jan', 'great-vibes', 138, 24, 514, 'url(#jan)') 
    o += '<defs>%s</defs>' % lin('jan', [(0, '#FFFFFF'), (1, '#6B6B6B')], 0, 0, 0, 1) + '<g>%s%s</g>' % (AT('translate', '0 0;3 0;0 0', '8s', spl=S(2, EASE)), sc)
    return o
def goth_dates():
    xs = [88, 152, 218, 284, 350]; nums = ['02', '03', '04', '05', '06']; y = 560
    o = ''
    for x, n in zip(xs, nums): o += T(n, 'rajdhani', 22, x, y + 7, '#6B6B6B', 'm')
    seq = [1, 2, 3, 2, 1]; vals = ';'.join('%s 0' % f(xs[i] - xs[1]) for i in [1, 2, 3, 4, 3, 2, 1]); kt = ';'.join(f(k / 6) for k in range(7))
    pill = '<g transform="translate(%s,%s)"><g>%s<circle r="42" fill="url(#halo)" opacity=".8"/><circle r="26" fill="%s"/><circle r="26" stroke="#FF6A82" stroke-width="1" opacity=".6"/></g></g>' % (xs[1], y, AT('translate', vals, '12s', kt=kt, spl=S(6, '.6 0 .2 1')), RED)
    o += pill
    o2 = ''
    for k, i in enumerate([1, 2, 3, 4, 3, 2, 1]): pass
    for i, (x, n) in enumerate(zip(xs, nums)):
        times = [k / 6 for k, j in enumerate([1, 2, 3, 4, 3, 2, 1]) if j == i]
        if not times: continue
        vals_o = ';'.join('1' if j == i else '0' for j in [1, 2, 3, 4, 3, 2, 1]); o += '<g opacity="0">%s%s</g>' % (A('opacity', vals_o, '12s', kt=kt, mode='discrete'), T(n, 'rajdhani', 24, x, y + 8, '#FFFFFF', 'm'))
    return o
def glow_card(x, y, w, h, r=16, col='#E11D48', sid='t'):
    d = rr(x, y, w, h, r)
    return '<path d="%s" fill="#0E090B"/>' % d + glow_stroke(rr(x - 1, y - 1, w + 2, h + 2, r), col, 12, .6, 5) + '<path d="%s" stroke="#E11D48" stroke-opacity=".5" stroke-width="1" fill="none"/>' % d + '<path d="%s" fill="url(#tg)" opacity=".5"/>' % d
def goth_player():
    x, y, w, h = 20, 590, 350, 80
    d = rr(x, y, w, h, 40); o = '<defs>%s%s</defs>' % (lin('pl', [(0, '#C41E3A'), (.7, '#E11D48'), (1, '#5E1022')], 0, 0, 1, 0), lin('pb', [(0, '#3A0A14'), (1, '#1A0509')]))
    o += glow_stroke(d, '#E11D48', 16, .5, 5) + '<path d="%s" fill="url(#pl)"/>' % d
    o += '<clipPath id="pc"><path d="%s"/></clipPath><g clip-path="url(#pc)"><g opacity=".25">%s</g><rect x="-60" y="%s" width="46" height="%s" fill="#fff" opacity=".18" transform="skewX(-20)">%s</rect></g>' % (d, ''.join('<path d="M%s %sH%s" stroke="#000" stroke-width="1"/>' % (x + 90, y + 10 + k * 6, x + 262) for k in range(12)), y, h, A('x', '-60;420', '5s', kt='0;1'))
    # play button
    o += '<circle cx="%s" cy="%s" r="34" fill="url(#pb)" stroke="#FF6A82" stroke-width="1.6"/><circle cx="%s" cy="%s" r="34" stroke="#FF6A82" stroke-width="1" opacity=".5" fill="none">%s%s</circle>' % (x + 40, y + 40, x + 40, y + 40, A('r', '34;44', '2.2s'), A('opacity', '.6;0', '2.2s'))
    o += '<g transform="translate(%s,%s)"><g>%s<path d="M-6 -12L14 0L-6 12Z" stroke="#FF8A9C" stroke-width="1.8" stroke-linejoin="round" fill="#FF8A9C" fill-opacity=".15"/></g></g>' % (x + 42, y + 40, AT('scale', '1;1.14;1', '2.2s', spl=S(2, EASE)))
    o += T('Give It To Me', 'rajdhani', 17, x + 92, y + 32, '#FFE4E8') + T('Midnight Static', 'rajdhani', 12, x + 92, y + 48, '#FFB4C0', op=.75)
    o += '<rect x="%s" y="%s" width="130" height="2" rx="1" fill="#000" opacity=".35"/><rect x="%s" y="%s" width="0" height="2" rx="1" fill="#fff">%s</rect><circle cy="%s" r="3" fill="#fff"><animate attributeName="cx" values="%s;%s" dur="8s" repeatCount="indefinite"/></circle>' % (x + 92, y + 58, x + 92, y + 58, A('width', '0;130', '8s'), y + 59, x + 92, x + 222)
    o += T('3:54', 'rajdhani', 10, x + 232, y + 66, '#FFD0D8')
    for i in range(5): o += '<rect x="%s" y="%s" width="3" height="14" rx="1.5" fill="#FFE4E8" opacity=".8" transform="translate(0,14)"><animate attributeName="height" values="4;14;6;12;4" dur="%ss" repeatCount="indefinite" begin="%ss"/><animate attributeName="y" values="-4;-14;-6;-12;-4" dur="%ss" repeatCount="indefinite" begin="%ss"/></rect>' % (x + 236 + i * 5, y + 20 + 8, 0.9 + i * .13, i * .1, 0.9 + i * .13, i * .1) if False else ''
    # album record
    cx, cy = x + w - 40, y + 40
    o += '<circle cx="%s" cy="%s" r="46" fill="#5E1022" opacity=".6"/><circle cx="%s" cy="%s" r="38" fill="#0B0608"/><g transform="translate(%s,%s)"><g>%s%s</g></g>' % (cx, cy, cx, cy, cx, cy, AT('rotate', '0;360', '6s', mode='linear'), '<circle r="34" fill="#150B0E" stroke="#2A1218"/>' + ''.join('<circle r="%s" stroke="#2E161C" stroke-width=".8" fill="none"/>' % r for r in (30, 26, 22, 18)) + '<path d="M-34 0A34 34 0 0 1 0 -34" stroke="#E11D48" stroke-width="2" fill="none" opacity=".7"/><circle r="10" fill="#E11D48"/><circle r="2.4" fill="#0B0608"/><path d="M-6 -22L6 -22" stroke="#fff" opacity=".18"/>')
    return o
def goth_tiles():
    items = [('Bag', 'Your picks, waiting.', 'bag', 20, 686), ('Wishlist', 'Pieces you can\'t quit.', 'heart', 206, 686), ('Discover', 'New drops, after dark.', 'discover', 20, 760), ('Alerts', 'Restocks & rituals.', 'bell', 206, 760)]
    o = '<defs>%s</defs>' % '<linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E11D48" stop-opacity=".25"/><stop offset=".5" stop-color="#E11D48" stop-opacity="0"/></linearGradient>'
    outs = []
    for k, (t, s_, ic, x, y) in enumerate(items):
        from icons import glyph_svg
        g = glyph_svg(sk_goth, ic, True)
        c = glow_card(x, y, 164, 64) + T(t, 'rajdhani', 17, x + 16, y + 27, RED) + T(s_, 'rajdhani', 11, x + 16, y + 44, '#B0334A') + '<g transform="translate(%s,%s) scale(1.1)">%s</g>' % (x + 128, y + 33, g.replace('stroke-width="1.5"', 'stroke-width="1.5"'))
        c += '<path d="%s" stroke="#fff" stroke-opacity=".5" stroke-width="1" fill="none"><animate attributeName="stroke-dasharray" values="0 800;60 800;0 800" dur="%ss" begin="%ss" repeatCount="indefinite"/></path>' % (rr(x, y, 164, 64, 16), 5 + k, k * .8)
        outs.append(c)
    return o, outs
from worlds import Goth
sk_goth = Goth()
def goth_home():
    body = goth_bg() + '<rect width="390" height="844" fill="none"/>'
    hero = goth_hero()
    body += hero + scan(390, 844, '#ffffff', .05, '4s', 4)
    body += enter(status(), 0, 'up')
    body += enter(goth_titles(), 1, 'left') + enter(goth_dates(), 2, 'up') + enter(goth_player(), 3, 'up')
    d, tiles = goth_tiles(); body = body.replace('</svg>', '') + '<defs>' + d[6:-7] + '</defs>' if False else body
    for i, t in enumerate(tiles): body += enter(t, 4 + i, 'up')
    body += '<rect x="145" y="832" width="100" height="4" rx="2" fill="#E7E5E4" opacity=".5"/>'
    defs = '<linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E11D48" stop-opacity=".25"/><stop offset=".5" stop-color="#E11D48" stop-opacity="0"/></linearGradient>'
    return svg(390, 844, body, defs)
if __name__ == '__main__':
    open('t/goth_home.svg', 'w').write(goth_home())
