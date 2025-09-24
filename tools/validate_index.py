# tools/validate_index.py
# Uso: python tools/validate_index.py
# Verifica:
# 1) index.json é JSON válido
# 2) IDs duplicados
# 3) Caminhos existem
# 4) Plataforma coerente com a pasta (gamemaker -> snippets/GameMaker)

import os, sys, json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(REPO_ROOT, "snippets", "index.json")

def error(msg):
    print(f"[ERRO] {msg}")

def warn(msg):
    print(f"[AVISO] {msg}")

def ok(msg):
    print(f"[OK] {msg}")

def main():
    if not os.path.exists(INDEX_PATH):
        error(f"Não encontrei {INDEX_PATH}")
        sys.exit(1)

    # 1) JSON válido
    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            idx = json.load(f)
        ok("index.json é JSON válido.")
    except Exception as e:
        error(f"index.json inválido: {e}")
        sys.exit(1)

    items = idx.get("items") or idx.get("snippets") or []
    if not items:
        warn("Nenhum 'items' ou 'snippets' encontrado. Nada a validar de paths.")

    # 2) IDs duplicados
    seen = {}
    dup = []
    for it in items:
        i = it.get("id")
        if not i:
            warn(f"Item sem 'id': {it}")
            continue
        if i in seen:
            dup.append(i)
        seen[i] = True
    if dup:
        error(f"IDs duplicados: {', '.join(dup)}")
    else:
        ok("Sem IDs duplicados.")

    # 3) Caminhos existem
    missing = []
    for it in items:
        p = it.get("path")
        if not p:
            warn(f"Item {it.get('id')} sem 'path'.")
            continue
        abs_p = os.path.join(REPO_ROOT, p)
        if not os.path.exists(abs_p):
            missing.append((it.get("id"), p))
    if missing:
        for i, p in missing:
            error(f"Caminho não encontrado para {i}: {p}")
    else:
        ok("Todos os caminhos de 'path' existem.")

    # 4) Plataforma coerente com a pasta
    incoerentes = []
    for it in items:
        plat = (it.get("platform") or "").lower()
        path = (it.get("path") or "")
        if plat == "gamemaker" and "snippets/GameMaker/" not in path and "snippets/gamemaker/" not in path:
            incoerentes.append((it.get("id"), plat, path))
    if incoerentes:
        for i, plat, p in incoerentes:
            warn(f"Plataforma '{plat}' não bate com pasta em {i}: {p}")
    else:
        ok("Plataforma e pasta coerentes em todos os itens.")

    if dup or missing:
        sys.exit(1)
    ok("Validação concluída com sucesso.")

if __name__ == "__main__":
    main()
