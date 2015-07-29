#coding:utf-8

import sqlite3

conn = sqlite3.connect('chatroom.db')
cur  = conn.cursor()

def get_usertype(username):
	sql = "select usertype from user where username = '%s' limit 1" %(username)
	cur.execute(sql)
	usertype = cur.fetchone()
	return usertype[0]
#获取room表中的所有数据,返回[roomlist,room_owner]
def getRoomList():
	sql = "select room.roomid,room.roomname,room.created_time,room.owner_id,user.username \
			from room,user where room.owner_id == user.userid"

	cursor = conn.execute(sql)
	roomlist = list(cursor.fetchall())
	print roomlist
	#roominfo = []
	#room[0]:roomid,[1]:roomname,[2]:created_time,[3]:owner_id
	#for room in roomlist:
	#	sql = "select username from user where userid = %d " %(room[3])
	#	cursor = conn.execute(sql)
	#	for row in cursor:
	#		roominfo.append([row[0],list(room)])
    #		break

	return roomlist

#example
if __name__ == "__main__":
	a = '11111'
	print get_usertype(a)
