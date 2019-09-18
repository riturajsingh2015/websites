# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request , FormRequest
class EplanningSpider(Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        #pass
        urls=response.xpath("//a/@href").extract()
        urls =[url for url in urls if 'eplanning.ie' in url]
        for url in urls[0:1]: # you can change this line if you want to go through all the county's
            yield Request(url, callback=self.parse_application)

    def parse_application(self, response):
        #print('In the search Page Clicking the Received Applications Button')
        rc_button=response.xpath("/html/body/div[2]/div/div/div[2]/div[1]/a/@href").extract_first()
        rc_button=response.urljoin(rc_button)
        yield Request(rc_button,callback=self.parse_form)

    def parse_form(self, response):
        yield FormRequest.from_response(response,
                                        formdata={'RdoTimeLimit': '28',
                                        'AppStatus': '1'
                                        },
                                        formnumber=1,
                                        callback=self.parse_pages
                                        )
    def parse_pages(self,response):
        application_urls=(response.xpath('//td/a/@href').extract())
        for url in application_urls:
            url=response.urljoin(url)
            yield Request(url,callback=self.parse_items)
        next_button = response.xpath('//*[@class="PagedList-skipToNext"]/a/@href').extract_first()

        if next_button:
            next_button_url= response.urljoin(next_button)
            yield Request(next_button_url, callback=self.parse_pages)



    def parse_items(self,response):
        #
        #

        agent_btn_style=response.xpath('//*[@value="Agents"]/@style').extract_first()
        if 'visible' in agent_btn_style:
            #print('Extracting the info')
            name=response.xpath('//tr[th="Name :"]/td/text()').extract_first() # select all tr's with th value = Name :
            #then get its td's text
            phone=response.xpath('//tr[th="Phone :"]/td/text()').extract_first()
            fax=response.xpath('//tr[th="Fax :"]/td/text()').extract_first()
            e_mail=response.xpath('//tr[th="e-mail :"]/td/a/text()').extract_first()
            url= response.url
            yield {
            'name':name,
            'phone':phone,
            'fax':fax,
            'e_mail':e_mail,
            'url':url
            }

        else:
            self.logger.info('Agent Button not found !')
