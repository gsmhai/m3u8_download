# -*- coding: utf-8 -*-
# version: 0.1
# source: https://github.com/gsmhai/m3u8_download
# author: gsmhai

import os
import m3u8
import requests
import traceback
import threadpool
from Crypto.Cipher import AES

########################################## Extern input variable ######################################################
# 主程序下载的m3u8 url
m3u8Url = 'https://dalao.wahaha-kuyun.com/20201209/4679_4c0f5c63/1000k/hls/index.m3u8'
saveFile = 'Z:/碰撞地球.mp4'
cachePath = "Z:/cache"
proxy = {'http': 'http://10.217.10.40:80', 'https': 'https://10.217.10.40:80'}
UseProxy = False
breakSignal = None
printSignal = None
initSignal = None
updateSignal = None
MainUI = None
########################################## Local global variable ######################################################
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74"
}
# 本地m3u8链接批量
# 文件格式: 视频名称,m3u8地址
# eg: 鬼吹灯之龙岭迷窟,https://v5.szjal.cn/20200904/pqq5L2pb/index.m3u8
m3u8IndexFile = "Z:/index.m3u8"


taskThreadPool = None
threadPoolCount = 50
reqRetryTimes = 10
totalCount = 0
doneCount = 0
HostUrl = ''


def getM3u8Info():
    global m3u8Url
    global HostUrl
    global proxy
    global UseProxy
    retry = reqRetryTimes
    while True:
        if retry < 0:
            PrintInfo("M3U8下载失败！")
            return None
        retry -= 1
        try:
            if UseProxy is True:
                response = requests.get(m3u8Url, headers=headers, timeout=20, allow_redirects=True, proxies=proxy, verify=False)
            else:
                response = requests.get(m3u8Url, headers=headers, timeout=20, allow_redirects=True)
            if response.status_code == 301:
                m3u8Url = response.headers["location"]
                continue
            if '#EXTM3U' in response.text:
                HostUrl = m3u8Url[0:m3u8Url.rindex('/')]
                break
            else:
                raise Exception("未找到M3U8文件头！")
        except TimeoutError:
            traceback.print_exc()

    m3u8_info = m3u8.loads(response.text)
    if m3u8_info.is_variant:
        PrintInfo("下载多级码流M3U8文件...")
        for stream_url in response.text.split('\n'):
            if stream_url.endswith(".m3u8"):
                if stream_url.startswith("/"):
                    stream_url = stream_url[1:]
                    HostUrl = m3u8Url[0:m3u8Url.index('/', m3u8Url.index('://')+3)]
                else:
                    HostUrl = m3u8Url[0:m3u8Url.rindex('/', )]
                m3u8Url = HostUrl + '/' + stream_url
                return getM3u8Info()
        
        PrintInfo("未发现M3U8视频流！")
        return None
    else:
        return m3u8_info


def getKey(key_url):
    retry = reqRetryTimes
    while True:
        if retry < 0:
            PrintInfo("Key 下载失败！")
            return None
        retry -= 1
        try:
            if UseProxy is True:
                response = requests.get(key_url, headers=headers, timeout=20, allow_redirects=True, proxies=proxy, verify=False)
            else:
                response = requests.get(key_url, headers=headers, timeout=20, allow_redirects=True)
            if response.status_code == 301:
                key_url = response.headers["location"]
                PrintInfo("重定向继续下载Key！")
                continue
            expected_length = int(response.headers.get('Content-Length'))
            actual_length = len(response.content)
            if expected_length > actual_length:
                raise Exception("key下载不完整")
            PrintInfo("Key下载成功！key = {0}".format(response.content.decode("utf-8")))
            break
        except:
            PrintInfo("Key下载失败！")
    return response.text


def thread_download_ts(playlist):
    global totalCount
    global doneCount
    global taskThreadPool
    task_list = []
    if len(playlist) > 0:
        for index in range(len(playlist)):
            dic = {"ts_url": playlist[index], "index": index}
            task_list.append((None, dic))
        doneCount = 0
        totalCount = len(task_list)
        PrintInfo("加入线程池，开始下载ts...")
        request_ts = threadpool.makeRequests(download_ts, task_list)
        [taskThreadPool.putRequest(req) for req in request_ts]
        taskThreadPool.wait()
        return True
    else:
        PrintInfo("未找到可下载的流文件！")
        return False


def download_ts(ts_url, index):
    global totalCount
    global doneCount
    global cachePath
    global HostUrl
    succeed = False
    while not succeed:
        ts_path = cachePath + "/" + "{0:0>8}.ts".format(index)
        with open(ts_path, "wb+") as fp:
            UpdatePlayList([index, '下载中..'])
            try:
                if UseProxy is True:
                    response = requests.get(ts_url, headers=headers, timeout=20, allow_redirects=True,proxies=proxy, verify=False)
                else:
                    response = requests.get(ts_url, timeout=10, headers=headers, stream=True)
                if response.status_code == 200:
                    expected_length = int(response.headers.get('Content-Length'))
                    actual_length = len(response.content)
                    if expected_length > actual_length:
                        raise Exception("视频分片：{0:0>8} 下载长度异常".format(index))
                    fp.write(response.content)
                    doneCount += 1
                    UpdatePlayList([index, '完成'])
                    printProcess(doneCount, totalCount)
                    succeed = True
            except:
                PrintInfo("视频分片：{0:0>8} 下载失败！正在重试...".format(index))


def merge_ts(tsFileDir, outputFilePath, cryptor, count):
    with open(outputFilePath, "wb+") as tag_file:
        for index in range(count):
            printProcess(index+1, count)
            ts_path = tsFileDir + "/" + "{0:0>8}.ts".format(index)
            if not os.path.exists(outputFilePath):
                PrintInfo("视频分片： {0:0>8}.ts, 不存在，跳过！".format(index))
                continue
            with open(ts_path, "rb") as fp:
                data = fp.read()
                try:
                    if cryptor is None:
                        tag_file.write(data)
                    else:
                        tag_file.write(cryptor.decrypt(data))
                except Exception as exception:
                    tag_file.close()
                    PrintInfo(exception)
                    return False
    return True


def ffmpegToMp4(inputFilePath, ouputFilePath):
    shell = r'ffmpeg -i "{0}" -vcodec copy -acodec copy "{1}"'.format(inputFilePath, ouputFilePath)
    if os.system(shell) == 0:
        PrintInfo(inputFilePath + "转换成功")
        return True
    else:
        PrintInfo(inputFilePath + "转换失败！")
        return False


def VideoDownloader():
    global saveFile
    global m3u8Url
    global cachePath
    global HostUrl
    PrintInfo("开始下载M3U8...")
    m3u8_info = getM3u8Info()
    if m3u8_info is None:
        return False
    dnlist = []
    for playlist in m3u8_info.segments:
        if playlist.uri.find("://") > 0:
            stream_url = playlist.uri
        elif playlist.uri.startswith("/"):
            HostUrl = m3u8Url[0:m3u8Url.index('/', m3u8Url.index('://')+3)]
            stream_url = HostUrl + playlist.uri
        else:
            stream_url = HostUrl + '/' + playlist.uri
        dnlist.append(stream_url)

    InitPlayList(dnlist)

    key_text = ""
    cryptor = None
    if (len(m3u8_info.keys) != 0) and (m3u8_info.keys[0] is not None):    # 判断是否加密
        # 默认选择第一个key，且AES-128算法
        key = m3u8_info.keys[0]
        if key.method != "AES-128":
            PrintInfo("{0}不支持的解密方式！".format(key.method))
            return False
        key_url = key.uri
        if not key_url.startswith("http"):
            key_url = m3u8Url.replace("index.m3u8", key_url)
        PrintInfo("开始下载key...")
        if getKey(key_url) is None:
            return False
        if key.iv is not None:  # 判断 Key 偏移量
            cryptor = AES.new(bytes(key_text, encoding='utf8'), AES.MODE_CBC, bytes(key.iv, encoding='utf8'))
        else:
            cryptor = AES.new(bytes(key_text, encoding='utf8'), AES.MODE_CBC, bytes(key_text, encoding='utf8'))

    if thread_download_ts(dnlist):
        PrintInfo("ts下载完成")
    else:
        return False
    PrintInfo("开始合并ts...")
    if merge_ts(cachePath, cachePath + "/cache.flv", cryptor, len(dnlist)):
        PrintInfo("ts合并完成！")
    else:
        PrintInfo(key_text)
        PrintInfo("ts合并失败！")
        return False
    PrintInfo("开始mp4转换...")
    if not ffmpegToMp4(cachePath + "/cache.flv",  saveFile):
        return False
    return True

def InitDownEnv():
    global taskThreadPool
    global cachePath
    if taskThreadPool is None:
        taskThreadPool = threadpool.ThreadPool(threadPoolCount)
    if not os.path.exists(cachePath):
        os.makedirs(cachePath)
    else:
        for root, dirs, files in os.walk(cachePath, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    #os.rmdir(cachePath)
    

def Download():
    InitDownEnv()
    '''
    import sys
    os.chdir(sys.path[0])
    dnlist = []
    HostUrl = 'Z:/'
    with open('index.m3u8', "r") as f:
        data = f.read()
        m3u8_info = m3u8.loads(data)
        for playlist in m3u8_info.segments:
            if playlist.uri.find("://") > 0:
                dnlist.append(playlist.uri)
            elif playlist.uri.startswith("/"):
                HostUrl = m3u8Url[0:m3u8Url.index('/', m3u8Url.index('://')+3)]
                dnlist.append(HostUrl + playlist.uri)
            else:
                dnlist.append(HostUrl + '/' + playlist.uri)

    InitPlayList(dnlist)
    UpdatePlayList([6, '完成'])
    return
    '''

    try:
        if VideoDownloader():
            PrintInfo("下载完成 ！")
    except Exception as exception:
        PrintInfo(exception)
        traceback.print_exc()
    breakSignal.emit()

def printProcess(complete, total):
    PrintInfo('完成进度: {0}/{1}   {2:.2f}%'.format(complete, total, complete*100/total))


def PrintInfo(msg=""):
    if printSignal is not None:
        printSignal.emit(msg)


def InitPlayList(playlist=[]):
    if initSignal is not None:
        initSignal.emit(playlist)


def UpdatePlayList(stat=''):
    if updateSignal is not None:
        updateSignal.emit(stat)


if __name__ == '__main__':
    with open(m3u8IndexFile, 'r', encoding="utf-8") as fp:
        while True:
            line = fp.readline().strip('\n')
            if line == "":
                break
            m3u8_info = line.split(',')
            if len(m3u8_info) > 1:
                saveFile = 'Z:/' + m3u8_info[0]+'.mp4'
                m3u8Url = m3u8_info[1]
            else:
                saveFile = 'Z:/' + '电影_' + m3u8_info[0].rsplit('.', 1)[0].rsplit('/', 1)[1]+'.mp4'
                m3u8Url = m3u8_info[0]
            Download()
