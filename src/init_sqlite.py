#coding:utf-8

import sqlite3

con = sqlite3.connect('chatroom.db')
cur = con.cursor()

command = """
BEGIN;
CREATE TABLE IF NOT EXISTS user(
	"userid" integer PRIMARY KEY AUTOINCREMENT,
	"username" varchar(25) NOT NULL, 
	"password" varchar(50) NOT NULL,
	"registed_time" datetime NOT NULL,
	"usertype" smallint DEFAULT 0,
	"email" varchar(30),
	"phone" varchar(20),
	"reverse1" integer DEFAULT NULL,
	"reverse2" varchar(50) DEFAULT NULL,
	UNIQUE("username") 
);
COMMIT;
"""

try:
	cur.executescript(command)
	con.commit()
except Exception as e:
	print e

cur.close()
con.close()

