#!/usr/bin/env python
# -*- coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from base import BaseFeedBook

def getBook():
    return Douban

class Douban(BaseFeedBook):
    title                 = u'豆瓣小组「我们代表月亮消灭居心不良的乐手」'
    __author__			  = u'Douban'
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
    
	feeds = [
        (u'豆瓣小组「我们代表月亮消灭居心不良的乐手」', 'https://rsshub.app/douban/group/biggirls'),
    ]
    
    