# Coach Gloria Celis — Landing Page

Landing page de una sola página para una entrenadora de básquetbol de alto rendimiento.
Concepto: **“El juego se gana antes del salto inicial.”**

**Sitio en vivo:** https://mrcastillof.github.io/coach-basket/

---

## Stack

HTML5 + CSS3 + JavaScript vanilla, sin build ni dependencias.
Fuentes autoalojadas (Barlow Condensed + Inter, licencia OFL) y fotografías locales.

## Estructura

```
.
├─ index.html                 Landing completa
├─ assets/
│  ├─ css/styles.css          Sistema de diseño, responsive y motion
│  ├─ js/main.js              Header, menú, contadores, formulario
│  ├─ fonts/                  woff2 (OFL)
│  └─ img/                    Fotografías del proyecto
├─ docs/                      Propuesta de diseño (PDF + DOCX)
└─ preview/                   Capturas del resultado
```

## Secciones

Hero · Palmarés · Filosofía · Método 360 · Programas · Galería · Testimonios · Contacto + FAQ

## Ver en local

```bash
git clone https://github.com/MrCastilloF/coach-basket.git
cd coach-basket
python -m http.server 8899
# http://127.0.0.1:8899/
```

> Ábrelo con un servidor local: las fuentes `.woff2` no cargan con `file://` por política CORS.

## Datos de demostración

El nombre **Gloria Celis** es real; el palmarés, los testimonios, el teléfono y el correo son
datos de ejemplo hasta que la coach entregue los definitivos.
Puntos a reemplazar: `index.html` (`<title>`, header, footer, JSON-LD), enlaces `wa.me`,
correo `hola@gloriacelis.co` y los textos de la sección de testimonios.

## Publicación

GitHub Pages, rama `main`, carpeta raíz (`/`). El archivo `.nojekyll` evita el procesamiento
de Jekyll y sirve los archivos tal cual.
