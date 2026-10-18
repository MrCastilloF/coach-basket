# Coach Gloria Celis — Landing Page

Prototipo navegable de la landing page para una coach de básquetbol de alto rendimiento.
Concepto: **“El juego se gana antes del salto inicial.”**
Dirección de arte: *vestuario oscuro, luz de cancha* — carbón + naranja balón + oro trofeo.

---

## Cómo verlo

```bash
# desde la carpeta coach-basket
python -m http.server 8899
# abrir http://127.0.0.1:8899/index.html
```

No requiere build ni dependencias: HTML + CSS + JS vanilla, fuentes autoalojadas (OFL) y fotos locales.
También funciona abriendo `index.html` directamente, aunque un servidor local garantiza la carga de fuentes.

---

## Estructura

```
coach-basket/
├─ index.html                  Landing completa (una sola página, anclas)
├─ assets/
│  ├─ css/styles.css           Sistema de diseño + responsive + motion
│  ├─ js/main.js               Header, menú, reveals, contadores, formulario
│  ├─ fonts/                   Barlow Condensed (500–800) e Inter (400–700), woff2
│  └─ img/                     Recortes de las fotos originales del cliente
├─ docs/
│  ├─ Propuesta_Landing_Coach_Basketball.docx
│  └─ Propuesta_Landing_Coach_Basketball.pdf
├─ preview/                    Capturas desktop / tablet / móvil + lámina showcase
└─ tools/                      Scripts de preparación y QA (Playwright + Pillow)
```

## Secciones

| # | Sección | Objetivo |
|---|---|---|
| — | Hero | Promesa + prueba + CTA en el primer viewport |
| 01 | Palmarés | Autoridad verificable: contadores, timeline, credenciales, impacto |
| 02 | Filosofía | Diferenciación: “no entreno cuerpos, entreno criterio” |
| 03 | Método 360 | Proceso en 4 fases + pizarra táctica isométrica |
| 04 | Programas | Clínica grupal, asesoría 1:1, dirección técnica |
| 05 | Galería | Evidencia real (blanco y negro → color al hover) |
| 06 | Testimonios | Prueba social cualitativa |
| 07 | Contacto | Formulario corto + agenda directa + FAQ |

## Sistema de diseño

- **Color:** carbón `#0A0B0D`, superficie `#111317`, crema `#F4F1E9`, naranja `#FF4D1F`, oro `#E9B44C`.
  Regla: naranja solo para acción, oro solo para logro.
- **Tipografía:** Barlow Condensed 700–800 para display (mayúsculas, tracking negativo),
  Inter 400–600 para lectura. Escala fluida con `clamp()`.
- **Grid:** 12 columnas, `max-width: 1240px`, gutter fluido, secciones con 76–132 px de aire.
- **Componentes:** botones rectos (radio 2 px), tarjetas con borde de 1 px, chips tipo píldora,
  pizarra 3D en CSS, marquesina, acordeón nativo `<details>`.

## Accesibilidad y performance

- HTML semántico, landmarks, `aria-expanded` / `aria-controls` en el menú, `aria-live` en el formulario.
- Contraste AA, `:focus-visible` visible, `prefers-reduced-motion` respetado.
- Imágenes con `width`/`height`, lazy loading salvo el hero (`fetchpriority="high"`),
  fuentes con `preload` y `display: swap`.

## Datos a reemplazar antes de publicar

1. **Nombre de marca** — “Gloria Celis” es el nombre real de la coach (ya aplicado en todo el proyecto).
   Si vuelve a cambiar, buscarlo en `<title>`, header, footer, JSON-LD y copy.
2. **Contacto** — `lorisisabel22@gmail.com` y `+57 298 5298` (ya aplicados en contacto y footer, con enlaces
   `mailto:` y `tel:`). El botón flotante y el de «Agenda directa» llaman al teléfono; si más adelante hay un
   número con WhatsApp, basta cambiar esos dos `tel:` por `https://wa.me/<numero>`.
3. **Credenciales y palmarés** — cifras, años y clubes son demostrativos; sustituir por los reales.
4. **Fotos** — las imágenes provienen de los archivos entregados por el cliente; el hero es 471 × 1024 px,
   conviene un original a mayor resolución para pantallas retina.
5. **Testimonios** — textos de ejemplo; reemplazar por citas autorizadas por escrito.
6. **Dominio / OG image** — `og:image` apunta a `assets/img/coach-hero.jpg`; ajustar a una imagen 1200 × 630.

## QA ejecutado

- `tools/shot.py` — capturas desktop 1440, tablet 834 y móvil 390 (full page + por sección).
- `tools/test.py` — 13 pruebas funcionales (validación de formulario, menú móvil, acordeón, anclas, sticky header): **13/13**.
- Sin desbordes horizontales en 1440, 834 y 390 px; sin errores de consola salvo el favicon (ya resuelto).

## Dirección de arte 3D (para producción)

El prototipo resuelve el 3D con CSS/SVG. Para producción se recomienda renderizar tres piezas
(balón, pizarra táctica isométrica y trofeo) en Blender o Spline y sustituirlas como PNG con alfa
o WebP < 300 KB. Especificación completa en el documento de propuesta, sección de dirección de arte.
