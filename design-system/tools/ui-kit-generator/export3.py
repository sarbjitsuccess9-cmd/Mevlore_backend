import os, json, shutil, re
from lay_gen3 import *
import lay_goth as LG, lay_pixel as LP
OUT = '/home/claude/kit/out3/design-system/assets/svg/worlds_v3'
shutil.rmtree('/home/claude/kit/out3', ignore_errors=True)
def W_(w, h, content, defs='', tx=0, ty=0): return svg(w, h, '<g transform="translate(%s,%s)">%s</g>' % (tx, ty, content), DEFS + defs)
def generic_widgets(sk):
    th = TH[sk.id]; P = sk.P; out = {}
    out['bg_ambient'] = (390, 844, bgsoft(sk, 0) if sk.id not in ('goth', 'pixel') else (goth_bg() if sk.id == 'goth' else pixel_bg()), '')
    out['status_bar'] = (390, 44, status(P['ink'], 'inter'), '')
    d, b = topbar(sk, th); out['topbar'] = (390, 60, b, d, 0, -44)
    sd, sb = sk.body(350, 48, 'ghost', 'sb'); out['search'] = (350, 48, sb + '<g transform="translate(24,24)"><circle cx="-1" cy="-1" r="6" stroke="%s" stroke-width="2"/><path d="M3.5 3.5L8 8" stroke="%s" stroke-width="2" stroke-linecap="round"/></g><rect x="52" y="20" width="0" height="8" rx="4" fill="%s" opacity=".5">%s</rect>' % (P['acc'], P['acc'], P['ink2'], A('width', '0;0;150;150;0', '6s', kt='0;.1;.6;.9;1')), sd)
    d, c = chips_row(sk, th, 0); out['chips_row'] = (440, 36, c, d)
    d, c = banner(sk, th, 0); out['banner'] = (350, 118, c, d, -20, 0)
    out['section_header'] = (390, 30, section(sk, th, 'New in', 20), '')
    d, c = prod_card(sk, th, 0, 0, 0); out['product_card'] = (168, 214, c, d)
    d, c = coupon(sk, th, 0); out['coupon'] = (350, 62, c, d, -20, 0)
    out['order_steps'] = (390, 60, stepper_steps(sk, th, 20), '')
    d, c = cta(sk, th, 0); out['cta_add_to_bag'] = (350, 58, c, d, -20, 0)
    d, c = nav_inner(sk, th, 0); out['nav_live'] = (358, 64, c, d, -16, 0)
    out['hero_art'] = (390, 380, hero_art(sk) if sk.id not in ('goth', 'pixel') else '', '')
    if sk.id not in ('goth', 'pixel'):
        out['title_block'] = (390, 170, title_block(sk, th), '', 0, -376)
        d, c = date_strip(sk, th); out['date_strip'] = (390, 80, c, d, 0, -527)
        d, c = player(sk, th, 0); out['player'] = (350, 80, c, d, -20, 0)
        d, ts = tiles(sk, th)
        for n, t in zip(('tile_bag', 'tile_wishlist', 'tile_discover', 'tile_alerts'), ts): out[n] = (164, 64, t, d, -(20 + (ts.index(t) % 2) * 186), -(688 + (ts.index(t) // 2) * 76))
    if sk.id == 'goth':
        out['hero_art'] = (390, 400, LG.goth_hero(), '', 0, 0); out['title_block'] = (390, 170, LG.goth_titles(), '', 0, -376); out['date_strip'] = (390, 80, LG.goth_dates(), '', 0, -525); out['player'] = (350, 80, LG.goth_player(), '', -20, -590)
        d, ts = LG.goth_tiles(); dg = '<linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E11D48" stop-opacity=".25"/><stop offset=".5" stop-color="#E11D48" stop-opacity="0"/></linearGradient>'
        for k, (n, t) in enumerate(zip(('tile_bag', 'tile_wishlist', 'tile_discover', 'tile_alerts'), ts)): out[n] = (164, 64, t, dg, -(20 + (k % 2) * 186), -(686 + (k // 2) * 74))
    if sk.id == 'pixel':
        out['os_window'] = (350, 148, LP.top_widget(), '', -20, -64); out['angel_tile'] = (160, 190, LP.angel_tile(20, 236), '', -20, -236)
        for k, (kind, lab) in enumerate((('mon', 'da shop*'), ('hrt', 'faves :)'), ('hgl', 'drops ok?'), ('cd', 'radio~'))): out['icon_tile_' + kind] = (80, 100, LP.icon_tile(5, 0, kind, lab), '')
        out['cd_player'] = (356, 166, LP.cd_player(), '', -17, -467); out['dock'] = (338, 120, LP.pager_dock(), '', -26, -690)
        out['title_block'] = (390, 170, T('LEVEL 27', 'silkscreen-bold', 14, 34, 30, '#fff') + T('SUNDAY', 'silkscreen-bold', 48, 30, 100, '#fff', stroke='#EE86B9', sw=5) + T('SUNDAY', 'silkscreen-bold', 48, 30, 100, '#fff') + T('start >', 'vt323', 40, 30, 150, '#E9E0FF'), '')
    return out
def screens(sk):
    s = {'shop': shop_screen(sk), 'product': product_screen(sk), 'bag': bag_screen(sk)}
    s['home'] = LG.goth_home() if sk.id == 'goth' else LP.pixel_home() if sk.id == 'pixel' else home(sk)
    return s
idx = {}; sizes = {}
for sk in SKINS:
    d = OUT + '/' + sk.id; os.makedirs(d + '/layouts', exist_ok=True); os.makedirs(d + '/widgets', exist_ok=True); L = {}; Wd = {}
    for n, s in screens(sk).items(): open('%s/layouts/%s.svg' % (d, n), 'w').write(s); L[n] = '/design-system/assets/svg/worlds_v3/%s/layouts/%s.svg' % (sk.id, n)
    for n, v in generic_widgets(sk).items():
        w, h, c, df = v[:4]; tx, ty = (v[4], v[5]) if len(v) > 4 else (0, 0)
        open('%s/widgets/%s.svg' % (d, n), 'w').write(W_(w, h, c, df, tx, ty)); Wd[n] = '/design-system/assets/svg/worlds_v3/%s/widgets/%s.svg' % (sk.id, n); sizes.setdefault(n, [w, h])
    idx[sk.id] = dict(layouts=L, widgets=Wd)
    print(sk.id, len(L), len(Wd))
json.dump(dict(worlds=idx, sizes=sizes, layout_size=[390, 844]), open('/home/claude/kit/out3/kit_v3_index.json', 'w'), indent=1)
tot = [os.path.getsize(os.path.join(r, f_)) for r, _, fs in os.walk(OUT) for f_ in fs]
print('files', len(tot), 'KB', sum(tot) // 1024, 'max KB', max(tot) // 1024)
