import requests
import os
import re
import json
import jsonpath
import time
from enum import Enum
import tkinter # 窗口界面 后续开发

def title_process(title):
    '''
    负责处理标题信息中的符号
    文件名不包含以下任何字符：“（双引号）、*（星号）、<（小于）、>（大于）、？（问号）、\（反斜杠）、/（正斜杠）、|（竖线）、：（冒号）。
    考虑 中文字符 和 英文字符

    将 这些字符 统一处理为 ''
    '''
    appeared_forbidden_str = ['|', '/', '*', '<', '>', '?', ':', '\\', '：', '？']
    for str in appeared_forbidden_str:
        if (str in title):
            title_last = title.replace(str,"")
            title = title_process(title_last)
        if(str_checking(title) == True):
            return title

def str_checking(str):
    appeared_forbidden_str = ['|', '/', '*', '<', '>', '?', ':', '\\', '：', '？']
    counter = 0
    for i in appeared_forbidden_str:
        counter += 1
        if(i in str):
            return False
        elif(counter == len(appeared_forbidden_str)):
            return True


class STATE(Enum):
    '''
        检查data_integrated.txt列表是否完全被使用
        检查日志中的错误信息
            错误日志001:在登录id时出错    
            错误日志002:在抓去所有id时出错
            错误日志003:在访问各个id作品页时出错
            错误日志004:在下载图片时出错
        :return 响应信息
        '''
    ERROR_1 = '错误日志001'
    ERROR_2 = '错误日志002'
    ERROR_3 = '错误日志003'
    ERROR_4 = '错误日志004'
    ERROR_DTATGET_INTERRUPTED = '数据抓取发生错误' # 数据采集被打断
    
    FINISH = '程序结束'            # 程序完全运行并结束
    UNINITIALIZED = '数据未初始化完成'
    INITIALIZED = '数据初始化完成' # 程序已完成初始化
    NORMAL = 0                     #程序一切正常
    PRIMARY = '程序启动'


def log_check(path):
        '''
        检查 日志
        :return 响应信息
        '''
        with open(path, 'r', encoding='utf-8')as f:
            line = f.readlines()
            log = line[-1]
         
        # 需要重新拉去数据的情况
        # 1.存在有 错误信息1/2 的日志   2.日志刚初始化
        if STATE.ERROR_1.value in log or STATE.ERROR_2.value in log or STATE.PRIMARY.value in log:
            return STATE.UNINITIALIZED.name
        elif STATE.ERROR_3.value in log or STATE.ERROR_4.value in log or STATE.INITIALIZED.value in log:
            return STATE.INITIALIZED.name
        
        # 需要 初始化 日志的情况
        elif STATE.FINISH.value in log:
            with open(path, 'w', encoding='utf-8')as f:
                f.write(STATE.PRIMARY.value)
            return STATE.PRIMARY.name
        
        else:
            return STATE.NORMAL.name



class Pixiv_bugger():
    def __init__(self, tags, login_id, password):
        # 初始化参数
        self.tags = tags
        self.login_id = login_id
        self.password = password
        
        # 日志路径初始化
        self.data_path = './data_integrated.json'
        self.log_path = './log.txt'

        # 写入请求标头,谷歌浏览器
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }

        # 配置代理,暂时不用
        self.proxies = {
            'http':"http//156.236.118.75:58192",
            'https':"https//156.236.118.75:58192"
        }
        

    def log_creat(self):
        # 创建用于数据文件
        if not os.path.exists(self.data_path):   
            with open(self.data_path, 'w'):
                pass
            
        # 创建日志,用于程序断连等突发情况
        if not os.path.exists(self.log_path):   
            with open(self.log_path, 'w', encoding='utf-8')as f:
                f.write(STATE.PRIMARY.value)
    
    def data_load(self):
        '''
        将得到的 data.json进行解析
        :return 返回的是 字典类型 数据
        '''
        with open(self.data_path, 'r')as f:
            data = json.load(f)
        return data
    
    def data_integrated(self, data):
        '''
        将数据更新到 本地文件中
        '''
        with open(self.data_path, 'w')as f:
            json.dump(data, f, indent=4)
        

    
    def login(self):
        # 模拟登录
        # 获取pixiv登录界面
        home_url = 'https://accounts.pixiv.net/login'
        params_home = {
            'return_to': 'https://www.pixiv.net/',
            'lang': 'zh',
            'source': 'pc',
            'view_type': 'page',
        }

        # 获取模拟登录所需的tt
        # requests.adapters.DEFAULT_RETRIES = 5 # 如果失败重复5次request请求
        try:
            search_login = requests.get(home_url, headers=self.headers, params=params_home)
            pixivAccount_tt = re.findall('"pixivAccount.tt":"(?P<tt>.*?)"', search_login.text)
        except BaseException as error:
            print("登录发生错误(；д；)")
            with open('./log.txt','a',encoding='utf-8')as f:
                f.write(str(error) + f'\n{STATE.ERROR_1.value}\n')
        
        # 及时关闭请求以免服务器检测
        search_login.close()
        # print(pixivAccount_tt)

        # 获取登录信息的url
        login_url = "https://accounts.pixiv.net/ajax/login?lang=zh"

        # 配置登录参数
        params_login = {
            'login_id': self.login_id,
            'password': self.password,
            'source': 'pc',
            'app_ios': 0,
            'ref':'' ,
            'return_to': 'https://www.pixiv.net/',
            'g_recaptcha_response':'', 
            'tt': pixivAccount_tt[0],
        }

        try:
            search_home = requests.post(login_url, headers=self.headers, data=params_login)
            print('登陆成功(￣▽￣)')
        except BaseException as error:
            print("登录发生错误(；д；)")
            with open('./log.txt','a',encoding='utf-8')as f:
                f.write(str(error) + f'\n{STATE.ERROR_1.value}')

        # 服务器已登录,备份cookie
        self.Cookie = search_home.cookies

        # 防盗链添加
        self.headers.update({'Referer':'https://www.pixiv.net/'})


    def data_get(self):
        '''
        从网页中抓取信息并储存在data_integrated.json文件中
        '''
        # 如果 确定当前 数据文件 未被完全使用,不改变该文件内容
        
        print('\n开始抓取网页数据')

        # 获取pixiv有相关tag的作品页面
        tag = self.tags
        url_page = f"https://www.pixiv.net/ajax/search/artworks/{tag}"

        # 网址对应参数
        params = {
            'word': tag,
            'order': 'date_d',
            'mode': 'all',
            'p': 1,
            's_mode': 's_tag',
            'type': 'all',
            'lang': 'zh',
            'version': '82d3db204a8e8b7e2f627b893751c3cc6ef300fb'
        }

        try:
            search_page = requests.get(url_page, headers=self.headers, params=params)
            page_data = search_page.json() # 已经转化为了json格式  
            # json_page_data = json.loads(search_page.text) 
        except BaseException as error:
            print("数据抓取发生错误(；д；)")
            with open('./log.txt','a', encoding='utf-8')as f:
                f.write(str(error) + f'\n{STATE.ERROR_2.value}')

        # with open('D://Users//10548//Desktop//data.txt','w')as f:
        #     f.write(search_page.text)

        # 解析json文件取得作品的信息
        data_compile_id = '$.body.illustManga.data..id'         # 此为所有作品id
        data_compile_title = '$.body.illustManga.data..title'   # 此为所有作品 title
        data_compile_total = '$.body.illustManga.total'         # 页面显示的作品总数
        data_compile_pageCount = '$.body.illustManga..pageCount'# 作品中的图片数量
        
        artwork_id = jsonpath.jsonpath(page_data, data_compile_id)
        artwork_title = jsonpath.jsonpath(page_data, data_compile_title)
        artwork_total = jsonpath.jsonpath(page_data, data_compile_total)
        artwork_pageCount = jsonpath.jsonpath(page_data, data_compile_pageCount)
        
        artwork_tag = jsonpath.jsonpath(page_data, '$.body.tagTranslation')
        # 打印相关的tag
        print(f"[相关的标签]:{artwork_tag}")
        # 打印作品总数
        print(f"[作品总数]:{artwork_total}")
    
        page_totle = int(artwork_total[0]/60) + 1 # 得到页面总数
        if(page_totle > 1):
            for page in range(2, page_totle+1):
                params['p'] = page
                try:
                    search_page = requests.get(url_page, headers=self.headers, params=params, cookies=self.Cookie)
                    page_data = search_page.json()
                    artwork_id += jsonpath.jsonpath(page_data, data_compile_id)
                    artwork_title += jsonpath.jsonpath(page_data, data_compile_title)
                    artwork_pageCount += jsonpath.jsonpath(page_data, data_compile_pageCount)

                    # 关闭请求
                    search_page.close()
                    print('\r', '[数据获取进度]:%s %.2f%%' % ('>'*int(page/page_totle*50), float(page/page_totle*100)), end=' ')
                except BaseException as error:
                    print("数据抓取发生错误(；д；)")
                    with open(self.log_path, 'a', encoding="utf-8")as f:
                        f.write(str(error) + f'\n{STATE.ERROR_2.value}')
        else:
            pass
        
        search_page.close()
        print('数据抓取成功(^ヮ^)\n正在处理数据')

        # 将数据处理成字典
        datadic = {}
        for key in range(artwork_total[0]):
            datadic[f'{key}'] = {} # 创建嵌套的字典
            datadic[str(key)]['id'] = artwork_id[key]
            datadic[str(key)]['title'] = artwork_title[key]
            datadic[str(key)]['pageCount'] = artwork_pageCount[key]
            datadic[str(key)]['dowmload_flag'] = 0
            # print('\r', '[数据处理进度]:%s %.2f%%' % ('>'*int(key/artwork_total[0]*50), float(key/artwork_total[0]*100)), end=' ')

        self.data_integrated(data=datadic)
        with open(self.log_path, 'a', encoding="utf-8")as f:
            f.write(f"\n{STATE.INITIALIZED.value}")
        
        print("数据初始化完成")

        
        '''     
        data_page = re.finditer('"id":"(?P<id>\d+)","title"', search_page.text)
        for it in data_page:
            id = it.group('id')
            author_id.append(id)

        # 获取 作者的id
        # search_input_soup=search_soup.find()
        # data_compile=re.compile("{.*?}",re.S)
        # data=re.findall(data_compile,search_input_soup['data-items']) 
        '''

   
    
    # def single_get(self, id, title):

    # def multipel_get(self, id, title, pageCount):

    def picture_get(self, data):
        '''
        获取并下载图片
        :param data 字典类型 的数据
        '''
        for sequence in data:
            id = data[sequence]['id']
            title = data[sequence]['title']
            pageCount = data[sequence]['pageCount']
            

    def artworkpage_get(self):
        '''
        获取作品页面数据
        将详细信息再次整合
        '''
        
        # 检查是否有作品文件夹，没有则创建文件夹
        path = './artworks'
        if not os.path.exists(path):   
            os.mkdir(path)
        
        # 解析数据
        data = self.data_load()
        print('数据解析完成◕ω◕')

        # 发送 作者的图片所对应的页面的 请求
        for sequence in data:
            id = data[sequence]['id']
            pageCount = data[sequence]['pageCount']
            title = data[sequence]['title']

            url_artwort = f"https://www.pixiv.net/artworks/{id}" 
            
            start = time.time() #下载开始时间

            # 发送作品页面请求
            # 预防 Traceback (most recent call last)
            # requests.adapters.DEFAULT_RETRIES = 5 # 如果失败重复5次request请求
            try:
                search_artwork = requests.get(url_artwort, headers=self.headers, cookies=self.Cookie)
            except BaseException as error:
                print("读取作品页面发生错误(；д；)")
                with open('./log.txt', 'a',encoding='utf-8')as f:
                    f.write(str(error) + f'\n{STATE.ERROR_3.value}')

            # 获取点赞等信息
            artwork_bookmarkCount = int(re.findall('"bookmarkCount":(\d+),', search_artwork.text)[0]) #收藏数量
            artwork_likeCount = int(re.findall('"likeCount":(\d+),', search_artwork.text)[0])


            if artwork_bookmarkCount >= 80 and data[sequence]['dowmload_flag']==0:
                # 获取图片地址
                if pageCount == 1: # 如果页面为单图                
                    # data_artwork = re.findall('"regular":"(?P<target>.*?)"', search_artwork.text) # 常规图
                    artwork_url = re.findall('"original":"(?P<target>.*?)"', search_artwork.text)[0] # 原图
                    search_artwork.close()

                    # 获取图片二进制 源码
                    try:
                        search_picture = requests.get(artwork_url, headers=self.headers, cookies=self.Cookie, stream=True)
                    except BaseException as error:
                        print("读取网页发生错误(；д；)")
                        with open('./log.txt', 'a', encoding='utf-8')as f:
                            f.write(str(error) + f'\n{STATE.ERROR_4.value}')
                    # 进度条显示
                    # size = 0    #初始化已下载大小
                    # chunk_size = 1024  # 每次下载的数据大小

                    # 获取图片的大小
                    content_size = len(search_picture.content) # 图片总的字节数(byte)
                    print("[File size]:{size:.2f} MB".format(size = content_size/1024/1024), end=' ')

                    # 保存图片
                    flie_path = f"{path}//{id}-{title_process(title)}.jpg"
                    with open(flie_path, "wb")as f:  # wb是写二进制
                        f.write(search_picture.content)
                        '''
                        for data in search_artwork.iter_content(chunk_size = chunk_size):
                            f.write(search_picture.content)
                            size += len(data)
                            print('\r', '[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
                        '''
                        end = time.time()   #下载结束时间
                        print(f'[图片{sequence}]:Download completed!,times: %.2f秒' % (end - start))  #输出下载用时时间
                        search_picture.close()
                        
                        # 日志记录
                        with open('./log.txt','a', encoding='utf-8')as f:
                            f.write(f'\n[图片{sequence}]:Download completed!,times: %.2f秒' % (end - start))

                    data[sequence]['dowmload_flag'] = 1

                else : # 获取多图的异步请求
                    url_artwort = f"https://www.pixiv.net/ajax/illust/{id}/pages"
                    params = {
                        'lang': 'zh',
                        'version': '82d3db204a8e8b7e2f627b893751c3cc6ef300fb'
                    }
                    try:
                        search_artwork = requests.get(url_artwort, headers=self.headers, params=params, cookies=self.Cookie)
                    except BaseException as error:
                        print("读取作品页面发生错误(；д；)")
                        with open('./log.txt', 'a',encoding='utf-8')as f:
                            f.write(str(error) + f'\n{STATE.ERROR_3.value}')

                    artwork_url = jsonpath.jsonpath(search_artwork.json(), "$..original")

                    for page in range(pageCount):
                        # 获取图片二进制 源码
                        try:
                            search_picture = requests.get(artwork_url[page], headers=self.headers, cookies=self.Cookie, stream=True)
                        except BaseException as error:
                            print("读取网页发生错误(；д；)")
                            with open('./log.txt', 'a', encoding='utf-8')as f:
                                f.write(str(error) + f'\n{STATE.ERROR_4.value}')

                        # 获取图片的大小
                        content_size = len(search_picture.content) # 图片总的字节数(byte)
                        print("[File size]:{size:.2f} MB".format(size = content_size/1024/1024), end=' ')

                        # 保存图片
                        flie_path = f"{path}//{id}-{title_process(title)}-{page}.jpg"
                        with open(flie_path, "wb")as f:  # wb是写二进制
                            f.write(search_picture.content)
                            end = time.time()   #下载结束时间
                            print(f'[图片{sequence}-{page}]:Download completed!,times: %.2f秒' % (end - start))  #输出下载用时时间
                            search_picture.close()
                            
                            # 日志记录
                            with open('./log.txt','a', encoding='utf-8')as f:
                                f.write(f'\n[图片{sequence}-{page}]:Download completed!,times: %.2f秒' % (end - start))

                        search_artwork.close()
                    data[sequence]['dowmload_flag'] = 1

            else:
                continue

            # 将数据再次整合
            data[sequence]['artwork_bookmarkCount'] = artwork_bookmarkCount
            data[sequence]['artwork_likeCount'] = artwork_likeCount
            data[sequence]['artwork_url'] = artwork_url

            self.data_integrated(data)

                # # 获取图片二进制 源码
                # try:
                #     search_picture = requests.get(artwork_url, headers=self.headers, cookies=self.Cookie, stream=True)
                # except BaseException as error:
                #     print("读取网页发生错误(；д；)")
                #     with open('./log.txt', 'a', encoding='utf-8')as f:
                #         f.write(str(error) + f'\n{STATE.ERROR_4.value}')
                # # 进度条显示
                # # size = 0    #初始化已下载大小
                # # chunk_size = 1024  # 每次下载的数据大小

                # # 获取图片的大小
                # content_size = len(search_picture.content) # 图片总的字节数(byte)
                # print("[File size]:{size:.2f} MB".format(size = content_size/1024/1024), end=' ')

                # # 保存图片
                # flie_path = f"{path}//{id}-{title_process(title)}.jpg"
                # with open(flie_path, "wb")as f:  # wb是写二进制
                #     f.write(search_picture.content)
                #     '''
                #     for data in search_artwork.iter_content(chunk_size = chunk_size):
                #         f.write(search_picture.content)
                #         size += len(data)
                #         print('\r', '[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
                #     '''
                #     end = time.time()   #下载结束时间
                #     print(f'[图片{sequence}]:Download completed!,times: %.2f秒' % (end - start))  #输出下载用时时间
                #     search_picture.close()
                    
                #     # 日志记录
                #     with open('./log.txt','a', encoding='utf-8')as f:
                #         f.write(f'\n[图片{sequence}]:Download completed!,times: %.2f秒' % (end - start))

            
        
        # 日志记录
        with open('./log.txt','a', encoding='utf-8')as f:
            f.write('STATE.FINISH.value')
        print('STATE.FINISH.value')




#输入对应参数
# tags = '小鸟游六花'
# login_id = '1054897561@qq.com'
# password = '200443jhd'

with open('./readme.txt', 'r',encoding='utf-8')as f:
    readme = f.readlines()
    for line in readme:
        print(line)
        time.sleep(3)

while True:
    tags = input("请输入女♂孩子的名字（≧▽≦）:")
    if tags.strip():  # 检查去除空格后的内容是否为空
        break  # 如果非空，退出循环
    else:
        print("标签不能为空，请重新输入。")

login_id = input('请输入pixiv账号:')
password = input('请输入pixiv密码:')


# 创建爬虫实例
bugger = Pixiv_bugger(tags= tags, login_id=login_id, password=password)

# 检查程序运行状态
state = log_check(bugger.log_path)

# 创建日志和数据库
bugger.log_creat()

# 模拟登录
bugger.login()

# 取得数据并存入 data文件
if state == STATE.UNINITIALIZED.name or state == STATE.PRIMARY.name:
    bugger.data_get()
else:
    print('\n数据已完成初始化')
    
# 取得图片
bugger.artworkpage_get()




























