-- tab_label must be a lowercase snake_case key (enforced by G2PRegisterUITab's
-- ORM validator in openg2p_registry_core/models/g2p_register_tab.py: pattern
-- ^[a-z][a-z0-9_]*$). It doubles as a translation key — see the matching
-- entries added to registry_languages.sql's core_translation for the
-- human-readable text ("Farmer", "Livestock", "Health & Vaccination", etc).
-- Using tab_id itself as the label (same convention as the reference
-- extension's g2p_register_ui_tabs.sql) keeps each key unique.
INSERT INTO "public"."g2p_register_ui_tabs" ("tab_id","register_id","tab_label","tab_order","is_active") VALUES
('livestock_livestock_tab','997676d3-7008-59f9-b23e-613ad79bbb08','livestock_livestock_tab',0,'TRUE'),
('livestock_animal_tab','997676d3-7008-59f9-b23e-613ad79bbb08','livestock_animal_tab',10,'TRUE'),
('livestock_health_event_tab','997676d3-7008-59f9-b23e-613ad79bbb08','livestock_health_event_tab',20,'TRUE'),
('livestock_vital_event_tab','997676d3-7008-59f9-b23e-613ad79bbb08','livestock_vital_event_tab',30,'TRUE'),
('livestock_import_batch_tab','997676d3-7008-59f9-b23e-613ad79bbb08','livestock_import_batch_tab',40,'TRUE'),
('livestock_farmer_tab','f9c6a359-9563-5a43-b0fe-6c7e452037a3','livestock_farmer_tab',10,'TRUE');
