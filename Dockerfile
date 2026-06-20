# MDMakeIt — Node (Express) + Python (markitdown) en un solo contenedor
FROM node:20-slim

# Python + ffmpeg (markitdown lo usa para audio/vídeo) + utilidades
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python3-venv python3-pip ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# venv aislado para markitdown
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHON_PATH="/opt/venv/bin/python"

WORKDIR /app

# Dependencias Python (cacheadas)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Dependencias Node (cacheadas)
COPY package*.json ./
RUN npm ci --omit=dev || npm install --omit=dev

# Código
COPY . .

ENV PORT=3003
EXPOSE 3003
CMD ["node", "server.js"]
