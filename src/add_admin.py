import sqlite3

print "**********   add admin 【请确保用户名和密码都是5位以上！！！】    **********\n"
username=raw_input('username: ')
password=raw_input('password: ')

conn = sqlite3.connect('chatroom.db')
sql = "insert into user (username, password, registed_time, usertype) \
                   values ('%s', '%s', datetime('now'), 2)" %(username, password)

conn.execute(sql)
conn.commit()
conn.close()

print "*********** done!!! ***********"

