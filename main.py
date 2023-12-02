from classes.casino_class import Casino

if __name__ == "__main__":
    """
    Subject to change if we want to use inputs instead of predefined constants. 
    Keep like this for now.
    """

    starting_balance = 100000000
    NUM_OF_TABLES = 6                   # MUST BE MULTIPLE OF 3
    NUM_OF_CUSTOMERS = 50
    NUM_OF_DEALERS = 10
    NUM_OF_BARTENDERS = 2
    NUM_OF_BOUNCERS = 2


    casino = Casino.__new__(cls=Casino)
    casino.__init__(STARTING_BALANCE=starting_balance,
                    NUM_OF_TABLES=NUM_OF_TABLES,
                    NUM_OF_CUSTOMERS=NUM_OF_CUSTOMERS,
                    NUM_OF_DEALERS=NUM_OF_DEALERS,
                    NUM_OF_BARTENDERS=NUM_OF_BARTENDERS,
                    NUM_OF_BOUNCERS=NUM_OF_BOUNCERS)
    
    casino.run()







