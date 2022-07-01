import matplotlib.pyplot as plt
import numpy as np




def draw_result(x,y):
    plt.plot(x,y)
    plt.plot(x,[0 for i in range(len(x))])
    plt.xlabel("turn")
    plt.ylabel("profit")
    plt.show()


####### test
# x = [i for i in range(10)]
# y = [1,2,3,4,5,4,5,6,7,8]
# draw_result(x,y)