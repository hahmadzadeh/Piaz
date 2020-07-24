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

    def addPresenceCol(self):
        presCol = np.zeros(self.patientDf.shape[0])
        for i in range(self.patientDf.shape[0]):
            if self.patientDf['bored'][i] == False:
                presCol[i] = self.patientDf['finish'][i] - self.patientDf['arriaval'][i]
                if presCol[i]>200:
                    print("iii")
            else:
                presCol[i] = self.patientDf['borredom'][i]
        self.patientDf['presenceTime'] = presCol



class Outputs(AnalyzeCsvs):
    def __init__(self, path):
        super().__init__(path)

    def meanPresInSystem(self):
        print("without covid19 patients average presense in system is: %f"%(self.patientDf['presenceTime'].mean()))
    

class AdditionalCharts(AnalyzeCsvs):
    def __init__(self, path):
        super().__init__(path)


    def triageLen(self):
#        print(self.triageDf.head())

        sns.lineplot(x = self.triageDf['clock'], y = self.triageDf['covid19'], label = 'with covid')
        sns.lineplot(x = self.triageDf['clock'], y = self.triageDf['others'], label = 'without covid')
#        plt.plot(self.triageDf['clock'], self.triageDf['covid19'])
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
            for i in range(row['arriaval'], row['finish']):
                presCol[i] += 1

        sns.lineplot(clock, presCol)
        plt.show()


    def waitFreq(self):

        col = self.patientDf[self.patientDf['covid19'] == False]['inspection'] - self.patientDf[self.patientDf['covid19'] == False]['arriaval']
        sns.distplot(col, label='without covid', hist=False)
#        print(col)
        col = self.patientDf[self.patientDf['covid19'] == True]['inspection'] - self.patientDf[self.patientDf['covid19'] == True]['arriaval']
#        print(col)
        sns.distplot(col, label='with covid', hist=False)

        plt.xlim(0,)

        plt.xlabel('patients number')
        plt.title('patients waiting frequency')
        plt.show()



    def answerFreq(self):
        col = self.patientDf[self.patientDf['covid19'] == False]['finish']
        sns.distplot(col, label='without covid', hist=False)

        col = self.patientDf[self.patientDf['covid19'] == True]['finish']
        sns.distplot(col, label='with covid', hist= False)

        plt.xlim(0,)
        plt.xlabel('patients number')
        plt.title('patients answer frequency')
        plt.show()
'''
        a = col.hist(bins=100)
        print(a)
        a.plot()
        plt.show()
        '''





analyzeCsv = Outputs('')
#chart = AdditionalCharts('')
#chart.triageLen()
analyzeCsv.meanPresInSystem()
