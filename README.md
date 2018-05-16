# zhilianPosition
智联招聘爬虫玩具

### 1.获取数据

智联招聘的url:

```http://sou.zhaopin.com/jobs/searchresult.ashx?jl= 地点(需url转码) &kw=关键字(需url转码)&sm=0&p=1(页面)```

抓取该页面的职位链接://a[@style='font-weight: bold']/@href

对提取到的每个职位链接发送请求,并做处理,提取以下数据

```职位月薪  //ul[@class='terminal-ul clearfix']//li[1]/span/text()

招聘人数	//ul[@class='terminal-ul clearfix']//li[7]/span/text()

职位名称	//ul[@class='terminal-ul clearfix']//li[8]//a/text()

工作地点	//ul[@class='terminal-ul clearfix']//li[2]//a/text()

工作要求	//div[@class='terminalpage-main clearfix']//div[@class='tab-inner-cont'][1]
```

我在采集过程中对这些提取到的数据进行了处理,整理成了json格式,方便后续的数据处理

### 2.GUI界面
简单一个小界面,有三个按钮 
#### 搜索 上一页 下一页







