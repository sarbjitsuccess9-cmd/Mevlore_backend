-- Melvore design system v1.6.0 activation (idempotent, non-destructive).
-- The v1.6.0 manifest ships as design-system/live/manifest.json. The API serves whichever of
-- (file, published DB release) has the higher design_version, so no JSON needs importing here.
-- This only makes sure the "live" slot is the active one.
INSERT INTO `app_design_settings` (`setting_key`, `active_design`, `updated_by`)
VALUES ('global', 1, 0)
ON DUPLICATE KEY UPDATE `active_design` = 1, `updated_by` = 0;
