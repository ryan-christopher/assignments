'''
Ryan Christopher
Class: CS 677
Date: 9/19/2023
Assignment 2 Question 1

=======Description of Problem=======
Taking the csv of my stock and SPY, create a dataframe with that info.
Then, add in a column of the "True Value" of the stock as a + or -,
and write a function that can determine the likelihood of a day's "True Value"
based off the prior sequence of up and down days.
'''
import pandas as pd

# ========== Part 1 ==========
# determineTrueValue assigns the True Value column to + if the 
# day's return is positive, and - if the day's return is negative
def determineTrueValue(df):
    if float(df['Return']) >= 0:
        df['True Value'] = '+'
    else:
        df['True Value'] = '-'
    return df

# use the apply method on the dataframe to assign the correct 
# True Value for each day
def getTable(stock):
    # read CSV data and store into dataframe called stock_data
    stock_data = pd.read_csv('assignment2/stock_data/' + stock + '.csv')

    # remove extra info that we will not need to use
    stock_data = stock_data.drop(['Week_Number', 'Year_Week', 'Open', 'High', 'Low',
                  'Close', 'Volume', 'Adj Close', 'Short_MA', 'Long_MA'], 
                  axis = 1)
    
    stock_data = stock_data.apply(determineTrueValue, axis = 1)

    return stock_data

stock_data = getTable('COST')
# print(stock_data)


# ========== Part 2 ==========
# taking years 1, 2, and 3, determine the probability
# of the next day being an "up" day

# create global level string to store sequence of +'s and -'s
# (global level works best as it is mainly 
# being used with an apply method)
true_labels = ""

# gatherValues is a helper function that takes a given
# day's True Value and adds it to the string true_labels
def gatherValues(df):
    global true_labels
    if int(df['Year']) < 2019:
        true_labels += df['True Value']

# apply the gatherValues function to the dataframe given 
# as a parameter, and return the probability of an up day
def upDayProb(df):
    global true_labels
    true_labels = ""
    df.apply(gatherValues, axis = 1)
    return true_labels.count("+") / len(true_labels)

# print(upDayProb(stock_data))


# ========== Part 3 and 4 ==========
# taking years 1, 2, and 3, determine the probability
# that after seeing k number of consecutive days the 
# next day will be have an opposite value
def kSequenceProbability(df, sequenceVal, targetVal, kVal):
    global true_labels
    true_labels, probabilities = "", []

    # generate string of True Values 
    df.apply(gatherValues, axis = 1)

    # calculate probability of each value for k, then append 
    # result to the list probabilities 
    for k in range(1, kVal + 1):
         numTarget = true_labels.count((sequenceVal * k) + targetVal)
         numOpposite = true_labels.count((sequenceVal * k) + sequenceVal)
         probabilities.append(numTarget / (numTarget + numOpposite))
    
    # return the k number of probabilities 
    return probabilities

# probability of up day after k consecutive down days
# print(kSequenceProbability(stock_data, '-', '+', 3))

# probability of down day after k consecutive up days
# print(kSequenceProbability(stock_data, '+', '-', 3))