-- mvlschema core initial migration (PostgreSQL 13+)
\set ON_ERROR_STOP 1

BEGIN;

-- Extensions ---------------------------------------------------------------

CREATE EXTENSION IF NOT EXISTS pgcrypto; -- for gen_random_uuid()

-- ===================== CORE =====================

CREATE TABLE users (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  external_id  uuid UNIQUE,
  first_name   varchar,
  middle_name  varchar,
  last_name    varchar,
  email        text NOT NULL UNIQUE,
  attrib       jsonb NOT NULL DEFAULT '{}'::jsonb,
  data         jsonb NOT NULL DEFAULT '{}'::jsonb,
  contact      varchar,
  active       boolean NOT NULL DEFAULT true,
  created_at   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE projects (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name       varchar NOT NULL,
  code       varchar NOT NULL,
  config     jsonb   NOT NULL DEFAULT '{}'::jsonb,
  active     boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (code)
);

CREATE TABLE access_groups (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name       varchar NOT NULL,
  data       jsonb   NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (name)
);

CREATE TABLE project_access_groups (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id      uuid NOT NULL,
  access_group_id uuid NOT NULL,
  created_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (project_id, access_group_id)
);

CREATE TABLE access_group_members (
  access_group_id uuid NOT NULL,
  user_id         uuid NOT NULL,
  role            text NOT NULL DEFAULT 'member',
  created_at      timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (access_group_id, user_id)
);

CREATE TABLE user_project_roles (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,
  user_id    uuid NOT NULL,
  role       text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (project_id, user_id, role)
);

-- ===================== CATALOG & PIPELINE =====================

CREATE TABLE asset_categories (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,
  name       text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (project_id, name)
);

CREATE TABLE asset_types (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id        uuid NOT NULL,
  asset_category_id uuid NOT NULL,
  name              text NOT NULL,
  created_at        timestamptz NOT NULL DEFAULT now(),
  UNIQUE (project_id, name)
);

CREATE TABLE sequences (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,
  code       text NOT NULL,
  name       text,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (project_id, code)
);

CREATE TABLE assets (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id        uuid NOT NULL,
  asset_category_id uuid NOT NULL,
  asset_type_id     uuid NOT NULL,
  code              text NOT NULL,
  name              text,
  status            text NOT NULL DEFAULT 'new',
  meta              jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at        timestamptz NOT NULL DEFAULT now(),
  UNIQUE (project_id, code)
);

CREATE TABLE shots (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id  uuid NOT NULL,
  sequence_id uuid NOT NULL,
  code        text NOT NULL,
  name        text,
  status      text NOT NULL DEFAULT 'new',
  cutin       double precision,
  cutout      double precision,
  headin      double precision,
  tailout     double precision,
  meta        jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at  timestamptz NOT NULL DEFAULT now(),
  UNIQUE (project_id, code)
);

CREATE TABLE tasks (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id  uuid NOT NULL,
  assignee_id uuid,
  parent_id   uuid,
  asset_id    uuid,
  shot_id     uuid,
  name        text NOT NULL,
  status      text NOT NULL DEFAULT 'todo',
  created_at  timestamptz NOT NULL DEFAULT now(),
  due_at      timestamptz
);

CREATE TABLE product_types (
  id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name   varchar NOT NULL,
  family varchar,
  scope  varchar,
  UNIQUE (name)
);

CREATE TABLE products (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id      uuid NOT NULL,
  asset_id        uuid,
  shot_id         uuid,
  task_id         uuid,
  product_type_id uuid NOT NULL,
  name            varchar NOT NULL,
  status          varchar NOT NULL DEFAULT 'draft',
  user_id         uuid NOT NULL,
  created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE versions (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id uuid NOT NULL,
  version    int  NOT NULL,
  status     varchar NOT NULL DEFAULT 'draft',
  notes      text,
  user_id    uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (product_id, version)
);

CREATE TABLE representations (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  version_id uuid NOT NULL,
  name       varchar,
  ext        varchar NOT NULL,
  path       text    NOT NULL,
  hash       varchar,
  size_bytes bigint  NOT NULL DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Polymorphic links (no strict FKs by design)
CREATE TABLE links (
  id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  link_kind varchar NOT NULL,
  scope     varchar,
  src_kind  varchar NOT NULL,
  src_id    uuid    NOT NULL,
  dst_kind  varchar NOT NULL,
  dst_id    uuid    NOT NULL,
  meta      jsonb   NOT NULL DEFAULT '{}'::jsonb
);

-- ===================== FOREIGN KEYS (CORE) =====================

-- catalog / pipeline
ALTER TABLE asset_categories
  ADD CONSTRAINT fk_asset_categories_project
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;

ALTER TABLE asset_types
  ADD CONSTRAINT fk_asset_types_project
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  ADD CONSTRAINT fk_asset_types_category
    FOREIGN KEY (asset_category_id) REFERENCES asset_categories(id) ON DELETE CASCADE;

ALTER TABLE sequences
  ADD CONSTRAINT fk_sequences_project
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;

ALTER TABLE assets
  ADD CONSTRAINT fk_assets_project
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  ADD CONSTRAINT fk_assets_category
    FOREIGN KEY (asset_category_id) REFERENCES asset_categories(id) ON DELETE RESTRICT,
  ADD CONSTRAINT fk_assets_type
    FOREIGN KEY (asset_type_id) REFERENCES asset_types(id) ON DELETE RESTRICT;

ALTER TABLE shots
  ADD CONSTRAINT fk_shots_project
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  ADD CONSTRAINT fk_shots_sequence
    FOREIGN KEY (sequence_id) REFERENCES sequences(id) ON DELETE CASCADE;

ALTER TABLE tasks
  ADD CONSTRAINT fk_tasks_project
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  ADD CONSTRAINT fk_tasks_assignee
    FOREIGN KEY (assignee_id) REFERENCES users(id) ON DELETE SET NULL,
  ADD CONSTRAINT fk_tasks_parent
    FOREIGN KEY (parent_id) REFERENCES tasks(id) ON DELETE SET NULL,
  ADD CONSTRAINT fk_tasks_asset
    FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE SET NULL,
  ADD CONSTRAINT fk_tasks_shot
    FOREIGN KEY (shot_id) REFERENCES shots(id) ON DELETE SET NULL;

ALTER TABLE products
  ADD CONSTRAINT fk_products_project
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  ADD CONSTRAINT fk_products_asset
    FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE SET NULL,
  ADD CONSTRAINT fk_products_shot
    FOREIGN KEY (shot_id) REFERENCES shots(id) ON DELETE SET NULL,
  ADD CONSTRAINT fk_products_task
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL,
  ADD CONSTRAINT fk_products_type
    FOREIGN KEY (product_type_id) REFERENCES product_types(id) ON DELETE RESTRICT,
  ADD CONSTRAINT fk_products_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT;

ALTER TABLE versions
  ADD CONSTRAINT fk_versions_product
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  ADD CONSTRAINT fk_versions_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT;

ALTER TABLE representations
  ADD CONSTRAINT fk_representations_version
    FOREIGN KEY (version_id) REFERENCES versions(id) ON DELETE CASCADE;

-- ===================== INDEXES (CORE) =====================

CREATE INDEX idx_auth_identities_provider_id ON auth_identities(provider_id);
CREATE INDEX idx_auth_identities_user_id     ON auth_identities(user_id);
CREATE INDEX idx_auth_credentials_user_id    ON auth_credentials(user_id);
CREATE INDEX idx_auth_mfa_user_id            ON auth_mfa_totp(user_id);
CREATE INDEX idx_auth_sessions_user_id       ON auth_sessions(user_id);
CREATE INDEX idx_password_resets_user_id     ON password_resets(user_id);
CREATE INDEX idx_email_verifications_user_id ON email_verifications(user_id);

CREATE INDEX idx_proj_acc_groups_project_id  ON project_access_groups(project_id);
CREATE INDEX idx_proj_acc_groups_group_id    ON project_access_groups(access_group_id);
CREATE INDEX idx_acc_group_members_group_id  ON access_group_members(access_group_id);
CREATE INDEX idx_acc_group_members_user_id   ON access_group_members(user_id);
CREATE INDEX idx_user_project_roles_project  ON user_project_roles(project_id);
CREATE INDEX idx_user_project_roles_user     ON user_project_roles(user_id);

CREATE INDEX idx_asset_categories_project_id ON asset_categories(project_id);
CREATE INDEX idx_asset_types_project_id      ON asset_types(project_id);
CREATE INDEX idx_asset_types_category_id     ON asset_types(asset_category_id);
CREATE INDEX idx_sequences_project_id        ON sequences(project_id);

CREATE INDEX idx_assets_project_id           ON assets(project_id);
CREATE INDEX idx_assets_category_id          ON assets(asset_category_id);
CREATE INDEX idx_assets_type_id              ON assets(asset_type_id);

CREATE INDEX idx_shots_project_id            ON shots(project_id);
CREATE INDEX idx_shots_sequence_id           ON shots(sequence_id);

CREATE INDEX idx_tasks_project_id            ON tasks(project_id);
CREATE INDEX idx_tasks_assignee_id           ON tasks(assignee_id);
CREATE INDEX idx_tasks_asset_id              ON tasks(asset_id);
CREATE INDEX idx_tasks_shot_id               ON tasks(shot_id);

CREATE INDEX idx_products_project_id         ON products(project_id);
CREATE INDEX idx_products_asset_id           ON products(asset_id);
CREATE INDEX idx_products_shot_id            ON products(shot_id);
CREATE INDEX idx_products_task_id            ON products(task_id);
CREATE INDEX idx_products_type_id            ON products(product_type_id);
CREATE INDEX idx_products_user_id            ON products(user_id);

CREATE INDEX idx_versions_product_id         ON versions(product_id);
CREATE INDEX idx_versions_user_id            ON versions(user_id);

CREATE INDEX idx_representations_version_id  ON representations(version_id);

COMMIT;
