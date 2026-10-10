"""

#  Google Pay-Inspired Expense Sharing System

##  Project Overview

The **Expense Sharing System** is a Python-based application developed to help friends manage shared expenses and calculate who owes whom.

The system is inspired by the expense-sharing concept used in digital payment applications such as Google Pay.

When a group of friends shares expenses such as accommodation, food, transportation, or fuel, different people may pay different amounts. This application records those expenses, calculates each participant's share, maintains individual balances, and generates the final settlement.

The project also includes basic **Data Science concepts** using **Pandas** for data handling and **Matplotlib** for expense visualization.

---

##  Problem Statement

In group activities, one person may pay the complete amount for an expense while the expense is shared among multiple people.

For example:

- Rasi pays ₹900 for accommodation.
- Ashmi pays ₹300 for meals.
- Sree pays ₹200 for fuel.

Manually calculating the individual shares and determining who owes whom can be difficult.

This project automates the calculation and provides a clear settlement between group members.

---

##  Objectives

The main objectives of this project are:

- To record expenses made by different users.
- To divide expenses equally among selected participants.
- To calculate individual balances.
- To identify debtors and creditors.
- To determine who owes whom.
- To analyze total contributions using Pandas.
- To visualize spending patterns using a bar chart.
- To reduce manual calculation errors.

---

"""

# --> Business use case: Friends want to easily track shared expenses and settle debts using a simple tool similar to Google Pay.
"""
--> Description: Create a Python program that helps friends manage shared expenses and calculate who owes whom.
Suppose there are three friends-Alice, Bob, and Carol. They went on a trip and shared expenses for accommodation
and meals. The program will allow them to input these expenses, calculate how much each person needs to pay or be
reimbursed, and display the final settlement amounts.

"""
import pandas as pd
import matplotlib.pyplot as plt
class ExpenseSharing:
    def __init__(self,friends): # constructor - when ever we call the class it will call by itself
        self.friends = friends
        self.expenses = {friend: 0 for friend in friends} # stores the expenses of the friend from 0
        self.expense_data = []
    def add_expense(self, payer,amount,participants):
        split_amount = amount / len(participants)
        for participant in participants:
            if participant != payer:
                self.expenses[participant] += split_amount
                self.expenses[payer] -= split_amount
        self.expense_data.append({"Payer": payer, "Amount": amount})
    def calculate_settlement(self):
        for friend, balance in self.expenses.items():
            if balance > 0:
                print(f"{friend} needs to be reimbursed: Rs.{balance:.2f}")
            elif balance < 0:
                print(f"{friend} owes: Rs.{-balance:.2f}")
            else:
                print(f"{friend} is settled up.")

    def show_bar_chart(self):
        df = pd.DataFrame(self.expense_data)
        if df.empty:
            print("No expenses available.")
            return
        # Calculate total amount paid by each person
        total_paid = (df.groupby("Payer")["Amount"].sum())
        print("\n ======== Expense Summary ========")
        print(total_paid)
        # Create bar chart
        plt.figure(figsize=(8, 5))

        total_paid.plot(kind="bar")
        plt.title("Total Amount Paid by Each Person")
        plt.xlabel("Person")
        plt.ylabel("Amount Paid (Rs.)")
        # Keep names horizontal
        plt.xticks(rotation=0)

        # Display values on top of bars
        for index, value in enumerate(total_paid):
            plt.text(index,value,f"Rs.{value:.0f}",ha="center",va="bottom")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    friends = ["Rasi", "Ashmi", "Sree"]
    expense_sharing = ExpenseSharing(friends)

    # Add some sample expenses:
    expense_sharing.add_expense("Rasi", 900, ["Rasi", "Ashmi", "Sree"]) # paid for accomodation
    expense_sharing.add_expense("Ashmi", 300, ["Rasi", "Ashmi", "Sree"]) # paid for meals
    expense_sharing.add_expense("Sree", 200, ["Rasi", "Sree"]) # paid for fuel

    # calculate settlement:
    print("\n Final settlement")
    expense_sharing.calculate_settlement()

    print("\nGenerating expense visualization...")
    expense_sharing.show_bar_chart()
"""
Explanations: 

Rasi: Rs. 900 - 300 = Rs. 600(Alice needs to be reimbursed Rs.600)
    Ashmi: Rs. 0 - 300 = Rs. -300 (negative balance, Bob owes Rs.300)
    Sree: Rs. 0 -300 (negative balance carol owes Rs. 300)
Ashmi: Rs. 300 - 100 = 200
    Rasi: Rs: 600 - Rs 100 = Rs. 500
    Ashmi: -Rs 300 + Rs 200 = Rs. -100
    Sree: -Rs. 300 - 100 = Rs. -400
Sree: Rs. 200 - 100 = 100
    Rasi: Rs 500 - 100 = 400
    Ashmi: -100
    Sree: -400 + 100 = -300

"""
# Who Owes Who
class ExpenseSharing:
    def __init__(self,friends): # constructor - when ever we call the class it will call by itself
        self.friends = friends
        self.balances = {friend: 0 for friend in friends} # stores the expenses of the friend from 0
        self.balances_data = []
    def add_expense(self, payer,amount,participants):
        split_amount = amount / len(participants)
        for participant in participants:
            self.balances[participant] -= split_amount
        self.balances[payer] += amount
        self.balances_data.append({"Payer": payer, "Amount": amount})
    def calculate_settlement(self):
        creditors = []
        debtors = []
        for friend, balance in self.balances.items():
            if balance > 0:
                creditors.append((friend,balance))
            elif balance < 0:
                debtors.append((friend, -balance))
        while debtors and creditors:
            debtor, debt_amount = debtors.pop()
            creditor, credit_amount = creditors.pop()
            payment = min(debt_amount, credit_amount)
            print(f"{debtor} owes {creditor}: Rs.{payment:.2f}")

            if debt_amount > payment:
                debtors.append((debtor,debt_amount - payment))
            if credit_amount > payment:
                creditors.append((creditor,credit_amount - payment))

    def show_bar_chart(self):
        df = pd.DataFrame(self.balances_data)
        if df.empty:
            print("No expenses available.")
            return
        # Calculate total amount paid by each person
        total_paid = (df.groupby("Payer")["Amount"].sum())
        print("\n ======== Expense Summary ========")
        print(total_paid)
        # Create bar chart
        plt.figure(figsize=(8, 5))

        total_paid.plot(kind="bar")
        plt.title("Total Amount Paid by Each Person")
        plt.xlabel("Person")
        plt.ylabel("Amount Paid (Rs.)")
        # Keep names horizontal
        plt.xticks(rotation=0)

        # Display values on top of bars
        for index, value in enumerate(total_paid):
            plt.text(index,value,f"Rs.{value:.0f}",ha="center",va="bottom")
        plt.tight_layout()
        plt.show()

# if __name__ == "__main__":
#     friends = ["Rasi", "Ashmi", "Sree"]
#     expense_sharing = ExpenseSharing(friends)
#
#     # Add some sample expenses:
#     expense_sharing.add_expense("Rasi", 900, ["Rasi", "Ashmi", "Sree"]) # paid for accomodation
#     expense_sharing.add_expense("Ashmi", 300, ["Rasi", "Ashmi", "Sree"]) # paid for meals
#     expense_sharing.add_expense("Sree", 200, ["Rasi", "Sree"]) # paid for fuel
#
#
#     # calculate settlement:
#     print("\n Final settlement")
#     expense_sharing.calculate_settlement()

if __name__ == "__main__":
    friends = input("Enter friends: ").split(",")
    friends = [friend.strip() for friend in friends]
    expense_sharing = ExpenseSharing(friends)
    while True:
        payer = input("Enter the name of the person who paid (of 'done' to finish): ")
        if payer.lower() == "done":
            break
        amount = float(input("Enter the amount paid: "))
        participants = input("Enter participants: ").split(",")
        participants = [participant.strip() for participant in participants]
        expense_sharing.add_expense(payer, amount, participants)
    print("\n Final settlement")
    expense_sharing.calculate_settlement()

    print("\nGenerating expense visualization...")
    expense_sharing.show_bar_chart()