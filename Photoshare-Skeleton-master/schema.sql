CREATE DATABASE teamformation;
USE teamformation;

CREATE TABLE Users(
	user_id int4  AUTO_INCREMENT,
	email varchar(255) UNIQUE,
	fname varchar(255),
	lname varchar(255),
	gender bit, 
	PRIMARY KEY (user_id)
);

CREATE TABLE Skills(
	skill_id int4  AUTO_INCREMENT,
  	name varchar(255) UNIQUE,
  	description varchar(255),
	PRIMARY KEY (skill_id)
);

CREATE TABLE Owns(
	user_id int4 NOT NULL,
	skill_id int4 NOT NULL,
	FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
	FOREIGN KEY (skill_id) REFERENCES Skills(skill_id) ON DELETE CASCADE
);

INSERT INTO Users (email, fname, lname) VALUES ('test@bu.edu', 'test', 'test');
INSERT INTO Skills (name, description) VALUES ('mysql', 'proficient at mysql');
INSERT INTO Owns (user_id,skill_id) VALUES (1,1);
