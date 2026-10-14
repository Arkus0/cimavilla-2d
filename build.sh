#!/bin/sh
set -e; cd "$(dirname "$0")"
python3 art/gen.py
python3 - <<'PY'
import base64,glob,json,os
a={os.path.basename(f)[:-4]:'data:image/png;base64,'+base64.b64encode(open(f,'rb').read()).decode() for f in glob.glob('art/out/*.png')}
open('dist/assets.js','w').write('window.ASSETS='+json.dumps(a)+';\nwindow.META='+open('art/out/meta.json').read()+';\n')
PY
cp src/index.html src/game.js dist/
