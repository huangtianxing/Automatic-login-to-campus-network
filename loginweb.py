import argparse
import configparser
import json
import os
import platform
import sys
import time
from subprocess import run, PIPE

import requests


def login(username, password):
    # 定义post数据
    data = dict(qrCodeId='', username='', pwd='', validCode='', validCodeFlag='', ssid='', mac='', t='', wlanacname='',
                url='', nasip='', wlanuserip='')
    data['username'] = username
    data['pwd'] = password
    data['qrCodeId'] = '请输入编号'
    data['validCode'] = '验证码'
    data['validCodeFlag'] = 'false'
    try:
        first_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47',
                        'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
        r = requests.get('http://www.baidu.com', headers=first_header)
        # print(r.headers)
        # print(r.request.headers)
    except:
        # print("r = requests.get('http://www.baidu.com') failed!")
        write_log("r = requests.get('http://www.baidu.com') failed!")
        return
    url = r.text.split('\'')[1]
    login = requests.get(url, headers=first_header)
    attrlist = login.url.split('?')[-1].split('&')
    for i in range(0, len(attrlist)):
        key = attrlist[i].split('=')[0]
        value = attrlist[i].split('=')[1]
        if key in data.keys():
            data[key] = value

    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Content-Length': '451',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '',
        'Host': '',
        'Origin': '',
        'Pragma': 'no-cache',
        'Referer': '',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
        'X-Requested-With': 'XMLHttpRequest'

    }
    filecounter = 'failCounter=0'
    cookies = 'JSESSIONID=' + login.cookies.get_dict()['JSESSIONID'] + ': ' + filecounter
    header['Referer'] = login.url
    header['Cookie'] = cookies
    header['Host'] = login.url.split('/')[2]
    header['Origin'] = 'http://' + header['Host']

    loginurl = header['Origin'] + '/zportal/login/do'
    try:
        do = requests.post(loginurl, data=data, headers=header)
    except:
        print('login failed!')
        return
    datas = json.loads(do.text)
    if datas['result'] == 'success':
        # print('login success!')
        write_log('login success!')
    elif datas['result'] == 'online':
        # print(datas['message'])
        write_log(datas['message'])
    else:
        # print(datas['message'])
        write_log(datas['message'])


def write_log(log_txt):
    corrent_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
    logfile = os.path.join(corrent_dir, 'login.txt')
    with open(logfile, 'a') as f:
        f.write(log_txt + '\n')


def readconfig():
    corrent_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
    configfile = os.path.join(corrent_dir, 'config.ini')
    config = configparser.ConfigParser()
    if not os.path.exists(configfile):
        write_log('No configuration file, creating!')
        createconfig(configfile)

    config.read(configfile, encoding="utf-8")
    username = config.get('global', 'username')
    password = config.get('global', 'password')
    return username, password


def createconfig(configfile):
    config = configparser.ConfigParser()
    config.read(configfile, encoding="utf-8")
    if not config.has_section("global"):
        config.add_section("global")
    if not config.has_option("global", "username"):
        config.set('global', 'username', '')
    if not config.has_option("global", "password"):
        config.set('global', 'password', '')
    config.write(open(configfile, 'w'))


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--username', type=str, default=None)
    # parser.add_argument('--password', type=str, default=None)
    # opt = parser.parse_args()

    write_log('\n' + time.asctime())
    username, password = readconfig()
    if platform.system() == 'Windows':
        netok = run(["ping www.baidu.com"], stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    else:
        netok = run(["ping -c 3 www.baidu.com"], stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    if netok.returncode == 0:
        # print('network connect ok!')
        write_log('Network connect is ok!')
    elif username == '' or password == '':
        write_log('No username or password!')
        # print('no network!')
    else:
        write_log('No network, connecting!')
        login(username, password)
