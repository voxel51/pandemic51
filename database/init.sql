DROP TABLE IF EXISTS streams;
DROP TABLE IF EXISTS stream_history;

CREATE TABLE streams (
    id int(11) NOT NULL AUTO_INCREMENT,
    uuid char(128),
    name varchar(255),
    PRIMARY KEY (`id`)
)
AUTO_INCREMENT=1;

CREATE TABLE stream_history (
    id int(11) NOT NULL AUTO_INCREMENT,
    stream_uuid char(128),
    datetime DATETIME,
    data_path varchar(255),
    labels_path varchar(255),
    PRIMARY KEY (`id`)
)
AUTO_INCREMENT=1;


INSERT INTO streams(uuid, name) VALUES(UUID(), "time_square");
INSERT INTO streams(uuid, name) VALUES(UUID(), "chicago");
