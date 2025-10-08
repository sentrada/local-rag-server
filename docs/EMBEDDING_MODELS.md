# Embedding modellek összehasonlítása

| Modell név                              | Méret   | Sebesség | Nyelvi támogatás | Pontosság |          Megjegyzés         |
|-----------------------------------------|---------|----------|------------------|-----------|-----------------------------|
| all-MiniLM-L6-v2                        | ~80MB   | Gyors    | EN               | Közepes   | Alapértelmezett, kis méret  |
| paraphrase-multilingual-MiniLM-L12-v2   | ~120MB  | Gyors    | Multilingual     | Jó        | Jelenlegi default           |
| paraphrase-multilingual-mpnet-base-v2   | ~1GB    | Lassabb  | Multilingual     | Nagyon jó | Nagyobb memória igény       |
| intfloat/multilingual-e5-large          | ~2.2GB  | Lassú    | Multilingual     | Legjobb   | Nagy, pontos, lassú         |

## Mikor melyiket használd?
- Kis projekthez, gyors indexeléshez: **all-MiniLM-L6-v2**
- Többnyelvű, közepes projekt: **paraphrase-multilingual-MiniLM-L12-v2**
- Nagy pontosság, többnyelvű: **mpnet-base-v2** vagy **e5-large**
- Ha fontos a pontosság, és nem gond a lassúság: **e5-large**

## Docker image méret
A nagy modellek jelentősen növelik az image méretét. Ha a konténer nem lát ki a netre, célszerű előre letölteni a szükséges modelleket.

## Teljesítmény figyelmeztetés
Az e5-large modell lassabb, de pontosabb. A UI figyelmeztesse a felhasználót modellváltáskor.
