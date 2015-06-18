#coding:utf-8

import sqlite3

con = sqlite3.connect('chatroom.db')
cur = con.cursor()

command = """
BEGIN;
CREATE TABLE IF NOT EXISTS user(
	"userid" integer PRIMARY KEY AUTOINCREMENT,
	"username" varchar(20) NOT NULL, 
	"password" varchar(50) NOT NULL,
	"registed_time" datetime NOT NULL,
	"isvip" smallint DEFAULT 0,
	"isadmin" smallint DEFAULT 0,
	"email" varchar(30),
	"phone" varchar(20),
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

