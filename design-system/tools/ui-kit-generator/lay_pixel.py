from lay_core import *
def grid(w, h, fn):
    rows = []; pal = {}; keys = {}
    for y in range(h):
        r = ''
        for x in range(w):
            c = fn(x, y)
            if not c: r += '.'; continue
            if c not in keys: keys[c] = chr(65 + len(keys)); pal[keys[c]] = c
            r += keys[c]
        rows.append(r)
    return rows, pal
def disc(w, h, fn, r):
    cx, cy = (w - 1) / 2, (h - 1) / 2
    return grid(w, h, lambda x, y: fn(x, y, math.hypot(x - cx, y - cy), math.atan2(y - cy, x - cx)) if math.hypot(x - cx, y - cy) <= r else None)
def pic(rows, pal, u, x, y): return pxrows(rows, pal, u, x, y)
MON = ['.BBBBBBBBBBBB.', 'BGGGGGGGGGGGGB', 'BGKKKKKKKKKKGB', 'BGKKKKKKKKKKGB', 'BGKKKKKKKKKKGB', 'BGKKKKKKKKKKGB', 'BGKKKKKKKKKKGB', 'BGGGGGGGGGGGGB', '.BBBBBBBBBBBB.', '....BGGGGB....', '....BGGGGB....', '..BBBGGGGBBB..', '.BGGGGGGGGGGB.', '.BBBBBBBBBBBB.']
MONP = dict(B='#2B2540', G='#D9D6E6', K='#14131F')
HRT = ['..PP...PP...', '.PWPP.PPPP..', 'PWPPPPPPPPP.', 'PPPPPPPPPPP.', '.PPPPPPPPP..', '..PPPPPPP...', '...PPPPP....', '....PPP.....', '.....P......']
HRTP = dict(P='#FF9EC7', W='#FFFFFF')
HEART_BIG = ['..BB...BB..', '.BPPB.BPPB.', 'BPWPPBPPPPB', 'BPWPPPPPPPB', 'BPPPPPPPPPB', '.BPPPPPPPB.', '..BPPPPPB..', '...BPPPB...', '....BPB....', '.....B.....']
HGL = ['BBBBBBBBBB', 'BWWWWWWWWB', '.BWPPPPWB.', '..BWPPWB..', '...BWWB...', '....BB....', '....BB....', '...BWWB...', '..BWWWWB..', '.BWWWWWWB.', 'BWWWWWWWWB', 'BBBBBBBBBB']
HGLP = dict(B='#C2547E', W='#FFE3EF', P='#F7A8C8')
CLOUD = ['......XXXX..........', '....XXXXXXXX..XXX...', '..XXXXXXXXXXXXXXXX..', '.XXXXXXXXXXXXXXXXXX.', 'XXXXXXXXXXXXXXXXXXXX']
def clouds_layer(w, h, seed, col, col2, n=5, ys=None, u=6, dur=60):
    rnd = random.Random(seed); o = ''
    for i in range(n):
        y = (ys[i] if ys else rnd.uniform(0, h)); s = rnd.choice([1, 1.5, 2]); x0 = rnd.uniform(-100, w); sp = dur * rnd.uniform(.8, 1.4)
        cl = pxrows([r.replace('X', 'X') for r in CLOUD], {'X': col}, u * s, 0, 0) + pxrows(['.' * 0 + '.' * 20 for _ in range(0)], {}, 1)
        sh = pxrows(['....................'] * 4 + ['XXXXXXXXXXXXXXXXXXXX'], {'X': col2}, u * s, 0, 0)
        o += '<g><animateTransform attributeName="transform" type="translate" values="%s %s;%s %s" dur="%ss" begin="%ss" repeatCount="indefinite" calcMode="discrete" keyTimes="%s"/>%s%s</g>' % (f(-130 * s), f(y), f(w + 20), f(y), f(sp), f(-rnd.uniform(0, sp)), ';'.join(f(k / 40) for k in range(40)) if False else '0;1', cl, sh) if False else '<g transform="translate(0,%s)"><g>%s%s%s</g></g>' % (f(y), AT('translate', '%s 0;%s 0' % (f(-130 * s), f(w + 20)), '%ss' % f(sp), '%ss' % f(-rnd.uniform(0, sp)), mode='linear'), cl, sh)
    return o
def pixel_bg():
    o = '<defs>%s</defs>' % lin('pbg', [(0, '#5A48B2'), (1, '#43359A')])
    o += '<rect width="390" height="844" fill="url(#pbg)"/>'
    o += clouds_layer(390, 844, 3, '#7762CC', '#6A55C2', 7, [60, 200, 330, 470, 600, 720, 140], 6, 70)
    rnd = random.Random(11)
    for i in range(26):
        x = int(rnd.uniform(0, 390) // 4 * 4); y = int(rnd.uniform(0, 844) // 4 * 4); s = rnd.choice([3, 3, 4, 6])
        o += '<rect x="%s" y="%s" width="%s" height="%s" fill="#E9E0FF"><animate attributeName="opacity" values="1;1;.15;1" keyTimes="0;.5;.6;1" dur="%ss" begin="%ss" repeatCount="indefinite" calcMode="discrete"/></rect>' % (x, y, s, s, f(rnd.uniform(1.6, 4)), f(-rnd.uniform(0, 3)))
    for k, (x, y) in enumerate(((70, 790), (330, 300), (28, 640))): o += sparkle_plus(x, y, 1.2, '#fff', 2, k * .5)
    return o
def sparkle_plus(x, y, s=1, col='#fff', dur=1.8, b=0):
    return '<g transform="translate(%s,%s)"><g>%s<path d="M-1.5 -9h3v6h6v3h-6v6h-3v-6h-6v-3h6z" fill="%s" transform="scale(%s)"/></g></g>' % (x, y, AT('scale', '1;.3;1;1', '%ss' % dur, '%ss' % b, mode='discrete', kt='0;.4;.7;1'), col, s)
def win_panel(x, y, w, h, title, bodyfill='#C8C6D6', tb=('#4A56C8', '#8CA2F0')):
    o = '<rect x="%s" y="%s" width="%s" height="%s" fill="#1E1A3D" transform="translate(4,4)" opacity=".5"/>' % (x, y, w, h)
    o += '<rect x="%s" y="%s" width="%s" height="%s" fill="#2B2540"/><rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (x - 3, y - 3, w + 6, h + 6, x, y, w, h, bodyfill)
    o += '<rect x="%s" y="%s" width="%s" height="1" fill="#fff"/><rect x="%s" y="%s" width="1" height="%s" fill="#fff"/><rect x="%s" y="%s" width="%s" height="1" fill="#7E7C92"/><rect x="%s" y="%s" width="1" height="%s" fill="#7E7C92"/>' % (x, y, w, x, y, h, x, y + h - 1, w, x + w - 1, y, h)
    o += '<defs>%s</defs><rect x="%s" y="%s" width="%s" height="20" fill="url(#tb%s)"/>' % (lin('tb' + str(int(y)), [(0, tb[0]), (1, tb[1])], 0, 0, 1, 0), x + 3, y + 3, w - 6, int(y))
    o += T(title, 'vt323', 18, x + 10, y + 19, '#fff')
    for k, g in enumerate(('_', '□', '×')):
        o += '<rect x="%s" y="%s" width="16" height="14" fill="#C8C6D6"/><rect x="%s" y="%s" width="16" height="1" fill="#fff"/><rect x="%s" y="%s" width="16" height="1" fill="#6E6C82"/>' % (x + w - 60 + k * 18, y + 6, x + w - 60 + k * 18, y + 6, x + w - 60 + k * 18, y + 19) + '<path d="%s" stroke="#222" stroke-width="2" fill="none"/>' % ({'_': 'M%s %sh8', '□': 'M%s %sh8v7h-8z', '×': 'M%s %sl8 7m0 -7l-8 7'}[g] % (x + w - 56 + k * 18, y + 15 if k == 0 else y + 10))
    return o
def top_widget():
    x, y, w, h = 20, 64, 350, 148
    d = rr(x, y, w, h, 20); o = '<defs>%s<clipPath id="tw"><path d="%s"/></clipPath></defs>' % (lin('sky', [(0, '#7FA9E8'), (1, '#B5C9F4')]), d)
    o += '<path d="%s" fill="url(#sky)"/><g clip-path="url(#tw)">' % d
    o += clouds_layer(390, 200, 5, '#D8E4FB', '#C4D3F2', 4, [y + 20, y + 62, y + 96, y + 40], 5, 40)
    # waving 4-pane logo made of pixels
    for i, (c, dx, dy) in enumerate((('#FF7AA8', 0, 0), ('#7FE0C8', 24, 0), ('#FFD36B', 0, 24), ('#8FA6FF', 24, 24))):
        o += '<g transform="translate(%s,%s)"><g>%s<rect width="21" height="21" fill="%s"/><rect width="21" height="4" fill="#fff" opacity=".5"/></g></g>' % (x + 236 + dx, y + 18 + dy, AT('translate', '0 0;0 -3;0 0;0 2;0 0', '2.4s', '%ss' % (i * .3), mode='discrete', kt='0;.25;.5;.75;1'), c)
    o += T('MELVORE', 'bungee' if False else 'silkscreen-bold', 34, x + 18, y + 78, '#FFFFFF', stroke='#EE86B9', sw=4) + T('MELVORE', 'silkscreen-bold', 34, x + 18, y + 78, '#FFFFFF')
    o += T('OS 27  mobile', 'vt323', 22, x + 20, y + 98, '#fff', op=.95)
    o += '</g>'
    ty = y + h - 30; o += '<g clip-path="url(#tw)"><rect x="%s" y="%s" width="%s" height="30" fill="#E9A9D6"/><rect x="%s" y="%s" width="%s" height="2" fill="#fff"/></g>' % (x, ty, w, x, ty, w)
    o += '<rect x="%s" y="%s" width="64" height="22" fill="#F7C7E8"/><rect x="%s" y="%s" width="64" height="2" fill="#fff"/><rect x="%s" y="%s" width="64" height="2" fill="#B05A92"/>' % (x + 8, ty + 4, x + 8, ty + 4, x + 8, ty + 24) + T('Start', 'vt323', 20, x + 20, ty + 22, '#4A2250')
    for k, c in enumerate(('#FFD36B', '#8FA6FF', '#7FE0C8', '#FF7AA8')): o += '<rect x="%s" y="%s" width="16" height="16" fill="%s"/><rect x="%s" y="%s" width="16" height="3" fill="#fff" opacity=".6"/>' % (x + 86 + k * 22, ty + 7, c, x + 86 + k * 22, ty + 7)
    o += T('8:52 PM', 'vt323', 20, x + w - 18, ty + 22, '#4A2250', 'r')
    o += '<rect x="%s" y="%s" width="3" height="4" fill="#4A2250" opacity="0">%s</rect>' % (x + w - 52, ty + 12, A('opacity', '0;1;0', '1s', mode='discrete', kt='0;.5;1'))
    return o
def icon_tile(x, y, kind, label):
    s = 70; o = '<rect x="%s" y="%s" width="%s" height="%s" rx="16" fill="#fff"/><rect x="%s" y="%s" width="%s" height="%s" rx="16" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="3"/>' % (x, y, s, s, x, y, s, s)
    u = 3.4
    if kind == 'mon':
        o += pic(MON, MONP, u, x + 11, y + 12)
        o += '<rect x="%s" y="%s" width="%s" height="3" fill="#6F6AA8" opacity="0">%s</rect>' % (x + 17, y + 22, 34, A('opacity', '0;.8;0', '2.2s', mode='discrete', kt='0;.5;1')) + '<rect x="%s" y="%s" width="12" height="3" fill="#8DF0D0">%s</rect>' % (x + 18, y + 28, A('width', '4;28;4', '3s', mode='discrete', kt='0;.5;1'))
    if kind == 'hrt':
        o += '<g transform="translate(%s,%s)"><g>%s%s</g></g>' % (x + 8, y + 10, AT('translate', '0 0;0 -3;0 0', '1.4s', mode='discrete', kt='0;.5;1'), pic(HRT, HRTP, 4.2, 0, 0)) + '<g transform="translate(%s,%s)">%s</g>' % (x + 30, y + 30, pic(HRT, HRTP, 3.3, 0, 0))
    if kind == 'hgl':
        o += pic(HGL, HGLP, 4, x + 15, y + 11)
        o += '<rect x="%s" y="%s" width="8" height="8" fill="#F7A8C8"><animate attributeName="height" values="8;0;0;8" dur="4s" repeatCount="indefinite" keyTimes="0;.8;.99;1" calcMode="discrete"/><animate attributeName="y" values="%s;%s;%s;%s" dur="4s" repeatCount="indefinite" keyTimes="0;.8;.99;1" calcMode="discrete"/></rect><rect x="%s" y="%s" width="4" height="4" fill="#F7A8C8"><animate attributeName="opacity" values="1;0;1" dur=".6s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;.5;1"/></rect>' % (x + 31, y + 28, y + 28, y + 36, y + 36, y + 36, x + 33, y + 38)
    if kind == 'cd':
        rows, pal = disc(15, 15, lambda gx, gy, r, a: '#2B2540' if r > 6.5 else ('#FFFFFF' if r < 1.6 else ('#C9C6D6' if r < 2.6 else ['#FF9EC7', '#8FA6FF', '#7FE0C8', '#FFE08A', '#E6E1F5', '#FF9EC7', '#B9A8FF', '#8FE8FF'][int(((a + math.pi) / (2 * math.pi)) * 8) % 8])), 7)
        o += '<g transform="translate(%s,%s)"><g>%s<g transform="translate(-26,-26)">%s</g></g></g>' % (x + 35, y + 35, AT('rotate', '0;45;90;135;180;225;270;315;360', '2.4s', mode='discrete'), pic(rows, pal, 3.5, 0, 0).replace('', ''))
    o += T(label, 'vt323', 18, x + s / 2, y + s + 22, '#fff', 'm')
    return o
def angel_tile(x, y, s=160):
    o = '<rect x="%s" y="%s" width="%s" height="%s" rx="22" fill="#FFD3E6"/><clipPath id="at"><rect x="%s" y="%s" width="%s" height="%s" rx="22"/></clipPath><g clip-path="url(#at)">' % (x, y, s, s, x, y, s, s)
    o += clouds_layer(390, 600, 8, '#fff', '#F2E6F7', 3, [y + 110, y + 70, y + 130], 6, 30)
    o += '<g transform="translate(%s,%s)">%s</g>' % (x + s / 2, y + 80, '<g>%s%s</g>' % (AT('translate', '0 0;0 -5;0 0', '1.6s', mode='discrete', kt='0;.5;1'), pic(HEART_BIG, dict(B='#B8467A', P='#FF8CBC', W='#fff'), 9, -50, -45)))
    o += '<g transform="translate(%s,%s)"><rect x="-20" y="-72" width="40" height="5" fill="#FFE27A"/><rect x="-14" y="-77" width="28" height="5" fill="#FFE27A"/><rect x="-20" y="-72" width="40" height="2" fill="#fff"/></g>' % (x + s / 2, y + 80)
    for (px, py, d) in ((20, 28, 0), (130, 40, .5), (30, 130, 1), (136, 118, 1.5)): o += sparkle_plus(x + px, y + py, .8, '#fff', 1.6, d)
    return o + '</g>' + T('angel.exe', 'vt323', 18, x + s / 2, y + s + 22, '#fff', 'm')
def cd_player():
    x, y, w, h = 20, 470, 350, 160
    o = win_panel(x, y, w, h, 'CD Player.exe')
    # album art
    ax, ay = x + 12, y + 32
    art = '<rect x="%s" y="%s" width="84" height="84" fill="#FFB6D2"/>' % (ax, ay)
    rows, pal = grid(14, 14, lambda gx, gy: '#FFFFFF' if (gx + gy) % 5 == 0 and gx > 3 else None)
    art += '<rect x="%s" y="%s" width="84" height="40" fill="#8FA6FF"/>' % (ax, ay + 44) + '<g transform="translate(%s,%s)">%s</g>' % (ax + 22, ay + 12, '<g>%s%s</g>' % (AT('translate', '0 0;0 -4;0 0', '1.2s', mode='discrete', kt='0;.5;1'), pic(HEART_BIG, dict(B='#B8467A', P='#FF8CBC', W='#fff'), 4.2, 0, 0)))
    art += T('MELVORE', 'silkscreen-bold', 9, ax + 42, ay + 76, '#fff', 'm')
    o += art + '<rect x="%s" y="%s" width="84" height="84" fill="none" stroke="#6E6C82"/>' % (ax, ay)
    fx = ax + 96
    for k, (lab, val) in enumerate((('Artist:', 'Melvore Radio'), ('Track:', 'Neon Runway 03'))):
        yy = ay + k * 28; o += T(lab, 'vt323', 18, fx, yy + 18, '#222') + '<rect x="%s" y="%s" width="146" height="22" fill="#fff"/><rect x="%s" y="%s" width="146" height="1" fill="#6E6C82"/><rect x="%s" y="%s" width="1" height="22" fill="#6E6C82"/>' % (fx + 52, yy, fx + 52, yy, fx + 52, yy)
        o += '<clipPath id="fc%d"><rect x="%s" y="%s" width="142" height="22"/></clipPath><g clip-path="url(#fc%d)"><g>%s%s</g></g>' % (k, fx + 54, yy, k, AT('translate', '0 0;-60 0;-60 0;0 0', '8s', kt='0;.4;.7;1', mode='linear') if k else '', T(val, 'vt323', 20, fx + 58, yy + 17, '#111'))
        o += '<rect x="%s" y="%s" width="18" height="22" fill="#C8C6D6"/><rect x="%s" y="%s" width="18" height="1" fill="#fff"/>' % (fx + 182, yy, fx + 182, yy) + '<path d="M%s %sl6 7l6 -7z" fill="#222"/>' % (fx + 188, yy + 8)
    sy = ay + 66
    o += '<rect x="%s" y="%s" width="%s" height="4" fill="#fff"/><rect x="%s" y="%s" width="%s" height="1" fill="#6E6C82"/>' % (fx, sy, 200, fx, sy, 200)
    o += '<g><animateTransform attributeName="transform" type="translate" values="0 0;160 0;160 0;0 0" keyTimes="0;.9;.95;1" dur="10s" repeatCount="indefinite" calcMode="discrete"/>' + '<rect x="%s" y="%s" width="16" height="22" fill="#C8C6D6"/><rect x="%s" y="%s" width="16" height="2" fill="#fff"/><rect x="%s" y="%s" width="2" height="22" fill="#fff"/><rect x="%s" y="%s" width="16" height="2" fill="#6E6C82"/><rect x="%s" y="%s" width="2" height="22" fill="#6E6C82"/></g>' % (fx, sy - 9, fx, sy - 9, fx, sy - 9, fx, sy + 11, fx + 14, sy - 9)
    # transport buttons
    for k, g in enumerate(('◀◀', '▶▶', '▶', '■', '●')):
        bx = x + 12 + k * 66; by = y + h - 36; pr = (k == 2)
        o += '<g><rect x="%s" y="%s" width="60" height="26" fill="#C8C6D6"/><rect x="%s" y="%s" width="60" height="2" fill="#fff"/><rect x="%s" y="%s" width="2" height="26" fill="#fff"/><rect x="%s" y="%s" width="60" height="2" fill="#6E6C82"/><rect x="%s" y="%s" width="2" height="26" fill="#6E6C82"/>%s</g>' % (bx, by, bx, by, bx, by, bx, by + 24, bx + 58, by, ('<rect x="%s" y="%s" width="60" height="26" fill="#2B2540" opacity="0">%s</rect>' % (bx, by, A('opacity', '0;.18;0', '1.6s', mode='discrete', kt='0;.5;1'))) if pr else '')
        gl = {'◀◀': 'M-8 0L-1 -6V6ZM-1 0L6 -6V6Z', '▶▶': 'M-6 -6L1 0L-6 6ZM1 -6L8 0L1 6Z', '▶': 'M-4 -6L5 0L-4 6Z', '■': 'M-5 -5H5V5H-5Z', '●': 'M0 -5A5 5 0 1 1 -.01 -5Z'}[g]
        o += '<path d="%s" fill="%s" transform="translate(%s,%s)"/>' % (gl, '#E04A7E' if g == '●' else '#222', bx + 30, by + 13)
    return o
def pager_dock():
    o = ''
    for k in range(3): o += '<rect x="%s" y="686" width="8" height="8" fill="#B9A8FF" opacity=".6"/>' % (172 + k * 20)
    o += '<rect x="172" y="686" width="8" height="8" fill="#fff"><animate attributeName="x" values="172;192;212;192;172" dur="6s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;.25;.5;.75;1"/></rect>'
    d = rr(26, 716, 338, 100, 30); o += '<path d="%s" fill="#2E2468" transform="translate(0,5)" opacity=".6"/><path d="%s" fill="#3B2F7E"/><path d="%s" stroke="#fff" stroke-opacity=".12" stroke-width="2" fill="none"/>' % (d, d, d)
    apps = [('#E6C8F2', 'phone'), ('#FFFFFF', 'chat'), ('#B999E8', 'globe')]
    for k, (c, kind) in enumerate(apps):
        x = 54 + k * 100; y = 734
        o += '<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0;0 0" dur="3.6s" begin="%ss" repeatCount="indefinite" calcMode="discrete" keyTimes="0;.12;.24;1"/><rect x="%s" y="%s" width="68" height="64" rx="12" fill="%s"/><rect x="%s" y="%s" width="68" height="64" rx="12" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="2.5"/>' % (f(k * 1.2), x, y, c, x, y)
        if kind == 'phone': o += pic(['..BBBBBBBB..', '.BWWWWWWWWB.', 'BWWBBBBBBWWB', 'BBB......BBB', '....BBBB....', '...BWWWWB...', '..BWWWWWWB..', '.BWBBBBBBWB.', '.BWWWWWWWWB.', '..BBBBBBBB..'], dict(B='#6B5A86', W='#EFE4F7'), 4, x + 10, y + 12)
        if kind == 'chat': o += pic(['..BBBBBBBBBB..', '.BWWWWWWWWWWB.', 'BWWWWWWWWWWWWB', 'BWWWWWWWWWWWWB', 'BWWWWWWWWWWWWB', '.BWWWWWWWWWWB.', '..BBBWWBBBBB..', '....BWWB......', '.....BB.......'], dict(B='#6B5A86', W='#fff'), 4, x + 6, y + 14)
        if kind == 'globe':
            rows, pal = disc(14, 14, lambda gx, gy, r, a: '#5B3FB5' if r > 6.2 else ('#8FE8FF' if (gx * 7 + gy * 3) % 5 < 2 else '#B9A8FF'), 6.8); o += '<g transform="translate(%s,%s)">%s</g>' % (x + 6, y + 4, pic(rows, pal, 4, 0, 0))
        o += '</g>'
    return o
def pixel_status():
    return T('11:48', 'silkscreen-bold', 15, 22, 30, '#fff') + '<g fill="#fff"><rect x="316" y="22" width="3" height="4"/><rect x="321" y="19" width="3" height="7"/><rect x="326" y="16" width="3" height="10"/><rect x="331" y="13" width="3" height="13" opacity=".4"/><rect x="346" y="14" width="22" height="12" fill="none" stroke="#fff" stroke-width="2"/><rect x="349" y="17" width="12" height="6"/></g>'
def pixel_home():
    body = pixel_bg() + enter(pixel_status(), 0) + enter(top_widget(), 1, 'up')
    body += enter(angel_tile(20, 236), 2, 'up')
    for i, (kx, ky, kind, lab) in enumerate(((204, 236, 'mon', 'da shop*'), (292, 236, 'hrt', 'faves :)'), (204, 346, 'hgl', 'drops ok?'), (292, 346, 'cd', 'radio~'))): body += enter(icon_tile(kx - 0, ky, kind, lab) if False else icon_tile(kx - 4 if kx == 204 else kx - 8, ky, kind, lab), 3 + i, 'zoom')
    body += enter(cd_player(), 7, 'up') + enter(pager_dock(), 8, 'up')
    return svg(390, 844, body)
if __name__ == '__main__': open('t/pixel_home.svg', 'w').write(pixel_home())
