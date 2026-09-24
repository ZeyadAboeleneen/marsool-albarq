# CLAUDE.md — Execution Instructions

You are implementing **Marsool Al-Barq (مرسول البرق)**, the Al-Barq Quotation System. The plan in `docs/plan/` is the source of truth.
Read `docs/plan/README.md` first, then the files relevant to the current phase.

## Working rules
- Work **one phase at a time** from `docs/plan/08-roadmap.md`. At the end of each phase: run the quality
  gates, report what was done against its Definition of Done, list how the user can verify it manually,
  commit with message `phase-N: <summary>`, then STOP and wait for approval.
- If a decision is not covered by the plan, **ask** instead of guessing. Do not silently change the
  locked decisions in `docs/plan/README.md`. If you believe a decision is wrong, say so and propose.
- Development is local via Docker Compose. Never touch host ports 80/443. When production deployment
  comes (Phase 10), other projects on the server must not be affected.

## Stack (locked)
Python 3.12 · Django 5.2 LTS · PostgreSQL 16 · Redis 7 · Celery · HTMX 2 · Alpine.js 3 ·
Tailwind (standalone CLI) · WeasyPrint · OpenWA (engine whatsapp-web.js) · Docker Compose.
No Node build step for the Django app. HTMX/Alpine/fonts are vendored in `static/`.

## Domain rules
- A quotation is a **price list**: item, unit, unit price. No quantities, no line totals, no grand totals.
- Quote number format default `{prefix}-{year}/{month:02d}-{seq:02d}` (e.g. AB-2026/09-01);
  sequence resets monthly; configurable in OrganizationSettings.
- Sending requires a **self-review gate**: the sending user must have opened the final PDF preview
  (recorded server-side) and ticked the confirmation checkbox. Enforced in the backend, not only the UI.
- WhatsApp sender number: 01000967017 (configured through settings UI, never hardcoded).
- PDF layout reference: `docs/plan/assets/reference-quotation.pdf`. Colors/fonts: `docs/plan/seed/brand.json`.

## Non-negotiable conventions
- Every operational model inherits `TenantScopedModel`. Views query via `.for_org(request.organization)`.
  Never `Model.objects.all()` in views. Add a cross-tenant access test for every new view.
- Money is `Decimal(12,2)`. No floats.
- Phone numbers stored E.164 via `phonenumbers` (default region EG).
- Finalized quotations are immutable; changes create a revision.
- Quote numbers generated inside `transaction.atomic()` with `select_for_update()` on `QuoteSequence`.
- Permission checks in views via `@require_perm(...)`, never only in templates.
- Secrets only from environment (`.env`, never committed; provide `.env.example`).
  SMTP/OpenWA credentials stored in DB are Fernet-encrypted.
- Private files (PDFs, logos) served via permission-checked view (`FileResponse` locally,
  `X-Accel-Redirect` in production).
- UI is Arabic RTL; user-facing strings wrapped for i18n (`gettext`).
- Arabic search normalizes: أ/إ/آ→ا, ة→ه, ى→ي, removes tatweel and diacritics.

## Quality gates per phase
- `ruff check` clean, `pytest` green, migrations committed, no TODOs left in phase scope.
- New models registered in Django admin (superuser emergency access only).

## Seed data
- `python manage.py import_products docs/plan/seed/products.csv --org albarq` (idempotent upsert)
- `docs/plan/seed/brand.json` → initial Organization + OrganizationSettings for `albarq`.
