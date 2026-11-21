from core import *
random.seed(7)
class Skin:
    id = ''; P = {}; sw = 1.6; r = 12; dark = False
    def path(self, w, h, i=0): return rr(i, i, w - 2 * i, h - 2 * i, self.r - i if self.r > i else 0)
    def fills(self, role, uid):
        """-> (defs, fill, stroke, stroke-width)"""
        P = self.P
        if role == 'primary': return '', P['acc'], mixc(P['acc'], '#000000', .25), self.sw
        if role == 'ghost': return '', 'none', P['acc'], self.sw
        if role == 'tonal': return '', mixc(P['acc'], P['bg'], .84), mixc(P['acc'], P['bg'], .5), 1
        return '', P['surf'], P['bd'], 1.2
    def deco(self, w, h, role, uid): return ''
    def amb(self, w, h, role, uid): return sweep(w, h, self.path(w, h, 1), '3.6s', '#FFFFFF', .35, 26, id_='cp' + uid) if role == 'primary' else ''
    def motif(self, cx, cy, s, anim=True): return ''
    def thumb(self, cx, cy, r, anim=True): return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), self.P['acc'])
    def ink(self, role): return self.P['bg'] if role == 'primary' and not self.dark else (self.P['ink'] if self.dark or role != 'primary' else self.P['bg'])
    def body(self, w, h, role, uid):
        d_, fl, st, sw = self.fills(role, uid); d = self.path(w, h, 1)
        return d_, '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (d, fl, st, sw) + self.deco(w, h, role, uid)

# ---------------- GOTH ----------------
class Goth(Skin):
    id = 'goth'; dark = True; r = 3; sw = 1.5
    P = dict(bg='#08070B', surf='#121018', ink='#F4F4F5', ink2='#C4C2CF', acc='#C02638', acc2='#A1A1AA', bd='#342E42')
    def path(self, w, h, i=0):
        c = 10 - i * .4; m = w / 2; n = 5
        return poly([(i + c, i), (m - 16, i), (m, i - 4 + 2 * i), (m + 16, i), (w - i - c, i), (w - i, i + c), (w - i, h - i - c), (w - i - c, h - i), (m + 16, h - i), (m, h - i + 4 - 2 * i), (m - 16, h - i), (i + c, h - i), (i, h - i - c), (i, i + c)])
    def fills(self, role, uid):
        P = self.P
        if role == 'primary': return lin('g' + uid, [(0, '#1B1620'), (1, '#0C0A10')]), 'url(#g%s)' % uid, P['acc'], 1.6
        if role == 'ghost': return '', 'none', P['acc2'], 1.2
        if role == 'tonal': return '', '#1A1118', mixc(P['acc'], '#000000', .5), 1.2
        return '', P['surf'], P['bd'], 1.2
    def wing(self, side, h, s=1, anim=True):
        sx = -1 if side == 'L' else 1
        wing = 'M0 0 L2.5 -6 L5 1 C11 -2 20 -5 33 -7 C30 -2 30 3 28 7 C25 3 21 4 19 9 C16 5 12 7 10 13 C8 17 4 19 0 21Z'
        a = AT('scale', '1 1;1 .78;1 1', '1.3s', spl=S(2, EASE)) if anim else ''
        return '<g transform="translate(%s,%s) scale(%s,%s)"><g transform="translate(0,%s)"><g>%s<g transform="translate(0,%s)"><path d="%s" fill="#7D7A89"/><path d="M5 1C12 -1 20 -3 31 -6" stroke="#D4D2DE" stroke-width=".7" opacity=".5"/></g></g></g></g>' % (0, 0, sx * s, s, h / 2 - 5, a, -h / 2 + 5, wing)
    def deco(self, w, h, role, uid):
        P = self.P; m = w / 2
        o = '<path d="%s" stroke="%s" stroke-opacity=".3" stroke-width=".8"/>' % (self.path(w, h, 5), P['acc2'])
        o += '<path d="M%s %sH%s M%s %sH%s" stroke="%s" stroke-width="1"/>' % (14, h / 2, 30, w - 30, h / 2, w - 14, P['acc'])
        o += '<path d="M%s %sL%s %sL%s %sL%s %sZ" fill="%s"/>' % (m, 4.5, m + 3, 7.5, m, 10.5, m - 3, 7.5, P['acc'])
        o += '<path d="M%s %sL%s %sL%s %sL%s %sZ" fill="%s"/>' % (m, h - 4.5, m + 3, h - 7.5, m, h - 10.5, m - 3, h - 7.5, P['acc'])
        return o
    def amb(self, w, h, role, uid):
        m = w / 2
        return '<path d="M%s %sL%s %sL%s %sL%s %sZ" fill="#FF7A8A">%s</path><path d="M%s %sL%s %sL%s %sL%s %sZ" fill="#FF7A8A">%s</path>' % (m, 4.5, m + 3, 7.5, m, 10.5, m - 3, 7.5, A('opacity', '1;.2;1', '2.4s'), m, h - 4.5, m + 3, h - 7.5, m, h - 10.5, m - 3, h - 7.5, A('opacity', '.2;1;.2', '2.4s'))
    def motif(self, cx, cy, s, anim=True):  # bat
        return '<g transform="translate(%s,%s) scale(%s)"><path d="M0 -3 L1.5 -6 L3 -3 C6 -5 10 -4 14 -6 C13 -3 13 -1 12 1 C10 -1 8 0 7 3 C5 1 3 1 0 5 C-3 1 -5 1 -7 3 C-8 0 -10 -1 -12 1 C-13 -1 -13 -3 -14 -6 C-10 -4 -6 -5 -3 -3 L-1.5 -6Z" fill="%s">%s</path></g>' % (f(cx), f(cy), s, self.P['acc2'], AT('scale', '1 1;1 .8;1 1', '1s', spl=S(2, EASE)) if anim else '')
    def thumb(self, cx, cy, r, anim=True):
        return '<g transform="translate(%s,%s)"><path d="M0 %sL%s 0L0 %sL%s 0Z" fill="%s" stroke="#FF7A8A" stroke-width=".8">%s</path><path d="M0 %sL%s 0L0 0Z" fill="#fff" opacity=".25"/></g>' % (f(cx), f(cy), f(-r - 2), f(r), f(r + 2), f(-r), self.P['acc'], A('opacity', '1;.7;1', '2s') if anim else '', f(-r - 2), f(r * .5))
    def wings_btn(self, w, h):
        return '<g transform="translate(41,0)">%s</g><g transform="translate(%s,0)">%s</g>' % (self.wing('L', h), w - 41, self.wing('R', h))

# ---------------- COQUETTE ----------------
class Coquette(Skin):
    id = 'coquette'; r = 22; sw = 1.4
    P = dict(bg='#FFF6F9', surf='#FFFFFF', ink='#3B1824', ink2='#7D4E5E', acc='#D96588', acc2='#E8A5BA', bd='#F5CCD9')
    def path(self, w, h, i=0):
        r = min((h - 6) / 2, 24) - i; y0 = i + 3; y1 = h - i - 3
        nx = max(3, int((w - 2 * r - 2 * i) / 20)); sx = (w - 2 * r - 2 * i) / nx
        ny = max(0, int((y1 - y0 - 2 * r) / 20)); sy = (y1 - y0 - 2 * r) / ny if ny else 0
        d = 'M%s %s' % (f(r + i), f(y0)) + ''.join('a%s %s 0 0 1 %s 0' % (f(sx / 2), f(sx / 4), f(sx)) for _ in range(nx))
        d += 'A%s %s 0 0 1 %s %s' % (f(r), f(r), f(w - i), f(y0 + r))
        d += ''.join('a%s %s 0 0 1 0 %s' % (f(sy / 4), f(sy / 2), f(sy)) for _ in range(ny)) if ny else ''
        d += 'A%s %s 0 0 1 %s %s' % (f(r), f(r), f(w - i - r), f(y1))
        d += ''.join('a%s %s 0 0 1 %s 0' % (f(sx / 2), f(sx / 4), f(-sx)) for _ in range(nx))
        d += 'A%s %s 0 0 1 %s %s' % (f(r), f(r), f(i), f(y1 - r))
        d += ''.join('a%s %s 0 0 1 0 %s' % (f(sy / 4), f(sy / 2), f(-sy)) for _ in range(ny)) if ny else ''
        return d + 'A%s %s 0 0 1 %s %sZ' % (f(r), f(r), f(r + i), f(y0))
    def fills(self, role, uid):
        P = self.P
        if role == 'primary': return lin('g' + uid, [(0, '#E97FA0'), (1, '#CC5278')]), 'url(#g%s)' % uid, '#B84468', 1.2
        if role == 'ghost': return '', '#FFFFFF', P['acc'], 1.4
        if role == 'tonal': return '', '#FFE3EC', P['acc2'], 1
        return '', P['surf'], P['bd'], 1.4
    def bow(self, cx, cy, s, anim=True, c1='#FFE3EC', c2='#F6B8CB'):
        a = AT('rotate', '-6 0 0;6 0 0;-6 0 0', '2.6s', spl=S(2, EASE)) if anim else ''
        return '<g transform="translate(%s,%s) scale(%s)"><g>%s<path d="M0 0C-12 -10 -17 -1 -13 6C-9 13 -3 7 0 0Z" fill="%s"/><path d="M0 0C12 -10 17 -1 13 6C9 13 3 7 0 0Z" fill="%s"/><path d="M-1 3L-8 15L-3 12L0 16Z" fill="%s"/><path d="M1 3L8 15L3 12L0 16Z" fill="%s"/><path d="M-10 0Q-8 4 -4 4M10 0Q8 4 4 4" stroke="#fff" stroke-opacity=".6" stroke-width=".7"/><circle r="3.2" fill="%s"/></g></g>' % (f(cx), f(cy), s, a, c1, c1, c2, c2, mixc(c2, '#B84468', .4))
    def deco(self, w, h, role, uid):
        o = '<path d="M%s %sH%s" stroke="%s" stroke-opacity=".7" stroke-width="1" stroke-dasharray="2 5" stroke-linecap="round"/>' % (30, 11, w - 30, '#FFFFFF' if role == 'primary' else self.P['acc2'])
        o += '<path d="M%s %sH%s" stroke="%s" stroke-opacity=".7" stroke-width="1" stroke-dasharray="2 5" stroke-linecap="round"/>' % (30, h - 11, w - 30, '#FFFFFF' if role == 'primary' else self.P['acc2'])
        return o + self.bow(22, 12, .5, False) + self.bow(w - 22, 12, .5, False)
    def amb(self, w, h, role, uid):
        o = ''
        for k, (x, y) in enumerate(((w * .3, h * .5), (w * .62, h * .35), (w * .8, h * .62))):
            o += '<g transform="translate(%s,%s)"><path d="%s" fill="#fff" opacity="0">%s%s</path></g>' % (f(x), f(y), star4(0, 0, 4, .25), A('opacity', '0;.95;0', '2.4s', begin='%ss' % (k * .7)), AT('scale', '.4;1.1;.4', '2.4s', begin='%ss' % (k * .7)))
        return o
    def motif(self, cx, cy, s, anim=True): return self.bow(cx, cy, s * .9, anim, '#FFE3EC' , '#F6B8CB')
    def thumb(self, cx, cy, r, anim=True):
        k = r / 9
        return '<g transform="translate(%s,%s) scale(%s)"><path d="M0 8C-12 0 -9 -8 -4.5 -8C-2 -8 0 -6 0 -4C0 -6 2 -8 4.5 -8C9 -8 12 0 0 8Z" fill="%s" stroke="#fff" stroke-width="1.2">%s</path></g>' % (f(cx), f(cy), f(k), self.P['acc'], AT('scale', '1;1.12;1', '1.4s', spl=S(2, EASE)) if anim else '')

# ---------------- Y2K ----------------
class Y2K(Skin):
    id = 'y2k'; dark = True; sw = 1.4
    P = dict(bg='#0E0D1B', surf='#181632', ink='#FFFFFF', ink2='#D8D6F2', acc='#FF2EA6', acc2='#38BDF8', bd='#47427A')
    def path(self, w, h, i=0): return rr(i, i, w - 2 * i, h - 2 * i, min(h / 2, 26) - i)
    def fills(self, role, uid):
        P = self.P
        if role == 'primary': return lin('g' + uid, [(0, '#FFFFFF'), (.12, '#FFB6E0'), (.5, '#FF2EA6'), (.52, '#C2007A'), (1, '#FF6AC4')]), 'url(#g%s)' % uid, '#FFFFFF', 1.2
        if role == 'ghost': return lin('g' + uid, [(0, '#2A2652'), (1, '#181632')]), 'url(#g%s)' % uid, 'url(#b%s)' % uid, 1.6
        if role == 'tonal': return lin('g' + uid, [(0, '#33295F'), (1, '#1E1A3F')]), 'url(#g%s)' % uid, P['acc2'], 1
        return '', P['surf'], P['bd'], 1.4
    def body(self, w, h, role, uid):
        d_, fl, st, sw = self.fills(role, uid)
        if role == 'ghost': d_ += lin('b' + uid, [(0, '#38BDF8'), (.5, '#FF2EA6'), (1, '#38BDF8')], 0, 0, 1, 0)
        d = self.path(w, h, 1); o = '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (d, fl, st, sw)
        o += '<path d="%s" fill="#fff" opacity="%s"/>' % (rr(6, 3, w - 12, h * .42, h * .2), .38 if role == 'primary' else .1)
        o += '<path d="M%s %sH%s" stroke="#fff" stroke-opacity=".5" stroke-width="1" stroke-linecap="round"/>' % (h * .5, h - 5, w - h * .5)
        return d_, o + self.deco(w, h, role, uid)
    def deco(self, w, h, role, uid):
        return '<path d="%s" fill="#fff"/><path d="%s" fill="#38BDF8"/>' % (star4(w - 16, 12, 6), star4(16, h - 12, 4))
    def amb(self, w, h, role, uid):
        o = sweep(w, h, self.path(w, h, 1), '2.8s', '#FFFFFF', .7, 18, id_='cp' + uid)
        o += '<g transform="translate(%s,12)"><path d="%s" fill="#fff">%s%s</path></g>' % (w - 16, star4(0, 0, 8), AT('scale', '.5;1.2;.5', '1.8s', spl=S(2, EASE)), AT('rotate', '0;90', '1.8s', additive='sum'))
        o += '<g transform="translate(16,%s)"><path d="%s" fill="#38BDF8">%s</path></g>' % (h - 12, star4(0, 0, 5), AT('scale', '1.1;.4;1.1', '1.5s', spl=S(2, EASE)))
        return o
    def motif(self, cx, cy, s, anim=True): return '<g transform="translate(%s,%s) scale(%s)"><path d="%s" fill="#fff">%s</path><path d="%s" fill="#FF2EA6" transform="translate(9,-6)">%s</path></g>' % (f(cx), f(cy), s, star4(0, 0, 8), AT('scale', '.6;1.15;.6', '1.8s', spl=S(2, EASE)) if anim else '', star4(0, 0, 4), AT('scale', '1.1;.5;1.1', '1.4s', spl=S(2, EASE)) if anim else '')
    def thumb(self, cx, cy, r, anim=True):
        return '<g transform="translate(%s,%s)"><circle r="%s" fill="url(#orb)" stroke="#fff" stroke-width="1"/><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" opacity=".7"/></g>' % (f(cx), f(cy), f(r), f(-r * .25), f(-r * .35), f(r * .4), f(r * .25))

# ---------------- STREETWEAR ----------------
class Street(Skin):
    id = 'streetwear'; dark = True; r = 5; sw = 2
    P = dict(bg='#111215', surf='#191B20', ink='#FFFFFF', ink2='#D1D5DB', acc='#F97316', acc2='#38BDF8', bd='#323640')
    def path(self, w, h, i=0): return rr(i, i, w - 7 - 2 * i, h - 7 - 2 * i, 4)
    def body(self, w, h, role, uid):
        P = self.P; W = w - 7; H = h - 7; d = rr(1, 1, W - 2, H - 2, 4)
        cp = '<clipPath id="k%s"><path d="%s"/></clipPath>' % (uid, d)
        sh = '<path d="%s" fill="%s" transform="translate(7,7)"/>' % (d, '#000000' if role == 'primary' else P['acc'] if role != 'ghost' else '#000')
        sh = '<path d="%s" fill="%s" transform="translate(6,6)"/>' % (d, P['acc2'] if role == 'primary' else P['bd'])
        fl = P['acc'] if role == 'primary' else ('#111215' if role == 'ghost' else '#2A1608')
        o = sh + '<path d="%s" fill="%s" stroke="#fff" stroke-width="2"/>' % (d, fl)
        # hazard tape strip along bottom
        o += '<g clip-path="url(#k%s)"><g transform="translate(0,%s)">%s</g></g>' % (uid, H - 9, '<g>%s%s</g>' % (''.join('<path d="M%s 0l8 0l-8 8l-8 0z" fill="#111215" opacity=".9"/>' % (x * 16 - 6) for x in range(0, int(W / 16) + 3)), AT('translate', '0 0;16 0', '1s', mode='linear')))
        o += '<g clip-path="url(#k%s)"><g transform="translate(0,0)">%s</g></g>' % (uid, '<path d="M12 6h30M12 10h18" stroke="#fff" stroke-opacity=".35" stroke-width="1.5"/>')
        return cp, o
    def amb(self, w, h, role, uid):
        W = w - 7; return '<g><path d="M%s 5h14v14h-14z" fill="none" stroke="#fff" stroke-width="2"/><path d="M%s 8l5 5M%s 13l5-5" stroke="#fff" stroke-width="1.6"/>%s</g>' % (W - 24, W - 20, W - 20, A('opacity', '1;1;0;1', '2.4s', kt='0;.7;.75;1', mode='discrete'))
    def motif(self, cx, cy, s, anim=True): return '<g transform="translate(%s,%s) scale(%s)"><path d="M-6 -10L2 -10L-2 -2L6 -2L-6 12L-2 2L-8 2Z" fill="#F97316" stroke="#fff" stroke-width="1">%s</path></g>' % (f(cx), f(cy), s, A('opacity', '1;1;.3;1;.3;1', '2.2s', kt='0;.6;.65;.7;.75;1', mode='discrete') if anim else '')
    def thumb(self, cx, cy, r, anim=True): return '<g transform="translate(%s,%s)"><rect x="%s" y="%s" width="%s" height="%s" fill="#000" transform="translate(3,3)"/><rect x="%s" y="%s" width="%s" height="%s" fill="#F97316" stroke="#fff" stroke-width="2"/></g>' % (f(cx), f(cy), f(-r), f(-r), f(2 * r), f(2 * r), f(-r), f(-r), f(2 * r), f(2 * r))

# ---------------- K-FASHION ----------------
class KF(Skin):
    id = 'k-fashion'; r = 16; sw = 1
    P = dict(bg='#F5F6FA', surf='#FFFFFF', ink='#141519', ink2='#525866', acc='#4F6D8A', acc2='#94A3B8', bd='#D6DCE8')
    def path(self, w, h, i=0): return rr(i, i, w - 2 * i, h - 2 * i, min(h / 2, 26) - i)
    def fills(self, role, uid):
        P = self.P
        if role == 'primary': return lin('g' + uid, [(0, '#5C7C9B'), (1, '#3F5B77')]), 'url(#g%s)' % uid, 'none', 0
        if role == 'ghost': return '', '#FFFFFF', P['acc'], 1
        return '', '#E9EEF5', 'none', 0
    def deco(self, w, h, role, uid):
        c = '#fff' if role == 'primary' else self.P['acc']; o = ''
        for x, y, sx, sy in ((10, 8, 1, 1), (w - 10, 8, -1, 1), (10, h - 8, 1, -1), (w - 10, h - 8, -1, -1)):
            o += '<path d="M%s %sH%s M%s %sV%s" stroke="%s" stroke-width="1" opacity=".7"/>' % (x, y, x + 6 * sx, x, y, y + 6 * sy, c)
        o += '<circle cx="%s" cy="%s" r="1.6" fill="%s"/>' % (w / 2, 7, c)
        o += '<path d="M%s %sH%s" stroke="%s" stroke-width=".7" stroke-dasharray="1 3" opacity=".7"/>' % (h, h - 8, w - h, c)
        return o
    def amb(self, w, h, role, uid):
        c = '#fff' if role == 'primary' else self.P['acc']
        return '<g><path d="M%s %sH%s" stroke="%s" stroke-width="1" stroke-linecap="round">%s</path></g>' % (h * .6, h - 4, w - h * .6, c, A('stroke-dasharray', '0 400;400 0;0 400', '3.6s', spl=S(2, EASE)))
    def thumb(self, cx, cy, r, anim=True): return '<circle cx="%s" cy="%s" r="%s" fill="#fff" stroke="%s" stroke-width="1.5"/><circle cx="%s" cy="%s" r="%s" fill="%s">%s</circle>' % (f(cx), f(cy), f(r), self.P['acc'], f(cx), f(cy), f(r * .35), self.P['acc'], A('r', '%s;%s;%s' % (f(r * .35), f(r * .5), f(r * .35)), '2s', spl=S(2, EASE)) if anim else '')
    def motif(self, cx, cy, s, anim=True): return '<g transform="translate(%s,%s) scale(%s)"><circle r="7" stroke="%s" stroke-width="1"/><path d="M-10 0H10M0 -10V10" stroke="%s" stroke-width=".8">%s</path></g>' % (f(cx), f(cy), s, self.P['acc'], self.P['acc'], AT('rotate', '0;90', '4s', spl=EASE) if anim else '')

# ---------------- QUIET LUXURY ----------------
class QL(Skin):
    id = 'quiet-luxury'; r = 2; sw = 1
    P = dict(bg='#F7F4EF', surf='#FFFFFF', ink='#1C1917', ink2='#57534E', acc='#B48811', acc2='#78716C', bd='#E7E5E4')
    def path(self, w, h, i=0): return rr(i, i, w - 2 * i, h - 2 * i, 2)
    def fills(self, role, uid):
        P = self.P
        if role == 'primary': return lin('g' + uid, [(0, '#2A2623'), (1, '#14110F')]), 'url(#g%s)' % uid, P['acc'], 1
        if role == 'ghost': return '', '#FFFFFF', '#1C1917', 1
        return '', '#EFE9DD', 'none', 0
    def deco(self, w, h, role, uid):
        g = '#D6B24A' if role == 'primary' else self.P['acc']
        o = '<path d="%s" stroke="%s" stroke-width=".7" opacity=".9"/>' % (self.path(w, h, 5), g)
        o += '<path d="M%s %sL%s %sL%s %sL%s %sZ" fill="%s"/>' % (w / 2, 2.5, w / 2 + 3, 5, w / 2, 7.5, w / 2 - 3, 5, g)
        o += '<path d="M%s %sH%s M%s %sH%s" stroke="%s" stroke-width=".7"/>' % (12, h / 2, 24, w - 24, h / 2, w - 12, g)
        return o
    def amb(self, w, h, role, uid):
        g = '#F5DC8A' if role == 'primary' else self.P['acc']; d = self.path(w, h, 5)
        return '<path d="%s" stroke="%s" stroke-width="1.6" stroke-linecap="round" stroke-dasharray="24 %s" pathLength="1">%s</path>' % (d, g, 600, '<animate attributeName="stroke-dashoffset" values="0;-%s" dur="5s" repeatCount="indefinite"/>' % int(2 * (w + h) - 40)) + '<path d="%s" stroke="none"/>' % d
    def thumb(self, cx, cy, r, anim=True): return '<g transform="translate(%s,%s) rotate(45)"><rect x="%s" y="%s" width="%s" height="%s" fill="#14110F" stroke="#B48811" stroke-width="1"/></g>' % (f(cx), f(cy), f(-r * .75), f(-r * .75), f(r * 1.5), f(r * 1.5))
    def motif(self, cx, cy, s, anim=True): return '<g transform="translate(%s,%s) scale(%s)"><path d="M0 -8L5 0L0 8L-5 0Z" stroke="%s" stroke-width="1">%s</path></g>' % (f(cx), f(cy), s, self.P['acc'], AT('scale', '1 1;.4 1;1 1', '3s', spl=S(2, EASE)) if anim else '')

# ---------------- PIXEL ----------------
class Pixel(Skin):
    id = 'pixel'; dark = True; sw = 0
    P = dict(bg='#120B2E', surf='#1D1347', ink='#FFFFFF', ink2='#C9C2F5', acc='#FFD23F', acc2='#FF3D81', bd='#3A2C7A', cy='#38D9FF')
    def path(self, w, h, i=0, s=4):
        s = s; x0, y0, x1, y1 = i, i, w - i, h - i
        return poly([(x0 + 2 * s, y0), (x1 - 2 * s, y0), (x1 - 2 * s, y0 + s), (x1 - s, y0 + s), (x1 - s, y0 + 2 * s), (x1, y0 + 2 * s), (x1, y1 - 2 * s), (x1 - s, y1 - 2 * s), (x1 - s, y1 - s), (x1 - 2 * s, y1 - s), (x1 - 2 * s, y1), (x0 + 2 * s, y1), (x0 + 2 * s, y1 - s), (x0 + s, y1 - s), (x0 + s, y1 - 2 * s), (x0, y1 - 2 * s), (x0, y0 + 2 * s), (x0 + s, y0 + 2 * s), (x0 + s, y0 + s), (x0 + 2 * s, y0 + s)])
    def body(self, w, h, role, uid):
        P = self.P; s = 4
        face = {'primary': P['acc'], 'ghost': P['surf'], 'tonal': '#2A1F63'}.get(role, P['surf']); hi = {'primary': '#FFE88A', 'ghost': '#2E2266', 'tonal': '#3A2C7A'}.get(role, '#2E2266'); lo = {'primary': '#C9981A', 'ghost': '#120B2E', 'tonal': '#120B2E'}.get(role, '#120B2E')
        o = '<path d="%s" fill="#0A0620" transform="translate(0,4)"/><path d="%s" fill="%s"/>' % (self.path(w, h, 0), self.path(w, h, 0), '#0A0620')
        o += '<path d="%s" fill="%s"/>' % (self.path(w, h - 4, 4), lo) + '<path d="%s" fill="%s"/>' % (self.path(w, h - 8, 4), face)
        o += '<path d="M%s %sH%s v4 H%s Z" fill="%s"/>' % (12, 8, w - 12, 12, hi)
        if role == 'ghost': o += '<path d="%s" fill="none" stroke="%s" stroke-width="4" transform="translate(0,0)"/>' % (self.path(w, h - 4, 2), P['acc'])
        o += '<rect x="8" y="%s" width="8" height="8" fill="%s"/><rect x="%s" y="%s" width="8" height="8" fill="%s"/>' % (h / 2 - 8, P['cy'], w - 16, h / 2 - 8, P['acc2'])
        return '', o
    def amb(self, w, h, role, uid):
        P = self.P; return '<g>%s<rect x="%s" y="8" width="8" height="4" fill="#fff"/></g>' % (A('opacity', '1;1;0;0;1', '1.6s', kt='0;.4;.4;.6;1', mode='discrete'), w / 2 + 40) + '<g><rect x="12" y="%s" width="4" height="4" fill="#fff">%s</rect></g>' % (h - 18, A('opacity', '0;1;0', '1.2s', mode='discrete', kt='0;.5;1'))
    def thumb(self, cx, cy, r, anim=True): return '<rect x="%s" y="%s" width="%s" height="%s" fill="#0A0620"/><rect x="%s" y="%s" width="%s" height="%s" fill="#FFD23F"/><rect x="%s" y="%s" width="%s" height="%s" fill="#FFE88A"/>' % (f(cx - r - 2), f(cy - r - 2), f(2 * r + 4), f(2 * r + 4), f(cx - r), f(cy - r), f(2 * r), f(2 * r), f(cx - r), f(cy - r), f(2 * r), f(r * .5))
    def motif(self, cx, cy, s, anim=True):
        return '<g transform="translate(%s,%s) scale(%s)"><g>%s<rect x="-6" y="-8" width="12" height="16" fill="#C9981A"/><rect x="-4" y="-10" width="8" height="2" fill="#C9981A"/><rect x="-4" y="8" width="8" height="2" fill="#C9981A"/><rect x="-4" y="-8" width="8" height="16" fill="#FFD23F"/><rect x="-2" y="-6" width="2" height="12" fill="#FFE88A"/></g></g>' % (f(cx), f(cy), s, AT('scale', '1 1;.34 1;1 1;1 1', '1.4s', mode='discrete', kt='0;.25;.5;1') if anim else '')

# ---------------- MINIMAL ----------------
class Minimal(Skin):
    id = 'minimal'; r = 2; sw = 1
    P = dict(bg='#FAFAFA', surf='#FFFFFF', ink='#09090B', ink2='#52525B', acc='#18181B', acc2='#A1A1AA', bd='#E4E4E7')
    def path(self, w, h, i=0): return rr(i, i, w - 2 * i, h - 2 * i, 2)
    def fills(self, role, uid):
        if role == 'primary': return '', '#18181B', 'none', 0
        if role == 'ghost': return '', '#FFFFFF', '#18181B', 1
        return '', '#F4F4F5', 'none', 0
    def deco(self, w, h, role, uid):
        c = '#fff' if role == 'primary' else '#18181B'
        return '<circle cx="14" cy="%s" r="2" fill="%s"/><path d="M%s %sH%s" stroke="%s" stroke-width="1" opacity=".5"/>' % (h / 2, c, w - 40, h / 2, w - 16, c) + '<path d="M%s %sl4 -4M%s %sl4 4" stroke="%s" stroke-width="1" transform="translate(-16,0)"/>' % (w - 16, h / 2, w - 16, h / 2, c)
    def amb(self, w, h, role, uid):
        c = '#fff' if role == 'primary' else '#18181B'
        return '<path d="M12 %sH%s" stroke="%s" stroke-width="1.5"><animate attributeName="stroke-dasharray" values="0 %s;%s 0;%s 0;0 %s" keyTimes="0;.4;.8;1" dur="3.6s" repeatCount="indefinite"/></path>' % (h - 6, w - 12, c, w, w, w, w) + '<circle cx="14" cy="%s" r="2" fill="%s">%s</circle>' % (h / 2, c, A('r', '2;3.6;2', '2s', spl=S(2, EASE)))
    def thumb(self, cx, cy, r, anim=True): return '<circle cx="%s" cy="%s" r="%s" fill="#18181B"/>' % (f(cx), f(cy), f(r))
    def motif(self, cx, cy, s, anim=True): return '<circle cx="%s" cy="%s" r="%s" stroke="#18181B" stroke-width="1">%s</circle>' % (f(cx), f(cy), f(6 * s), A('r', '%s;%s;%s' % (f(4 * s), f(8 * s), f(4 * s)), '2.4s', spl=S(2, EASE)) if anim else '')

# ---------------- GRUNGE ----------------
class Grunge(Skin):
    id = 'grunge'; dark = True; r = 3; sw = 1.4
    P = dict(bg='#181512', surf='#221E1A', ink='#F4F4F5', ink2='#D6D3D1', acc='#D97706', acc2='#A8A29E', bd='#44403C')
    def path(self, w, h, i=0):
        rnd = random.Random(int(w * 7 + h * 3 + i)); pts = []
        n = int(w / 9)
        for k in range(n + 1): pts.append((i + k * (w - 2 * i) / n, i + rnd.uniform(0, 4) * (1 if k % 2 else .4)))
        for k in range(3): pts.append((w - i - rnd.uniform(0, 2), i + (k + 1) * (h - 2 * i) / 4))
        for k in range(n + 1): pts.append((w - i - k * (w - 2 * i) / n, h - i - rnd.uniform(0, 4) * (1 if k % 2 else .4)))
        for k in range(3): pts.append((i + rnd.uniform(0, 2), h - i - (k + 1) * (h - 2 * i) / 4))
        return poly(pts)
    def fills(self, role, uid):
        P = self.P
        if role == 'primary': return '', P['acc'], '#7C3F00', 1.2
        if role == 'ghost': return '', '#181512', P['acc2'], 1.2
        return '', '#2A2018', '#6B4A24', 1
    def deco(self, w, h, role, uid):
        P = self.P; c = '#181512' if role == 'primary' else P['acc2']; o = ''
        o += '<g opacity=".28">%s</g>' % ''.join('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(14 + (i % 22) * (w - 28) / 22), f(10 + (i // 22) * 7 + (i % 2) * 3), 1.2, c) for i in range(66))
        o += '<path d="M10 %sH%s" stroke="%s" stroke-width="1" stroke-dasharray="5 3" opacity=".6"/>' % (h - 7, w - 10, c)
        o += '<g transform="translate(%s,-3) rotate(-6)"><rect width="38" height="12" fill="#E8DFC8" opacity=".85"/></g><g transform="translate(%s,%s) rotate(5)"><rect width="38" height="12" fill="#E8DFC8" opacity=".85"/></g>' % (-8, w - 30, h - 9)
        return o
    def amb(self, w, h, role, uid):
        return '<g>%s<path d="M%s 14l14 0M%s 20l9 0" stroke="#fff" stroke-opacity=".5" stroke-width="1.4"/></g>' % (AT('translate', '0 0;1.5 -1;-1 1;0 0;0 0', '1.8s', mode='discrete', kt='0;.1;.2;.3;1'), w / 2 - 30, w / 2 - 30)
    def thumb(self, cx, cy, r, anim=True): return '<g transform="translate(%s,%s) rotate(-8)"><rect x="%s" y="%s" width="%s" height="%s" fill="#E8DFC8"/><rect x="%s" y="%s" width="%s" height="%s" fill="#D97706" opacity=".8"/></g>' % (f(cx), f(cy), f(-r - 2), f(-r), f(2 * r + 4), f(2 * r), f(-r + 2), f(-r + 2), f(2 * r), f(2 * r - 4))
    def motif(self, cx, cy, s, anim=True): return '<g transform="translate(%s,%s) scale(%s)"><path d="M-9 -2L-2 -9L9 2L2 9Z" fill="#D97706" stroke="#181512" stroke-width="1">%s</path><path d="M-4 0L0 -4L4 0L0 4Z" fill="#181512"/></g>' % (f(cx), f(cy), s, AT('rotate', '-4 0 0;4 0 0;-4 0 0', '1.4s', mode='discrete', kt='0;.5;1') if anim else '')

# ---------------- OLD MONEY ----------------
class OldMoney(Skin):
    id = 'old-money'; r = 4; sw = 1.2
    P = dict(bg='#F4F1EA', surf='#FFFFFF', ink='#14261C', ink2='#4A5D52', acc='#14261C', acc2='#3F624D', bd='#DDD6C8', gold='#B08D3C')
    def path(self, w, h, i=0):
        n = 9 - i
        return 'M%s %sH%sA%s %s 0 0 0 %s %sV%sA%s %s 0 0 1 %s %sH%sH%sA%s %s 0 0 0 %s %sV%sA%s %s 0 0 1 %s %sZ' % tuple(map(f, (i, i, w - i, n, n, w - i, h / 2 - n * 0 - 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))) if False else self._tk(w, h, i)
    def _tk(self, w, h, i):
        n = 8; m = h / 2
        return 'M%s %sH%sV%sA%s %s 0 0 0 %s %sV%sH%sH%sV%sA%s %s 0 0 0 %s %sV%sZ' % tuple(map(f, (i, i, w - i, m - n, n, n, w - i, m + n, h - i, i, i, m + n, n, n, i, m - n, i)))
    def fills(self, role, uid):
        P = self.P
        if role == 'primary': return lin('g' + uid, [(0, '#1D3A2B'), (1, '#0F2218')]), 'url(#g%s)' % uid, P['gold'], 1.2
        if role == 'ghost': return '', '#FFFFFF', P['acc'], 1.2
        return '', '#E9E5D8', 'none', 0
    def deco(self, w, h, role, uid):
        g = '#D8B65C' if role == 'primary' else self.P['gold']
        o = '<path d="%s" stroke="%s" stroke-width=".8" stroke-dasharray="2 3" opacity=".9"/>' % (self.path(w, h, 5), g)
        o += self.crest(w / 2, h / 2 - 1, .8, g, False) if False else ''
        o += '<path d="M%s %sH%s M%s %sH%s" stroke="%s" stroke-width=".8"/>' % (22, h / 2, w / 2 - 40, w / 2 + 40, h / 2, w - 22, g)
        return o
    def crest(self, cx, cy, s, g, anim=True):
        return '<g transform="translate(%s,%s) scale(%s)"><path d="M0 -9L7 -6V1C7 5 3 8 0 9C-3 8 -7 5 -7 1V-6Z" stroke="%s" stroke-width="1.2" fill="none"/><path d="M-3 -1L0 -4L3 -1M-3 2L0 -1L3 2" stroke="%s" stroke-width="1"/></g>' % (f(cx), f(cy), s, g, g)
    def amb(self, w, h, role, uid):
        g = '#F2D88A' if role == 'primary' else self.P['gold']
        return self.crest(w / 2, h / 2, 1, g) + '<g opacity=".0"><path d="M0 0" /></g>' + sweep(w, h, self.path(w, h, 1), '4.2s', '#F2D88A', .35, 14, id_='cp' + uid)
    def thumb(self, cx, cy, r, anim=True): return '<circle cx="%s" cy="%s" r="%s" fill="#14261C" stroke="#B08D3C" stroke-width="1.5"/><circle cx="%s" cy="%s" r="%s" stroke="#B08D3C" stroke-width=".7"/>' % (f(cx), f(cy), f(r), f(cx), f(cy), f(r * .55))
    def motif(self, cx, cy, s, anim=True): return self.crest(cx, cy, s * 1.1, self.P['gold'])

# ---------------- CASUAL ----------------
class Casual(Skin):
    id = 'casual'; r = 16; sw = 0
    P = dict(bg='#F8FAFC', surf='#FFFFFF', ink='#0F172A', ink2='#475569', acc='#059669', acc2='#64748B', bd='#E2E8F0')
    def path(self, w, h, i=0): return rr(i, i, w - 2 * i, h - 6 - 2 * i, (h - 6) / 2 - i)
    def body(self, w, h, role, uid):
        P = self.P; d = rr(0, 0, w, h - 6, (h - 6) / 2)
        fl = {'primary': P['acc'], 'ghost': '#FFFFFF', 'tonal': '#D8F3E7'}.get(role, '#fff'); sh = {'primary': '#047857', 'ghost': '#CBD5E1', 'tonal': '#A7DFC6'}.get(role, '#CBD5E1')
        o = '<path d="%s" fill="%s" transform="translate(0,5)"/><path d="%s" fill="%s"%s/>' % (d, sh, d, fl, (' stroke="#059669" stroke-width="1.6"' if role == 'ghost' else ''))
        o += '<path d="%s" fill="#fff" opacity="%s"/>' % (rr(10, 4, w - 20, 10, 5), .22 if role == 'primary' else .0)
        o += '<g transform="translate(%s,%s)"><path d="M0 0C6 -9 18 -8 20 -2C14 2 6 4 0 0Z" fill="%s" opacity=".95"/><path d="M0 0L14 -4" stroke="%s" stroke-width="1"/></g>' % (14, h / 2 - 3, '#6EE7B7' if role == 'primary' else '#10B981', '#047857')
        return '', o
    def amb(self, w, h, role, uid): return '<g>%s</g>' % ''.join('<circle cx="%s" cy="%s" r="2.2" fill="%s" opacity="0">%s%s</circle>' % (f(w - 26 + k * 7), f(h * .5), '#fff' if role == 'primary' else '#10B981', A('opacity', '0;1;0', '1.2s', begin='%ss' % (k * .25)), A('cy', '%s;%s' % (f(h * .5 + 6), f(h * .5 - 8)), '1.2s', begin='%ss' % (k * .25))) for k in range(3))
    def thumb(self, cx, cy, r, anim=True): return '<circle cx="%s" cy="%s" r="%s" fill="#fff" stroke="#047857" stroke-width="1.2"/><path d="M%s %sC%s %s %s %s %s %sC%s %s %s %s %s %sZ" fill="#10B981"/>' % (f(cx), f(cy + 1.5), f(r), f(cx - r * .45), f(cy + 2), f(cx - r * .2), f(cy - r * .5), f(cx + r * .35), f(cy - r * .35), f(cx + r * .45), f(cy), f(cx + r * .25), f(cy + r * .5), f(cx - r * .2), f(cy + r * .55), f(cx - r * .45), f(cy + 2))
    def motif(self, cx, cy, s, anim=True): return '<g transform="translate(%s,%s) scale(%s)"><path d="M0 8C-10 4 -10 -6 0 -9C10 -6 10 4 0 8Z" fill="#10B981">%s</path><path d="M0 8V-5" stroke="#047857" stroke-width="1.2"/></g>' % (f(cx), f(cy), s, AT('rotate', '-8 0 8;8 0 8;-8 0 8', '2.4s', spl=S(2, EASE)) if anim else '')

# ---------------- PARTY ----------------
class Party(Skin):
    id = 'party-wear'; dark = True; sw = 1.2
    P = dict(bg='#0D0A14', surf='#161122', ink='#FFFFFF', ink2='#D4D4D8', acc='#D4AF37', acc2='#E5E7EB', bd='#352B4D')
    def path(self, w, h, i=0): return rr(i, i, w - 2 * i, h - 2 * i, 16 - i)
    def fills(self, role, uid):
        P = self.P
        if role == 'primary': return lin('g' + uid, [(0, '#FFF1B0'), (.25, '#E6C453'), (.55, '#B98E1F'), (.8, '#E9CD6A'), (1, '#9A7413')]), 'url(#g%s)' % uid, '#FFF1B0', 1
        if role == 'ghost': return '', '#161122', '#D4AF37', 1.4
        return '', '#241B33', '#6B5A2A', 1
    def deco(self, w, h, role, uid):
        c = '#5A430A' if role == 'primary' else '#D4AF37'
        o = '<path d="%s" stroke="%s" stroke-width=".8" opacity=".55"/>' % (self.path(w, h, 5), c)
        o += '<path d="M%s %sH%s" stroke="%s" stroke-width=".8" opacity=".5"/>' % (24, h / 2, 40, c) + '<path d="M%s %sH%s" stroke="%s" stroke-width=".8" opacity=".5"/>' % (w - 40, h / 2, w - 24, c)
        o += '<path d="%s" fill="#fff" opacity="%s"/>' % (rr(8, 3, w - 16, h * .28, 8), .3 if role == 'primary' else .06)
        return o
    def amb(self, w, h, role, uid):
        o = sweep(w, h, self.path(w, h, 1), '2.6s', '#FFFFFF', .75 if role == 'primary' else .25, 22, id_='cp' + uid)
        for k, (x, y, s) in enumerate(((w * .2, h * .3, 4), (w * .5, h * .72, 3), (w * .83, h * .34, 4.5), (w * .68, h * .2, 3))):
            o += '<g transform="translate(%s,%s)"><path d="%s" fill="%s" opacity="0">%s%s</path></g>' % (f(x), f(y), star4(0, 0, s, .2), '#FFF6D0' if role != 'primary' else '#fff', A('opacity', '0;1;0', '2s', begin='%ss' % (k * .5)), AT('scale', '.3;1.2;.3', '2s', begin='%ss' % (k * .5)))
        return o
    def thumb(self, cx, cy, r, anim=True): return '<g transform="translate(%s,%s)"><circle r="%s" fill="url(#gold)" stroke="#FFF1B0" stroke-width="1"/><circle r="%s" stroke="#7A5C10" stroke-width=".7"/><path d="%s" fill="#fff" opacity=".8"/></g>' % (f(cx), f(cy), f(r), f(r * .62), star4(0, 0, r * .45))
    def motif(self, cx, cy, s, anim=True):  # disco ball
        return '<g transform="translate(%s,%s) scale(%s)"><circle r="8" fill="#C9CBD6"/><path d="M-8 -2H8M-7 3H7M-4 -7L-2 7M3 -7L5 7M0 -8V8" stroke="#fff" stroke-width=".8" opacity=".7"/><path d="%s" fill="#fff" transform="translate(-3,-4)">%s</path></g>' % (f(cx), f(cy), s, star4(0, 0, 3), AT('scale', '.3;1;.3', '1.5s', spl=S(2, EASE)) if anim else '')

SKINS = [Goth(), Coquette(), Y2K(), Street(), KF(), QL(), Pixel(), Minimal(), Grunge(), OldMoney(), Casual(), Party()]
