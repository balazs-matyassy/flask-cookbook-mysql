DROP TABLE IF EXISTS `image`;
DROP TABLE IF EXISTS `ingredient`;
DROP TABLE IF EXISTS `recipe`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `role`;

CREATE TABLE `role`
(
    `id`   INT          NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE (`name`)
);

CREATE TABLE `user`
(
    `id`          INT          NOT NULL AUTO_INCREMENT,
    `username`    VARCHAR(255) NOT NULL,
    `password`    VARCHAR(255) NOT NULL,
    `role_id`     INT          NOT NULL,
    `created_at`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_by`  INT,
    `modified_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `modified_by` INT,
    PRIMARY KEY (`id`),
    UNIQUE (`username`),
    FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
    FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
    FOREIGN KEY (`modified_by`) REFERENCES `user` (`id`)
);

CREATE TABLE `category`
(
    `id`          INT          NOT NULL AUTO_INCREMENT,
    `name`        VARCHAR(255) NOT NULL,
    `description` TEXT         NOT NULL,
    `created_at`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_by`  INT          NOT NULL,
    `modified_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `modified_by` INT          NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE (`name`),
    FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
    FOREIGN KEY (`modified_by`) REFERENCES `user` (`id`)
);

CREATE TABLE `recipe`
(
    `id`          INT          NOT NULL AUTO_INCREMENT,
    `category_id` INT          NOT NULL,
    `name`        VARCHAR(255) NOT NULL,
    `description` TEXT         NOT NULL,
    `difficulty`  INT          NOT NULL,
    `owned_by`    INT          NOT NULL,
    `created_at`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_by`  INT          NOT NULL,
    `modified_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `modified_by` INT          NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
    FOREIGN KEY (`owned_by`) REFERENCES `user` (`id`),
    FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
    FOREIGN KEY (`modified_by`) REFERENCES `user` (`id`)
);

CREATE TABLE `ingredient`
(
    `id`          INT          NOT NULL AUTO_INCREMENT,
    `recipe_id`   INT          NOT NULL,
    `name`        VARCHAR(255) NOT NULL,
    `quantity`    INT          NOT NULL DEFAULT 0,
    `unit`        VARCHAR(255) NOT NULL,
    `created_at`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_by`  INT          NOT NULL,
    `modified_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `modified_by` INT          NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE (`recipe_id`, `name`),
    FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
    FOREIGN KEY (`modified_by`) REFERENCES `user` (`id`)
);

CREATE TABLE `image`
(
    `id`          INT          NOT NULL AUTO_INCREMENT,
    `recipe_id`   INT          NOT NULL,
    `filename`    VARCHAR(255) NOT NULL,
    `mimetype`    VARCHAR(255) NOT NULL,
    `content`     MEDIUMBLOB   NOT NULL,
    `created_at`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_by`  INT          NOT NULL,
    `modified_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `modified_by` INT          NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
    FOREIGN KEY (`modified_by`) REFERENCES `user` (`id`)
);

INSERT INTO `role`(`name`)
VALUES ('ADMIN'),
       ('MODERATOR'),
       ('EDITOR'),
       ('USER');

INSERT INTO `user`(`username`, `password`, `role_id`)
VALUES ('admin', %(password)s, (SELECT `id` FROM `role` WHERE `name` = 'ADMIN'));