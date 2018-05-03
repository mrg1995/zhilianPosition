import requests
import tkinter
import urllib
from lxml import etree
import json
import jsonpath

def pageadd():
    global page
    page += 1
    search(page)

def pageless():
    global page
    page -= 1
    if page == 0:
        return
    search(page)

def search(page):
    global lb
    global entry1
    global entry2
    global text1
    lb.delete(0, tkinter.END)
    address = entry1.get()
    workName = entry2.get()
    if len(address) != 0 and len(workName) != 0:
        address = urllib.parse.quote(address)
        workName = urllib.parse.quote(workName)
        url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl={}&kw={}&p='.format(address, workName)
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        # 此次打开文件是为了擦除之前的数据
        url_start = url + str(page)
        respone = requests.get(url_start, headers=header)
        content = etree.HTML(respone.text)
        linkList = content.xpath('//a[@style="font-weight: bold"]/@href')
        str1 = pipeline(linkList)
        insert(str1)
    else:
        text1.delete(0.0, tkinter.END)
        text1.insert(tkinter.INSERT, '请将查询信息输入完整')
        return

def realSearch():
    global page
    page = 1
    search(page)

def insert(str):
    global lb
    global list_all
    list_all = []
    try:
        data = '{"data":[' + str[:(len(str) - 1)] + ']}'
        jsonobj = json.loads(data)
        for i in range(20):
            money = jsonpath.jsonpath(jsonobj, '$.data[{}].money'.format(i))[0]
            peopleNumber = jsonpath.jsonpath(jsonobj, '$.data[{}].peopleNumber'.format(i))[0]
            workName = jsonpath.jsonpath(jsonobj, '$.data[{}].workName'.format(i))[0]
            workAddress = jsonpath.jsonpath(jsonobj, '$.data[{}].workAddress'.format(i))[0]
            workSkill = jsonpath.jsonpath(jsonobj, '$.data[{}].workSkill'.format(i))[0]
            workUrl = jsonpath.jsonpath(jsonobj, '$.data[{}].workUrl'.format(i))[0]
            list = [workName, money, workAddress, peopleNumber, workSkill, workUrl]
            list_all.append(list)
    except:
        pass
    count = 0
    for company in list_all:
        count += 1
        lb.insert(tkinter.END, '{} {} 薪资:{}'.format(count, company[0], company[1]))

def pipeline(linkList):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    str = ''
    count = 0
    for link in linkList:
        count += 1
        item = {}
        respone = requests.get(link, headers=header)
        if len(respone.text) != 0:
            content = etree.HTML(respone.text)
            # 薪资
            print(link)
            if content.xpath("//ul[@class='terminal-ul clearfix']//li[1]/strong/text()") == []:
                continue
            # 薪资
            item['money'] = content.xpath("//ul[@class='terminal-ul clearfix']//li[1]/strong/text()")[0]
            # 招聘人数
            item['peopleNumber'] = content.xpath("//ul[@class='terminal-ul clearfix']//li[7]/strong/text()")[0]
            # 职位名称
            item['workName'] = content.xpath("//ul[@class='terminal-ul clearfix']//li[8]//a/text()")[0]
            # 工作地点
            item['workAddress'] = content.xpath("//ul[@class='terminal-ul clearfix']//li[2]//a/text()")[0]
            # 工作要求
            data = content.xpath("//div[@class='terminalpage-main clearfix']//div[@class='tab-inner-cont'][1]")
            item['workSkill'] = data[0].xpath('string(.)')
            # 网页链接
            item['workUrl'] = link
            text = json.dumps(dict(item), ensure_ascii=False)
            str += text + ','
        if count == 20:
            return str

def realmyPrint(event):
    global lb
    global text1
    global text2
    index = lb.curselection()
    text1.delete(0.0, tkinter.END)
    text1.insert(tkinter.INSERT,
                 '工作地点:{}\n招聘人数:{}\n{}'.format(list_all[index[0]][2], list_all[index[0]][3], list_all[index[0]][4]))
    text2.delete(0.0, tkinter.END)
    text2.insert(tkinter.INSERT, list_all[index[0]][5])

def main():
    global lb
    global entry2
    global entry1
    global text2
    global text1

    win = tkinter.Tk()
    win.title('招聘小脚本')
    win.geometry('900x500+200+0')
    frm1 = tkinter.Frame(win,width=900,height=500)
    frm1.place(x=0,y=0)
    tkinter.Label(frm1,font=('黑体',20),width = 12,text='工作地点').place(x=20,y=20)
    tkinter.Label(frm1,font=('黑体',20),width = 12,text='具体职位').place(x=20,y=70)
    entry1 = tkinter.Entry(frm1,font=('黑体',20),width = 12)
    entry1.place(x=200,y=20)
    entry2 = tkinter.Entry(frm1,font=('黑体',20),width = 12)
    entry2.place(x=200,y=70)

    tkinter.Label(frm1,font=('黑体',20),width = 12,text='具体要求').place(x=430,y=120)
    text1 = tkinter.Text(frm1, width=50, height=20,font=('黑体',12))
    text1.place(x=430,y=150)
    tkinter.Label(frm1,font=('黑体',20),width = 12,text='页面链接').place(x=500,y=20)
    text2 = tkinter.Text(frm1, width=30, height=2,font=('黑体',12))
    text2.place(x=480,y=70)
    tkinter.Button(frm1, text='下一页', font=('黑体', 20),command=pageadd).place(x=325,y=200)
    tkinter.Button(frm1, text='上一页', font=('黑体', 20),command=pageless).place(x=325,y=300)
    lb = tkinter.Listbox(frm1, selectmode=tkinter.BROWSE,width=40,height=20)
    lb.place(x=40,y=120)
    button1 = tkinter.Button(frm1, text='搜索', font=('黑体', 20),command=realSearch)
    button1.place(x=400, y=50)
    lb.bind('<Double-Button-1>',realmyPrint)

    win.mainloop()

if __name__ == '__main__':
    main()












































