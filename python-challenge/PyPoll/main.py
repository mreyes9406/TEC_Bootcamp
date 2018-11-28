import os
import csv
import statistics as stats

PyPoll_csv = os.path.join('election_data.csv')

with open(PyPoll_csv, newline = '') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    csv_header = next(csv_file)

    voter_id = []
    county = []
    candidate = []
    for row in csv_reader:
        voter_id.append(str(row[0]))
        county.append(str(row[1]))
        candidate.append(str(row[2]))
    
    khan_occur = [vote for vote in candidate if vote == 'Khan']
    khan_pct = len(khan_occur) * 100 /len(voter_id) 
    correy_occur = [vote for vote in candidate if vote == 'Correy'] 
    correy_pct = len(correy_occur) * 100/len(voter_id)
    li_occur = [vote for vote in candidate if vote == 'Li'] 
    li_pct = len(li_occur) * 100/len(voter_id)
    otooley_occur = [vote for vote in candidate if vote == "O'Tooley"] 
    otooley_pct = len(otooley_occur) * 100/len(voter_id)
    percents = {'Khan':khan_pct, 'Correy':correy_pct, 'Li':li_pct, "O'Tooley":otooley_pct}
    winner = max(percents, key = percents.get)

    print('Election Results')
    print('--------------------------------')
    print('Total Votes: ' + str(len(voter_id)))
    print('--------------------------------')
    print('Khan: ' + str(round(khan_pct,2)) + '%' + ' (' + str(len(khan_occur)) + ')')
    print('Correy: ' + str(round(correy_pct,2)) + '%' + ' (' + str(len(correy_occur)) + ')')
    print('Li: ' + str(round(li_pct,2)) + '%' + ' (' + str(len(li_occur)) + ')')
    print("O'Tooley: " + str(round(otooley_pct,2)) + '%' + ' (' + str(len(otooley_occur)) + ')')
    print('--------------------------------')
    print('Winner: ' + str(winner))