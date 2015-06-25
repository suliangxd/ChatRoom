#coding:utf-8

import sqlite3

conn = sqlite3.connect('chatroom.db')
cur  = conn.cursor()

def get_usertype(username):
	sql = "select usertype from user where username = '%s' limit 1" %(username)
	cur.execute(sql)
	usertype = cur.fetchone()
	return usertype[0]

#example
if __name__ == "__main__":
	a = '11111'
	print get_usertype(a)
