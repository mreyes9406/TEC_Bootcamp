import os
import csv
import statistics as stats

PyBank_csv = os.path.join( 'budget_data.csv' )

with open(PyBank_csv, newline = '') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    csv_header = next(csv_file)

    months = []
    PnL = []
    for row in csv_reader:
        months.append(row[0])
        PnL.append(int(row[1])) 
    
    PnL_aux_1 = PnL.copy()
    PnL_aux_2 = PnL.copy()
    months_aux = months.copy()
    PnL_aux_2.pop(0)
    PnL_aux_1.pop()
    months_aux.pop(0)

    monthly_dif = [x - y for x, y in zip(PnL_aux_2, PnL_aux_1)]
    monthly_dif_dict = {x:y for x, y in zip(months_aux, monthly_dif)}
    gr_in_prof = max(monthly_dif_dict, key = monthly_dif_dict.get)
    gr_dec_prof = min(monthly_dif_dict, key = monthly_dif_dict.get)

print('Financial Analysis')
print('---------------------------------------------')
print('Total months: ' + str(len(months)))
print('Total: $' + str(sum(PnL)))
print('Average Change: $' + str(round(stats.mean(monthly_dif),2)))
print('Greatest Increase in Profits: ' + str(gr_in_prof) + ' ' + '($' + str(monthly_dif_dict[gr_in_prof]) + ')')
print('Greatest Decrease in Profits: ' + str(gr_dec_prof) + ' ' + '($' + str(monthly_dif_dict[gr_dec_prof]) + ')')