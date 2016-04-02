import sqlite3

str_info = "**********    add admin    [ make sure the length of username and password more than 5!!! ]**********\n"
print(str_info)

try: # python2
    username=raw_input('username: ')
    password=raw_input('password: ')
except NameError: # python3
    username=input('username: ')
    password=input('password: ')

conn = sqlite3.connect('chatroom.db')
sql = "insert into user (username, password, registed_time, usertype) \
                   values ('%s', '%s', datetime('now'), 2)" %(username, password)

conn.execute(sql)
conn.commit()
conn.close()

print("*********** done!!! ***********")

