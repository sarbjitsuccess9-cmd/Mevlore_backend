import os, json, shutil
from icons import *
OUT = '/home/claude/kit/out/design-system/assets/svg/worlds_v2'
shutil.rmtree('/home/claude/kit/out', ignore_errors=True)
size = {}; man = {}
for sk in SKINS:
    d = OUT + '/' + sk.id; os.makedirs(d + '/icons', exist_ok=True); comp = {}
    for n, fn in COMPONENTS:
        s = fn(sk); open('%s/%s.svg' % (d, n), 'w').write(s); comp[n] = '/design-system/assets/svg/worlds_v2/%s/%s.svg' % (sk.id, n)
    ic = {}
    for n in ICON_NAMES:
        for ac in (False, True): open('%s/icons/%s%s.svg' % (d, n, '_active' if ac else ''), 'w').write(icon(sk, n, ac))
        ic[n] = dict(icon='/design-system/assets/svg/worlds_v2/%s/icons/%s.svg' % (sk.id, n), active_icon='/design-system/assets/svg/worlds_v2/%s/icons/%s_active.svg' % (sk.id, n))
    man[sk.id] = dict(components=comp, icons=ic)
import re
sizes = {}
for n, fn in COMPONENTS:
    m = re.search(r'viewBox="0 0 (\S+) (\S+)"', fn(SKINS[0])); sizes[n] = [float(m.group(1)), float(m.group(2))]
json.dump(dict(worlds=man, sizes=sizes), open('/home/claude/kit/out/kit_v2_index.json', 'w'), indent=1)
tot = sum(os.path.getsize(os.path.join(r, f_)) for r, _, fs in os.walk(OUT) for f_ in fs)
print('files', sum(len(fs) for _, _, fs in os.walk(OUT)), 'KB', tot // 1024, 'max', max(os.path.getsize(os.path.join(r, f_)) for r, _, fs in os.walk(OUT) for f_ in fs))
