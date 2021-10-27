import csv

def processCSV(csv):
    dataset = csv.read().decode('UTF-8')
    rows = dataset.split('\n')
    for row in rows[1:]:
        outlook, temp, humidity, windy, weather = row.split(',')
        print(outlook, temp, humidity, windy, weather)
        
        
    
