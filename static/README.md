### Fish Demo

这是我自己写的wsgi框架的Demo 

类似flask和Faskapi的用法

下面是第一次性能测试 目前版本: fish demo v0.2


### 2021 2月5日 各Demo 用http_load 压测情况汇总
cpu 2c4t 7200u 内存16g ddr4 2400 硬盘 ssd 860evo
**模拟并发50 持续10s**
返回数据统一:

```
# 以Flask为例
@app.route("/index")
def req():
    return {"code": 0, "msg": "Hello Word"}
```

压测语句 

http_load 版本为2016

```http_load -p 50 -s 10 url```

#### 各个框架情况:
```
My Fish
单线程
691 fetches, 50 max parallel, 22112 bytes, in 10.0006 seconds
32 mean bytes/connection
69.096 fetches/sec, 2211.07 bytes/sec
msecs/connect: 393.198 mean, 7511.56 max, 0.784 min
msecs/first-response: 4.69625 mean, 23.711 max, 0.81 min
HTTP response codes:
  code 200 -- 691

多线程方式
3932 fetches, 50 max parallel, 124768 bytes, in 10.0047 seconds
31.7314 mean bytes/connection
393.016 fetches/sec, 12471 bytes/sec
msecs/connect: 61.7558 mean, 2112.34 max, 0.722 min
msecs/first-response: 7.00383 mean, 63.479 max, 0.909 min
33 bad byte counts
HTTP response codes:
  code 200 -- 3899

==================================================================

Flask
单线程
462 fetches, 50 max parallel, 13860 bytes, in 10.0066 seconds
30 mean bytes/connection
46.1696 fetches/sec, 1385.09 bytes/sec
msecs/connect: 41.7393 mean, 3007.58 max, 0.759 min
msecs/first-response: 160.247 mean, 288.83 max, 1.656 min
HTTP response codes:
  code 200 -- 462
  
多线程
2670 fetches, 50 max parallel, 80100 bytes, in 10.0003 seconds
30 mean bytes/connection
266.993 fetches/sec, 8009.78 bytes/sec
msecs/connect: 8.16934 mean, 1013.81 max, 0.782 min
msecs/first-response: 149.9 mean, 333.652 max, 1.471 min
HTTP response codes:
  code 200 -- 2670

==================================================================

FastApi 

4560 fetches, 50 max parallel, 132240 bytes, in 10.0009 seconds
29 mean bytes/connection
455.959 fetches/sec, 13222.8 bytes/sec
msecs/connect: 1.42552 mean, 11.186 max, 0.696 min
msecs/first-response: 107.356 mean, 218.665 max, 28.871 min
HTTP response codes:
  code 200 -- 4560

fastapi 开启异步

5565 fetches, 50 max parallel, 161385 bytes, in 10 seconds
29 mean bytes/connection
556.499 fetches/sec, 16138.5 bytes/sec
msecs/connect: 1.422 mean, 19.825 max, 0.652 min
msecs/first-response: 87.2547 mean, 207.493 max, 10.2 min
HTTP response codes:
  code 200 -- 5565

==================================================================

Sanic 
6477 fetches, 50 max parallel, 194310 bytes, in 10 seconds
30 mean bytes/connection
647.699 fetches/sec, 19431 bytes/sec
msecs/connect: 1.62763 mean, 36.335 max, 0.678 min
msecs/first-response: 75.0222 mean, 191.586 max, 7.045 min
HTTP response codes:
  code 200 -- 6477

添加 async
6585 fetches, 50 max parallel, 197550 bytes, in 10 seconds
30 mean bytes/connection
658.5 fetches/sec, 19755 bytes/sec
msecs/connect: 1.5476 mean, 37.537 max, 0.617 min
msecs/first-response: 73.8971 mean, 183.193 max, 5.531 min
HTTP response codes:
  code 200 -- 6585

==================================================================
django 单文件运行

1012 fetches, 50 max parallel, 28739 bytes, in 10.0013 seconds
28.3982 mean bytes/connection
101.187 fetches/sec, 2873.53 bytes/sec
msecs/connect: 172.27 mean, 3010.35 max, 0.864 min
msecs/first-response: 42.0469 mean, 152.795 max, 1.977 min
21 bad byte counts
HTTP response codes:
  code 200 -- 991

```