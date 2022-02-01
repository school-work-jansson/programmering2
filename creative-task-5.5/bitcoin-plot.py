from cmu_graphics import *

from plot import Plot, PlotManager

# Source:
#   https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD
def load_data():
    
    with open('BTC-USD.csv', 'r') as data_file: 
        lines = data_file.readlines()
    
    data = []
    # remove first line of csv file (header)
    lines.pop(0)

    for line in lines:
        line.replace('\n', '')

        date, _, _, _, close, _, _ = line.split(',')
        data.append([date, close])

    return data

def process_data(data):
    xData = []
    yData = []

    for date, price in data:
        year, month, day = date.split('-')
        year_month_day = f"{year[2:]}{month}{day}"
        
        price_in_thousands = float(price) // 1000

        xData.append(year_month_day)
        yData.append(price_in_thousands)
        
    return xData, yData
    
def main():
    manager = PlotManager(left=60, bottom=350, width=300, height=300,
                        title='Bitcoin price (February 1 2021 - January 31 2022)',
                        xLabel='Day',
                        yLabel='Price (Thousands)')

    xData, yData = process_data(load_data())

    minY = min(yData)
    manager.plotLines(range(len(xData)), yData, color='steelBlue')
    manager.updateRanges(yMin=(minY / 2),)


main()

cmu_graphics.run()
