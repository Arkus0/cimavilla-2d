# Cimavilla 1992 — prototipo 2D (Phaser 4)

Plazuela de Cimavilla (Xixón) en 1992, vista cenital. Todo el arte se genera por código (`art/gen.py`, Python/PIL) con una paleta cerrada de 32 colores cálidos y apagados, tiles de 16 px.

**Jugar:** https://arkus0.github.io/cimavilla-2d/

- WASD / flechas: andar · E / Espacio: hablar · sube por la puerta del chigre para entrar, baja por la puerta para salir.

## Build
```
pip install pillow && ./build.sh   # genera art/out/*.png y dist/ (assets embebidos en base64)
```
Phaser 4.2.1 se carga desde jsDelivr.

## v2
- `art/gen2.py`: arte v2 (paleta cerrada de 40 colores, cuantizada sin dithering), capa de suelo + capa de primer plano, sprites 24×32, objetos cotidianos (máquina de refrescos, bici, bombona de butano, cajas de pescado, hortensias, carteles, cables, ropa tendida).
- `art/mockup.py`: render fijo «target mockup».
