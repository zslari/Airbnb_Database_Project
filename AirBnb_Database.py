""" This program first asks the user for their name, and then welcomes
them to CS 3A. The program then displays a menu on a loop for the user
to choose from and displays a message based on user input. The loop ends
when user quits. Currency conversion has been implemented. Headers have
been added. Reads a data set and provides cross table statistics. Option
1-7 functionality has been added. Option 8 loads data from a .CSV File.
"""

from enum import Enum
import csv

conversions = {
    "USD": 1,
    "EUR": .9,
    "CAD": 1.4,
    "GBP": .8,
    "CHF": .95,
    "NZD": 1.66,
    "AUD": 1.62,
    "JPY": 107.92
}

home_currency = ""

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


def print_menu():
    """ Display the main menu text. """
    print("Main Menu")
    print("1 - Print Average Rent by Location and Property Type")
    print("2 - Print Minimum Rent by Location and Property Type")
    print("3 - Print Maximum Rent by Location and Property Type")
    print("4 - Print Min/Avg/Max by Location")
    print("5 - Print Min/Avg/Max by Property Type")
    print("6 - Adjust Location Filters")
    print("7 - Adjust Property Type Filters")
    print("8 - Load Data")
    print("9 - Quit")


def menu(dataset: DataSet):
    """ present user with options to access the Airbnb dataset """
    currency_options(home_currency)
    print()
    while True:
        print(dataset.header)
        print_menu()
        try:
            selection = int(input("What is your choice? "))
        except ValueError:  # Talk about why this needs to be here
            print("Please enter a number only")
            continue
        if selection == 1:
            try:
                dataset.display_cross_table(DataSet.Stats.AVG)
            except dataset.EmptyDatasetError:
                print("Please Load a Dataset First")
        elif selection == 2:
            try:
                dataset.display_cross_table(DataSet.Stats.MIN)
            except dataset.EmptyDatasetError:
                print("Please Load a Dataset First")
        elif selection == 3:
            try:
                dataset.display_cross_table(DataSet.Stats.MAX)
            except dataset.EmptyDatasetError:
                print("Please Load a Dataset First")
        elif selection == 4:
            try:
                dataset.display_field_table(DataSet.Categories.PROPERTY_TYPE)
            except dataset.EmptyDatasetError:
                print("Please load a Dataset first")
        elif selection == 5:
            try:
                dataset.display_field_table(DataSet.Categories.LOCATION)
            except dataset.EmptyDatasetError:
                print("Please load a Dataset first")
        elif selection == 6:
            try:
                manage_filters(dataset, dataset.Categories.LOCATION)
            except dataset.EmptyDatasetError:
                print("Please load a Dataset first")
        elif selection == 7:
            try:
                manage_filters(dataset, dataset.Categories.PROPERTY_TYPE)
            except dataset.EmptyDatasetError:
                print("Please load a Dataset first")
        elif selection == 8:
            dataset.load_file()
        elif selection == 9:
            print("Goodbye!  Thank you for using the database")
            break
        else:
            print("Please enter a number between 1 and 9")


def currency_converter(quantity: float, source_curr: str, target_curr: str):
    """ Convert from one unit of currency to another.

    Keyword arguments:
        quantity -- a float representing the amount of currency to be
                    converted.
        source_curr -- a three letter currency identifier string from
                       the conversions dictionary
        target_curr -- a three letter currency identifier string from
                       the conversions dictionary
    """
    if source_curr not in conversions or target_curr not in \
            conversions or quantity <= 0:
        raise ValueError
    in_usd = quantity / conversions[source_curr]
    in_target = in_usd * conversions[target_curr]
    return in_target


def currency_options(base_curr='EUR'):
    """ Present a table of common conversions from base_curr to other
    currencies.
    """
    print("Options for converting from USD: ")
    for target in conversions:
        print(f"{target:10}", end="")
    print()
    for i in range(10, 100, 10):
        for target in conversions:
            print(f"{currency_converter(i, base_curr, target):<10.2f}", end="")
        print()


def manage_filters(dataset: DataSet, category: DataSet.Categories):
    """ Manage location and property type filters """
    flag = True
    while flag:
        print("The following labels are in the dataset: ")
        for item in enumerate(dataset.get_labels(category), 1):
            status = "ACTIVE" if item[1] in \
                                 dataset.get_active_labels(category) else "INACTIVE"
            print(f"{item[0]}: {item[1]:<25}{status}")
        user_input = input("Please select an item to toggle or enter a blank"
                           " line when you are finished. ")
        if user_input == "":
            break
        for item in enumerate(dataset.get_labels(category), 1):
            if int(user_input) == item[0]:
                dataset.toggle_active_label(category, item[1])


def main():
    global home_currency
    air_bnb = DataSet()
    print(air_bnb.header)
    name = input("Please enter your name: ")
    message = "Hi " + name + ", welcome to Foothill's database project."
    print(message)
    while home_currency not in conversions:
        home_currency = input("What is your home currency?")
    while True:
        print("Enter a header for the menu: ")
        header = input()
        try:
            air_bnb.header = header
            break
        except ValueError:
            print(f"Header must be a string less than {air_bnb.header_length} "
                  f"characters long")
    menu(air_bnb)


if __name__ == "__main__":
    main()

r"""
--- sample run #1 ---
Please enter your name: Zafir
Hi Zafir, welcome to Foothill's database project.
What is your home currency?CHF
Enter a header for the menu: 
Data for Airbnb
Options for converting from USD: 
USD       EUR       CAD       GBP       CHF       NZD       AUD       JPY       
10.53     9.47      14.74     8.42      10.00     17.47     17.05     1136.00   
21.05     18.95     29.47     16.84     20.00     34.95     34.11     2272.00   
31.58     28.42     44.21     25.26     30.00     52.42     51.16     3408.00   
42.11     37.89     58.95     33.68     40.00     69.89     68.21     4544.00   
52.63     47.37     73.68     42.11     50.00     87.37     85.26     5680.00   
63.16     56.84     88.42     50.53     60.00     104.84    102.32    6816.00   
73.68     66.32     103.16    58.95     70.00     122.32    119.37    7952.00   
84.21     75.79     117.89    67.37     80.00     139.79    136.42    9088.00   
94.74     85.26     132.63    75.79     90.00     157.26    153.47    10224.00  

Data for Airbnb
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 8
Data for Airbnb
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 1
               Private room        Entire home/apt     Shared room         
Queens         $ 71.76             $ 147.05            $ 69.02             
Bronx          $ 66.79             $ 127.51            $ 59.80             
Brooklyn       $ 76.50             $ 178.33            $ 50.53             
Manhattan      $ 116.78            $ 249.24            $ 88.98             
Staten Island  $ 62.29             $ 173.85            $ 57.44             
Data for Airbnb
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 9
Goodbye!  Thank you for using the database

Process finished with exit code 0
"""
