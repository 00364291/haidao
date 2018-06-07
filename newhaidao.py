#!/usr/bin/env python  

# -*- coding: utf-8 -*-  

""" 

__author__ = 'zhaokaihui' 

"""  

import requests

import datetime

from time import time

from time import sleep

import os

import platform

import zipfile

import json

from collections import OrderedDict

from hashlib import md5

from requests.packages.urllib3.exceptions import InsecureRequestWarning 

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import random

from requests.adapters import HTTPAdapter

from common_haidao import common_haidao

from common_haidao import sendmsg

from common_haidao import loadoffline

from common_haidao import offlineuid

import threading

import csv

def savecsv(data):

    header=['ID','等级','总金钱','能量','护盾','海豚蛋','唤醒石','炮弹','jigsaw','jewels']

    fname='playinfos.csv'

    with open(fname,'w') as f:

        f_csv = csv.writer(f)

        f_csv.writerow(header)

        f_csv.writerows(data)

        f.close()

class haidao(common_haidao):

    # https://pirate-api.hortor002.com/game/friend/login-reward

    #登录奖励uid

    def __init__(self,secret,userId=None,uid=None,encryptedCode=None,friendCode=None):

        self.ua='MicroMessenger/6.6.6.1300(0x26060636) NetType/WIFI Language/zh_CN'

        self.uid=uid#

        self.secret = secret

        self.userId=userId

        self.name=''

        self.money=0

        self.shields=0

        self.maxEnergy=0

        self.energy=1

        self.island=9

        self.buildings=[]

        self.buildingCost=[]

        self.rollmoney=0

        self.stealIslands=[]

        self.killTitanCannonBall=0

        self.summonStone=0

        self.crowns=0

        self.tuhao=0

        self.puffer=0

        self.friendlist=[]

        self.jigsawInfo = []

        self.Jewels = []

        self.encryptedCode=encryptedCode

        self.friendCode=friendCode

        self.result = ['金钱', '金钱', '攻击', '金钱', '护盾', '金钱', '金钱', '能量', '金钱', '偷取']

        self.headers = {

            'User-Agent': self.ua,

            'referer': 'https://servicewechat.com/wxec8f800476c3964a/29/page-frame.html'

        }

        self.s = requests.session()

        

        self.s.mount('http://', HTTPAdapter(max_retries=4))

        self.s.mount('https://', HTTPAdapter(max_retries=4))

        self.proxies = {

                "http": "http://z00364291:WICD**963@proxy.huawei.com:8080/",

                "https": "http://z00364291:WICD**963@proxy.huawei.com:8080/",

            }

        self.proxies=None

        if userId!=None:

            self.login()

        self.basic()

    def login(self):

        url='https://pirate-api.hortor002.com/game/entry/wxgame'

        data = self.get_signed_data({

                'encryptedCode': self.encryptedCode,

                'friendCode':self.friendCode,

                'shareType':'WX_default',

            })

        #print(data)

        r=self.s.post(url,data=data,headers=self.headers,proxies=self.proxies, verify=False).json()

        #print(r)

        if r['errcode']==0:

            self.secret=r['data']['secret']

        else:

            print(r)

            return False

        url='https://pirate-api.hortor002.com/game/basic/login'

        data = self.get_signed_data({

                'userId': self.userId,

                

            })

            

        #print(data)

        r=self.s.post(url,data=data,headers=self.headers,proxies=self.proxies, verify=False).json()

        #print(r)

        if r['errcode']==0:

            self.secret=r['data']['secret']

        else:

            print(r)

            return False

            

        #self.buildingCost=r['data']['buildingCost']

        self.secret=r['data']['secret']

        self.uid=r['data']['uid']

        self.stealIslands=r['data']['stealIslands']

        #print(self.secret)

        #print(self.uid)

        return r['errcode']

    def basic(self):

        url='https://pirate-api.hortor002.com/game/basic/player'

        data=self.get_signed_data({

        'uid': self.uid,

        

        })

        #print(data)

        r=self.s.post(url,data=data,headers=self.headers,proxies=self.proxies, verify=False).json()

        #print(r)

        self.shields=r['data']['shields']

        self.energy=r['data']['energy']

        self.money=r['data']['money']

        self.maxEnergy=r['data']['maxEnergy']

        self.island=r['data']['island']

        self.buildings=r['data']['buildings']

        self.name=r['data']['name']

        #self.stealIslands=r['data']['stealIslands']

        self.crowns=r['data']['crowns']

        self.summonStone = r['data']['summonStone']

        self.killTitanCannonBall = r['data']['killTitanCannonBall']

        self.puffer = r['data']['puffer']

        self.tuhao = r['data']['stealTarget']['crowns']

        #print('kong')

        #self.loadoffline()

        #print(self.offlineid)

        print('名字,{7}等级{0}，总金钱：{1}，能量：{2}，护盾：{3}，海豚蛋:{4},唤醒石{5}，炮弹{6}'.format(

            self.crowns,self.money,self.energy,self.shields,self.puffer,self.summonStone,self.killTitanCannonBall,self.name))

        

        #print(r)

    def getfriend(self):

        print('获得好友列表')

        url = 'https://pirate-api.hortor002.com/game/friend/show-donate'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        # print(data)

        r = self.s.get(url, params=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        self.friendlist = r['data']['friends']

        sysstr = platform.system()

        if (sysstr == "Windows"):

            fp = open(r'friendlist.txt', 'w+', encoding='utf-8')

        elif (sysstr == "Linux"):

            fp = open(r'/home/task/checkin/friendlist.txt', 'w+', encoding='utf-8')

        self.friendlist.sort(key=lambda k: (k.get('updateElapse', 0)))

        ownername='id:{0},姓名:{1}\r\n'.format(self.uid,self.name)

        fp.write(ownername)

        for f in self.friendlist:

           info='好友id:{0},名称:{1}，等级:{2},离线时间:{3}天\r\n'.format(f['uid'],f['name'],f['crowns'],round(f['updateElapse']/60/60/24,2))

           fp.write(info)

        #print('好友id{0},名称{1}，等级{2},离线时间:{3}小时'.format(f['uid'],f['name'],f['crowns'],f['updateElapse']/60/60))

        fp.close()

    def treasureMaphelp(self,fid,bid):

        print('帮助')

        url = 'https://pirate-api.hortor002.com/game/treasureMap/help'

        thelp=False

        for bid in range(0,3):

            data = self.get_signed_data({

                'uid': self.uid,

                'fid': fid,

                'bid': bid

            })

            print(data)

            r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

            print(r)

            if r['errcode'] == 0:

                thelp=True

            elif r['errcode'] == 20174:

                thelp = True

            else:

                thelp = False

        return thelp

def patchrun(uidlist,mode,t):

    index=0

    for uid in uidlist:

        print('线程:{0},UID:{1}'.format(t,index))

        roll=haidao(secret, None, uid)

        

        roll.autoplay(mode)

        

        index+=1

    

def loadplayers():

    testFile=r'player.json'

    with open(testFile, 'r') as f:

    

       players = json.load(f)

       return players

def apprun(index,mode):

    #,188666027,222057521

    #'1zhao','2xh',

    playerlist=[257187920,188270670,270285531,253356959,189307805,184223883,156535685,170359243,161776059,160125279,198460035,194579081,195093379,164085030,]

    #playername=['0xh','1xm','2物是人非','3幻听物友','4百褶','5心如荒岛','6发福的瘦子','7磨刀发友','8鹏鹏哥','9疯狂逃跑冲','10蜀人蜀事','11real','临时']

    playername=[]

    players=loadplayers()

    for key in players:

        playername.append(key['username'])

    print(playername)

        

    #index=2

        #index=input(playername)

    

    if index=='':

        index='0'

    index=int(index)

    #print(playername[index])

    secret = '418785a803d8e0d9'

    uid=players[index]['uid']

    userid=players[index]['userid']

    encryptedCode=players[index]['encryptedCode']

    friendCode=players[index]['friendCode']

    modelist=['0自动','1保护','2批跑','3批查询','4章鱼',

              '5抢章鱼','6恶魔','7每日奖励','8猜土豪','9PVP','10下一座','11修复','12基本信息','13一键送能量，开宝箱','14新手奖励','15加好友','16助威','17送碎片','18送首饰','19查询好友']

    #mode=input(modelist)

    if mode=='':

        mode=0

    mode=int(mode)

    print(modelist[mode])

    if mode ==12:

        myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

        myroll.moreinfo()

if __name__ == "__main__":

    playername=[]

    players=loadplayers()

    for key in players:

        playername.append(key['username'])

    print(playername)

        

    index=2

    while index!='q':

        index=input(playername)

    

        if index=='':

            index='0'

        index=int(index)

        #print(playername[index])

        secret = '418785a803d8e0d9'

        

        uid=players[index]['uid']

        userid=players[index]['userid']

        encryptedCode=players[index]['encryptedCode']

        friendCode=players[index]['friendCode']

        

            

        modelist=['0自动','1保护','2批跑','3批查询','4章鱼',

                  '5抢章鱼','6恶魔','7每日奖励','8猜土豪','9PVP','10下一座','11修复','12基本信息','13一键送能量，开宝箱','14新手奖励','15加好友','16助威','17送碎片','18送首饰','19查询好友']

        modelist = ['0自动', '1保护', '2章鱼', '3恶魔','4猜土豪','5助威', '6送能量，开宝箱',

                    '7抢章鱼', '8每日奖励',  '9PVP', '10下一座', '11修复', '12基本信息', '13新手奖励', '14加好友',

                     '15送碎片', '16送首饰', '17查询好友']

        mode=input(modelist)

        if mode=='':

            mode=0

        mode=int(mode)

        print(modelist[mode])

        if mode in (0,1):

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            myroll.autoplay(mode)

        elif mode==2:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            myroll.octopus()

        elif mode==3:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            HP = 0

            tid = None

            

            

            print('打谁的怪兽')

            indexother = int(input(playername))

            if myroll.killTitanCannonBall==30:

                myroll.watchvideo()

            if indexother==index:

                print('打自己怪兽')

                if myroll.summonStone!=0:

                    tid, HP = myroll.openselftitan()

                    print(tid)

                    print('唤醒不为0')

                if tid==None or tid==0:

                    myroll0 = haidao(secret, None, playerlist[0])

                    tid,HP=myroll0.gettitanid(players[int(indexother)]['uid'])

                    

            else:

                tid,HP=myroll.gettitanid(players[int(indexother)]['uid'])

            print(tid)

            if tid==0 or tid==None:

                print('唤醒失败，未找到tid')

            else:

                myroll.attack(tid, 42)

        elif mode==4:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            myroll.steal(myroll.stealIslands)

        elif mode==5:

            print('给谁助威')

            index = int(input(playername))

            for player in players:

                uid = player['uid']

                if uid == 188270670 or uid == players[index]['uid']:

                    continue

                userid = player['userid']

                encryptedCode = player['encryptedCode']

                friendCode = player['friendCode']

                myroll = haidao(secret, userid, uid, encryptedCode, friendCode)

                sleep(1)

                myroll.treasureMaphelp(players[index]['uid'],2)

        elif mode==6:

            print('送能量选择送给谁')

            index = int(input(playername))

            for player in players:

                uid = player['uid']

                if uid == 188270670 or uid == players[index]['uid']:

                    continue

                userid = player['userid']

                encryptedCode = player['encryptedCode']

                friendCode = player['friendCode']

                myroll = haidao(secret, userid, uid, encryptedCode, friendCode)

                sleep(4)

                myroll.dailyenergy(players[index]['uid'])

            i = 1

            for player in players:

                uid = player['uid']

                if uid == 188270670 or uid == players[index]['uid']:

                    continue

                userid = player['userid']

                encryptedCode = player['encryptedCode']

                friendCode = player['friendCode']

                myroll = haidao(secret, userid, uid, encryptedCode, friendCode)

                sleep(4)

                if myroll.openbox(players[index]['uid'], i) == True:

                    break

                i = i + 1

        elif mode == 8:

            # 174164289,

            myroll = haidao(secret, userid, uid, encryptedCode, friendCode)

            myroll.getreward()

        elif mode==7:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            myroll.otheroctopus()

        elif mode==9:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            myroll.pvp()

        elif mode==10:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            myroll.nextisland()

        elif mode==11:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            myroll.repair()

        elif mode==12:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            myroll.moreinfo()

        elif mode==13:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            myroll.achivereward()

        elif mode==14:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            otherindex=0

            otherindex=int(input('加谁的好友，0zkh，1xm'))

            myroll.addfriend(otherindex)

        elif mode==15:

            #myroll.basic()

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            print('选择送给谁')

            index = int(input(playername))

            print(myroll.jigsawInfo)

            selected=1

            selected=int(input('几号碎片?'))

            if index == 0:

               myroll.sendjigsaw(playerlist[int(index)],selected)

        elif mode==16:

            #myroll.basic()

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            print('选择送给谁')

            index = int(input(playername))

            print(myroll.Jewels)

            selected=1

            selected=int(input('几号碎片?'))

            if index == 0:

               myroll.sendJewels(playerlist[int(index)],selected)

        elif mode==17:

            myroll = haidao(secret, userid, uid,encryptedCode,friendCode)

            myroll.getfriend()

        elif mode==222:

            loadoffline()

            step=len(offlineuid)//7

            print(step)

            print(offlineuid)

            threads = []

            for t in range(1,11):

                print('t{0},range{1}-{2}\n'.format(t,(t-1)*step,t*step))

                t1 = threading.Thread(target=patchrun,args=(offlineuid[(t-1)*step:t*step],mode,t))

                threads.append(t1)

            for t in threads:

                t.setDaemon(True)

                t.start()

            t.join()

        elif mode==22:

            loadoffline()

            for uid in offlineuid:

                print(uid)

                myroll = haidao(secret, None, uid)

                myroll.autoplay(mode)

        elif mode == 33:

            haidaozhuang = ['1酒杯', '2钩子', '3望远镜', '4短刀', '5火枪', '6海盗帽']

            types = 0

            types = int(input('查找什么0碎片，1首饰'))

            if types == 1:

                print(haidaozhuang)

            idx = 0

            idx = int(input('查找哪一个'))

            rows = []

            row = []

            loadoffline()

            if types == 0:

                for uid in offlineuid:

                    print(uid)

                    myroll = haidao(secret, None, uid)

                    myroll.moreinfo()

                    row = [myroll.uid, myroll.crowns, myroll.money, myroll.energy, myroll.shields, myroll.puffer,

                           myroll.summonStone, myroll.killTitanCannonBall, myroll.jigsawInfo, myroll.Jewels]

                    rows.append(row)

                    if len(myroll.jigsawInfo) != 0:

                        if myroll.jigsawInfo[idx - 1] != 0:

                            print('找到一个{0}号碎片,名称：{1},uid{2}'.format(idx, myroll.name, myroll.uid))

                            break

            else:

                for uid in offlineuid:

                    print(uid)

                    myroll = haidao(secret, None, uid)

                    myroll.moreinfo()

                    row = [myroll.uid, myroll.crowns, myroll.money, myroll.energy, myroll.shields, myroll.puffer,

                           myroll.summonStone, myroll.killTitanCannonBall, myroll.jigsawInfo, myroll.Jewels]

                    rows.append(row)

                    if len(myroll.Jewels) != 0:

                        if myroll.Jewels[idx] != 0:

                            print('找到一个{0},名称：{1},uid{2}'.format(haidaozhuang[idx - 1], myroll.name, myroll.uid))

                            break

            savecsv(rows)
