-- Fri Nov  2 09:15:41 2018
-- Name: note_tags.sql
-- Author: Patryk Niedźwiedziński
-- Version: 02.00.0000


CREATE
    OR REPLACE VIEW `note_tags` AS SELECT
        note.idnote,
        tagging.tag_id,
        tag.name AS 'tag_name'
    FROM
        tagging,
        note,
        tag
    WHERE
        tagging.note_id = note.idnote
        AND tagging.tag_id = tag.idtag;
