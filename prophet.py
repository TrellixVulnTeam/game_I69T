from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB


from getAPI import make_data

def predict_by_decisiontree(X_train,Y_train,X_test,random_state=100,max_depth=10):
    # global tree
    tree = DecisionTreeClassifier(criterion = "gini",random_state = random_state,max_depth=max_depth, min_samples_leaf=5)
    return tree.fit(X_train,Y_train).predict(X_test)[0]



# def predict_by_neural_network(data,label,dt,random_state=1):
#     clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state = random_state)
#     clf.fit(data, label)
#     MLPClassifier(alpha=1e-05, hidden_layer_sizes=(5, 2), random_state=1,solver='lbfgs')
#     return clf.predict(dt)[0]

def predict_by_naive_bayes(X_train, y_train,X_test):
    gnb = GaussianNB()
    return gnb.fit(X_train, y_train).predict(X_test)[0]


class Prophet:
    def __init__(self,id,algorithm,random_state,max_depth):
        self.id = id #lenofdata
        self.algorithm = algorithm
        self.random_state =random_state
        self.max_depth = max_depth
        self.predict = None
        self.true = 1
        self.false = 1
        self.percent = 50
    
    def check_resutl(self,result):
        if self.predict == None:
            return
        if "BIG" in result:
            result = "BIG"
        else:
            result = "SMALL"
        if self.predict >10:
            predict = "BIG"
        else:
            predict = "SMALL"
        if predict == result:
            self.true+=1
        else:
            self.false+=1
        self.percent = self.true*100/(self.true+self.false)
    def make_predict(self):
        X_train,Y_train,X_test = make_data(self.id)

        if self.algorithm == "tree":
            self.predict = predict_by_decisiontree(X_train,Y_train,X_test,self.random_state,self.max_depth)
        else:
            self.predict = predict_by_naive_bayes(X_train,Y_train,X_test)
    def show(self):
        print(self.id,self.algorithm,self.predict,int(self.percent))


def make_prophet_list():
    prophet_list = []

    algorithms = ["tree","naive"]
    for id in range(5,21,5):
        for algorithm in algorithms:
            for random_state in [1,50,100]:
                for max_depth in [5,10,100]:
                    prophet_list.append(Prophet(id,algorithm,random_state,max_depth))
    return prophet_list

def check_resutl(result):
    global prophet_list
    for prophet in prophet_list:
        prophet.check_resutl(result)
        # prophet.show()
def make_predict():
    global prophet_list
    big = 0
    small = 0

    sample_space = [0 for i in range(19)]
    for prophet in prophet_list:
        prophet.make_predict()
        sample_space[prophet.predict]+=1
        if prophet.predict >10:
            big += prophet.percent
        else:
            small += prophet.percent
    show_percent(big,small)
    print([i for i in range(19)])
    print(sample_space)
    if big>small:
        return "BIG"
    elif small > big:
        return "SMALL"
    else:
        return None

def show_percent(big,small):
    big = int(big*100/(big+small))
    small = 100-big
    print(r"BIG:{}% small:{}%".format(big,small))
prophet_list = make_prophet_list()