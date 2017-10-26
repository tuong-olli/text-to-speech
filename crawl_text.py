# -*- coding: utf-8 -*-
import newspaper, codecs
from newspaper import Article
import requests
from bs4 import BeautifulSoup
import codecs, csv
import librosa
import numpy as np
from util import audio

url = "http://bazantravel.com/am-thuc/am-thuc-can-tho"
name = "vn_"
num = 1641
story = list()
docs = list()
count = 0

def read_article(url):
    art = Article(url, language = 'vi')
    #print(fulltext(url, language='vi'))
    art.download()
    art.parse()
    return art.title + '.\n' +art.text + '.\n'


def read_url(url):
    paper = newspaper.build(url)
    i=0
    names = url.split('//')
    for article in paper.articles:
        print ("Process to "+str(article.url))
        fout = codecs.open('/home/tuong/Downloads/tacotron/bongdavn/'+names[1].split('.')[0]+str(i)+'.txt','w')
        fout.write(read_article(article.url))
        fout.close()
        i += 1

def get_url(url):
    html = requests.get(url+'/').text
    #print(html)
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        #print(link)
        if href.split('//')[0] == 'http:' and story.count(href) <= 0 \
                and str(href) !='http://dien-kien-5-dia-diem-vui-choi-trung-thu-tai-da-nang-chua-bao-gio-ngung-hot' \
                and str(href) != 'http://hoi%20anhttp://bazantravel.com/diem-den-du-lich/diem-tham-quan-hoi-an/':
            print(href)
            story.append(href)
            get_url(href)

def getfile(url):
     global count
     html = requests.get(url+'/').text
     soup = BeautifulSoup(html, 'html.parser')
     with open('link.txt', 'a') as f:
         for link in soup.find_all('a'):
             href = link.get('href')
             # if (str(href).split('/')[0] == 'http:' or\
             #                 str(href).split('/')[0] == 'https:') and \
             #                 docs.count(href) <= 0 and \
             #                 len(str(href))>10:
             #     print(href)
             #     docs.append(str(href))
             #     f.write(str(count)+' '+str(href)+'\n')
             #     count+=1
             if len(str(href)) > 10 and docs.count(str(href)) <= 0 and href.split(':')[0] !='javascript' and href != '/nhip-song/cuoi.html' \
                     and href.split(':')[0] != 'http' \
                     and href.split(':')[0] != 'https':
                 print(href)
                 docs.append('https://news.zing.vn'+str(href))
                 f.write(str(count) + ' ' + str(href) + '\n')
                 count += 1

def get_data():
    global num
    num = 0
    #print("dddddd")
    for doc in docs:
        print(doc)
        with codecs.open(str(num) + ".txt", 'w', 'utf-8') as f:
            html = requests.get(doc).text
            soup = BeautifulSoup(html, 'html.parser')
            for p in soup.find_all('p'):
                f.write(str(p.text)+'\n')
            num += 1
def presize(audio):
    y, sr = librosa.core.load(audio)
    spectrogram = librosa.feature.melspectrogram(y, sr=sr)
    log_S = librosa.logamplitude(spectrogram, ref_power=np.max)
    s = log_S[:, 150:].reshape(-1)
    av_s, std_s = np.average(s), np.std(s)
    print(spectrogram.shape)

    print(av_s, std_s)

    clen = spectrogram.shape[1]
    window_size = 30
    pos = clen
    std_s = 2
    power = None
    for i in range(clen-window_size):
        tmp_w = log_S[:,i:i+window_size]
        av_w = np.average(tmp_w)
        if av_w > av_s - 1.5 * std_s and av_w < av_s + 1.5 * std_s:
            pos = i
            print(pos)
            break
    print(pos)

    power = np.max(spectrogram)
    # power = np.max
    # power = np.median
    spectrogram = spectrogram[:,:pos]
    print(spectrogram.shape)
    librosa.output.write_wav("out_trim.wav", y, sr)
def testing():
    spectrogram = np.load('olli-mel-00001.npy')
    wav = audio.inv_spectrogram(spectrogram.T)
    audio.save_wav(wav, 'test-audio.wav')
if __name__=="__main__":
    #testing()
    # for i in range(1, 500):
    #     if i==1:
    #         getfile('http://www.tinthethao.com.vn/bong-da-viet-nam')
    #     else: getfile('http://www.tinthethao.com.vn/bong-da-viet-nam/p'+str(i))
    getfile('https://news.zing.vn/bong-da-viet-nam.html')
    get_data()
    #read_url('http://bazantravel.com')


    #get_url('http://bazantravel.com/am-thuc/am-thuc-can-tho')
    #for link in story:
    #    get_data(link)
    #global num
    # num = 0
    # with open('link', 'r') as fin:
    #     for link in fin.readlines():
    #         print(link)
    #         with codecs.open(str(num) + ".txt", 'w', 'utf-8') as f:
    #             html = requests.get(link).text
    #            # print(html)
    #             soup = BeautifulSoup(html, 'html.parser')
    #             for p in soup.find_all('p'):
    #                 f.write(str(p.text) + '\n')
    #             num += 1
    #presize('vn_5650_Nhi.wav')