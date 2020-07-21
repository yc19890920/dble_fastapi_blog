CREATE TABLE `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(150) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL  COMMENT '密码',
    `email` VARCHAR(254)   COMMENT '邮箱',
    `first_name` VARCHAR(30)   COMMENT 'first name',
    `last_name` VARCHAR(30)   COMMENT 'last name',
    `is_superuser` BOOL NOT NULL  COMMENT '是否是超级用户' DEFAULT 0,
    `is_staff` BOOL NOT NULL  COMMENT '管理员' DEFAULT 0,
    `is_active` BOOL NOT NULL  COMMENT '账户启用' DEFAULT 1,
    `last_login` DATETIME(6)   COMMENT '最后登录时间',
    `date_joined` DATETIME(6) NOT NULL  COMMENT '最后登录时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci  COMMENT='用户表';
CREATE TABLE `blog_category` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL UNIQUE COMMENT '名称',
    `created` DATETIME(6) NOT NULL  COMMENT '创建时间' ,
    `updated` DATETIME(6) NOT NULL  COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci  COMMENT='标签';
CREATE TABLE `blog_article` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(100) NOT NULL  COMMENT '主题',
    `content` LONGTEXT   COMMENT '内容',
    `abstract` LONGTEXT   COMMENT '摘要',
    `status` VARCHAR(20)   COMMENT '状态',
    `created` DATETIME(6) NOT NULL  COMMENT '创建时间' ,
    `updated` DATETIME(6) NOT NULL  COMMENT '更新时间'  ,
    `category_id` INT,
    CONSTRAINT `fk_blog_art_blog_cat_0966199c` FOREIGN KEY (`category_id`) REFERENCES `blog_category` (`id`) ON DELETE SET NULL,
    KEY `idx_blog_articl_title_8186fa` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci  COMMENT='标签';
CREATE TABLE `blog_tag` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL UNIQUE COMMENT '名称',
    `created` DATETIME(6) NOT NULL  COMMENT '创建时间' ,
    `updated` DATETIME(6) NOT NULL  COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci  COMMENT='标签';
CREATE TABLE `blog_article_tag` (
    `blog_article_id` INT NOT NULL,
    `tag_id` INT NOT NULL,
    FOREIGN KEY (`blog_article_id`) REFERENCES `blog_article` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tag_id`) REFERENCES `blog_tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;