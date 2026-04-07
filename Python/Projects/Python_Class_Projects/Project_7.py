'''
Alright, here's your next assignment.
We need an inventory tracking system. We've got products coming in and out of our 
warehouse and right now nobody knows what we have, what it's worth, or what's running low.

Build me a Product class. Every product has a name, a SKU, a price, and how many we have in stock. 

SKUs are always exactly 8 characters, uppercase, letters and numbers only — things like "WIDGET01" 
or "BOLT8823". If a SKU doesn't follow that format, it shouldn't be allowed into the system.

I want to be able to check the total value of any product — that's just price times quantity. 
But make it work like an attribute, not a method call. I want product.total_value, 
not product.total_value(). And nobody should be able to set that value manually — it should 
always be calculated from the price and quantity.


Then build me an Inventory class that holds all our products. I need to be able to add products 
to it, but only if their SKU is valid. I also need a way to quickly see which products are 
running low — give me a threshold and tell me what's below it.

Our warehouse team sometimes sends us data as a list of tuples — stuff like 
("Widget", "WIDGET01", 9.99, 50). I need a quick way to take a whole batch of those and create a 
fully loaded inventory from it in one call.


And finally, I need to know the total value of everything in our warehouse at any given moment.
One thing to research before you start — look into Python's @property decorator. You haven't used 
it yet but you'll need it for this one. Try figuring it out on your own first and ask me if you 
get stuck.
Get this to me when it's ready.
'''

class Product:
    def __init__(self, name, sku, price, stock):
        self.name = name
        # New Idea 
        #if len(sku) is not equal to 8 or are there invalid characters raise an error 
        '''
        Why not use ==? If you use == you would be raising the error on valid input and letting bad input through. != means if the length is wrong raise the error. 
        For example if len(sku) == 8 raise value error. This is incorrect. You dont want to trigger errors when they are valid you want to trigger them when they are invalid. 
        The logic here is to catch all bad input. So everything is written from is this wrong perspective. Now what I have been taught is to use if/else for valid and invalid but 
        it is cleaner to just work with the invalid instances 
        '''
        if len(sku) != 8 or not sku.isalnum():
            raise ValueError ("SKU not accessible")
        self.sku = sku.upper()
        self.price = price
        self.stock = stock 
    #New @property 
    @property
    def total_price(self):
        a = self.price * self.stock
        return a 
    
    @staticmethod
    def is_valid(sku):
        if len(sku) == 8:
            return True
        else:
            return False

    


class Inventory:
    def __init__(self):
        self.products = []

    #product here will be the instance of the class Product visually remember that
    def add_stock(self, product):
        if product.is_valid(product.sku) == True:
            self.products.append(product)
    #fix this
    def low_stock(self, product):
        if product.stock < 20:
            return "Low stock"


    @classmethod
    def from_tuple(cls, tuple_list):

        new_list = cls()
        for items in tuple_list:
            name = items[0] 
            sku = items[1]
            price = items[2]
            stock = items[3]
            added = Product(name, sku, price, stock)
            new_list.add_stock(added)
        return new_list
    
    @property
    def all_inventory_total(self):
        total_price = 0
        for x in self.products:
            #total_price is from @property in the Product class
            total_price += x.total_price
        return total_price

'''
        for x in self.products:
            all_total_inventory = sum(x.stock) * sum(x.price)
        return all_total_inventory
'''
'''
^^^ so whats wrong with the above green out code :
x is a single Product instance — x.stock and x.price are just numbers, 
not lists. You can't call sum() on a number. And the loop overwrites 
all_total_inventory on every iteration so you'd only ever get the last product's 
total anyway.

Every iteration creates a brand new all_total_inventory and assigns it. 
It never accumulates — it just replaces whatever was there before.
'''
