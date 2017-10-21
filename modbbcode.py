#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

smile_start = '<img src="http://static.t-ru.org/smiles/'
smile_end = '.gif" alt="" />'
sm={':D':'icon_biggrin',':)':'icon_smile',':(':'icon_sad',':o':'icon_surprised',
':shock:':'icon_eek',':?':'icon_confused',':cool:':'icon_cool',':lol:':'icon_lol',
':x':'icon_mad',':wow:':'icon_razz',':blush:':'icon_redface',':cry:':'icon_cry',
':evil:':'icon_evil',':twisted:':'icon_twisted',':roll:':'icon_rolleyes',
':wink:':'icon_wink',':!:':'icon_exclaim',':?:':'icon_question',
':idea:':'icon_idea',':arrow:':'icon_arrow',':arrow2:':'icon_arrow2',
':angry:':'icon_angry',':P':'be-e',':mrgreen:':'icon_mrgreen',':boxed:':'icon_boxed',
':furious:':'icon_furious',':greedy:':'icon_greedy',':in_love:':'icon_in_love',
':rant:':'icon_rant',':sick:':'icon_sick',':wall:':'icon_wall',
':weep:':'icon_weep',':yawn:':'icon_yawn',':up:':'ges_up',':down:':'ges_down',
':yes:':'ges_yes',':no:':'ges_no',':help:':'ges_help',':bow:':'ges_bow',
':clap:':'ges_clap',':clap2:':'ges_clap2',':hmm:':'ges_hmm',':slap:':'ges_slap',
':biker:':'ppl_biker',':chef:':'ppl_chef',':cylon:':'ppl_cylon',':hannibal:':'ppl_hannibal',
':santa:':'santa',':indian:':'ppl_indian',':king:':'ppl_king',':mario:':'ppl_mario',
':ninja:':'ppl_ninja',':ninjajig:':'ppl_ninjajig',':shuriken:':'ppl_shuriken',
':oldtimer:':'ppl_oldtimer',':snegurochka:':'snegurochka',':pimp:':'ppl_pimp',
':pirat:':'ppl_pirat',':pirate:':'ppl_pirate',':police:':'ppl_police',
':pop:':'ppl_pop',':priest:':'ppl_priest',':punk:':'ppl_punk',
':rambo:':'ppl_rambo',':rock:':'ppl_rock',':newyear:':'new_year',
':smurf:':'ppl_smurf',':spidey:':'ppl_spidey',':wolverine:':'ppl_wolverine',
':zorro:':'ppl_zorro',':artist:':'ext_artist',':argue:':'ext_argue',
':baby:':'ext_baby',':beer:':'ext_beer',':beer2:':'ext_beer2',
':book:':'ext_book',':bounce:':'ext_bounce',':box:':'ext_box',
':cigar:':'ext_cigar',':clown:':'ext_clown',':cry_baby:':'ext_crybaby',
':crutch:':'ext_crutch',':doc:':'ext_doc',':drunk:':'ext_drunk',
':flex:':'ext_flex',':jump2:':'ext_jump2',':lamo:':'ext_lame',
':komp_cr:':'ext_komp_cr',':hooray:':'ext_hooray',':hump:':'ext_hump',
':icecream:':'ext_icecream',':kiss:':'ext_kiss',':lovers:':'ext_lovers',
':mobile:':'ext_mobile',':music:':'ext_music',':secret:':'ext_secret',
':shutup:':'ext_shutup',':sleep:':'ext_sleep',':spider:':'ext_spider',
':tease:':'ext_tease',':tomato:':'ext_tomato',':wheelcha:':'ext_wheelcha',
':2guns:':'gun_2guns',':axe:':'gun_axe',':bash:':'gun_bash',
':chair:':'gun_chair',':gun:':'gun_gun',':alien:':'non_alien',
':bananadance:':'non_banana1',':bananadance2':'non_banana2',
':cat:':'non_cat',':clover:':'non_clover',':homestar:':'non_homestar',
':love:':'non_love',':nuke:':'non_nuke',':shaun:':'non_shaun',
':angel:':'big_angel',':band:':'big_band',':hang:':'big_hang',
':hbd:':'big_hbd',':ban:':'tr_ban',':hi:':'tr_hi',':offtopic:':'tr_offtopic',
':respect:':'tr_respect',':rip:':'tr_rip',':RTFM:':'tr_rtfm',':russ:':'tr_russ',
':t_oops:':'tr_oops',':sorry:':'tr_sorry',':spam:':'tr_spam',
':thankyou:':'tr_thankyou',':biggrin:':'icon_biggrin2',
':crazy:':'crazy0to',':hooligan:':'hooligan',':closetema:':'closetema',
':disk:':'disk',':jumper:':'jumper',':P:':'be-e-e',':dancer:':'dancer',
':kiss2:':'kiss',':girls_dance:':'girls_dance',':beautiful:':'beautiful',
':finest:':'finest',':modesty:':'modesty',':amazement:': 'amazement',
':affliction:': 'affliction ',':stupid:': 'stupid',':coolest:':'coolest',
':bis:':'bis',':rose:':'in_love2',':anime_01:':'anime_01',
':anime_02:':'anime_02',':anime_03:':'anime_03',':anime_04:':'anime_04',
':anime_05:':'anime_05',':anime_06:':'anime_06',':dont_ment:':'ext_dont_ment',
':gimmefive:':'ext_gimmefive',':mirror:':'ext_mirror',':skillet:':'ext_skilletgirl',
':good:':'good',':ne:':'ne',':kiss3:':'kiss3',':na_metle:':'na_metle',
':lock:':'lock',':boy:':'cupidboy',':girl:':'cupidgirl',':medved:':'medved',
':bayan:':'bayan',':kk:':'kak_kino',':-|':'icon_neutral',':search:':'use_search'}

zam = {'[b]':'<span class="post-b">', '[/b]':'</span>',
    '[i]':'<span class="post-i">', '[/i]':'</span>',
    '[u]':'<span class="post-u">', '[/u]':'</span>',
    '[s]':'<span class="post-s">', '[/s]':'</span>',
    '[list]':'<ol class="post-ul">','[list=1]':'<ol class="post-ul">', '[/list]':'</ol>',
    '[*]':'</span></li><li><span class="post-font-serif1">',
    '[hr]':'<hr>',
    '[br]':'<span class="post-br"></span>'}

tags=[('[b]','[/b]'),('[i]','[/i]'),('[u]','[/u]'),('[s]','[/s]'),('[list]','[/list]'),
      ('[size','[/size]'),('[img','[/img]'),('[color','[/color]'),('[font','[/font]'),
      ('[pre','[/pre]'),('[code','[/code]'),('[url','[/utl]'),('[spoiler','[/spoiler]'),
      ('[quote','[/quote]'),('[align','[/align]')]

def smiles(bbc=''):
    for key in sm.keys():
        if bbc.find(key):
            bbc=bbc.replace(key,smile_start + sm[key] + smile_end)
    return bbc

def zams(bbc=''):
    for key in zam.keys():
        bbc=bbc.replace(key,zam[key])
    return bbc

def zamena(tag,header,ender,intext='',n=0):
    patt=r'(\[%s.*?\])(.*?)(\[/%s\])' % (tag,tag)
    fa=[]
    fa=re.findall(patt,intext,flags=26)
    for i in fa:
        pozs=i[0].find('=')
        poze=i[0].find(']')
        if pozs != -1:
            par=i[0][pozs+1:poze]
            par=par.replace('"','')
        else:
            par=''

        if tag == 'QUOTE' and par == '': par='Цитата:'
                
        original= i[0]+i[1]+i[2]
        body=i[1]
        val=test_tag(body,tag)
        if tag == 'IMG':
            intext=intext.replace(original,(header % (par,val[0]))+ender+val[1])
        elif tag == 'PRE':
            val1=val[0].replace('<br />\n','\n')
            intext=intext.replace(original,(header % (par,))+val1+ender+val[1])
        elif tag == 'BOX':
            par1=par.split(',')[0]
            try:
                par2=par.split(',')[1]
            except:
                par2=''
            intext=intext.replace(original,(header % (par1,par2))+i[1]+ender)
        else:
            intext=intext.replace(original,(header % (par,))+val[0]+ender+val[1])
    return intext   

def zamena_1(tag,header,intext=''):
    patt=r'\[%s.*?\]' % (tag)
    fa=[]
    fa=re.findall(patt,intext,flags=26)
    for i in fa:
        pozs=i.find('=')
        poze=i.find(']')
        if pozs != -1:
            par=i[pozs+1:poze]
            par=par.replace('"','')
        else:
            par=''
        intext=intext.replace(i,(header % (par,)))
        intext=intext.replace('[/%s]' % tag.lower(),'</span>')
    return intext

def zam_sp(intext,n):
    
    patt=r'(\[SPOILER.*?\])(.*?)(\[/SPOILER\])'
    header='''<div class="sp-wrap"><div class="sp-head folded"><a href="#" onclick="showBlock('%s'); return false"><span class="sp-w">%s</span></a></div><div class="sp-body" id="%s" style="display: none;">'''
    ender='</div></div>'
    
    obj=re.search(patt,intext,flags=26)
    if obj:
        start= obj.span()[0]
        stop= obj.span()[1]
        fraza=intext[start:stop]
        if fraza.count('[spoiler')>1:
            start=fraza.rfind('[spoiler')
            fraza=fraza[start:]
        fa=re.findall(patt,fraza,flags=26)
        for i in fa:
            pozs=i[0].find('=')
            poze=i[0].find(']')
            if pozs != -1:
                par=i[0][pozs+1:poze]
                par=par.replace('"','')
            else:
                par='Скрытый текст:'
            cat="cat"+str(n)
            val=i[1]
            test_tag(val,'SPOILER')
            intext=intext.replace(fraza,(header % (cat,par,cat))+val+ender)
        return intext

def zam_html(intext):
    patt=r'[^]="](https?://[a-z0-9.\-](?:[^\s()<>]+|\([^\s()<>]+\))+(?:\([^\s()<>]+\)|[^\s`!()\[\]{};:\'".,<>?]))'
    repl='<a href="%s">%s</a>'
    
    urls=re.findall(patt,intext)
    for url in urls:
        intext=intext.replace(url,repl % (url,url))
    return intext
    
def test_tag(text,uptag):
    for tag in tags:
        count_start=text.count(tag[0])
        count_stop=text.count(tag[1])
        if count_start>count_stop:
            pos=text.rfind(tag[0])
            #print(pos)
            #print(uptag,starttag+':\t'+str(count_start)+'\t'+str(count_stop))
            ret = [text[:pos],text[pos:]]
            break
        else:
            ret = [text,'']
    return ret

def bbcode2html(intext):
    Dictag={'IMG':('<img align="%s" alt="" src="%s','">'),
            'SIZE':('<span style="font-size: %spx; line-height: normal;">','</span>'),
            'ALIGN':('<span class="post-align" style="text-align: %s;">','</span>'),
            'URL':('<a href="%s">', '</a>'),
            'FONT':('<span style="font-family: %s;">', '</span>'),
            'COLOR':('<span class="p-color" style="color: %s;">', '</span>'),
            'PRE':('<pre class="post-pre"%s>', '</pre>'),
            'CODE':('''<div class="c-wrap"><div class="c-head"><b>Код %s:</b></div><div class="c-body">''','</div></div>'),
            'QUOTE':('<div class="q-wrap"><div class="q-head"><span><b>%s</b></span></div><div class="q">','</div></div>'),
            'QPOST':('', ''),
            'BOX':('<div class="post-box" style="border-color: %s; background: %s;">','</div>')}

    intext=intext.replace('\n','<br />\n')
    intext=zams(intext)
    
    for key in Dictag:
        intext=zamena(key,Dictag.get(key)[0],Dictag.get(key)[1],intext)
    for key in Dictag:
        if key in ['SIZE','FONT','COLOR']:
            intext=zamena_1(key,Dictag.get(key)[0],intext)
    n=0
    intext+='[/spoiler]'
    while re.search(r'\[SPOILER',intext,flags=26):
        intext=zam_sp(intext,n)
        n+=1
    intext=re.sub(r'\[/spoiler\]','',intext,flags=26)    

    intext=smiles(intext)
    intext=intext.replace('''href="tracker.php''','''href="http://rutracker.org/forum/tracker.php''')
    intext=intext.replace('''href="viewtopic.php?t''','''href="http://rutracker.org/forum/viewtopic.php?t''')
    intext=intext.replace('[img]','')
    intext=zam_html(intext)
    intext=intext.replace('''href="http://rutracker.org/forum/viewtopic.php?t''','''href="info.py?tid''')
    intext=intext.replace('[hr]','<hr>')
    intext=intext.replace('[/align]','</span>')
    intext=intext.replace('[/quote]','</div>')
    intext=intext.replace('[/color]','</span>')
    intext=intext.replace('[align=center]','<span class="post-align" style="text-align: center">')
    intext=intext.replace('[/size]','</span>')
    
    #intext=intext.replace('</SIZE>','</span>')
    intext=intext.replace('[/font]','</span>')
    #intext=intext.replace('</COLOR>','</span>')
    
    
    return intext


if __name__ == '__main__':
    bbcode2html(content)

