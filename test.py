import requests
import json
import time
import pyautogui
import random



# def get_response():
#     return requests.get("https://api-csn-sun.gameland.vip/api/v1/round/ended?limit=150&page=1&tableId=103")



# def make_data(listt,lenrecord):
#     data = []
#     label = []
#     for i in range(len(listt)-lenrecord):
#         data.append(listt[i:i+lenrecord])
#         label.append(listt[i+lenrecord])
#     dt = listt[len(listt)-lenrecord:len(listt)]
#     return data,label,[dt]

# def make_predict(data,label,dt,random_state,max_depth):
#     # global tree
#     tree = DecisionTreeClassifier(criterion = "gini",random_state = random_state,max_depth=max_depth, min_samples_leaf=5)
#     tree.fit(data,label)
#     return tree.predict(dt)[0]



# def get_history_result():# return [10,14,5,7,16]
#     response = get_response()

#     history_list = response.json()["content"]
#     history = []
#     for i in range(len(history_list)-1,0,-1):
#         kq = history_list[i]["resultRaw"]
#         history.append(int(kq[0])+int(kq[2])+int(kq[4]))
#     return history


# def make_predict_2(random_state,lenrecord,max_depth):
#     history = get_history_result()
#     data,label,dt = make_data(history,lenrecord)
#     # predict = make_predict(data,label,dt,random_state,max_depth)
#     predict = prophet.predict_by_naive_bayes(data,label,dt)
#     if predict >10:
#         return "BIG"
#     return "SMALL"


# def make_predict_3():
#     BIG = 0
#     SMALL = 0
#     for number in range(10,31,5):
#         for max_depth in range(10,56,5):
#             for random_state in range(1,101,100):
#                 if make_predict_2(random_state,number,max_depth) == "BIG":
#                     BIG+=1
#                 else:
#                     SMALL +=1 
#     # print("BIG:{} SMALL:{}".format(BIG,SMALL))
#     if BIG>SMALL:
#         return "BIG"
#     return "SMALL"
# class Record:
#     index = 0
#     id = 0
#     def __init__(self,total,id,resultRaw,betTypeResult):
#         self.total = total
#         self.id = id
#         self.resultRaw = resultRaw
#         self.betTypeResult = betTypeResult

#         if Record.index !=0:
#             if self.id - Record.id !=1:
#                 import sys
#                 sys.exit("da xay ra loi ket qua khong lien tiep")
#         Record.index +=1
#         Record.id = self.id


#     def show(self):
#         print("|id:{}   |resultRaw:{}  |betTypeResult:{}".format(self.id,self.resultRaw,self.betTypeResult))


# def create_record():
#     response = get_response()

#     while "resultRaw" not in response.json()["content"][0]:
#         response = get_response()
#         time.sleep(2)

#     rc = Record(response.json()["total"],
#         response.json()["content"][0]["id"],
#         response.json()["content"][0]["resultRaw"],
#         response.json()["content"][0]["betTypeResult"])
#     return rc
# def is_betting():
#     response = get_response()
#     return response.json()["content"][0]["status"] == "BETTING"

class Wallet:
    def __init__(self,minmoney):
        self.predict = make_predict()
        self.minmoney = minmoney
        self.money = minmoney
        self.playing = True
        self.true = 0
        self.false = 0
        self.falseChain = 0
        self.maxFalse = 0
        self.percent = 0
    def check_predict(self,record):
        print("Predict:{} in  Result:{}  is:{}".format(self.predict,record.betTypeResult,self.predict in record.betTypeResult))


        if self.predict in record.betTypeResult:
            self.true  +=1
            self.falseChain = 0
            self.money -=10
            self.money = max(self.money,self.minmoney) 
        else:
            self.false+=1 
            self.falseChain+=1
            self.maxFalse = max(self.maxFalse,self.falseChain)
            self.money +=10
        if self.true - self.false>=5:
            quit_game("Hoan thanh")
        self.percent = int(self.true*100/(self.true+self.false))
    def make_predict(self):
        self.predict = make_predict()
    def show(self):
        print("True:{} False:{}  P:{}%  /Fchain:{}".format(self.true,self.false,self.percent,self.maxFalse))
    def bets(self):
        global indexBIG,indexSMALL,indexVND10K,indexVND50K,indexVND100K
        #########################
        return
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


# def calculate(money ):
#     numbervnd100 = money//100
#     money = money%100
#     numbervnd50 = money//50
#     money = money%50
#     numbervnd10 = money//10 
#     return numbervnd100,numbervnd50,numbervnd10

# def get_index(name):
#     confirm = input("Is {} in this position?".format(name))
#     if confirm == "":
#         print(pyautogui.position())
#         return pyautogui.position()
#     return None

# def moveclick_and_moveclicks(index1,index2,number2):
#     pyautogui.moveTo(index1)
#     pyautogui.click()

#     pyautogui.moveTo(index2)
#     pyautogui.click(clicks = number2,interval=2 )

#_________________________________________________________________

from manipulation import  *
from prophet import *
from getAPI import *
#_________________________________________________________________
indexBIG = get_index("BIG")
indexSMALL = get_index("SMALL")
indexVND10K = get_index("VND10K")
indexVND50K = get_index("VND50K")
indexVND100K = get_index("VND100K")

if None in [indexBIG,indexSMALL,indexVND10K,indexVND50K,indexVND100K]:
    quit_game("cai dai that bai")

start_game = input("start_game: ")
WL = Wallet(200)
print(WL.predict)
WL.bets()

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


