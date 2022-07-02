import requests
import json
import time
import pyautogui
import random




class Wallet:
    def __init__(self,minmoney=0,playing=False) :
        self.predict = make_predict()
        self.minmoney = minmoney
        self.money = minmoney
        self.playing = playing
        self.true = 0
        self.false = 0
        self.falseChain = 0
        self.maxFalse = 0
        self.percent = 0
        self.history = []
    def check_predict(self,record):

        if self.predict == None:
            return
        print("Predict:{} in  Result:{}  is:{}".format(self.predict,record.betTypeResult,self.predict in record.betTypeResult))

        if self.predict in record.betTypeResult:
            self.true  +=1
            self.falseChain = 0
            # self.money -=10
            # self.money = max(self.money,self.minmoney) 
        else:
            self.false+=1 
            self.falseChain+=1
            self.maxFalse = max(self.maxFalse,self.falseChain)
            # self.money +=10
        # if self.true - self.false>=5:
        #     quit_game("Hoan thanh")

        self.history.append(self.true - self.false)
        self.percent = int(self.true*100/(self.true+self.false))
    def make_predict(self):
        self.predict = make_predict()
    def show(self):
        print("True:{} False:{}  P:{}%  /Fchain:{}".format(self.true,self.false,self.percent,self.maxFalse))
    def bets(self):
        global indexBIG,indexSMALL,indexVND10K,indexVND50K,indexVND100K
        #########################
        if self.playing == False:
            return

        numbervnd100,numbervnd50,numbervnd10 = calculate(self.money)


        if self.predict == "BIG":
            index = indexBIG
        elif self.predict == "SMALL":
            index = indexSMALL
        else:
            print("should not participate")
        moveclick_and_moveclicks(indexVND100K,index,numbervnd100)
        moveclick_and_moveclicks(indexVND50K,index,numbervnd50)
        moveclick_and_moveclicks(indexVND10K,index,numbervnd10)




#_________________________________________________________________

from manipulation import  *
from prophet import *
from getAPI import *
#_________________________________________________________________


try:
    minmoney = int(input("minmoney: "))
    WL = Wallet(minmoney,True)

    indexBIG = get_index("BIG")
    indexSMALL = get_index("SMALL")
    indexVND10K = get_index("VND10K")
    indexVND50K = get_index("VND50K")
    indexVND100K = get_index("VND100K")

    if None in [indexBIG,indexSMALL,indexVND10K,indexVND50K,indexVND100K]:
        quit_game("cai dai that bai")
except:
    WL = Wallet()
print(WL.predict)
WL.bets()

try:
    while 1:
        record = create_record()
        record.show()

        WL.check_predict(record)
        WL.show()
        check_resutl(record.betTypeResult)

        print("\n______________________________________________")
        while 1:
            if is_betting():
                a = time.time()

                WL.make_predict()
                print("{} x {}".format(WL.predict,WL.money))
                # print("\a")
                WL.bets()
                b = time.time()
                time.sleep(max(50-int(b-a),0))
                break


except:
    from draw import draw_result
    turn = [i for i in range(1,len(WL.history)+1)]
    draw_result(turn,WL.history)