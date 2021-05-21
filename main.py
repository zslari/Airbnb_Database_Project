from dataset_options import DataSet

home_currency = ""

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
        home_currency = input("What is your home currency?"
                              " (USD/EUR/CAD/GBP/CHF/NZD/AUD/JPY)")
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
