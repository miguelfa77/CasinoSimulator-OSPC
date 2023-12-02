from classes.casino_class import Casino

if __name__ == "__main__":
    """
<<<<<<< HEAD
    Subject to change if we want to use inputs instead of predefined constants. 
=======
    Subject to change if we want to use inputs instead of predefined constants.
>>>>>>> refs/remotes/origin/testing
    Keep like this for now.
    """

    starting_balance = 100000000
    SIM_DURATION = 100
<<<<<<< HEAD
    NUM_OF_TABLES = 3                   # MUST BE MULTIPLE OF 3
=======
    NUM_OF_TABLES = 6  # MUST BE MULTIPLE OF 3
>>>>>>> refs/remotes/origin/testing
    NUM_OF_CUSTOMERS = 50
    NUM_OF_DEALERS = 10
    NUM_OF_BARTENDERS = 2
    NUM_OF_BOUNCERS = 2

<<<<<<< HEAD

    casino = Casino.__new__(cls=Casino)
    casino.__init__(STARTING_BALANCE=starting_balance,
                    SIM_DURATION=SIM_DURATION,
                    NUM_OF_TABLES=NUM_OF_TABLES,
                    NUM_OF_CUSTOMERS=NUM_OF_CUSTOMERS,
                    NUM_OF_DEALERS=NUM_OF_DEALERS,
                    NUM_OF_BARTENDERS=NUM_OF_BARTENDERS,
                    NUM_OF_BOUNCERS=NUM_OF_BOUNCERS)
    
    casino.run()







=======
    casino = Casino.__new__(cls=Casino)
    casino.__init__(
        STARTING_BALANCE=starting_balance,
        SIM_DURATION=SIM_DURATION,
        NUM_OF_TABLES=NUM_OF_TABLES,
        NUM_OF_CUSTOMERS=NUM_OF_CUSTOMERS,
        NUM_OF_DEALERS=NUM_OF_DEALERS,
        NUM_OF_BARTENDERS=NUM_OF_BARTENDERS,
        NUM_OF_BOUNCERS=NUM_OF_BOUNCERS,
    )

    casino.run()
>>>>>>> refs/remotes/origin/testing
