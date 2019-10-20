# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle
urls = (
    '/weixin/gateway', 'Handle',
    '/alipay/comfirm', 'notify'
)


import urllib
import time
import json
import os

#def printAlipay(post):

def notify(cls,request):
    """
    支付宝内部支付完成后，异步通知到这个接口，返回支付宝状态，同步到数据库中
    """
    """处理不同得参数，必须返回success"""
#    data = request.values.to_dict()
#    # sign, sign_type 都要从数据中取出，否则签名通不过
#    sign, sign_type = data.pop('sign'), data.pop('sign_type')
#    #排序
#    params = sorted(data.items(), key=lambda e: e[0], reverse=False)
#    #拼接成字符串
#    message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()
#    alipay_public_key = cls.alipay_client_config.alipay_public_key
#    try:
#        if verify_with_rsa(alipay_public_key.encode('utf-8').decode('utf-8'), message, sign):
#            # 一定是success这个单词，其他的alipay不认
#            return 'success'
#        else:
#            return 'failure'
# 
#    except:
#        return 'failure'
    print(request)
    return 'success'


def text_save(content,filename,mode='a'):
        # Try to save a list variable in txt file.
        os.remove(filename) 
        file = open(filename,mode)
        file.write(content)
        file.close()
        
        
def text_read(filename):
    # Try to read a txt file and return a list.Return [] if there was a mistake.
    file = open(filename,'r')
    content = file.read()
    file.close()
    return content

class Basic:
    def __init__(self):
        self.__accessToken = ''
#        self.__leftTime = 0
        self.endtime = 0
    def __real_get_access_token(self,appId,appSecret):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret))
        print(postUrl)
        urlResp = urllib.request.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())
        self.__accessToken = urlResp['access_token']
        print(self.__accessToken)
#        self.__leftTime = urlResp['expires_in']
        self.endtime = time.time() + 7050
        text_save(self.__accessToken,'token',mode='a')
    
        
        
    def get_access_token(self,appId,appSecret):
        """
        expires_in字段是微信access_token的有效时间，超时将无法使用
        """
#        if self.endtime < time.time() - 150:
        self.__real_get_access_token(appId,appSecret)
        return self.__accessToken
    def run(self):
        while(True):
            if self.endtime > time.time():
                time.sleep(100)
                print(time.time())
#                pass
            else:
                appId = 'wx10ce9404fe56ca4e'
                appSecret = 'eee1a42114c526634c991306c24438b2' 
                self.__real_get_access_token(appId,appSecret)

token = Basic()
if __name__ == '__main__':
    import threading
    class myThread (threading.Thread):
        def __init__(self, threadID, name):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
        def run(self):
            print ("开始线程：" + self.name)
            if self.threadID == 1:
                app = web.application(urls, globals())
                app.run()
            elif self.threadID == 2:
                token.run()
            print ("退出线程：" + self.name)
    
    thread2 = myThread(2, "token")    
    thread1 = myThread(1, "app")
    
    thread2.start()
    thread1.start()
    

    
#handle.py