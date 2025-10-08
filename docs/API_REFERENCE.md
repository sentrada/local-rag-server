# API Reference – Embedding Model Management

## GET /models
- Leírás: Elérhető embedding modellek listája
- Válasz példa:
```
["all-MiniLM-L6-v2", "paraphrase-multilingual-MiniLM-L12-v2", "paraphrase-multilingual-mpnet-base-v2", "intfloat/multilingual-e5-large"]
```

## GET /projects/{project}/model
- Leírás: Az adott projekt aktuális embedding modellje
- Válasz példa:
```
{"project_path": "/app/data/projects/XY", "embedding_model": "intfloat/multilingual-e5-large"}
```

## POST /projects/{project}/model
- Leírás: Modell váltás az adott projekthez (index törlés, újraindexelés opció)
- Request body példa:
```
{"model": "paraphrase-multilingual-mpnet-base-v2", "auto_reindex": true}
```
- Válasz példa:
```
{"status": "ok", "project_path": "/app/data/projects/XY", "embedding_model": "paraphrase-multilingual-mpnet-base-v2", "reindex_started": true}
```

## Megjegyzés
- Modell váltáskor a régi index törlődik, újraindexelés szükséges.
- A modellek listája bővíthető, a backend oldalon kell karbantartani.
