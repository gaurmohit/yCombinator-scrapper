from scrapy.spiders import Spider
from scrapy import Request
from assign.items import AssignItem
from assign.mongo import Process


class NewsSpider(Spider):
    name = "blog_scrap"
    # count = 0
    obj = Process()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        "Host": "httpbin.org",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        'Referer': 'https://news.ycombinator.com/',
    }

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    #
    # }

    # allowed_domains = []

    def start_requests(self):
        url = "https://news.ycombinator.com"
        yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        # get all the rows in the article table 
        articles = response.xpath("//table[@class= 'itemlist']")
        # get the id of every blog
        item_ids = articles.xpath("//tr[@class= 'athing']/@id").extract()

        # Iterate over blogs using id
        for id in item_ids:
            item = AssignItem()

            # get the heading of the blog and in case the title is empty then None is saved
            item['header'] = articles.xpath(
                "//tr[@id= %s]/td[@class= 'title']/a[@class= 'storylink']/text()" % id).extract_first()

            # get the url of the blog and in case the url is empty then None is saved
            item['url'] = response.xpath(
                "//tr[@id= %s]/td[@class= 'title']/a[@class= 'storylink']/@href" % id).extract_first()

            # get vote count for every blog and in case vote count is absent then None is saved
            vote = response.xpath("//td[@class= 'subtext']/span[@id= 'score_%s']/text()" % id).extract_first()
            if vote:
                item['vote'] = int(vote.split()[0])
            else:
                item['vote'] = None

            # yield item 

            if item['url']:
                yield Request(url=item['url'], headers=self.headers, callback=self.parse_sublink, meta={'item': item})

    def parse_sublink(self, response):
        item = response.meta['item']
        item['image'] = response.xpath("//img/@src").extract()
        item['desc'] = response.xpath("//p/text()").extract_first()
        # self.count += 1
        # get the title after opening the corresponding link of the post or None
        item['title'] = response.xpath("//title/text()").extract_first()
        # print(self.count)
        self.obj.process(item)
        yield item
