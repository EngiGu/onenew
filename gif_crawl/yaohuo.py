import re
import sys

import requests


class YaoHuo():
    def __init__(self):
        self.user = '15527434825'
        self.pass_ = '61f8d36d68e5165bc7cb4dad6232972d'
        self.sess = requests.session()
        self._login()

    def _login(self):
        login_url = 'https://yaohuo.me/waplogin.aspx'
        data = {
            'logname': self.user,
            'logpass': self.pass_,
            'savesid': '0',
            'action': 'login',
            'classid': '0',
            'siteid': '1000',
            'sid': '-3-0-0-0-0',
            'backurl': '',
            'g': '登 录',
        }
        r = self.sess.post(login_url, data=data)
        # print(r.content.decode())
        if '登录成功' in r.content.decode():
            return True
        return False

    def post_article(self, title, content):
        if self._login():
            # post
            pre_url = 'https://yaohuo.me/bbs/book_view_add.aspx?page=1&classid=240&siteid=1000'
            r = self.sess.get(pre_url)
            args_list = re.findall(r'name="(\w+)" value="(.*?)"', r.content.decode())
            args = {i[0]: i[1] for i in args_list}
            data = {
                'face': '',
                'stype': '',
                'book_title':  title,
                'book_content': content,
                'g': '发表新帖子',
            }
            data.update(args)
            print(data)
            # res = self.sess.post('https://yaohuo.me/bbs/book_view_add.aspx',data=data)
            # print(res.content.decode())
            pass
        else:
            sys.exit('login failed and exit!')



if __name__ == '__main__':
    y = YaoHuo()
    y.post_article('','')
