import tkinter as tk
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use('TkAgg')


class Loan:
    def __init__(self, interest=5.99, principle=15559.99, term=60, payment_frequency="monthly"):
        self.interest = interest
        self.principle = principle
        self.term = term
        self.payment_frequency = payment_frequency

    def get_interest_percent_to_float(self):
        return self.interest / 100

    def get_interest_per_period(self):
        # Use of dictionary makes for cleaner code and easy readability
        interest = self.get_interest_percent_to_float()
        return {
            "monthly": interest / 12,
            "biweekly": interest / (365 / 14),
            "weekly": interest / (365 / 7),
            "daily": interest / 365
        }[self.payment_frequency]

    def get_payments_per_period(self):
        i = self.get_interest_per_period()
        p = self.principle
        t = self.term
        period_payments = p * ((i * (1 + i) ** t) / (((1 + i) ** t) - 1))
        return period_payments

    def get_total_interest_to_be_paid(self):
        principle = self.principle
        term = list(range(self.term))

        i = self.get_interest_per_period()
        p = self.get_payments_per_period()

        total_interest_paid = 0
        for t in term:
            interest_paid_this_period = i*principle
            principle -= (p-interest_paid_this_period)
            total_interest_paid += interest_paid_this_period
        return total_interest_paid

    def get_payment_schedule(self):
        principle = self.principle
        term = list(range(self.term))

        i = self.get_interest_per_period()
        p = self.get_payments_per_period()

        payments = []
        for t in term:
            payments.append({
                "#": t,
                "total_payment": p,
                "amount_toward_principle": i*principle,
                "amount_toward_interest": p-(i*principle),
                "remaining_principle": principle - (p-(i*principle))
            })
            principle -= (p-(i*principle))

        return payments

    def get_total_to_be_paid_on_loan(self):
        return self.principle + self.get_total_interest_to_be_paid()


class Window:
    def __init__(self, window):
        self.window = window
        self.window.title = "Loan Calculator"
        


loan = Loan()

print("percent to float:", loan.get_interest_percent_to_float())

periods = ["monthly", "biweekly", "weekly", "daily"]

for period in periods:
    loan_test = Loan(payment_frequency=period)
    print("\nperiod:", period)
    print("interest_per_period:", loan_test.get_interest_per_period())
    print("payment_per_period:", loan_test.get_payments_per_period())

count = 0
list1 = list(range(60))
for li in list1:
    count += 1

print(list)
print(count)

print(loan.get_total_interest_to_be_paid())

schedule = loan.get_payment_schedule()
for sch in schedule:
    print(sch)

# root = tk.Tk()
# start = Window(root)
# root.mainloop()
