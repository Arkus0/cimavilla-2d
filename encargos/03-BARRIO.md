# El barrio (casco histórico) · decisiones y cuestionario

**Orden acordado:** primero el ART-GATE (la microcalle del chigre). Después, el trazado del barrio: Claude lo propone y tú lo corriges. Luego un greybox jugable a escala real y, por último, el arte del barrio.

## Decisiones tomadas (14-10-2026)
| Tema | Decisión | Consecuencia práctica |
|---|---|---|
| Escala | **2–3 min** cruzarlo andando en línea recta | Unos 480–720 tiles de extensión, o 16–24 pantallas. Del orden de **350 huecos de fachada** que salen de unas 40 fachadas modulares, con variantes y volteos, más 15–20 edificios singulares |
| Continuidad | **Exterior continuo**, interiores aparte | Un solo mapa de barrio sin cargas; se entra a los interiores por la puerta |
| Fidelidad | **Ciudad ficticia** inspirada en Cimavilla | Nombres y trazado propios. El esquema de 02-MAPA.md con nombres reales queda **solo como guía de orientación** |
| Verticalidad | **Varios niveles** | Terrazas con muros de contención, escaleras, cuestas y miradores. Hace falta un tileset de muros y escaleras (E12) |
| Época | **1992** | Pesetas, cabinas, antenas de TV, coches de la época, carteles y tiendas de 1992 |
| Coches | **Aparcados y alguno circulando** | Calles principales con calzada para dos coches; sprites de coche en 4 direcciones (E13) |
| Tiempo | **Ciclo día/noche completo** | **Cada fachada necesita una capa `_luces`** con las ventanas y rótulos encendidos. Negocios con horario |
| Interiores | **Casi todo** | Propuesta: **interiores únicos** para negocios y trama, y **plantillas redecorables** para viviendas y portales (unas 6–8 plantillas) |
| Tono | **Realista, con su lado duro** | Pintadas, persianas bajadas, locales cerrados, solares, suciedad, carteles de la época… sin caricatura |
| Puerto | **Muelle, rula y barcos jugables** | Borde de agua con barcos amarrados, lonja y redes; da horizonte y escala |
| Movimiento | **Andar, correr, bici o vespino, atajos** | Escaleras sin vehículo; los atajos se descubren. La bici hace el barrio más pequeño, por eso las escaleras la frenan |
| Encuadre | **480×270** (30×17 tiles) | Se mantiene |
| Gente | **Varía con la hora** | Mañana de recados, tarde tranquila, noche de pubs; NPC con rutina y figurantes |
| Otros barrios | Centro comercial · Playa y paseo · Barrio obrero · Puerto industrial y astillero | Las salidas de este barrio apuntan hacia ellos y se ven en el horizonte |
| Microcalle del gate | **Se reutiliza** en el barrio final | El arte aprobado ya es producción |
| Orientación del jugador | **Plano en papel dentro del juego** + rótulos de calle | El trazado tiene que ser legible; el plano será también un asset |
| Pensión | **Base temporal** del jugador | Céntrica; luego se muda (¿a dónde? ver P13) |

## Cuestionario abierto
Responde debajo de cada pregunta, editando este archivo en GitHub; vale con lo que sepas. Lo que dejes en blanco lo propondré yo.

### Identidad
**P1.** ¿Cómo se llaman la ciudad ficticia y el barrio? ¿Se mantiene "Cimavilla" o va otro nombre?
> 

**P2.** Rótulos de calles y negocios: ¿castellano, asturiano o mezcla? (En 1992 lo oficial era sobre todo en castellano; los diálogos del prototipo usan asturiano.)
> 

**P3.** ¿Nombre de la calle de la microcalle y del chigre? (En el prototipo anterior era "Casa Pachu".)
> 

### Lugares (con nombre ficticio y una línea de qué es)
**P4.** Chigres y sidrerías: ¿cuántos y cuáles?
> 

**P5.** Bares y cafeterías de día:
> 

**P6.** Pubs y bares de copas de noche. ¿Hay una "zona de pubs" concreta?
> 

**P7.** Tiendas (ultramarinos, estanco, panadería, pescadería, farmacia, quiosco, peluquería, ferretería, videoclub…):
> 

**P8.** Salón recreativo o máquinas en bares. ¿Viven aquí los minijuegos del portal (Tenis de Chigre, Escanciar sidra, Costa Verde 2000, Burbujas del Muelle)? ¿Dónde?
> 

**P9.** Servicios e instituciones (iglesia, escuela, comisaría o cuartel, ambulatorio, correos, cofradía de pescadores, fábrica…):
> 

**P10.** Espacios abiertos (plazas, miradores, lavadero, bolera de bolos, jardines, el cerro). ¿Qué hay arriba del cerro?
> 

**P11.** Zonas degradadas o peligrosas (solares, casas en ruina, callejones): ¿cuáles y qué pasa en ellas?
> 

### Historia y personajes
**P12.** Lugares que **necesita la trama** (aunque sea con spoilers): escena del crimen, guaridas, casas de personajes, trabajos…
> 

**P13.** La pensión: nombre, quién la lleva, cuántas habitaciones. ¿A dónde se muda luego el jugador?
> 

**P14.** ¿Cuántos personajes con nombre viven en el barrio? ¿Cuáles tienen casa visitable?
> 

**P15.** Trabajos del jugador en el barrio (rula, chigre, reparto…): ¿cuáles y dónde?
> 

### Tiempo y vida
**P16.** ¿Cuánto dura un día en tiempo real (por ejemplo 30 min)? ¿Horarios de negocios y pubs?
> 

**P17.** Clima: ¿orbayu, lluvia, niebla, temporal? ¿Con qué frecuencia?
> 

**P18.** Fiestas o eventos que cambien el decorado (fiestas del barrio, Semana Negra, partido del equipo local…):
> 

**P19.** Coches: ¿por qué calles circulan? ¿Solo una calle principal y el muelle?
> 

**P20.** Vehículo del jugador: ¿bici o vespino? ¿Desde el principio o se consigue?
> 

### Conexiones
**P21.** ¿Por dónde se sale hacia cada barrio (centro, playa, barrio obrero, puerto industrial)? ¿A pie, en autobús…?
> 

### Producción
**P22.** Interiores "casi todo": ¿te vale la propuesta de **plantillas redecorables** para viviendas y portales, con interiores únicos solo para negocios y trama?
> 

**P23.** ¿Cuántas fachadas o assets podéis producir por semana y con qué herramienta? (Para planificar en serio.)
> 

**P24.** ¿Tienes referencias propias: fotos de Cimavilla de los 90, películas, otros juegos además de Eastward y Shenmue?
> 
