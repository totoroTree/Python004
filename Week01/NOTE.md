[TOC]

#学习笔记

## Highlights in this week
### Packages:
1. Requests: 请求网络连接的库
2. BeautifulSoup: BeautifulSoup支持Python的HTML解析器.
3. Xpath: XPath 是一门在XML文档中查找信息的语言。XPath可用来在XML文档中对元素和属性进行遍历。
4. Scrapy: Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架。 可以应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。

### 爬虫原理：

### 爬虫工作流程：
1. 获取初始的url模拟浏览器发送网络请求
    使用HTTP协议向目标网站发送请求。有效的request中一般包含下面参数：
    1) 目标url地址
    2) headers: 包含user-agent, cookies 等参数。这些参数可以从浏览器中获取。
2. 获取响应数据
    如果目标网站相应成功（返回200标识码），一般会得到一个HTML类型的response，其中包含了所需要的信息。
3. 解析响应数据
    解析HMTL文本数据，可以用正则表达式，也可以用已有工具，如xPath，selector等。
4. 保存解析后的数据

### Scrapy workflow
#####  Install Scrapy
https://docs.scrapy.org/en/latest/intro/install.html#intro-install
##### Creating a project
```
scrapy startproject movie
cd movie
scrapy genspider maoyan maoyan.com
```
A project can contains multiply spiders. The above command will create a tutorial directory with the following contents:
```
movie/
    scrapy.cfg            # deploy configuration file

    movie/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py 
            maoyan.py     # a file where you'll later customized your spiders
```
##### Generate the first Spider
Create a spider class named test_spider.py under the folder **tutorial/spider/** directory.
The spider class would includes the followed methods and attributes:
    1) name: identify the Spider within the project
    2) start_requests(): a method returning a Request that the spider can start to work on.
    3) parse(): it will be called when handling the response, it will extract the data we wanted.

Also, please update the followed 
##### Run the spider
Run the followed command to start a spider.
```
scrapy crawl maoyan
```
If the output are as followed, it means the crawl works fine
```
2020-09-27 20:12:50 [scrapy.utils.log] INFO: Scrapy 2.3.0 started (bot: movie)
2020-09-27 20:12:50 [scrapy.utils.log] INFO: Versions: lxml 4.5.0.0, libxml2 2.9.5, cssselect 1.1.0, parsel 1.6.0, w3lib 1.22.0, Twisted 20.3.0, Python 3.7.6 (tags/v3.7.6:43364a7ae0, Dec 19 2019, 00:42:30) [MSC v.1916 64 bit (AMD64)
], pyOpenSSL 19.1.0 (OpenSSL 1.1.1h  22 Sep 2020), cryptography 3.1.1, Platform Windows-10-10.0.17134-SP0
2020-09-27 20:12:50 [scrapy.utils.log] DEBUG: Using reactor: twisted.internet.selectreactor.SelectReactor
2020-09-27 20:12:50 [scrapy.crawler] INFO: Overridden settings:
{'BOT_NAME': 'movie',
 'COOKIES_ENABLED': False,
 'DOWNLOAD_DELAY': 3,
 'NEWSPIDER_MODULE': 'movie.spiders',
 'ROBOTSTXT_OBEY': True,
 'SPIDER_MODULES': ['movie.spiders']}
2020-09-27 20:12:50 [scrapy.extensions.telnet] INFO: Telnet Password: 7e8b9acbe65854dc
2020-09-27 20:12:50 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.logstats.LogStats']
2020-09-27 20:12:51 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware',
 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2020-09-27 20:12:51 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2020-09-27 20:12:51 [scrapy.middleware] INFO: Enabled item pipelines:
['movie.pipelines.MoviePipeline']
2020-09-27 20:12:51 [scrapy.core.engine] INFO: Spider opened
2020-09-27 20:12:51 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2020-09-27 20:12:51 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023
2020-09-27 20:12:53 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://maoyan.com/robots.txt> (referer: None)
2020-09-27 20:12:56 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://maoyan.com/films?showType=3> (referer: None)
2020-09-27 20:12:56 [scrapy.core.scraper] DEBUG: Scraped from <200 https://maoyan.com/films?showType=3>
{'category': '爱情／喜剧', 'name': '我的女友是机器人', 'release_time': '2020-09-11'}
2020-09-27 20:12:56 [scrapy.core.scraper] DEBUG: Scraped from <200 https://maoyan.com/films?showType=3>
{'category': '爱情／奇幻／喜剧', 'name': '我在时间尽头等你', 'release_time': '2020-08-25'}
2020-09-27 20:12:56 [scrapy.core.scraper] DEBUG: Scraped from <200 https://maoyan.com/films?showType=3>
{'category': '剧情', 'name': '夺冠', 'release_time': '2020-09-25'}
2020-09-27 20:12:56 [scrapy.core.scraper] DEBUG: Scraped from <200 https://maoyan.com/films?showType=3>
{'category': '剧情／战争／历史', 'name': '八佰', 'release_time': '2020-08-21'}
2020-09-27 20:12:56 [scrapy.core.scraper] DEBUG: Scraped from <200 https://maoyan.com/films?showType=3>
{'category': '剧情／冒险', 'name': '花木兰', 'release_time': '2020-09-11'}
2020-09-27 20:12:56 [scrapy.core.scraper] DEBUG: Scraped from <200 https://maoyan.com/films?showType=3>
{'category': '科幻／动作／剧情', 'name': '信条', 'release_time': '2020-09-04'}
2020-09-27 20:12:56 [scrapy.core.scraper] DEBUG: Scraped from <200 https://maoyan.com/films?showType=3>
{'category': '纪录片／战争／历史', 'name': '蓝色防线', 'release_time': '2020-09-18'}
2020-09-27 20:12:56 [scrapy.core.scraper] DEBUG: Scraped from <200 https://maoyan.com/films?showType=3>
{'category': '剧情／爱情', 'name': '荞麦疯长', 'release_time': '2020-08-25'}
2020-09-27 20:12:56 [scrapy.core.scraper] DEBUG: Scraped from <200 https://maoyan.com/films?showType=3>
{'category': '剧情', 'name': '我和我的祖国', 'release_time': '2019-09-30'}
2020-09-27 20:12:56 [scrapy.core.scraper] DEBUG: Scraped from <200 https://maoyan.com/films?showType=3>
{'category': '剧情', 'name': '麦路人', 'release_time': '2020-09-17'}
2020-09-27 20:12:56 [scrapy.core.engine] INFO: Closing spider (finished)
**************************************************************************************************
2020-09-27 20:12:56 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 1686,
 'downloader/request_count': 2,
 'downloader/request_method_count/GET': 2,
 'downloader/response_bytes': 11931,
 'downloader/response_count': 2,
 'downloader/response_status_count/200': 2,
 'elapsed_time_seconds': 5.368455,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2020, 9, 27, 12, 12, 56, 729260),
 'item_scraped_count': 10,
 'log_count/DEBUG': 12,
 'log_count/INFO': 10,
 'response_received_count': 2,
 'robotstxt/request_count': 1,
 'robotstxt/response_count': 1,
 'robotstxt/response_status_count/200': 1,
 'scheduler/dequeued': 1,
 'scheduler/dequeued/memory': 1,
 'scheduler/enqueued': 1,
 'scheduler/enqueued/memory': 1,
 'start_time': datetime.datetime(2020, 9, 27, 12, 12, 51, 360805)}
2020-09-27 20:12:56 [scrapy.core.engine] INFO: Spider closed (finished)
```

## Trouble-shooting
### Scrapy
1. 如何在Scrapy中设置Cookie -- 方案一：setting文件中设置cookie

    当COOKIES_ENABLED是注释的时候scrapy默认没有开启cookie
    当COOKIES_ENABLED没有注释设置为False的时候scrapy默认使用了settings里面的cookie
    当COOKIES_ENABLED设置为True的时候scrapy就会把settings的cookie关掉，使用自定义cookie
    所以当我使用settings的cookie的时候，又把COOKIES_ENABLED设置为True，scrapy就会把settings的cookie关闭，
    而且我也没使用自定义cookie，导致整个请求根本没有cookie,导致获取页面失败。

    总结：
    如果使用自定义cookie就把COOKIES_ENABLED设置为True
    如果使用settings的cookie就把COOKIES_ENABLED设置为False
 2. Scrapy 运行过程中无法获取movie网页数据
    Request 中增加cookie
3. Scrapy 运行后没有任何数据输出
   根本原因是数据XPath数据解析错误，这个时候需要：
   1） 打印Response.text确认是否是所需要的网页
   2）逐个校验XPath数据解析部分，可以用PDB调试模式下逐个打印目标值，确保解析正确
   

## 练习Code
### Parser HTTP response with BeautifulSoup
```
def spider_requests_bs():
    """
    Parser HTTP response with BeautifulSoup
    """
    results = []
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ' \
                 'like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
    header = {'user-agent': user_agent}
    myurl = "https://www.gushiwen.org/gushi/tangshi.aspx"
    # requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(10054, 'An existing
    # connection was forcibly closed by the remote host', None, 10054, None))
    response = requests.get(myurl, headers=header)
    bs_info = bs(response.text, 'html.parser')
    counter = 0
    for tags in bs_info.find_all('div', attrs={'class': 'typecont'}):
        for atag in tags.find_all('a', ):
            link = atag.get('href')
            title = atag.next
            author = atag.nextSibling
            results.append({'link': link, 'title': title, 'author': author})
    print(*results, sep='\n')
```

### Parser with XPath
```
def get_movie(url):
    """
    Parser HTTP response with XPath
        :param: url, the request url address
        :return: a list of movies information, including: name, rating, time
    """
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ' \
                 'like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
    header = {'user-agent': user_agent}
    response = requests.get(url, headers=header)
    selector = lxml.etree.HTML(response.text)

    file_name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')
    rating = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
    time = selector.xpath('//*[@id="info"]/span[10]/text()')
    mylist = [file_name, rating, time]
    return mylist
```

### Spider with Scrapy
```
import scrapy
from bs4 import BeautifulSoup as bs
from doubanMovie.items import DoubanMovieItem
from scrapy.selector import Selector

class MoviesSpider(scrapy.Spider):
    name = 'doubanMovie'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/top250']

    # def parse(self, response):
    #     pass

    def start_requests(self):
        for i in range(0, 10):
            url = f'http://douban.com/top250?start={i * 25}'
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        items = []
        soup = bs(response.txt, 'html.parse')
        title_list = soup.find_all('div', attrs={'class': 'hd'})
        # for i in range(len(title_list)):
        for i in title_list:
            item = DoubanMovieItem()
            title = i.find('a').get('span', ).text
            url = i.find('a').get('href')
            item['title'] = title
            item['link'] = url
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        soup = bs(response.text, 'html.parser')
        content = soup.find('div', attrs={'class': 'related-info'}).get_text().strip()
        item['content'] = content
        yield item


class MoviesSpider2(scrapy.Spider):
    name = 'doubanMovie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://douban.com/top250']

    def start_requests(self):
        i = 0
        url = f'http://movie.douban.com/top250?start={i * 25}'
        print(url)
        yield scrapy.Request(url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        print(response.url)
        movies = Selector(response=response).xpath('//div[@class="hd"]')
        for movies in movies:
            # title = [<Selector xpath='./a/span/text()' data='疯狂动物城'>, <Selector xpath='./a/span/text()'
            # data='\xa0/\xa0Zootopia'>, <Selector xpath='./a/span/text()' data='\xa0/\xa0优兽大都会(港)  / 动物方城市(台)'>]
            title = movies.xpath('./a/span/text()')
            # link = [<Selector xpath='./a/@href' data='https://movie.douban.com/subject/2566...'>]
            link = movies.xpath('./a/@href')
            print('-------------------')
            print(title)
            print(link)
            print('---------')
            print(title.extract())
            print(link.extract())
            print(title.extract_first())
            print(link.extract_first())
            print(title.extract_first().strip())
            print(link.extract_first().strip())

if __name__ == '__main__':
    spider = MoviesSpider2()
    spider.start_requests()

```