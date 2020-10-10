# Scrapy settings for movie project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'movie'

SPIDER_MODULES = ['movie.spiders']
NEWSPIDER_MODULE = 'movie.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'movie (+http://www.yourdomain.com)'
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    # 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10',
    # 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)',
    # 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5',
    # 'Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; '
    # '.NET4.0E)',
    # 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    # 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    # 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2',
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
]

import random

USER_AGENT = random.choice(USER_AGENT_LIST)

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     # 'Accept-Language': 'en',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
#     'Cookie': 'uuid_n_v=v1; uuid=E8B8B530006811EB8026CDB2BA3E8FD439E453FC2C1D4123A0F9155857AECEC6; '
#               'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1601173617,1601201367; '
#               'mojo-uuid=d6f71e9e9b340709e0abe0b8b5057517; '
#               '_lxsdk_cuid=174cd62911662-01d21c8e39ab768-4c3f247a-144000-174cd6291179e; '
#               '_lxsdk=E8B8B530006811EB8026CDB2BA3E8FD439E453FC2C1D4123A0F9155857AECEC6; '
#               '__mta=250920249.1601173623167.1601174301571.1601201368530.5; '
#               '_csrf=6e6c5421cbf80c5da3104fae2320e3b71ebe5eeb9f2fe30e3701a0073475621f; '
#               '_lxsdk_s=174cf09e7ce-0e1-956-f7b%7C%7C2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1601201367; '
#               'mojo-trace-id=1; mojo-session-id={"id":"cd42c8d693e39f5dd08838220b40dcd4","time":1601201367100} '
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'movie.middlewares.MovieSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'movie.middlewares.MovieDownloaderMiddleware': 543,
    'movie.middlewares.MyProxyMiddleware': 350,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'movie.pipelines.MoviePipeline2SQL': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MY_PROXIES = ['http://183.207.95.27:80', 'http://111.6.100.99:80', 'http://122.72.99.103:80',
              'http://106.46.132.2:80', 'http://112.16.4.99:81', 'http://123.58.166.113:9000',
              'http://118.178.124.33:3128', 'http://116.62.11.138:3128', 'http://121.42.176.133:3128',
              'http://111.13.2.131:80', 'http://111.13.7.117:80', 'http://121.248.112.20:3128',
              'http://112.5.56.108:3128', 'http://42.51.26.79:3128', 'http://183.232.65.201:3128',
              'http://118.190.14.150:3128', 'http://123.57.221.41:3128', 'http://183.232.65.203:3128',
              'http://166.111.77.32:3128', 'http://42.202.130.246:3128', 'http://122.228.25.97:8101',
              'http://61.136.163.245:3128', 'http://121.40.23.227:3128', 'http://123.96.6.216:808',
              'http://59.61.72.202:8080', 'http://114.141.166.242:80', 'http://61.136.163.246:3128',
              'http://60.31.239.166:3128', 'http://114.55.31.115:3128', 'http://202.85.213.220:3128']

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3366
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'test'
MYSQL_CHARSET = 'utf8mb4'