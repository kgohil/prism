import random
import sys
from operator import itemgetter


def displayModel(model):
    for rule,targetClass in model:
        print(str(rule.items())+'-->'+targetClass+"\n")


def handleMissingVals(trainData):
    #fetch nominal attrbutes in each column
    n = len(trainData[0])
    attrDict= dict()
    for col in range(0,n):

        attrList = []
        for data in trainData:
            if data[col] in trainData:
                attrList[data[col]] = attrList[data[col]] + 1
            else:
                attrList[data[col]] = 1
        attrDict[col] = attrList



def main():
    dataList = fetchData('weather.nominal.data')
    trainData = dataList[:]
    #trainData = handleMissingVals(trainData)
    #testData = dataList[8:]
    model = prism(trainData)
    #predictedList = predict(model,testData)
    displayModel(model)


#predicts and prints the results using the model and the test data
def predict(model, Data):
    predictedList = []
    testData = Data[:]
    for rule,classVal in model:
        if len(testData)>0:
            list = getCoveredInstances(rule,testData)
            predictedList.append(classVal,list)
            testData.remove(list)
        else:
            break
    if len(testData)>0:
        predictedList.append('outliers',testData)
    return predictedList

#fetching data
def fetchData(fileName):
    datalist = []
    rd =open(fileName,mode='r')
    list = rd.readlines()
    for l in list:
        subList = l.strip().split(',')
        datalist.append(subList)
    return datalist

#implements seperate and conquer and returns a model(a list of rule,class combination)
def prism(data):
    n = len(data)
    y=len(data[0])-1
    prismData = data[:]
    model = []
    #Start the algorithm
    while n>=1:
        ## select the most occuring class object form the list
        maxClass=getMaxClass(prismData,y)
        #get all the records related to that class
        list = getRecords(prismData,maxClass,y)
        #gets the rule and appends to the list of rules
        rule = getRule(list,y,maxClass,prismData)
        #extract values covered by the rule
        covered = getCoveredInstances(rule,prismData)
        if len(covered)>0:
            t =rule,maxClass
            model.append(t)
            #removes the elements that are already covered by the rule
            n=n-len(covered)
            prismData = [x for x in prismData if x not in covered]
    return model

#gets the maximum occuring class
def getMaxClass(prismData, y):
    maxClass,maxVal = getMaxElements(prismData,y)
    return maxClass

#gets the max attribute value and count for a given column
def getMaxElements(mainlist,col):
    list=dict()
    maxKey = str()
    maxValue = int()
    for data in mainlist:
        if data[col] in list:
           list[data[col]] = list[data[col]] + 1
        else:
            list[data[col]] = 1
    maxValue = 0
    maxKey = str()
    #gets the column with max count
    for key,value in list.items():
        if maxValue<=value:
            maxValue = value
            maxKey = key

    return maxKey,maxValue

#gets the list of records from which the rul will be extracted
def getRecords(prismData, maxClass, y):
    list = []
    for data in prismData:
        if data[y] == maxClass:
            list.append(data)
    return list

#gets a list of data that matches a value(val) in cloumn(i)
def getList(i, val, dataSet):
    list= []
    for row in dataSet:
        if row[i]== val:
            list.append(row)
    return list

#checks if extracted data as more than the target class
def checkList(targetClass, list, classCol):
    classVal = set()
    for row in list:
        classVal.add(row[classCol])
    if len(classVal) == 1 and classVal.__contains__(targetClass):
        return 1
    else:
        return 0

#Checking if rule is optimal
def validateRule(rule, targetClass, dataSet, y):
    list = dataSet[:]
    for i, val in rule.items():
        list = getList(i, val, list)
    found = checkList(targetClass, list, y)
    return found

#main function for extracting rules
def getRule(list, y, targetClass, DataSet):
    dictionary = dict()
    #get a list of max elements of all the attributes in the dataset
    for i in range(0,y):
        maxAttr, maxVal = getMaxElements(list,i)
        t = maxAttr,i
        dictionary[t]=maxVal
    sortedDict = sorted(dictionary.items(),key=itemgetter(1),reverse = True)#sort them according to their value
    rule = dict()
    validity = 0
    while validity==0:
        for tup in sortedDict:#gets the rules individually and checks for their validity
            attr = tup[0]
            rule[attr[1]] = attr[0]
            validity = validateRule(rule, targetClass, DataSet, y)
            if validity == 1:
                break
        if validity == 1:
                break
        else:
            sortedDict=random.sample(sortedDict,len(sortedDict))
            rule.clear()
    return rule

#prism implementation data: list of list type returns model: list of list[key,value]
def getCoveredInstances(rule, prismData):
    list = prismData[:]
    for col,val in rule.items():
        list = getList(col,val,list)
    return list


if __name__ == "__main__":
    main()