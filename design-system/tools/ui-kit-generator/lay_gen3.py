from lay_gen2 import *
from comps import DEFS
def bgsoft(sk, op=.78):
    P = sk.P
    b = goth_bg() if sk.id == 'goth' else pixel_bg() if sk.id == 'pixel' else bg_for(sk)
    return b + '<rect width="390" height="844" fill="%s" opacity="%s"/>' % (P['bg'], op if sk.id not in ('pixel',) else .25)
def ph_img(sk, x, y, w, h, seed=0, motif=True):
    P = sk.P; r_ = min(sk.r if sk.id not in ('y2k', 'k-fashion', 'coquette', 'casual', 'party-wear') else 16, 18); u = 'ph%d%d' % (seed, int(x))
    c1 = mixc(P['acc'], P['bg'], .6 if not sk.dark else .55); c2 = mixc(P['acc2'], P['bg'], .5)
    o = '<defs>%s<clipPath id="%s"><rect x="%s" y="%s" width="%s" height="%s" rx="%s"/></clipPath></defs><g clip-path="url(#%s)">' % (lin('g' + u, [(0, c1), (1, c2)]), u, x, y, w, h, r_, u)
    o += '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#g%s)"/>' % (x, y, w, h, u)
    o += '<g opacity=".18" stroke="%s" stroke-width="1">%s</g>' % (P['ink'], ''.join('<path d="M%s %sl%s %s"/>' % (x - h + k * 14, y + h, h, -h) for k in range(int((w + h) / 14))))
    o += '<g transform="translate(%s,%s)"><g>%s%s</g></g>' % (x + w / 2, y + h / 2, AT('translate', '0 0;0 -6;0 0', '%ss' % (3.4 + seed * .4), spl=S(2, EASE)), sk.motif(0, 0, min(5.5, min(w, h) / 22), False) or '<circle r="%s" fill="%s" opacity=".5"/>' % (min(w, h) / 6, P['acc']))
    o += '<rect x="%s" y="%s" width="%s" height="%s" fill="#fff" opacity="%s" transform="skewX(-16)">%s</rect></g>' % (x - 60, y, 40, h, .35 if not sk.dark else .12, A('x', '%s;%s' % (x - 60, x + w + 140), '3.2s', '%ss' % (seed * .7), mode='linear'))
    return o
def nav_inner(sk, th, y=758):
    P = sk.P; w = 358; x = 16; d_, b = sk.body(w, 64, 'card', 'nv'); names = ['home', 'discover', 'videos', 'bag', 'profile']; slot = w / 5
    o = '<g transform="translate(%s,%s)">%s' % (x, y, b); cyc = 12; kt = ';'.join(f(k / 5) for k in range(6))
    for k, n in enumerate(names):
        cx = slot * (k + .5)
        o += '<g transform="translate(%s,16) scale(1.15)">%s</g>' % (f(cx - 14), glyph_svg(sk, n, False))
        o += '<g opacity="0" transform="translate(%s,16) scale(1.15)">%s%s</g>' % (f(cx - 14), A('opacity', ';'.join('1' if j == k else '0' for j in range(6)), '%ss' % cyc, kt=kt, mode='discrete'), glyph_svg(sk, n, True))
    o += '<g><animateTransform attributeName="transform" type="translate" values="%s" dur="%ss" keyTimes="%s" repeatCount="indefinite" calcMode="spline" keySplines="%s"/><circle cx="%s" cy="56" r="2.6" fill="%s"/></g>' % (';'.join('%s 0' % f(slot * (min(j, 4) + .5) - slot * .5) for j in range(6)), cyc, kt, S(5, '.5 0 .2 1'), f(slot * .5), P['acc'])
    return d_, o + '</g>'
def topbar(sk, th, title='Discover', y=48):
    P = sk.P; o = T(title, th['disp'], 28 if th['disp'] != 'orbitron' else 24, 24, y + 30, P['ink'], track=0)
    d_, b = sk.body(44, 44, 'card', 'tb'); o += '<g transform="translate(322,%s)">%s<g transform="translate(10,10)">%s</g></g>' % (y, b, glyph_svg(sk, 'bag', False))
    o += '<g transform="translate(360,%s)"><circle r="9" fill="%s">%s</circle>%s</g>' % (y + 4, P['acc'], pulse('r', 8, 10, '1.6s'), T('2', th['body'] if th['body'] != 'syncopate' else 'inter', 11, 0, 4, onc(P['acc']), 'm'))
    return d_, o
def section(sk, th, label, y):
    P = sk.P; return T(label, th['disp'], 17, 24, y, P['ink']) + '<path d="M%s %sH300" stroke="%s" stroke-opacity=".5"/>' % (24 + txt(label, th['disp'], 17, 0, 0)[1] + 12, y - 6, P['acc']) + T('See all', th['body'], 12, 366, y, P['acc'], 'r')
def chips_row(sk, th, y):
    P = sk.P; o = ''; d = ''; labels = ['All', 'Dresses', 'Tops', 'Denim', 'Shoes']; x = 20; kt = ';'.join(f(j / 5) for j in range(6))
    for k, l in enumerate(labels):
        wid = txt(l, th['body'], 13, 0, 0)[1] + 30; d1, b1 = sk.body(wid, 36, 'tonal', 'cr%d' % k); d2, b2 = sk.body(wid, 36, 'primary', 'cs%d' % k); d += d1 + d2
        o += '<g transform="translate(%s,%s)">%s%s<g opacity="0">%s%s%s</g></g>' % (f(x), y, b1, T(l, th['body'], 13, wid / 2, 23, P['ink'], 'm'), A('opacity', ';'.join('1' if j == k else '0' for j in range(6)), '10s', kt=kt, mode='discrete'), b2, T(l, th['body'], 13, wid / 2, 23, onc(P['acc']), 'm'))
        x += wid + 8
    return d, o
def prod_card(sk, th, x, y, k=0, name='Pleated Skirt', price='Rs. 2,490'):
    P = sk.P; w, h = 168, 214; d_, b = sk.body(w, h, 'card', 'pc%d' % k)
    o = '<g transform="translate(%s,%s)">%s' % (x, y, b) + ph_img(sk, 8, 8, w - 16, 134, k)
    hd, hb = sk.body(30, 30, 'card', 'hh%d' % k)
    o += '<g transform="translate(%s,16)">%s<g transform="translate(3,3) scale(1)">%s</g></g>' % (w - 46, hb, '<g>%s%s</g>' % (AT('scale', '1;1.18;1;1', '3s', '%ss' % (k * .6), kt='0;.1;.2;1', spl=S(3, EASE)), glyph_svg(sk, 'heart', k % 2 == 0).replace('<path', '<path transform="translate(0,0)"', 0)))
    o += T(name, th['body'], 14, 14, 166, P['ink']) + T(price, th['body'], 13, 14, 192, P['acc'])
    for j in range(5): o += '<path d="%s" fill="%s" opacity=".9"/>' % (star5(w - 70 + j * 11 + 4, 187, 4.6), P['acc'])
    return hd, o + '</g>'
def banner(sk, th, y=224):
    P = sk.P; w, h = 350, 118; d_, b = sk.body(w, h, 'primary', 'bn'); oc = onc(P['acc'])
    o = '<g transform="translate(20,%s)">%s%s' % (y, b, sk.amb(w, h, 'primary', 'bn'))
    o += T('NEW SEASON', th['body'], 11, 22, 32, oc, track=4, op=.8) + T('Up to 40% off', th['disp'], 27 * min(1, 200 / txt('Up to 40% off', th['disp'], 27, 0, 0)[1]), 22, 66, oc) + '<g transform="translate(24,84)">%s</g>' % ''.join(T('Shop now', th['body'], 12, 0, 12, oc) for _ in [0])
    o += '<g transform="translate(%s,%s)"><g>%s%s</g></g>' % (w - 66, h / 2, AT('rotate', '-8;8;-8', '4s', spl=S(2, EASE)), sk.motif(0, 0, 3.2, True))
    return d_, o + '</g>'
def stepper_steps(sk, th, y):
    P = sk.P; labs = ['Ordered', 'Packed', 'Shipped', 'Delivered']; o = ''
    for k in range(4):
        x = 52 + k * 95
        if k < 3: o += '<path d="M%s %sH%s" stroke="%s" stroke-width="3" stroke-opacity=".3" stroke-linecap="round"/><path d="M%s %sH%s" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-dasharray="0 100"><animate attributeName="stroke-dasharray" values="0 100;70 100;70 100;0 100" keyTimes="0;%s;.9;1" dur="8s" repeatCount="indefinite"/></path>' % (x + 12, y, x + 83, P['ink2'], x + 12, y, x + 83, P['acc'], f(.12 + k * .18))
        o += '<circle cx="%s" cy="%s" r="9" fill="%s" fill-opacity=".25" stroke="%s" stroke-width="1.5"/><circle cx="%s" cy="%s" r="9" fill="%s" opacity="0">%s</circle>' % (x, y, P['bg'], P['ink2'], x, y, P['acc'], A('opacity', '0;0;1;1;0', '8s', kt='0;%s;%s;.9;1' % (f(.1 + k * .18), f(.16 + k * .18))))
        o += T(labs[k], th['body'], 10.5, x, y + 26, P['ink2'], 'm')
    return o
def coupon(sk, th, y):
    P = sk.P; w = 350; d_, b = sk.body(w, 62, 'tonal', 'cp'); o = '<g transform="translate(20,%s)">%s' % (y, b) + '<path d="M236 8V54" stroke="%s" stroke-width="1.5" stroke-dasharray="3 4"/>' % P['acc'] + T('MELVORE27', th['disp'], 20, 22, 30, P['ink'], track=2) + T('Extra 10% off today', th['body'], 11, 22, 48, P['ink2'])
    o += '<g transform="translate(236,31)"><g>%s<path d="M-5 -8L5 8M5 -8L-5 8" stroke="%s" stroke-width="1.6" stroke-linecap="round"/></g></g>' % (AT('scale', '1;1;.7;1', '2.4s', kt='0;.6;.7;1'), P['acc'])
    o += T('Apply', th['disp'], 14, 292, 36, P['acc'], 'm')
    return d_, o + '</g>'
def cta(sk, th, y, label='Add to bag'):
    P = sk.P; d_, b = sk.body(350, 58, 'primary', 'ct'); oc = onc(P['acc'])
    o = '<g transform="translate(20,%s)">%s%s' % (y, b, sk.amb(350, 58, 'primary', 'ct'))
    o += '<g>%s%s</g>' % (A('opacity', '1;1;0;0;1', '6s', kt='0;.3;.34;.9;1', mode='discrete'), T(label, th['disp'], 18 * min(1, 200 / txt(label, th['disp'], 18, 0, 0)[1]), 175, 36, oc, 'm', track=1))
    o += '<g opacity="0">%s%s<path d="M-14 0l8 8l18 -18" stroke="%s" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="44" stroke-dashoffset="44" transform="translate(175,29)">%s</path></g>' % (A('opacity', '0;0;1;1;0', '6s', kt='0;.36;.4;.9;1', mode='discrete'), '', oc, A('stroke-dashoffset', '44;44;0;0;44', '6s', kt='0;.4;.5;.9;1'))
    o += '<g opacity="0"><rect x="12" y="46" width="0" height="3" rx="1.5" fill="%s" opacity=".8">%s</rect>%s</g>' % (oc, A('width', '0;0;326;326;0', '6s', kt='0;.1;.3;.31;1', mode='linear'), A('opacity', '0;1;1;0;0', '6s', kt='0;.1;.3;.31;1', mode='discrete'))
    return d_, o + '</g>'
def shop_screen(sk):
    th = TH[sk.id]; P = sk.P; body = bgsoft(sk) + enter(status(P['ink'], 'inter'), 0)
    dt, tb = topbar(sk, th); body += enter(tb, 1)
    sd, sb = sk.body(350, 48, 'ghost', 'sb'); sbar = '<g transform="translate(20,106)">%s<g transform="translate(24,24)"><circle cx="-1" cy="-1" r="6" stroke="%s" stroke-width="2"/><path d="M3.5 3.5L8 8" stroke="%s" stroke-width="2" stroke-linecap="round"/></g><rect x="52" y="20" width="0" height="8" rx="4" fill="%s" opacity=".5">%s</rect><rect x="52" y="17" width="2" height="14" fill="%s">%s</rect></g>' % (sb, P['acc'], P['acc'], P['ink2'], A('width', '0;0;150;150;0', '6s', kt='0;.1;.6;.9;1'), P['acc'], A('opacity', '1;0;1', '.9s'))
    body += enter(sbar, 2)
    cd, cr = chips_row(sk, th, 170); body += enter(cr, 3)
    bd_, bn = banner(sk, th, 222); body += enter(bn, 4, 'zoom') + enter(section(sk, th, 'New in', 372), 5)
    pc = [prod_card(sk, th, 20, 388, 0), prod_card(sk, th, 202, 388, 1, 'Wide Denim', 'Rs. 3,190')]
    for i, (hd, c) in enumerate(pc): body += enter(c, 6 + i, 'up')
    nd, nv = nav_inner(sk, th); body += enter(nv, 9, 'up')
    return svg(390, 844, body, DEFS + dt + sd + cd + bd_ + ''.join(h for h, _ in pc) + nd)
def product_screen(sk):
    th = TH[sk.id]; P = sk.P; body = bgsoft(sk, .86)
    img = ph_img(sk, 0, 0, 390, 430, 2) 
    body += enter(img, 0, 'zoom') + enter(status(P['ink'], 'inter'), 1)
    hb = ''
    for k, x in enumerate((20, 326)):
        d_, b = sk.body(44, 44, 'card', 'pb%d' % k); hb += '<g transform="translate(%s,52)">%s<g transform="translate(10,10)">%s</g></g>' % (x, b, glyph_svg(sk, 'search' if k == 0 else 'heart', k == 1))
    body += enter(hb, 2)
    dots = ''.join(pip(sk, 175 + k * 20, 410, 4, k == 0) for k in range(4)) + '<g><animateTransform attributeName="transform" type="translate" values="0 0;20 0;40 0;60 0;0 0" dur="6s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;.25;.5;.75;1"/>%s</g>' % pip(sk, 175, 410, 5.2, True)
    body += enter(dots, 3)
    body += enter(T('Pleated Skirt', th['disp'], 28 * min(1, 200 / txt('Pleated Skirt', th['disp'], 28, 0, 0)[1]), 24, 478, P['ink']) + T('Rs. 2,490', th['disp'], 22 * min(1, 105 / txt('Rs. 2,490', th['disp'], 22, 0, 0)[1]), 366, 476, P['acc'], 'r') + ''.join('<path d="%s" fill="%s"/>' % (star5(32 + j * 20, 500, 7.5), P['acc']) for j in range(5)) + T('4.8  (212)', th['body'], 12, 140, 505, P['ink2']), 4)
    sz = ''; defs = ''; xs = 20
    for k, l in enumerate(('S', 'M', 'L', 'XL')):
        d1, b1 = sk.body(70, 44, 'ghost', 'z%d' % k); d2, b2 = sk.body(70, 44, 'primary', 'zp%d' % k); defs += d1 + d2; t0 = k / 4
        sz += '<g transform="translate(%s,526)">%s<g opacity="0">%s%s</g>%s</g>' % (20 + k * 80, b1, A('opacity', ';'.join('1' if j == k else '0' for j in range(5)), '8s', kt=';'.join(f(j / 4) for j in range(5)), mode='discrete'), b2, T(l, th['disp'], 15, 35, 28, P['ink'], 'm'))
    body += enter(sz, 5)
    sw = ''
    for k, c in enumerate((P['acc'], P['acc2'], P['ink'])): sw += '<g transform="translate(%s,608)"><circle r="14" fill="%s"/><circle r="14" stroke="%s" stroke-width="1" fill="none" opacity=".4"/></g>' % (34 + k * 40, c, P['ink'])
    sw += '<g transform="translate(34,608)"><g>%s<circle r="19" stroke="%s" stroke-width="2" fill="none"/></g></g>' % (AT('translate', '0 0;40 0;80 0;40 0;0 0', '9s', kt='0;.25;.5;.75;1', spl=S(4, '.5 0 .2 1')), P['acc'])
    body += enter(sw + T('Colour', th['body'], 12, 366, 612, P['ink2'], 'r'), 6)
    st = ''
    sd, sb = sk.body(132, 44, 'ghost', 'st'); st = '<g transform="translate(20,650)">%s<path d="M18 22H34M98 22H114M106 14V30" stroke="%s" stroke-width="2.2" stroke-linecap="round"/><g transform="translate(66,22)"><g>%s<rect x="-4" y="-9" width="8" height="18" rx="2" fill="%s"/></g></g></g>' % (sb, P['acc'], AT('translate', '0 14;0 0;0 0;0 -14', '3s', kt='0;.15;.85;1', spl='.2 1 .4 1;0 0 1 1;.6 0 1 1'), P['ink'])
    st += T('Free delivery - 3 days', th['body'], 12, 366, 678, P['ink2'], 'r')
    body += enter(st, 7)
    cd_, cb = cta(sk, th, 726); body += enter(cb, 8, 'up')
    return svg(390, 844, body, DEFS + defs + sd + cd_ + ''.join(sk.body(44, 44, 'card', 'pb%d' % k)[0] for k in range(2)))
def bag_screen(sk):
    th = TH[sk.id]; P = sk.P; body = bgsoft(sk) + enter(status(P['ink'], 'inter'), 0); dt, tb = topbar(sk, th, 'My bag'); body += enter(tb, 1); defs = dt
    for k in range(2):
        d_, b = sk.body(350, 118, 'card', 'bi%d' % k); defs += d_; y = 112 + k * 132
        c = '<g transform="translate(20,%s)">%s' % (y, b) + ph_img(sk, 10, 10, 82, 98, k + 3) + T(['Pleated Skirt', 'Wide Denim'][k], th['body'], 15, 108, 34, P['ink']) + T('Size M - Rose', th['body'], 11, 108, 52, P['ink2']) + T(['Rs. 2,490', 'Rs. 3,190'][k], th['body'], 15, 108, 100, P['acc'])
        sd, sb = sk.body(92, 34, 'ghost', 'bs%d' % k); defs += sd
        c += '<g transform="translate(240,66)">%s<path d="M14 17H26M66 17H78M72 11V23" stroke="%s" stroke-width="2" stroke-linecap="round"/><g transform="translate(46,17)"><g>%s<rect x="-3.5" y="-7" width="7" height="14" rx="2" fill="%s"/></g></g></g>' % (sb, P['acc'], AT('translate', '0 10;0 0;0 0;0 -10', '3.4s', '%ss' % (k * .8), kt='0;.15;.85;1', spl='.2 1 .4 1;0 0 1 1;.6 0 1 1'), P['ink']) + '</g>'
        body += enter(c, 2 + k, 'right')
    cd_, cp = coupon(sk, th, 380); defs += cd_; body += enter(cp, 4)
    sm = T('Subtotal', th['body'], 13, 24, 486, P['ink2']) + T('Rs. 5,680', th['body'], 13, 366, 486, P['ink'], 'r') + T('Delivery', th['body'], 13, 24, 512, P['ink2']) + T('Free', th['body'], 13, 366, 512, P['acc'], 'r') + '<path d="M24 526H366" stroke="%s" stroke-opacity=".5" stroke-dasharray="3 4"/>' % P['ink2'] + T('Total', th['disp'], 20, 24, 556, P['ink']) + T('Rs. 5,112', th['disp'], 24, 366, 556, P['acc'], 'r')
    body += enter(sm, 5) + enter(stepper_steps(sk, th, 616) + T('Order progress', th['body'], 12, 24, 586, P['ink2']), 6)
    cd2, cb = cta(sk, th, 678, 'Checkout'); defs += cd2; body += enter(cb, 7)
    nd, nv = nav_inner(sk, th, 760); body += enter(nv, 8) ; defs += nd
    return svg(390, 844, body, DEFS + defs)
SCREENS = {'shop': shop_screen, 'product': product_screen, 'bag': bag_screen}
if __name__ == '__main__':
    import sys
    only = sys.argv[1].split(',') if len(sys.argv) > 1 else [s.id for s in SKINS]
    for sk in SKINS:
        if sk.id not in only: continue
        for n, fn in SCREENS.items(): open('t/%s_%s.svg' % (n, sk.id), 'w').write(fn(sk))
