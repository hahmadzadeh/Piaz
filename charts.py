import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class AnalyzeCsvs():
    def __init__(self, path):
        self.patientDf = pd.read_csv(path+'./patients.csv')
        self.roomsDf = pd.read_csv(path+'room.csv')
        self.triageDf = pd.read_csv('triage.csv')
        self.addPresenceCol()
        self.addWaitCol()

    def addPresenceCol(self):
        presCol = np.zeros(self.patientDf.shape[0])
        for i in range(self.patientDf.shape[0]):
            if self.patientDf['bored'][i] == False:
                presCol[i] = self.patientDf['finish'][i] - self.patientDf['arriaval'][i]
            else:
                presCol[i] = self.patientDf['borredom'][i]
        self.patientDf['presenceTime'] = presCol

    def addWaitCol(self):
        waitCol = np.zeros(self.patientDf.shape[0])
        for i in range(self.patientDf.shape[0]):
            if self.patientDf['bored'][i] == False:
                waitCol[i] = self.patientDf['inspection'][i] - self.patientDf['arriaval'][i]
            else:
                waitCol[i] = self.patientDf['borredom'][i]
        self.patientDf['waitTime'] = waitCol

class Outputs(AnalyzeCsvs):
    def __init__(self, path):
        super().__init__(path)

    def meanPresInSystem(self):
        print("part 1")
        print("without covid19 patients average presense in system is: %f"%(self.patientDf[self.patientDf['covid19']==False]['presenceTime'].mean()))
        print("with covid19 patients average presense in system is: %f"%(self.patientDf[self.patientDf['covid19']==True]['presenceTime'].mean()))
        print("all patients average presense in system is: %f"%(self.patientDf['presenceTime'].mean()))

    def meanWaitInSystem(self):
        print("part 2")
        print("without covid19 patients average wait in system is: %f"%(self.patientDf[self.patientDf['covid19']==False]['waitTime'].mean()))
        print("with covid19 patients average wait in system is: %f"%(self.patientDf[self.patientDf['covid19']==True]['waitTime'].mean()))
        print("all patients average wait in system is: %f"%(self.patientDf['waitTime'].mean()))

    def leavedPatients(self):
        print("part 3")
        print("number of leaved patients is: %d"%(self.patientDf[self.patientDf['bored']==True].shape[0]))

    def queuesMean(self):
        print("part 4")
        print("mean of number of persons in triage is: %f"%(self.triageDf['total'].mean()))
        numberOfRooms = self.roomsDf['id'].max()
        for i in range(1,numberOfRooms+1):
            print("mean of room number %d is: %f"%(i, self.roomsDf[self.roomsDf['id']==i]['total'].mean()))
        #print(self.roomsDf.head())


    def findN(self):
        print("part 5")
        n = ((1.96* self.patientDf['waitTime'].std())/(0.05* self.patientDf['waitTime'].mean()))**2 + 1
        print("for 95 percent of accuracy number of persons should be: %d"% (int(n)))


    def changeDocorRate(self):
        print("part6")
        print("if we set mean of random.exponential=0.5 for doctors then there would be no queue in rooms.\n"
              "one room simulated csv with this parameters is attached to this code.")




class AdditionalCharts(AnalyzeCsvs):
    def __init__(self, path):
        super().__init__(path)


    def triageLen(self):
#        print(self.triageDf.head())

        sns.lineplot(x = self.triageDf['clock'], y = self.triageDf['covid19'], label = 'with covid')
        sns.lineplot(x = self.triageDf['clock'], y = self.triageDf['others'], label = 'without covid')

#        plt.plot(self.triageDf['clock'], self.triageDf['covid19'])
        plt.title("part5 | queue chart")
        plt.show()

    def presenceFreq(self): #TODO: kasaii ke bored=true hast alan ignore mishan ke nabayad beshan.

        maxClock = -1
        ctr = 1
        while maxClock==-1:
            maxClock  = self.patientDf['finish'][self.patientDf.shape[0]-ctr]
            ctr += 1
#        print(maxClock)

        clock = np.array([i for i in range(maxClock)])
        presCol = np.zeros(maxClock)

        for _, row in self.patientDf.iterrows():

            if row['bored']==False:
                for i in range(row['arriaval'], row['finish']):
                    presCol[i] += 1
            else:
                for i in range(row['arriaval'], row['arriaval']+row['borredom']):
                    presCol[i] += 1


        sns.lineplot(clock, presCol)
        plt.title("part3(and4) | presence frequency")
        plt.show()


    def waitFreq(self):

        col = self.patientDf[self.patientDf['covid19'] == False]['inspection'] - self.patientDf[self.patientDf['covid19'] == False]['arriaval']
        sns.distplot(col, label='without covid', hist=False)
        plt.xlabel('patients number')
        plt.xlim(0,)
        plt.title('part2 | patients(without covid) waiting frequency')
        plt.show()
#        print(col)
        col = self.patientDf[self.patientDf['covid19'] == True]['inspection'] - self.patientDf[self.patientDf['covid19'] == True]['arriaval']
#        print(col)
        sns.distplot(col, label='with covid', hist=False)

        plt.xlim(0,)

        plt.xlabel('patients number')
        plt.title('part2 | patients(with covid) waiting frequency')
        plt.show()



    def answerFreq(self):
        col = self.patientDf[self.patientDf['covid19'] == False]['finish']
        sns.distplot(col, label='without covid', hist=False)

        col = self.patientDf[self.patientDf['covid19'] == True]['finish']
        sns.distplot(col, label='with covid', hist= False)

        plt.xlim(0,)
        plt.xlabel('patients number')
        plt.title('part1 | patients answer frequency')
        plt.show()
'''
        a = col.hist(bins=100)
        print(a)
        a.plot()
        plt.show()
        '''





analyzeCsv = Outputs('')
additionalChart = AdditionalCharts('')


analyzeCsv.meanPresInSystem()
print("----------")
analyzeCsv.meanWaitInSystem()
print("-----------")
analyzeCsv.leavedPatients()
print("-----------")
analyzeCsv.queuesMean()
print("-----------")
analyzeCsv.findN()
print("-----------")
analyzeCsv.changeDocorRate()

additionalChart.answerFreq()
additionalChart.waitFreq()
additionalChart.presenceFreq()
additionalChart.triageLen()
