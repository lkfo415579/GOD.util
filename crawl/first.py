# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import codecs

class FirstSpider(CrawlSpider):
    name = 'first'
    # domain = "politics"
    domain = "finance"
    allowed_domains = ['%s.people.com.cn' % domain]
    start_urls = ['http://%s.people.com.cn/' % domain]
    
    output = codecs.open('output', 'w')
    
    le = LinkExtractor(allow=r'.*.html')
    rules = (
        Rule(le, callback="parse_item", follow=True),
    )
    def parse_item(self, response):
        self.logger.info('item page! %s', response.url)
        title = response.css('h1::text').get()
        if title and title.strip():
          context = response.css('div#rwb_zw p::text').getall()
          context.extend(response.css('div#p_content p::text').getall())
          context.extend(response.css('div#box_con p::text').getall())
          context.extend(response.css('font.show_c::text').getall())
          # combine all context together
          context = [x.strip() for x in context]
          context = [x for x in context if x]
          self.output.write("=" * 100 + "\n")
          self.output.write(title + "\n")
          for ele in context:
            self.output.write(ele + "\n")
          # error page record
          if not len(context):
            self.output.write(response.url + '\n')
          # print (title)
          # print (context)
          pass
