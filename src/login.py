#coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

import os.path
import sqlite3
import time

from tornado.options import define, options

conn = sqlite3.connect('chatroom.db')
cur  = conn.cursor()

#登录验证，设置cookie
class LoginHandler(tornado.web.RequestHandler):
	#检测用户名，密码是否正确
	def check_user(self, username, password):
		sql = "select * from user where username = '%s' and password = '%s' " %(username, password)
		cur.execute(sql)

		if cur.fetchall():
			return True;
		return False;

	def get(self):
		cookie_user = self.get_secure_cookie("username")
		self.render('login.html',cookieUser=cookie_user)
	
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		if self.check_user(username, password): #密码正确
			self.set_secure_cookie("username", username,1)
			cookie_user = self.get_argument('username')
			self.render('login.html', cookieUser=cookie_user)

		else: #密码错误
			self.write("用户名或密码错误,重新登录")
			self.render('login.html',cookieUser=None)
#注销
class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_all_cookies()
		time.sleep(1.5)
		self.redirect("/login")

if __name__ == '__main__':
	define("port", default=8000, help="run on given port", type=int)
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r'/login', LoginHandler),
				  (r'/logout', LogoutHandler)],
		template_path=os.path.join(os.path.dirname(__file__), "templates"),
		cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E="
		)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
