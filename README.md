# Loan-Calculator

 App to calculate interest and principle amounts of a loan
 
 Python version: 3.8.7

 TkInter is used to create the graphical user interface
 
  ## Sample:
  
  ![alt text](https://github.com/RasbeeTech/Loan-Calculator/blob/main/sample_image.jpeg)
  
  To see finished program code, click [here](https://github.com/RasbeeTech/Loan-Calculator/blob/main/loan_calculator.py)
  
  ## Process:
  1. Create a class object for loan calculations
  ```python
  class Loan:
  	# defined default variables for testing
    def __init__(self, interest=5.99, principle=15559.99, term=60, payment_frequency="monthly"):
        self.interest = interest
        self.principle = principle
        self.term = term
        self.payment_frequency = payment_frequency
  ```
  2. Create Loan class function to calculate interest based on payment/amortization frequency
  ```python
  def get_interest_percent_to_float(self):
  	# converts percentage(%) to a float(decimal) number 
  	return self.interest / 100
  
  def get_interest_per_period(self):
  	# returns the amount of interest calculated
  	# Use of dictionary makes for cleaner code and easy readability
    interest = self.get_interest_percent_to_float()
    return {
        "monthly": interest / 12,
        "biweekly": interest / (365 / 14),
        "weekly": interest / (365 / 7),
        "daily": interest / 365
    }[self.payment_frequency]
  ```
  3. Create function to calculate the amount to be paid per period
  		1. The following formula is used:
  		![alt text](https://github.com/RasbeeTech/Loan-Calculator/blob/main/loan_payment_formula.jpeg)
  		2.  Formula to code:
  ```python
  def get_payments_per_period(self):
	i = self.get_interest_per_period()
    p = self.principle
    t = self.term
    # using formula to calculate payments per period
    period_payments = p * ((i * (1 + i) ** t) / (((1 + i) ** t) - 1))
    return period_payments
  ```
  3.
  ```python
  
  ```
