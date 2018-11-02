-- Fri Nov  2 09:15:41 2018
-- Name: notegroup_view.sql
-- Author: Patryk Niedźwiedziński
-- Version: 02.00.0000


CREATE
    OR REPLACE VIEW `notegroup_view` AS SELECT
        usergroup_membership.idusergroup,
        usergroup_membership.name,
        notegroup.idnotegroup,
        notegroup.name AS 'folder_name',
        notegroup.parent_id,
        usergroup_membership.iduser
    FROM
        notegroup,
        usergroup_has_notegroup,
        usergroup_membership
    WHERE
        usergroup_membership.idusergroup = usergroup_has_notegroup.usergroup_id
        AND notegroup.idnotegroup = usergroup_has_notegroup.notegroup_id
        AND usergroup_membership.idusergroup = usergroup_has_notegroup.usergroup_id;
