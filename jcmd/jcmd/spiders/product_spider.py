#encoding=utf-8
import re

from scrapy.selector import Selector
from scrapy.spiders import Spider

from jcmd.items import productItem


#from scrapy.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.spiders.crawl import CrawlSpider, Rule
class product_spider(Spider):
    name = 'product'
    
    allowed_domain = ['china-10.com/']
    
    start_urls = ['http://www.china-10.com/product/92626.html'
                  ]
    
    begin = 365000
    scop = 35000
    i = 0
    while(i<=scop):
        url = 'http://www.china-10.com/product/%d.html' % (begin+i)
        start_urls.append(url)
        i = i + 1
    
    
    #产品url
    rule_url = re.compile(r'[\d]+.html$')
    #获取id规则
    rule_get_id = re.compile(r'[\d]+')
    #产品型号
    rule_get_producttype = re.compile(u'\u4ea7\u54c1\u578b\u53f7')
    #产品规格
    rule_get_productformat = re.compile(u'\u4ea7\u54c1\u89c4\u683c')
    #产品系列
    rule_get_productset = re.compile(u'\u4ea7\u54c1\u7cfb\u5217')
    #信息指数
    rule_get_infonum = re.compile(u'\u4fe1\u606f\u6307\u6570')
    #关注指数
    rule_get_concernnum = re.compile(u'\u5173\u6ce8\u6307\u6570')
    #去除html规则
    rule_remove_html= re.compile(r'<[^>]+>',re.S)
    #空格分隔符
    split_blank = ' '
         
    def parse(self,response):
        
        pItem = productItem()
        
        sel = Selector(response)
        #product的url尾部
        tail= product_spider.rule_url.findall(response.url)[0]
        #得到productid
        pItem['product_id'] = product_spider.rule_get_id.findall(tail)[0]
        #product_name pipe中去除标签
        pItem['product_name']= ""
        #相关品牌信息
        brand_info = sel.xpath(".//div[@class='keywordlist']/div/a[@key='brandid']")
        pItem['brand_id'] = brand_info.xpath("@tid").extract()[0] if brand_info.xpath("@tid").extract() else ""
        pItem['brand_name'] = brand_info.xpath("@qname").extract()[0] if brand_info.xpath("@qname").extract() else ""
        #相关分类信息
        category_info = sel.xpath(".//div[@class='keywordlist']/div/a[@key='catid']")
        pItem['category_id'] = category_info.xpath("@tid").extract()[0] if category_info.xpath("@tid").extract() else ""
        pItem['category_name'] = category_info.xpath("@qname").extract()[0] if category_info.xpath("@qname").extract() else ""
        
        #相关图片
        pItem['image_urls'] = sel.xpath(".//div[@class='topbox']/a/img/@src").extract()
        #产品参数
        pItem['product_data'] = sel.xpath(".//ul[@class='speclist clearfix']/li/@title").extract()
        #其他详细信息
        pItem['url'] = response.url
        pItem['product_type'] = ""
        pItem['product_fomate'] = ""
        pItem['product_set'] = ""
        pItem['product_infonum'] = ""
        pItem['product_concern_num'] = ""
        #产品信息列表
        product_infolist = sel.xpath(".//div[@class='infobox']/ul/li")
        
        
        for pi in product_infolist:
            
            content = pi.extract()[0]
            #content = si.xpath("./span").extract()
            if product_spider.rule_get_producttype.findall(content):
                pItem['product_type'] = pi.xpath("text()").extract()[0]
            elif product_spider.rule_get_productformat.findall(content):
                pItem['product_format'] = pi.xpath("text()").extract()[0]
            elif product_spider.rule_get_productset.findall(content):
                pItem['product_set'] = pi.xpath("text()").extract()[0]
            elif product_spider.rule_get_infonum.findall(content):
                pItem['product_infonum'] = pi.xpath("text()").extract()[0]
            elif product_spider.rule_get_concernnum.findall(content):
                pItem['product_concern_num'] = pi.xpath("text()").extract()[0]
        yield pItem
        
        
        
        
        
        
        