class Model():
    def select(self):
        """
        Gets all entries from the database
        :return: Tuple containing all rows of database
        """
        pass

    def insert(self,name,streetaddress, city, state, zipcode, date, note):
        """
        Inserts entry into database
        :param name: String
        :param streetaddress: String
        :param city: String
        :param state: String
        :param zipcode: Int
        :param date: String
        :param note: String
        :return: none
        :raises: Database errors on connection and insertion
        """
        pass
