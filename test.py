from datetime import datetime, timedelta

from ryanair import Ryanair

a = Ryanair()
START = datetime.now().date() + timedelta(days=1)
END = START + timedelta(days=1)
a.get_cheapest_return_flights("DUB", START, START, END, END)
