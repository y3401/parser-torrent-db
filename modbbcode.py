#

import re,webbrowser

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
':pop:':'ppl_pop',':prist:': 'ppl_priest',':punk:':'ppl_punk',
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
    '[i]':'<i>', '[/i]':'</i>',
    '[u]':'<u>', '[/u]':'</u>',
    '[s]':'<span class="post-s">', '[/s]':'</span>',
    '[list]':'<ol class="post-ul">', '[/list]':'</ol>',
    '[*]':'</span></li><li><span class="post-font-serif1">',
    '[hr]':'<hr>',
    '[br]':'<span class="post-br"></span>'}

html_header = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru" dir="ltr">
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
<link rel="stylesheet" type="text/css" href="style.css" />
<head><title>Инфо о раздаче</title></head><body>
<script language="JavaScript" type="text/javascript">
     function showBlock(t) {
           var elStyle = document.getElementById( t ).style;
           elStyle.display = (elStyle.display == 'none') ? '' : 'none';}
</script>
<div class="post_body">
"""
html_end='</div><br /><br /></body></html>'

tags=[('[b]','[/b]'),('[i]','[/i]'),('[u]','[/u]'),('[s]','[/s]'),('[list]','[/list]'),
      ('[size','[/size]'),('[img','[/img]'),('[color','[/color]'),('[font','[/font]'),
      ('[pre','[/pre]'),('[code','[/code]'),('[url','[/utl]'),('[spoiler','[/spoiler]'),
      ('[quote','[/quote]'),('[align','[/align]')]


content="""
[size=24][align=center][b]US Open 2016. 3-й круг
Daniel EVANS GBR - Stan WAWRINKA SUI [3][/b][/align][/size]

[img=right]http://i82.fastpic.ru/big/2016/0830/b8/198d61f8212dd812c7482b84e53ae1b8.png[/img]

[b]Дата эфира[/b]: 03.09.2016
[b]Вид спорта[/b]: Теннис
[b]Комментарий[/b]: Профессиональный
[b]Язык комментариев[/b]: Русский / Английский
[hr]
[b]Описание[/b]: US Open 2016. Матч третьего круга женского одиночного разряда Даниэль Эванс (Великобритания) - Стэн Вавринка (Швейцария).

[b][size=16]Согласно Re Do, на записи есть ошибки. Но не много.[/size][/b]
[hr]
[b]Автор рипа[/b]: [i]sanchez2011[/i]

[b]Качество[/b]: SATRemux
[b]Формат[/b]: TS
[b]Видео кодек[/b]: H.264
[b]Аудио кодек[/b]: MP2
[b]Видео[/b]: MPEG4 Video (H264) 720x576 (16:9) 25fps 2511kbps
[b]Аудио 1[/b]: MPEG Audio 48000Hz stereo 128kbps [i](Русский)[/i]
[b]Аудио 2[/b]: MPEG Audio 48000Hz stereo 96kbps [i](Английский)[/i]

[spoiler="Скриншоты"][align=center]
[URL=http://fastpic.ru/view/83/2016/0904/2b04de8b5d57619a3b42419d9b9e63d9.png.html][IMG]http://i83.fastpic.ru/thumb/2016/0904/d9/2b04de8b5d57619a3b42419d9b9e63d9.jpeg[/IMG][/URL] [URL=http://fastpic.ru/view/82/2016/0904/7a9113ce7e06f703c54e9a866ca76865.png.html][IMG]http://i82.fastpic.ru/thumb/2016/0904/65/7a9113ce7e06f703c54e9a866ca76865.jpeg[/IMG][/URL] [URL=http://fastpic.ru/view/78/2016/0904/ecfc3d6beb9c00c316eedc6af80d598e.png.html][IMG]http://i78.fastpic.ru/thumb/2016/0904/8e/ecfc3d6beb9c00c316eedc6af80d598e.jpeg[/IMG][/URL] [URL=http://fastpic.ru/view/85/2016/0904/92299c90c3cf91835c7b550f0cd1e4e0.png.html][IMG]http://i85.fastpic.ru/thumb/2016/0904/e0/92299c90c3cf91835c7b550f0cd1e4e0.jpeg[/IMG][/URL] [URL=http://fastpic.ru/view/78/2016/0904/aa1c98df30c544958b1432d574d2a4cb.png.html][IMG]http://i78.fastpic.ru/thumb/2016/0904/cb/aa1c98df30c544958b1432d574d2a4cb.jpeg[/IMG][/URL]
[/align][/spoiler]

[spoiler="Media Info"][pre]
General
ID                                       : 1 (0x1)
Complete name                            : W:\раздачи\\US Open 16. MS R3 Daniel EVANS GBR - San WAWRINKA SUI. Rutracker.org.ts
Format                                   : MPEG-TS
File size                                : 4.86 GiB
Duration                                 : 4h 1mn
Overall bit rate mode                    : Variable
Overall bit rate                         : 2 880 Kbps

Video
ID                                       : 206 (0xCE)
Menu ID                                  : 706 (0x2C2)
Format                                   : AVC
Format/Info                              : Advanced Video Codec
Format profile                           : High@L3
Format settings, CABAC                   : Yes
Format settings, ReFrames                : 4 frames
Format settings, GOP                     : M=4, N=28
Codec ID                                 : 27
Duration                                 : 4h 1mn
Bit rate                                 : 2 511 Kbps
Width                                    : 720 pixels
Height                                   : 576 pixels
Display aspect ratio                     : 16:9
Frame rate                               : 25.000 fps
Standard                                 : PAL
Color space                              : YUV
Chroma subsampling                       : 4:2:0
Bit depth                                : 8 bits
Scan type                                : Interlaced
Scan type, store method                  : Separated fields
Scan order                               : Top Field First
Bits/(Pixel*Frame)                       : 0.242
Stream size                              : 4.24 GiB (87%)
Color range                              : Limited
Color primaries                          : BT.601 PAL
Transfer characteristics                 : BT.470 System B, BT.470 System G
Matrix coefficients                      : BT.601

Audio #1
ID                                       : 306 (0x132)
Menu ID                                  : 706 (0x2C2)
Format                                   : MPEG Audio




[/pre][/spoiler]

[spoiler="Продолжительность"][align=center]
04:01:32
[/align][/spoiler]

[spoiler="Счёт"][align=center]
Daniel EVANS GBR - [b]Stan WAWRINKA SUI [3][/b]
[b]6[/b]-4, 3-[b]6[/b], [b]7[/b]-6, 6-[b]7[/b], 2-[b]6[/b]
[/align][/spoiler]"""


def smiles(bbc=''):
    for key in sm.keys():
        if bbc.find(key):
            bbc=bbc.replace(key,smile_start + sm[key] + smile_end)
    return bbc

def zams(bbc=''):
    for key in zam.keys():
        if bbc.find(key):
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
        else:
            par=''

        if tag == 'QUOTE' and par == '': par='Цитата:'
                
        original= i[0]+i[1]+i[2]
        body=i[1]
        val=test_tag(body,tag)
        if tag == 'IMG':
            intext=intext.replace(original,(header % (par,val[0]))+ender+val[1])
        elif tag in ['PRE']:
            val1=val[0].replace('<br />\n','\n')
            intext=intext.replace(original,(header % (par,))+val1+ender+val[1])
        else:
            intext=intext.replace(original,(header % (par,))+val[0]+ender+val[1])
    return intext   

def zam_sp(intext,n):
    
    patt=r'(\[SPOILER.*?\])(.*?)(\[/SPOILER\])'
    header='''<div class="sp-wrap"><div class="sp-head folded">
    <a href="#" onclick="showBlock('%s'); return false"><span>%s</span>
    </a></div><div class="sp-body"; id="%s"; style="display:none;">'''
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
            #test_tag(val,'SPOILER')
            intext=intext.replace(fraza,(header % (cat,par,cat))+val+ender)
        return intext

def zam_html(intext):
    patt=r'[^]=">](https?://[a-z0-9.\-](?:[^\s()<>]+|\([^\s()<>]+\))+(?:\([^\s()<>]+\)|[^\s`!()\[\]{};:\'".,<>?]))'
    repl='<a href="%s">%s</a>'
    
    urls=re.findall(patt,intext)
    for url in urls:
        intext=intext.replace(url,repl % (url,url))
    return intext
    
def write_html(intext=''):
    f=open('info.htm','w',encoding='utf-8')
    f.write(intext)
    f.close
    webbrowser.open_new_tab('info.htm')

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
    Dictag={'IMG':('<img align="%s" src="%s','">'),
            'SIZE':('<span style="font-size: %spx; line-height: normal;">','</span>'),
            'ALIGN':('<span class="post-align" style="text-align: %s;">','</span>'),
            'URL':('<a href="%s">', '</a>'),
            'FONT':('<font="%s">', '</font>'),
            'COLOR':('<span class="p-color" style="color: %s;">', '</span>'),
            'PRE':('<pre class="post-pre"%s>', '</pre>'),
            'CODE':('''<div class="c-wrap"><div class="c-head"><b>Код %s:</b></div><div class="c-body">''','</div></div>'),
            'QUOTE':('<div class="q-wrap"><div class="q-head"><span><b>%s</b></span></div><div class="q">','</div></div>'),
            'QPOST':('', '')}

    intext=intext.replace('\n','<br />\n')
    intext=zams(intext)
    for key in Dictag:
        #print(key,Dictag.get(key)[0],Dictag.get(key)[1])
        intext=zamena(key,Dictag.get(key)[0],Dictag.get(key)[1],intext)
    n=0
    while re.search(r'\[spoiler',intext,26):
        intext=zam_sp(intext,n)
        n+=1

    intext=smiles(intext)
    intext=zam_html(intext)

    write_html(html_header+intext+html_end)


if __name__ == '__main__':
    bbcode2html(content)

"""
Надо сделать:

    ошибка из-за обратных слешей. их надо экранировать
    в sel_content вставить запрос на заголовки и хэш для передачи в bbcode2html
 <[^>]+> - html tag

"""
