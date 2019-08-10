import datetime
import unittest
import requests
import pprint


class TestUsersRepository(unittest.TestCase):

    def setUp(self):
        self.url = "http://localhost:5000"

    def print(self, obj):
        print("=============================\n")
        pprint.pprint(obj)
        print("=============================\n")

    def validate_response(self, result, message="no data"):
        if result.status_code > 299:
            raise ValueError(message + " " + result.reason)


    def test_sources(self):
        start = datetime.date(2019, 7, 1)
        end = datetime.date(2019, 7, 31)
        res = requests.get(self.url + "/customers", verify=False)
        self.validate_response(res)
        customers = res.json()
        for customer in customers:
            res = requests.get(self.url + "/products?customerId={}".format(customer["id"]), verify=False)
            self.validate_response(res)
            products = res.json()
            for product in products:
                res = requests.get(self.url + "/sources?productId={}".format(product["id"]), verify=False)
                self.validate_response(res)
                sources = res.json()
                for source in sources:
                    res = requests.get(self.url + "/sources/{}/reports/daily/series?start={}&end={}".format(
                        source["id"], start, end), verify=False)
                    self.validate_response(res)
                    report = res.json()
                    self.print(report)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
