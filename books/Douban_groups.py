#!/usr/bin/env python
# -*- coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from base import BaseFeedBook
import re, urllib
from lib.urlopener import URLOpener
from bs4 import BeautifulSoup
import json
from config import SHARE_FUCK_GFW_SRV

__author__ = 'douban'

def getBook():
    return Douban_groups_biggirls

class Douban_groups_biggirls(BaseFeedBook):
    title                 = u'豆瓣小组「我们代表月亮消灭居心不良的乐手」'
    description           = u'大波浪乐队月亮组秘密基地。'
    language              = 'zh-cn'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_douban_biggirls.gif"
    coverfile             = "cv_douban_biggirls.jpg"
    oldest_article        = 1
    fulltext_by_readability = False
    needs_subscription 	  = True
    login_url			  = 'https://accounts.douban.com/passport/login?source=group'
    

    remove_tags = ['meta']
    remove_attrs = ['xmlns']

    feeds = [ (u'我们代表月亮消灭居心不良的乐手', SHARE_FUCK_GFW_SRV % urllib.quote('https://rsshub.app/douban/group/biggirls'), True) ]
    
    def url4forwarder(self, url):
        #生成经过转发器的URL
        return SHARE_FUCK_GFW_SRV % urllib.quote(url)
    
    def fetcharticle(self, url, opener, decoder):
        #链接网页获取一篇文章
        return BaseFeedBook.fetcharticle(self, self.url4forwarder(url), opener, decoder)
        
    def soupbeforeimage(self, soup):
        for img in soup.find_all('img'):
            imgurl = img['src'] if 'src' in img.attrs else ''
            if imgurl.startswith('http'):
                img['src'] = self.url4forwarder(imgurl)
                
    def postprocess(self, content):
        pn = re.compile(ur'<a href="(\S*?)">本话题在小组内有.*?条讨论，点击查看。</a>', re.I)
        comment = ''
        mt = pn.search(content)
        url = mt.group(1) if mt else None
        if url:
            opener = URLOpener(url, timeout=self.timeout)
            result = opener.open(url)
            if result.status_code == 200 and result.content:
              if self.feed_encoding:
                try:
                  comment = result.content.decode(self.feed_encoding)
                except UnicodeDecodeError:
                  return content

        pn = re.compile(r'SNB.data.goodComments\ =\ ({.*?});', re.S | re.I)
        mt = pn.search(comment)
        if mt:
            comment_json = mt.group(1)
            j = json.loads(comment_json)
            soup = BeautifulSoup(content, "lxml")
            for c in j['comments']:
                u = c['user']['screen_name']
                t = BeautifulSoup('<p>@%s:%s</p>' % (u, c['text']))
                for img in t.find_all('img', alt=True):
                    img.replace_with(t.new_string(img['alt']))
                soup.html.body.append(t.p)

            content = unicode(soup)
        return content
