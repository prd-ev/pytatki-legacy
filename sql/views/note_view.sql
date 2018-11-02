-- Fri Nov  2 09:15:41 2018
-- Name: note_view.sql
-- Author: Patryk Niedźwiedziński
-- Version: 02.00.0000


CREATE
    OR REPLACE VIEW `note_view` AS SELECT
        note.idnote,
        note.value,
        note.title,
        note.status_id,
        note_type.name AS 'note_type',
        note.user_id AS 'creator_id',
        usergroup_membership.login AS 'creator_login',
        note.notegroup_id, c.folder_name AS 'notegroup_name'
    FROM
        note,
        note_type note_type,
        notegroup_view,
        usergroup_membership
    WHERE
        note.note_type_id = note_type.idnote_type
        AND note.user_id = notegroup_view.iduser
        AND note.notegroup_id = notegroup_view.idnotegroup
        AND usergroup_membership.idusergroup = notegroup_view.idusergroup;
