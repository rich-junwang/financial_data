import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import chromedriver_binary
import string

pd.options.display.float_format = '{:.0f}'.format

#ticker = input("Input the ticker of the company you'd like to see the financials of: ")
ticker = "aapl"

is_link = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
bs_link = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
cf_link = f'https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}'


def yahoo_financial_statements(ticker):

    #ticker = input("Input the ticker of the company you'd like to see the financials of: ")

    is_link = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
    bs_link = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
    cf_link = f'https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}'

    statements_list = [is_link,bs_link,cf_link]

    headers = []
    temp_list = []
    label_list = []
    final = []
    index = 0

    df_lists = list()
    driver = webdriver.Chrome()

    for link in statements_list:


        driver.get(link)
        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html,'lxml')

        features = soup.find_all('div', class_='D(tbr)')

        #create headers
        for item in features[0].find_all('div', class_='D(ib)'):
            headers.append(item.text)

        #statement contents
        while index <= len(features)-1:
            #filter for each line of the statement
            temp = features[index].find_all('div', class_='D(tbc)')
            for line in temp:
                #each item added to a temp list
                temp_list.append(line.text)
            #temp_list added to final list
            final.append(temp_list)
            #clear temp_list
            temp_list = []
            index+=1

        df = pd.DataFrame(final[1:])
        df.columns = headers
        df.index = final[1]

        #function to make all values numerical
        def convert_to_numeric(column):

            first_col = [i.replace(',','') for i in column]
            second_col = [i.replace('-','') for i in first_col]
            final_col = pd.to_numeric(second_col)

            return final_col

        for column in headers[1:]:
            df[column] = convert_to_numeric(df[column])

        final_df = df.fillna('-')
        df_lists.append(final_df)

        #reset all lists
        headers = []
        temp_list = []
        label_list = []
        final = []
        index = 0

    return df_lists


financials = yahoo_financial_statements("appl")

income_statement = financials[0]
balance_sheet = financials[1]
cash_flow_statement = financials[2]

income_statement.index = income_statement[['Breakdown']]


