import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Outputs()
    def __init__(self, patientDf, roomDf, triageDf):
        self.patientDf = patientDf
        self.roomDf = roomDf
        self.triageDf = triageDf

    def meanPresInSystem(self):
        



class AdditionalCharts:
    def __init__(self, patientDf, roomDf, triageDf):
        self.patientDf = patientDf
        self.roomDf = roomDf
        self.triageDf = triageDf


    def triageLen(self):
#        print(self.triageDf.head())

        sns.lineplot(x = self.triageDf['clock'], y = self.triageDf['covid19'], label = 'with covid')
        sns.lineplot(x = self.triageDf['clock'], y = self.triageDf['others'], label = 'without covid')
#        plt.plot(self.triageDf['clock'], self.triageDf['covid19'])
        plt.show()

    def presenceFreq(self):

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



def readCsvs(path):
    patients = pd.read_csv(path+'./patients.csv')
    rooms = pd.read_csv(path+'room.csv')
    triage = pd.read_csv('triage.csv')
    return patients, rooms, triage

a,b,c = readCsvs('')
chart = AdditionalCharts(a, b, c)
chart.triageLen()