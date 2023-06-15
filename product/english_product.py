from product.spiders.english import EnglishSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sys import argv


url=argv[1]
#"https://www.englishhome.com/absy-zen-dokuma-hali-160x230-cm-lacivert/"
def main(): 
    settiings=get_project_settings()
    process = CrawlerProcess(settings=settiings)
    process.crawl(EnglishSpider,product_url=url)
    process.start()
    
if __name__ == '__main__':
    main()