# DATUMBIM WEB REVIT

Professional Web-Based BIM Workstation

## Architecture

- **Frontend**: React / Next.js — Revit-style UI shell
- **Backend**: FastAPI / Python — BIM domain services
- **Database**: SQLAlchemy / Alembic — PostgreSQL-ready, SQLite dev
- **Packages**: Monorepo workspace for shared UI, core, BIM engine, format engine, viewer, SDK manager

## Structure

```
apps/
  web/       — Next.js frontend
  api/       — FastAPI backend
  desktop/   — Electron desktop shell (planned)
packages/
  ui/            — Reusable UI components (Revit-style shell)
  core/          — Shared core utilities
  database/      — Database models, migrations, connection
  bim-engine/    — BIM domain logic, adapters
  sdk-manager/   — SDK registry and discovery
  format-engine/ — File format readers/writers/converters
  viewer/        — 3D viewport / model tree
  shared/        — Cross-cutting shared code
resources/
  external-index/ — Discovered resource registry
```

## Getting Started

```bash
pnpm install
pnpm dev
```

## License

PROPRIETARY — DATUMBIM Confidential
