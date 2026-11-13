# TerangaFlow

Plateforme intelligente de supervision des opérations logistiques pour les ONG et organisations humanitaires.

> **Phase 1 — Fondations.** Ce dépôt contient le socle technique : le frontend React, l'API FastAPI, le schéma PostgreSQL (Supabase), les migrations, les données de démonstration et le premier layout du dashboard.
> Il n'y a encore ni authentification, ni CRUD, ni moteur de risques, ni IA, ni GPS.

## Stack

| Couche | Technologies |
|---|---|
| Frontend | React 19, TypeScript, Vite 8, Tailwind CSS 4, React Router 8, client `fetch` typé |
| Backend | Python 3.12+, FastAPI, Pydantic v2 / pydantic-settings, SQLAlchemy 2, Alembic |
| Base de données | PostgreSQL via Supabase (driver `psycopg` 3) |

## Arborescence

```text
TerangaFlow/
├── frontend/                 # Application React (Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/       # AppLayout, Sidebar, Header, navigation
│   │   │   ├── dashboard/    # KpiCard, RecentDeliveries, InventoryStatus, RecentRiskAlerts
│   │   │   └── ui/           # Card, Badge, Icon
│   │   ├── pages/            # Overview, placeholders, 404
│   │   ├── services/         # apiClient (fetch), healthService
│   │   ├── hooks/            # useApiHealth
│   │   ├── types/            # Types API et domaine
│   │   ├── data/             # Données de démonstration statiques (simulées)
│   │   ├── utils/            # env, formatage
│   │   ├── App.tsx           # Routeur
│   │   └── main.tsx
│   └── .env.example
├── backend/
│   ├── app/
│   │   ├── api/v1/           # Routes versionnées (health)
│   │   ├── core/             # Config (pydantic-settings), erreurs, logging
│   │   ├── db/               # Base déclarative, engine & sessions
│   │   ├── models/           # Modèles SQLAlchemy + ENUMs
│   │   ├── schemas/          # Schémas Pydantic
│   │   └── main.py           # Application FastAPI
│   ├── alembic/              # Migrations
│   ├── scripts/              # seed.py + seed_data.py (données simulées)
│   ├── tests/
│   ├── requirements.txt      # Dépendances d'exécution
│   ├── requirements-dev.txt  # + pytest, httpx2, ruff
│   └── .env.example
├── docs/data-model.md        # Description du schéma
└── README.md
```

## Prérequis

- **Node.js** ≥ 22.22 (testé avec Node 24) et npm
- **Python** ≥ 3.12 (testé avec 3.13)
- Un projet **Supabase**, ou n'importe quel PostgreSQL ≥ 13

---

## 1. Backend (FastAPI)

```bash
cd backend
python -m venv .venv

# Activer l'environnement
# Windows (PowerShell) :  .venv\Scripts\Activate.ps1
# Windows (Git Bash)   :  source .venv/Scripts/activate
# macOS / Linux        :  source .venv/bin/activate

pip install -r requirements-dev.txt     # ou requirements.txt en production
cp .env.example .env                   # puis renseigner DATABASE_URL
uvicorn app.main:app --reload --port 8000
```

| URL | Description |
|---|---|
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc |
| http://localhost:8000/api/v1/openapi.json | Schéma OpenAPI |
| http://localhost:8000/api/v1/health | Liveness de l'API |
| http://localhost:8000/api/v1/health/database | Connectivité PostgreSQL (`SELECT version()`) |

L'API démarre même sans `DATABASE_URL`. Dans ce cas, `/health/database` répond `503` avec `"status": "unavailable"`.

### Configurer Supabase

1. Dans Supabase, ouvrir **Project → Connect → Connection string (URI)**.
2. Choisir **Session pooler** (port `5432`, compatible IPv4). C'est le mode recommandé pour l'API et pour Alembic.
3. Copier l'URI dans `backend/.env` en remplaçant le mot de passe :

   ```env
   DATABASE_URL=postgresql://postgres.<project-ref>:<password>@aws-0-<region>.pooler.supabase.com:5432/postgres?sslmode=require
   ```

   Les caractères spéciaux du mot de passe doivent être encodés en URL (`@` → `%40`, `#` → `%23`…).
4. Vérifier la connexion : `curl http://localhost:8000/api/v1/health/database` doit répondre `"status": "ok"`.

Le **transaction pooler** (port `6543`) est détecté automatiquement : le pool côté client et les prepared statements sont alors désactivés.

### Migrations (Alembic)

Toujours lancer depuis `backend/`, avec le venv activé. L'URL est lue dans `DATABASE_URL` et n'est jamais écrite dans `alembic.ini`.

```bash
alembic upgrade head                       # crée le schéma (8 tables, 10 ENUMs)
alembic current                            # révision appliquée
alembic check                              # vérifie que les modèles et la base sont alignés
alembic downgrade -1                       # annule la dernière migration
alembic upgrade head --sql                 # affiche le SQL sans se connecter
alembic revision --autogenerate -m "..."   # nouvelle migration après une modification des modèles
```

### Données de démonstration (seed)

```bash
python -m scripts.seed
```

- Le script charge une **organisation fictive** (« Alliance Humanitaire Teranga ») avec :
  - 4 entrepôts (Dakar, Thiès, Kaolack, Tambacounda) ;
  - 9 points de distribution (dont Kaffrine, Koungheul, Mbour, Diourbel, Goudiry, Bakel) ;
  - 13 lignes de stock et 26 mouvements ;
  - 10 véhicules ;
  - **18 livraisons** : 7 livrées, 5 en transit, 3 en retard, 1 en chargement, 1 planifiée, 1 annulée ;
  - 6 alertes de risque.
- **Toutes ces données sont simulées.** Seules les localités et leurs coordonnées sont réelles.
- Le script est **réexécutable** : chaque ligne est insérée ou mise à jour selon sa clé naturelle (`INSERT … ON CONFLICT DO UPDATE`), dans une seule transaction, sans doublon. Les dates sont relatives au jour de l'exécution.
- Les soldes de stock correspondent exactement à la somme des mouvements.

### Tests et lint

```bash
pytest                       # 12 tests ; le test de connexion live est ignoré par défaut
TEST_DATABASE_URL=postgresql://... pytest   # active aussi le test live sur une vraie base
ruff check                   # lint (config dans pyproject.toml)
```

---

## 2. Frontend (React + Vite)

```bash
cd frontend
npm install
cp .env.example .env.local   # optionnel : les valeurs par défaut visent http://localhost:8000
npm run dev                  # http://localhost:5173
```

| Commande | Rôle |
|---|---|
| `npm run dev` | Serveur de développement |
| `npm run build` | Vérification TypeScript + build de production (`dist/`) |
| `npm run preview` | Sert le build de production |
| `npm run lint` | Lint (oxlint) |

| Variable | Défaut | Rôle |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000/api/v1` | URL de base de l'API |
| `VITE_API_TIMEOUT_MS` | `10000` | Timeout des requêtes |

Le header affiche l'état de l'API (`GET /health`, vérifié toutes les 30 s). Les chiffres de la page Overview sont des **données statiques de démonstration**, signalées comme telles dans l'interface. Ils reprennent le jeu de données du seed.

---

## Variables d'environnement backend

Voir `backend/.env.example`, qui documente chaque variable.

| Variable | Obligatoire | Défaut |
|---|---|---|
| `DATABASE_URL` | pour les fonctions BDD | — |
| `APP_ENV` | non | `development` |
| `LOG_LEVEL` | non | `INFO` |
| `CORS_ORIGINS` | non | `http://localhost:5173,http://127.0.0.1:5173` |
| `DB_POOL_SIZE` / `DB_MAX_OVERFLOW` / `DB_POOL_TIMEOUT` / `DB_POOL_RECYCLE` / `DB_CONNECT_TIMEOUT` | non | `5` / `5` / `30` / `1800` / `10` |
| `DB_ECHO` | non | `false` |

## Format des erreurs API

Toutes les erreurs suivent la même enveloppe, dupliquée côté frontend dans `frontend/src/types/api.ts` :

```json
{ "error": { "code": "not_found", "message": "Not Found", "details": null } }
```

## Démarrage rapide (2 terminaux)

```bash
# Terminal 1
cd backend && source .venv/Scripts/activate && uvicorn app.main:app --reload
# Terminal 2
cd frontend && npm run dev
```
