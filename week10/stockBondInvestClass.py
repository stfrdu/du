try: 
    import workspaceURL as url
except ModuleNotFoundError:
    print("Failed to import modules")
    
#declare class for Stocks
class Stocks:
    #initialize method to hold all major class attributes
    def __init__(self, name, share, purchase, current, pDate, purchaseID):
        self.name = name
        self.share = share
        self.purchase = purchase
        self.current = current
        self.pDate = pDate
        self.purchaseID = purchaseID
    
    #declare class method to calculate days between purchase and now
    def dayCalculator(self):
        try:
            #import date functionality
            from datetime import datetime
            #take current day, recorded purchase date, convert their format, run a calculation, and return
            d1 = datetime.today()
            d2 = self.pDate
            d2Update = datetime.strptime(d2, '%m/%d/%Y')
            daysBetween = ((d1 - d2Update).days)
            return daysBetween
        except:
            print('days between purchase and today calculation failed, make sure dates are formatted properly')

    #declare class method to calculate earnings/loss
    def calculateLossGain(self):
        try:
            earningLoss = round((float(self.current) - float(self.purchase)) * float(self.share), 2)
            return earningLoss
        except:
            print('calculation for loss/gain has failed')

    #declare class method to calculate per share earnings/loss
    def calculatePerShareEarnings(self):
        try:
            perShareEarning = round(float(Stocks.calculateLossGain(self))/float(self.share), 2)
            return perShareEarning
        except:
            print('calculation for perShareEarnings has failed')

    #declare class method to calculate Percentage Yield Loss
    def calculatePctYieldLoss(self):
        try:
            pctYield = round(((((float(self.current) - float(self.purchase))/float(self.purchase)))) * 100, 4)
            return pctYield
        except:
            print('calculation for percentage yield loss has failed')

    #declare class method to calculate yearly earnings/loss rate
    def calculateEarnLossRate(self):
        try:
            yrEarningRate = round((((((self.current) - float(self.purchase))/float(self.purchase))/(float(Stocks.dayCalculator(self)))) * 100), 4)
            return yrEarningRate
        except:
            print('calculation for yearly earnings loss rate has failed')
    
    #declare class method to print out all table header
    def printStockHeader():
        try:
            print("-" *90)
            print ('| {:^86} |'.format("Stock Ownership for Bob Smith"))
            print("-" *90)
            print ('| {:^20}'.format("Stock") + '| {:^20}'.format("Share #") + '| {:^20}'.format("Earnings/Loss") + '| {:^20} |'.format("Yearly Earning/Loss"))
            print("-" *90)
        except:
            print('printing the stock header has failed')
    
    #declare class method to print dynamic table values
    def printStockValues(self):
        try:
            #print data values for stocks into text file
            print (
            '| {:^20}'.format(str(self.name)) + 
            '| {:^20}'.format(str(self.share)) +
            '| {:^20}'.format("$" + str(Stocks.calculateLossGain(self))) +
            '| {:^20} |'.format(str(Stocks.calculateEarnLossRate(self)) + "%")
            )
            print("-" *90)
        except:
            print('printing stock values to text file has failed')

# declare bonds subclass
class Bonds(Stocks):
    def __init__(self, name, share, purchase, current, pDate, purchaseID, coupon, yieldAttr):
        super().__init__(name, share, purchase, current, pDate, purchaseID)
        self.coupon = coupon
        self.yieldAttr = yieldAttr

    #declare class method to print header
    def printBondHeader():
        try:
            #print header with formatting
            print("-" *155)
            print ('| {:^152} |'.format("Bond Ownership for Bob Smith"))
            print("-" *155)
            print ('| {:^20}'.format("Bond") + '| {:^20}'.format("Share #") + '| {:^20}'.format("Purchase Price") + '| {:^20}'.format("Current Price") + '| {:^20}'.format("Coupon") + '| {:^20}'.format("Yield") + '| {:^20} |'.format("Purchase Date"))
            print("-" *155)
        except:
            print('bond header has failed to print to text file')

    #declare class method to print dynamic table values
    def printBondValues(self):
        try:
            #print data values for bonds into text file
            print (
            '| {:^20}'.format(str(self.name)) + 
            '| {:^20}'.format(str(self.share)) +
            '| {:^20}'.format("$" + str(self.purchase)) +
            '| {:^20}'.format("$" + str(self.current)) +
            '| {:^20}'.format(str(self.coupon)) +
            '| {:^20}'.format(str(self.yieldAttr) + "%") +
            '| {:^20} |'.format(self.pDate)
            )
            print("-" *155)
        except:
            print('printing bond values to text file has failed')

#declare investor class
class Investor():
    def __init__(self, investorID, address, phoneNum):
        self.investorID = investorID
        self.address = address
        self.phoneNum = phoneNum

    def printInvestorFooter(self):
        try:
            #print investor info into text file
            #print header with formatting
            print("-" *90)
            print ('| {:^86} |'.format("Investor ID: #" + str(self.investorID)))
            print ('| {:^86} |'.format(str(self.phoneNum)))
            print ('| {:^86} |'.format(str(self.address)))
            print("-" *90)
        except:
            print('printing investor values to text file has failed')
        try:
            #close file after printing
            open(url.workspace + '\\' + 'output.txt', "a").close()
        except:
            print('file was not successfully closed')