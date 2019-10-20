
# -*- coding: utf-8 -*-
# filename: handle.py
 
import hashlib
import web
import receive
import time
import os
#import sys
#sys.path.append('/data')
import add 
import tao_turn



class Handle(object):
 
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)  #指向模板路径
        
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "a123456789"
 
            list = [token, timestamp, nonce]
            list.sort()
            s = list[0] + list[1] + list[2]
            hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
            print( "handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return echostr
        except (Exception) as Argument:
            return Argument
 
    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is:\n", webData)
            #打印消息体日志
            recMsg = receive.parse_xml(webData)     #parse 处理得到正确的信息格式
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType =='event' and recMsg.Event == 'subscribe':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = '购物，书籍，影视资源为一体的搜索订阅号，还有更多功能等你来反馈添加，默认回复某宝链接，返回优惠券以及返利信息；查找书籍请输入书， 影视资源请输入（影视名称） PS：不要忘加括号亲~'
                
                return self.render.reply_text(toUser, fromUser, int(time.time()), content)
            
            elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text': #判断是否为此类型变量
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = tao_turn.tao_content(str(recMsg.Content))
#                content = "欢迎关注德隆望尊！" + str(recMsg.Content)
                add.flash_friends(toUser)
                print('Reply message info:\n')
                print('toUser =', toUser)
                print('fromUser = ', fromUser)
                print('content = ', content)
                
#                content = '&lt;a href="http://www.baidu.com">百度</a>'
#                content = content.encode('')
#                print(111111111111)
                if content[0] == '绑定':
                    print('进入输出文本判断')
                    add.flash_aliply(toUser, content[2], content[1])
                    msg = msg_press(self.render.reply_text(toUser, fromUser, int(time.time()), '绑定成功,回复余额查看累计奖励'))
                elif content[0] == '查询订单':
                    print('进入输出订单判断')
                    flag = -1
                    k = tao_turn.Turn_orders_link(content)
                    print('字典返回正常')
                    if k['type'] == '查询时间段内暂无订单':
                        msg = msg_press(self.render.reply_text(toUser, fromUser, int(time.time()), '查询时间附件内暂无此订单'))
                    elif k['type'] == '获取成功':
                        print('获取成功')
                        for i in range(len(k['data'])):
                            print(i)
                            if k['data'][i]['trade_parent_id'] == content[1]:
                               flag = i
                        print('确定flag值',flag)
                        if flag == -1:
                            msg = msg_press(self.render.reply_text(toUser, fromUser, int(time.time()), '查询时间段内暂无此订单'))
                        else:
                            order_date = add.search_elem('orders', 'order_num', '1')
                            if content[1] in order_date:
                                msg = msg_press(self.render.reply_text(toUser, fromUser, int(time.time()), '订单已存在，无法重复添加'))
                            
#                            for i in range(len(order_date)):
#                                if content[1] == order_date[i]['order_num']:
#                                    print(order_date[i]['order_num'],i)
#                                    msg = msg_press(self.render.reply_text(toUser, fromUser, int(time.time()), '订单已存在，无法重复添加'))
#                                    return msg
                            else:
                                now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                print('订单输入数据库')
                                add.flash_orders(content[1], toUser, now, k['data'][flag]['tk_create_time'], k['data'][flag]['pub_share_pre_fee'], k['data'][flag]['alimama_share_fee'], '%.2f'%(float(k['data'][flag]['pub_share_pre_fee'])*0.8))
                            
                                msg = msg_press(self.render.reply_text(toUser, fromUser, int(time.time()), '查询成功，返利已转入余额'))
                    else:
                       msg = msg_press(self.render.reply_text(toUser, fromUser, int(time.time()), '其他错误'))
                        
                        
                    
                else:
                    msg = msg_press(self.render.reply_text(toUser, fromUser, int(time.time()), content))
                return msg#按照模板格式回复
            else:
                print("不支持的消息类型：",recMsg.MsgType)
                return "success"
        except (Exception) as Argment:
            return Argment


def prn_obj(obj):
    print ('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

def msg_press(msg):   
    msg._parts[12] = msg._parts[12].replace('&lt;', '<')
    msg._parts[12] = msg._parts[12].replace('&gt;', '>')
    msg._parts[12] = msg._parts[12].replace('&amp;', '&')
    msg._parts[12] = msg._parts[12].replace('&quot;', '"')
    msg._parts[12] = msg._parts[12].replace('&apos;', "'")
    return msg
def text_read(filename):
    # Try to read a txt file and return a list.Return [] if there was a mistake.
    file = open(filename,'r')
    content = file.read()
    file.close()
    return content
def tostr(k):
    a = str(k)
    