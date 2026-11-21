from lay_gen import *
def lum(c): r, g, b = [int(c[i:i + 2], 16) for i in (1, 3, 5)]; return (.299 * r + .587 * g + .114 * b) / 255
def onc(c): return '#FFFFFF' if lum(c) < .62 else '#141414'
def ids(sk, s): return s + sk.id[:3]
def hero_art(sk):
    P = sk.P; i = sk.id; cx, cy = 195, 190; o = ''
    if i == 'coquette':
        o += '<g transform="translate(%s,%s)"><g>%s%s</g></g>' % (cx, cy, AT('rotate', '0;360', '80s', mode='linear'), ''.join('<g transform="rotate(%s) translate(0,-132)"><path d="M0 6C-12 -2-9 -10 -4.5 -10C-2 -10 0 -8 0 -6C0 -8 2 -10 4.5 -10C9 -10 12 -2 0 6Z" fill="#F28AAB" opacity=".85"/></g>' % (k * 20) for k in range(18)))
        o += '<circle cx="%s" cy="%s" r="108" fill="#FFE3EC"/><circle cx="%s" cy="%s" r="108" stroke="#F28AAB" stroke-dasharray="2 6" stroke-linecap="round" fill="none"/>' % (cx, cy, cx, cy)
        o += sk.bow(cx, cy - 10, 4.6, True, '#FFC4D6', '#E8789C') + particles(10, 390, 380, '#fff', 6, 1.5, 3, False, 4, 8, .9, '<path d="%s" fill="#fff"/>' % star4(0, 0, 5, .25))
    elif i == 'y2k':
        o += '<defs>%s</defs>' % lin('chr', [(0, '#FFFFFF'), (.35, '#BFD8FF'), (.55, '#FF7AC8'), (.8, '#7A5CFF'), (1, '#FFFFFF')])
        o += '<g transform="translate(%s,%s)"><g>%s<circle r="150" stroke="#38BDF8" stroke-dasharray="4 12" stroke-width="2" fill="none"/><circle r="124" stroke="#FF2EA6" stroke-opacity=".6" fill="none"/></g></g>' % (cx, cy, AT('rotate', '0;360', '40s', mode='linear'))
        o += '<g transform="translate(%s,%s)"><g>%s<path d="%s" fill="url(#chr)" stroke="#fff" stroke-width="2"/><path d="%s" fill="#fff" opacity=".5"/></g></g>' % (cx, cy, AT('rotate', '-6;6;-6', '6s', spl=S(2, EASE)), star4(0, 0, 118, .3), star4(-10, -14, 40, .3))
        for k, c in enumerate(('#FF2EA6', '#38BDF8', '#FFE27A')): o += '<g transform="translate(%s,%s)"><g>%s<circle cx="%s" r="9" fill="%s"/></g></g>' % (cx, cy, AT('rotate', '%s;%s' % (k * 120, k * 120 + 360), '%ss' % (9 + k * 2), mode='linear'), 150 - k * 12, c)
    elif i == 'streetwear':
        o += '<g transform="translate(%s,%s)"><g>%s%s</g></g>' % (cx, cy, AT('rotate', '0;360', '30s', mode='linear'), ''.join('<path d="M-16 -150L0 -122L16 -150Z" fill="#F97316" transform="rotate(%s)"/>' % (k * 20) for k in range(18)))
        o += '<circle cx="%s" cy="%s" r="112" fill="#F97316" stroke="#fff" stroke-width="4"/><circle cx="%s" cy="%s" r="96" fill="none" stroke="#111" stroke-width="3" stroke-dasharray="10 6"/>' % (cx, cy, cx, cy)
        o += '<g transform="translate(%s,%s)"><g>%s%s</g></g>' % (cx, cy + 36, AT('rotate', '-4;4;-4', '3s', mode='discrete', kt='0;.5;1'), T('27', 'anton', 150, 0, 0, '#111', 'm') + T('27', 'anton', 150, 5, 5, None, 'm', stroke='#fff', sw=2) .replace('<g', '<g', 1))
    elif i == 'k-fashion':
        for r_, d_ in ((150, 70), (108, 50), (66, 30)): o += '<g transform="translate(%s,%s)"><circle r="%s" stroke="#4F6D8A" stroke-width="1" fill="none"/><g>%s<circle r="%s" stroke="#4F6D8A" stroke-width="2" stroke-dasharray="%s 900" fill="none"/></g></g>' % (cx, cy, r_, AT('rotate', '0;360', '%ss' % d_, mode='linear'), r_, r_ * 1.1)
        o += '<path d="M%s %sH%s M%s %sV%s" stroke="#4F6D8A" stroke-width="1"/><circle cx="%s" cy="%s" r="6" fill="#4F6D8A">%s</circle>' % (cx - 170, cy, cx + 170, cx, cy - 170, cy + 170, cx, cy, A('r', '4;9;4', '2.4s', spl=S(2, EASE)))
        for (x, y, t) in ((46, 100, 'N 37.56°'), (292, 138, 'E 126.97°'), (62, 290, 'SS/27')): o += '<g><path d="M%s %sh44" stroke="#4F6D8A" stroke-width=".8"/>%s%s</g>' % (x, y, T(t, 'inter', 10, x, y - 5, '#4F6D8A'), A('opacity', '.4;1;.4', '3s'))
    elif i == 'quiet-luxury':
        o += '<circle cx="%s" cy="%s" r="116" fill="#fff" stroke="#B48811" stroke-width=".8"/><circle cx="%s" cy="%s" r="104" stroke="#B48811" stroke-width=".5" fill="none"/>' % (cx, cy, cx, cy)
        o += T('M', 'cormorant-garamond', 190, cx, cy + 62, '#1C1917', 'm') + '<clipPath id="mq"><circle cx="%s" cy="%s" r="116"/></clipPath><g clip-path="url(#mq)"><rect x="-80" y="0" width="40" height="400" fill="#F5DC8A" opacity=".5" transform="skewX(-18)">%s</rect></g>' % (cx, cy, A('x', '40;460', '5s', mode='linear'))
        o += '<g transform="translate(%s,%s)"><g>%s%s</g></g>' % (cx, cy, AT('rotate', '0;360', '60s', mode='linear'), ''.join('<path d="M0 -122L3 -128L0 -134L-3 -128Z" fill="#B48811" transform="rotate(%s)"/>' % (k * 30) for k in range(12)))
    elif i == 'minimal':
        o += '<circle cx="%s" cy="%s" r="96" fill="#09090B">%s</circle>' % (cx, cy, A('r', '90;100;90', '5s', spl=S(2, EASE)))
        o += '<g transform="translate(%s,%s)"><g>%s<circle cx="140" r="7" fill="#09090B"/></g></g><path d="M40 %sH350" stroke="#09090B" stroke-width="1" opacity=".5"/>' % (cx, cy, AT('rotate', '0;360', '12s', mode='linear'), cy)
    elif i == 'grunge':
        o += '<g transform="translate(%s,%s) rotate(-5)"><rect x="-125" y="-125" width="250" height="250" fill="#2A2420" stroke="#D6D3D1" stroke-width="2" stroke-dasharray="14 4 3 4"/><path d="M-125 -125L125 125M125 -125L-125 125" stroke="#D97706" stroke-width="10" opacity=".9"/><circle r="64" fill="#181512" stroke="#E8DFC8" stroke-width="3"/>%s<rect x="-60" y="-140" width="70" height="20" fill="#E8DFC8" opacity=".85" transform="rotate(-8)"/></g>' % (cx, cy, T('27', 'permanent-marker', 70, 0, 24, '#E8DFC8', 'm'))
    elif i == 'old-money':
        sh = 'M0 -92L74 -66V10C74 52 36 82 0 98C-36 82 -74 52 -74 10V-66Z'
        o += '<g transform="translate(%s,%s) scale(1.5)"><path d="%s" fill="#fff" stroke="#B08D3C" stroke-width="1.6"/><path d="M0 -92L0 98M-74 -20H74" stroke="#B08D3C" stroke-width=".8" opacity=".6"/><path d="M-60 -50H-14V-20H-60ZM14 -50H60V-20H14Z" fill="#14261C"/><path d="M-60 0H-14V40H-60Z" fill="#B08D3C" opacity=".35"/>%s</g>' % (cx, cy - 6, sh, '<g>%s<path d="M0 6L6 -2L0 -10L-6 -2Z" fill="#B08D3C"/></g>' % AT('scale', '1;1.25;1', '2.4s', spl=S(2, EASE)))
        for sx in (-1, 1): o += '<g transform="translate(%s,%s) scale(%s,1)">%s</g>' % (cx, cy, sx, ''.join('<g transform="rotate(%s) translate(0,-150)"><path d="M0 0C10 -8 14 -2 10 8C4 6 0 4 0 0Z" fill="#3F624D">%s</path></g>' % (20 + k * 16, A('opacity', '.5;1;.5', '3s', '%ss' % (k * .2))) for k in range(8)))
    elif i == 'casual':
        o += '<g transform="translate(%s,%s)"><g>%s%s</g><circle r="86" fill="#FDE68A" stroke="#fff" stroke-width="4"/><circle r="70" fill="#FCD34D"/></g>' % (cx, cy, AT('rotate', '0;360', '50s', mode='linear'), ''.join('<path d="M-9 -108L0 -142L9 -108Z" fill="#FDE68A" transform="rotate(%s)"/>' % (k * 24) for k in range(15)))
        for k, (x, y, r_) in enumerate(((-96, 60, -30), (100, 52, 24), (0, 108, 0))): o += '<g transform="translate(%s,%s)"><g transform="rotate(%s)"><g>%s<path d="M0 0C-26 -14 -22 -54 0 -66C22 -54 26 -14 0 0Z" fill="%s"/><path d="M0 0V-52" stroke="#047857" stroke-width="2"/></g></g></g>' % (cx + x, cy + y, r_, AT('rotate', '-6;6;-6', '%ss' % (3 + k * .6), spl=S(2, EASE)), ('#10B981', '#34D399', '#059669')[k])
    elif i == 'party-wear':
        o += '<path d="M%s 0V%s" stroke="#9A7413" stroke-width="2"/><g transform="translate(%s,%s)"><g>%s<circle r="100" fill="url(#bl)"/>%s<g clip-path="url(#blc)">%s</g></g></g>' % (cx, cy - 100, cx, cy, AT('rotate', '-5 0 -100;5 0 -100;-5 0 -100', '5s', spl=S(2, EASE)), '<defs><radialGradient id="bl" cx=".35" cy=".3"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".5" stop-color="#B9BCD0"/><stop offset="1" stop-color="#4B4E66"/></radialGradient><clipPath id="blc"><circle r="100"/></clipPath></defs>', ''.join('<path d="M-100 %sH100" stroke="#0D0A14" stroke-opacity=".55" stroke-width="1.4"/>' % (k * 20) for k in range(-4, 5)) + ''.join('<path d="M%s -100Q%s 0 %s 100" stroke="#0D0A14" stroke-opacity=".55" fill="none"/>' % (k * 20, k * 34, k * 20) for k in range(-4, 5)) + ''.join('<rect x="%s" y="%s" width="18" height="18" fill="#fff"><animate attributeName="opacity" values="0;.9;0" dur="%ss" begin="%ss" repeatCount="indefinite"/></rect>' % (-80 + (k * 37) % 150, -80 + (k * 53) % 150, 1.4 + (k % 4) * .3, k * .2) for k in range(14)))
        o += particles(18, 390, 380, '#FFE9A8', 14, .8, 2.4, False, 5, 10, 1, '<path d="%s" fill="#FFE9A8"/>' % star4(0, 0, 5, .25))
    return o
def title_block(sk, th):
    P = sk.P; ink = P['ink']; o = ''; y0 = 396
    o += T(th['kick'], th['body'], 13, 34, y0, ink, track=5) + '<path d="M%s %sH%s" stroke="%s" stroke-width="1"><animate attributeName="d" values="M%s %sH%s;M%s %sH%s;M%s %sH%s;M%s %sH%s" dur="%ss" keyTimes="0;.12;.93;1" repeatCount="indefinite"/></path>' % (0, 0, 0, ink, 220, y0 - 5, 220, 220, y0 - 5, 330, 220, y0 - 5, 330, 220, y0 - 5, 220, D) if False else T(th['kick'], th['body'], 13, 34, y0, ink, track=5)
    sz = 84 * min(1, 330 / txt(th['word'], th['disp'], 84, 0, 0)[1]); big = T(th['word'], th['disp'], sz, 28, y0 + 74, None, stroke=ink, sw=1.1, op=.3)
    o += '<g>%s%s</g>' % (AT('translate', '0 0;0 0;-3 1;3 -1;0 0;0 0', '6s', kt='0;.6;.62;.64;.66;1', mode='discrete'), big)
    o += T(th['word'], th['disp'], 22 * min(1, 250 / txt(th['word'], th['disp'], 22, 0, 0, track=12)[1]), 58, y0 + 52, P['acc'], track=12)
    o += '<defs>%s</defs>' % lin('sg' + sk.id[:3], [(0, ink), (1, P['acc2'])], 0, 0, 0, 1) + '<g>%s%s</g>' % (AT('translate', '0 0;4 0;0 0', '8s', spl=S(2, EASE)), T(th['scr'], th['script'], (100 if th['script'] in ('great-vibes', 'dancing-script') else 70) * min(1, 320 / txt(th['scr'], th['script'], 100 if th['script'] in ('great-vibes', 'dancing-script') else 70, 0, 0)[1]), 26, y0 + 128, 'url(#sg%s)' % sk.id[:3]))
    return o
def date_strip(sk, th):
    P = sk.P; xs = [88, 152, 218, 284, 350]; nums = ['02', '03', '04', '05', '06']; y = 562; kt = ';'.join(f(k / 6) for k in range(7)); seq = [1, 2, 3, 4, 3, 2, 1]
    o = ''.join(T(n, th['body'], 21, x, y + 7, P['ink2'], 'm', op=.7) for x, n in zip(xs, nums))
    d_, b = sk.body(54, 54, 'primary', 'ds'); a_ = sk.amb(54, 54, 'primary', 'ds')
    o += '<g transform="translate(%s,%s)"><g>%s<g transform="translate(-27,-27)">%s%s</g></g></g>' % (xs[1], y, AT('translate', ';'.join('%s 0' % f(xs[j] - xs[1]) for j in seq), '12s', kt=kt, spl=S(6, '.6 0 .2 1')), b, a_)
    for i, (x, n) in enumerate(zip(xs, nums)): o += '<g opacity="0">%s%s</g>' % (A('opacity', ';'.join('1' if j == i else '0' for j in seq), '12s', kt=kt, mode='discrete'), T(n, th['body'], 23, x, y + 8, onc(P['acc']), 'm'))
    return d_, o
def player(sk, th, y=592):
    P = sk.P; x, w, h = 20, 350, 80; d_, b = sk.body(w, h, 'primary', 'pl'); oc = onc(P['acc'])
    o = '<g transform="translate(%s,%s)">%s%s' % (x, y, b, sk.amb(w, h, 'primary', 'pl'))
    o += '<g transform="translate(40,40)"><circle r="30" fill="%s" opacity=".18"/><g>%s<path d="M-6 -11L12 0L-6 11Z" fill="%s"/></g></g>' % (oc, AT('scale', '1;1.1;1', '2.2s', spl=S(2, EASE)), oc)
    o += T('Give It To Me', th['body'], 16, 86, 34, oc) + T('Midnight Static', th['body'], 11, 86, 50, oc, op=.7)
    o += '<rect x="86" y="58" width="130" height="2" rx="1" fill="%s" opacity=".3"/><rect x="86" y="58" width="0" height="2" rx="1" fill="%s">%s</rect>' % (oc, oc, A('width', '0;130', '8s', mode='linear'))
    for k in range(5): o += '<rect x="%s" y="14" width="3" height="12" rx="1.5" fill="%s" opacity=".85" transform-origin="0 26"><animate attributeName="height" values="3;13;5;11;3" dur="%ss" begin="%ss" repeatCount="indefinite"/></rect>' % (232 + k * 6, oc, f(.9 + k * .13), f(k * .1)) if False else ''
    o += '<g transform="translate(%s,%s)"><g>%s<circle r="30" fill="#000" opacity=".25"/><circle r="22" stroke="%s" stroke-width="1" fill="none" opacity=".5"/><circle r="8" fill="%s" opacity=".9"/><path d="M-30 0A30 30 0 0 1 0 -30" stroke="%s" stroke-width="3" fill="none" opacity=".7"/></g></g>' % (w - 44, 40, AT('rotate', '0;360', '6s', mode='linear'), oc, oc, oc)
    return d_, o + '</g>'
def tiles(sk, th):
    P = sk.P; items = [('Bag', 'Your picks', 'bag'), ('Wishlist', 'Saved pieces', 'heart'), ('Discover', 'New drops', 'discover'), ('Alerts', 'Restocks', 'bell')]; out = []; defs = ''
    for k, (t, s_, ic) in enumerate(items):
        x = 20 + (k % 2) * 186; y = 688 + (k // 2) * 76; d_, b = sk.body(164, 64, 'card', 'tl%d' % k); defs += d_
        c = '<g transform="translate(%s,%s)">%s' % (x, y, b) + T(t, th['body'], 16, 16, 28, P['acc']) + T(s_, th['body'], 10.5, 16, 45, P['ink2']) + '<g transform="translate(130,32) scale(1.15) translate(-12,-12)">%s</g>' % glyph_svg(sk, ic, True) + '</g>'
        out.append(c)
    return defs, out
def home(sk):
    th = TH[sk.id]; P = sk.P; body = bg_for(sk) + enter(status(P['ink'], th['body'] if th['body'] in ('rajdhani', 'inter', 'poppins') else 'inter'), 0)
    body += '<g>%s</g>' % hero_art(sk) + enter(title_block(sk, th), 1, 'left')
    d1, ds = date_strip(sk, th); d2, pl = player(sk, th); d3, tl = tiles(sk, th)
    body += enter(ds, 2) + enter(pl, 3)
    for i, t in enumerate(tl): body += enter(t, 4 + i)
    body += '<rect x="145" y="834" width="100" height="4" rx="2" fill="%s" opacity=".4"/>' % P['ink']
    from comps import DEFS
    return svg(390, 844, body, DEFS + d1 + d2 + d3)
if __name__ == '__main__':
    import sys
    for sk in SKINS:
        if sk.id in ('goth', 'pixel'): continue
        if len(sys.argv) > 1 and sk.id not in sys.argv[1].split(','): continue
        open('t/h_%s.svg' % sk.id, 'w').write(home(sk))
