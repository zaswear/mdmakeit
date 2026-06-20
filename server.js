import express from 'express';
import multer from 'multer';
import cors from 'cors';
import { execFile } from 'child_process';
import fs from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3003;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Ensure uploads directory exists
const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

// Multer storage setup
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
    cb(null, file.fieldname + '-' + uniqueSuffix + ext);
  }
});

const upload = multer({ storage: storage });

// Configurable por entorno: en local tu venv; en Docker/Render → /opt/venv/bin/python
const pythonPath = process.env.PYTHON_PATH || 'python3';
const convertScript = path.join(__dirname, 'convert.py');

// Common function to execute conversion via Python script
function runConversion(sourcePathOrUrl, res, cleanupCallback = null) {
  execFile(pythonPath, [convertScript, sourcePathOrUrl], { maxBuffer: 1024 * 1024 * 10 }, (error, stdout, stderr) => {
    if (cleanupCallback) {
      cleanupCallback();
    }

    if (error) {
      console.error('Error during conversion:', error);
      console.error('Stderr:', stderr);
      return res.status(500).json({
        error: 'Error al convertir el recurso a Markdown.',
        details: stderr || error.message
      });
    }

    res.json({
      markdown: stdout
    });
  });
}

// 1. API endpoint for file uploads
app.post('/api/convert', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No se ha subido ningún archivo.' });
  }

  const filePath = req.file.path;
  const originalName = req.file.originalname;

  console.log(`Convirtiendo archivo: ${originalName} -> ${filePath}`);

  runConversion(filePath, res, () => {
    // Delete uploaded file after conversion
    fs.unlink(filePath, (err) => {
      if (err) console.error(`Error deleting temp file: ${filePath}`, err);
    });
  });
});

// 2. API endpoint for URL conversion (Webpages, Youtube transcribing, Epubs, ZIPs etc.)
app.post('/api/convert-url', (req, res) => {
  const { url } = req.body;
  if (!url) {
    return res.status(400).json({ error: 'Falta la URL de entrada.' });
  }

  console.log(`Convirtiendo URL remota: ${url}`);

  runConversion(url, res);
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Servidor MDMakeIt escuchando en http://localhost:${PORT}`);
});
