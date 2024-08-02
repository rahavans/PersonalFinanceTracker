import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
from openpyxl import Workbook

class PersonalFinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")

        # Create and set up the DataFrame
        self.df = pd.DataFrame(columns=["Date", "Type", "Description", "Amount"])
        self.total_income = 0.0

        # Expense types
        self.expense_types = ["Groceries", "Utilities", "Rent", "Entertainment", "Other"]

        # Create widgets
        self.date_label = ttk.Label(root, text="Date:")
        self.date_entry = ttk.Entry(root)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # default to current date

        self.type_label = ttk.Label(root, text="Type:")
        self.type_var = tk.StringVar()
        self.type_combobox = ttk.Combobox(root, textvariable=self.type_var, values=self.expense_types, state="readonly")
        self.type_combobox.bind("<<ComboboxSelected>>", self.on_type_selected)

        self.description_label = ttk.Label(root, text="Description:")
        self.description_entry = ttk.Entry(root)

        self.amount_label = ttk.Label(root, text="Amount:")
        self.amount_entry = ttk.Entry(root)

        self.other_type_label = ttk.Label(root, text="Other Type:")
        self.other_type_entry = ttk.Entry(root)
        self.other_type_entry.grid_remove()

        self.add_button = ttk.Button(root, text="Add Entry", command=self.add_entry)

        self.tree = ttk.Treeview(root, columns=["Date", "Type", "Description", "Amount"], show="headings")

        for col in ["Date", "Type", "Description", "Amount"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)

        self.total_label = ttk.Label(root, text="Total Expenses: $0.00")

        self.income_label = ttk.Label(root, text="Enter Income:")
        self.income_entry = ttk.Entry(root)

        self.add_income_button = ttk.Button(root, text="Add Income", command=self.add_income)

        self.total_income_label = ttk.Label(root, text="Total Income: $0.00")

        self.budget_left_label = ttk.Label(root, text="Budget Left: $0.00")

        self.clear_all_button = ttk.Button(root, text="Clear All", command=self.clear_all)
        self.delete_expense_button = ttk.Button(root, text="Delete Expense", command=self.delete_selected_expense)

        self.export_button = ttk.Button(root, text="Export to Excel", command=self.make_excel)

        # Grid layout
        self.date_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        self.type_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
        self.type_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.description_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        self.amount_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)

        self.other_type_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
        self.other_type_entry.grid(row=4, column=1, padx=5, pady=5)

        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.tree.grid(row=6, column=0, columnspan=6, pady=10, sticky="nsew")

        self.total_label.grid(row=7, column=0, columnspan=2, pady=5)

        self.income_label.grid(row=0, column=2, padx=5, pady=5, sticky="E")
        self.income_entry.grid(row=0, column=3, padx=5, pady=5)

        self.add_income_button.grid(row=1, column=2, columnspan=2, pady=10)

        self.total_income_label.grid(row=2, column=2, columnspan=2, pady=5, sticky="E")

        self.budget_left_label.grid(row=3, column=2, columnspan=2, pady=5, sticky="E")

        self.clear_all_button.grid(row=10, column=2, pady=10)
        self.delete_expense_button.grid(row=8, column=3, pady=10)

        self.export_button.grid(row=8, column=0, columnspan=6, pady=10)

        # Column weight to allow resizing
        for i in range(6):
            self.root.grid_columnconfigure(i, weight=1)

        # Row weight to allow resizing
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)

    def add_entry(self):
        date = self.date_entry.get()
        entry_type = self.type_var.get()

        if entry_type == "Other":
            entry_type = self.other_type_entry.get()

        description = self.description_entry.get()
        amount = float(self.amount_entry.get())

        new_data = pd.DataFrame({"Date": [date], "Type": [entry_type], "Description": [description], "Amount": [amount]})
        self.df = pd.concat([self.df, new_data], ignore_index=True)

        self.update_table()

    def add_income(self):
        income = float(self.income_entry.get())
        self.total_income += income
        self.income_entry.delete(0, tk.END)
        self.update_income_display()

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        total_expenses = 0.0

        for index, row in self.df.iterrows():
            values = (row["Date"], row["Type"], row["Description"], "${:.2f}".format(row["Amount"]))
            self.tree.insert("", index, values=values)

            total_expenses += row["Amount"]

        self.total_label.config(text="Total Expenses: ${:.2f}".format(total_expenses))
        self.update_budget_display()

    def update_income_display(self):
        self.total_income_label.config(text="Total Income: ${:.2f}".format(self.total_income))
        self.update_budget_display()

    def update_budget_display(self):
        budget_left = self.total_income - self.df["Amount"].sum()
        self.budget_left_label.config(text="Budget Left: ${:.2f}".format(budget_left))

    def on_type_selected(self, event):
        selected_type = self.type_var.get()

        if selected_type == "Other":
            self.other_type_entry.grid(row=4, column=1, padx=5, pady=5)
        else:
            self.other_type_entry.grid_remove()

    def clear_all(self):
        self.df = pd.DataFrame(columns=["Date", "Type", "Description", "Amount"])
        self.total_income = 0.0
        self.update_table()

    def delete_selected_expense(self):
        selected_items = self.tree.selection()

        for item in selected_items:
            index = int(item[1:], 16) - 1  # Extract index from item ID
            self.df = self.df.drop(index)

        self.df.reset_index(drop=True, inplace=True)
        self.update_table()

    def make_excel(self):
        excel_filename = "finance_tracker_export.xlsx"
        self.df.to_excel(excel_filename, index=False)
        messagebox.showinfo("Export Successful", f"Data exported to {excel_filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalFinanceTracker(root)
    root.mainloop()
