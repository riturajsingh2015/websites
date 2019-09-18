# -*- coding: utf-8 -*-
import csv
from scrapy import Spider
from selenium import webdriver
from time import sleep
#from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from parsel import Selector
class ScrapLinkedinSpider(Spider):
    name = 'scrap_linkedin'
    allowed_domains = ['linkedin.com']
    start_urls = ['http://linkedin.com/']

    def start_requests(self): # this function will not have response ,
    # since there is no start_url defined here.

        writer=csv.writer(open('myfile.csv','w'))
        writer.writerow(['Name','Job Title', 'Current URL'])

        self.driver = webdriver.Chrome(r'C:\Users\Singh\Downloads\chromedriver_win32\chromedriver.exe')
        site_url='https://www.linkedin.com/'
        self.driver.get(site_url)
        sign_in_button=self.driver.find_element_by_xpath('//a[text()="Sign in"]')
        self.logger.info('Sleeping for 3 Seconds.')
        sign_in_button.click()
        sleep(3)
        #page_source=self.driver.page_source
        #sel=Selector(text=page_source)
        username=self.driver.find_element_by_id("username")
        sleep(0.5)
        password=self.driver.find_element_by_id("password")
        sleep(0.5)
        sign_in_button=self.driver.find_element_by_xpath('//button[text()="Sign in"]')
        sleep(0.5)
        myusername=input('Enter your LinkedIn Username/Email ID : ')
        mypassword=input('Enter your LinkedIn Password : ')
        username.send_keys(myusername)
        password.send_keys(mypassword)
        sign_in_button.click()
        sleep(5)

        site_url='https://www.google.com/'
        self.driver.get(site_url)
        search_query=self.driver.find_element_by_name("q")
        search_key_job_profile=input('Enter Job Profile You want to search like python developer/java developer : ')
        search_key_city=input('Enter the city in the world in which you want to search the person : ')
        search_query_string='site:linkedin.com/in/ AND "{}" AND "{}"'.format(search_key_job_profile,search_key_city)
        search_query.send_keys(search_query_string)
        search_query.send_keys(Keys.RETURN)
        parents=self.driver.find_elements_by_css_selector(".r a")
        urls_per_page=[]
        for parent in parents:
            url=parent.get_attribute("href")
            urls_per_page.append(url)
        for url in urls_per_page:
            self.driver.get(url)
            sleep(3)
            sel= Selector(text=self.driver.page_source)
            name=sel.xpath('//*[@id="ember45"]/div[2]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first()
            job_profile=sel.xpath('//*[@id="ember45"]/div[2]/div[2]/div[1]/h2[1]/text()').extract_first()
            try:
                print('Name ' , name)
                print('Job Profile' , job_profile)
                writer.writerow([name.encode('utf-8'),job_profile.encode('utf-8'), url.encode('utf-8')])
            except:
                pass

        self.driver.close()
