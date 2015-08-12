#coding:utf-8

import sqlite3

conn = sqlite3.connect('chatroom.db')
cur  = conn.cursor()

def get_usertype(username):
	sql = "select usertype from user where username = '%s' limit 1" %(username)
	cur.execute(sql)
	usertype = cur.fetchone()
	if not usertype:
		return None
	return usertype[0]
#获取room表中的所有数据,返回[roomlist,room_owner]
def getRoomList():
	sql = "select room.roomid,room.roomname,room.created_time,room.owner_id,user.username \
			from room,user where room.owner_id == user.userid"

	cursor = conn.execute(sql)
	roomlist = list(cursor.fetchall())
	#print roomlist
	return roomlist
def getRoomInfo(roomid):
	sql = "select room.roomid,room.roomname,room.created_time,room.owner_id,user.username \
			from room,user where room.roomid = %d and room.owner_id == user.userid" %(roomid)
	cursor = conn.execute(sql)
	roominfo = list(cursor.fetchone())
	return roominfo

#example
if __name__ == "__main__":
	a = '11111'
	print get_usertype(a)
