import datetime
import random

import requests

from mongo_DB import MongoDB
from yaohuo import YaoHuo

WEEK_DICT = {0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四', 4: '星期五', 5: '星期六', 6: '星期日'}
POST_NUM = 30

class PostArt():
    def __init__(self):
        self.m = MongoDB('mongodb://sooko.ml:36565', 'yaohuo', need_auth=True, auth=('tk', 'Aa123456'))
        pass

    def prepare_content(self):
        content = ''
        date = datetime.datetime.now().strftime('%Y-%m-%d') + '  {}'.format(WEEK_DICT[datetime.datetime.today().weekday()])
        date = '[b]Date: {}[/b]\n\n'.format(date)
        # print(date)
        content += date
        tmp_title_list = []
        for i in range(POST_NUM):
            one = self.m.get_one_and_pop_one('img')
            print(one)
            if one is not None:
                title = one['title']
                img_url = one['img_url']
                content += '[img]{}[/img]\n'.format(img_url)
                content += '[b]{}[/b]\n\n\n'.format(title)
                tmp_title_list.append(title)
        post_title = random.choice(tmp_title_list)
        print(post_title)
        print(content)
        return post_title, content

    def run(self):
        post_title, content = self.prepare_content()
        post_title += '-GIF分享-{}P'.format(POST_NUM)

        y = YaoHuo()
        y.post_article(post_title, content)

        with open('post.txt','w',encoding='utf-8') as f:
            f.write(post_title+'\n\n')
            f.write(content)


if __name__ == '__main__':
    p = PostArt()
    p.run()
