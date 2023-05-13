USE ARSnipper;
DELIMITER //
CREATE PROCEDURE add_user(
    IN email VARCHAR(255),
    IN first_name VARCHAR(50),
    IN last_name VARCHAR(50),
    IN phone VARCHAR(15)
)
BEGIN
    INSERT INTO USERS (C_EMAIL, C_FIRST_NAME, C_LAST_NAME, C_PHONE)
    VALUES (email, first_name, last_name, phone);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE add_account(
    IN email VARCHAR(255),
    IN password VARCHAR(255)
)
BEGIN
    DECLARE salt VARCHAR(32);
    SET salt = SHA2(RAND(), 256);
    INSERT INTO ACCOUNTS (C_EMAIL, C_PASSWORD, C_SALT)
    VALUES (email, SHA2(CONCAT(salt, password), 256), salt);
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE check_account_data(
    IN email VARCHAR(255),
    IN password VARCHAR(255),
    OUT account_exists BOOLEAN
)
BEGIN
    SELECT IF(COUNT(*) > 0, 1, 0) INTO account_exists FROM ACCOUNTS WHERE C_EMAIL = email AND C_PASSWORD = SHA2(CONCAT(C_SALT, password), 256);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE CheckEmailExists(
  IN email VARCHAR(255),
  OUT result INT
)
BEGIN
  DECLARE count INT;
  SELECT COUNT(*) INTO count FROM USERS WHERE C_EMAIL = email;
  IF count > 0 THEN
    SET result = 1;
  ELSE
    SET result = 0;
  END IF;
END //
DELIMITER ;
