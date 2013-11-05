
/*database scloud*/

/*for access control and auth*/
DROP TABLE IF EXISTS `domain_type`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `domain_type` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `type` varchar(255)  NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;


DROP TABLE IF EXISTS `role`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `role` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `role_name` varchar(255)  NOT NULL,
  `role_type` varchar(255) NOT NULL default '',
  `role_expires` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL default 1,
  `metadata` text NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;

DROP TABLE IF EXISTS `roles_in_domain`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `roles_in_domain` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `domain_type_id` int  NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;


DROP TABLE IF EXISTS `user_space`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `user_space` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(255)  NOT NULL,
  `owner_id` int  NOT NULL,
  `size` int NOT NULL default 0,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;

DROP TABLE IF EXISTS `domain`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `domain` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `domain_type_id` int  NOT NULL,
  `space_id` int  NOT NULL,
  `size` int NOT NULL default 0,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;

DROP TABLE IF EXISTS `permission`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `permission` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(255)  NOT NULL,
  `action_type` varchar(255)  NOT NULL,
  `res_type` varchar(255)  NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;

DROP TABLE IF EXISTS `user`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(255)  NOT NULL,
  `pass` varchar(255)  NOT NULL,
  `email` varchar(255)  NOT NULL,
  `is_active` tinyint(1)  NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;

DROP TABLE IF EXISTS `user_roles`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `user_roles` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `user_id` int  NOT NULL,
  `role_id` int  NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;

DROP TABLE IF EXISTS `data_acl`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `data_acl` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `data_uri` varchar(255)  NOT NULL,
  `data_type` varchar(255)  NOT NULL,
  `owner_id` varchar(255)  NOT NULL,
  `acl_type` varchar(255)  NOT NULL,/*public read, public read&write, private, protected*/
  /*ACL = { ACE [, ACE ...] }"acetype": "ALLOW","identifier": "OWNER@","aceflags": "OBJECT_INHERIT, CONTAINER_INHERIT","acemask": "ALL_PERMS"*/
  `acl_content` text  NOT NULL,  
  `data_pass` varchar(255)  NOT NULL default '',
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
SET character_set_client = @saved_cs_client;

/*==========================================================*/





