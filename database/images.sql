USE ARSnipper;



DELIMITER //
CREATE PROCEDURE check_object_exists(
    IN object_code VARCHAR(255),
    OUT object_exists INT
)
BEGIN
    SELECT COUNT(*) INTO object_exists FROM OBJECTS WHERE OBJECT_CODE = object_code;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE add_object_for_user(
    IN email VARCHAR(255),
    IN image_code VARCHAR(255),
    IN object_code VARCHAR(255)
)
BEGIN
    INSERT INTO OBJECTS (C_EMAIL, IMAGE_CODE, OBJECT_CODE)
    VALUES (email, image_code, object_code);
END //
DELIMITER ;



DELIMITER //

CREATE FUNCTION generate_unique_object_code() RETURNS TEXT
BEGIN
  DECLARE code TEXT;
  SET code = FLOOR(RAND() * 9999999999999) + 1;
  WHILE EXISTS (SELECT 1 FROM OBJECTS WHERE OBJECT_CODE = code) DO
    SET code = FLOOR(RAND() * 9999999999999) + 1;
  END WHILE;
  RETURN code;
END//
DELIMITER ;

CREATE FUNCTION generate_unique_image_code() RETURNS TEXT
BEGIN
  DECLARE code TEXT;
  SET code = FLOOR(RAND() * 9999999999999) + 1;
  WHILE EXISTS (SELECT 1 FROM IMAGES WHERE IMAGE_CODE = code) DO
    SET code = FLOOR(RAND() * 9999999999999) + 1;
  END WHILE;
  RETURN code;
END//

DELIMITER ;


DELIMITER //

CREATE PROCEDURE insert_user_image(
    IN p_image_code TEXT,
    IN p_email TEXT,
    IN p_object_code TEXT
)
BEGIN
    INSERT INTO USER_IMAGE (IMAGE_CODE, C_EMAIL, OBJECT_CODE)
    VALUES (p_image_code, p_email, p_object_code);
END //

DELIMITER ;


DELIMITER //
CREATE PROCEDURE insert_image(
    IN p_image_code TEXT,
    IN p_image_object TEXT
)
BEGIN
    INSERT INTO IMAGES (IMAGE_CODE, IMAGE_OBJECT)
    VALUES (p_image_code, p_image_object);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_image_object(
    IN p_image_code TEXT,
    IN p_object_code TEXT
)
BEGIN
    INSERT INTO IMAGE_OBJECTS (IMAGE_CODE, OBJECT_CODE)
    VALUES (p_image_code, p_object_code);
END //

DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_object(
    IN p_object_code TEXT,
    IN p_object_data TEXT
)
BEGIN
    INSERT INTO OBJECTS (OBJECT_CODE, OBJECT_DATA)
    VALUES (p_object_code, p_object_data);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_user_image_by_email(
    IN p_email TEXT
)
BEGIN
    SELECT *
    FROM USER_IMAGE
    WHERE C_EMAIL = p_email;
END //

DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_image_by_code(
    IN p_image_code TEXT
)
BEGIN
    SELECT *
    FROM IMAGES
    WHERE IMAGE_CODE = p_image_code;
END //

DELIMITER ;


DELIMITER //
CREATE PROCEDURE get_image_object_by_image_code(
    IN p_image_code TEXT
)
BEGIN
    SELECT *
    FROM IMAGE_OBJECTS
    WHERE IMAGE_CODE = p_image_code;
END //


DELIMITER ;


DELIMITER //
CREATE PROCEDURE get_object_by_code(
    IN p_object_code TEXT
)
BEGIN
    SELECT *
    FROM OBJECTS
    WHERE OBJECT_CODE = p_object_code;
END //
DELIMITER ;







