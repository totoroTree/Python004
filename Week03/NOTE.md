[TOC]

# 本周Highlight
# Troubleshooting
# 本质知识点汇总
## 3.1 Scrapy并发参数优化原理

**Scrapy参数中三个设置项来控制下载器的容量**
性能优化时需要先考虑两个因素:
1. 目标网站的承载
2. 爬虫机器的CPU及运行能力

然后可以考虑设置下面的参数对并行进行设置
> 1. DOWNLOAD_DELAY # 下载延时，限制爬虫速度，防止过快被封, 当有CONCURRENT_REQUESTS，有DOWNLOAD_DELAY 时，服务器不会在同一时间收到大量的请求
> 2. CONCURRENT_REQUESTS 最大并发（即同时）连接数。默认16
> 3. CONCURRENT_REQUESTS_PER_DOMAIN 将对任何单个域执行的最大并发（即同时）请求数
> 4. CONCURRENT_REQUESTS_PER_IP 对任何单个IP执行的最大并发（即同时）请求数。如果设置这个会忽略CONCURRENT_REQUESTS_PER_DOMAIN设置

**Scrapy 底层是基于twisted的异步IO框架**
> 1. Twisted是一个基于Reactor模式的异步IO网络框架, 它基于Reactor模式帮我们抽象出了异步编程模型以及各种非阻塞的io模块（tcp、http、ftp等），使我们很方便地进行异步编程。
> 2. Reactor模式就是利用循环体来等待事件发生，然后处理发生的事件的模式

## 3.2 / 3.3 多进程: 进程的创建以及调试
### Python Process创建进程
> 第一种方法:通过Process类创建进程
```
from multiprocessing import Process
import os

# 定义一个函数，准备作为新进程的 target 参数
def action(name, *add):
    print( name )
    for arc in add:
        print( "%s --当前进程%d" % (arc, os.getpid()) )

if __name__ == '__main__':
    # 定义为进程方法传入的参数
    my_tuple = ("http://c.biancheng.net/python/", \
                "http://c.biancheng.net/shell/", \
                "http://c.biancheng.net/java/")
    # 创建子进程，执行 action() 函数
    my_process = Process( target=action, args=("my_process进程", *my_tuple) )
    my_process.start()
    my_process.join()
    action( "主进程", *my_tuple )
```
> 第二种方法: 通过Process继承类创建进程
```
from multiprocessing import Process
import os

# 定义一个函数，供主进程调用
def action(name, *add):
    print( name )
    for arc in add:
        print( "%s --当前进程%d" % (arc, os.getpid()) )


# 自定义一个进程类
class My_Process( Process ):
    def __init__(self, name, *add):
        super().__init__()
        self.name = name
        self.add = add

    def run(self):
        print( self.name )
        for arc in self.add:
            print( "%s --当前进程%d" % (arc, os.getpid()) )


if __name__ == '__main__':
    my_tuple = ("http://c.biancheng.net/python/", \
                "http://c.biancheng.net/shell/", \
                "http://c.biancheng.net/java/")
    my_process = My_Process( "my_process进程", *my_tuple )
    my_process.start()
    action( "主进程", *my_tuple )
```

### 多进程如何对代码进行优化
todo

## 3.4 多进程: 使用队列实现进程间通信

### Multiprocessing中的队列
**multiprcessing.Queue.put() 为 入队操作**
> q.put(item,block,timeout):将item放入队列，如果此时队列已满：
> 1. 如果block=True，timeout没有设置，就会阻塞，直到有可用空间为止。
> 2. 如果block=True，timeout也设置，就会阻塞到timeout，超过这个时间会报Queue.Full异常。
> 3. 如果block=False，timeout设置无效，直接报Queue.Full异常。

**multiprcessing.Queue.get() 为 出队操作**
> q.get([block,timeout])：返回q中的一个项
>1. block如果设置为True,如果q队列为空，该方法会阻塞（就是不往下运行了，处于等待状态），
直到队列中有项可用为止，
>2. 如果同时页设置了timeout，那么在改时间间隔内，都没有等到有用的项，就会引发Queue.Empty异常。
如果block设置为false，timeout没有意义，如果队列为空，将引发Queue.Empt异常。

### 例子：
下面是一个队列通信的例子，但会发生阻塞。
TODO：思考如何避免阻塞进而实现无限元素的读写的非阻塞任务。
```
import random
import time
from multiprocessing import Process, Queue


# 写数据进程执行的代码:
def write(q):
    for value in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']:
        print( 'Put %s to queue...' % value )
        q.put( value )
        time.sleep( random.random() )


# 读数据进程执行的代码:
def read(q):
    while True:
        if not q.empty():
            value = q.get( True )
            print( 'Get %s from queue.' % value )
            time.sleep( random.random() )
        else:
            break


if __name__ == '__main__':
    q = Queue(4)
    pw = Process( target=write, args=(q,) )
    pr = Process( target=read, args=(q,) )
    pw.start()
    pr.start()
    pw.join()
    pr.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止
```

## 3.5 多进程：管道通信、共享内存通信
### 管道通信
多进程通过管道通信的原理：在内存中开辟管道空间，生成管道操作对象，多个进程使用"同一个"管道对象进行操作即可实现通信

管道就是一个数据流，所有的unix都提供管道，由pipe函数创建，单个管道提供一个单向的数据流。
管道在单个进程中，内核控制数据管道，用户通过一个写fd和读fd来进行数据传递。
管道虽然是由单个进程创建的，但是通常在有亲缘关系的进程之间进行通信。

> 1. fd1,fd2 = Pipe(duplex = True) 参数duplex默认表示双向管道，如果设置为False则为单向管道
> 2. fd.recv() 从管道读取信息, *如果管道为空则阻塞
> 3. fd.send(data), 向管道写入内容
### 共享内存通信
在内存空开辟一块空间，对多个进程可见，进程可以写入输入，但是每次写入的内容会覆盖之前的内容。
> 1. obj = Value(ctype,obj), 开辟共享内存空间, ctype 要存储的数据类型, obj 共享内存的初始化数据
> 2. obj.value 即为共享内存值，对其修改即修改共享内存
> 3. obj = Array(ctype,obj) 也是开辟共享内存空间, obj  初始化存入的内容 比如列表，字符串. 可以通过遍历过户每个元素的值

## 3.6 多进程: 锁机制解决资源抢占
上面介绍的三种通信机制中队列通信是进程安全的,因为Queue中引入了锁机制.
加入锁机制强迫不同进程间对同一份资源进行单一操作.

例子:
```
import multiprocessing as mp
import time
import os

def job(v, num, l):
    l.acquire()
    for _ in range(5):
        time.sleep(0.1)
        v.value += num
        print(v.value, end='|')
    print('/n')
    l.release()

def multi_job():
    l = mp.Lock()
    v = mp.Value('i', 0)
    p1 = mp.Process(target=job, args=(v, 1, l))
    p2 = mp.Process(target=job, args=(v, 2, l))
    p3 = mp.Process( target=job, args=(v, 3, l) )
    p4 = mp.Process( target=job, args=(v, 4, l) )
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()

if __name__ == '__main__':
    for _ in range(100):
        multi_job()
```

## 3.7 多进程: 进程池
如果要启动大量的子进程，可以用进程池的方式批量创建子进程. 可以用Multiprocessing.Pool.
1. 当有新的请求提交到pool中时，如果池还没有满，那么就会创建一个新的进程用来执行该请求；
2. 但如果池中的进程数已经达到规定最大值，那么该请求就会等待，直到池中有进程结束，才会创建新的进程来执行它。
3. **对于线程池,调用join之前，先调用close或者terminate方法，否则会出错。**

**异步进程执行**
apply_async函数是异步进程池（非阻塞）
Pool.apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None).
```
from multiprocessing import Pool
import os,time,random

def worker(msg):
    t_start = time.time()
    print("%s start, pid: %d"%(msg,os.getpid()))
    time.sleep(random.random()*2) 
    t_stop = time.time()
    print(msg," end, time: %0.2f"%(t_stop-t_start))


if __name__ == '__main__':
    po=Pool(3) #定义一个进程池，最大进程数3
    for i in range(0, 10):
        #Pool.apply_async(要调用的目标,(传递给目标的参数元祖,))
        #每次循环将会用空闲出来的子进程去调用目标
        po.apply_async(worker,(i,))  #如果不用async 直接使用apply, 那么会使用堵塞式,任务一个一个执行

    print("----start----")
    po.close() #关闭进程池，关闭后po不再接收新的请求
    po.join() #等待po中所有子进程执行完成，必须放在close语句之后
    print("-----end-----")

```

## 38 多线程: 创建线程
多任务可以由多进程完成，也可以由一个进程内的多线程完成。
线程是操作系统直接支持的执行单元, Python的线程是真正的Posix Thread，而不是模拟出来的线程。

### 线程 VS 进程
| index  | 线程   |进程   |
|---|---|---|
| 1 | Process is heavy weight or resource intensive.  |  Thread is light weight, taking lesser resources than a process. |
| 2 | Process switching needs interaction with operating system.  |  Thread switching does not need to interact with operating system. |
| 3 | In multiple processing environments, each process executes the same code but has its own memory and file resources.  | All threads can share same set of open files, child processes.  |
| 4|If one process is blocked, then no other process can execute until the first process is unblocked. |While one thread is blocked and waiting, a second thread in the same task can run. |

### 多进程 VS 多线程
Program 应用程序
> A program is an executable file which consists of a set of instructions to perform some task and 
> is usually stored on the disk of your computer.

Process 进程
> A process is what we call a program that has been loaded into memory along with all the resources 
>it needs to operate. It has its own memory space.

进程
> A thread is the unit of execution within a process. A process can have multiple threads running as 
>a part of it, where each thread uses the process’s memory space and shares it with other threads.

多线程
> Multithreading is a technique where multiple threads are spawned by a process to do different tasks,
> at about the same time, just one after the other. 
>This gives you the illusion that the threads are running in parallel, 
>but they are actually run in a concurrent manner. 
>In Python, the Global Interpreter Lock (GIL) prevents the threads from running simultaneously.

多进程
> Multiprocessing is a technique where parallelism in its truest form is achieved. 
>Multiple processes are run across multiple CPU cores, which do not share the resources among them. 
>Each process can have many threads running in its own memory space. 
>In Python, each process has its own instance of Python interpreter doing the job of executing 
>the instructions.

**线程切换的代价**
>操作系统切换线程，它需要先保存当前执行的现场环境（CPU寄存器状态、寄存页等），
然后把新任务执行环境准备好，才能开始执行。
如果要有几千个任务同时执行，操作系统可能就只忙着切换任务，根本没多少时间切换任务。
所以，多任务一旦到一个限度，就会消耗掉系统的所有资源，结果效率急剧下降，所有任务都做不好

**计算密集型 vs IO密集型**
1. 计算密集型  / CPU bound
> 1. 计算密集型主要进行计算，如计算圆周率、对视频进行高清解码等。为了达到CPU高效利用率，计算密集型任务同时进行的数量应等于CPU的核心数。
> 2. 计算密集型任务主要消耗CPU资源，因此，代码运行效率至关重要。Python这样的语言运行效率很低，完全不合适计算密集型任务，这种任务最好用C语言编写。

2. IO密集型  / IO bound
>1. 主要涉及到网络硬盘、磁盘IO读取的任务都是IO密集型。这种任务表现为CPU消耗的少，主要等待IO操作完成（IO的速度远远低于CPU和内存的速度）。对于IO任务，任务越多，CPU利用率越高，但也有一个限度。常见的大部分任务都是IO密集型任务，比如Web应用。
>2. IO密集型任务运行期间，99%的时间都花费在IO上，花在CPU上的时间很少，因此用速度极快的C语言替换运行速度极低的Python完全起不到提升运行效率。最合适的语言就是开发效率最高（代码量最少）的语言，脚本语言是首选。C语言最差。

## 3.9/3.10/3.11 多线程: 线程锁 & 线程池
多线程如果操作同一份数据，必须加锁，因为多线程共享进程资源。
多线程的一大问题就是通过加锁来”抢夺“共享资源的时候有可能造成死锁
为了避免死锁，需要所有的线程按照指定的算法（或优先级）来进行加锁操作。

### 线程锁
1. 线程锁使用
>1. acquire():上锁，这个时候只能运行上锁后的代码
> 2. release():解锁，解锁后把资源让出来，给其他线程使用
2. 使用Python的with语句实现对锁的获取和释放会更简捷
3. 创建多线程或多进程，都必须要先经过主模块判断，即必须在if __name__=='__main__':语句之后才行，这是为了保护资源的一种强制性机制

**例子：注意两种锁的区别：Lock普通锁不可嵌套，RLock普通锁可嵌套**
```
import threading
import time
# Lock普通锁不可嵌套，RLock普通锁可嵌套
mutex = threading.Lock()

class MyThread(threading.Thread):
    def run(self):
        if mutex.acquire(1):
            print("thread " + self.name + " get mutex")
            time.sleep(1)
            mutex.acquire()
            mutex.release()
        mutex.release()

if __name__ == '__main__':
    for i in range(5):
        t = MyThread()
        t.start()
```
## 3.10 队列

### Python中队列是线程安全的
**队列Queue**
>Python的Queue模块提供一种适用于多线程编程的FIFO实现。
它可用于在生产者(producer)和消费者(consumer)之间线程安全(thread-safe)地传递消息或其它数据，
因此多个线程可以共用同一个Queue实例。Queue的大小（元素的个数）可用来限制内存的使用。

>Queue类实现了一个基本的先进先出(FIFO)容器，使用put()将元素添加到序列尾端，get()从队列尾部移除元素。
同时，python中也支持LifoQueue使用后进先出序（它会关联一个栈数据结构）

**Priority Queue（优先队列）**
PriorityQueue依据队列中内容的排序顺序(sort order)来决定那个元素将被检索。

### 队列的使用方法
1. 创建队列
    q=Queue.Queue(maxsize=10)
2. 读取/存放数据
```
q.put(x,block=True,timeout=None)
# 这里放入一个数据x，q.put(x)。
# block=True表示队列堵塞，直到队列有空的地方出来再把元素传进去，
# timeout=10表示10秒后如果没有新的元素传进去就报错。
q.get(x,block=True,timeout=None)
# 这里是把数据x取出来，q.get(x)。
# 如果设置block=True,timeout=10，就是说如果10秒没有接收到数据就直接报错，
# 如果设置block=False的话，timeout参数会被忽略，此时就是只要队列有元素就直接弹出这个元素，
# 没有元素就直接报错。
```
3. 队列是否满：q.full()，如果满会返回True
4. 队列是否空：q.Empty()
4. 队列个数：q.qsize()

**例子**
通过队列实现多线程之间的通信，这里模拟的是Produce-Consumer模式
```
import threading
import time
import queue

'''
模拟包子店卖包子
厨房每一秒钟制造一个包子
顾客每三秒吃掉一个包子
厨房一次性最多存放100个包子
'''
q = queue.Queue( maxsize=100 )


# 厨房一次性最多存放100个包子

def produce(q):
    # 这个函数专门产生包子
    for i in range( 10000 ):
        q.put( '第{}个包子'.format( str( i ) ) )
        # 生产出包子，表明包子的id号
        time.sleep( 1 )
        # 要一秒才能造出一个包子


def consume(q):
    while not q.empty():
        # 只要包子店里有包子
        print( '包子店的包子剩余量：' + str( q.qsize() ) )
        # q.qsize()是获取队列中剩余的数量
        print( '小桃红吃了:' + str( q.get() ) )
        # q.get()是一个堵塞的，会等待直到获取到数据
        print( '------------' )
        time.sleep( 3 )


t1 = threading.Thread( target=produce, args=(q,) )
t2 = threading.Thread( target=consume, args=(q,) )
t1.start()
t2.start()
```
### 队列和多线程结合实现requests多线程并行下载

这里需要注意：
1. Queue.task_done()用来标识task完成，但只用在consumer线程中, 所以put()操作后不能带task_done()
2. 如果consumer线程从队列中取走任务，但没有执行task_done(),则队列的join无法判断队列中所有任务是否结束
3. Queue.join() 实际上意味着等到队列为空，再执行别的操作

```
import os
import queue
import threading
import requests
from fake_useragent import UserAgent


class DownloadThread( threading.Thread ):
    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            url = self.q.get()  # 从队列取出一个元素

            print( f'{self.name} begin download {url}' )
            self.download_file( url )  # 下载文件
            self.q.task_done()  # 下载完成发送信号
            print( f'{self.name} download completed' )

    def download_file(self, url):
        ua = UserAgent()
        headers = {"User-Agent": ua.random}
        r = requests.get( url, stream=True, headers=headers )
        fname = os.path.basename( url ) + '.html'
        with open( fname, 'wb' ) as f:
            for chunk in r.iter_content( chunk_size=1024 ):
                if not chunk: break
                f.write( chunk )


if __name__ == '__main__':
    urls = ['http://www.baidu.com',
            'http://www.python.org',
            'http://www.douban.com',
            'https://maoyan.com/',
            'https://movie.douban.com/']

    q = queue.Queue()

    for i in range( 15 ):
        t = DownloadThread( q )  # 启动5个线程
        t.setDaemon( True )
        t.start()

    for url in urls:
        q.put( url )

    q.join()
```
## 3.12 GIL锁与多线程的性能瓶颈
GIL(全局解释器锁，GIL 只有cpython有)：在同一个时刻，只能有一个线程在一个cpu上执行字节码，
没法像c和Java一样将多个线程映射到多个CPU上执行，但是GIL会根据执行的字节码行数(为了让各个线程能够平均
利用CPU时间，python会计算当前已执行的微代码数量，达到一定阈值后就强制释放GIL)和时间片以及遇到IO操作
的时候主动释放锁，让其他字节码执行。

基于GIL的存在，在遇到大量的IO操作(文件读写，网络等待)代码时，使用多线程效率更高。

## 3.xx 作用：哲学家就餐问题
哲学家就餐问题（英语：Dining philosophers problem）是在计算机科学中的一个经典问题，
用来演示在并发计算中多线程同步（Synchronization）时产生的问题。

### 背后的概念：死锁与资源竞争
### 死锁为什么发生
死锁的发生必须满足四个条件：
1. 资源有限。
2. 持有等待。 即一个线程在请求新资源时，不会释放已获得的资源。
3. 不能抢占
4. 循环等待。 你等我我等你，大家的等待和持有关系形成了一个闭环。
以上四个条件对死锁的形成来说缺一不可，我们只要打破其中一个条件，死锁便不会发生。
### 死锁解决方案
避免死锁有两种方式：动态避免与静态避免。

**动态避免，银行家算法，在资源分配上下文章**
>动态避免算法便是在每次进行资源分配时，都需要仔细计算，确保该资源的申请不会使系统进入一个不安全状态。
>安全状态是指我们能够找到一种资源分配的方法和顺序，使每个在运行的线程都可以得到其需要的资源。
>如果资源的分配将使系统进入不安全状态，则拒绝。动态避免是一种在资源分配上下功夫的防止死锁的手段。

**静态避免，从任务代码上避免死锁**
1. 加锁顺序（线程按照一定的顺序加锁）
2. 加锁时限（线程尝试获取锁的时候加上一定的时限，超过时限则放弃对该锁的请求，并释放自己占有的锁）
2. 死锁检测, 主要是针对那些不可能实现按序加锁并且锁超时也不可行的场景。具体做法是：
>每当一个线程获得了锁，会在线程和锁相关的数据结构中（map、graph等等）将其记下。
>除此之外，每当有线程请求锁，也需要记录在这个数据结构中。
> 当一个线程请求锁失败时，这个线程可以遍历锁的关系图看看是否有死锁发生。
>例如，线程A请求锁7，但是锁7这个时候被线程B持有，这时线程A就可以检查一下线程B是否已经请求了线程A
>当前所持有的锁。如果线程B确实有这样的请求，那么就是发生了死锁（线程A拥有锁1，请求锁7；线程B拥有锁7，
>请求锁1）。
