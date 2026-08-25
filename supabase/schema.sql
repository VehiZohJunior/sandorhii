-- SandorHii - schema Postgres (Supabase)
-- Genere a partir du blueprint d'architecture (Phase 0).
-- Les tables marquees "Phase 2+" n'ont pas encore de code cote backend :
-- elles sont creees a l'avance pour que la base soit prete quand ces
-- phases commencent, mais restent vides tant que le module correspondant
-- n'existe pas.

create extension if not exists "pgcrypto";

-- ============================================================
-- Phase 1 - utilise des maintenant
-- ============================================================

create table if not exists submissions (
  id uuid primary key default gen_random_uuid(),
  content_type text not null default 'texte' check (content_type in ('texte', 'url', 'image', 'video')),
  raw_content text not null,
  content_hash text not null unique,
  language text not null default 'fr',
  status text not null default 'nouveau'
    check (status in ('nouveau', 'analyse', 'en_attente_validation', 'publie', 'rejete')),
  created_at timestamptz not null default now()
);
create index if not exists idx_submissions_status on submissions (status);
create index if not exists idx_submissions_hash on submissions (content_hash);

create table if not exists linguistic_analyses (
  id uuid primary key default gen_random_uuid(),
  submission_id uuid not null unique references submissions (id) on delete cascade,
  score numeric not null,
  suggested_level text not null,
  signals jsonb not null default '[]',
  stats jsonb not null default '{}',
  model_version text not null,
  language_supported boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists fact_checks (
  id uuid primary key default gen_random_uuid(),
  submission_id uuid not null unique references submissions (id) on delete cascade,
  verdict text not null check (verdict in ('vrai', 'faux', 'partiellement_vrai', 'non_verifiable', 'trompeur')),
  global_score numeric not null,
  resume text not null,
  auteur text not null,
  statut text not null default 'brouillon' check (statut in ('brouillon', 'publie')),
  created_at timestamptz not null default now(),
  published_at timestamptz
);
create index if not exists idx_fact_checks_statut on fact_checks (statut, published_at desc);

-- ============================================================
-- Phase 2+ - reservees, pas encore utilisees par le backend
-- ============================================================

create table if not exists media_analyses (
  id uuid primary key default gen_random_uuid(),
  submission_id uuid not null unique references submissions (id) on delete cascade,
  score numeric,
  source_credibility_score numeric,
  reverse_search_results jsonb default '[]',
  deepfake_score numeric,
  created_at timestamptz not null default now()
);

create table if not exists tech_analyses (
  id uuid primary key default gen_random_uuid(),
  submission_id uuid not null unique references submissions (id) on delete cascade,
  score numeric,
  bot_network_score numeric,
  ai_generated_score numeric,
  metadata jsonb default '{}',
  created_at timestamptz not null default now()
);

create table if not exists sources (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  url text,
  credibility_score numeric,
  country text,
  language text,
  history jsonb default '[]',
  created_at timestamptz not null default now()
);

create table if not exists themes (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  category text
);

create table if not exists fact_check_sources (
  fact_check_id uuid not null references fact_checks (id) on delete cascade,
  source_id uuid not null references sources (id) on delete cascade,
  primary key (fact_check_id, source_id)
);

create table if not exists fact_check_themes (
  fact_check_id uuid not null references fact_checks (id) on delete cascade,
  theme_id uuid not null references themes (id) on delete cascade,
  primary key (fact_check_id, theme_id)
);

create table if not exists veille_signals (
  id uuid primary key default gen_random_uuid(),
  source_type text not null,
  raw_data jsonb not null default '{}',
  virality_score numeric,
  priority_score numeric,
  detected_at timestamptz not null default now(),
  linked_submission_id uuid references submissions (id) on delete set null
);

create table if not exists reports (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  content_text text,
  content_url text,
  reason text,
  status text not null default 'nouveau' check (status in ('nouveau', 'examine', 'ferme')),
  created_at timestamptz not null default now()
);

-- ============================================================
-- Phase 4 (auth reelle) - Supabase fournit deja auth.users.
-- Cette table de profils sera activee quand le back-office
-- passera du mot de passe partage a de vrais comptes.
-- ============================================================

create table if not exists profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  role text not null default 'lecteur' check (role in ('lecteur', 'fact_checkeur', 'moderateur', 'admin')),
  langue text not null default 'fr',
  streak_count integer not null default 0,
  created_at timestamptz not null default now()
);
