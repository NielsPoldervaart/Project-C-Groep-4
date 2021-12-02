##FILE GENERATES DATABASE TABLE STRUCTURE IF NOT EXISTS
import pymysql

##Database information
conn = pymysql.connect(
    host="sql11.freesqldatabase.com",
    database="sql11455878",
    user="sql11455878",
    password="tEwKz5RhgR",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

sql_creation = [
"""
CREATE TABLE IF NOT EXISTS  `Gallery` (
  `gallery_id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`gallery_id`),
  UNIQUE INDEX `gallery_id_UNIQUE` (`gallery_id` ASC))
ENGINE = InnoDB;""",
"""
CREATE TABLE IF NOT EXISTS `Collection` (
  `collection_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `Gallery_gallery_id` INT NOT NULL,
  PRIMARY KEY (`collection_id`),
  UNIQUE INDEX `collection_id_UNIQUE` (`collection_id` ASC),
  INDEX `fk_Collection_Gallery1_idx` (`Gallery_gallery_id` ASC),
  CONSTRAINT `fk_Collection_Gallery1`
    FOREIGN KEY (`Gallery_gallery_id`)
    REFERENCES `Gallery` (`gallery_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS `Company` (
  `company_id` INT NOT NULL AUTO_INCREMENT,
  `company_name` VARCHAR(45) NOT NULL,
  `Collection_collection_id` INT NOT NULL,
  PRIMARY KEY (`company_id`),
  UNIQUE INDEX `company_id_UNIQUE` (`company_id` ASC),
  INDEX `fk_Company_Collection1_idx` (`Collection_collection_id` ASC),
  CONSTRAINT `fk_Company_Collection1`
    FOREIGN KEY (`Collection_collection_id`)
    REFERENCES `Collection` (`collection_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS `Role` (
  `role_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE INDEX `role_id_UNIQUE` (`role_id` ASC))
ENGINE = InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS `User` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `Company_company_id` INT NOT NULL,
  `Role_role_id` INT NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC),
  INDEX `fk_User_Company1_idx` (`Company_company_id` ASC),
  INDEX `fk_User_Role1_idx` (`Role_role_id` ASC),
  CONSTRAINT `fk_User_Company1`
    FOREIGN KEY (`Company_company_id`)
    REFERENCES `Company` (`company_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_Role1`
    FOREIGN KEY (`Role_role_id`)
    REFERENCES `Role` (`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS `Template` (
  `template_id` INT NOT NULL AUTO_INCREMENT,
  `tamplate_file` VARCHAR(255) NOT NULL,
  `Company_company_id` INT NOT NULL,
  PRIMARY KEY (`template_id`),
  UNIQUE INDEX `template_id_UNIQUE` (`template_id` ASC),
  INDEX `fk_Template_Company1_idx` (`Company_company_id` ASC),
  CONSTRAINT `fk_Template_Company1`
    FOREIGN KEY (`Company_company_id`)
    REFERENCES `Company` (`company_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS `Product` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `price` DECIMAL(2,2) NOT NULL,
  `verified` TINYINT NOT NULL,
  `downloads` INT NOT NULL,
  `template_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `Gallery_gallery_id` INT NOT NULL,
  PRIMARY KEY (`product_id`),
  UNIQUE INDEX `product_id_UNIQUE` (`product_id` ASC),
  INDEX `fk_Product_Template1_idx` (`template_id` ASC),
  INDEX `fk_Product_User1_idx` (`user_id` ASC),
  INDEX `fk_Product_Gallery1_idx` (`Gallery_gallery_id` ASC),
  CONSTRAINT `fk_Product_Template1`
    FOREIGN KEY (`template_id`)
    REFERENCES `Template` (`template_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Product_User1`
    FOREIGN KEY (`user_id`)
    REFERENCES `User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Product_Gallery1`
    FOREIGN KEY (`Gallery_gallery_id`)
    REFERENCES `Gallery` (`gallery_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS `Image` (
  `image_id` INT NOT NULL AUTO_INCREMENT,
  `image` BLOB(1) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`image_id`),
  UNIQUE INDEX `image_id_UNIQUE` (`image_id` ASC))
ENGINE = InnoDB;
""",
"""
CREATE TABLE IF NOT EXISTS `Image_has_Collection` (
  `Image_image_id` INT NOT NULL,
  `Collection_collection_id` INT NOT NULL,
  INDEX `fk_Image_has_Collection_Image1_idx` (`Image_image_id` ASC),
  INDEX `fk_Image_has_Collection_Collection1_idx` (`Collection_collection_id` ASC),
  CONSTRAINT `fk_Image_has_Collection_Image1`
    FOREIGN KEY (`Image_image_id`)
    REFERENCES `Image` (`image_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Image_has_Collection_Collection1`
    FOREIGN KEY (`Collection_collection_id`)
    REFERENCES `Collection` (`collection_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
"""
]

sql_insert = [
  f"""INSERT INTO `Gallery` VALUES (default)""",
  f"""INSERT INTO `Collection` VALUES (default, 'TestCollection1', 1)""",
  f"""INSERT INTO `Company` VALUES (default, 'TestCompany1', 1)""",
  f"""INSERT INTO `Role` VALUES (default, 'KYNDA_ADMIN'), (default, 'COMPANY_ADMIN'), (default, 'COMPANY_WORKER')""",
  f"""INSERT INTO `Template` VALUES (default, 'Cassettes.html', 1)""",
  f"""INSERT INTO `User` Values (default, 'Test', 'User', 'TestUser@hr.nl', 'admin', 1, 1)"""
]

#sql_query1 = """SELECT * FROM `User`;"""
#cursor.execute(sql_query2)
#print(cursor.fetchall())
for query in sql_insert:
    cursor.execute(query)
#for i in temps:
#  print(i)
conn.commit()
conn.close()