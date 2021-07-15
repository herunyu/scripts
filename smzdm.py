#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
什么值得买自动签到脚本
'''
import os
import json
import requests

DEFAULT_HEADERS = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'zhiyou.smzdm.com',
        'Referer': 'https://www.smzdm.com/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = DEFAULT_HEADERS

    def load_cookie_str(self, cookie):
        '''为session添加cookie.
        
        Args:
            cookie: 什么值得买登录cookie.
        '''
        self.session.headers['Cookie'] = cookie

    def checkin(self):
        '''签到函数.

        Returns:
            请求响应内容.
        '''
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        rsp = self.session.get(url)
        try:
            result = rsp.json()
            return result
        except:
            return rsp.content

def pushplus(title, content, token, template='html'):
    '''pushplus消息推送.

    Args:
        title: 消息标题.
        content: 具体消息内容，根据不同template支持不同格式.
        token: 用户令牌.
        template: 发送消息模板, html或json.

    Returns:
        JSON格式的请求响应内容.
    '''
    url = 'https://www.pushplus.plus/send'
    body = {
        'token': token,
        'title': title,
        'content': content,
        'template': template
    }
    data = json.dumps(body).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    rsp = requests.post(url, data=data, headers=headers)
    return rsp.json()

def test_push_plus():
    res = pushplus(title='Title',
                   content='Content',
                   token=os.environ.get('PUSH_PLUS_TOKEN'))

def checkin():
    sb = SMZDM_Bot()
    cookie = os.environ.get('SMZDM_COOKIE')
    if not cookie:
        print('没有找到cookie')
        return
    sb.load_cookie_str(cookie)
    res = sb.checkin()
    print(res)
    if res.get('error_msg'):
        result = res
    else:
        result = res.get('data')
    TOKEN = os.environ.get('PUSH_PLUS_TOKEN')
    if TOKEN:
        print('检测到PUSH_PLUS_TOKEN, 准备推送')
        title = '什么值得买每日签到' + ('成功' if not res.get('error_code') else '失败')
        pushplus(title=title, content=result, token=TOKEN, template='json')
    print('代码执行完毕')


if __name__ == '__main__':
    checkin()