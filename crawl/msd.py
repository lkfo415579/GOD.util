# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import codecs
from scrapy import Selector


class FirstSpider(CrawlSpider):
    name = 'msd'
    web = 'msdmanuals.cn'
    allowed_domains = ['%s' % web]
    # start_urls = ['https://%s.cn/首页' % web]
    start_urls = ['http://%s' % web]
    output = codecs.open('output', 'w')
    # le = LinkExtractor(allow=r'.*.html')
    le = LinkExtractor(allow=r'.*.*')
    rules = (
        Rule(le, callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        if response.status != 200:
            return
        self.logger.info('item page! %s', response.url)
        try:
            title = response.css('article h1::text').get()
        except Exception as e:
            return
        # world = response.css('article *').getall()
        world = response.xpath('//article/descendant::node()')
        context = []
        for w in world:
            name = w.xpath('name()').get()
            CLASS = w.xpath('./@class').get()
            if name == 'script' or name == "None":
                continue
            # Conditional filter
            RUN = False
            if name == 'div' and CLASS == 'para' or name == 'section':
                RUN = True

            if RUN:
                line = w.xpath(".//*[not(contains(name(), 'script'))]/text()").getall()
                line = [x.strip() for x in line]
                line = "".join(line)
                if line:
                    context.append(line)
        if title:
            # debug
            print(title)
            self.output.write("=" * 100 + "\n")
            self.output.write(response.url + '\n')
            #
            context = [x.strip() for x in context]
            context = [x for x in context if x]
            # self.output.write(title + "\n")
            for ele in context:
                self.output.write(ele + "\n")
            # error page record
            # if not len(context):
            #     self.output.write(response.url + '\n')
            pass
