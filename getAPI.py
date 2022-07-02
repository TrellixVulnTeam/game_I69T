import requests
import json
import numpy
import time



def number_to_result(number):
    if number>10:
        return "BIG"
    return "SMALL"
def get_response():
    return requests.get("https://api-csn-sun.gameland.vip/api/v1/round/ended?limit=150&page=1&tableId=103")


def get_history_result():# return [10,14,5,7,16]
    response = get_response()

    history_list = response.json()["content"]
    history = []
    for i in range(len(history_list)-1,0,-1):
        kq = history_list[i]["resultRaw"]
        history.append(int(kq[0])+int(kq[2])+int(kq[4]))
    return history

def make_data(lenrecord):
    history = get_history_result()
    data = []
    label = []
    for i in range(len(history)-lenrecord):
        data.append(history[i:i+lenrecord])
    #     label.append(history[i+lenrecord])
        label.append(number_to_result(history[i+lenrecord]))
    dt = history[len(history)-lenrecord:len(history)]
    return data,label,[dt]


class Record:
    index = 0
    id = 0
    def __init__(self,total,id,resultRaw,betTypeResult):
        self.total = total
        self.id = id
        self.resultRaw = resultRaw
        self.betTypeResult = betTypeResult

        if Record.index !=0:
            if self.id - Record.id !=1:
                import sys
                sys.exit("da xay ra loi ket qua khong lien tiep")
        Record.index +=1
        Record.id = self.id


    def show(self):
        print("|id:{}   |resultRaw:{}  |betTypeResult:{}".format(self.id,self.resultRaw,self.betTypeResult))


def create_record():
    response = get_response()

    while "resultRaw" not in response.json()["content"][0]:
        response = get_response()
        time.sleep(2)

    rc = Record(response.json()["total"],
        response.json()["content"][0]["id"],
        response.json()["content"][0]["resultRaw"],
        response.json()["content"][0]["betTypeResult"])
    return rc
def is_betting():
    response = get_response()
    return response.json()["content"][0]["status"] == "BETTING"