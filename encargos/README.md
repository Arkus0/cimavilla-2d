# Encargos de arte · ART-GATE estilo Eastward

Este repo es el **buzón de entregas**. Claude deja aquí los encargos y la especificación. Tú subes los PNG a `entregas/` y Claude los integra en la escena de prueba (`minijuegos-cimavilla`, rama `ccr-324be5cd-py8gxv`, carpeta `prototypes/poc-2d-eastward-00/`).

- Lista de encargos y estado: **[01-ART-GATE.md](01-ART-GATE.md)**
- Lema de todo prompt de imagen: **«Shenmue asturiano con el nivel gráfico de Eastward»**

## Cómo entregar
1. Sube cada PNG a la subcarpeta que toque: `entregas/suelo/`, `entregas/fachadas/`, `entregas/props/` o `entregas/personajes/`.
2. Nómbralo con el código del encargo: `E1_empedrado.png`, `E3_fachada_galeria.png`…
3. Añade una línea a `entregas/ORIGEN.md`: herramienta o autor, licencia, prompt si es IA y factor de escala si viene ampliado.
4. Haz commit. Claude vigila el repo y avisa de lo que falta o hay que corregir.

## Especificación técnica (resumen)
| Tema | Regla |
|---|---|
| Rejilla | Tile de **16×16 px** |
| Resolución del juego | 480×270, escalado entero (×2, ×3, ×4) |
| Personaje de referencia | Frame de **24×32**, figura de 28–30 px de alto, ancla en los pies |
| Escala de edificios | Planta ≈ 48–56 px de alto · puerta ≈ 20–24 × 32–36 px · ventana ≈ 12–16 × 18–24 px |
| Proyección | **3/4 frontal**: suelo visto desde arriba y fachadas de frente, paralelas a la pantalla. **Sin puntos de fuga ni perspectiva cónica**. Tejados y aleros escorzados, vistos un poco desde arriba |
| Luz | **Desde arriba a la izquierda**. Sombras hacia abajo a la derecha, mejor en capa aparte |
| Formato | **PNG con transparencia**. 1 píxel de arte = 1 píxel de imagen; si viene ampliado, indica el factor en ORIGEN.md |
| Bordes | Duros (alfa 0 o 255), sin antialias ni halos. **Nada de JPG ni WebP** |
| Paleta | Cerrada y compartida: unos 64 colores para toda la escena. Si no, Claude cuantiza |
| Fachadas | Si se puede, **por capas** del mismo tamaño: `_base` (pared, zócalo, sillería), `_huecos` (ventanas, galería, puerta), `_alero` (tejado, tapa al jugador), `_rotulo`. Si no, un PNG completo y Claude lo recorta. Ancho en múltiplos de 16 px |
| Suelo | Tiles de 16×16 que **se repiten sin costura** (en mosaico 3×3 no se ve la junta). Mejor en una hoja sin márgenes ni separación |
| Props | Uno por PNG, recortado, fondo transparente, ancla en el centro de la base. Si dan luz, dos versiones: `_off` y `_on` |
| Procedencia | **Obligatoria**. Nada extraído, calcado ni retocado de Eastward, Alundra, SEGA ni otros juegos comerciales |
