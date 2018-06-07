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

import zipfile

import json

from collections import OrderedDict

from hashlib import md5

from requests.packages.urllib3.exceptions import InsecureRequestWarning 

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import random

import platform

offlineuid = []

class common_haidao():

    def __init__(self,secret,userId=None,uid=None):

        pass

    def login(self):

        url='https://pirate-api.hortor002.com/game/basic/login'

        data={

        'secret': self.secret,

        'userId': self.userId,

        'isWxGame': 'true',

        't': int(time()),

        }

        data['sign'] = md5(''.join([

                    '{0}={1}'.format(index, value) for index, value in OrderedDict(sorted(data.items())).items()

                ]).encode()).hexdigest()

        #print(data)

        r=self.s.post(url,data=data,headers=self.headers,proxies=self.proxies, verify=False).json()

        #print(r)

        #self.buildingCost=r['data']['buildingCost']

        self.secret=r['data']['secret']

        self.uid=r['data']['uid']

        self.stealIslands=r['data']['stealIslands']

        #print(self.secret)

        #print(self.uid)

        return r['errcode']

    def get_signed_data(self,data):

        data['secret'] = self.secret

        data['isWxGame'] = 'true'

        data['t'] = int(time())

        data['sign'] = md5(''.join([

            '{0}={1}'.format(index, value) for index, value in OrderedDict(sorted(data.items())).items()

        ]).encode()).hexdigest()

        del data['secret']

        return data

    def achivereward(self):

        print('新手奖励')

        url='https://pirate-api.hortor002.com/game/achievement/reward'

        for idx in range(1,5):

            data = self.get_signed_data({

                'uid': self.uid,

                'idx': idx,

            })

            #print(data)

            r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

            print(r)

        print('新手奖励')

        url = 'https://pirate-api.hortor002.com/game/achievement/next'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        #print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

    def cheer(self,fid):

        url='https://pirate-api.hortor002.com/game/beach/cheer'

        data = self.get_signed_data({

            'uid': self.uid,

            'fid': fid,

            'tid': fid

        })

        print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

        if r['errcode'] == 0:

            return r['errcode']

        else:

            return True

    def dailyenergy(self, fid):

        url = 'https://pirate-api.hortor002.com/game/dayShare/playerEnter'

        data = self.get_signed_data({

            'uid': self.uid,

            'fid': fid,

        })

        print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

    def openbox(self, fid, idx):

        url = 'https://pirate-api.hortor002.com/game/octopus/treasure-open'

        data = self.get_signed_data({

            'uid': self.uid,

            'fid': fid,

            'idx': idx

        })

        print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

        if r['errcode'] == 0:

            return r['data']['hasOpen']

        else:

            return True

    def getreward(self):

        print('送体力')

        url = 'https://pirate-api.hortor002.com/game/friend/donate'

        data = self.get_signed_data({

            'uid': self.uid,

            'fid': 0,

        })

        print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

        print('登录奖励')

        url = 'https://pirate-api.hortor002.com/game/friend/daily-reward'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        #print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

        '''

        print('VIP能量奖励')

        url='https://pirate-api.hortor002.com/game/friend/monthcard-reward'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

        '''

        print('收金币')

        url = 'https://pirate-api.hortor002.com/game/island/collect'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        #print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

        print('怪兽奖励')

        url = 'https://pirate-api.hortor002.com/game/killtitan/gain-award'

        data = self.get_signed_data({

            'uid': self.uid,

            'awardId': 0

        })

        #print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

        print('每日能量')

        url = 'https://pirate-api.hortor002.com/game/friend/login-reward'

        data = self.get_signed_data({

            'uid': self.uid,

            'awardId': 0

        })

        #print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

    def sharereward(self):

        url='https://pirate-api.hortor002.com/game/friend/share-coin-reward'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

    def watchvideo(self):

        url = 'https://pirate-api.hortor002.com/game/killtitan/share-reward'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        #print(data)

        for x in range(1,3):

            sleep(4)

            r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

            print(r)

    def steal(self,as_data):

        # 找出哪个是土豪，判断谁是土豪

        idx=2

        print('系统土豪:{0}'.format(self.tuhao))

        

        for index, item in enumerate(as_data):

            #print(item)

            if int(item['crowns'])==int(self.tuhao):

                idx=index

        url='https://pirate-api.hortor002.com/game/pvp/steal'

        data=self.get_signed_data({

        'uid': self.uid,

        'idx': idx

        })

        print(data)

        r=self.s.post(url,data=data,headers=self.headers,proxies=self.proxies, verify=False,timeout=6).json()

        print(r)

        

        #判断是否猜中土豪，如果没猜中，记录特征:crowns数量

        isRichMan=False

        for tuhao in r['data']['targets']:

            #print('tuhao=',tuhao)

            #as_tuhao=json.loads(tuhao)

            if tuhao['money']==r['data']['reward'] and tuhao['isRichMan']:

                print('猜中土豪，金币：{0},土豪是{1}'.format(r['data']['reward'],tuhao['crowns']))

                self.tuhao=0

                isRichMan=True

                break

            else:

                if tuhao['isRichMan']:

                    self.tuhao=tuhao['crowns']

        if isRichMan==False:        

            print('没有猜中土豪，金币：{0}'.format(r['data']['reward']))

    def pvp(self):

        #敌人列表

        url='https://pirate-api.hortor002.com/game/rank/vengeance'

        data=self.get_signed_data({

            'uid': self.uid,

        })

        res = self.s.get(url, params=data,headers=self.headers,proxies=self.proxies, verify=False).json()

        #print(res)

        if len(res['data']['Enemies'])!=0:

            puid=res['data']['Enemies'][0]['uid']

            #puid=248925296

            sleep(5)

            #选中攻击某一个人

            url='https://pirate-api.hortor002.com/game/island/show'

            data=self.get_signed_data({

                'uid': self.uid,

                'fid': puid,

    

            })

            res = self.s.get(url, params=data,headers=self.headers,proxies=self.proxies, verify=False).json()

            #print(res)

        else:

            puid=0

        print('puid=',puid)

        

        # 攻击建筑

        #index=res['data']['buildings'][0]

        sleep(4)

        url='https://pirate-api.hortor002.com/game/pvp/attack'

        data=self.get_signed_data({

            'uid': self.uid,

            'puid': puid,

            'building':2

        })

        res = self.s.post(url, data=data,headers=self.headers,proxies=self.proxies, verify=False).json()

        print(res)

    def bulid(self):

        url = 'https://pirate-api.hortor002.com/game/island/build'

        # print(self.buildings)

        # print(self.buildingCost)

        gainIslandReward = False

        for index, item in enumerate(self.buildings):

            level = int(item['level'])

            # print(self.money)

            # if level<5:

            #    print(self.buildingCost[index][level])

            #    print(self.buildingCost[index][level+1])

            if len(self.buildingCost) != 0:

                if item['status'] == 1:

                    print('需要修理')

                    self.repair()

                if level < 5 and self.money >= self.buildingCost[index][level] and item['status'] !=1:

                    print('建筑金钱{0},等级{1}'.format(self.buildingCost[index][level], level))

                    data = self.get_signed_data({

                        'uid': self.uid,

                        'island': self.island,

                        'building': index,

                        'level': level + 1

                    })

                    #print(data)

                    r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

                    #print(r)

                    if r['errcode'] == 0:

                        print('建造成功1')

                        self.buildingCost = r['data']['buildingCost']

                        self.buildings = r['data']['buildings']

                        self.money = r['data']['money']

                        gainIslandReward = r['data']['gainIslandReward']

                        # 如果建造完成，下一站

                        if gainIslandReward:

                            self.nextisland()

                            break

            else:

                if item['status'] == 1:

                    print('需要修理')

                    self.repair()

                if level < 5 and self.money > 3000000 and item['status'] !=1:

                    data = self.get_signed_data({

                        'uid': self.uid,

                        'island': self.island,

                        'building': index,

                        'level': level + 1

                    })

                    #print(data)

                    r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

                    #print(r)

                    if r['errcode'] == 0:

                        print('建造成功2')

                        self.buildingCost = r['data']['buildingCost']

                        self.buildings = r['data']['buildings']

                        self.money = r['data']['money']

                        gainIslandReward = r['data']['gainIslandReward']

                        # 如果建造完成，下一站

                        if gainIslandReward:

                            self.nextisland()

                            break

                            # return r['errcode']

    def repair(self):

        url = 'https://pirate-api.hortor002.com/game/island/repair'

        # print(self.buildings)

        # print(self.buildingCost)

        for index, item in enumerate(self.buildings):

            level = int(item['level'])

            # print(self.money)

            # if level<5:

            #    print(self.buildingCost[index][level])

            #    print(self.buildingCost[index][level+1])

            if len(self.buildingCost) != 0:

                if level < 5 and self.money >= self.buildingCost[index][level] and item['status']== 1:

                    print('建筑金钱{0},等级{1}'.format(self.buildingCost[index][level], level))

                    data = self.get_signed_data({

                        'uid': self.uid,

                        'island': self.island,

                        'building': index,

                        'level': level + 1

                    })

                    #print(data)

                    r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

                    print(r)

                    if r['errcode'] == 0:

                        print('修理成功1')

                        self.buildingCost = r['data']['buildingCost']

                        self.buildings = r['data']['buildings']

                        self.money = r['data']['money']

            else:

                if level < 5 and item['status']== 1 and self.money>2000000:

                    data = self.get_signed_data({

                        'uid': self.uid,

                        'island': self.island,

                        'building': index,

                        'level': level + 1

                    })

                    #print(data)

                    r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

                    #print(r)

                    if r['errcode'] == 0:

                        print('修理成功2')

                        self.buildingCost = r['data']['buildingCost']

                        self.buildings = r['data']['buildings']

                        self.money = r['data']['money']

                        # return r['errcode']

    def nextisland(self):

        url = 'https://pirate-api.hortor002.com/game/island/reward'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        #print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

        self.buildingCost = r['data']['buildingCost']

        self.island+=1

    def openselftitan(self):

        url = 'https://pirate-api.hortor002.com/game/killtitan/open-titan'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        print(data)

        print("唤醒")

        res = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(res)

        if res['errcode']==0:

            return res['data']['titan']['tid'],res['data']['titan']['remainHP']

        elif res['errcode']==20045:

            return 0,0

        else:

            return None,None

    def gettitanid(self,uid):

        url = 'https://pirate-api.hortor002.com/game/killtitan/list'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        print(data)

        print("获得列表")

        res = self.s.get(url, params=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(res)

        tid=None

        if res['errcode'] == 0:

            for item in res['data']['friendList']:

                if item['uid']==uid and item['remainTime']!=0 and item['remainHP']!=0:

                    return item['tid'],item['remainHP']

        return  tid,item['remainHP']

    def attack(self,tid,times):

        url = 'https://pirate-api.hortor002.com/game/killtitan/attack-titan'

        HP = 4500

        damage = 100

        for x in range(1,times+1):

            # tid怪兽的id

            if times>=5:

                if x%5==0:

                    damage=random.randint(75, 79)

                else:

                    damage=100

            else:

                if x%4==0:

                    damage=random.randint(75, 79)

                else:

                    damage=100

            if HP==0:

                break

            elif HP<100:

                damage=HP

            data = self.get_signed_data({

                'uid': self.uid,

                'tid': tid,

                'damage': damage,

                'buffing': 'false',

            })

            #print(data)

            sleep(5)

            print("攻击中")

            res = self.s.post(url, data=data,headers=self.headers,proxies=self.proxies, verify=False).json()

            cannonBallCount=0

            print(res)

            if res['errcode']==0:

                HP=res['data']['titan']['remainHP']

                cannonBallCount=res['data']['cannonBallCount']

            else:

                break

            if cannonBallCount==0:

                print('炮弹不足，退出')

                break

    def octopus(self):

        if self.puffer==0:

            return False

        url = 'https://pirate-api.hortor002.com/game/octopus/enter'

        data = self.get_signed_data({

            'uid': self.uid,

            'fid': self.uid,

        })

        print(data)

        res = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        url = 'https://pirate-api.hortor002.com/game/octopus/open'

        if res['data']['octopusInfo']['openingRemain'] == 0:

            for index, item in enumerate(res['data']['octopusInfo']['boxes']):

                if index == 0:

                    pass

                elif item != 0:

                    data = self.get_signed_data({

                        'uid': self.uid,

                        'fid': self.uid,

                        'idx': index,

                    })

                    print(data)

                    sleep(5)

                    res = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies,

                                      verify=False).json()

                    if res['errcode']==0:

                        

                        self.puffer=res['data']['puffer']

                        print(self.puffer)

                        if self.puffer==0:

                            break

                        

                    else:

                        print(res)

                        return False

                    print(res)

    def otheroctopus(self):

            #章鱼列表

            url='https://pirate-api.hortor002.com/game/octopus/list'

            excellent=[]

            chuanqi=[]

            data = self.get_signed_data({

                'uid': self.uid,

                

            })

            print(data)

            res = self.s.get(url, params=data, headers=self.headers, proxies=self.proxies, verify=False).json()

            for octopuslist in res['data']['friends']:

                if  octopuslist['openingRemain']==0:

                    boxnum=0

                    for index, item in enumerate(octopuslist['boxes']):

                        if index != 0 and item!=0:

                            boxnum+=1

                    if octopuslist['color']=='excellent' and boxnum+octopuslist['ownerGotGoods']>2:

                        excellent.append(octopuslist['uid'])

                    elif octopuslist['color']!='normal' and boxnum+octopuslist['ownerGotGoods']>2:

                        chuanqi.append(octopuslist['uid'])

            if len(chuanqi)==0:

                print('无传奇章鱼')

            else:

                print('传奇章鱼：')

                print(chuanqi)    

            if len(excellent)==0:

                print('无稀有章鱼')

            else:

                print('稀有章鱼：')

                print(excellent)  

            for fid in chuanqi:

                if self.puffer==0:

                    print('puffer不足')

                    break

                url = 'https://pirate-api.hortor002.com/game/octopus/enter'

                data = self.get_signed_data({

                    'uid': self.uid,

                    'fid': fid,

                })

                print(data)

                res = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

                url = 'https://pirate-api.hortor002.com/game/octopus/open'

                if res['data']['octopusInfo']['openingRemain'] == 0 and self.puffer > 0:

                    for index, item in enumerate(res['data']['octopusInfo']['boxes']):

                        if index == 0:

                            pass

                        elif item != 0:

                            data = self.get_signed_data({

                                'uid': self.uid,

                                'fid': fid,

                                'idx': index,

                            })

                            print(data)

                            sleep(5)

                            res = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies,

                                              verify=False).json()

                            #print(res)

                            self.puffer=res['data']['puffer']

                            if self.puffer == 0:

                                print('puffer不足')

                                break

            for fid in excellent:

                if self.puffer==0:

                    print('puffer不足')

                    break

                url = 'https://pirate-api.hortor002.com/game/octopus/enter'

                data = self.get_signed_data({

                    'uid': self.uid,

                    'fid': fid,

                })

                # print(data)

                res = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

                url = 'https://pirate-api.hortor002.com/game/octopus/open'

                if res['data']['octopusInfo']['openingRemain'] == 0 and self.puffer > 0:

                    for index, item in enumerate(res['data']['octopusInfo']['boxes']):

                        if index == 0:

                            pass

                        elif item != 0:

                            data = self.get_signed_data({

                                'uid': self.uid,

                                'fid': fid,

                                'idx': index,

                            })

                            print(data)

                            sleep(5)

                            res = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies,

                                              verify=False).json()

                            print(res)

                            self.puffer = res['data']['puffer']

                            if self.puffer == 0:

                                print('puffer不足')

                                break

    def roll(self):

        if self.energy == 0:

            return 20005, 0, None

        url = 'https://pirate-api.hortor002.com/game/roller/roll'

        # data={

        #    'uid': self.uid,

        #    'bet': '1',

        #    'isWxGame': 'true',

        # }

        data = self.get_signed_data({

            'uid': self.uid,

            'bet': '1'

        })

        print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False,timeout=6)

        as_json = r.json()

        print(as_json)

        # {'errcode': 20005, 'errmsg': '体力不足'}

        as_data = None

        shareCoinType = 'share'

        if 'data' in as_json:

            # 更新最新的能量，金钱，护盾

            # 金钱(0.1,3,5,6,8)(14,112,84,28,56)

            # 攻击=2，护盾=4，能量=7，偷取=9

            self.money = as_json['data']['money']

            self.energy = as_json['data']['energy']

            self.shields = as_json['data']['shields']

            self.rollmoney = as_json['data']['rollerItem']['value']

            shareCoinType = as_json['data']['shareCoinType']

            if shareCoinType == 'video':

                print('分享50倍奖励')

                self.sharereward()

            # return self.result[as_json['data']['rollerItem']['index']]

            if as_json['data']['rollerItem']['index'] == 2:

                as_data = as_json['data']['attackTarget']

            elif as_json['data']['rollerItem']['index'] == 9:

                as_data = as_json['data']['stealIslands']

            return as_json['errcode'], as_json['data']['rollerItem']['index'], as_data

        elif as_json['errcode'] == 20005:

            print(as_json)

            return as_json['errcode'], 0, as_data

        else:

            print(as_json)

            return as_json['errcode'], 0, as_data

    def autoplay(self, mode):

        # myroll = haidao(uid, t, sign)

        # tip = '请输入命令：q(退出),r(roll）,s(偷123）,a(攻击1234):'

        command = 'r'

        sendwx = True

        as_data = None

        #errcode = self.basic()

        while command != 'q' and self.energy > 0:

            if mode == 1 and self.shields >= 1 and self.money < 1500000:

                print('{3}:mode2,等待,金币：{0},能量{1},盾{2}'.format(self.money, self.energy, self.shields, self.name))

                sleep(5 * 60)

                errcode = self.basic()

            elif self.energy > 0:

                times = random.randint(5, 10)

                sleep(times)

                errcode, result, as_data = self.roll()

                print('{5}:结果:{0}{1},钱:{2},能量:{3},盾:{4}'.format(self.result[result], self.rollmoney, self.money,

                                                                self.energy,

                                                                self.shields, self.name))

                if errcode == 0:

                    if result == 9:

                        print('偷取中')

                        self.steal(as_data)

                    elif result == 2:

                        print('攻击中')

                        self.pvp()

                    if self.money > 2000000:

                        print('检测建筑升级！！')

                        self.bulid()

                elif errcode == 20005:

                    print('没有体力了')

                    self.bulid()

                    if self.shields == 0:

                        sendmsg('{0}没体力，没盾牌，等待15分钟后重试'.format(self.uid))

                    sleep(10 * 60)

                elif errcode == 40001:

                    print('命令错误，需要重新登录')

                    command = 'q'

                elif errcode == 20010:

                    self.pvp()

                    self.steal()

                    print('状态不正确')

                else:

                    print('未知错误')

                    command = 'q'

        print('能量不足')

    def moreinfo(self):

        print('查询拼图信息')

        url = 'https://pirate-api.hortor002.com/game/guide/activity'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        # print(data)

        r = self.s.get(url, params=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r'[1, 2, 3, 4, 5, 6, 7, 8, 9]')

        print(r['data']['jigsawInfo']['bags'])

        self.jigsawInfo = r['data']['jigsawInfo']['bags']

        # fp = open('d:\\friends.txt', 'a', encoding='utf-8')

        # ownername = 'id:{0},姓名:{1}\r\n'.format(self.uid, self.name)

        # fp.write(ownername)

        # fp.write('查询拼图信息\n')

        # fp.write(str(r['data']['jigsawInfo']['bags']))

        print('查询章鱼物品')

        url = 'https://pirate-api.hortor002.com/game/octopus/show'

        data = self.get_signed_data({

            'uid': self.uid,

        })

        # print(data)

        r = self.s.get(url, params=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        if r['errcode'] == 0:

            print(r['data']['octopusPlayer']['Jewels'])

            self.Jewels = r['data']['octopusPlayer']['Jewels']

            # fp.write('\n查询章鱼信息\n')

            # fp.write(str(r['data']['octopusPlayer']['Jewels']))

            # fp.close()

    def sendjigsaw(self,fid,idx):

        self.moreinfo()

        print(self.jigsawInfo)

        if self.jigsawInfo[idx-1]==0:

            print('没有{0}号碎片'.format(idx))

            print(self.jigsawInfo)

            return False

        url = 'https://pirate-api.hortor002.com/game/jigsaw/donate'

        password=random.randint(7154,7200)

        data = self.get_signed_data({

            'uid': self.uid,

            'fid': fid,

            'idx': idx,

            'password':7154

        })

        print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

        if r['errcode'] == 0:

            print('赠送成功，密码7154')

            return True

        else:

            return False

    def sendJewels(self,fid,idx):

        self.moreinfo()

        print(self.Jewels)

        if self.Jewels[idx] == 0:

            print('没有{0}号东西'.format(idx))

            print(self.Jewels)

            return False

        url = 'https://pirate-api.hortor002.com/game/octupos/donate'

        password = random.randint(7154, 7200)

        data = self.get_signed_data({

            'uid': self.uid,

            'fid': fid,

            'idx': idx,

            'password': 7154

        })

        print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

        if r['errcode'] == 0:

            print('7154')

            return True

        else:

            return False

    def addfriend(self,index):

        url='https://pirate-api.hortor002.com/game/friend/join'

        code=''

        if index==0:

            code='P1E3VU8'

        elif index==1:

            code = '6PVRVSC'

        #6PVRVSC

        #P1E3VU8

        data = self.get_signed_data({

            'uid': self.uid,

            'code':code,

            'message':'',

        })

        print(data)

        r = self.s.post(url, data=data, headers=self.headers, proxies=self.proxies, verify=False).json()

        print(r)

def sendmsg(msg):

    APIaddress = 'https://pushbear.ftqq.com/sub'

    timestamp = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    proxies = {

        "http": "http://z00364291:WICD**963@proxy.huawei.com:8080/",

        "https": "http://z00364291:WICD**963@proxy.huawei.com:8080/",

    }

    msgbody = {

        'sendkey': '2143-b713ccee5a17d67abfa932ca114b140e',

        'text': '海盗来了' + timestamp,

        'desp': msg,

    }

    r = requests.get(APIaddress, params=msgbody, verify=False)

def loadoffline():

    sysstr = platform.system()

    if (sysstr == "Windows"):

        fp = open(r'E:\Pysrc\checkin\offline.txt', 'r', encoding='utf-8')

    elif (sysstr == "Linux"):

        fp = open(r'/home/task/checkin/offline.txt', 'r', encoding='utf-8')

    line = None

    while line != '':

        line = fp.readline()

        #print(line)

        #print(line[0:9])

        if line[0:9].isnumeric():

            offlineuid.append(line[0:9])

    fp.close()

if __name__ == "__main__":

    loadoffline()

    print(offlineuid)

