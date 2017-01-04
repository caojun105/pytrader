from django.core.management.base import BaseCommand
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import utc
class Command(BaseCommand):

    help = 'pulls prices and stores them in a DB'
    def tick(slef):
        from history.poloniex import poloniex
        from history.models import Price
        import time
        poo = poloniex(settings.API_KEY, settings.API_SECRET)
        price = poo.returnTicker()

        for ticker in price.keys():
            if ticker =="BTC_ETH" or ticker=="USDT_BTC":
                this_price = price[ticker]['last']
                this_volume = price[ticker]['quoteVolume']
                the_str = ticker + ',' + str(time.time()) + ',' + this_price + ", " + this_volume
                #print("(pp)"+the_str)
                p = Price()
                p.price = this_price
                p.volume = this_volume
                p.lowestask = price[ticker]['lowestAsk']
                p.highestbid = price[ticker]['highestBid']
                p.symbol = ticker
                p.created_on_str = str(p.created_on)
                p.save()


    def handle(self, *args, **options):
        import time
        scheduler = BlockingScheduler()
        scheduler.add_job(self.tick, 'interval', seconds=10)
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass


