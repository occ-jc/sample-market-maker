import sys
from market_maker.market_maker import OrderManager

##################################################
# Acess to settings
##################################################
from market_maker.settings import settings
###################################################
# My functions
###################################################
def readLiqFile(path):
        try:

            file = open(path,"r")
            temp = file.read()
            temp = temp.splitlines()

            side = temp[0]
            qty = float(temp[1])
            price = float(temp[2])
            
            file.close()

            # overwrite the file
            file = open(path,"w")
            file.close()
            return [side,qty,price]
        except:
            return [0,0,0]

####################################################################

class CustomOrderManager(OrderManager):
    """A sample order manager for implementing your own custom strategy"""

    def place_orders(self) -> None:
        # implement your custom strategy here
        buy_orders = []
        sell_orders = []

        # populate buy and sell orders, e.g.
        # buy_orders.append({'price': 999.0, 'orderQty': 100, 'side': "Buy"})
        # sell_orders.append({'price': 1001.0, 'orderQty': 100, 'side': "Sell"})

######################################################################################
        # my own garbage
        side,qty,price = readLiqFile(settings.liqfilepath)

        ########## trading logic###########3        
        try:
            print(qty)
            if qty > 1:
                print("p1")

                ## We do sell when shorts get Liquidatet
                if side == "Buy":    # is it a short liquidation?
                    print("p2")
                    if settings.sell_active:    # is the sell side activatet ?
                        print("p3")
                        if not self.short_position_limit_exceeded(): #short positon limit not exceeded
                            print("p3.1")
                            if settings.sell_threshold < price:                # is the price above the sell threshold ? 
                                qty = int(round(qty/settings.factor_short))       # reduce by factor
                                print("p4")
                                if qty > 0:
                                    print("p5")
                                    sell_orders.append({'price': price, 'orderQty': qty, 'side': "Sell"})   # send the orders

                                
                ## We do buy when longs get liquidatet
                if side == "Sell":    # is it a long liquidation?
                    print("p2.2")
                    if settings.buy_active:    # is the buy side activatet ?
                        print("p3.3")
                        if not self.long_position_limit_exceeded(): #long positon limit not exceeded
                            print("p3.3.1")
                            if settings.buy_threshold > price:                # is the price below the buy threshold ?
                                print("p4.4")
                                qty = int(round(qty/settings.factor_long))       # reduce by factor
                                if qty > 0:
                                    print("p5.5")
                                    buy_orders.append({'price': price, 'orderQty': qty, 'side': "Buy"})   # send the orders
            
        except:
            pass
           
##################################################################################################

        self.converge_orders(buy_orders, sell_orders)

    def run() -> None:
        order_manager = CustomOrderManager()

        # Try/except just keeps ctrl-c from printing an ugly stacktrace
        try:
            order_manager.run_loop()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()


CustomOrderManager.run()
