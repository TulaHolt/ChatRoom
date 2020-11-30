"""
Python list model
"""
from datetime import date
from .Model import Model

class model(Model):
    def __init__(self):
        self.guestentries = []

    def select(self):
        """
        Returns guestentries list of lists
        Each list in guestentries contains: name, street address, city, state, zipcode, store hours, phone number, rating, 
        review, type of cusine, and vegan friendly.
        :return: List of lists
        """
        return self.guestentries

    def insert(self,name,streetaddress, city, state, zipcode, date, note):
        """
        Appends a new list of values representing new message into guestentries
        :param name: String
        :param streetaddress: String
        :param city: String
        :param state: String
        :param zipcode: Int
        :param date: String
        :param note: String
        :return: True
        """
        params = [name, streetaddress, city, state, zipcode, date, note]
        self.guestentries.append(params)
        return True
