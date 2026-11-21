# Melvore PHP 8.3 Customer App Experience API (`/php_api`)

## Overview
Drop-in PHP 8.3 + PDO (`MySQL` / `MariaDB`) REST API modules built for `https://app.melvore.co.in` sharing database `u205121999_melvore` and media root `https://melvore.co.in` without duplicating existing auth, cart, order, or payment logic.

## Server Prerequisites
1. Execute `melvore_customer_app_experience_migration.sql` against `u205121999_melvore` after exporting a full phpMyAdmin SQL backup.
2. Optionally run `sql/melvore_experience_companion_indexes.sql` for hot search/review/personalization query indexes.
3. Configure `.env` in `/php_api/` (same directory level as existing `config/env.php` reads):
   - `DB_HOST`, `DB_NAME=u205121999_melvore`, `DB_USER`, `DB_PASS`, `DB_CHARSET=utf8mb4`
   - `AUTH_TOKEN_SECRET` (matching existing HMAC token signing secret in `/api/auth/*.php`)
   - `STOREFRONT_BASE_URL=https://melvore.co.in`
   - `UPLOAD_ROOT_DIR` (writable upload folder, e.g., `/home/u.../public_html/uploads`)
   - `UPLOAD_PUBLIC_PREFIX=/uploads`
   - `MAIL_FROM_ADDRESS=noreply@melvore.co.in`
4. Ensure `UPLOAD_ROOT_DIR/reviews` and `UPLOAD_ROOT_DIR/support` are writable (`0755`) and PHP `fileinfo` extension is enabled.

## Implemented Endpoints
- `GET /api/home/feed.php` — Hero slider, regional/scheduled active campaigns (`app_campaigns`), quick categories, dynamic homepage sections (`app_home_sections`), placements (`app_product_placements`), and initial discovery grid.
- `GET /api/categories/list.php`, `GET /api/categories/details.php`
- `GET /api/brands/list.php`, `GET /api/brands/details.php`, `POST /api/brands/view.php`
- `GET /api/products/list.php`, `GET /api/products/details.php`, `GET /api/products/recommendations.php`, `GET /api/products/recently_viewed.php`
- `GET /api/search/query.php`, `GET /api/search/suggestions.php`
- `GET /api/styles/list.php`, `GET /api/styles/details.php`, `POST /api/styles/signal.php`
- `GET /api/videos/feed.php`, `GET /api/videos/details.php`, `POST /api/videos/event.php`
- `GET /api/elite/home.php`, `GET /api/elite/pack.php`
- `GET /api/personalization/for_you.php`
- `GET /api/delivery/check.php`
- `GET /api/reviews/list.php`, `POST /api/reviews/request_otp.php`, `POST /api/reviews/verify_otp.php`, `POST /api/reviews/create.php`, `POST /api/reviews/helpful.php`, `POST /api/reviews/upload_media.php`
- `GET /api/help/topics.php`, `GET /api/help/flow.php`, `POST /api/help/session.php`, `POST /api/support/upload_media.php`

## Design manifest endpoint (added)
`GET /api/design/manifest.php?slot=live|default` returns `{manifest, manifest_hash, asset_base_url}` with ETag/304 support.
Manifest asset paths (e.g. `/design-system/assets/svg/worlds_v3/<world>/layouts/home.svg`) are served statically; the app prefixes them with `asset_base_url` (falls back to the API host).

## Setup notes
- Copy `.env.example` to `.env` on the server and fill the values. **Never commit `.env`.**
- PHP service classes live in `services/` (they were previously nested under `docs/services/`).
- Import SQL in order: `sql/migrations/002_*.sql`, then `sql/seeds/002_*.sql`.
