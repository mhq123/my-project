import scrapy
from bs4 import BeautifulSoup
from ..items import Jobui1Item

class JobuiSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['www.jobui.com']
    start_urls = ['https://www.jobui.com/rank/company/']


    def parse(self,response):
        soup = BeautifulSoup(response.text,'html.parser')
        url_list = soup.find_all('ul',class_='textList flsty cfix')
        for url in url_list:
            a_list = url.find_all('a')
            for a in a_list:
                company_id = a['href']
                url = 'https://www.jobui.com{id}jobs/'
                real_url = url.format(id=company_id)
                yield scrapy.Request(real_url,callback=self.parse_job)

    def parse_job(self,response):
        soup = BeautifulSoup(response.text,'html.parser')
        company = soup.find(id='companyH1').text
        datas = soup.find_all('div',class_='job-simple-content')
        for data in datas:
            item = Jobui1Item()
            item['company'] = company
            item['job'] = data.find('div',class_='job-segmetation').find('h3').text
            item['address'] = data.find('div',class_='job-desc').find('span').text
            item['detail'] = data.find('div',class_='job-desc').find('span').text
            yield item

