CREATE TABLE stream_history (
    id int(11) NOT NULL AUTO_INCREMENT,
    stream_name varchar(255),
    datetime DATETIME,
    data_path varchar(255),
    labels_path varchar(255),
    anno_img_path varchar(255),
    count int,
    PRIMARY KEY (`id`)
)
AUTO_INCREMENT=1;
