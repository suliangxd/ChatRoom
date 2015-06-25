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

class ChatHandler(tornado.web.RequestHandler):
	def get(self):
		cookie_user = self.get_secure_cookie("username")
		if cookie_user:
			usertype = common.get_usertype(cookie_user)
			self.render('chatroom.html', cookieUser=cookie_user, usertype = usertype)
		else:
			self.render('login.html', cookieUser=None)
	def post(self):
		return 