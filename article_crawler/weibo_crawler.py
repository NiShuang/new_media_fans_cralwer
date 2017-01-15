# -*- coding: UTF-8 -*-

import time
import re
import datetime
import json
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import selenium.webdriver.support.ui as ui
reload(sys)
sys.setdefaultencoding("utf-8")

'''
版本过低
pip install -U selenium
WebDriverException: Message: Can't load the profile.
Profile Dir: %s If you specified a log_file in the FirefoxBinary constructor,
check it for details.
'''

# 先调用无界面浏览器PhantomJS或Firefox
# driver = webdriver.PhantomJS(executable_path="G:\phantomjs-1.9.1-windows\phantomjs.exe")
driver = webdriver.PhantomJS()
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
# driver = webdriver.Chrome(chrome_options=options)
wait = ui.WebDriverWait(driver, 10)


# ********************************************************************************
#                  第一步: 登陆weibo.cn 获取新浪微博的cookie
#        该方法针对weibo.cn有效(明文形式传输数据) weibo.com见学弟设置POST和Header方法
#                LoginWeibo(username, password) 参数用户名 密码

#        https://www.zhihu.com/question/21451510
#        http://www.cnblogs.com/fnng/p/3606934.html
#                             验证码暂停时间手动输入
# ********************************************************************************

def LoginWeibo(username, password):
    # **********************************************************************
    # 直接访问driver.get("http://weibo.cn/5824697471")会跳转到登陆页面 用户id
    #
    # 用户名<input name="mobile" size="30" value="" type="text"></input>
    # 密码 "password_4903" 中数字会变动,故采用绝对路径方法,否则不能定位到元素
    #
    # 勾选记住登录状态check默认是保留 故注释掉该代码 不保留Cookie 则'expiry'=None
    # **********************************************************************

    # 输入用户名/密码登录
    print u'准备登陆Weibo.cn网站...'
    driver.get("http://weibo.com/")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(lambda x: x.find_element_by_id("loginname"))
    except TimeoutException:
        return

    # time.sleep(5)

    elem_user = driver.find_element_by_id("loginname")
    elem_user.send_keys(username)  # 用户名
    elem_pwd = driver.find_element_by_name("password")
    elem_pwd.send_keys(password)  # 密码
    # elem_rem = driver.find_element_by_id("login_form_savestate")
    # elem_rem.click()  # 记住登录状态,默认是记住，所以不需要

    elem_sub = driver.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[6]/a")
    elem_sub.click()  # 点击登陆
    time.sleep(5)

    # 获取Coockie 推荐 http://www.cnblogs.com/fnng/p/3269450.html
    # print driver.current_url
    # print driver.get_cookies()  #获得cookie信息 dict存储
    # print u'输出Cookie键值对信息:'
    # for cookie in driver.get_cookies():
    #     #print cookie
    #     for key in cookie:
    #         print key, cookie[key]

    # driver.get_cookies()类型list 仅包含一个元素cookie类型dict
    print u'登陆成功...'


def VisitPersonPage(user_id):

    print u'准备访问个人网站.....'
    driver.get("http://weibo.cn/" + user_id)
    result = []
    print '\n'
    print u'获取微博内容信息'
    num = 1
    while num <= 10:
        url_wb = "http://weibo.cn/" + user_id + "?filter=0&page=" + str(num)
        driver.get(url_wb)
        info = driver.find_elements_by_xpath("//div[@class='c']")
        for value in info:
            print value.text
            info = value.text

            # 跳过最后一行数据为class=c
            # Error:  'NoneType' object has no attribute 'groups'
            if u'设置:皮肤.图片' not in info:
                if info.startswith(u'转发'):
                    print u'转发微博'
                    status = '转发'
                else:
                    print u'原创微博'
                    status = '原创'

                # 获取最后一个点赞数 因为转发是后有个点赞数
                str1 = info.split(u" 赞")[-1]
                # print str1
                like = 0
                if str1:
                    val1 = re.match(r'\[(.*?)\]', str1).groups()[0]
                    like = val1

                str2 = info.split(u" 转发")[-1]
                share = 0
                if str2:
                    val2 = re.match(r'\[(.*?)\]', str2).groups()[0]
                    share = val2

                str3 = info.split(u" 评论")[-1]
                comment = 0
                if str3:
                    val3 = re.match(r'\[(.*?)\]', str3).groups()[0]
                    comment = val3

                str4 = info.split(u" 收藏 ")[-1]
                flag = str4.find(u"来自")
                temp_time = str4[:(flag - 1)]
                # print temp_time
                created_time = format_time(temp_time)
                date = created_time[0:10]
                message = info[:info.rindex(u" 赞")]

                try:
                    url = value.find_element_by_xpath('div[2]/a[1]').get_attribute("href")
                except NoSuchElementException:
                    url = ''
                temp = {
                    'account': user_id,
                    'message': message,
                    # 'id': item['id_str'],
                    'public_time': created_time,
                    'date': date,
                    'share': share,
                    'like': like,
                    'comment': comment,
                    'link': url,
                    'status': status
                }
                result.append(temp)
            else:
                break
        else:
            print u'next page...\n'
        num += 1
        print '\n\n'
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

def format_time(string):
    now = datetime.datetime.now()
    result = now.strftime('%Y-%m-%d %H:%M:%S')
    if u'分钟前' in string:
        d = int(string[0:1])
        temp = now - datetime.timedelta(minutes= d)
        result =temp.strftime('%Y-%m-%d %H:%M:%S')

    elif u'今天' in string:
        t = string[-5:]
        temp = now.strftime('%Y-%m-%d')
        result = temp + ' ' + t + ':00'

    elif u'月' in string:
        temp = time.strptime(string, "%m月%d日 %H:%M".decode('utf-8'))
        result = str(now.year) + '-' + time.strftime("%m-%d %H:%M:%S", temp)

    elif len(string) == 19:
        result = string


    return result
# *******************************************************************************
#                                程序入口 预先调用
# *******************************************************************************


def get_by_selenium():
    # 定义变量
    username = '15850786305'  # 输入你的用户名
    password = '11223344'  # 输入你的密码

    # 操作函数
    LoginWeibo(username, password)  # 登陆微博

    # driver.add_cookie({'name':'name', 'value':'_T_WM'})
    # driver.add_cookie({'name':'value', 'value':'c86fbdcd26505c256a1504b9273df8ba'})
    user_id = 'insta360'
    # 注意
    # 因为sina微博增加了验证码,但是你用Firefox登陆一次输入验证码,再调用该程序即可,因为Cookies已经保证
    # 会直接跳转到明星微博那部分,即: http://weibo.cn/guangxianliuyan

    return VisitPersonPage(user_id)  # 访问个人页面

if __name__ == '__main__':
    get_by_selenium()

