import specialized_web_scraper
from apscheduler.schedulers.background import BackgroundScheduler
import constants
from db.specialized_repository import SpecializedRepository
from sqlite3 import connect

class SpecializedScheduler:

    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()
        self.repository = SpecializedRepository()

    def __init_products(self):
        with connect('db/specialized.db') as conn:
            bikes = specialized_web_scraper.get_products(constants.BIKES_URL)
            sales = specialized_web_scraper.get_products(constants.SALES_URL)
            shoes = specialized_web_scraper.get_products(constants.SHOES_URL)
            helmets = specialized_web_scraper.get_products(constants.HELMETS_URL)
            pedals = specialized_web_scraper.get_products(constants.PEDALS_URL)
            wheels = specialized_web_scraper.get_products(constants.WHEELS_URL)
            self.repository.create_tables(conn)
            self.repository.replace(conn, 'bikes', bikes)
            self.repository.replace(conn, 'sales', sales)
            self.repository.replace(conn, 'shoes', shoes)
            self.repository.replace(conn, 'helmets', helmets)
            self.repository.replace(conn, 'pedals', pedals)
            self.repository.replace(conn, 'wheels', wheels)

    def __configure(self):
        self.scheduler.add_job(self.__init_products, 'interval', seconds=60, max_instances=3)

    def run(self):
        self.__configure()
        self.scheduler.start()
