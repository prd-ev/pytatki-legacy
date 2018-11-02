-- Fri Nov  2 09:15:41 2018
-- Name: usergroup_membership.sql
-- Author: Patryk Niedźwiedziński
-- Version: 02.00.0000


CREATE
    OR REPLACE VIEW `usergroup_membership` AS SELECT
        user.iduser,
        user.login,
        usergroup.idusergroup,
        usergroup.name,
        usergroup.color,
        usergroup.description,
        usergroup.image_path
    FROM
        user,
        usergroup,
        user_membership
    WHERE
        user.iduser = user_membership.user_id
        AND usergroup.idusergroup = user_membership.usergroup_id;