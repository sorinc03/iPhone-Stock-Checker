import json, urllib, urllib2, base64, time, os

## [readme]
#  (1). Install python 2.7 (this script will not work with python 3+)
#  (2). Install PushBullet to your mobile device's + set it up (takes few minutes)
#       - On PC, login to pushbullet.com and go to Account Settings, copy your API key and paste it into pushbullet_Key below
#  (3). Look at stores variable below to find the exact names of the stores you want to be checked, enter their names exactly as shown into allowedStores below (use a comma for multiple stores)
#       - DO NOT CHANGE stores/appleStores/appleStock URL's unless you know what you are doing / modfying this script for alternative locations (Canada?)
#  (4). Look at the models variable in the Vars section below, locate all of the model codes that you want to be notified of when they are in stock at the stores chosen
#       - Enter them into the wantedModels variable..
#  (5). Change nextCheck to how long to wait until performing the next check (this is in seconds, 60seconds is recommended!)
#  (6). Run script and leave running, as soon as there is stock for the chosen stores/models a PUSH notifation will be sent to all of your devices that are linked with the specified pushbullet account!
#
#
#  (*) - See below as an example of a configuration that checks the Basingstake/Southampton/Reading stores for ANY iPhone 6+ stock every 60seconds
## [/readme]

## Config
pushbullet_Key = ""
allowedStores = "Union Square,Festival Place,SouthGate,Bullring,Churchill Square,Cabot Circus,Cribbs Causeway,Bromley,Grand Arcade,St David's 2,Princes Street,Braehead,Buchanan Street,Lakeside,Bluewater,Bentall Centre,Trinity Leeds,Highcross,Liverpool ONE,Apple Watch at Selfridges,Brent Cross,Covent Garden,White City,Stratford City,Manchester Arndale,Trafford Centre,Milton Keynes,Eldon Square,Chapelfield,The Oracle,Meadowhall,Touchwood Centre,WestQuay,Watford"
wantedModels = {
                  # 7+ 128GB
                  "MN4V2" : True,
                  # 7+ 256GB
                  "MN512" : True
                };
nextCheck = 5

## Vars
appleStores = "https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/stores.json"
appleStock = "https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/availability.json"
stores = {
            "R659" : "Apple Watch at Selfridges",
            "R227" : "Bentall Centre",
            "R113" : "Bluewater",
            "R340" : "Braehead",
            "R163" : "Brent Cross",
            "R496" : "Bromley",
            "R135" : "Buchanan Street",
            "R118" : "Bullring",
            "R252" : "Cabot Circus",
            "R391" : "Chapelfield",
            "R244" : "Churchill Square",
            "R245" : "Covent Garden",
            "R393" : "Cribbs Causeway",
            "R545" : "Drake Circus",
            "R341" : "Eldon Square",
            "R482" : "Festival Place",
            "R270" : "Grand Arcade",
            "R308" : "Highcross",
            "R242" : "Lakeside",
            "R239" : "Liverpool ONE",
            "R215" : "Manchester Arndale",
            "R153" : "Meadowhall",
            "R423" : "Metrocentre",
            "R269" : "Milton Keynes",
            "R328" : "Princes Street",
            "R279" : "Princesshay",
            "R092" : "Regent Street",
            "R335" : "SouthGate",
            "R334" : "St David's 2",
            "R410" : "Stratford City",
            "R176" : "The Oracle",
            "R255" : "Touchwood Centre",
            "R136" : "Trafford Centre",
            "R372" : "Trinity Leeds",
            "R363" : "Union Square",
            "R313" : "Victoria Square",
            "R527" : "Watford",
            "R174" : "WestQuay",
            "R226" : "White City"
         };
models = {  # iPhone 7
            "MN962" : "iPhone 7 Jet Black 128GB",
            "MN9C2" : "iPhone 7 Jet Black 256GB",
            "MN8X2" : "iPhone 7 Black 32GB",
            "MN922" : "iPhone 7 Black 128GB",
            "MN972" : "iPhone 7 Black 256GB",
            "MN8Y2" : "iPhone 7 Silver 32GB",
            "MN932" : "iPhone 7 Silver 128GB",
            "MN982" : "iPhone 7 Silver 256GB",
            "MN902" : "iPhone 7 Gold 32GB",
            "MN942" : "iPhone 7 Gold 128GB",
            "MN992" : "iPhone 7 Gold 256GB",
            "MN912" : "iPhone 7 Rose 32GB",
            "MN952" : "iPhone 7 Rose 128GB",
            "MN9A2" : "iPhone 7 Rose 256GB",

            # iPhone 7+
            "MN4V2" : "iPhone 7+ Jet Black 128GB",
            "MN512" : "iPhone 7+ Jet Black 256GB",
            "MNQM2" : "iPhone 7+ Black 32GB",
            "MN4M2" : "iPhone 7+ Black 128GB",
            "MN4W2" : "iPhone 7+ Black 256GB",
            "MNQN2" : "iPhone 7+ Silver 32GB",
            "MN4P2" : "iPhone 7+ Silver 128GB",
            "MN4X2" : "iPhone 7+ Silver 256GB",
            "MNQP2" : "iPhone 7+ Gold 32GB",
            "MN4Q2" : "iPhone 7+ Gold 128GB",
            "MN4Y2" : "iPhone 7+ Gold 256GB",
            "MNQQ2" : "iPhone 7+ Rose 32GB",
            "MN4U2" : "iPhone 7+ Rose 128GB",
            "MN502" : "iPhone 7+ Rose 256GB"
          };

## Quick Classes
class AppleStore:
    def GetStores(self):
        storesData = urllib2.urlopen(appleStores).read()
        tmp = json.loads(storesData)
        tmp2 = {}
        for store in tmp['stores']:
            if store['storeEnabled'] is True:
                tmp2[store['storeNumber']] = store['storeName']
        
        return tmp2

    def GetStock(self):
        return urllib2.urlopen(appleStock).read()

class PushBullet:
    def __init__(self, apiKey):
        self.key = apiKey
        self.auth = 'Basic {0}'.format(base64.b64encode(apiKey))
        
    def sendNote(self, title, message):
        header = { 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json', 'Authorization': self.auth }
        postData = urllib.urlencode({'type': 'note', 'title': title, 'body': message})
        req = urllib2.Request("https://api.pushbullet.com/v2/pushes", postData, header)
        return urllib2.urlopen(req).read()
        

## Funcs
def DoCheck():
    apple = AppleStore()
    push = PushBullet(pushbullet_Key)

    stock = apple.GetStock()
    tmp = json.loads(stock)
    #tmp = json.load(open("test.txt"))

    for store in tmp:
        if store == "updated":
            continue
        if store[:1] != 'R':
            continue
        if allowedStores.find(stores[store]) != -1:
            # Store is in allowedStores
            found = 0
            for item in tmp[store]:
                try:     # Exceptions will occur if model is not in the wanted list
                    if wantedModels[item[:5]] and tmp[store][item] == 'ALL':
                         # Found stock!
                        push.sendNote(models[item[:5]], "Stock found at " + stores[store] + "\n\n" + time.strftime('(%d.%b.%y/%I:%M%p)'))
                        os.system("say " + store + " " + stores[store])
                            # os.system("open -a Safari https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/availability?channel=1&sourceID=50F4C7FD71960CDA-23E9BC7B89D857DD&rv=0&path=&iPP=E&appleCare=Y&store=" + store)
                        print time.strftime('(%d.%b.%y/%I:%M%p)') + ": Found " + models[item[:5]] + " at " + stores[store]
                except:
                    pass # continue the loop as current model is not wanted
    
    print time.strftime('(%d.%b.%y/%I:%M%p)') + ": Finished checking..."

## Main Code
if __name__ == '__main__':
    tmp = AppleStore()
    tmp2 = PushBullet(pushbullet_Key)
    tmp2.sendNote("Stock Checker", "iPhone Stock checker is up and running!\n\nYou will be notifed immediately once stock is found for your locations!")

    while True:
        try:
            DoCheck()
        except:
            print time.strftime('(%d.%b.%y/%I:%M%p)') + ": Hmm, reserve for pickup may be down?"

        time.sleep(nextCheck)