-- Fri Nov  2 09:15:41 2018
-- Name: user_view.sql
-- Author: Patryk Niedźwiedziński
-- Version: 02.00.0000


CREATE
    OR REPLACE VIEW `user_view` AS SELECT
        user.*,
        status.name AS 'status_name'
    FROM
        user,
        status
    WHERE
        user.status_id = status.idstatus;
