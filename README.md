# ChatRoom web聊天室        
体验： http://120.25.0.104:8000/        
基于tornado框架 + sqlite3 + redis 

    多聊天室，多人实时聊天
##开发环境
**开发语言:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[python](https://www.python.org/)        
**web服务器:**&nbsp;[tornado](http://www.tornadoweb.org/en/stable/)    
**数据库:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[sqlite](https://www.sqlite.org/)     
**缓存数据库:**&nbsp;&nbsp;[redis](http://redis.io/)    
##Quick Start at local    
###依赖组件：   
1. python 2.7+
2. tornado
3. redis server
4. sqlite3   
  
###Start    
$ git clone https://githup.com/suliangxd/ChatRoom.git   
$ cd ChatRoom      
$ cd src    
$ redis-server  （开启redis服务）          
$ python init_sqlite.py（初始化数据库）      
$ python server.py    
then open your browser and type http://127.0.0.1:8000       

##开发说明
###功能结构图
**version 1.0**
![fun](http://i.niupic.com/images/2015/08/04/55c0a1aac44c8.jpg)
##实时聊天功能基本架构
**version 1.0**     

当用户进入某个聊天室，即相当于订阅了此聊天室对应在redis里的一个channel      
这里给出的架构图是指用户进入聊天室之后的实时聊天架构   
        
    思路说明：前端基于ajax的longpolling，后端采用redis的sub/pub机制
        1. 服务器端会阻塞请求直到有数据传递或超时才返回，这里设置超时时间为60s
        2. 客户端JavaScript响应处理函数会在处理完服务器返回的信息后，再次发出请求，重新建立连接
    出现的问题：
        当客户端处理接收的数据、重新建立连接时，此时相当于取消订阅该房间的channel而服务器端可能有新的数据到达，
        这样的情况下可能会造成数据丢失     
**架构图 V1.0**     
![jiagou1.0](http://i.niupic.com/images/2015/08/05/55c1775f7bed6.jpg)

##Screenshots     
--
###Login    

![Login] (http://pic.sueri.cn/di-J5QC.jpg)   
###chatroom

![ChatRoom] (http://pic.sueri.cn/di-O5Y6.png)
###chat   

![Chat] (http://pic.sueri.cn/di-IGVR.jpg)
