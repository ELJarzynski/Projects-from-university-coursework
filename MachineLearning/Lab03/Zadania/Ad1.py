import pandas as pd
"""File lanching"""
file_directory: str = r"C:\Users\kamil\Desktop\Studia\Semestr VI\MachinLearning\Auta.csv"
cars = pd.read_csv(file_directory)

"""Display of terminal setup"""
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

