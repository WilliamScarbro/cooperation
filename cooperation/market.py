import random

class market:
    resource_names = {"Wheat","Pork","Wood"}
    def __init__(self, resources, people):
        self.people=people
        self.resources=resources
    
    def set_initial_prices(self):
        for name in self.resources:
            self.resources[name].price=int(10*person.min_require[name]*len(self.people)/self.resources[name].quantity)

    def produce(self):
        for r_name in self.resources:
            self.resources[r_name].quantity=0
        for name in self.people:
            success_fac = random.randint(5,10)
            (r_name, quantity) = self.people[name].produce(success_fac)
            self.resources[r_name].quantity+=quantity
    
    def trade(self):
        prices = {name:self.resources[name].price for name in self.resources}
        offers = []
        for name in self.people:
            offers += self.people[name].make_offers(prices.copy())
        transac = market.resolve(offers)
        self.adjust_prices(offers)
        return transac

    
    @staticmethod
    def resolve(offers):
        obyr = {name:[[],[]] for name in market.resource_names}
        for offer in offers:
            if offer.sell:
                obyr[offer.resource][0].append(offer)
            else:
                obyr[offer.resource][1].append(offer)
        transactions=0
        for name in market.resource_names:
            obyr[name][0].sort(key = lambda x: x.price)
            obyr[name][1].sort(key = lambda x: -x.price)
            for offer in obyr[name][0]:
                buy_count=0
                while offer.quantity>0 and buy_count<len(obyr[name][1]):
                    cur_buy = obyr[name][1][buy_count]
                    #print(offer.quantity,buy_count,cur_buy.quantity)
                    if cur_buy.quantity==0 or cur_buy.price<offer.price:
                        buy_count+=1
                        continue
                    #print(f"combining {cur_buy} and {offer}")
                    cur_buy.combine(offer,cur_buy.price)
                    transactions+=1
        return transactions

    def __str__(self):
        ret = "Resources:\nResource | Quantity |  Price\n"
        for name in self.resources:
            ret+=str(self.resources[name])+'\n'
        oc_s = self.occ_spread()
        for name in oc_s:
            ret+=f"There are {oc_s[name][0]} {name}ers with ${oc_s[name][1]/oc_s[name][0]} per person.\n"
        ret+=f"{self.total_satisfied()} of {len(self.people)} have their needs satisfied."
        return ret
    
    def occ_spread(self):
        ocs = {name:[0,0] for name in self.resources}
        for name in self.people:
            ocs[self.people[name].occupation][0]+=1
            ocs[self.people[name].occupation][1]+=self.people[name].money
        return ocs
    
    def adjust_prices(self, failed_offers):
        total_price = {name:0 for name in self.resources}
        total_quantity= total_price.copy()
        for offer in failed_offers:
                total_price[offer.resource]+=offer.price*offer.quantity
                total_quantity[offer.resource]+=offer.quantity
        for name in self.resources:
            self.resources[name].price=int(total_price[name]/total_quantity[name])
        

    def new_year(self):
        self.produce()
        self.set_initial_prices()
        print("INTIAL PRICES")
        print(self)
        while input("price cycle")!="quit":
            transactions = self.trade()
            print(f"transactions: {transactions}")
            print(self)
    
    def total_satisfied(self):
        total=0
        for name in self.people:
            if people[name].met_require():
                total+=1
        return total
        
        
class resource:
    def __init__(self, name, price, quantity):
        self.name=name
        self.price=price
        self.quantity=quantity

    def copy(self):
        return resource(self.name,self.price,self.quantity)

    def __str__(self):
        return f"{self.name}    | {self.quantity}      | {self.price}     "

class offer:
    #to sell make price and quantity negative
    def __init__(self, offerer, resource, quantity, price, sell):
        self.person = offerer
        self.resource = resource
        self.quantity = quantity
        self.price = price
        self.sell = sell
    
    def accept(self, person2, sub_quant, price):
        if sub_quant>self.quantity:
            print("sub_quant error")
        if self.sell:
            if self.person.resources[self.resource].quantity - sub_quant < 0:
                self.problem("Insufficient Quantity", person2, self.person, sub_quant, price)
            if person2.money - (price*sub_quant) < 0:
                self.problem("Insufficient Money", person2, self.person, sub_quant, price)
            self.transact(person2, self.person, sub_quant, price)
        else:
            if person2.resources[self.resource].quantity + sub_quant < 0:
                self.problem("Insufficient Quantity", self.person, person2, sub_quant, price)
            if self.person.money - (price*sub_quant) < 0:
                self.problem("Insufficient Money", self.person, person2, sub_quant, price)
            self.transact(self.person, person2, sub_quant, price)
        self.quantity -= sub_quant

    def transact(self, buyer, seller, quant, price):
        buyer.resources[self.resource].quantity += quant
        seller.resources[self.resource].quantity -= quant
        buyer.money -= price*quant
        seller.money += price*quant
        
        
    def problem(self, message, buyer, seller, quantity, price):
        print(self)
        print(f"Buyer {buyer}")
        print(f"Seller {seller}")
        print(f"Quantity {quantity}")
        print(f"Price {price}")
        raise Exception(message)    
    #assumes other offer is for the same resource and opposite sell
    def combine(self, offer2, price):
        if offer2.quantity<self.quantity:
            self.accept(offer2.person, offer2.quantity, price)
            offer2.quantity=0
        else:
            offer2.accept(self.person, self.quantity, price)
            self.quantity=0

    def __str__(self):
        return f"Offer ({'SELL' if self.sell else 'BUY'}):\n       person: {self.person}\n         {self.resource},{self.quantity},${self.price}"
            
class person:
    production = {"Wheat":10, "Pork":5, "Wood":1}
    min_require = {"Wheat":20, "Pork":10, "Wood":2}
    def __init__(self, name, occupation):
        self.name=name
        self.resources={name:resource(name,0,0) for name in person.production}
        self.occupation=occupation
        self.money=100
    
    def met_require(self):
        for name in self.resources:
            if self.resources[name].quantity<person.min_require[name]:
                return False
        return True
  
    def produce(self, success):
        for name in self.resources:
            self.resources[name].quantity=0
        quantity = success*person.production[self.occupation]
        self.resources[self.occupation].quantity=quantity
        return (self.occupation, quantity)
        
    def project_income(self, prices):
        income = 0
        for r_name in self.resources:
            #needed can be negative
            needed = self.resources[r_name].quantity - person.min_require[r_name]
            cost = needed*prices[r_name]
            income += cost
        return income
    

    #maybe should only include possitive needs, this assumes the person can sell at the set price
    def cost_of_needs(self, prices):
        total = 0
        for name in self.resources:
            need = self.need(name)
            if need>0:
                total+=need*prices[name]
        return total

    
    def make_offers(self, prices):
        if not self.met_require():
            while self.cost_of_needs(prices)>self.money:
                for name in self.resources:
                    need = self.need(name)
                    if need>0:
                        prices[name]-=1
                    #if need<0:
                    #    prices[name]+=1
        else:
            while self.project_income(prices)<0 and counter>=0:
                #counter-=1
                for name in self.resources:
                    need = self.need(name)
                    if need < 0:
                        prices[name]+=1
                    if need > 0:
                        prices[name]-=1
        return self.mo_help(prices)

    def need(self, name):
        return person.min_require[name] - self.resources[name].quantity

    def mo_help(self,prices):
        offers = []
        for name in self.resources:
            need = self.need(name)
            if need < 0:
                offers.append(offer(self, name, -need, prices[name],True))
            if need > 0:
                offers.append(offer(self, name, need, prices[name],False))
        return offers

    def __str__(self):
        ret= f"{self.name}:  {self.occupation}er, {self.money}"
        for name in self.resources:
            ret+='\n'+str(self.resources[name])
        return ret

def init_people(number):
    people = {}
    occupations=["Wheat","Wood","Pork"]
    for i in range(0,number):
        name = "person"+str(i)
        people[name]=person(name, random.choice(occupations))
    return people

if __name__=="__main__":
    resources = {"Wood":resource("Wood",0,0),"Pork":resource("Pork",0,0), "Wheat":resource("Wheat",0,0)}
    people = init_people(100)
    town = market(resources, people)
    print(town)
    town.start()
