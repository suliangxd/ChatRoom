/*
 * author: the5fire
 * blog:  the5fire.com
 * date: 2014-03-16
 * */
$(function(){
    WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
    WEB_SOCKET_DEBUG = true;

    var socket = io.connect();
    socket.on('connect', function(){
        console.log('connected');
    });

    $(window).bind("beforeunload", function() {
        socket.disconnect();
    });

    var User = Backbone.Model.extend({
        urlRoot: '/user',
    });

    var Topic = Backbone.Model.extend({
        urlRoot: '/topic',
    });

    var Message = Backbone.Model.extend({
        urlRoot: '/message',
        sync: function(method, model, options) {
            if (method === 'create') {
                socket.emit('message', model.attributes);
                // 错误处理没做
                $('#comment').val('');
            } else {
                return Backbone.sync(method, model, options);
            };
        },
    });

    var Topics = Backbone.Collection.extend({
        url: '/topic',
        model: Topic,
    });

    var Messages = Backbone.Collection.extend({
        url: '/message',
        model: Message,
    });

    var topics = new Topics;

    var TopicView = Backbone.View.extend({
        tagName:  "div class='column'",
        templ: _.template($('#topic-template').html()),

        // 渲染列表页模板
        render: function() {
          $(this.el).html(this.templ(this.model.toJSON()));
          return this;
        },
    });

    var messages = new Messages;

    var MessageView = Backbone.View.extend({
        tagName:  "div class='comment'",
        templ: _.template($('#message-template').html()),

        // 渲染列表页模板
        render: function() {
          $(this.el).html(this.templ(this.model.toJSON()));
          return this;
        },
    });


    var AppView = Backbone.View.extend({
        el: "#main",
        topic_list: $("#topic_list"),
        topic_section: $("#topic_section"),
        message_section: $("#message_section"),
        message_list: $("#message_list"),
        message_head: $("#message_head"),

        events: {
            'click .submit': 'saveMessage',
            'click .submit_topic': 'saveTopic',
            'keypress #comment': 'saveMessageEvent',
        },

        initialize: function() {
            _.bindAll(this, 'addTopic', 'addMessage');

            topics.bind('add', this.addTopic);

            // 定义消息列表池，每个topic有自己的message collection
            // 这样保证每个主题下得消息不冲突
            this.message_pool = {};
            this.socket = null;

            this.message_list_div = document.getElementById('message_list');
        },

        addTopic: function(topic) {
            var view = new TopicView({model: topic});
            this.topic_list.append(view.render().el);
        },

        addMessage: function(message) {
            var view = new MessageView({model: message});
            this.message_list.append(view.render().el);
            self.message_list.scrollTop(self.message_list_div.scrollHeight);
        },

        saveMessageEvent: function(evt) {
            if (evt.keyCode == 13) {
                this.saveMessage(evt);
            }
        },
        saveMessage: function(evt) {
            var comment_box = $('#comment')
            var content = comment_box.val();
            if (content == '') {
                alert('内容不能为空');
                return false;
            }
            var topic_id = comment_box.attr('topic_id');
            var message = new Message({
                content: content,
                topic_id: topic_id,
            });
            var messages = this.message_pool[topic_id];
            message.save(); // 依赖上面对sync的重载
        },

        saveTopic: function(evt) {
            var topic_title = $('#topic_title');
            if (topic_title.val() == '') {
                alert('主题不能为空！');
                return false
            }
            var topic = new Topic({
                title: topic_title.val(),
            });
            self = this;
            topic.save(null, {
                success: function(model, response, options){
                    topics.add(response);
                    topic_title.val('');
                },
                error: function(model, resp, options) {
                    alert(resp.responseText);
                }
            });
        },

        showTopic: function(){
            topics.fetch();
            this.topic_section.show();
            this.message_section.hide();
            this.message_list.html('');

            this.goOut()
        },

        goOut: function(){
            // 退出房间
            socket.emit('go_out');
            socket.removeAllListeners('message');
        },

        initMessage: function(topic_id) {
            var messages = new Messages;
            messages.bind('add', this.addMessage);
            this.message_pool[topic_id] = messages;
        },

        showMessage: function(topic_id) {
            this.initMessage(topic_id);

            this.message_section.show();
            this.topic_section.hide();
            
            this.showMessageHead(topic_id);
            $('#comment').attr('topic_id', topic_id);

            var messages = this.message_pool[topic_id];
            // 进入房间
            socket.emit('topic', topic_id);
            // 监听message事件，添加对话到messages中
            socket.on('message', function(response) {
                messages.add(response);
            });
            messages.fetch({
                data: {topic_id: topic_id},
                success: function(resp) {
                    self.message_list.scrollTop(self.message_list_div.scrollHeight)
                },
                error: function(model, resp, options) {
                    alert(resp.responseText);
                }
            });
        },

        showMessageHead: function(topic_id) {
            var topic = new Topic({id: topic_id});
            self = this;
            topic.fetch({
                success: function(resp, model, options){
                    self.message_head.html(model.title);
                },
                error: function(model, resp, options) {
                    alert(resp.responseText);
                }
            });
        },

    });


    var LoginView = Backbone.View.extend({
        el: "#login",
        wrapper: $('#wrapper'),
        
        events: {
            'keypress #login_pwd': 'loginEvent',
            'click .login_submit': 'login',
            'keypress #reg_pwd_repeat': 'registeEvent',
            'click .registe_submit': 'registe',
        },

        hide: function() {
            this.wrapper.hide();
        },

        show: function() {
            this.wrapper.show();
        },

        loginEvent: function(evt) {
            if (evt.keyCode == 13) {
                this.login(evt);
            }
        },

        login: function(evt){
            var username_input = $('#login_username');
            var pwd_input = $('#login_pwd');
            var u = new User({
                username: username_input.val(),
                password: pwd_input.val(),
            });
            u.save(null, {
                url: '/login',
                success: function(model, resp, options){
                    g_user = resp;
                    // 跳转到index
                    appRouter.navigate('index', {trigger: true});
                },
                error: function(model, resp, options) {
                    alert(resp.responseText);
                }
            });
        },

        registeEvent: function(evt) {
            if (evt.keyCode == 13) {
                this.registe(evt);
            }
        },

        registe: function(evt){
            var reg_username_input = $('#reg_username');
            var reg_pwd_input = $('#reg_pwd');
            var reg_pwd_repeat_input = $('#reg_pwd_repeat');
            var u = new User({
                username: reg_username_input.val(),
                password: reg_pwd_input.val(),
                password_repeat: reg_pwd_repeat_input.val(),
            });
            u.save(null, {
                success: function(model, resp, options){
                    g_user = resp;
                    // 跳转到index
                    appRouter.navigate('index', {trigger: true});
                },
                error: function(model, resp, options) {
                    alert(resp.responseText);
                }
            });
        },
    });

    var UserView = Backbone.View.extend({
        el: "#user_info",
        username: $('#username'),

        show: function(username) {
            this.username.html(username);
            this.$el.show();
        },
    });

    var AppRouter = Backbone.Router.extend({
        routes: {
            "login": "login",
            "index": "index",
            "topic/:id" : "topic",
        },

        initialize: function(){
            // 初始化项目, 显示首页
            this.appView = new AppView();
            this.loginView = new LoginView();
            this.userView = new UserView();
            this.indexFlag = false;
        },

        login: function(){
            this.loginView.show();
        },

        index: function(){
            if (g_user && g_user.id != undefined) {
                this.appView.showTopic();
                this.userView.show(g_user.username);
                this.loginView.hide();
                this.indexFlag = true;  // 标志已经到达主页了
            }
        },

        topic: function(topic_id) {
            if (g_user && g_user.id != undefined) {
                this.appView.showMessage(topic_id);
                this.userView.show(g_user.username);
                this.loginView.hide();
                this.indexFlag = true;  // 标志已经到达主页了
            }
        },
    });

    var appRouter = new AppRouter();
    var g_user = new User;
    g_user.fetch({
        success: function(model, resp, options){
            g_user = resp;
            Backbone.history.start({pustState: true});

            if(g_user === null || g_user.id === undefined) {
                // 跳转到登录页面
                appRouter.navigate('login', {trigger: true});
            } else if (appRouter.indexFlag == false){
                // 跳转到首页
                appRouter.navigate('index', {trigger: true});
            }
        },
        error: function(model, resp, options) {
            alert(resp.responseText);
        }
    }); // 获取当前用户
});
