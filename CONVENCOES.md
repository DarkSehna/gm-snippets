# Convenções do repositório (v1)

IDs
- Formato: snake_case (regex: ^[a-z0-9_]+$). Ex.: basic_movement, collect_coin.
- O nome do arquivo do snippet é exatamente o ID + `.json`.

Plataforma e linguagem
- platform: "gamemaker"
- lang: "gml"

Estrutura de pastas
- snippets/ (índice e coleções)
- snippets/GameMaker/ (arquivos .json do Game Maker)
- (futuro) snippets/Construct3/, snippets/Scratch/

Index
- `snippets/index.json` é a fonte canônica.
- Cada item tem (mínimo): id, title, platform, lang, tags, path.

Tags (vocabulário base)
- plataforma, movimento, pulo, inimigo, patrulha,
  moeda, coletavel, hud, pontuacao, pause, menu,
  knockback, colisao, camera, cenario, ui, gamefeel, acessibilidade

Validação
- Antes de dar push, rode o validador:
  `python tools/validate_index.py --root . --index snippets/index.json`
