import re
import sys
from pathlib import Path

EXCEPTIONS = {"TV", "PC", "PP", "HP", "HM", "TM", "MC", "DNA", "HQ", "AM", "PM", "ID", "OT"}

def fix_caps_in_string(s):
    def replace(m):
        word = m.group()
        if word.startswith('{'):  # ignora comandos entre {}
            return word
        if word in EXCEPTIONS:
            return word
        return word.capitalize()
    # Alternância: captura {COMANDO} primeiro, depois ALL CAPS
    return re.sub(r'\{[^}]*\}|\b[A-Z]{2,}\b', replace, s)

def process_party_file(path, dry_run=True):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    new_lines = []
    
    for line in lines:
        if line.startswith("Name:"):
            fixed = re.sub(r'\b[A-Z]{2,}\b', lambda m: m.group() if m.group() in EXCEPTIONS else m.group().capitalize(), line)
            if fixed != line:
                print(f"  {line.rstrip()!r}  →  {fixed.rstrip()!r}")
            new_lines.append(fixed if not dry_run else line)
        else:
            new_lines.append(line)
    
    if not dry_run and "".join(new_lines) != text:
        path.write_text("".join(new_lines), encoding="utf-8")
        
def process_file(path, dry_run=True):
    text = path.read_text(encoding="utf-8")
    
    # Só mexe no conteúdo dentro de aspas duplas
    def replace_in_string(match):
        original = match.group(0)
        fixed = '"' + fix_caps_in_string(match.group(1)) + '"'
        if original != fixed:
            print(f"  {original!r}  →  {fixed!r}")
        return fixed if not dry_run else original

    new_text = re.sub(r'"([^"]*)"', replace_in_string, text)
    
    if not dry_run and new_text != text:
        path.write_text(new_text, encoding="utf-8")

# --- Configuração ---
dry_run = True

#root = Path(".")  # or Path("src") if you want to limit to that folder
#
#for file in sorted(root.rglob("*.inc")):
#    print(f"\n[{file}]")
#    process_file(file, dry_run=dry_run)

party_files = [
    Path("src/strings.c"),
#    Path("src/contest.c"),
#    Path("src/field_specials.c"),
#    Path("src/frontier_util.c"),
#    Path("src/item_menu.c"),
#    Path("src/landmark.c"),
#    Path("src/player_pc.c"),
#    Path("src/pokeblock.c"),
#    Path("src/pokemon_storage_system.c"),
]

for file in party_files:
    print(f"\n[{file}]")
    process_file(file, dry_run=dry_run)  # ← era process_party_file
