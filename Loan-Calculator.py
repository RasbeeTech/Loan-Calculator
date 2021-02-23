loan_interest = 5.99
loan_principle = 15559.99
months = 60
# interest-only loans: payments go to interest for first few years before and nothing on principle
# amortized loans: include both principle and interest paid over the term
amortized = True


# Formula: Loan Payment(p) = Amount(a) / Discount Factor(d)
# Calculate monthly payment amount
def amortized_calculated(total_loan_amount, interest_rate, number_of_payments):
    a = total_loan_amount
    n = number_of_payments
    if interest_rate > 1:
        r = interest_rate / 100
        r /= 12
    print("Loan:", a)
    print("Payments:", n)
    print("Interest:", r)

    l = r + 1
    q = l ** n

    m = l ** n

    t = m * r

    print("n:", n)
    print("r:", r)
    print("l:", l)
    print("q:", q)
    print("m:", m)
    print("t:", t)

    final = q / t
    print("final:", final)

    d = ((1 + r) ** n) / (r * (1 + r) ** n)
    print("Discount:", d)
    #monthly payments:
    lp = a * ((r*(1+r)**n)/(((1+r)**n)-1))
    print("monthly:",round(lp,2))

    print("total",round((lp*n)))
    p = a / d
    print("payment:", p)


if __name__ == '__main__':
    print("Loan Calculator\n")
    amortized_calculated(loan_principle, loan_interest, months)
