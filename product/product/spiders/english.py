import scrapy

from urllib.parse import urlencode
from ..items import ProductItem
from bs4 import BeautifulSoup


API_KEY='ff3cc8159137f06335075d726050e683'

headers = {

    "authority": "www.englishhome.com",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.6",
    "cache-control": "no-cache",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

# def get_scraperapi_url(url):
#     payload = {'api_key': API_KEY, 'url': url , 'keep_headers':'true'}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
#     return proxy_url

class EnglishSpider(scrapy.Spider):
    name = "english"
    #allowed_domains = ["englishhome.com"]
    #product_url = "https://www.englishhome.com/absy-zen-dokuma-hali-160x230-cm-lacivert/"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'FEEDS':{
            'englishome_data.json':{
                'format':'json',
                'overwrite':True
            }
        }
    }    
    def start_requests(self):
        #return super().start_requests()
        #url = "https://www.englishhome.com" + i['absolute_url']
            
        #url_link= get_scraperapi_url(url=self.product_url)
        
        yield scrapy.Request(url=self.product_url,headers=headers, callback=self.parse)
    def parse(self, response):
        items = ProductItem()
        
        data = response.json()
        urls =[]


        
        if len(data['variants']) > 0:
            for size in data['variants'][0]['options']:
                #print(type(color['is_selected']), color['is_selected'])
                if not (size['is_selected']):
                    #current_color = color['label']
                
                    product_url= "https://www.englishhome.com" + size['product']['absolute_url']
                    urls.append(product_url)

                else:
                    continue
        if len(data['variants']) > 0:
            for counter , item  in enumerate(data['variants']):
                try:
                    for i in item['options'][counter]['product']['attributes'].keys():
                        if i == "Description":
                            description=data['variants'][counter]['options'][counter]['product']['attributes']['Description']
                except IndexError:
                    break
            
        try:           
            if description != '':   
                soup = BeautifulSoup(description,'lxml')
                description = soup.get_text(strip=True).strip().replace('\n'," ")
        except UnboundLocalError:
            description=''
            
        if len(data['variants']) > 0:      
            for size in data['variants'][1]['options']:
                if not (size['is_selected']):

                
                    product_url= "https://www.englishhome.com" + size['product']['absolute_url']
           
                    urls.append(product_url)
                else:
                    continue
                
        
        try:      
            name = data['selected_variant']['name']
            product_code = data['selected_variant']['attributes']['integration_sku_int']
            list_price = data['selected_variant']['price']
            price =data['selected_variant']['retail_price']
            scrap_url = "https://www.englishhome.com" + data['selected_variant']['absolute_url']
            qty = data['selected_variant']['stock']
            # try:
            #     items['color'] = data['selected_variant']['attributes_kwargs']['integration_color']['label']
            # except:
            #     items['color']=data['selected_variant']['absolute_url'].split('-')[-1].replace('/','')
            # try:
            #     items['size'] = data['selected_variant']['attributes_kwargs']['integration_size']['label']
            # except:
            #     items['size']= ''
            try:
                items['category'] = data['selected_variant']['attributes']['integration_material_group_desc']
            except KeyError:
                items['category'] = data['selected_variant']['attributes']['erp_material_group_desc']
                
        except TypeError:
            name = data['product']['name']
            
            product_code = data['product']['attributes']['integration_sku_int']
            
            list_price = data['product']['price']
            
            price =data['product']['retail_price']
            
            scrap_url = "https://www.englishhome.com" + data['product']['absolute_url']
            
            qty = data['product']['stock']
            
            # try:
            #     items['color'] = data['product']['attributes_kwargs']['integration_color']['label']
            # except:
            #     items['color']=data['product']['absolute_url'].split('-')[-1].replace('/','')
            # try:
            #     items['size'] = data['product']['attributes_kwargs']['integration_size']['label']
            # except:
            #     items['size']=''
            try:
                items['category'] = data['product']['attributes']['integration_material_group_desc']
            except KeyError:
                items['category']=data['product']['attributes']['erp_material_group_desc']
            
        items['name'] = name
        
        items['brand'] = "English Home"
        
        
        items['product_code'] = product_code
        

        
        #items['description'] = description
        
        
        items['list_price'] = list_price
        
        
        items['price'] = price
        
        
        items['scrap_url'] = scrap_url
        
        
        items['qty'] = qty
        

        

        # try:
        #     for counter,image in enumerate(data['selected_variant']['productimage_set'],start=1):
        #         image_src = image['image']
        #         items[f'image{counter}'] = image_src
        # except:
        #     for counter,image in enumerate(data['product']['productimage_set'],start=1):
        #         image_src = image['image']
        #         items[f'image{counter}'] = image_src
            
            
        yield items
        res = [*set(urls)]

        for url in res:
            #print(url)
            #url=get_scraperapi_url(url)
            yield scrapy.Request(url=url, headers=headers,callback=self.parse)
