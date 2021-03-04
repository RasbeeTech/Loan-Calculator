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
            interest_paid_this_period = i * principle
            principle -= (p - interest_paid_this_period)
            total_interest_paid += interest_paid_this_period
        return total_interest_paid

    def get_payment_schedule(self):
        principle = self.principle
        term = list(range(self.term))

        i = self.get_interest_per_period()
        p = self.get_payments_per_period()

        payments = []
        total_interest_paid = 0
        for t in term:
            payments.append({
                "#": t,
                "total_payment": p,
                "amount_toward_principle": p - (i * principle),
                "amount_toward_interest": i * principle,
                "remaining_principle": principle - (p - (i * principle)),
                "total_paid": p * (t + 1),
                "total_interest_paid": total_interest_paid + (i * principle)
            })
            total_interest_paid += i * principle
            principle -= (p - (i * principle))

        return payments

    def get_total_to_be_paid_on_loan(self):
        return self.principle + self.get_total_interest_to_be_paid()

    def update(self, interest=5.99, principle=15559.99, term=60, payment_frequency="monthly"):
        self.interest = interest
        self.principle = principle
        self.term = term
        self.payment_frequency = payment_frequency


class Window:
    def __init__(self, window):
        self.window = window
        self.loan = Loan()

        self.input_labels = ["Principle ($)", "Interest (%)", "Term Length", "Frequency"]
        self.output_labels = ["Total Interest", "Total repaid", "Pay/Period"]
        self.frequency_options = ["yearly", "monthly", "biweekly", "weekly", "daily"]
        self.menuVar = tk.StringVar(self.window)
        self.data_input = {}
        self.data_output = {}

        self.setup_gui()
        self.set_gui_default_values()
        self.graph = self.setup_graph()

    def setup_gui(self):
        # input labels
        input_labels = self.input_labels
        for label in input_labels:
            row = input_labels.index(label)
            tk_label = tk.Label(text=label, font="Helvetica 15 bold")
            tk_label.grid(row=row, column=0)

            if label == "Frequency":
                choices = self.frequency_options
                input = tk.OptionMenu(self.window, self.menuVar, *choices)
                input.grid(row=row, column=1, pady=5, sticky="nesw")
            else:
                input = tk.Entry(bd=3, width=20, justify="center")
                input.grid(row=row, column=1, pady=5)
            self.data_input[label] = input

        calculate_button = tk.Button(text="Calculate", font="Helvetica 15 bold", command=self.calculate_button)
        calculate_button.grid(row=len(input_labels), column=0, columnspan=2, pady=20)

        # output labels
        output_labels = self.output_labels
        for label in output_labels:
            row = len(input_labels) + output_labels.index(label) + 1
            tk_label = tk.Label(text=label, font="Helvetica 15 bold")
            tk_label.grid(row=row, column=0)

            output = tk.Label(text="", font="Helvetica 15 bold", width="20", bg="#d3d3d3", bd=3, relief="ridge")
            output.grid(row=row, column=1, pady=5)
            self.data_output[label] = output

        view_button = tk.Button(text="View payment schedule", font="Helvetica 15 bold",
                                command=self.view_payment_schedule_button)
        view_button.grid(row=len(output_labels) + len(input_labels) + 1, column=0, columnspan=2, pady=20)

    def set_gui_default_values(self):
        default_principle = self.loan.principle
        default_interest = self.loan.interest
        default_term = self.loan.term

        self.data_input["Principle ($)"].insert(index=tk.END, string=str(default_principle))
        self.data_input["Interest (%)"].insert(index=tk.END, string=str(default_interest))
        self.data_input["Term Length"].insert(index=tk.END, string=str(default_term))
        self.menuVar.set(self.frequency_options[1])

        default_interest_to_be_paid = round(self.loan.get_total_interest_to_be_paid(), 2)
        default_total_to_be_paid = round(self.loan.get_total_to_be_paid_on_loan(), 2)
        default_pay_per_period = round(self.loan.get_payments_per_period(), 2)
        self.data_output["Total Interest"].config(text="$" + str(default_interest_to_be_paid))
        self.data_output["Total repaid"].config(text="$" + str(default_total_to_be_paid))
        self.data_output["Pay/Period"].config(text="$" + str(default_pay_per_period))

    def calculate_button(self):
        new_principle = self.data_input["Principle ($)"].get()
        new_interest = self.data_input["Interest (%)"].get()
        new_term = self.data_input["Term Length"].get()
        new_frequency = self.menuVar.get()
        self.loan.update(principle=float(new_principle),
                         interest=float(new_interest),
                         term=int(new_term),
                         payment_frequency=new_frequency)
        self.data_output["Total Interest"].config(text="$" + str(round(self.loan.get_total_interest_to_be_paid(), 2)))
        self.data_output["Total repaid"].config(text="$" + str(round(self.loan.get_total_to_be_paid_on_loan(), 2)))
        self.data_output["Pay/Period"].config(text="$" + str(round(self.loan.get_payments_per_period(), 2)))
        self.update_graph()

    def view_payment_schedule_button(self):
        schedule_window = tk.Toplevel(self.window)
        payment_schedule = self.loan.get_payment_schedule()

        header = ["#", "payment", "interest", "principle"]
        for head in header:
            label = tk.Label(schedule_window, text=head)
            label.grid(row=0, column=header.index(head))

        for payment in payment_schedule:
            label_num = tk.Label(schedule_window, text=payment.get("#") + 1).grid(row=payment.get("#") + 1, column=0)
            label_pay = tk.Label(schedule_window, text=payment.get("total_payment") + 1).grid(
                row=payment.get("total_payment") + 1, column=1)
            label_interest = tk.Label(schedule_window, text=payment.get("amount_toward_interest") + 1).grid(
                row=payment.get("amount_toward_interest") + 1, column=2)
            label_principle = tk.Label(schedule_window, text=payment.get("remaining_principle") + 1).grid(
                row=payment.get("remaining_principle") + 1, column=3)

    def setup_graph(self):
        x_period, y_principle_paid, y_interest_paid, y_remaining_balance = self.get_plot_points()
        width = 0.3
        x = np.array(x_period)
        y1 = np.array(y_principle_paid)
        y2 = np.array(y_interest_paid)
        y3 = np.array(y_remaining_balance)

        figure = Figure(figsize=(9, 5))
        fig = figure.add_subplot(111)

        fig.bar(x, y1, width, label="Total paid", color="orange")
        fig.bar(x + width, y2, width, label="Interest paid", color="blue")
        fig.bar(x + width * 2, y3, width, label="Balance remaining", color="purple")

        fig.set_title("Loan Calculator", fontsize=16)
        fig.set_ylabel("Amount ($)", fontsize=14)
        fig.set_xlabel("Year", fontsize=14)
        fig.legend()

        canvas = FigureCanvasTkAgg(figure, master=self.window)
        canvas.get_tk_widget().grid(columnspan=10, rowspan=10, row=0, column=2)
        canvas.draw()
        return fig

    def get_plot_points(self):
        points = self.loan.term / 12
        x_period = list(range(1, (int(points) + 1)))

        schedule = self.loan.get_payment_schedule()[11::12]

        y_interest_paid = []
        y_principle_paid = []
        y_remaining_balance = []

        for s in schedule:
            y_interest_paid.append(s.get("total_interest_paid"))
            y_principle_paid.append(s.get("total_paid"))
            y_remaining_balance.append(s.get("remaining_principle"))

        return x_period, y_principle_paid, y_interest_paid, y_remaining_balance

    def update_graph(self):
        self.graph.clear()
        self.graph = self.setup_graph()


root = tk.Tk()
start = Window(root)
root.mainloop()
