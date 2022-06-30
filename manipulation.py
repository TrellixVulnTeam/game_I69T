import pyautogui


def quit_game(mes):
    import sys
    sys.exit(mes)
    
def calculate(money ):
    numbervnd100 = money//100
    money = money%100
    numbervnd50 = money//50
    money = money%50
    numbervnd10 = money//10 
    return numbervnd100,numbervnd50,numbervnd10

def get_index(name):
    confirm = input("Is {} in this position?".format(name))
    if confirm == "":
        print(pyautogui.position())
        return pyautogui.position()
    return None

def moveclick_and_moveclicks(index1,index2,number2):
    pyautogui.moveTo(index1)
    pyautogui.click()

    pyautogui.moveTo(index2)
    pyautogui.click(clicks = number2,interval=2 )