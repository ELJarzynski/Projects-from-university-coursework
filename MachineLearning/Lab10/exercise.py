from Lab08.main import *


precision = TP / (TP + FP)
sensitivity = TP / (TP + FN)
specificity = TN / (TN + FP)
global_accuracy = (TP + TN) / (TN + FP + FN + TP)
print(f'Precision: {precision}, sensitivity: {sensitivity}, specificity: {specificity}, accuracy {global_accuracy}')
