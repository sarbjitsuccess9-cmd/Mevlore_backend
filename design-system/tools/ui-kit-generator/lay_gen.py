from lay_goth import *
from lay_pixel import *
TH = {
 'pixel': dict(disp='silkscreen-bold', script='vt323', body='vt323', kick='LEVEL 27', word='SUNDAY', scr='start'),
 'goth': dict(disp='oswald', script='great-vibes', body='rajdhani', kick='FIVE ZERO', word='SUNDAY', scr='Jan'),
 'coquette': dict(disp='playfair-display', script='dancing-script', body='playfair-display', kick='LITTLE LETTERS', word='SUNDAY', scr='Darling'),
 'y2k': dict(disp='orbitron', script='dancing-script', body='orbitron', kick='SYSTEM ONLINE', word='SUNDAY', scr='Baby'),
 'streetwear': dict(disp='anton', script='permanent-marker', body='oswald', kick='DROP 027', word='SUNDAY', scr='Run it'),
 'k-fashion': dict(disp='space-grotesk', script='inter', body='inter', kick='SEOUL / SS27', word='SUNDAY', scr='edit'),
 'quiet-luxury': dict(disp='cormorant-garamond', script='playfair-display', body='cormorant-garamond', kick='THE QUIET HOUR', word='SUNDAY', scr='Maison'),
 'minimal': dict(disp='inter', script='space-grotesk', body='inter', kick='ISSUE 27', word='SUNDAY', scr='plain'),
 'grunge': dict(disp='special-elite', script='permanent-marker', body='special-elite', kick='LOUD & LOST', word='SUNDAY', scr='Noise'),
 'old-money': dict(disp='playfair-display', script='great-vibes', body='cormorant-garamond', kick='EST. 1927', word='SUNDAY', scr='Heritage'),
 'casual': dict(disp='poppins', script='dancing-script', body='poppins', kick='EASY WEEKEND', word='SUNDAY', scr='Fresh'),
 'party-wear': dict(disp='syncopate', script='great-vibes', body='syncopate', kick='AFTER DARK', word='SUNDAY', scr='Gala'),
}
# ---------------- world backgrounds ----------------
def bg_for(sk):
    P = sk.P; i = sk.id; o = ''; B = P['bg']
    o += '<rect width="390" height="844" fill="%s"/>' % B
    if i == 'coquette':
        o = '<defs>%s</defs><rect width="390" height="844" fill="url(#cb)"/>' % lin('cb', [(0, '#FFEEF4'), (1, '#FFD6E4')])
        o += ''.join('<g transform="translate(%s,%s)" opacity=".5">%s</g>' % (x, y, sk.bow(0, 0, .5, True)) for x, y in ((40, 120), (350, 380), (60, 640), (330, 760)))
        o += particles(14, 390, 844, '#F28AAB', 21, 3, 6, True, 8, 15, .5, '<path d="M0 6C-12 -2-9 -10 -4.5 -10C-2 -10 0 -8 0 -6C0 -8 2 -10 4.5 -10C9 -10 12 -2 0 6Z" fill="#F28AAB" transform="scale(.5)"/>')
        o += '<path d="%s" fill="#fff" opacity=".7"/>' % edge(sk, 'scallop', 390, 8).replace('M0', 'M0').replace('Z', '') + ''
        o += '<path d="M0 0H390V16" fill="#fff"/>' 
    elif i == 'y2k':
        o += '<defs>%s</defs><rect width="390" height="500" fill="url(#yg)"/>' % lin('yg', [(0, '#1B1346'), (1, '#0E0D1B')])
        o += '<g transform="translate(195,560)"><circle r="150" fill="url(#orb2)" opacity=".5"/></g><defs><radialGradient id="orb2"><stop offset="0" stop-color="#FF2EA6" stop-opacity=".7"/><stop offset="1" stop-color="#FF2EA6" stop-opacity="0"/></radialGradient></defs>'
        o += '<g stroke="#38BDF8" stroke-opacity=".5" stroke-width="1">' + ''.join('<path d="M195 560L%s 844"/>' % f(195 + k * 90) for k in range(-8, 9)) + '</g><g stroke="#38BDF8" stroke-opacity=".5">%s</g>' % ''.join('<path d="M0 %sH390">%s</path>' % (f(560 + 284 * (k / 6.0) ** 2), A('d', 'M0 %s H390;M0 %s H390' % (f(560 + 284 * (k / 6.0) ** 2), f(560 + 284 * ((k + 1) / 6.0) ** 2)), '2s', mode='linear')) for k in range(6))
        o += particles(18, 390, 560, '#fff', 5, .8, 2, False, 6, 12, .9)
    elif i == 'streetwear':
        o += '<pattern id="hd" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#fff" opacity=".07"/></pattern><rect width="390" height="844" fill="url(#hd)"/>'
        for k in range(5): o += '<g opacity=".1">%s</g>' % '<g><animateTransform attributeName="transform" type="translate" values="%s 0;%s 0" dur="%ss" repeatCount="indefinite" calcMode="linear"/>%s</g>' % (0 if k % 2 == 0 else -600, -600 if k % 2 == 0 else 0, 24 + k * 3, T('DROP DROP DROP DROP DROP DROP', 'anton', 70, 0, 100 + k * 150, None, stroke='#fff', sw=1)) 
        o += '<g transform="translate(300,620) rotate(-12)"><rect x="-120" width="240" height="22" fill="#F97316"/>%s</g>' % ('<g>%s%s</g>' % (AT('translate', '0 0;-40 0', '1.4s', mode='linear'), ''.join('<path d="M%s 0l12 0l-12 22l-12 0z" fill="#111" transform="translate(%s,0)"/>' % (0, k * 24 - 120) for k in range(14))))
    elif i == 'k-fashion':
        o += '<g stroke="#4F6D8A" stroke-opacity=".12">' + ''.join('<path d="M%s 0V844"/>' % (k * 39) for k in range(11)) + ''.join('<path d="M0 %sH390"/>' % (k * 39) for k in range(22)) + '</g>'
        o += '<g stroke="#4F6D8A" stroke-width="1.2" opacity=".5">%s</g>' % ''.join('<path d="M%s %sh10M%s %sv10" />' % (x - 5, y, x, y - 5) for x in (39, 195, 351) for y in (117, 351, 585))
        o += '<path d="M0 0H390" stroke="#4F6D8A" stroke-width="1.4" opacity=".7">%s</path>' % A('d', 'M0 0H390;M0 844H390', '7s', mode='linear')
        o += '<circle cx="195" cy="200" r="150" stroke="#4F6D8A" stroke-opacity=".2" fill="none"/>'
    elif i == 'quiet-luxury':
        o += '<rect x="14" y="14" width="362" height="816" stroke="#B48811" stroke-opacity=".5" stroke-width=".8" fill="none"/><rect x="20" y="20" width="350" height="804" stroke="#1C1917" stroke-opacity=".2" stroke-width=".6" fill="none"/>'
        o += '<path d="M14 14H376V830H14Z" stroke="#E7C65A" stroke-width="2" stroke-linecap="round" stroke-dasharray="40 3000" fill="none">%s</path>' % A('stroke-dashoffset', '0;-3300', '12s', mode='linear')
        o += particles(30, 390, 844, '#C9A24A', 9, .5, 1.6, False, 9, 18, .6)
        o += '<circle cx="195" cy="210" r="130" stroke="#B48811" stroke-opacity=".3" fill="none"/><circle cx="195" cy="210" r="168" stroke="#B48811" stroke-opacity=".15" fill="none"/>'
    elif i == 'minimal':
        o += '<pattern id="dg" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#09090B" opacity=".18"/></pattern><rect width="390" height="844" fill="url(#dg)"/>'
        for k in range(3): o += '<circle cx="195" cy="210" r="40" stroke="#09090B" stroke-opacity=".5" fill="none">%s%s</circle>' % (A('r', '40;190', '7s', '%ss' % (k * 2.33), mode='linear'), A('stroke-opacity', '.5;0', '7s', '%ss' % (k * 2.33), mode='linear'))
    elif i == 'grunge':
        o += noise(390, 844, '#E7E0D2', 700, 4, .12, 1.4) + '<g stroke="#D6D3D1" stroke-opacity=".08">%s</g>' % ''.join('<path d="M%s %sl%s %s"/>' % (k * 41 % 390, k * 97 % 844, 90, 14) for k in range(26))
        o += '<g>%s%s%s</g>' % (A('opacity', '1;1;.2;1;1;.4;1', '6s', mode='discrete', kt='0;.4;.42;.44;.8;.82;1'), '<rect x="0" y="300" width="390" height="10" fill="#D97706" opacity=".25"/><rect x="0" y="520" width="390" height="5" fill="#fff" opacity=".1"/>', '<g transform="translate(0,0)">%s</g>' % AT('translate', '0 0;6 0;-4 0;0 0', '6s', mode='discrete', kt='0;.4;.5;1'))
        o += '<circle cx="195" cy="200" r="120" stroke="#D97706" stroke-width="3" fill="none" stroke-dasharray="760" stroke-dashoffset="760" stroke-linecap="round">%s</circle>' % A('stroke-dashoffset', '760;0;0;760', '8s', kt='0;.4;.9;1')
    elif i == 'old-money':
        o += '<pattern id="lt" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0H40M0 0V40" stroke="#14261C" stroke-opacity=".07" stroke-width="1"/><circle cx="20" cy="20" r="2" fill="#B08D3C" opacity=".25"/></pattern><rect width="390" height="844" fill="url(#lt)"/>'
        o += '<rect width="390" height="844" fill="url(#sh)"/><defs><linearGradient id="sh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#F2D88A" stop-opacity=".25"><animate attributeName="offset" values=".1;.9;.1" dur="9s" repeatCount="indefinite"/></stop><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
    elif i == 'casual':
        o = '<defs>%s%s%s</defs><rect width="390" height="844" fill="#F8FAFC"/>' % ('<radialGradient id="b1"><stop offset="0" stop-color="#6EE7B7" stop-opacity=".7"/><stop offset="1" stop-color="#6EE7B7" stop-opacity="0"/></radialGradient>', '<radialGradient id="b2"><stop offset="0" stop-color="#7DD3FC" stop-opacity=".6"/><stop offset="1" stop-color="#7DD3FC" stop-opacity="0"/></radialGradient>', '<radialGradient id="b3"><stop offset="0" stop-color="#FDE68A" stop-opacity=".6"/><stop offset="1" stop-color="#FDE68A" stop-opacity="0"/></radialGradient>')
        o += '<circle cx="80" cy="140" r="170" fill="url(#b1)">%s%s</circle><circle cx="330" cy="300" r="160" fill="url(#b2)">%s</circle><circle cx="120" cy="640" r="190" fill="url(#b3)">%s</circle>' % (A('cx', '80;150;80', '12s', spl=S(2, EASE)), A('cy', '140;200;140', '9s', spl=S(2, EASE)), A('cx', '330;260;330', '10s', spl=S(2, EASE)), A('cy', '640;560;640', '11s', spl=S(2, EASE)))
        o += particles(10, 390, 844, '#10B981', 3, 4, 7, False, 10, 18, .35, '<path d="M0 8C-10 4-10 -6 0 -9C10 -6 10 4 0 8Z" fill="#10B981" transform="scale(.8)"/>')
    elif i == 'party-wear':
        o += '<defs><radialGradient id="pg"><stop offset="0" stop-color="#3A1B66" stop-opacity=".9"/><stop offset="1" stop-color="#0D0A14" stop-opacity="0"/></radialGradient></defs><ellipse cx="195" cy="120" rx="320" ry="320" fill="url(#pg)"/>'
        for k, c in enumerate(('#D4AF37', '#E879F9', '#38BDF8', '#D4AF37')): o += '<g transform="translate(195,0)"><g>%s<path d="M0 0L-36 560L36 560Z" fill="%s" opacity=".1"/></g></g>' % (AT('rotate', '%s;%s;%s' % (-32 + k * 4, 32 - k * 4, -32 + k * 4), '%ss' % (7 + k * 1.5), spl=S(2, EASE)), c)
        o += particles(26, 390, 844, '#FFE9A8', 12, .8, 2.2, False, 7, 14, .9, '<path d="%s" fill="#FFE9A8"/>' % star4(0, 0, 4, .25))
    return o
