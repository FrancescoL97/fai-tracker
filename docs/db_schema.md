# SQLite schema (design)

This document describes the database schema and the core SQL queries used by the application (MVP).

## Table: fai_records

```sql
CREATE TABLE IF NOT EXISTS fai_records (
  id           TEXT PRIMARY KEY,           -- UUID (string)
  pn           TEXT NOT NULL,               -- Part Number
  issue_year   INTEGER NOT NULL,            -- YYYY
  issue_month  INTEGER NOT NULL,            -- 1-12
  folder_name  TEXT NOT NULL,               -- FAI_YYYY-MM_(PN) or ..._OLD.n
  path         TEXT NOT NULL,               -- full path to the FAI folder
  location     TEXT NOT NULL CHECK (location IN ('ACTIVE','ARCHIVED')),
  old_version  INTEGER,                     -- NULL if ACTIVE, 1..n if ARCHIVED
  created_at   TEXT NOT NULL,               -- ISO timestamp
  updated_at   TEXT NOT NULL,               -- ISO timestamp
  archived_at  TEXT                         -- ISO timestamp, only for ARCHIVED
);

-- At most 1 ACTIVE per PN
CREATE UNIQUE INDEX IF NOT EXISTS ux_active_per_pn
ON fai_records(pn)
WHERE location = 'ACTIVE';

-- Search indexes
CREATE INDEX IF NOT EXISTS ix_records_pn
ON fai_records(pn);

CREATE INDEX IF NOT EXISTS ix_records_issue
ON fai_records(issue_year, issue_month);
```
## Core queries
### Get ACTIVE record by PN
``` sql
SELECT *
FROM fai_records
WHERE pn = :pn AND location = 'ACTIVE'
LIMIT 1;
```
### Get all records by PN (ACTIVE + ARCHIVED)
``` sql
SELECT *
FROM fai_records
WHERE pn = :pn
ORDER BY
  CASE location WHEN 'ACTIVE' THEN 0 ELSE 1 END,
  issue_year DESC, issue_month DESC,
  COALESCE(old_version, 0) DESC;
```
### Compute next OLD version number (for ARCHIVED)
```sql
SELECT COALESCE(MAX(old_version), 0) + 1 AS next_old
FROM fai_records
WHERE pn = :pn AND location = 'ARCHIVED';
```
### Insert new ACTIVE record
```sql
INSERT INTO fai_records (
  id, pn, issue_year, issue_month, folder_name, path,
  location, old_version, created_at, updated_at, archived_at
) VALUES (
  :id, :pn, :yy, :mm, :folder_name, :path,
  'ACTIVE', NULL, :now, :now, NULL
);
```
### Archive an existing ACTIVE record (becomes ARCHIVED + old_version)
```sql
UPDATE fai_records
SET
  location = 'ARCHIVED',
  old_version = :old_version,
  folder_name = :arch_folder_name,
  path = :arch_path,
  archived_at = :now,
  updated_at = :now
WHERE id = :id_active;
```
### Update timestamp (overwrite case)
```sql
UPDATE fai_records
SET updated_at = :now
WHERE id = :id_active;
```
## Notes
Expiry date and status (VALID / EXPIRING_SOON / EXPIRED) are derived from issue_year and issue_month and are not persisted in the DB for the MVP.

The application uses two configured root folders: ACTIVE_ROOT and ARCHIVE_ROOT. The path column always points to the current folder location.