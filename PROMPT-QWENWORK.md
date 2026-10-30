# Prompt para QwenWork — publicar la landing en Alibaba Cloud

Copia todo el bloque de abajo en QwenWork (o en cualquier agente de código de Alibaba).
Está escrito para que el agente **reutilice el repositorio tal cual** y lo publique con una
**URL propia e independiente** en Alibaba Cloud, sin tocar el diseño.

---

## PROMPT (copiar desde aquí)

Eres un ingeniero de despliegue web. Tu tarea es **publicar en Alibaba Cloud** un sitio
estático que ya existe y funciona; **no rediseñes, no reescribas el contenido y no cambies
la estructura**. Solo despliega y verifica.

### 1. Contexto del proyecto

- Repositorio: `https://github.com/MrCastilloF/coach-basket` (rama `main`).
- Es una **landing page estática** de una sola página (HTML + CSS + JS vanilla, sin build,
  sin Node, sin framework).
- Nombre de marca: **Team SKY — Gloria Isabel Celis Suárez, coach de baloncesto**.
- Archivos clave:
  - `index.html` — la página completa.
  - `assets/css/styles.css` — sistema de diseño (tema claro: papel, azul cielo, naranja).
  - `assets/js/main.js` — menú, contadores, formulario, reproductor y galería (lightbox).
  - `assets/img/` — fotos optimizadas (hero, equipo, galería).
  - `assets/img/archivo/` — **95 fotos** (`t01…t95` miniatura 360×450, `f01…f95` versión 720×900).
  - `assets/video/sky-film.mp4` — film de 25 s, 4:5, H.264, con audio AAC (≈ 6 MB).
  - `assets/fonts/` — Barlow Condensed + Inter en woff2.
  - `PROPUESTA.md` — documento de diseño, copy y ficha del film.
- **No hay paso de compilación.** El sitio se sirve tal cual desde la raíz del repo.
- Requisitos especiales de MIME: `.woff2` → `font/woff2`, `.mp4` → `video/mp4`,
  `.jpg` → `image/jpeg`, `.css` → `text/css`, `.js` → `application/javascript`.

### 2. Objetivo

Publicar el sitio en **Alibaba Cloud** con una **URL pública independiente** (por ejemplo,
un bucket OSS con *static website hosting* o un dominio propio), accesible por HTTPS,
sin depender de GitHub Pages.

### 3. Plan de trabajo (recomendado: OSS + CDN)

1. **Clona el repositorio** y confirma que el sitio corre en local:
   ```bash
   git clone https://github.com/MrCastilloF/coach-basket.git
   cd coach-basket
   python -m http.server 8080     # abrir http://localhost:8080
   ```
   Verifica que no haya 404 y que el video reproduzca.

2. **Crea un bucket OSS** en la región más cercana a Colombia (por ejemplo
   `oss-us-west-1` o `oss-ap-southeast-1`) con nombre único, p. ej. `team-sky-web`.
   - Permisos: lectura pública (public-read) **solo si** no usarás CDN autenticado.
   - Activa **Static Website Hosting**: documento índice `index.html`, documento de error
     `index.html` (para rutas internas) o `404.html` si lo agregas.

3. **Sube el sitio conservando la estructura**, excluyendo `.git`, `work/`, `tools/` y
   cualquier archivo temporal:
   ```bash
   ossutil cp -r ./  oss://team-sky-web/  --exclude ".git/*" --exclude "work/*" --exclude "tools/*"
   ```
   Ajusta los tipos MIME si tu herramienta no los detecta (ver punto 1).

4. **Entrega la URL**. Tres caminos válidos, en orden de preferencia:
   - **CDN de Alibaba Cloud** delante del bucket con dominio propio
     (`https://sky.tudominio.com`), certificado SSL gratuito y caché para
     `assets/*` (1 año) e `index.html` (sin caché o 5 min).
   - **Endpoint de static website** del bucket
     (`http://team-sky-web.oss-<region>.aliyuncs.com/index.html`), con HTTPS habilitado
     vía CDN o certificado del bucket.
   - **Function Compute / ESA** si la cuenta ya usa ese servicio: sirve los archivos
     estáticos desde el mismo contenido.

5. **Opcional pero recomendado:** apunta un subdominio propio (registro CNAME al CDN),
   activa HTTPS y comprime `html/css/js` en el CDN (brotli/gzip).

### 4. Verificación obligatoria (no entregues sin esto)

- La URL responde **200** y muestra el hero con el nombre completo.
- **No hay errores de consola** ni peticiones 404.
- Las **fuentes** cargan (8 archivos woff2) y el texto no cae a fuente del sistema.
- El **video** (`assets/video/sky-film.mp4`) se reproduce con sonido al pulsar play.
- La **galería de 95 fotos** abre, navega con flechas y cierra con Escape.
- **Móvil (390 px)**: sin scroll horizontal y menú hamburguesa operativo.
- El formulario valida y muestra el mensaje de confirmación (es demostrativo, no envía).

### 5. Entregables de tu respuesta

1. **URL pública final** (la que debo compartir con la clienta).
2. Servicio de Alibaba Cloud usado y región.
3. Comandos o pasos ejecutados (para reproducirlo).
4. Resultado de la verificación (checklist de arriba).
5. Cómo actualizar el sitio en el futuro: `git pull` + `ossutil sync` (o pipeline equivalente).

### 6. Restricciones

- **No modifiques** el diseño, los textos, las fotos ni el video.
- **No inventes** testimonios, cifras ni datos de contacto: son demostrativos y están
  señalados en `PROPUESTA.md`.
- **No uses** el tema de *Rocky* ni música con copyright; el film ya trae una pista
  licenciada (**«Rising Game» — Kevin MacLeod, CC BY 4.0**) y su crédito debe conservarse
  visible en la página.
- Mantén el repositorio de GitHub como fuente de verdad y el despliegue como espejo.

## FIN DEL PROMPT

---

## Notas para ti (no van en el prompt)

- **Costo**: un bucket OSS con ~17 MB y tráfico bajo cuesta céntimos al mes; el CDN cobra
  por GB servido. El video de 6 MB solo se descarga cuando alguien pulsa play.
- **Alternativa sin OSS**: si QwenWork tiene acceso a *Alibaba Cloud ESA Pages* o a un
  servicio de hosting estático, sirve igual: el sitio no necesita backend.
- **Dominio**: si compras uno (p. ej. `teamsky.co`), el CNAME al CDN te da HTTPS gratis.
- **Actualizaciones**: cada `git push` a `main` sigue publicando en GitHub Pages; para
  Alibaba, repite el `ossutil sync` (o conecta un pipeline).
