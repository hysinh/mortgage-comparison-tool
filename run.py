import gspread
from google.oauth2.service_account import Credentials
import math

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('mortgage_calculator')



"""
Mortgage Calculator / Comparison Tool:
Enter your mortgage(loan) amount, the APR (Annual Percentage Rate), and the length of
the loan to compare monthly payments and how much interest you pay over the lifetime of 
the loan.

# Principal = int(loan/mortgage amount)
# APR = float(Annual percentage rate as a percentage - 4.5%)
# loan_length = int(length of the loan in years - eg 15, 20, 30 , etc)

Users can input up to 4 sets of loan data.

# add new mortgage (creates a new class instance)
# delete/remove mortgage 
# save mortgage(s) (writes to my google sheet - removes class references)
# load mortgages (retrieve from google sheets - adds classes references)
# set active mortgage
# list mortgage
# everything is an Class instance operated on that mortgage

Program calculates:
1. Monthly_loan_payment = float(number with two decimal placements)
2. total_interest = float(total interest paid over the lifetime of the loan)
3. Difference in interest between different loans

# interest paid (# of months into mortgage)
# How much interest / principal paid in year (input year eg 12)
# amortization schedule
# if i pay XX, how much does it shorten the mortgage

Program displays a table:
1. Principal Amount
2. APR
3. loan_length
4. Monthly_loan_payment
5. total_interest paid over the course of the loan
6. how much money you save in interest with each reduction in total loan_length

Program requests if the user would like to run the program again to create new inputs and comparisons.

"""

class Mortgage:
    """
    Base Class for Mortgages
    """
    mortgage_ID = 0

    def __init__(self, principal, apr, length_of_mortgage):
        #instance attribute
        self.principal = principal
        self.apr = apr
        self.length_of_mortgage = length_of_mortgage
        Mortgage.mortgage_ID += 1
        self.mortgage_ID = Mortgage.mortgage_ID

    def details(self):
        """
        Method to return employee details as a string 
        """
        return f"MORTGAGE {self.mortgage_ID}:\nPrincipal: €{self.principal} \nLength of Mortgage: {self.length_of_mortgage} years\nAnnual Percentage Rate: {self.apr}%"
    
    def calculate_monthly_payment(self):
        """
        Calculates monthly payment
        """
        monthly_payment = ((self.apr / 100 / 12) * self.principal) / (1 - (math.pow((1 + (self.apr / 100 / 12)), (-self.length_of_mortgage * 12))))
        return f"Monthly payment = €{round(monthly_payment, 2)}"
    
    def calculate_lifetime_interest(self):
        pass

    def calculate_amoritization(self):
        pass



def input_validator(input):
    while True:
        try:
            return int(input)
        except ValueError:
            print("Not a valid number. Please enter a whole number.")


def compare_mortgages():
    print("inside the compare_mortgages function")

print("Welcome to my Mortgage Comparison Tool")
#compare_mortgages()

def create_mortgage():
    """
    Creates each Class Instance of a Mortgage - requires user input
    for the Principal amount, APR amount, and Length of Mortgage for
    caculations.
    """
    while True:
        try:
            principal = int(input('Enter the principal or loan amount: '))
            print(principal)
        except ValueError:
            print("That is not a whole number. Please enter a valid number.")
            continue
        if principal < 1:
            print("Please enter a valid number greater than 0.")
            continue
        
        try: 
            apr = float(input('Enter the Annual Percentage rate (eg. 4.3): '))
            print(apr)
        except ValueError:
            print("That is not a valid entry. Please enter a valid percentage.")
            continue
        if apr > 100 or apr < 0:
            print("That is not a valid percentage. Please enter a number between 0 - 100.")
            continue

        try:
            length_of_mortgage = int(input('Enter the length of the mortgage in years (eg 30): '))
            print(length_of_mortgage)
        except ValueError:
            print("That is not a valid number. Please enter a number.")
            continue
        if length_of_mortgage < 1:
            print("That is not a valid entry. Please enter a whole number greater than 0.")
            continue
        
        mortgage1 = Mortgage(principal, apr, length_of_mortgage)
        print(mortgage1.details())
        print(mortgage1.calculate_monthly_payment()) 

        break



    #if not int(principal):
        #print("That is not a whole number. Please enter a whole number.")   
    
    
    mortgage1 = Mortgage(principal, apr, length_of_mortgage)
    print(mortgage1.details())
    print(mortgage1.calculate_monthly_payment())    


create_mortgage()





