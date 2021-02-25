# pip install matplotlib
import tkinter as tk
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use('TkAgg')


class Loan:
    def __init__(self, interest, principle, payment_type, term):
        self.loan_interest = interest/12/100
        self.loan_principle = principle
        self.months = term
        if payment_type == "monthly":
            self.months = term
        #interest_rate = interest / 100
        self.monthly_payments = principle * (
                    (self.loan_interest * (1 + self.loan_interest) ** term) / (((1 + self.loan_interest) ** term) - 1))
        self.loan_total = self.monthly_payments * term
        amortized = True
        self.print_attributes()

    def print_attributes(self):
        print("Loan")
        print("Principle: ", self.loan_principle)
        print("Interest: ", self.loan_interest)
        print("Total: ", self.loan_total)
        print("Monthly: ", self.monthly_payments)

    def get_amount_paid(self):
        m_payment = self.monthly_payments
        m_principle = self.loan_principle
        count_x = self.months
        interest_paid = 0
        count_y = 0
        payments = []
        while count_x > count_y:
            payments.append(
                {
                    "#": count_y,
                    "paid": round(m_payment, 2),
                    "total_paid": round(m_payment*(count_y+1), 2),
                    "interest": round((self.loan_interest * m_principle)+interest_paid,2),
                    "toward_principle": round(m_payment-(self.loan_interest * m_principle), 2),
                    "principle": round(m_principle-m_payment, 2)
                }
            )
            interest_paid += (self.loan_interest * m_principle)
            m_principle -= (m_payment - (m_principle * self.loan_interest))
            if m_payment > m_principle:
                m_payment = m_principle+(m_principle*self.loan_interest)
            count_y += 1
        for i in payments:
            print(i)



def plot_graph():
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    v = np.array([16, 16.31925, 17.6394, 16.003, 17.2861, 17.3131, 19.1259, 18.9694, 22.0003, 22.81226])
    p = np.array([1, 16.23697, 17.31653, 17.22094, 17.68631, 17.73641, 18.6368,
                  19.32125, 19.31756, 21.20247, 22.41444, 22.11718, 22.12453])

    fig = Figure(figsize=(5, 5))
    a = fig.add_subplot(111)
    # a.scatter(v, x, color='red')
    a.plot(range(2 + max(x)), p, color='red')
    # a.invert_yaxis()

    a.set_title("Loan Calculator", fontsize=16)
    a.set_ylabel("Amount ($)", fontsize=14)
    a.set_xlabel("Year", fontsize=14)

    return fig


def get_plot_points(obj):
    # Get x values
    points = obj.months / 12
    x = []
    while points > 0:
        x.insert(0, points)
        points -= 1
    print(x)

    # Get y values
    points = obj.loan_total
    point = obj.loan_total / len(x)
    y = []
    count = len(x)
    # while points > 0:
    #   y.append(points-(point*))
    print(y)


if __name__ == '__main__':
    print("Loan Calculator\n")
    # amortized_calculated(loan_principle, loan_interest, months)
    loan = Loan(interest=5.99, principle=15559.99, payment_type="monthly,", term=60)
    window = tk.Tk()
    window.title("Loan Calculator")

    plot = plot_graph()

    # labels
    label_loan_amount = tk.Label(text="Loan Amount($):", font="Helvetica 13 bold").grid(row=0, column=0)
    label_interest = tk.Label(text="Interest Rate(%):", font="Helvetica 13 bold").grid(row=1, column=0)
    label_num_payments = tk.Label(text="Length(months):", font="Helvetica 13 bold").grid(row=2, column=0)

    # entries
    entry_loan_amount = tk.Entry(bd=3)
    entry_loan_amount.insert(index=tk.END, string=str(loan.loan_principle))
    entry_interest = tk.Entry(bd=3)
    entry_interest.insert(index=tk.END, string=str(loan.loan_interest))
    entry_num_payments = tk.Entry(bd=3)
    entry_num_payments.insert(index=tk.END, string=str(loan.months))

    entry_loan_amount.grid(row=0, column=1)
    entry_interest.grid(row=1, column=1)
    entry_num_payments.grid(row=2, column=1)

    # Calculate button
    btn_calculate = tk.Button(text="Calculate",
                              font="Helvetica 15 bold",
                              # command=lambda: amortized_calculated(loan.loan_principle,
                              #                                     loan.loan_interest,
                              #                                     loan.months)
                              )
    btn_calculate.grid(columnspan=2, row=3, column=0, pady=20)

    # place plot graph in tkinter window
    plot_graph = plot_graph()
    canvas = FigureCanvasTkAgg(plot_graph, master=window)
    canvas.get_tk_widget().grid(columnspan=30, rowspan=30, row=0, column=3)
    canvas.draw()

    get_plot_points(loan)
    loan.get_amount_paid()
    window.mainloop()
