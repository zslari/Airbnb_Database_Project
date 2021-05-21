from enum import Enum
import csv

filename = './AB_NYC_2019.csv'


class DataSet:
    """ the DataSet class will present summary tables based on
    information imported from a .csv file
    """

    class Categories(Enum):
        LOCATION = 0
        PROPERTY_TYPE = 1

    class Stats(Enum):
        MIN = 0
        AVG = 1
        MAX = 2

    class EmptyDatasetError(Exception):
        pass

    header_length = 30

    def __init__(self, header=""):
        self._active_labels = {DataSet.Categories.LOCATION: set(),
                               DataSet.Categories.PROPERTY_TYPE: set()}
        self._labels = {DataSet.Categories.LOCATION: set(),
                        DataSet.Categories.PROPERTY_TYPE: set()}
        self._data = None
        try:
            self.header = header
        except ValueError:
            self.header = ""

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, new_header: str):
        if isinstance(new_header, str) and \
                len(new_header) < self.header_length:
            self._header = new_header
        else:
            raise ValueError

    def load_file(self):
        """ Load data from .CSV file into self._data"""
        with open(filename, 'r', newline="") as file:
            csvreader = csv.reader(file)
            my_data = [tuple(i) for i in [row[1::] for row in csvreader][1::]]
            my_new_data = [(my_data[x][0], my_data[x][1], int(my_data[x][2]))
                           for x in range(len(my_data))]
            self._data = my_new_data
            self._initialize_sets()

    def _initialize_sets(self):
        """ Examine the category labels in self._data and create a set
        for each category containing the labels.
        """
        if not self._data:
            raise DataSet.EmptyDatasetError
        for category in self.Categories:
            self._labels[category] = set([i[category.value] for i in self._data])
            self._active_labels[category] = self._labels[category].copy()

    def load_default_data(self):
        """ Load sample data into self._data"""
        self._data = [("Staten Island", "Private room", 70),
                      ("Brooklyn", "Private room", 50),
                      ("Bronx", "Private room", 40),
                      ("Brooklyn", "Entire home / apt", 150),
                      ("Manhattan", "Private room", 125),
                      ("Manhattan", "Entire home / apt", 196),
                      ("Brooklyn", "Private room", 110),
                      ("Manhattan", "Entire home / apt", 170),
                      ("Manhattan", "Entire home / apt", 165),
                      ("Manhattan", "Entire home / apt", 150),
                      ("Manhattan", "Entire home / apt", 100),
                      ("Brooklyn", "Private room", 65),
                      ("Queens", "Entire home / apt", 350),
                      ("Manhattan", "Private room", 99),
                      ("Brooklyn", "Entire home / apt", 200),
                      ("Brooklyn", "Entire home / apt", 150),
                      ("Brooklyn", "Private room", 99),
                      ("Brooklyn", "Private room", 120)]
        self._initialize_sets()

    def _alternate_category_type(self, first_category_type):
        """ Given one of the two Category Enum entries, return the
        other one.
        """
        if first_category_type is self.Categories.LOCATION:
            second_category_type = self.Categories.PROPERTY_TYPE
        else:
            second_category_type = self.Categories.LOCATION
        return second_category_type

    def _cross_table_statistics(self, descriptor_one: str,
                                descriptor_two: str):
        """ Given a label from each category, calculate summary
        statistics for the items matching both labels.

        Keyword arguments:
            descriptor_one -- the label for the first category
            descriptor_two -- the label for the second category

        Returns a tuple of min, average, max from the matching rows.
        """
        if not self._data:
            raise DataSet.EmptyDatasetError
        value_list = [item[2] for item in self._data if
                      item[0] == descriptor_one and item[1] == descriptor_two]
        if len(value_list) == 0:
            return None, None, None
        return min(value_list), sum(value_list) / len(value_list), \
               max(value_list)

    def display_cross_table(self, stat: Stats):
        """ Given a stat from DataSet.Stats, produce a table that
        shows the value of that stat for every pair of labels from the
        two categories.
        """

        if not self._data:
            raise DataSet.EmptyDatasetError
        property_labels = list(self._labels[DataSet.Categories.PROPERTY_TYPE])
        location_labels = list(self._labels[DataSet.Categories.LOCATION])
        print(f"               ", end="")
        for item in property_labels:
            print(f"{item:20}", end="")
        print()
        for item_one in location_labels:
            print(f"{item_one:15}", end="")
            for item_two in property_labels:
                value = self._cross_table_statistics(item_one,
                                                     item_two)[stat.value]
                if value is None:
                    print(f"$ {'N/A':<18}", end="")
                else:
                    print(f"$ {value:<18.2f}", end="")
            print()

    def _table_statistics(self, row_category: Categories, label: str):
        """ Given a category from DataSet.Categories, and a string
        calculate the min, max, and average rent of properties in the
        category
        """
        if not self._data:
            raise DataSet.EmptyDatasetError
        if row_category == DataSet.Categories.LOCATION:
            filter_prop = [item[2] for item in self._data if
                           label in item and item[1] in self._active_labels
                           [DataSet.Categories.PROPERTY_TYPE]]
            if not filter_prop:
                return 0, 0, 0
            return min(filter_prop), sum(filter_prop) \
                   / len(filter_prop), max(filter_prop)
        elif row_category == DataSet.Categories.PROPERTY_TYPE:
            filter_loc = [item[2] for item in self._data if
                          label in item and item[0] in self._active_labels
                          [DataSet.Categories.LOCATION]]
            if not filter_loc:
                return 0, 0, 0
            return min(filter_loc), sum(filter_loc) \
                   / len(filter_loc), max(filter_loc)
        else:
            return "N/A", "N/A", "N/A"

    def display_field_table(self, rows: Categories):
        """ Given a category display a filtered table of the min, max,
         and average rent of properties in the category
        """
        if not self._data:
            raise DataSet.EmptyDatasetError
        print("The following data are from properties matching this criteria:")
        for item in list(self._active_labels[rows]):
            print(f"- {item}")
        print(f"                    Minimum             Average"
              f"             Maximum", end="")
        print()
        null_value = "N/A"
        for _ in DataSet.Categories:
            if _ == rows:
                for i in self._labels[DataSet._alternate_category_type(self,
                                                                       rows)]:
                    value = DataSet._table_statistics(
                        self, DataSet._alternate_category_type(self, rows), i)
                    if value == (0, 0, 0):
                        print(f"{i:19} {null_value:<19} {null_value:<19}"
                              f" {null_value:<19}")
                        print()
                    else:
                        print(f"{i:20}$ {value[0]:<18.2f}$"
                              f" {value[1]:<18.2f}$ {value[2]:<18.2f}")
                        print()

    def get_labels(self, category: Categories):
        if not self._data:
            raise DataSet.EmptyDatasetError
        return list(self._labels[category])

    def get_active_labels(self, category: Categories):
        return list(self._active_labels[category])

    def toggle_active_label(self, category: Categories, descriptor: str):
        """ Add or remove labels from the active labels """

        if descriptor not in self._labels[category]:
            raise KeyError
        if descriptor in self._active_labels[category]:
            self._active_labels[category].remove(descriptor)
        else:
            self._active_labels[category].add(descriptor)
