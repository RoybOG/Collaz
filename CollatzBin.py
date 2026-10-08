testNum = 10




import re
import json
import numpy as np
import pandas as pd

import time
from functools import wraps

def time_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start high-res timer
        result = func(*args, **kwargs)
        end_time = time.perf_counter()    # End timer
        
        duration = end_time - start_time
        print(f"[{func.__name__}] Executed in {duration:.6f} seconds")
        return result
    return wrapper

'''

                            Online Python Compiler.
                Code, Compile, Run and Debug python program online.
Write your code in this editor and press "Run" button to execute it.

'''
BINARYSTRINGSDIR = "BINARYSTRINGSDICT.json"

def formatBinNum(n):
   

        

  consecutiveOnesPattern = re.compile(r'1{2,}')
  alternatingOnesPattern = re.compile(r'1(?:01)+')
    

  t =format(n, 'b') #np.base_repr(n,base=4) #
  #print(t)
   #print(re.findall(consecutiveOnesPattern, t))
  coloredT =re.sub(alternatingOnesPattern,f"\033[1;31m\\g<0>\033[39m", t)
  #coloredT =re.sub(consecutiveOnesPattern,f"\033[1;33m\\g<0>\033[39m", t)
 # if n % 2 == 1:  
  #  coloredT =  coloredT + "*"
#coloredT = coloredT.replace("/","\\")
  return coloredT
  #print(coloredT)
# Syntax structure: \033[STYLE;COLORm Your Text \033[0m

"""
def seperateBins(binStr):
    carryCascades = True
    seperatorPatterns = {"00":False, "11":True}
    binParts = []
    binPart = binStr[-1]
    for i in range(len(binStr)-1,0,-1):
        twoBits = binStr[i:i+1]
        if twoBits in seperatorPatterns:
            if seperatorPatterns[twoBits] ^ carryCascades:
                carryCascades = seperatorPatterns[twoBits]
"""


toBitStr = lambda b: format(b, 'b')

def seperateBins(n):
    carryCascades = True
    seperatorPatterns = {0:False, 3:True} # 00, 11
    getLastBits = lambda d=1: n & (2**d - 1)
    
    binParts = [""]
    
    while n >0:
        lastTwoBits = getLastBits(2)
        if lastTwoBits in seperatorPatterns and n >=2: #n is at least 2 bin digits (10=2)
            
            if seperatorPatterns[lastTwoBits] ^ carryCascades:
                binParts = binParts + [f"{lastTwoBits:02b}"]
                carryCascades = seperatorPatterns[lastTwoBits]    
                #binParts.append(""
            else:
                binParts[-1] = f"{lastTwoBits:02b}{binParts[-1]}"

            n = n >> 2
        else:
            binParts[-1] = toBitStr(getLastBits()) + binParts[-1]
            n = n >> 1

    return [s for s in binParts if s][::-1]


    #binParts[-1] =  binParts[-1] + format(n & 1, 'b')

def collatzBin(userNum):#, formatFunc):
    n=userNum
    finalText = ""
    binStringsDictGlobal = {}
    try:
        with open(BINARYSTRINGSDIR, "r", encoding="utf-8") as file:
            binStringsDictGlobal = json.load(file) 
    except FileNotFoundError:
        pass
      
    binStringsList = []
#printNum(n)

    while n > 1 :
       
        #finalText  = finalText + formatBinNum(n) + "\n"
        if n % 2 == 0:
            n = n // 2 
        else: 
            finalText = finalText + f"{n} ({toBitStr(n)})" #:{seperateBins(n)}"
             
            binStringsList.append(format(n, 'b'))
            #finalText  = finalText + "\n" #+ formatBinNum(n) + "\n"

            n = n * 3 + 1 
            finalText = finalText + f" -> {toBitStr(n)}\n"
            #finalText  = finalText+ "\n"# + formatBinNum(n) + "\n"
        #   printNum(n)
    else:

        #d = {num: i for i,num in enumerate(reversed(binStringsList))}
        #finalText  = finalText 
        finalText = f"{len(binStringsList)} steps \n" + finalText  + "1"
        print(finalText)
        with open(f"./binaryFiles/binaryText-{userNum}({format(userNum, 'b')}).txt", "w") as f:
            f.write(finalText)
            #print(finalText)
        #print(binStringsDictGlobal)

        binStringsDictGlobal.update(zip(binStringsList, range(len(binStringsList) - 1, -1, -1)))
        #binStringsDictGlobal.sort()
        with open(BINARYSTRINGSDIR, "w", encoding="utf-8") as file:
            json.dump(dict(sorted(binStringsDictGlobal.items(), key=lambda x: (x[1],x[0]))),file, indent=4)
        #print(1)

def collatzBinDerivative(userNum):#, formatFunc):
    n=userNum
    finalText = ""

    def addRow(rowValues): #build a csv file
        finalText = finalText + ', '.join(rowValues) + "\n"

    countLeadingZeros = lambda s: len(s) - len(s.rstrip('0'))
    binStringsDictGlobal = {}
    
      
    binStringsList = [] #
#printNum(n)

    #d = {"Number":[], "Bin":[],"NextEvenBin":[], "Reduction Size":[]} #,"Reduction Size":[], "Reductions By 2":[0], "Reductions By 4":[0], "Reductions By 8":[0], "Reductions By 16":[0]}

    d = {"Number":[], "Bin":[],"NextEvenBin":[],"NextEvenBinReduced":[], "Reduction Size":[]} #,"Reduction Size":[], "Reductions By 2":[0], "Reductions By 

    


    while n > 1 :
        
        #finalText  = finalText + formatBinNum(n) + "\n"
        if n % 2 == 0:
            n = n // 2 
        else: 
            
            d["Number"].append(n)
            d["Bin"].append(toBitStr(n))
          #  df[1]toBitStr(n)



            binStringsList.append(format(n, 'b'))
            #finalText  = finalText + "\n" #+ formatBinNum(n) + "\n"

            n = n * 3 + 1 
            d["NextEvenBin"].append(toBitStr(n))
            d["Reduction Size"].append(countLeadingZeros(toBitStr(n)))
            d["NextEvenBinReduced"].append(toBitStr(n).rstrip('0'))
            #dataRow[2] =toBitStr(n)
            #dataRow[3] = countLeadingZeros(dataRow[2])
            #finalText  = finalText+ "\n"# + formatBinNum(n) + "\n"
        #   printNum(n)
    else:
        df = pd.DataFrame(d)
        df['derivative'] = df['Number'].diff()

        df['Reudction Power'] = 2 ** df["Reduction Size"]
       
        #print(df)

        redCountDF = pd.get_dummies(df['Reudction Power'], dtype = int).cumsum().add_prefix("Cnt Reduction By ")
        df["Leading Reduction"] = redCountDF.idxmax("columns")
        df = df.join(redCountDF)
        df.to_csv(f"{userNum} old analysis.csv")
        #print(df)


def collatzBinDerivative2(userNum):#, formatFunc):
    n=userNum
    finalText = ""

    binStringsDictGlobal = {}
    
      
    binStringsList = [] #


    #df = pd.DataFrame(columns=("Number", "Bin","NextEvenBin","NextEvenBinReduced", "Reduction Size")) 
    d = {"Number":[], "Bin":[],"NextEvenBin":[],"NextEvenBinReduced":[], "Reduction Size":[], "diff":[]} #,"Reduction Size":[], "Reductions By 
    

    newRow = {"Number":n, "Bin": toBitStr(n)}
    while n > 1 :
        #finalText  = finalText + formatBinNum(n) + "\n"
   
            
          #  df[1]toBitStr(n)

        binStringsList.append(newRow["Bin"])
        #finalText  = finalText + "\n" #+ formatBinNum(n) + "\n"

        n = n * 3 + 1 
        
        newRow["NextEvenBin"] = toBitStr(n)
        newRow["NextEvenBinReduced"] =  newRow["NextEvenBin"].rstrip('0')

        newRow["Reduction Size"]= len(newRow["NextEvenBin"]) - len(newRow["NextEvenBinReduced"])
        
        n = int(newRow["NextEvenBinReduced"],2)
        newRow["diff"] = n - newRow["Number"]


        for k,v in newRow.items():
            d[k].append(v)
        #df = pd.concat([df, pd.DataFrame([newRow])], ignore_index=True)
        #print(df)
        
        newRow = {"Number":n, "Bin": newRow["NextEvenBinReduced"] }

            #dataRow[2] =toBitStr(n)
            #dataRow[3] = countLeadingZeros(dataRow[2])
            #finalText  = finalText+ "\n"# + formatBinNum(n) + "\n"
        #   printNum(n)
    else:
        df = pd.DataFrame(d)
        #df['derivative'] = df['Number'].diff()

        df['Reudction Power'] = 2 ** df["Reduction Size"]
       
        #print(df)

        redCountDF = pd.get_dummies(df['Reudction Power'], dtype = int).cumsum().add_prefix("Cnt Reduction By ")
        df["Leading Reduction"] = redCountDF.idxmax("columns")
        df = df.join(redCountDF)
        df.to_csv(f"{userNum} analysis.csv")
        #print(df)


def is_binary(s):
    # מחזיר True רק אם המחרוזת לא ריקה וכוללת רק 0 ו-1
    return set(s).issubset({'0', '1'})


#userNum = int("100101001", 2) 
#userNumRaw = input("Enter a number: ") ##27 #
#userNum = int(userNumRaw, 0)
#print(userNum)

#collatzBin(27)

#collatzBin(userNum)



def allStructuresWithNoConsesetiveZeros(maxDigits):
    maxNum = 1 << maxDigits
    noConsecutiveZerosInStructure = lambda n:(((~n) & ((~n)<<1)) & (maxNum-1)) ==0
    return [f"{i:0{maxDigits}b}" for i in range(maxNum) if noConsecutiveZerosInStructure(i)]


def collatz_sequence(n, max_tries=None):
    """
    Generator that yields the Collatz sequence starting from n.
    If max_tries is provided, will stop after that many iterations.
    """
    tries = 0
    current = n
    
    while current != 1:
        yield current
        
        if max_tries and tries >= max_tries:
            break
            
        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1
            
        tries += 1
    
    yield current  # Yield the final 1


def allStructuresWithNoConsesetiveOnes(maxDigits):
    maxNum = 1 << maxDigits
    hasConsecutiveZerosInStructure = lambda n:(((n) & ((n)<<1)) & (maxNum-1)) ==0
    return [f"{i:0{maxDigits}b}" for i in range(maxNum) if hasConsecutiveZerosInStructure(i)]




def allStructures(maxDigits):
    structures = [ # "carries":
        [s+"11" for s in allStructuresWithNoConsesetiveZeros(maxDigits-2)], # "noCarries":
        [s+"00" for s in allStructuresWithNoConsesetiveOnes(maxDigits-2)],

    ]
    return structures 

def printTrajectory(n):
    print(n)
    for tregNum in collatz_sequence(n):
        if True: #tregNum%2!=0:
            #print(seperateBins(n))
            tregNumBinStr = format(tregNum,'b')
        #tregNumBinStr = tregNumBinStr.replace("00","00, ")
        #tregNumBinStr = tregNumBinStr.replace("11","11, ")
            print(tregNumBinStr)

#userNum = int(input(),0)

#structs = allStructures(6)
#print(structs)
#10pri ntTrajectory(int(structs[0][0],2))

#def special_numbers

#while True:
userNum = 97 
userNum = int(input("Enter: "),0)
collatzBinDerivative2(userNum)
#time_performance(collatzBinDerivative)(userNum)

#time_performance(collatzBinDerivative2)(userNum)#userNum)





#print(allStructures(userNum))
