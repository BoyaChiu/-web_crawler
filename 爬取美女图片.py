import urllib.request
import re,os
def url_open(url):
    web_data = urllib.request.Request(url)
    web_data.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
    response = urllib.request.urlopen(web_data)
    html = response.read()
    return html

def get_total_num(url):
    html =url_open(url).decode('gbk')
    reg  = re.compile(r'共 <strong>(.*?)</strong>页')
    total_num = re.findall(reg,html)[0]
    return int(total_num)
def get_cover_list(url):#获得一页的50个url
    html = url_open(url).decode('gbk')
    reg = re.compile(r'<p><a href="(.*?)"')
    cover_url_list = re.findall(reg,html)
    return cover_url_list

def get_img_list(cover_url):#获得每张图片的url
    html = url_open(cover_url).decode('gbk')
    reg1 = re.compile(r'<li><a>共(.*?)页')
    img_num = int(re.findall(reg1,html)[0])#取出每一个cover的图片数量
    img_url_list = [] #一个cover的第一个url，
    img_url_list.append(cover_url)
    for num in range(2,img_num+1):#http://www.youmzi.com/14298_2.html
        url = cover_url[:-5] +'_' + str(num) + cover_url[-5:]
        img_url_list.append(url)
    return img_url_list

def get_img(img_url):
    html = url_open(img_url).decode('gbk')
    req2 = r"<img src='(.*?)'"
    img = re.findall(req2,html)[0]
    return img

def download(folder='成功的爬虫'):
    try:
        os.mkdir(folder)
        os.chdir(folder)
    except:
        os.chdir(folder)
    url = 'http://www.youmzi.com/meinv.html'#初始url
    total_num = get_total_num(url)
    print(total_num)
    for tatol in range(1,total_num+1):
        page_url = url[:-5] + '_' + str(tatol) + url[-5:]
        cover_url_list = get_cover_list(page_url)
        for cover_url in cover_url_list:
            img_url_list = get_img_list(cover_url)
            for img_url in img_url_list:
                img = get_img(img_url)
                print(img)
                filename = img.split('/')[-1]
                urllib.request.urlretrieve(img,filename)

if __name__ =='__main__':
    download()
