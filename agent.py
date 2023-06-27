import random


class Client:
    def __init__(self, client_id, items, items_threshold, waiting_time_threshold):
        self.id = client_id
        self.state = "inshop"
        self.items = items
        self.items_threshold = items_threshold
        self.waiting_time = 0
        self.waiting_time_threshold = waiting_time_threshold
        self.acumulated_waiting_time = 0
        self.nr_drop_outs = 0
        self.nr_times_queues = 0
        self.tick = 0

    def get_id(self):
        return self.id

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def reduce_item(self, value):
        self.items -= value

    def get_items(self):
        return self.items

    def set_items(self, items):
        self.items = items

    def get_items_threshold(self):
        return self.items_threshold

    def get_waiting_time(self):
        return self.waiting_time

    def reset_waiting_time(self):
        self.waiting_time = 0

    def increment_waiting_time(self, value):
        self.waiting_time += value

    def increment_acumulated_waiting_time(self, value:int):
        self.acumulated_waiting_time += value

    def get_waiting_time_threshold(self):
        self.waiting_time_threshold

    def increment_nr_times_queue(self):
        self.nr_times_queues += 1

    def increment_drop_outs(self):
        self.nr_drop_outs += 1

    def increment_tick(self):
        self.tick += 1

    def get_tick(self):
        return self.tick




    def __str__(self):
        return f"Agent {self.id}: State={self.state}, Items={self.items}, Waiting Time={self.waiting_time}"