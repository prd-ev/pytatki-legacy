-- Fri Nov  2 09:15:41 2018
-- Name: action_view.sql
-- Author: Patryk Niedźwiedziński
-- Version: 02.00.0000


CREATE
    OR REPLACE VIEW `action_view` AS SELECT
        action.idaction,
        action.content,
        action.user_id,
        user.login AS 'login_user',
        action.note_id,
        note.title,
        action.date
    FROM
        action,
        user,
        note
    WHERE
        action.user_id = user.iduser
        AND action.note_id = note.idnote;
