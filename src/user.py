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

#用户信息修改
class ModifyHandler(tornado.web.RequestHandler):
	
	def get(self):
		cookie_user = self.get_secure_cookie("username")
		if cookie_user is None:
			self.redirect('/login')
		self.render('modify.html',cookieUser=cookie_user)
	
	def post(self):
		username = self.get_secure_cookie("username")
		if username is None:
			self.redirect('/login')
		password = self.get_argument('password')
		rep_password = self.get_argument('rep_password')
		email = self.get_argument('email')
		phone = self.get_argument('phone')
		if password != rep_password:
			self.write("两次密码输入不一致")
			self.render('modify.html',cookieUser=username)
		sql = "update user set password='%s', email='%s', phone='%s' where username ='%s' "\
				 %(password, email, phone, username)
		conn.execute(sql)
		conn.commit()
		self.write("修改成功")
		self.redirect('/chatroom')
#管理员特权操作
class AdminHandler(tornado.web.RequestHandler):

	def get(self):
		cookie_user = self.get_secure_cookie("username")
		if cookie_user is None:
			self.redirect('/login')
		else:
			usertype = common.get_usertype(cookie_user)
			self.render("admin.html",userType=usertype)
		
	def post(self):
		setvip_username = self.get_argument("username1", None)
		cancelvip_username = self.get_argument("username2", None)
		delete_username = self.get_argument("username3", None)
		delete_roomname = self.get_argument("roomname", None)
		cookie_user = self.get_secure_cookie("username")
		if cookie_user is None:
			self.redirect('/login')
		else:
			usertype = common.get_usertype(cookie_user)
		if setvip_username:
			sql = "update user set usertype = 1 where username = '%s' " %(setvip_username);
			conn.execute(sql)
			conn.commit()
			self.write("设置成功")
			self.render("admin.html",userType=usertype)
		if cancelvip_username:
			sql = "update user set usertype = 0 where username = '%s' " %(cancelvip_username)
			conn.execute(sql)
			conn.commit()
			self.write("取消成功")
			self.render("admin.html",userType=usertype)
		if delete_username:
			sql = "delete from user where username = '%s' " %(delete_username)
			conn.execute(sql)
			conn.commit()
			self.write("删除成功")
			self.render("admin.html",userType=usertype)
		if delete_roomname:
			sql = "delete from room where roomname = '%s' " %(delete_roomname)
			conn.execute(sql)
			conn.commit()
			self.redirect("/chatroom")

if __name__ == '__main__':
	define("port", default=8000, help="run on given port", type=int)
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r'/modify', ModifyHandler)],
		template_path=os.path.join(os.path.dirname(__file__), "templates")
		)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
