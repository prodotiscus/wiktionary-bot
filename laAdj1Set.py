#!/usr/bin/python3
import json, re, requests
pages = json.loads(open('la-adj.json', 'r').read())
pages = pages[1:]
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
    if p[-2:] == 'us':
        print(p)
        c = read(p)
        try:
            c = re.sub('прил\sla\s*', 'прил la 1a|' + p[:-2] + '|', c)
            edit(p, c, 'добавление шаблона 1a склонения')
        except:
            print('Some error with ' + p)