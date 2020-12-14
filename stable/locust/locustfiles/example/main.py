# -*- coding: utf-8 -*-

from locust import HttpUser, task, between
from locustlib.example_functions import choose_random_page
import csv
import random


default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}


class WebsiteUser(HttpUser):
    pattern = []

    def on_start(self):
        with open('locustdata/example_data.csv', 'r') as f:
            data = csv.reader(f, delimiter=',', doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
            for row in data:
                self.pattern.append(row)

    wait_time = between(1, 2)

    @task(1)
    def get_index(self):
        self.client.get("/", headers=default_headers)

    @task(3)
    def get_random_page(self):
        self.client.get(choose_random_page(), headers=default_headers)

    @task(1)
    def get_random_page_param(self):
        i = random.randint(0, len(self.pattern)-1)

        self.client.get("{0}?param={1}".format(self.pattern[i][0], self.pattern[i][1]), headers=default_headers)
