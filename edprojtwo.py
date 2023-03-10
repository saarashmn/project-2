import numpy as np
import random
import sys
import math
import matplotlib.pyplot as plt

def spin(PosOut, Probs, ProbsHouse):
    
    Sum1 = 0
    Sum2 = 0
    
    while Sum1 == Sum2:
        
        value1 = np.random.multinomial(n=PosOut, pvals=ProbsHouse)
        value2 = np.random.multinomial(n=PosOut, pvals=Probs)
    
        Sum1 = sum(np.where(value1 !=0)[0]) + 2
        Sum2 = sum(np.where(value2 !=0)[0]) + 2
        
        if len(np.where(value1 !=0)[0]) == 1: #Degeneracies 
            Sum1 = 2*sum(np.where(value1 !=0)[0]) + 2
        elif len(np.where(value2 !=0)[0]) == 1:
            Sum2 = 2*sum(np.where(value2 !=0)[0]) + 2
        
    if Sum2 > Sum1: #House won
        return 0
    else:
        return 1    #House lost

#Significance testing
def Alpha_J(Dos_Params,alph):
    
    Dos0   = Dos_Params[0]
    Dos1   = Dos_Params[1]
    
    Dos0 = np.array(Dos0) #Transform to numpy array
    Dos1 = np.array(Dos1)

    alpha     = alph # 
    crit_val  = Dos0[0][min(int((1-alpha)*len(Dos0[0])),len(Dos0[0])-1)]
    remainder = np.where(Dos1[0] > crit_val)[0][0] 
    J      = remainder/len(Dos1[0]) # 
    power     = 1-J                 # the non-rejection side of the critical value."

    # 
    print("This is obtained critical value, beta and power respectively: " + str(crit_val)+" "+str(beta)+" "+ str(power))
    return [crit_val,beta,power,remainder]

# Obtain our probabilities and normalize them
def sum_to_one(p):
    flag = False
    while flag == False:
        s = np.random.normal(size = 3, loc = p)
        normalize1 = abs(s/sum(s))
        if sum(normalize1) == 1:
            flag == True
            return(normalize1)
#capture
nexp = 100
trials = 100
univ = 20
particles = 2
al = 0.3
multi_verse = []
poss1 = []
poss2 = []
Stdev = []
Avg    = []

for i in range(0,univ):
    
    probs        = sum_to_one(al)  # [1,2,3]
    probb2       = probs                 # [1,2,3]
    poss1.append(probs)
    poss2.append(probb2)
    
    Expm = [[spin(particles, probs, probb2) for i in range(0,trials)] for t in range(0,nexp)] 
    Expm = np.array(Expm)
    
    b = np.sum(Expm,axis=1) # frequency counting for a whole experiment 
    multi_verse.append(b)
    ddos0 = plt.hist(b, trials+1, density=True, facecolor='b', stacked =True, alpha=0.7)
    
    Avg.append(np.mean(ddos0[1]))
    Stdev.append(np.std(ddos0[1]))
title = "Universe of Distributions: Average number of trials to get desired excited states"
multi_b = plt.hist(Avg, 70, density=True, facecolor='r', stacked =True, alpha=0.7)
plt.title(title)
plt.grid()
plt.xlabel("Average number of trials to getexcited states")
plt.ylabel("Probability")
plt.show()

print(np.average(np.round(multi_b[1],2)))
print(round(np.std(multi_b[1])))

#
a = np.where(multi_b[0] == max(multi_b[0]))
print("The location of the most likely excited states " +str(a[0][0]))
print("The value " +str(round(multi_b[1][25])))
print("The probability is: "+str(100*round(multi_b[0][25],4))+"%")


power0     = []
crit_val0  = []
J0      = []
remainder0 = []
significance = 0.5
representative = plt.hist(multi_verse[25], trials+1, density=True, facecolor='b', stacked =True, alpha=0.7)

for i in range(0,univ):
    b = plt.hist(multi_verse[i], trials+1, density=True, facecolor='b', stacked =True, alpha=0.7)
    parameters = [representative,b]
    cv0,Jj0,p0,remd0 = Alpha_J(parameters, significance) 
    
    power0.append(p0)
    crit_val0.append(cv0)
    J0.append(Jj0)
    remainder0.append(remd0)

plt.figure()
plt.scatter(Avg,power0)
plt.xlabel("Likely Average # successful transfers")
plt.ylabel("coupling strength")
plt.title("Likely transfer vs Power with significance" + " $\\alpha$ = " +str(significance))

likely_mean_wins = multi_b[1][25]
print(round(likely_mean_wins))
plt.axvspan(likely_mean_wins, mean_wins, alpha=0.9, color='red',label = 'Critical Likely Win')
plt.legend()
plt.grid()
plt.show()

# We will find places where the Std varies greatly with different means.
Stdev = np.array(Stdev)
#print(Stdev)
el = np.where(Stdev < 8)[0]
em = np.where(Stdev > 9)[0]
oh = np.where(Stdev > 10)[0]
pe = np.where(Stdev > 11)[0]

print(el)
print(em)
print(oh)
print(pe)

for e in (el[1],em[5],oh[10],pe[1]):
    b = multi_verse[e]
    title = "Average # successful transfer"
    plt.figure()
    dos0 = plt.hist(b, trais+1, density=True, facecolor='g', stacked =True, alpha=0.7)
    
    sigma0 = np.std(dos0[1])
    mean0 = np.mean(dos0[1])
    
    print("The means are: "+ str(mean0))

    plt.xlabel('$\\lambda = N_{wins}$')
    plt.ylabel('Probability')
    plt.title(title)
    plt.axvspan(mean0-sigma0, sigma0+mean0, alpha=0.1, color='r',label = '1 $\\sigma$ = ' +str(round(sigma0))+" Games")
    plt.axvspan(mean0, mean0, alpha=0.5, color='red',label = 'Mean')
    plt.grid(True)
    plt.legend()
    plt.show()
