# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 15:24:23 2019

@author: Administrator
"""
import re
import json
import requests
import datetime

def search_orders(content):
    
    txt = 'https://api.open.21ds.cn/apiv2/tbkorderdetailsget?apkey=794d154c-cac1-1524-5796-eba0265532ba&start_time=%s&end_time=%s&tbname=lfj870838406'%(content[2],content[3])
    return txt
def Turn_orders_link(content):
    html = getHTMLText(search_orders(content))
    #write(html)
    user_dict = json.loads(html)
    user_dict['type'] = user_dict['msg']
    return user_dict

def search_goods(keyword):
    adzoneid = '109442250042'
    siteid = '887200231'
    tbname = 'lfj870838406'
    sort = 'tk_total_commi_des'
    pagesize = '5'
    pageno = '1'
    txt = 'https://api.open.21ds.cn/apiv2/gettkmaterial?apkey=794d154c-cac1-1524-5796-eba0265532ba&adzoneid=%s&siteid=%s&tbname=%s&keyword=%s&sort=%s&pagesize=%s&pageno=%s'%(adzoneid, siteid, tbname, keyword, sort, pagesize, pageno) 
    return txt

def Turn_goods_link(keyword):

    html = getHTMLText(search_goods(keyword))
    #write(html)
    user_dict = json.loads(html)
    user_dict['type'] = user_dict['msg']
    return user_dict


def sub_link(tpwdcode):
    txt_link = 'TAOLINK'
    txt = 'https://api.open.21ds.cn/apiv2/getitemgyurlbytpwd?apkey=794d154c-cac1-1524-5796-eba0265532ba&tpwdcode=TAOLINK&pid=mm_503340173_887200231_109442250042&tbname=lfj870838406&shorturl=1&tpwd=1&tpwdpic&extsearch=1 '
    op = re.sub(txt_link,tpwdcode, txt)
    return op

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
      
def goods(id):
    txt_link = '568706761354'
    txt = 'https://api.open.21ds.cn/apiv1/getiteminfo?apkey=794d154c-cac1-1524-5796-eba0265532ba&itemid=568706761354'
    op = re.sub(txt_link,id, txt)
    return op

def goods_link(id):
    txt = 'https://api.open.21ds.cn/apiv2/getitemgyurl?apkey=794d154c-cac1-1524-5796-eba0265532ba&itemid=%s&pid=mm_503340173_887200231_109442250042&tbname=lfj870838406&shorturl=1&tpwd=1'%(id)
    return txt
def Turn_id_msg(id):
    html = getHTMLText(goods_link(id))
    goods_dict = json.loads(html)
    return goods_dict



def Turn_money(k):
    
    html = getHTMLText(goods(k['result']['data']['item_id']))
#    goods_dict = json.loads(html)
#    a = goods_dict['data']['n_tbk_item']['zk_final_price']
#    b = k['result']['data']['max_commission_rate']
#    print(k)
    goods_dict = json.loads(html)
    print(goods_dict)
    
    if 'youhuiquan' in k['result']['data'] :
        pass
    else:
        k['result']['data']['youhuiquan'] = 0
    a = float(goods_dict['data']['n_tbk_item']['zk_final_price']) - float(k['result']['data']['youhuiquan'])
    b = k['result']['data']['max_commission_rate']
    c = float(a)*float(b)*0.008 
    rate = float(b)*0.008
    d = {0: c, 1: rate}
    return d
    
    
def Turn_link(Taolink):

    html = getHTMLText(sub_link(Taolink))
    #write(html)
    user_dict = json.loads(html)
    user_dict['type'] = 'taolink'
    return user_dict

def panduanMsg(msg):
    pattern = re.compile('[\u0000-\u0029\u0080-\uFFFF][a-zA-Z0-9]+[\u0000-\u0029\u0080-\uFFFF]')
    match = pattern.findall(msg)            
    print('开始判断类型')
    if (msg[0] == '(') | (msg[0] =='（'):
        print('进入影视搜索')
        return {'type' : '影'}
    elif msg[0:4] == '查询订单':
        print('进入查询模式')
        return {'type' : '查询订单'}
    elif msg[0:2] == '绑定':
        print('进入绑定模式')
        return {'type' : '绑定'}
    elif ('vpn' in msg.lower()):
        print('进入vpn搜索')
        return {'type' : 'vpn'}
#    elif ('绑定' in msg):
#        print('进入绑定搜索')
#        return {'code' : 'alipay'}
    elif match:
        print('进入优惠券搜索')
        for i in range(len(match)):
            if match[i][0] == match[i][-1]:
                match[0] = match[i]
                
        return Turn_link(match[0])
    elif ('小说' in msg) | ('书' in msg) | ('杂志' in msg) | ('论文' in msg):
        print('进入小说搜索')
        return {'type' : '书'}

        
    else:
        print('进入搜索')
        return Turn_goods_link(msg)

def tao_content(msg):
    k = panduanMsg(msg)
    if k['type'] == '1':
#        if 
#            pass
        return '没有相关文本信息'
#    elif k['code'] == 'alipay':
#        a = re.sub([],'',msg)
    elif k['type'] == 'vpn':
        return '''无需赞赏，分享订阅号就是对我最大的支持
    <a href="https://s1.mobileapkfree.com/data/apps/com.muma.pn_3.3.9_339_mobileapkfree.com.apk?verify=U2FsdGVkX19evJvhTHChgPCBtEli9jUKoadIsx6DzRcsJVIQgxE0p7nrDsCQbJuLtvRFsacUwfx1AQcex3UebNFF3BdFOEBjHZkjajPMOqRJQ/M8Sz05tuFvxDbeWaw64IZryQQjDshEx4LVC8G8o3I23HNkQuAzshaQbGNkZONeFuSvv6VnOpF/fXJxYprsxHYfX7Oy1PQ04auW/j1w9xijTicPertm4J5Q64P9yssK6L8gEYj5ATy5bkBXOvu4XQPsPHmFuYRp0t9IKuJTOkbai6qu50v+scJw1FEAGSM=">免费vpn</a>
    '''
    elif k['type'] == '查询订单':
        print('进入订单匹配')
        #订单格式  查询订单，订单号，下单时间（用于核实是否本人）
        pattern = re.compile('查询订单[,，][0-9]{18,19}[,，][0-9]{4}[-][0-9]{2}[-][0-9]{2} [0-9]{2}[:][0-9]{2}[:][0-9]{2}')
        match = pattern.findall(msg)
        print(match)
        a = '''输入格式错误  
订单格式  查询订单,616XXXXXXXXXXXX837(订单号),2019-09-09 21:44:15（创建订单时间，用于核实是否本人）
日期与时间之间用空格隔开,建议复制模板使用。
'''
        if match:
            if match[0] == msg:
                print('准备查询分割')
                msg = re.sub('，',',',msg)
                k = msg.split(',')
                k[2] = datetime.datetime.strptime(k[2],'%Y-%m-%d %H:%M:%S')
                k.append(k[2])
                k[2] = datetime.datetime.strftime(k[2] + datetime.timedelta(minutes = -10),'%Y-%m-%d %H:%M:%S')
                k[3] = datetime.datetime.strftime(k[3] + datetime.timedelta(minutes = +10),'%Y-%m-%d %H:%M:%S')
                return k

            else:
                print('输出查询错误')
                return a
        else:
            print('输出查询错误')
            return a 
    elif k['type'] == '绑定':
        #绑定格式 绑定，张三（真实姓名，用于自动返钱），188XXXXX002（支付宝手机号）
        print('进入绑定匹配')
        pattern = re.compile('绑定[,，][\u4e00-\u9fa5]{2,3}[,，][0-9]{11}')
        match = pattern.findall(msg)
        print(match)
        a = '''输入格式错误  
绑定格式 绑定，张三（真实姓名，用于自动返钱），188XXXXX002（支付宝手机号）
'''
        if match:
            if match[0] == msg:
                print('准备分割')
                if msg[2] == ',':
                    return msg.split(',')
                elif msg[2] == '，':    
                    return msg.split('，')
            else:
                print('输出绑定错误')
                return a
        else:
            print('输出绑定错误')
            return a 
    elif k['type'] == '书':
        print('进入类型 书')
        a = '''无需赞赏，分享订阅号就是对我最大的支持
 
网站
<a href="https://www.jiumodiary.com/">鸠摩书屋</a>(多类型图书)
<a href="https://www.cn-ki.net/">仿知网</a>(知网文献下载，有下载次数限制)
<a href="http://www.hejizhan.com/html/search/">万千合集站</a>(文献免费下载 嵌套
ps：与楼上形成combo)
<a href="https://kgbook.com/">苦瓜书盘</a>(全类型图书集合，慢~)
    
安卓
www.lanzous.com/b773475  追更神器

苹果
<a href="https://apps.apple.com/cn/app/%E5%BF%AB%E8%AF%BB%E5%85%A8%E6%9C%AC%E5%B0%8F%E8%AF%B4-%E5%B0%8F%E8%AF%B4%E4%B9%8B%E7%94%B5%E5%AD%90%E4%B9%A6%E9%98%85%E8%AF%BB%E8%BF%BD%E6%9B%B4%E7%A5%9E%E5%99%A8/id1444741505">追更神器</a>
'''
        return a
    elif k['type'] == '影':
        print('进入类型 影')
        msg = re.sub('[()（）]','',msg)
        return '观影愉快<a href="http://ifkdy.com/?q=' + msg + '">' + msg + '</a>'
    elif k['type'] == '淘客商品获取成功':
        print('进入类型 淘客')
        a = ''
        print('淘客商品获取成功')
        for  i in range(3):
            c = Turn_id_msg(k['data'][i]['num_iid'])
#            print(c)
#            a = a + '%s %s\n'%(k['data'][i]['tpwd'], k['data'][i]['short_title'])
            if c['result']['data']['has_coupon']:
                a = a  +' <a href="%s">%s</a>%s,%s'%(c['result']['data']['short_url'], k['data'][i]['short_title'], c['result']['data']['tpwd'], c['result']['data']['coupon_info'])
            else:
                a = a  +' <a href="%s">%s</a>%s'%(c['result']['data']['short_url'], k['data'][i]['short_title'], c['result']['data']['tpwd'])
            m = Turn_money(c)
            a = a + '返利%.1f元\n'%(m[0])
        return a
    
    elif k['type'] == 'taolink':
        print('进入类型 taolink')
        a = ''
        if k['result']['data']['has_coupon']:    
            print('有优惠券 ')
            a = k['result']['data']['tpwd'] + ',' + k['result']['data']['coupon_info']+',结束时间到'+ k['result']['data']['coupon_end_time']
        else:
            print('无优惠券 ')
            a = k['result']['data']['tpwd'] + ',' + '无优惠券'
        m = Turn_money(k)
        print(m)
        return a + '\n最低套餐券后可反%.1f元，比例为百分之%.1f'%((m[0]),(m[1]*100))
    elif k['code'] == -1:
        return re.sub('[a-zA-Z]','',k['data'])
    else:
        return '没有相关信息'
    
