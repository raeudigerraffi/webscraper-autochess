# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import csv
from w3lib.http import basic_auth_header
import random

def standard(input,number):
#function to standardize the data
    std = number - len(input)
    if std == 0 :
        print("10 units")
    else:
        for x in range(0,std):
            input.append("NA")


            
class AutochessTableSpider(scrapy.Spider):
    name = 'autochess_table'
    user_agent = 'Mozilla/5.0'


    def start_requests(self):
            self.index = []
            urls = [
                'https://autochess.op.gg//user/%E6%99%BA%E9%BD%BF%E5%B0%91%E5%A5%B3%E8%8B%B1%E6%A2%A8%E6%A2%A8-128194',
            ]
            fields = ["date","duration","place","rank",'unit1','unit2','unit3','unit4','unit5','unit6','unit7','unit8','unit9','unit10','synergy1','synergy2','synergy3','synergy4','synergy5','synergy6','synergy7','synergy8','synergy9','synergy10','synergy11','synergy12','synergy13','synergy14']
            with open('autochess.csv', 'w') as csV:
            	writer = csv.writer(csV, delimiter=',')
            	writer.writerow(fields)
            csV.close()

            auth = basic_auth_header('user','userpass')
    				
            for url in urls:
                # We make a request to each url and call the parse function on the http response.
                yield SplashRequest(url=url, callback=self.parse,args={'wait':'2'}, splash_headers = {'Authorization': auth})
    


    def parse(self, response):
        div = response.xpath('//div[@id="vue-app"]')
        self.index.append(response.url)
        user_agent_list = [
           #Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            #Firefox
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]
        matches = div.xpath('.//div[@class="kt-portlet__content"]')
        rank = response.xpath('//h3[@style="color: #000; margin-bottom: 0;"]/text()').get()

        auth = basic_auth_header('user','userpass')
        with open ("autochess.csv","a") as file:
        	writer = csv.writer(file, delimiter=',') 		       
	        for match in matches:
	        	
	        	stats = match.xpath('.//td[1]')
	        	legion = match.xpath('.//td[2]')
	        	comp = match.xpath('.//td[3]')
	        	

	        	#extraction of individual items
	        	units = []
	        	synergy = []
	        	
	        	place = stats.xpath('.//b/text()').get()
	        	duration = stats.xpath('.//div[@class="duration text-muted"]/text()').get()
	        	date = stats.xpath('.//div[@class="text-muted"]/@title').get()
	        	
	        	for u in legion.xpath('.//div/div[@style="cursor: pointer;"]') :
	        		name = u.xpath('.//img/@title').get()
	       
	        		stars = len(u.xpath('.//i').getall())
	        		unit = name + " "+ str(stars)+","
	        		units.append(unit)
	        	


	        	
	        	for x in comp.xpath('.//div'):
	        		syn = x.xpath('.//span/text()').get()
	        		synergy.append(syn)

	        	standard(units,10)
	        	standard(synergy,14)

	        	result =[date,duration,place[1],rank] 
	        	for x in units:
	        		result.append(x)
	        	for s in synergy:
	        		result.append(s)
	        	self.log("Match-------->")
	        	self.log(result)
	        	
        	
        		writer.writerow(result)
        	file.close()
        	

        players = div.xpath('.//div[@class="kt-portlet__content"]//td[4]//div//a/@href').getall()
        		
        for l in players:
        		
        		k = "https://autochess.op.gg/"
        		link = k + l
        		
        		if link in self.index:
        			
        			continue
        		user_agent = random.choice(user_agent_list)
        		yield SplashRequest(url = link, callback=self.parse,args={'wait':'2'},splash_headers = {'Authorization': auth,'User-Agent': user_agent})
			
      
      
        
		
