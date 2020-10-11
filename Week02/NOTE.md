[TOC]

# 本周 Highlight

## 异常处理最佳实践
**合理使用异常处理**

参考： 
https://www.zlovezl.cn/articles/three-rituals-of-exceptions-handling/

> 1. 单个函数不要返回多种类型，可以用抛出异常的方式实现对参数的校验，用抛出异常替代返回错误结果
> 1. 只捕获可能会抛出异常的语句，避免含糊的捕获逻辑
> 1. 保持模块异常类的抽象一致性，必要时对底层异常类进行包装
> 1. 使用“上下文管理器(context manager)”可以简化重复的异常处理逻辑
> 1. 使用trackback打印更详细的异常信息

## 常见的反爬虫机制有哪些？
1. 合理地模拟浏览器headers，确保其包含的User agent与正常的浏览器行为类似。
>   因为服务器后台对访问的User_Agent进行统计，单位时间内同一User_Agent访问的次数超过特定的阀值，则会被不同程度的封禁IP，
>   从而造成无法进行爬虫的状况。
2. 合理的切换IP地址
>   因为后台服务器对访问进行统计，单位时间内同一IP访问的次数超过一个特定的值（阀值），就会不同程度的禁封IP，导致无法进行爬虫操作。
3. 设置合理的IP访问频率。背后的策略是分布式爬虫，
>  Scrapy-Redis是分布式爬虫的工具之一。它与Redis结合，将request网址从start_urls中分离出来，改为从redis中读取，多个客户端可以同时
>   读取一个redis，从而实现分布式爬虫。
>  首先Slaver端从Master端拿任务（Request、url）进行数据抓取，Slaver抓取数据的同时，产生新任务的Request便提交给 Master 处理；
>  Master端只有一个Redis数据库，负责将未处理的Request去重和任务分配，将处理后的Request加入待爬队列，并且存储爬取的数据。
4. 模拟登录—浏览器登录的爬取
> 设置一个cookie处理对象，它负责将cookie添加到http请求中，并能从http响应中得到cookie，向网站登录页面发送一个请求Request, 
 包括登录url，cookie等完整信息。

## 分布式爬虫原理
如果爬虫要处理的数据比较少，单机运行就可以，但如果目标网站数据量很大，这个时候就需要使用分布式爬虫，以便提高爬虫效率。
Scrapy-Redis是典型的分布式爬虫，原理就是待抓取request请求信息和数据items信息的存取放到redis queue里，使多台服务器可以
同时执行crawl和items process，大大提升了数据爬取和处理的效率。

# 本周知识点记录
## 2.1 异常捕获与处理
### 如何使用except同时处理多个异常类型？
```
try:
   ......................
except(Exception1[, Exception2[,...ExceptionN]]]):
   ......................
else:
```
### 如何更好的打印异常结果?
可以使用trackback打印更详细的异常信息
```
def to_digital(a):
    try:
        return int(a)
    except ValueError as ex:
        print(ex)

print(to_digital('12'))
print(to_digital('qwe'))
```
返回结果：invalid literal for int() with base 10: 'qwe'

### 如何避免太多处理异常的冗余代码
在下面的函数中有针对输入参数的异常处理，那是否有方法可以简化这段代码呢？
答案是有的，但这里的方法仅仅是一个例子，它虽然简化了异常处理代码，但却导致异常信息无法输出，所以也不算是最佳实践。
```
class NULLAccount:
    name = ''
    balance = 0

    @classmethod
    def to_account(cls, s: str):
        raise NotImplementedError


class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    @classmethod
    def to_account(self, s):
        try:
            name, balance = s.split()
            balance = float(balance)
        except ValueError:
            return NULLAccount(s)
        if balance < 0:
            return NULLAccount(s)
        return Account(name, balance)


def get_total_balance(users):
    results = sum(Account.to_account(s).balance for s in accounts)
    return results

accounts = [
    'alice 19000',
    'eva 2145',
    'jim 34980',
    'invalid-user',
    'invalid-user, -30',
    'invalid-user $320.8'
]
print(get_total_balance(accounts))
```
修改后的代码：使用NullAccount避免处理输入参数导致的异常
```
class NULLAccount:
    name = ''
    balance = 0

    @classmethod
    def to_account(cls, s: str):
        raise NotImplementedError


class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    @classmethod
    def to_account(self, s):
        try:
            name, balance = s.split()
            balance = float(balance)
        except ValueError:
            return NULLAccount(s)
        if balance < 0:
            return NULLAccount(s)
        return Account(name, balance)

def get_total_balance(users):
    results = sum(Account.to_account(s).balance for s in accounts)
    return results
```

## 2.2 使用PyMySQL进行数据库操作

## 2.3 反爬虫：模拟浏览器头部
**Python库fake_useragent**
>   UserAgent是识别浏览器的一串字符串，相当于浏览器的身份证，在利用爬虫爬取网站数据时，频繁更换UserAgent可以避免触发相应的反爬机制。fake-useragent对频繁更换UserAgent提供了很好的支持.
**fake_useragent 出现time out error 如何解决？**
>   Reference：
>   https://blog.csdn.net/qq_39360343/article/details/106019841?depth_1-
>   https://tding.top/archives/3caecd5b.html

**HTTP中Referer 的定义和作用**
>   1. 定义：Referer是HTTP请求Header的一部分，Referer会告诉服务器当前request是从哪个页面链接过来的。
>   2. 作用：安全范围检测, 服务器有时候只接受某些可接受的安全链接，所以它需要检查referer当前HTTP request是否安全。

## 2.4 Cookies验证

**HTTP code 302 -- 重定向**
> 1. 302作用：网页重定向作用类似呼叫转移操作
> 2. 301与302都是重定向状态，301表示永久性地转移到新位置，例如网站地址发生变化，希望用户直接访问新网址。
>   302 表示临时移动到某个路径下面。

**Http中如何通过form-data进行cookies登陆验证**
![avatar](D:\01_Projects\Github\Python-202009\week2/cookies_form_data.png)

## 2.5 使用WebDriver模拟浏览器行为
**WebDriver**
> WebDriver is a clean, fast framework for automated testing of webapps.
> WebDriver是浏览器自动操作工具Selenium的一部分。Selenium主要由三种工具组成。
> 第一个工具SeleniumIDE，是Firefox的扩展插件，支持用户录制和回访测试。
>录制/回访模式存在局限性，对许多用户来说并不适合，
>因此第二个工具——Selenium WebDriver提供了各种语言环境的API来支持更多控制权和编写符合标准软件开发实践的应用程序。
>最后一个工具——SeleniumGrid帮助工程师使用Selenium API控制分布在一系列机器上的浏览器实例，支持并发运行更多测试。

**WebDriver常用接口函数**
> 1. id定位：find_element_by_id()
> 2. name定位：find_element_by_name()
> 3. class定位：find_element_by_class()
> 4. tag定位：find_element_by_tag_name()
> 5. link定位：find_element_by_link_text()
> 6. partial link 定位： find_element_by_partial_link_text()
> 7. CSS定位：find_element_by_css_selector()
> 8. Xpath定位绝对路径：find_element_by_xpath("/html/body/div[x]/div[x]/div/div/dl[x]/dt/a")
> 9. Xpath定位元素属性：find_element_by_xpath("//unput[@id=‘kw’]")
> 10. Xpath定位层级与属性结合：find_element_by_xpath("//form[@id=‘loginForm’]/ul/input[1]")
> 11. Xpath定位逻辑运算符：find_element_by_xpath("//input[@id=‘kw’ and@class=‘s_ipt’]")

**Chrome driver**
> 使用WebDriver时候会用到浏览器的API接口，所以需要按照对应的浏览器接口文件。

## 2.6 验证码识别 -- 基于图像识别技术
对图像类型的验证码识别进行识别，需要进行图像识别操作。验证码识别依赖的工具包：
> 1. libpng, jped, libtiff, leptonica 支持不同图像格式
> 2. tesseract：Tesseract是一个开源的OCR（Optical Character Recognition，光学字符识别）引擎，可以识别多种格式的图像文件并将其转换成文本，目前已支持60多种语言（包括中文）。 Tesseract最初由HP公司开发，后来由Google维护。
> 3. pytesseract：用于图片转文字
> 4. pillow：python中进行图像操作的库

图像识别的大致流程：
> 1. 图像灰度化
> 2. 二值化
> 3. 识别

## 2.7 爬虫中间件&系统代理IP
**Scrapy download middleware**
> 1. 下载器中间件是介于Scrapy的request/response处理的钩子框架，是用于全局修改Scrapy request和response的一个轻量、底层的系统
> 2. 下载器常见的功能应用场景：更换代理IP，更换Cookies，更换User-Agent，自动重试。

**Scrapy download middleware激活**
> 激活中间件要在settings.py文件中设置DOWNLOADER_MIDDLEWARES. 其中包括一个数字项.这个数字描述的是是中间件的优先级.
> 数字越小,优先级越高,对应的request会优先处理. 设置None则是关闭中间件.
```
DOWNLOADERMIDDLEWARES = {
    'myproject.middlewares.Custom_A_DownloaderMiddleware': 543,
    'myproject.middlewares.Custom_B_DownloaderMiddleware': 643,
    'myproject.middlewares.Custom_B_DownloaderMiddleware': None,
}
```
## 2.8 自定义中间件
## 2.9 分布式爬虫
