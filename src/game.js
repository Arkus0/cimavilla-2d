// Cimavilla 1992 — prototype (Phaser 4)
const A = window.ASSETS, META = window.META;
const VW = 320, VH = 180;
const DIALOG = document.getElementById('dialog');
let dlg = null; // {lines, i, name}
function showLine() { DIALOG.style.display = 'block'; DIALOG.innerHTML = `<b>${dlg.name}</b><br>${dlg.lines[dlg.i]}<span class="nx">▼</span>`; }
function startDialog(name, lines) { dlg = { name, lines, i: 0 }; showLine(); }
function advance() { dlg.i++; if (dlg.i >= dlg.lines.length) { dlg = null; DIALOG.style.display = 'none'; } else showLine(); }

const NPCS = {
  guela: ['Ai, fíu, ¿tú de quién yes? Que nun te conozo.', 'Esto antes yera tou de pescadores. Agora namás quedamos los vieyos y los gatos.', 'Ten cuidáu cola sidra, que sube más rápido que la marea.'],
  pescador: ['Güei la mar taba mala, nin un bonitu pa remediar.', 'En El Muelle dicen que van facer no sé qué pa la Expo... ¡Ho, a mí qué me cuenten!', 'Si vas al chigre dí-y a Pachu que-y debo dos culinos. Mañana-y pago.'],
  neno: ['¿Viste el partíu? ¡El Sporting ganó-y al Oviedo, ho!', 'Toi esperando a mio güela, que ta faciendo la compra en la plaza.', 'Dicen que en la Atalaya hai un cañón de cuando los ingleses. ¡Yo nun lu vi!'],
  chigrero: ['¡Bienveníu a Casa Pachu! ¿Qué va ser, una botella?', 'Echada bien alta, que la sidra tien que respirar. Si non, nun espalma.', 'Esto ye de Villaviciosa, de llagar bueno. Nada de gaseosa, ¿eh?', 'Y el culín, d\'un trago. Lo que quede, pal suelu, que ye costumbre.'],
};

class Boot extends Phaser.Scene {
  constructor() { super('boot'); }
  preload() {
    for (const k of ['plaza', 'interior', 'lamp', 'bench', 'barrel', 'crate', 'pot', 'glow', 'vignette', 'tree', 'table'])
      this.load.image(k, A[k]);
    for (const k of ['player', 'guela', 'pescador', 'chigrero', 'neno'])
      this.load.spritesheet(k, A[k], { frameWidth: 16, frameHeight: 24 });
  }
  create() {
    const dirs = ['down', 'left', 'right', 'up'];
    for (const k of ['player', 'guela', 'pescador', 'chigrero', 'neno'])
      dirs.forEach((d, r) => {
        this.anims.create({ key: `${k}-walk-${d}`, frames: this.anims.generateFrameNumbers(k, { frames: [r * 4, r * 4 + 1, r * 4 + 2, r * 4 + 3] }), frameRate: 8, repeat: -1 });
        this.anims.create({ key: `${k}-idle-${d}`, frames: this.anims.generateFrameNumbers(k, { frames: [r * 4, r * 4, r * 4 + 2, r * 4 + 2] }), frameRate: 1.5, repeat: -1 });
      });
    this.scene.start('plaza', { x: 240, y: 150, dir: 'down' });
  }
}

class Base extends Phaser.Scene {
  makePlayer(x, y, dir) {
    this.player = this.physics.add.sprite(x, y, 'player', 0).setOrigin(0.5, 1);
    this.player.body.setSize(10, 6).setOffset(3, 18);
    this.player.dir = dir; this.player.play(`player-idle-${dir}`);
    this.keys = this.input.keyboard.addKeys('W,A,S,D,UP,DOWN,LEFT,RIGHT,E,SPACE');
    this.input.keyboard.on('keydown-E', () => this.interact());
    this.input.keyboard.on('keydown-SPACE', () => this.interact());
    this.npcs = [];
    this.solids = this.physics.add.staticGroup();
  }
  wall(x, y, w, h) { const r = this.add.zone(x + w / 2, y + h / 2, w, h); this.physics.add.existing(r, true); this.solids.add(r); }
  prop(key, x, y, bw, bh) { const s = this.add.image(x, y, key).setOrigin(0.5, 1); s.setDepth(y); if (bw) this.wall(x - bw / 2, y - bh, bw, bh); return s; }
  npc(key, x, y, dir) {
    const n = this.physics.add.staticSprite(x, y, key, 0).setOrigin(0.5, 1); n.key = key; n.home = dir;
    n.body.setSize(12, 6).setOffset(2, 18); n.refreshBody?.(); n.body.reset(x, y - 3);
    n.play(`${key}-idle-${dir}`); n.setDepth(y); this.npcs.push(n); this.solids.add(n);
    return n;
  }
  interact() {
    if (!this.sys.isActive()) return;
    if (dlg) return advance();
    const p = this.player; let best = null, bd = 42;
    for (const n of this.npcs) { const d = Phaser.Math.Distance.Between(p.x, p.y, n.x, n.y); if (d < bd) { bd = d; best = n; } }
    if (best) {
      const dx = p.x - best.x, dy = p.y - best.y;
      const f = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 'right' : 'left') : (dy > 0 ? 'down' : 'up');
      best.play(`${best.key}-idle-${f}`);
      const names = { guela: 'Güela Maruja', pescador: 'Celestino, pescador', neno: 'Nel, el neñu', chigrero: 'Pachu, el chigreru' };
      startDialog(names[best.key], NPCS[best.key]);
      this.talking = best;
    }
  }
  lighting(lights, tint, alpha) {
    this.add.rectangle(0, 0, VW, VH, tint, alpha).setOrigin(0).setScrollFactor(0).setDepth(9000).setBlendMode(Phaser.BlendModes.MULTIPLY);
    for (const [x, y, s, a] of lights) this.add.image(x, y, 'glow').setScale(s).setAlpha(a).setDepth(9001).setBlendMode(Phaser.BlendModes.ADD);
    this.add.image(0, 0, 'vignette').setOrigin(0).setScrollFactor(0).setDepth(9002);
  }
  update() {
    const p = this.player, k = this.keys; let vx = 0, vy = 0;
    if (!dlg) {
      if (this.talking) { this.talking.play(`${this.talking.key}-idle-${this.talking.home}`); this.talking = null; }
      if (k.LEFT.isDown || k.A.isDown) vx = -1; else if (k.RIGHT.isDown || k.D.isDown) vx = 1;
      if (k.UP.isDown || k.W.isDown) vy = -1; else if (k.DOWN.isDown || k.S.isDown) vy = 1;
    }
    const sp = 60, n = vx && vy ? 0.7071 : 1;
    p.setVelocity(vx * sp * n, vy * sp * n);
    if (vx || vy) {
      p.dir = vx ? (vx < 0 ? 'left' : 'right') : (vy < 0 ? 'up' : 'down');
      p.anims.play(`player-walk-${p.dir}`, true);
    } else p.anims.play(`player-idle-${p.dir}`, true);
    p.setDepth(p.y);
    this.tick?.();
  }
}

class Plaza extends Base {
  constructor() { super('plaza'); }
  create(data) {
    this.physics.world.setBounds(0, 0, 480, 352);
    this.add.image(0, 0, 'plaza').setOrigin(0).setDepth(-10);
    this.makePlayer(data.x, data.y, data.dir);
    this.wall(0, 0, 480, 128); this.wall(0, 128, 44, 180); this.wall(436, 128, 44, 180); this.wall(0, 298, 480, 54);
    this.prop('lamp', 120, 150, 6, 4); this.prop('lamp', 360, 150, 6, 4); this.prop('lamp', 240, 290, 6, 4);
    this.prop('bench', 150, 222, 30, 8); this.prop('bench', 330, 296, 30, 8);
    this.prop('barrel', 196, 140, 12, 6); this.prop('barrel', 210, 136, 12, 6); this.prop('barrel', 290, 140, 12, 6);
    this.prop('crate', 274, 140, 14, 6);
    this.prop('pot', 108, 134); this.prop('pot', 330, 134); this.prop('pot', 344, 134); this.prop('pot', 56, 134);
    this.prop('tree', 240, 214, 6, 5).setDepth(214);
    this.npc('guela', 170, 222, 'down').setDepth(223);
    this.npc('pescador', 380, 288, 'left');
    this.npc('neno', 96, 190, 'right');
    const cam = this.cameras.main; cam.setBounds(0, 0, 480, 352); cam.startFollow(this.player, true, 0.15, 0.15); cam.roundPixels = true;
    this.physics.add.collider(this.player, this.solids);
    this.player.setCollideWorldBounds(true);
    const L = [[120, 132, 1.0, 0.55], [360, 132, 1.0, 0.55], [240, 272, 1.0, 0.55], ...META.glows.map(([x, y]) => [x, y + 6, 0.6, 0.35])];
    this.lighting(L, 0xd8a890, 1);
    this.cameras.main.fadeIn(400, 26, 20, 24);
  }
  tick() { const p = this.player; if (!this.leaving && p.y < 136 && p.x > 232 && p.x < 248 && p.dir === 'up' && this.keys.UP.isDown + this.keys.W.isDown) { this.leaving = 1; this.cameras.main.fadeOut(300, 26, 20, 24); this.time.delayedCall(320, () => this.scene.start('chigre')); } }
}

class Chigre extends Base {
  constructor() { super('chigre'); }
  create() {
    this.physics.world.setBounds(0, 40, 256, 136);
    this.add.image(0, 0, 'interior').setOrigin(0).setDepth(-10);
    this.makePlayer(128, 168, 'up');
    this.wall(0, 0, 256, 52); this.wall(104, 60, 136, 34);
    this.npc('chigrero', 170, 66, 'down').setDepth(60);
    for (const [x, y] of [[20, 70], [20, 92], [40, 70]]) this.prop('barrel', x, y, 12, 6);
    this.prop('table', 50, 140, 22, 8); this.prop('table', 200, 150, 22, 8); this.prop('crate', 238, 120, 14, 6);
    this.npc('pescador', 76, 142, 'left');
    this.physics.add.collider(this.player, this.solids);
    this.player.setCollideWorldBounds(true);
    const cam = this.cameras.main; cam.centerOn(128, 88);
    this.lighting([[60, 40, 1.4, 0.4], [180, 50, 1.6, 0.45], [128, 130, 1.4, 0.25]], 0xd8b098, 1);
    this.cameras.main.fadeIn(300, 26, 20, 24);
  }
  tick() { const p = this.player; if (!this.leaving && p.y > 173 && p.x > 112 && p.x < 144) { this.leaving = 1; this.cameras.main.fadeOut(300, 26, 20, 24); this.time.delayedCall(320, () => this.scene.start('plaza', { x: 240, y: 146, dir: 'down' })); } }
}

window.game = new Phaser.Game({
  type: Phaser.AUTO, parent: 'game', width: VW, height: VH, pixelArt: true, roundPixels: true, backgroundColor: '#1a1418',
  physics: { default: 'arcade', arcade: { debug: false } },
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
  scene: [Boot, Plaza, Chigre],
});
