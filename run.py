import gspread
from google.oauth2.service_account import Credentials
import math
#from PIL import Image, ImageFont, ImageDraw
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
import pyfiglet
from tabulate import tabulate
import os
import pandas as pd

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('mortgage_calculator')


mortgage_dict = {}

def clear():
    """
    Function to clear terminal through the game.
    """
    os.system("cls" if os.name == "nt" else "clear")


def welcome_screen():
    """
    ASCII PIXEL ART CODE
    """
    clear()
    logo_text = pyfiglet.figlet_format("Mortgage\nCalculator")
    print(logo_text)
    print("Welcome to my Mortgage Comparison Tool")
    is_valid = False
    while is_valid != True:
        try:
            proceed = input("Enter any key to proceed \n").lower()
            if proceed != "":
                is_valid = True
            # elif proceed == "n":
            #     is_valid = True
            #     print("*** Thanks for visiting! ***")
            #     exit()
            else:
                print("Please enter any letter to proceed.")
        except ValueError:
            print("That is not a valid reponse. Please enter Y or N.")
    


def menu_screen():
    """
    Menu Screen with options displayed in a table
    """
    clear()
    print("\n")
    print("** Mortgage Calculator Tool **\n")
    print("You have the following options:\n ")
    table = [
        ["Option",1,"Add a mortgage"],
        ["Option",2,"View a Mortgage"],
        ["Option",3,"Display Mortgage Comparison"],
        ["Option",4,"Calculate Overpayments"],
        ["Option",5,"View Amortization Schedules"],
        ["Option",6,"Exit Program"],
        ["Option",0,"Return to Main Menu"]]
    print(tabulate(table))
    print("\n")
    

def small_menu():
    """
    Compressed Menu that in a single line 
    """
    print("** Mortgage Calculator Tool MENU OPTIONS **")
    print("1. Add Mortgage | 2. View a Mortgage | 3. Display Mortgage Comparison")
    print("4. Calculate Overpayments | 5. View Amortization Schedules | 0. Return to Main Menu | ")
    print("6. Exit Program | 0. Return to Main Menu | ")
    print("\n*******************************************************")



def validate_value(prompt_text):
    """
    Prompts user for input and validates that input is an integer greater
    than 0.
    """
    is_valid = False
    while is_valid != True:
        try:
            value = int(input(prompt_text))
            if value > 0:
                is_valid = True
            else:
                print("Value must be greater than 0. Please enter a valid number.")
        except ValueError:
            print("That is not a whole number. Please enter a valid number.")
        
    return value


def validate_apr():
    """
    Prompts user for input and validates that the input is a float
    with a value between 0 and 100.
    """
    is_valid = False
    while is_valid != True:
        try:
            apr = float(input('Enter the Annual Percentage rate or APR (e.g. 4.3): \n'))
            if apr > 0 and apr < 100:
                is_valid = True
            else:
                print("APR must be greater than 0. Please enter a valid number.")
        except ValueError:
            print("That is not a number. Please enter a valid number.")
        
    return apr



class Mortgage:
    """
    Base Class for Mortgages
    """
    mortgage_ID = 200
    start_year = 0 # start of mortgage
    extra_monthly_principal = 0

    def __init__(self, principal, apr, length_of_mortgage):
        #instance attribute
        self.principal = principal
        self.apr = apr
        self.length_of_mortgage = length_of_mortgage
        Mortgage.mortgage_ID += 1
        self.mortgage_ID = Mortgage.mortgage_ID
        self.start_year = Mortgage.start_year
        self.extra_monthly_principal = Mortgage.extra_monthly_principal

    def details(self):
        """
        Method to return employee details as a string 
        """
        return f"\nMORTGAGE {self.mortgage_ID}:\nPrincipal: €{self.principal} \nLength of Mortgage: {self.length_of_mortgage} years\nAnnual Percentage Rate: {self.apr}%"
    
    def calculate_monthly_payment(self):
        """
        Calculates monthly payment
        """
        monthly_payment = round(((self.apr / 100 / 12) * self.principal) / (1 - (math.pow((1 + (self.apr / 100 / 12)), (-self.length_of_mortgage * 12)))), 2)
        return monthly_payment
    
    def calculate_lifetime_interest(self):
        total_interest = round((self.length_of_mortgage * 12 * self.calculate_monthly_payment()) - self.principal, 2)
        return total_interest

    def get_table_values(self):
        row = [self.mortgage_ID, "€{:,.2f}".format(self.principal), self.apr, self.length_of_mortgage, "€{:,.2f}".format(self.calculate_monthly_payment()), "€{:,.2f}".format(self.calculate_lifetime_interest())]
        return row

    def calculate_revised_interest(self):
        pass
    
    def calculate_amortization_schedule(self):
        schedule = []
        balance = self.principal
        rate = self.apr/100/12
        total_payments = self.length_of_mortgage*12
        monthly_payment = self.calculate_monthly_payment()
        for Month in range(1, total_payments):
            interest_payment = balance * rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            total_payments -= 1
            schedule.append({
                    'Month #' : Month,
                    'Payments Left' : total_payments,
                    'Payment' : "€{:,.2f}".format(monthly_payment),
                    'Principal' : "€{:,.2f}".format(principal_payment),
                    'Interest' : "€{:,.2f}".format(interest_payment),
                    'Balance' : "€{:,.2f}".format(balance)     
                })

        return pd.DataFrame(schedule) 


def create_mortgage():
    """
    Creates each Class Instance of a Mortgage - requires user input
    for the Principal amount, APR amount, and Length of Mortgage for
    caculations.
    """
    clear()
    small_menu()
    print("\nEnter Your Mortgage details in below:\n")
    principal = validate_value('Enter the principal or loan amount in Euro: \n')
    apr = validate_apr()
    length_of_mortgage = validate_value("Enter the length of the mortgage in years (e.g. 30): \n")

    # Creates a Mortgage Class Instance
    mortgage = Mortgage(principal, apr, length_of_mortgage)
    mortgage_dict[mortgage.mortgage_ID] = mortgage

    print("\nYou created a Mortgage with the following details:")
    print(mortgage.details())
    print("Your monthly payment is: €{:,.2f}".format(mortgage.calculate_monthly_payment())) 

    print("\n*******************************************************\n")
    

def view_mortgage():
    """
    Allows user to view individual Mortgage details one at a time
    """
    clear()
    small_menu()

    # Prints a column of the available Mortgage Class Instances
    print("You have entered the following mortgages:\n")
    for x in mortgage_dict:
        print(f"Mortgage: {x}")

    # Prompts user to select a mortgage to view or user can select to return to main menu
    print("\n")
    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter the number of the mortgage that you'd like to view \nor enter '0' to return to the main menu: \n"))
            if selection == 0:
                menu_screen()
                is_valid = True
            else:
                for x in mortgage_dict:
                    if selection == x:
                        print(mortgage_dict[x].details())
                        print("Monthly Payment: €{:,.2f}".format(mortgage_dict[x].calculate_monthly_payment()))
                        print("Cost of this loan: €{:,.2f}".format(mortgage_dict[x].calculate_lifetime_interest()))
                        is_valid = True
                    else:
                        continue
        except ValueError:
            print("Please enter a valid number")

    print("\n*******************************************************")
        


def compare_mortgages():
    """
    Displays a comparison table of all the mortgages entered by the user
    """
    clear()
    small_menu()
    mortgage_table = [["Mortgage","Principal","APR %","Loan\nLength","Monthly\nPayment", "Total\nInterest", "Total\nSavings"]]

    print("\nMORTGAGE COMPARISON TABLE\n")
    for x in mortgage_dict:
        mortgage_table.append(mortgage_dict[x].get_table_values())

    print(tabulate(mortgage_table, tablefmt="simple"))
    print("\n******************************************************* \n")
    


def extra_monthly_principal():
    """
    Calculates new payment and total interest with extra monthly principal payments
    """
    clear()
    small_menu()
    print("Calculate Mortgage Overpayments:\n")

    principal = validate_value('Enter the remaining principal left on your loan in Euro: \n')
    apr = input_apr()
    remaining_length_of_mortgage = validate_value('How many years are left on your mortgage?  (e.g. 30) \n')

    extra_principal = validate_value('Enter the extra principal you would like to pay each month: \n')
    
    mortgage = Mortgage(principal, apr, remaining_length_of_mortgage)
    mortgage_dict[mortgage.mortgage_ID] = mortgage
    print("\nCurrent Mortgage: ")
    print(mortgage.details())
    print("Your current monthly payment is: €{:,.2f}".format(mortgage.calculate_monthly_payment()))
    
    print("\nUpdated Mortgage:")
    print(f"Extra principal: {extra_principal}")


    print("\n*******************************************************\n")


    #interest = (monthly+extra amount) * totalpayments - principal


def lump_payment():
    """
    Calculates new payment and total interest with an extra lump principal payments
    """
    clear()
    small_menu()
    print("Calculate Mortgage Overpayments:\n")

    principal = validate_value('Enter the remaining principal left on your loan in Euro: \n')
    apr = validate_apr()
    remaining_length_of_mortgage = validate_value("Enter the remaining length of your mortgage in years: \n")

    lump_payment = validate_value('How much of a lump payment do you want to make? \n')
    
    # Creates Mortgage Instance with Current Mortgage inputs
    mortgage = Mortgage(principal, apr, remaining_length_of_mortgage)
    mortgage_dict[mortgage.mortgage_ID] = mortgage
    
    # Prints Current Mortgage Details
    print("\nCurrent Mortgage: ----------------------------------------")
    print(mortgage.details())
    print("Your current monthly payment is: €{:,.2f}".format(mortgage.calculate_monthly_payment()))
    print("The current cost of the remainder of this mortgage is: €{:,.2f}".format(mortgage.calculate_lifetime_interest()))
    
    # Prints Updated Mortgage Details after Lump Payment applied
    print("\nUpdated Mortgage: ----------------------------------------")
    new_mortgage = Mortgage((principal-lump_payment), apr, remaining_length_of_mortgage)
    mortgage_dict[new_mortgage.mortgage_ID] = new_mortgage
    print(new_mortgage.details())
    print("Your new monthly payment is: €{:,.2f}".format(new_mortgage.calculate_monthly_payment()))
    print("The updated cost of the remainder of this mortgage is: €{:,.2f}".format(new_mortgage.calculate_lifetime_interest()))
    print(f"Extra principal: €{lump_payment}")

    print("\n*******************************************************\n")



def overpayments():
    """
    Gives User the selection of making monthly overpayments or a lump sum overpayment
    """
    clear()
    small_menu()
    print("Mortgage Overpayments:\n")

    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter 1 for monthly overpayments,  2 for a lump overpayment \nor enter '0' to exit this menu: \n"))
            if selection == 0:
                menu_screen()
            elif selection == 1:
                print("Make monthly overpayments")
                #extra_monthly_principal()
                is_valid = True
            elif selection == 2:
                lump_payment()
                is_valid = True
            else:
               print("That is not a valid option. Please choose one from the list above.")
        except ValueError:
            print("Please enter a valid mortgage number")



def amortization():
    """
    Allows user to view an amoritization for individual Mortgage details one at a time
    """
    clear()
    small_menu()
    print("You have entered the following mortgages:\n")
    for x in mortgage_dict:
        print(f"Mortgage: {x}")

    print("\n")
    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter the number of the mortgage that you'd like to amortize \nor enter '0' to return to the main menu: \n"))
            if selection == 0:
                menu_screen()
                is_valid = True
            else:
                for x in mortgage_dict:
                    if selection == x:
                        clear()
                        menu_screen()
                        print(f"AMORTIZATION SCHEDULE FOR:")
                        schedule = mortgage_dict[x].calculate_amortization_schedule()
                        print(mortgage_dict[x].details())
                        print(schedule)
                        print("\n")
                        is_valid = True
                    else:
                        continue
        except ValueError:
            print("Please enter a correct number")

    print("\n*******************************************************\n")


def run_mortgage_tool():
    """
    Allows the user to select from various menu options for the Mortgage Comparison Tool
    """
    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter a menu selection: \n"))
            if selection == 1:
                create_mortgage()
                #is_valid = True
            elif selection == 2:
                view_mortgage()
                print("\n")
            elif selection == 3:
                compare_mortgages()
            elif selection == 4:
                overpayments()
            elif selection == 5:
                amortization()
                #amortization_schedule = generate_amortization_schedule(PV,n,r)
            elif selection == 6:
                print("Option 6: Exit the program.")
                is_valid = True
            elif selection == 0:
                menu_screen()
            else:
                print("That is a not a valid option. Please type in a number between 1 - 4.")
        except ValueError:
            print("That is not a valid input. Please type in a number betwee 1 - 14.")    


# Code from https://sidhanthk9.medium.com/how-to-code-an-amortization-schedule-in-python-e2d2b417c61a
def calculate_monthly_payments(PV,n,r):
    monthly_payment = round(((r / 100 / 12) * PV) / (1 - (math.pow((1 + (r / 100 / 12)), (-n*12)))), 2)
    return monthly_payment
    #output= (PV*r)/(((1/(1+r)**n))-1)  # formula calculated using sum of infinite GP series
    #return output


# Code from https://sidhanthk9.medium.com/how-to-code-an-amortization-schedule-in-python-e2d2b417c61a
def generate_amortization_schedule(PV,n,r):
    schedule = []
    balance = PV
    rate = r/100/12
    total_payments = n*12
    monthly_payment = calculate_monthly_payments(PV,n,r)
    for Month in range(1,total_payments):
        interest_payment = balance * rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        total_payments -= 1
        schedule.append({
                'Month #' : Month,
                'Payments Left' : total_payments,
                'Payment' : "€{:,.2f}".format(monthly_payment),
                'Principal' : "€{:,.2f}".format(principal_payment),
                'Interest' : "€{:,.2f}".format(interest_payment),
                'Balance' : "€{:,.2f}".format(balance)     
            })

    return pd.DataFrame(schedule) 


if __name__ == '__main__':
    # PV=350000
    # n=19
    # r=4.3
    # amortization_schedule = generate_amortization_schedule(PV,n,r)

    # print(amortization_schedule)
    welcome_screen()
    menu_screen()
    run_mortgage_tool()
    #print(f"Mort_dict: {mort_dict}")
    




