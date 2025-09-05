import data_handling.crud as crud
import data_handling.statistics as stat
import data_handling.create_html as create_html


def main():
    """
    main function where the print_menu function is called
    """
    # Your code here
    print_menu()


def print_menu():
    """
    Prints menu to the terminal and asks user for input.
    based on user input the corresponding function is called.
    """
    while True:
        print()
        print("********** My Movies Database **********")
        print()
        print(
            "Menu \n 0. Exit \n 1. List Movies \n 2. Add movie \n 3. Delete movie \n 5. Stats \n 6. Random movie \n 7. Search movie \n 8. Sort movies by rating or year \n 9. Save a histogram of the ratings to png-file \n 10. Filter Movies for year and rating\n 11. Create html")
        print()
        user_input = input("Enter choice (0-11): ")
        try:
            if not user_input.isnumeric():
                raise ValueError("Please enter a number between 0 and 11.")
            if user_input.isnumeric():
                if not 0 <= int(user_input) <= 11:
                    raise ValueError("Please enter a number between 0 and 11.")
            if user_input == "0":
                print("Bye")
                break
            elif user_input == "1":
                crud.list_movies()
            elif user_input == "2":
                crud.add_movie()
            elif user_input == "3":
                crud.delete_movie()
            elif user_input == "4":
                crud.update_movie()
            elif user_input == "5":
                stat.stats()
            elif user_input == "6":
                crud.random_movie()
            elif user_input == "7":
                crud.search_movie()
            elif user_input == "8":
                stat.sort_movies()
            elif user_input == "9":
                stat.create_rating_histogram()
            elif user_input == "10":
                stat.filter_movies()
            elif user_input == "11":
                create_html.create_website()
        except ValueError as e:
            print("Error:", e)
        print()




if __name__ == "__main__":
    main()
