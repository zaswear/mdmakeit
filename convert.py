import sys
import os
import re
from markitdown import MarkItDown

def clean_markdown(text):
    if not text:
        return ""

    lines = text.split('\n')
    cleaned_lines = []
    in_code_block = False

    # Expresión regular para detectar comandos de terminal habituales
    def is_command_line(line):
        trimmed = line.strip()
        if not trimmed:
            return False
        
        # Ignorar comentarios generales que no parecen código
        if trimmed.startswith('#') and not in_code_block:
            # Si contiene comando git, puede ser comentario de git
            if 'git ' not in trimmed.lower():
                return False
                
        words = trimmed.split()
        first_word = words[0].lower().replace('$', '')
        
        # Palabras clave de comandos comunes
        cmd_keywords = {
            'git', 'npm', 'node', 'python', 'python3', 'pip', 'pip3', 
            'cat', 'cd', 'wsl', 'mkdir', 'hatch', 'curl', 'wget', 
            'ssh', 'docker', 'sudo', 'ls', 'pwd', 'mv', 'cp', 'rm'
        }
        
        if first_word in cmd_keywords:
            return True
        if trimmed.startswith('$ ') and len(words) > 1 and words[1] in cmd_keywords:
            return True
        if trimmed.startswith('#') and in_code_block:
            return True
        return False

    for line in lines:
        # 1. Limpieza de tabuladores dobles o triples entre palabras a espacios sencillos
        leading_space_len = len(line) - len(line.lstrip('\t '))
        leading_spaces = line[:leading_space_len].replace('\t', '    ')
        content = line[leading_space_len:]
        
        # Reemplazar tabulaciones en el contenido por espacios
        content_clean = re.sub(r'\t+', ' ', content)
        # Colapsar múltiples espacios seguidos
        content_clean = re.sub(r' +', ' ', content_clean)
        
        # Reconstruir la línea limpia
        line_clean = leading_spaces + content_clean.strip()
        trimmed = line_clean.strip()

        # 2. Formatear advertencias o reglas como Blockquotes de GitHub Alerts
        if trimmed.startswith('Regla n.º') or trimmed.startswith('Regla nº') or trimmed.startswith('Regla:'):
            line_clean = f"\n> [!IMPORTANT]\n> **{trimmed}**"
        elif trimmed.startswith('Mantra:'):
            line_clean = f"\n> [!NOTE]\n> **{trimmed}**"
        elif trimmed.startswith('! '):
            line_clean = f"\n> [!WARNING]\n> **{trimmed[2:]}**"
        
        # 3. Detectar Títulos principales y subtítulos (líneas enteras en mayúsculas o numeradas)
        elif re.match(r'^\d+\s+[A-ZÁÉÍÓÚÑ\s\-\—\(\)\d\:\,\.\#\º\ª]+$', trimmed):
            line_clean = f"\n## {trimmed}"
        elif re.match(r'^[A-ZÁÉÍÓÚÑ\s\-\—\(\)\d\:\,\.\#\º\ª\+]+$', trimmed) and len(trimmed) > 8:
            if "RUTINA" in trimmed or "GIT" in trimmed or len(trimmed) > 28:
                line_clean = f"\n# {trimmed}"
            else:
                line_clean = f"\n## {trimmed}"
        elif trimmed.startswith('? ') or (trimmed.startswith('¿') and trimmed.endswith('?')):
            line_clean = f"\n### {trimmed}"

        # 4. Agrupación y formateo de bloques de código
        is_cmd = is_command_line(line_clean)
        if is_cmd:
            if not in_code_block:
                cleaned_lines.append('```bash')
                in_code_block = True
            
            # Formatear el comentario de código git para que tenga separación limpia
            if '#' in line_clean:
                parts = line_clean.split('#', 1)
                line_clean = f"{parts[0].strip():<45} # {parts[1].strip()}"
                
            cleaned_lines.append(line_clean)
        else:
            if in_code_block:
                cleaned_lines.append('```')
                in_code_block = False
            cleaned_lines.append(line_clean)

    if in_code_block:
        cleaned_lines.append('```')

    # Retornar texto unido y limpiar saltos de línea triples a dobles
    result_text = '\n'.join(cleaned_lines)
    result_text = re.sub(r'\n{3,}', '\n\n', result_text)
    return result_text.strip() + '\n'


def main():
    if len(sys.argv) < 2:
        print("ERROR: Falta el archivo o URL de entrada.", file=sys.stderr)
        sys.exit(1)

    source = sys.argv[1]
    is_url = source.startswith(('http://', 'https://'))
    
    if not is_url and not os.path.exists(source):
        print(f"ERROR: El archivo local no existe: {source}", file=sys.stderr)
        sys.exit(1)

    try:
        # Inicializar MarkItDown
        md = MarkItDown(enable_plugins=True)
        result = md.convert(source)
        
        # Aplicar el formateador post-conversión
        formatted_md = clean_markdown(result.text_content)
        
        # Enviar salida estándar en UTF-8
        sys.stdout.buffer.write(formatted_md.encode('utf-8'))
    except Exception as e:
        print(f"ERROR en la conversión de markitdown: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
