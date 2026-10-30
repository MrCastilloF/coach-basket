# Propuesta — Landing “Team SKY”

**Cliente:** Gloria Isabel Celis Suárez — Coach de Baloncesto
**Equipo:** Team SKY
**Concepto:** *“SKY no es un nombre. Es una forma de jugar.”*
**Versión:** 2.0 · Octubre 2026

---

## 1. Concepto creativo

La marca personal no se construye con adjetivos: se construye con **evidencia y carácter**.
SKY da el marco perfecto —altura, ambición, pertenencia— y la landing lo convierte en una
promesa concreta: *jugadoras que leen el juego antes de que ocurra*.

- **Promesa:** criterio + carácter + resultados medibles.
- **Prueba:** 12 temporadas · 9 títulos · +340 jugadoras · 94 % de continuidad.
- **Diferenciador:** el método (Sistema 360) y el archivo real del equipo, no stock.
- **Tono:** autoridad tranquila, frases cortas, cero motivación vacía.

**Anti-tono:** frases tipo “transforma tu vida”, emojis, degradados pastel, stock genérico.

---

## 2. Estructura de la página

| # | Sección | Objetivo de conversión |
|---|---|---|
| — | **Hero** | Promesa + prueba + CTA en el primer viewport; integrar Team SKY y el film |
| 01 | **Film** | Pieza central multimedia: 25 s del equipo + ficha técnica + dirección musical |
| 02 | **Team SKY** | Cultura de equipo: identidad, competencia, comunidad |
| 03 | **Palmarés** | Autoridad verificable: contadores, timeline, credenciales, impacto |
| 04 | **Filosofía** | “No entreno cuerpos. Entreno criterio.” + 4 pilares |
| 05 | **Método 360** | Proceso medible en 4 fases + pizarra táctica isométrica |
| 06 | **Programas** | Clínica grupal · Asesoría 1:1 · Dirección técnica |
| 07 | **Galería** | Evidencia real (B/N → color al hover) |
| 08 | **Testimonios** | Prueba social cualitativa |
| 09 | **Contacto** | Formulario de 4 campos + agenda directa + FAQ |
| — | **Footer** | Cierre de marca, contacto y recordatorio de SKY |

### Hero — copy final
- **Eyebrow:** Gloria Isabel Celis Suárez · Head coach · Team SKY
- **H1:** *SKY no es un nombre. Es una forma de jugar.*
- **Sub:** Formo jugadoras que leen el juego antes de que ocurra: criterio, carácter y una
  metodología que convierte talento en resultados medibles. **12 temporadas, 9 títulos** y un
  equipo que compite con identidad.
- **CTA primario:** `Agendar diagnóstico gratuito`
- **CTA secundario:** `Ver el film · 0:25`
- **Micro-prueba:** 30 min · sin costo · cupos limitados · respuesta < 24 h.

---

## 3. Sección multimedia — el film

### 3.1 Guion y ritmo (25 s · 11 planos + 2 tarjetas)

| # | Plano | Movimiento | Duración |
|---|---|---|---|
| 00 | Tarjeta SKY · Temporada 2025–26 · nombre completo | zoom in lento | 2,8 s |
| 01 | Equipo al aire libre (cancha abierta, cielo) | paneo lateral | 2,6 s |
| 02 | Huddle del equipo antes del partido | zoom in | 2,6 s |
| 03 | Celebración equipo turquesa | zoom out | 2,6 s |
| 04 | Medallas y trofeo | zoom in | 2,6 s |
| 05 | Equipo con el trofeo | paneo | 2,6 s |
| 06 | Cancha institucional (plano general) | zoom out | 2,6 s |
| 07 | Equipo amarillo en formación | zoom in | 2,6 s |
| 08 | Team SKY en formación | paneo | 2,6 s |
| 09 | Coach y jugadoras juntas | zoom out | 2,6 s |
| 10 | Coach con flores y canasta | zoom in | 2,6 s |
| 11 | Jugadora con balón (retrato) | paneo | 2,6 s |
| 12 | Tarjeta final: “El juego se gana antes del salto inicial” | estático | 3,2 s |

- **Transiciones:** fundido de 0,8 s entre planos (nunca corte seco: el film respira).
- **Atmósfera:** carbón profundo, grano fino, viñeta suave, contraste alto y saturación contenida.
  La cámara inicia y termina quieta: el movimiento solo existe en el medio.
- **Regla de oro:** ninguna cara se corta; cada plano respeta el encuadre del sujeto.

### 3.2 Dirección musical

- **Pista actual:** «**Rising Game**» — Kevin MacLeod ([incompetech.com](https://incompetech.com)),
  licencia **CC BY 4.0**. Corte desde 1:16 con fades de 0,8 s / 1,6 s y normalización a −15 LUFS.
  Crédito obligatorio y visible en la página.
- **Carácter:** rock deportivo ascendente, 112 BPM, percusión marcada y sintetizadores cálidos;
  la energía crece durante todo el corte. Es la referencia “motivacional tipo Rocky” sin usar
  material con copyright.
- **Estructura del corte:** entrada en seco con las tarjetas, tema principal del 02 al 08,
  clímax en el bloque de equipo SKY y cierre en fade con la tarjeta final.
- **Si se quiere una versión más sinfónica** (metales y cuerdas, fanfarria heroica), la
  alternativa es un encargo original o una pista con licencia comercial (Artlist, Epidemic Sound,
  Musicbed). **No** usar el tema de *Rocky* ni audio de redes sociales: son obras protegidas.
- **Implementación:** el video ya viaja con la pista montada; reemplazarla no requiere
  recomprimir el video, solo volver a mezclar el audio (25 s).

### 3.3 Especificación técnica del video

| Parámetro | Valor |
|---|---|
| Formato / relación | 4:5 vertical · **960 × 1200** |
| Códec | H.264 (avc1) · yuv420p · 30 fps |
| Duración | 25 s · loop |
| Peso | ≈ 6,2 MB (`sky-film.mp4`) |
| Póster | `sky-film-poster.jpg` (fotograma 6,6 s) |
| Antes / después | tarjetas de marca con la tipografía del sitio |
| Reproducción | `preload="none"`, póster primero, carga al primer clic |

**Integración en la web:** reproductor propio (play, pausa, progreso, mute), sin controles
nativos; se pausa automáticamente al salir del viewport y respeta `prefers-reduced-motion`.

---

## 4. Dirección de arte

### 4.1 Paleta

| Token | Hex | Rol | Proporción |
|---|---|---|---|
| Carbón 900 | `#0A0B0D` | Fondo / vestuario | 45 % |
| Carbón 800 | `#111317` | Secciones alternas | 20 % |
| Carbón 700 | `#1A1D22` | Tarjetas | 15 % |
| Crema | `#F4F1E9` | Texto | 10 % |
| Naranja balón | `#FF4D1F` | CTA, SKY, datos | 6 % |
| Oro trofeo | `#E9B44C` | Logros y credenciales | 3 % |

Regla: el naranja solo para acción y marca; el oro solo para logro. Nunca juntos en un componente.

### 4.2 Tipografía

- **Display:** Barlow Condensed 700–800, mayúsculas, tracking negativo (titulares, cifras, botones).
- **Lectura:** Inter 400–600, 16–19 px, líneas de máximo 62 caracteres.
- **Escala:** `clamp()` fluida; H1 44–90 px según viewport.

### 4.3 Fotografía

- Tratamiento de archivo: blanco y negro con contraste alto y grano fino; color al hover.
- Recortes: 4:5 en galería, 16:9 en la foto de equipo, 4:5 en hero y póster.
- Origen: 95 capturas de Facebook → se aisló la foto real de cada una (se eliminó la interfaz
  y las barras negras) antes de recortar. Ver `tools/extract.py`.

### 4.4 Elementos 3D y gráficos

- Pizarra táctica isométrica en CSS/SVG junto al Método 360.
- Líneas de cancha al 6 % como textura; diagramas de jugada en SVG.
- La pieza 3D nunca compite con la foto: si no aporta lectura, se elimina.

---

## 5. Copywriting

**Titulares aprobados**

| Uso | Texto |
|---|---|
| H1 | SKY no es un nombre. Es una forma de jugar. |
| H2 film | El juego, en 25 segundos. |
| H2 equipo | Un equipo, una cultura. |
| H2 logros | Autoridad que se mide en la cancha. |
| H2 filosofía | No entreno cuerpos. Entreno criterio. |
| H2 método | El sistema 360. |
| H2 programas | Elige tu cancha. |
| H2 galería | Dentro y fuera de la cancha. |
| H2 testimonios | Quienes ya jugaron este juego. |
| H2 contacto | Hablemos de tu próxima temporada. |

**CTAs**

1. `Agendar diagnóstico gratuito` — recomendada (riesgo cero, acción concreta).
2. `Ver el film · 0:25` — para visitantes fríos que aún no confían.
3. `Quiero este nivel de producción` — cierre del bloque multimedia.

**Variantes A/B de H1**
- A (actual): SKY no es un nombre. Es una forma de jugar.
- B: El juego se gana antes del salto inicial.
- C: 12 temporadas. 9 títulos. Una forma de jugar.

---

## 6. CRO

- Un solo CTA primario, repetido 5 veces con el mismo texto.
- Promesa + prueba + CTA sin scroll en desktop y móvil.
- Formulario de 4 campos; el botón dice el resultado, no la acción.
- Escasez real (3 cupos) y microcopy de riesgo cero junto al CTA.
- Llamada directa como canal de menor fricción (el número es fijo, no WhatsApp).
- Eventos a medir: `cta_click_hero`, `film_play`, `film_complete`, `form_start`,
  `form_submit`, `phone_click`, `scroll_75`. Objetivo: ≥ 4 % formulario / ≥ 8 % llamada.

---

## 7. Especificación técnica

- HTML + CSS + JS vanilla, fuentes autoalojadas (woff2, OFL), sin dependencias.
- Video con `preload="none"` y póster; 6 MB que solo se descargan al pulsar play.
- Breakpoints 480 / 720 / 1024 / 1280; sin scroll horizontal.
- Accesibilidad: contraste AA, `:focus-visible`, `aria-*` en el reproductor y el menú,
  `prefers-reduced-motion` desactiva animaciones.
- SEO: `<title>`, meta description, Open Graph y datos estructurados `Person` + `SportsTeam`.

---

## 8. Entregables

1. `index.html` + `assets/` — landing completa y responsive.
2. `assets/video/sky-film.mp4` — film 25 s con música (Kevin MacLeod, CC BY 4.0).
3. `assets/img/` — fotos recortadas y optimizadas desde la carpeta original.
4. `PROPUESTA.md` — este documento.
5. Repositorio publicado en GitHub Pages.

## 9. Pendientes del cliente

- Pista musical licenciada (o encargo) para el máster final del film.
- Testimonios reales autorizados por escrito.
- Enlaces de Instagram / YouTube / LinkedIn (hoy `#`).
- Validación del palmarés y credenciales (los datos actuales son demostrativos).
