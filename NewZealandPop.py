import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import tabpy as tp

def riba(zod):
    print('\n'+'|' * 50)
    print('*** '+ zod.upper() + ' ***')
    print('|' * 50 )


# READING CSV FILES:
dbRegions = pd.read_csv('bd-dec20-births-deaths-by-region.csv', sep=',')
dbMother = pd.read_csv('bd-dec20-births-by-mothers-age.csv', sep=',', encoding='cp1252')
dbNatural = pd.read_csv('bd-dec20-births-deaths-natural-increase.csv', sep=',')
dbSexAge = pd.read_csv('bd-dec20-deaths-by-sex-and-age.csv', sep=',', encoding='cp1252')

# EXAMPLE OF TABLE 'DBNATURAL':
riba('Primary view of the table \'dbNatural\'')
print(dbNatural.head(10).to_string())

# COUNT OF VALUES CHECK:
# print(dbNatural[dbNatural['Births_Deaths_or_Natural_Increase'] == 'Births'].count())
# print(dbNatural[dbNatural['Births_Deaths_or_Natural_Increase'] == 'Deaths'].count())
# print(dbNatural[dbNatural['Births_Deaths_or_Natural_Increase'] == 'Natural_Increase'].count())

# NEW COLUMNS WITH NAN:
dbNatural['Births'] = np.nan
dbNatural['Deaths'] = np.nan
dbNatural['Natural_Increase'] = np.nan

# COPYING VALUES FROM COUNT TO NEW COLUMNS:
dbNatural['Births'][0:21] = dbNatural['Count'][0:21]
dbNatural['Deaths'][0:21] = dbNatural['Count'][21:42]
dbNatural['Natural_Increase'][0:21] = dbNatural['Count'][42:63]


# DELETING COPIED COLUMNS:
dbNatural = dbNatural.drop(labels=['Births_Deaths_or_Natural_Increase', 'Count'], axis=1)
dbNatural = dbNatural.drop(labels=range(21, 63), axis=0)

# SETTING TYPE:
dbNatural['Births'] = dbNatural['Births'].astype(int)
dbNatural['Deaths'] = dbNatural['Deaths'].astype(int)
dbNatural['Natural_Increase'] = dbNatural['Natural_Increase'].astype(int)

# CLEANED DATA IN 'DBNATURAL' TABLE:
riba('view of CLEANED table \'dbNatural\'')
print(dbNatural.head(10).to_string)

riba('dbnatural table correlations')
print(dbNatural.corr())
# sns.heatmap(dbNatural.corr(), annot=True)

# CORRELATION BETWEEN DEATHS AND PERIOD, OVER 0.9. CREATING LINEAR REGRESSION
x = dbNatural.Deaths.values.reshape(-1, 1)
Y = dbNatural.Period.values.reshape(-1, 1)
lm = linear_model.LinearRegression()
xTrain, xTest, yTrain, yTest = train_test_split(x, Y, test_size=0.1)
lm.fit(xTrain, yTrain)
yhat = lm.predict(x)
plt.scatter(x, Y)
plt.plot(x, yhat)
plt.title('Deaths over Period\n2005-2020')
plt.xlabel('Deaths')
plt.ylabel('Period')
print('')
print('A COEFFICIENT---', lm.coef_)
print('B COEFFICIENT ---', lm.intercept_)
print('R2---', lm.score(xTest, yTest))
plt.show()


# EXAMPLE OF TABLE 'DBREGIONS':
riba('Primary view of the table \'DBREGIONS\'')
print(dbRegions.head(22).to_string())

# COUNT OF VALUES CHECK:
# print(dbRegions[dbRegions['Birth_Death'] == 'Births'].count())
# print(dbRegions[dbRegions['Birth_Death'] == 'Deaths'].count())

# NEW COLUMNS WITH NAN:
dbRegions['Births'] = np.nan
dbRegions['Deaths'] = np.nan

# COPYING VALUES FROM COUNT TO NEW COLUMNS:
dbRegions = dbRegions.sort_values(['Birth_Death', 'Period'])
dbRegions['Births'][0:288] = dbRegions['Count'][0:288]
dbRegions['Deaths'][0:288] = dbRegions['Count'][288:]

# DELETING COPIED COLUMNS:
dbRegions.dropna(subset=['Deaths'], inplace=True)
dbRegions.drop(labels=['Birth_Death', 'Count'], axis=1, inplace=True)

# RESET OF INDEX:
dbRegions.reset_index(inplace=True)

# EXCLUDING UNNECESSARY ROWS:
dbRegions = dbRegions[dbRegions.Region != 'New Zealand']

# SETTING DATA IN THE SAME FORMAT AS IN TABLEAU MAP:
dbRegions['Births'] = dbRegions['Births'].astype(int)
dbRegions['Deaths'] = dbRegions['Deaths'].astype(int)
dbRegions['Period'] = dbRegions['Period'].astype(str)#


def area_fix(x):
    return (str(x).replace("Region not stated or\narea outside region", "Area Outside Region"))


def r_fix(x):
    return x.replace("region", "Region")


dbRegions['Region'] = dbRegions['Region'].apply(area_fix)
dbRegions['Region'] = dbRegions['Region'].apply(r_fix)

riba('cleaned and prepared \'dbregions\' for tableau')
print(dbRegions.head().to_string())

# EXPORTING TABLE AS XLSX:
dbRegions.to_excel('dbRegions.xlsx', index=False)

# CHECK TABLEAU!

# EXAMPLE OF TABLE 'DBMOTHER':
riba('Primary view of the table \'DBMOTHER\'')
print(dbMother.head().to_string())

# GROUP BY AGE RANGES:
dbMotherA = dbMother.groupby("Mothers_Age").sum()
dbMotherA = dbMotherA.drop(labels=['Total'], axis=0)
riba('dbmother grouped and counted by age ranges')
print(dbMotherA.to_string())

dbMotherA = dbMotherA.reindex(index = ['Under 15', '20–24', '15–19', '25–29', '30–34', '35–39', '40–44', '45 and over'])
explode = (0.4, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
dbMotherA.plot.pie(x="Mothers_Age", explode=explode, y='Count', labels=['','','','','','','',''], autopct='%1.1f%%',
                   startangle=180, colors = ['#ff9999','blue','#99ff99','#ffcc99', '#6465A5', '#F28A30', 'gold', 'brown'],
                   pctdistance=0.5, radius = 1.2)
plt.subplots_adjust(right=0.75)
plt.title('Mothers giving Birth in different age ranges\n2005-2020')
plt.ylabel(None)
plt.legend(title='Legend', bbox_to_anchor=(1, 1), labels=dbMotherA.index, loc='upper left')
plt.show()


# SETTING DBMOTHER'S DATA FOR OTHER REQUIREMENTS:

# FUNCTION FOR INTERACTIVE OUTPUT:
def MothersAge(mamzius):
    if mamzius <15:
        return 'Under 15'
    elif mamzius >= 15 and mamzius < 20:
        return '15–19'
    elif mamzius >= 20 and mamzius < 25:
        return '20–24'
    elif mamzius >= 25 and mamzius < 30:
        return '25–29'
    elif mamzius >= 30 and mamzius < 35:
        return '30–34'
    elif mamzius >= 35 and mamzius < 40:
        return '35–39'
    elif mamzius >= 40 and mamzius < 45:
        return '40–44'
    elif mamzius >= 45:
        return '45 and over'


# INTERACTIVE OUTPUT:
riba('fill the requested information bellow')
mmetai = int(input('Mother\'s age: '))
mamos=MothersAge(mmetai)
age_grupe = dbMother[dbMother.Mothers_Age == mamos]
age_grupe.plot.line(x='Period', y='Count')
plt.xlabel('Period')
plt.ylabel('Count')
plt.LineWidth = 10
plt.title('Count of Births for {} age group\n 2005-2020'.format(mamos))
plt.show()

# CLEANING DATA FOR OTHER VIEW:
dbMother['Under 15'] = np.nan
dbMother['15–19'] = np.nan
dbMother['20–24'] = np.nan
dbMother['25–29'] = np.nan
dbMother['30–34'] = np.nan
dbMother['35–39'] = np.nan
dbMother['40–44'] = np.nan
dbMother['45 and over'] = np.nan

dbMother = dbMother.sort_values(['Mothers_Age', 'Period'])
dbMother['15–19'][0:16] = dbMother['Count'][0:16]
dbMother['20–24'][0:16] = dbMother['Count'][16:32]
dbMother['25–29'][0:16] = dbMother['Count'][32:48]
dbMother['30–34'][0:16] = dbMother['Count'][48:64]
dbMother['35–39'][0:16] = dbMother['Count'][64:80]
dbMother['40–44'][0:16] = dbMother['Count'][80:96]
dbMother['45 and over'][0:16] = dbMother['Count'][96:112]
dbMother['Under 15'][0:16] = dbMother['Count'][128:]

dbMother.dropna(subset=['15–19'], inplace=True)
dbMother.drop(labels=['Mothers_Age', 'Count'], axis=1, inplace=True)
dbMother.reset_index(inplace=True)
dbMother.drop(labels='index', axis=1, inplace=True)

dbMother['Under 15'] = dbMother['Under 15'].astype(int)
dbMother['15–19'] = dbMother['15–19'].astype(int)
dbMother['20–24'] = dbMother['20–24'].astype(int)
dbMother['25–29'] = dbMother['25–29'].astype(int)
dbMother['30–34'] = dbMother['30–34'].astype(int)
dbMother['35–39'] = dbMother['35–39'].astype(int)
dbMother['40–44'] = dbMother['40–44'].astype(int)
dbMother['45 and over'] = dbMother['45 and over'].astype(int)

riba('DBMOTHER with new columns for general view on count of births')
print(dbMother.head().to_string())

plot=dbMother.plot.line('Period', ['Under 15', '15–19', '20–24', '25–29', '30–34', '35–39', '40–44', '45 and over'])
plt.xlabel('Period')
plt.ylabel('Count')
plt.title('Count of Births in different age groups\n2005-2020')
plt.subplots_adjust(right=0.75)
plt.legend(title='Legend', bbox_to_anchor=(1, 1), loc='upper left')
plt.show()


# EXAMPLE OF TABLE 'DBSEXAGE':
riba('Primary view of the table \'DBSEXAGE\'')
print(dbMother.head(25).to_string())

# FUNCTIONS FOR CLEANING DATA:
def num_fix(x):
    return int(str(x).replace(",", ""))

def line_fix(x):
    return x.replace("–", "-")

dbSexAge['Count'] = dbSexAge['Count'].apply(num_fix)
dbSexAge['Age'] = dbSexAge["Age"].apply(line_fix)


# FUNCTION FOR INPUT:
def SexAge(amzius):
    if amzius == 0:
        return 'Infant'
    elif amzius >= 1 and amzius < 5:
        return '1-4'
    elif amzius >= 5 and amzius < 10:
        return '5-9'
    elif amzius >= 10 and amzius < 15:
        return '10-14'
    elif amzius >= 15 and amzius < 20:
        return '15-19'
    elif amzius >= 20 and amzius < 25:
        return '20-24'
    elif amzius >= 25 and amzius < 30:
        return '25-29'
    elif amzius >= 30 and amzius < 35:
        return '30-34'
    elif amzius >= 35 and amzius < 40:
        return '35-39'
    elif amzius >= 40 and amzius < 45:
        return '40-44'
    elif amzius >= 45 and amzius < 50:
        return '45-49'
    elif amzius >= 50 and amzius < 55:
        return '50-54'
    elif amzius >= 55 and amzius < 60:
        return '55-59'
    elif amzius >= 65 and amzius < 70:
        return '65-69'
    elif amzius >= 70 and amzius < 75:
        return '70-74'
    elif amzius >= 75 and amzius < 80:
        return '75-79'
    elif amzius >= 80 and amzius < 85:
        return '80-84'
    elif amzius >= 85 and amzius < 90:
        return '85-89'
    elif amzius >= 90 and amzius < 95:
        return '90-94'
    elif amzius >= 95 and amzius < 100:
        return '95-99'
    elif amzius >= 100:
        return '100 and over'

# INPUTS FOR INTERACTIVE OUTPUTS:
riba('fill the requested information bellow:')
amzius = int(input('Your age: '))
lytis = str(input('Your gender: '))
vieta = str(input(('Your region in NZ: ')))

# OUTPUTS ACCORDING TO THE INPUTS:
age_gr = SexAge(amzius)
dbSexAges = dbSexAge[(dbSexAge['Age'] == age_gr) & (dbSexAge['Sex'].str.contains(lytis))]
dbSexAges.plot.line(x='Period', y='Count')
plt.xlabel('Period')
plt.ylabel('Count')
plt.title('Deaths around age {} \n 2010-2020'.format(amzius))
plt.grid(True)
plt.show()
dbRegionss = dbRegions[(dbRegions['Region'] == vieta)]
dbRegionss.plot.line(x='Period', y=['Births', 'Deaths'])
plt.xlabel('Period')
plt.ylabel('Births and Deaths')
plt.title('Births and Deaths in {} \n 2005-2020'.format(vieta))
plt.grid(True)
plt.show()

riba('thank you for your attention\nsee you in new zealand after quarantine')
