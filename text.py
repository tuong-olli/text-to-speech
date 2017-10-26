import csv
import nltk, os
import string
import enchant
import re


count = dict()

def get_filepaths(directory):
    """
    Load data file paths
    :param directory:
    :return:
    """
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths
def generate_text():
    fmusic = open('amnhac_vi.txt', 'r')
    musics = list()
    singers = list()
    musicians = list()
    for music in fmusic.readlines():
        musics.append(music)
    fsinger = open('singer', 'r')
    for singer in fsinger.readlines():
        singers.append(singer)
    fmusician = open('musician', 'r')
    for musician in fmusician.readlines():
        musicians.append(musician)
    with open('out_generate', 'w') as fwrite:
        num = 0
        for step in range(25):
            with open('generate', 'r') as fread:
                for line in fread.readlines():
                    out = ''
                    tokens = nltk.word_tokenize(line)
                    num += 1
                    for token in tokens:
                        if out != '' and token != ':' \
                                and token != '?' and token != ',' \
                                and token != '.' and token != ')' \
                                and tokens[tokens.index(token) -1] != '(': out += ' '
                        if token == 'music':
                            out += musics.pop()[:-1]
                        elif token == 'musicians':
                            out += musicians.pop()[:-1]
                            musicians.pop()
                        elif token == 'singer':
                            out += singers.pop()[:-1]
                        elif token == 'number':
                            out += int_to_vn(num)
                        else: out += token
                    print(out)
                    fwrite.write(out+'\n')
    fmusic.close()
    fsinger.close()
    fmusician.close()
def text(output, dir):
    with open(output, 'w') as fout:
        files = get_filepaths(dir)
        for file in files:
            print(file)
            with open(file, 'r') as fin:
                for line in fin.readlines():
                    if line == '':
                        break
                    tokens = line.split(' ')
                    if line != '\n' and line != ' ' \
                            and len(tokens) > 7:
                        check = 0
                        for word in tokens:
                            if word not in string.punctuation and word not in count:
                                    check = check + 1
                        if check >= 10:
                            out = list()
                            for word in tokens:
                                if word not in string.punctuation:
                                    out.append(word)
                                    if word not in count:
                                        count[word] = 1
                                    else:
                                        count[word] += 1
                            fout.write(' '.join(out))

def rewrite_index():
    i = 4194
    with open('256', 'w') as w:
        with open('25', 'r') as f:
            for line in f.readlines():
                t1 = line.split(':')
                w.write('vn_'+ str(i) +':'+t1[1])
                i+=1

def detectEnglish(input):
    fe = open('en_'+input, 'w', encoding='utf-8')
    fv = open('vi_'+input, 'w', encoding='utf-8')
    with open(input, 'r') as fin:
        d = enchant.Dict("en_US")
        for line in fin.readlines():
            tokens = nltk.word_tokenize(line)
            check = False
            for token in tokens:
                if d.check(token):
                    check = True
                    break
            if check:
                fe.write(line)
            else: fv.write(line)
    fe.close()
    fv.close()


def int_to_vn(num):
    d = {0: 'không', 1: 'một', 2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm', 6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín', 10: 'mười'}
    if num <= 10: return d[num]
    if num//1000000 > 0:
        if num % 1000000 == 0: return int_to_vn(num // 1000000) + " triệu"
        if num%1000000 <= 10:
            return int_to_vn(num//1000000) + " triệu không nghìn không trăm linh "+int_to_vn(num % 1000000)
        if num % 1000000 < 100:
            return int_to_vn(num // 1000000) + " triệu không nghìn không trăm " + int_to_vn(num % 1000000)
        if num % 1000000 < 1000:
            return int_to_vn(num // 1000000) + " triệu không nghìn " + int_to_vn(num % 1000000)
        if num % 1000000 != 0:
            return int_to_vn(num // 1000000) + " triệu " + int_to_vn(num % 1000000)
    if num // 1000 > 0:
        if num % 1000 == 0: return int_to_vn(num//1000) + " nghìn"
        if num%1000 <=10:
            return int_to_vn(num//1000) + " nghìn không trăm linh "+int_to_vn(num%1000)
        if num%1000 <100:
            return int_to_vn(num//1000) + " nghìn không trăm "+int_to_vn(num%1000)
        if num%1000 != 0:
            return int_to_vn(num//1000) + " nghìn "+int_to_vn(num%1000)
    if num // 100 > 0:
        if num%100 == 0:
            return int_to_vn(num // 100) + " trăm"
        if num%100 <10:
            return int_to_vn(num//100) + " trăm linh " + int_to_vn(num%100)
        if num%100 == 10:
            return int_to_vn(num//100) + " trăm mười"
        if num%100 != 0:
            return int_to_vn(num//100) +  " trăm " + int_to_vn(num%100)
    if num // 10 > 0 and num >= 20:
        if num%10 != 0:
            if num%10 == 5:
                return int_to_vn(num//10) + ' mươi lăm'
            if num%10 == 1:
                return int_to_vn(num//10) + ' mươi mốt'
            if num%10 == 4:
                return int_to_vn(num//10) + ' mươi tư'
            return int_to_vn(num // 10) + ' mươi ' + int_to_vn(num % 10)
        return int_to_vn(num//10) + ' mươi'
    if num // 10 > 0:
        if num == 15:
            return 'mười lăm'
        return "mười "+ d[num%10]

def processNumber(input, output):
    with open(output, 'w') as fout:
        with open(input, 'r') as fin:
            for line in fin.readlines():
                out =''
                tokens = nltk.word_tokenize(line)
                for word in tokens:
                    word_out = word
                    if word.isdigit():
                        word_out = int_to_vn(int(word))
                    date = word.split('/')
                    if len(date)==3 and date[0].isdigit() and date[1].isdigit() and date[2].isdigit():
                        word_out = ' '+int_to_vn(int(date[0]))+' tháng '+int_to_vn(int(date[1]))+' năm ' +int_to_vn(int(date[2]))

                    if len(date) == 2 and date[0].isdigit() and date[1].isdigit() and int(date[1])>12:
                        word_out = 'tháng ' + int_to_vn(int(date[0])) + ' năm ' + int_to_vn(int(date[1]))

                    if len(date) == 2 and date[0].isdigit() and date[1].isdigit() and int(date[1])<=12:
                        word_out = ' '+int_to_vn(int(date[0])) + ' tháng ' + int_to_vn(int(date[1]))

                    if len(date) == 2 and not date[0].isdigit() and not date[1].isdigit():
                        word_out = date[0]+ ' trên '+ date[1]

                    num = word.split('.')
                    if len(num) ==2 and num[0].isdigit() and num[1].isdigit():
                        word_out = int_to_vn(int(num[0]+num[1]))

                    mnum = word.split(',')
                    if len(mnum) ==2 and mnum[0].isdigit() and mnum[1].isdigit():
                        word_out = int_to_vn(int(mnum[0]+mnum[1]))

                    if word_out == '%': word_out = 'phần trăm'
                    if word_out == tokens[0] or word_out == ',' or word_out == ';' or word_out == '.' or tokens[tokens.index(word) -1] == '(' or\
                                    word_out == ':' or word_out == '?' or word_out == '!' or word_out == ')' or word_out == '\'':
                        out += word_out
                    else: out+= ' ' + word_out
                fout.write(out+'\n')


def process2record(input, output, id):
    i=id
    with open(output, 'w') as w:
        with open(input, 'r') as f:
            for line in f.readlines():
                if line=='\n':
                    continue
                t =''
                for char in line:
                    if char != '“' and char != '”' and char != '\n' and char != '‘' and char != '’' and char !='…':
                        t += char
                text = 'vn_'+str(i)+':###'+t+'###'+'\n'
                w.write(text)
                i+=1

def process2train(input, output):
    with open(output, 'w') as m:
        with open(input, 'r') as f:
            for line in f.readlines():
                if line == '\n':
                    break
                t = line.split('###')
                print(t)
                output = t[0].split(':')[0]+'_Nhi'+'|'+t[1]+'|'+t[1]+'\n'
                m.write(output)

def process2csv():
    write = csv.writer(open('metadata.csv', 'a'))
    readline = csv.reader(open('thethaovanhoa-v1-train.txt', 'r'), delimiter=',')
    write.writerows(readline)

def checkFile():
    files  = get_filepaths('/home/tuong/Downloads/tacotron/data_train/wavs')
    f = list()
    names = list()
    for file in files:
        f.append(file.split('/')[-1].split('.')[0])
    print(len(f))
    datas = open('/home/tuong/Downloads/tacotron/data_train/matching', 'r')
    for data in datas.readlines():
        names.append(data.split('|')[0])
    print(len(names))
    print("Search file in csv:")
    for name in names:
        if name not in f:
            print(name)
    print("Search name in file:")
    for file in f:
        if file not in names:
            print(file)

if __name__=="__main__":

    text('data.txt', '/home/tuong/tacotron/data') # choose sentences having new word
    detectEnglish('data.txt') # classify sentence E and VN
    #processNumber('data.txt', 'data-v1.txt') # convert number to text
    #process2record('data-v1.txt', 'data-v1-record.txt', 11000) # process to record
    #process2train('data-v1-record.txt', 'data-v1-train.txt') # process to train
    #print(int_to_vn(1000005))
    #generate_text()
    #checkFile()
