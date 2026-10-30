# Team SKY — Landing page

Sitio de una página para **Gloria Isabel Celis Suárez**, coach de baloncesto del **Team SKY**
(Bogotá, Colombia).

**Concepto:** *“SKY no es un nombre. Es una forma de jugar.”*
**En vivo:** https://mrcastillof.github.io/coach-basket/

---

## Qué incluye

- **Hero** con el nombre completo, Team SKY y acceso al film.
- **Film de 25 s** montado con 11 fotos reales del equipo (Ken Burns + fundidos) y cama
  sonora original, en reproductor propio.
- **Sección Team SKY**, palmarés con contadores, filosofía, método 360, programas, galería,
  testimonios y agenda.
- Diseño responsive, accesible y sin dependencias (HTML + CSS + JS vanilla).

## Estructura

```
.
├─ index.html
├─ PROPUESTA.md              Documento de diseño, copy y especificación del film
├─ assets/
│  ├─ css/styles.css         Sistema de diseño y responsive
│  ├─ js/main.js             Menú, reveals, contadores, formulario y reproductor
│  ├─ img/                   Fotos recortadas y optimizadas
│  ├─ video/                 sky-film.mp4 + póster
│  └─ fonts/                 Barlow Condensed + Inter (woff2, OFL)
└─ .nojekyll                 Sirve los archivos tal cual en GitHub Pages
```

## Ver en local

```bash
git clone https://github.com/MrCastilloF/coach-basket.git
cd coach-basket
python -m http.server 8896
# http://127.0.0.1:8896/
```

> Usa un servidor local: las fuentes `.woff2` no cargan con `file://`.

## El film

| Dato | Valor |
|---|---|
| Archivo | `assets/video/sky-film.mp4` |
| Formato | 4:5 · 960 × 1200 · H.264 · 30 fps |
| Duración | 25 s (loop) |
| Peso | ≈ 6 MB (se descarga solo al pulsar play) |
| Póster | `assets/video/sky-film-poster.jpg` |
| Audio | Cama sonora original provisional |

Las fotos venían como capturas de Facebook (720 × 1600 con interfaz). Se aisló la foto real de
cada captura, se recortó a 4:5 y se corrigió color antes del montaje. Si llega una pista
musical licenciada, se reemplaza el audio sin recomprimir el video.

## Datos de demostración

El nombre y el equipo son reales; **el palmarés, los testimonios, las cifras y los enlaces
sociales son demostrativos**. Están señalados en `PROPUESTA.md` (sección 9) para sustituirlos
por la información validada por la coach.
