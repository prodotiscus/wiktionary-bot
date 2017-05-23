#!/usr/bin/python3
import json, re, requests
obj = json.loads(open('grc-words.json', 'r').read())
pages = []
for p in obj['pages']:
    if not re.search('[zmsrqwpilk]', p['page_title']):
        pages.append(p['page_title'])
psi = pages.index('ἐπικουρία') + 1
pages = pages[psi:]
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
    e = s.post(msp, {'action':'edit','title':page,'summary':summary,'text':text,'token':et,'bot':'1'})
def read(page):
    global s
    c = s.get('http://ru.wiktionary.org/w/index.php?title=' + page + '&action=raw')
    return c.text
for p in pages:
    print(p)
    c = read(p)
    try:
        l = re.split('=\s?\{\{-\w+-\}\}\s?=', c)
        #print(l)
        lc = re.findall('\w+(?=-\}\}\s?=\n)', c)
        #print(lc)
        grc_code = l[lc.index('grc') + 1]
        new_grc_code = re.sub('\{\{transcription.*', '{{transcription-grc|' + p + '}}', grc_code)
        c = c.replace(grc_code, new_grc_code)
        edit(p, c, 'Добавление древнегреческой транскрипции')
    except:
        print('Some error with ' + p)