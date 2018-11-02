-- Update model to v1.2
-- Mon Oct 09 10:53:44 2018
-- Source-Model-Version: 1.1
-- Model: Pytatki    Target-Version: 1.2
-- Author: Patryk Niedźwiedziński

USE pytatki;

ALTER TABLE note 
ADD status_id INT NOT NULL DEFAULT 1;
ALTER TABLE note
ADD INDEX fk_note_status1_idx (status_id ASC),
ADD CONSTRAINT fk_note_status_id1 FOREIGN KEY (status_id) REFERENCES status(idstatus);