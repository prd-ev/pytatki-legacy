USE pytatki_backup;

ALTER VIEW note_view AS
SELECT a.idnote, a.value, a.title, a.status_id, b.name AS 'note_type', a.user_id AS 'creator_id', d.login AS 'creator_login', a.notegroup_id, c.folder_name AS 'notegroup_name'
FROM note a, note_type b, notegroup_view c, usergroup_membership d
WHERE a.note_type_id = b.idnote_type AND a.user_id = c.iduser AND c.iduser = d.iduser AND a.notegroup_id = c.idnotegroup AND d.idusergroup = c.idusergroup;