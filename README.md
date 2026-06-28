# UniPath Ghana

AI-powered university admission, course recommendation, and career guidance platform for SHS students in Ghana.

This is a **monorepo**: `backend/` (Flask + MongoDB Atlas) and `frontend/` (React + Tailwind + shadcn/ui).

## Core principle

> Recommendation and admission logic is **fully deterministic and rule-based**. AI is used **only** to explain results in friendlier language — never to decide scores, ranks, or admission outcomes, and never to invent cut-offs or course facts.

See `backend/app/services/ai_layer/guardrails.py` for the enforced rules.

---

## Project structure

```
unipath-ghana/
├── backend/                  Flask API
│   ├── app/
│   │   ├── config/           Settings + MongoDB Atlas connection
│   │   ├── models/            MongoDB document models (12 collections)
│   │   ├── routes/            API endpoints (blueprints)
│   │   ├── schemas/           Marshmallow request validation
│   │   ├── services/
│   │   │   ├── recommendation_engine/   Deterministic scoring (Steps 1-4)
│   │   │   ├── admission_engine/        Cut-off comparison, trends, Safe/Competitive/Reach
│   │   │   └── ai_layer/                Guardrailed AI explanation layer
│   │   ├── middleware/        RBAC + premium-tier gating
│   │   └── utils/             Validators, error handlers
│   ├── data/seed/             Placeholder seed JSON (courses, universities, cut-offs)
│   ├── scripts/               seed_database.py
│   ├── tests/                 pytest unit + integration tests
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
│
├── frontend/                  React app
│   ├── src/
│   │   ├── components/        UI components (onboarding, dashboard, charts, etc.)
│   │   ├── pages/              Route-level pages
│   │   ├── context/            Auth, Theme, StudentProfile (React Context)
│   │   ├── services/           Axios API clients per domain
│   │   ├── routes/             ProtectedRoute wrapper
│   │   ├── constants/          Shared dropdown options (mirrors backend choices)
│   │   └── lib/                cn() utility for Tailwind/shadcn
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── components.json        shadcn/ui config
│
└── .gitignore
```

---

## Getting started

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env: add your MongoDB Atlas URI, JWT secrets, Anthropic API key

python scripts/seed_database.py   # loads placeholder seed data
python run.py                      # starts on http://localhost:5000
```

### 2. Frontend

```bash
cd frontend
npm install

cp .env.example .env
npm run dev                        # starts on http://localhost:5173
```

The Vite dev server proxies `/api/*` to `http://localhost:5000` (see `vite.config.js`), so the frontend and backend talk to each other out of the box in development.

### 3. shadcn/ui components

The `components.json` is already configured. To add more shadcn components beyond the included `button` and `card`:

```bash
cd frontend
npx shadcn@latest add dialog dropdown-menu select tabs
```

---

## MongoDB Atlas setup

1. Create a free cluster at https://www.mongodb.com/cloud/atlas
2. Create a database user and allow your IP (or `0.0.0.0/0` for dev)
3. Copy the connection string into `backend/.env` as `MONGO_URI`
4. Run `python scripts/seed_database.py` to populate placeholder data

**Important:** seed data in `backend/data/seed/*.json` is illustrative only — replace it with verified cut-off points and course/university data sourced from official Ghanaian admissions bodies before using this in production. The whole "no hallucination" guarantee depends on the database only ever holding verified facts.

---

## Recommendation flow (deterministic)

1. **Grade Conversion** (`grade_converter.py`) — WASSCE letters → numeric (A1=1 ... F9=9)
2. **Weighted Scoring** (`engine.py`) — Academic 40% / Interest 25% / Skills 20% / Career 15%
3. **Admission Classification** (`admission_classifier.py`) — compares aggregate vs. DB cut-offs → Safe/Competitive/Reach
4. **Explanation Generation** (`explanation_generator.py`) — rule-based bullet points from the scores above
5. **AI Layer** (`ai_layer/explainer.py`) — *optionally* rephrases step 4's bullet points in friendlier prose; never adds new facts

All of steps 1-4 are covered by unit tests in `backend/tests/unit/`.

---

## Business model tiers

| Feature | Free | Premium |
|---|---|---|
| Course recommendations | ✅ (top 10) | ✅ |
| Admission likelihood | ✅ | ✅ |
| Comparisons | Limited (3 items) | Unlimited |
| AI chat advisor | ❌ | ✅ |
| What-if simulator | ❌ | ✅ |
| PDF reports | ❌ | ✅ |
| Career roadmap | ❌ | ✅ |

Enforced server-side via `app/middleware/rbac.py` (`@premium_required`).
