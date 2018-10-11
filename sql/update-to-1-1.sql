-- Update model to v1.1
-- Mon Sep 26 21:44:44 2018
-- Source-Model-Version: 1.0
-- Model: Pytatki    Target-Version: 1.1

USE pytatki;

DROP VIEW pytatki.note_view;

DROP TABLE IF EXISTS pytatki.note_view;
USE pytatki;
CREATE  OR REPLACE VIEW note_view AS
SELECT a.idnote, a.value, a.title, b.name AS 'note_type', a.user_id AS 'creator_id', d.login AS 'creator_login', a.notegroup_id, c.folder_name AS 'notegroup_name'
FROM note a, note_type b, notegroup_view c, usergroup_membership d
WHERE a.note_type_id = b.idnote_type AND a.user_id = c.iduser AND a.notegroup_id = c.idnotegroup AND d.idusergroup = c.idusergroup;
