DROP TABLE IF EXISTS xfc_region;
CREATE TABLE `xfc_region` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '表id',
  `name` varchar(32) NULL COMMENT '地区名称',
  `level` tinyint(4) '0' COMMENT '地区等级 分省市县区',
  `parent_id` int(10) NULL COMMENT '父id',
  `gid` varchar(30) NULL COMMENT '行政区划id',
  `pinyin` varchar(100) NULL COMMENT '拼音',
  `city_code` varchar(16) NULL COMMENT '区号',
  `latitude` decimal(12, 5) null comment '纬度',
  `longitude` decimal(12, 5) null comment '经度',
  `zipcode` varchar(16) null comment '邮政编码',
  PRIMARY KEY (`id`),
  UNIQUE KEY `Index 4` (`parent_id`,`name`),
  KEY `parent_id` (`parent_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='地址表';