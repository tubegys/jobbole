# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urljoin
from jobbole.items import JobboleArticleItemLoader


class PythonSpiderSpider(scrapy.Spider):
    name = 'python_spider'
    allowed_domains = ['python.jobbole.com']
    start_urls = ['http://python.jobbole.com/all-posts/']

    def parse(self, response):
        """
        获得文章列表页中所有的URL，将获得的URL交给scrapy进一步下载
        """
        post_urls = response.css('#archive .floated-thumb .post-thumb'
                                 ' a::attr(href)').extract()
        for post_url in post_urls:
            yield Request(url=urljoin(response.url, post_url),
                          callback=self.parse_detail)

        next_url = response.css('a.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        item_loader = JobboleArticleItemLoader()
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_css('publish_time', '.entry-meta p::text')
        item_loader.add_value('url', response.url)
        item_loader.add_css('praise_num', '.post-adds span h10::text')
        item_loader.add_css('fav_num', '.post-adds span::text')
        item_loader.add_css('comment_num', '.post-adds span::text')
