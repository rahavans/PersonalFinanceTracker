# Personal Finance Tracker

Hi! This is a project I am working on, that I hope to eventually transform into a full-stack application, utilizing a unique front-end, Flask backend, and SQL database. However, this is the blueprint I have set out.

I used Python's Tkinter GUI to simulate a personal finance tracker for the month, that allows users to track their expenditures across their income. Spendings are divided into several default categories, with the option for a custom category as well. In addition, the tracker can get exported to an Excel file as well, for filing purposes. The project's purpose is to promote saving by tracking expenses, and budgetting across the month.

Right now, this project can be converted into an executable desktop application using Pyinstaller, to see its performance and interact with the application.

The terminal command is as follows:

pyinstaller  --onefile --windowed --name MyFinanceTracker personalfinancetracker.py

This will save an executable in the working directory in the "dist" folder under the name "MyFinanceTracker.exe". You can rename the program by changing the MyFinanceTracker parameter in the terminal command. Now, by opening the application, it is ready for use!

