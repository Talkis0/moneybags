## This aqcuires data from AV and orginizes this data into csvs create a commodities function 


import requests
import csv


##Oil
month = '2009-01'
function  = 'WTI'

url = 'https://www.alphavantage.co/query?function=WTI&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()

with open("WTI.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n") 

function  = 'Brent'

url = 'https://www.alphavantage.co/query?function=BRENT&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()

with open("Brent.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n") 

##Natural Gass
function  = 'NATURAL_GAS'

url = 'https://www.alphavantage.co/query?function=NATURAL_GAS&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()

with open("NatGas.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n") 

##Copper
function  = 'COPPER'

url = 'https://www.alphavantage.co/query?function=COPPER&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()

with open("COPPER.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n") 

##Aluminum
function  = 'ALUMINUM'

url = 'https://www.alphavantage.co/query?function=ALUMINUM&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()

with open("ALUMINUM.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n") 



##Wheat
function  = 'WHEAT'

url = 'https://www.alphavantage.co/query?function=WHEAT&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()

with open("WHEAT.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n") 

##CORN
function  = 'CORN'

url = 'https://www.alphavantage.co/query?function=CORN&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()

with open("CORN.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n") 


##COTTON
function  = 'COTTON'

url = 'https://www.alphavantage.co/query?function=COTTON&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()

with open("COTTON.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n")     


##SUGAR
function  = 'SUGAR'

url = 'https://www.alphavantage.co/query?function=SUGAR&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()

with open("SUGAR.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n")


##COFFEE
function  = 'COFFEE'

url = 'https://www.alphavantage.co/query?function=COFFEE&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()

with open("COFFEE.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n")


##ALL_COMMODITIES 

function  = 'ALL_COMMODITIES'

url = 'https://www.alphavantage.co/query?function=ALL-COMODITIES&interval=monthly&apikey=GOIR6JKN4TW5HNGO'

r = requests.get(url)
data = r.json()
print(data) 
with open("ALL_COMMODITIES.csv", "w+") as file:
    for i in data["data"]:
        file.write( i["date"] + "," + i["value"]+ "\n")   

# does not work, running with this yeilds the message ""