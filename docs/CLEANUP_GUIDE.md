# 🗑️ Felesleges Fájlok Listája

## ❌ Törlendő Fájlok

### 1. Redundáns/Elavult Dokumentáció (Duplikátumok)
- `STATUS.md` ❌ - Elavult projekt statisztika
- `NUMPY_FIX.md` ❌ - Régi fix dokumentáció (már nincs rá szükség)
- `MULTI_PROJECT_DONE.md` ❌ - Átmeneti jegyzet (MULTI_PROJECT_SUPPORT.md-ben van)
- `MULTILINGUAL_MODEL_DONE.md` ❌ - Átmeneti jegyzet (PROJECT_SUMMARY.md-ben frissíthető)

### 2. Üres/Felesleges Könyvtárak
- `ui/` ❌ - Teljesen üres mappa
- `examples/copilot_extension.py` ⚠️ - Nem használt példa (opcionális törlés)
- `examples/usage_examples.py` ⚠️ - Nem használt példa (opcionális törlés)

### 3. Nem Használt Konfigurációs Fájlok
- `package.json` ⚠️ - Node.js package (nem szükséges Python projekthez)
  - Alternatíva: PowerShell scriptek már megvannak
- `health_check.py` ⚠️ - Standalone health check (API `/health` endpoint-tal helyettesíthető)
- `test_server.py` ⚠️ - Manual teszt script (scriptekkel helyettesíthető)
- `setup_rag_windows.ps1` ⚠️ - Régi setup script (README.md-ben van jobb)

### 4. Dev Fájlok (Ha nem fejlesztesz)
- `docker-compose.dev.yml` ⚠️ - Development override (csak ha fejlesztesz)

---

## ✅ Megtartandó Fontosabb Fájlok

### Core Dokumentáció (Megtartani)
- `README.md` ✅ - Fő dokumentáció
- `QUICKSTART.md` ✅ - Gyors kezdés
- `TROUBLESHOOTING.md` ✅ - Hibaelhárítás
- `COPILOT_INTEGRATION.md` ✅ - Copilot integráció
- `MIGRATION_GUIDE.md` ✅ - Migration használat
- `PROJECT_SUMMARY.md` ✅ - Projekt áttekintés
- `CHANGELOG.md` ✅ - Verzió történet

### Multi-Project Dokumentáció
- `MULTI_PROJECT_SUPPORT.md` ✅ - Multi-project használat
- `MULTI_PROJECT_GUIDE.md` ✅ - Részletes példák
- `SCRIPTS_README.md` ✅ - PowerShell scriptek dokumentáció

### PowerShell Scriptek (Megtartani)
- `Ask-RAG.ps1` ✅
- `Reindex-Project.ps1` ✅
- `Switch-Project.ps1` ✅
- `List-Projects.ps1` ✅
- `Add-Project.ps1` ✅

### Konfiguráció (Megtartani)
- `.env` ✅
- `.env.example` ✅
- `.gitignore` ✅
- `docker-compose.yml` ✅
- `Dockerfile` ✅
- `requirements.txt` ✅

---

## 🧹 Takarítási Terv

### Opció 1: Konzervatív (Biztonságos)
Csak az egyértelműen felesleges fájlok törlése:

```powershell
# Törlendő
Remove-Item STATUS.md
Remove-Item NUMPY_FIX.md
Remove-Item MULTI_PROJECT_DONE.md
Remove-Item MULTILINGUAL_MODEL_DONE.md
Remove-Item -Recurse ui/  # Üres mappa
```

**Eredmény:** -5 fájl, -1 mappa

### Opció 2: Agresszív (Minimális)
Minden nem esszenciális fájl törlése:

```powershell
# Redundáns dokumentáció
Remove-Item STATUS.md
Remove-Item NUMPY_FIX.md
Remove-Item MULTI_PROJECT_DONE.md
Remove-Item MULTILINGUAL_MODEL_DONE.md

# Nem használt/elavult
Remove-Item package.json
Remove-Item health_check.py
Remove-Item test_server.py
Remove-Item setup_rag_windows.ps1
Remove-Item docker-compose.dev.yml

# Examples (ha nem használod)
Remove-Item -Recurse examples/

# Üres mappa
Remove-Item -Recurse ui/
```

**Eredmény:** -13 fájl, -2 mappa

### Opció 3: Archiválás (Biztonságos)
Ne töröld, hanem mozgasd egy `archive/` mappába:

```powershell
# Archive létrehozása
New-Item -ItemType Directory -Path archive -Force

# Áthelyezés
Move-Item STATUS.md archive/
Move-Item NUMPY_FIX.md archive/
Move-Item MULTI_PROJECT_DONE.md archive/
Move-Item MULTILINGUAL_MODEL_DONE.md archive/
Move-Item package.json archive/
Move-Item health_check.py archive/
Move-Item test_server.py archive/
Move-Item setup_rag_windows.ps1 archive/
Move-Item docker-compose.dev.yml archive/
```

**Eredmény:** Minden megmarad, de rendezett

---

## 📊 Jelenlegi vs. Takarított Struktúra

### Előtte (Most)
```
24+ dokumentációs fájl
3 redundáns "DONE" fájl
1 üres mappa (ui/)
4 nem használt utility script
```

### Utána (Opció 1)
```
19 dokumentációs fájl
0 redundáns fájl
0 üres mappa
Tiszta struktúra ✅
```

---

## 💡 Ajánlás

**Javasolt: Opció 1 (Konzervatív)**

```powershell
# Futtasd ezt:
Remove-Item STATUS.md -Force
Remove-Item NUMPY_FIX.md -Force
Remove-Item MULTI_PROJECT_DONE.md -Force
Remove-Item MULTILINGUAL_MODEL_DONE.md -Force
Remove-Item -Recurse ui/ -Force

Write-Host "✅ Takarítás kész! -5 felesleges fájl törölve" -ForegroundColor Green
```

**Miért?**
- ✅ Biztonságos (csak egyértelmű duplikátumok)
- ✅ Gyors
- ✅ Nem veszít fontos információt
- ✅ Megtartja az összes működő funkciót

---

## ⚠️ NE Töröld Ezeket!

- ❌ `.env` - Konfiguráció
- ❌ `src/` - Forráskód
- ❌ `data/` - ChromaDB adatok
- ❌ `logs/` - Logok
- ❌ `config/` - Konfiguráció
- ❌ PowerShell scriptek (`.ps1`)
- ❌ Docker fájlok (`docker-compose.yml`, `Dockerfile`)
- ❌ Core dokumentáció (`README.md`, stb.)

---

## 🎯 Következő Lépés

**Döntsd el:**

1. **Konzervatív takarítás** (ajánlott)
   ```powershell
   # Futtasd:
   Remove-Item STATUS.md, NUMPY_FIX.md, MULTI_PROJECT_DONE.md, MULTILINGUAL_MODEL_DONE.md -Force
   Remove-Item -Recurse ui/ -Force
   ```

2. **Archiválás** (biztonságos)
   ```powershell
   New-Item -ItemType Directory -Path archive -Force
   # Move fájlok...
   ```

3. **Megtartani mindent** (ha bizonytalan vagy)
   - Nincs teendő, minden marad

**Mondd meg, melyiket választod!** 🗑️
