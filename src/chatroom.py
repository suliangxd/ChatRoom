#coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

import os.path
import sqlite3
import datetime
import time
import common

from tornado.options import define, options

conn = sqlite3.connect('chatroom.db')
cur  = conn.cursor()

#显示所有聊天室的类
class ChatRoomHandler(tornado.web.RequestHandler):

	def get(self):
		cookie_user = self.get_secure_cookie("username")
		roomlist = common.getRoomList()
		if cookie_user:
			usertype = common.get_usertype(cookie_user)
			self.render('chatroom.html', cookieUser=cookie_user, usertype = usertype,Error=False,
						roomlist=roomlist)
		else:
			self.render('login.html', cookieUser=None, Error = False)
			
	def post(self):
		return

#创建聊天室
class CreateRoomHandler(tornado.web.RequestHandler):

	#检查roomname是否被使用，未被使用返回False
	def check_is_userd(self,roomname):
		sql = "select roomname from room where roomname = '%s' " %(roomname)
		cur.execute(sql)
		if cur.fetchall():
			return True;
		return False;

	def get(self):
		cookie_user = self.get_secure_cookie("username")
		if cookie_user:
			usertype = common.get_usertype(cookie_user)
			self.render('createroom.html', cookieUser=cookie_user, usertype = usertype,Error=False)
		else:
			self.render('login.html', cookieUser=None, Error = False)
	#创建聊天室
	def post(self):
		roomname = self.get_argument('roomname')
		username = self.get_secure_cookie('username')
		
		#roomname被使用过
		if self.check_is_userd(roomname):
			usertype = common.get_usertype(username)
			self.render('createroom.html', cookieUser=username, usertype = usertype, Error=True)
			return

		sql = "select userid from user where username = '%s' " % (username)
		cursor = conn.execute(sql)
		for row in cursor:
			userid = row[0]
		#创建
		sql = "insert into room (roomname, created_time, owner_id) \
				values('%s', datetime('now'), %d)" %(roomname, userid)
		conn.execute(sql)
		conn.commit()
		self.redirect("/chatroom")
#聊天
class ChatHandler(tornado.web.RequestHandler):
	def get(self):
		cookie_user = self.get_secure_cookie("username")
		if cookie_user:
			usertype = common.get_usertype(cookie_user)
			self.render('chat.html', cookieUser=cookie_user, usertype = usertype, Error=False)
		else:
			self.render('login.html', cookieUser=None, Error = False)

	def post(self):
		roomid = self.get_argument("roomid")
		roomname = self.get_argument("roomname")
		created_time = self.get_argument("created_time")
		owner_id = self.get_argument("owner_id")
		owner_name = self.get_argument("owner_name")
		print "Success:  ",roomid,roomname,created_time,owner_id,owner_name
