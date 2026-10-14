import sys,time
from playwright.sync_api import sync_playwright
url=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else 'shots'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); errs=[]
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None); pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto(url); time.sleep(3)
    print('phaser',pg.evaluate('Phaser.VERSION'),'renderer',pg.evaluate('game.renderer.type'))
    pg.screenshot(path=f'{out}/v2_01_plaza.png')
    def hold(k,s): pg.keyboard.down(k); time.sleep(s); pg.keyboard.up(k)
    hold('ArrowLeft',1.0); hold('ArrowDown',0.9); time.sleep(.2); pg.screenshot(path=f'{out}/v2_02_paseo.png')
    pg.evaluate("game.scene.getScene('plaza').player.setPosition(196,226)"); hold('ArrowLeft',0.15); pg.keyboard.press('e'); time.sleep(.3); pg.screenshot(path=f'{out}/v2_03_dialogo_guela.png')
    for _ in range(3): pg.keyboard.press('e'); time.sleep(.1)
    pg.evaluate("(()=>{const p=game.scene.getScene('plaza').player;p.setPosition(240,160)})()"); time.sleep(.3); pg.screenshot(path=f'{out}/v2_04_puerta_chigre.png'); hold('ArrowUp',1.2); time.sleep(1)
    pg.screenshot(path=f'{out}/v2_05_chigre_interior.png')
    pg.evaluate("game.scene.getScene('chigre').player.setPosition(168,100)"); hold('ArrowUp',0.3); pg.keyboard.press('Space'); time.sleep(.3)
    pg.screenshot(path=f'{out}/v2_06_dialogo_chigrero.png')
    print('scene',pg.evaluate('game.scene.getScenes(true).map(s=>s.scene.key)'),'errors',errs)
    b.close()
