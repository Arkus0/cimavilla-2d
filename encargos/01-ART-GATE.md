# Encargos del ART-GATE

Estado: ⬜ pendiente · 📥 recibido, Claude revisando · 🔧 hay que corregir (ver nota) · ✅ integrado
**Antes de dibujar edificios, lee [02-MAPA.md](02-MAPA.md)**: solo fachadas SUR en alzado, tejados desde arriba y luz cenital.
**Hay ciclo día/noche ([03-BARRIO.md](03-BARRIO.md)):** cada fachada y cada prop con luz llevan una capa `_luces` del mismo tamaño, con ventanas, escaparates y rótulos encendidos (el resto transparente).

## 🚩 Para empezar (mínimo)
Con **E1, E2, E3 y E9** ya se puede montar y recorrer la calle con arte de verdad.

| Código | Encargo | Tamaño | Detalles | Estado |
|---|---|---|---|---|
| **E1** | **Empedrado** de Cimavilla (canto rodado gris-ocre) | Tile 16×16: 1 base + 3 variantes | Piedras de tamaños distintos, juntas oscuras y algo de musgo en una variante. Las 4 deben casar entre sí por todos los bordes | ⬜ |
| **E2** | **Acera de losa de granito + bordillo + escalones** | Tiles 16×16 | Losa (2 variantes), bordillo entre acera y calzada, y 2 escalones para las callejas norte-sur | ⬜ |
| **E3** | **Fachada SUR con galería acristalada blanca** | **112×176** (PB+2, incluido el alero) | Alzado puro, sin laterales ni perspectiva. Revoco pastel, sillería en las esquinas, galería de madera blanca con cristales, puerta de madera. Se usará también **volteada**, así que nada de rótulos ni luz lateral marcada. **+ capa `_luces`** | ⬜ |
| **E9** | **Tileset de tejado de teja árabe** visto desde arriba | Tiles 16×16 | Campo (3 variantes), cumbrera, alero norte con canalón (el que tapa la acera), unión con la cornisa de la fachada, canto de calleja (oeste; el este sale volteado) y 4 esquinas | ⬜ |

## Siguiente tanda
| Código | Encargo | Tamaño | Detalles | Estado |
|---|---|---|---|---|
| **E4** | **Fachada SUR del chigre** | 112×176 | Planta baja con puerta legible y escaparate con luz cálida. **Rótulo en capa aparte** (nombre a elegir) y pizarra "Hai sidra". **+ capa `_luces`** con el escaparate y el rótulo encendidos | ⬜ |
| **E5** | **Props del chigre** | 16–32 px cada uno | Cajas de sidra con botellas verdes, pipa o barrica, banco o taburete, **farol de pared `_off` y `_on`** | ⬜ |
| **E8** | **Casa B** (PB+1) y **casa estrecha** (PB+2) | 96×128 y 64×176 | Otro color de revoco y balcón de forja; también se voltean | ⬜ |
| **E6** | Detalles de suelo | 16×16 | Tapa de alcantarilla y charco | ⬜ |
| **E7** | Props marineros | 16–32 px | Nasas, boyas, redes, maceta con hortensias, bolardo | ⬜ |
| **E10** | Personaje de escala | Frames de 24×32 | Idle + caminar en 4 direcciones (abajo, izquierda, derecha, arriba) | ⬜ |
| **E11** | Props de tejado | 16–32 px | Chimenea, antena de TV, claraboya, gato | ⬜ |

## Para el barrio (después del ART-GATE; no empezar todavía)
| Código | Encargo | Notas |
|---|---|---|
| E12 | Tileset de **muros de contención y escaleras** entre niveles | Muro visto de frente (cara sur), remates y escaleras norte-sur |
| E13 | **Coches de 1992** en 4 direcciones | Aparcados y circulando |
| E14 | **Plano del barrio en papel** (objeto del juego) | Cuando el trazado esté aprobado |
| E15 | Plantillas de **interiores** | Viviendas y portales redecorables; los únicos, según la trama |

## Notas de revisión de Claude
_(aquí apunto lo que haya que corregir de cada entrega)_
