import tkinter as tk

loan_interest = 5.99
loan_principle = 15559.99
months = 60
# interest-only loans: payments go to interest for first few years before and nothing on principle
# amortized loans: include both principle and interest paid over the term
amortized = True


# Formula: Loan Payment(p) = Amount(a) / Discount Factor(d)
# Calculate monthly payment amount
def interest_only_calculated(total_loan_amount=loan_principle, interest_rate=loan_interest, number_of_payments=months):
    a = total_loan_amount
    n = number_of_payments
    r = interest_rate
    print("Interest Only:")
    monthly_payments = a * (r / n)
    print("Monthly:", monthly_payments)


def amortized_calculated(total_loan_amount, interest_rate, number_of_payments):
    a = total_loan_amount
    n = number_of_payments
    if interest_rate > 1:
        r = interest_rate / 100
        r /= 12
    print("Amortized\n")
    print("Loan:", a)
    print("Payments:", n)
    print("Interest:", interest_rate, "%")

    # monthly payments:
    monthly_payments = a * ((r * (1 + r) ** n) / (((1 + r) ** n) - 1))
    print("monthly: $", round(monthly_payments, 2))

    print("total interest: $", round(((monthly_payments * n) - a), 2))
    print("total: $", round((monthly_payments * n)))


if __name__ == '__main__':
    print("Loan Calculator\n")
    amortized_calculated(loan_principle, loan_interest, months)

    window = tk.Tk()
    window.title("Loan Calculator")

    # labels
    label_loan_amount = tk.Label(text="Loan Amount($):").grid(row=0, column=0)
    label_interest = tk.Label(text="Interest Rate(%):").grid(row=1, column=0)
    label_num_payments = tk.Label(text="Length(months):").grid(row=2, column=0)

    # entries
    entry_loan_amount = tk.Entry(bd=3)
    entry_loan_amount.insert(index=tk.END, string=str(loan_principle))
    entry_interest = tk.Entry(bd=3)
    entry_interest.insert(index=tk.END, string=str(loan_interest))
    entry_num_payments = tk.Entry(bd=3)
    entry_num_payments.insert(index=tk.END, string=str(months))

    entry_loan_amount.grid(row=0, column=1)
    entry_interest.grid(row=1, column=1)
    entry_num_payments.grid(row=2, column=1)

    # Calculate button
    btn_calculate = tk.Button(text="Calculate", command=lambda: amortized_calculated(loan_principle, loan_interest, months))
    btn_calculate.grid(columnspan=2, row=3, column=0, pady=20)
    window.mainloop()
