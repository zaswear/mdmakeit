# MDMakeIt

Un convertidor local privado de documentos a Markdown. Sube archivos PDF, Word, Excel, PowerPoint o imágenes y obtén código Markdown limpio estructurado listo para VS Code.

Esta utilidad actúa como un puente web sobre el motor de conversión de **Microsoft MarkItDown** de Python instalado en tu entorno local.

## Características
* **Conversor local rápido**: Sube tus archivos locales sin que salgan de tu red o servidor privado.
* **Drag & Drop**: Interfaz intuitiva y moderna para arrastrar y soltar ficheros.
* **Visualizador y Utilidades**: Caja de previsualización monospaced con funciones integradas de "Copiar al portapapeles" y "Descargar como archivo `.md`".

## Requisitos
El servidor de backend de Node.js ejecuta el comando de markitdown mediante el entorno virtual de Python configurado en tu directorio. Asegúrate de tener:
* Python 3 y `markitdown` instalados en `/home/zaswear/projects/markitdown/.venv/`

## Instrucciones de Lanzamiento Local

1. Abre una terminal de WSL e ingresa a la carpeta del proyecto:
   ```bash
   cd /home/zaswear/projects/MDMakeIt
   ```

2. Instala las dependencias ligeras necesarias de Express:
   ```bash
   npm install
   ```

3. Inicia el servidor local de desarrollo:
   ```bash
   node server.js
   ```

4. Abre la utilidad en tu navegador:
   ```
   http://localhost:3003
   ```

---
*Nota: Este proyecto está enlazado a tu panel general local `ZaswearProjects` en la tarjeta de utilidad `[U2]`.*
