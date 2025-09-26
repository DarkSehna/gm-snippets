# tools/validate_index.py
# Uso: python tools/validate_index.py
# Verifica:
# 1) index.json é JSON válido
# 2) IDs duplicados
# 3) IDs em snake_case ^[a-z0-9_]+$
# 4) Caminhos existem
# 5) Plataforma coerente com a pasta (gamemaker -> snippets/GameMaker)
# 6) (AVISO) nome de arquivo == id + ".json"
# 7) (leve) tags é lista de strings, se presente

import os, sys, json, re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(REPO_ROOT, "snippets", "index.json")

SNAKE_RE = re.compile(r"^[a-z0-9_]+$")  # snake_case

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

    # 2) IDs duplicados + 3) snake_case
    seen = {}
    dup = []
    bad_case = []
    for it in items:
        i = it.get("id")
        if not i:
            warn(f"Item sem 'id': {it}")
            continue
        if i in seen:
            dup.append(i)
        seen[i] = True
        if not SNAKE_RE.fullmatch(i):
            bad_case.append(i)
    if dup:
        error(f"IDs duplicados: {', '.join(dup)}")
    else:
        ok("Sem IDs duplicados.")
    if bad_case:
        error("IDs fora do padrão snake_case: " + ", ".join(bad_case))
    else:
        ok("Todos os IDs estão em snake_case.")

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

    # (extra) tags é lista de strings, se presente
    bad_tags = []
    for it in items:
        tags = it.get("tags")
        if tags is None:
            continue
        if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
            bad_tags.append(it.get("id"))
    if bad_tags:
        error("Campo 'tags' inválido (deve ser lista de strings) nos IDs: " + ", ".join(bad_tags))
    else:
        ok("Campo 'tags' válido (quando presente).")

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

    # 6) (AVISO) checar se nome do arquivo bate com id
    for it in items:
        _id = it.get("id")
        p = it.get("path") or ""
        fname = os.path.splitext(os.path.basename(p))[0] if p else ""
        if _id and fname and _id != fname:
            warn(f"Nome do arquivo '{fname}.json' difere do id '{_id}' para path '{p}'")

    # saída
    # falhar se houver: ids duplicados, ids fora do padrão, caminhos ausentes, tags inválidas
    has_errors = bool(dup or bad_case or missing or bad_tags)
    if has_errors:
        sys.exit(1)
    ok("Validação concluída com sucesso.")

if __name__ == "__main__":
    main()
