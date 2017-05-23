#!/usr/bin/python3
import re, codecs, json, requests
d = codecs.open('GrcRu.dsl', 'r', encoding='utf-16').read()
d = d.replace('\xa0', '')
headers = re.findall('(?<=\[b\]\[c\sgray\])[^\[]{2,}(?=\[/c\]\[/b\])', d)
names = re.findall('(?<=\n)[A-ζ].*(?=\r\n\t)', d)[1:]
def get_article(index):
    #w = re.findall(r'(?<=' + names[index] + r')\r\n\t(\[m1\].*\r\n\t)+\[m1\].*\r\n(?=' + names[index+1] + r')', d)
    w = re.findall(r'(?<='  +names[index] + r')\r*\n((\t\[m1\].+\r*\n)+)', d)
    #q = re.split('(?<=\n)' + names[index], d)
    #w = re.split('(?<=\n)' + names[index + 1], q[1])
    return w[0][0]
def get_meanings(i):
    global article
    article = get_article(i)
    article = re.sub('\([А-я]+\)', '', article)
    gr = re.findall('(?<=\[b\]\[c\sgray\])[^\[]{2,}(?=\[/c\]\[/b\])', article)[0]
    if re.search('\d+\)\[/\!trs\][^\[]+', article):
        translations = re.findall('\d+\)\[/\!trs\][^\[]+', article)
        t = []
        for tr in translations:
            tr = re.sub('^\d+\)\[/\!trs\]\s', '', tr)
            t.append(tr)
    else:
        t = re.findall('[А-я][А-я\s,;]+', article)
    return {'greek' : gr, 'russian' : t}
msp = 'http://ru.wiktionary.org/w/api.php'
user = '...'
password = '...'
s = requests.Session()
lr = s.post(msp, {'action':'login', 'lgname':user, 'lgpassword':password, 'format':'json'})
token = json.loads(lr.text)['login']['token']
li = s.post(msp, {'action':'login', 'lgname':user, 'lgpassword':password, 'lgtoken':token, 'format':'json'})
get = s.get(msp + '?action=query&prop=info|revisions&intoken=edit&rvprop=timestamp&titles=Main%20Page&format=json')
et = json.loads(get.text)['query']['pages'][list(json.loads(get.text)['query']['pages'])[0]]['edittoken']
#
def edit(page, text, summary):
    global s, et
    e = s.post(msp, {'action':'edit','title':page,'summary':summary,'text':text,'token':et,'bot':'1','recreate':'','createonly':1})
def read(page):
    global s
    c = s.get('http://ru.wiktionary.org/w/index.php?title=' + page + '&action=raw')
    return c.text
def read_alpha