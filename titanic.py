"""
===============================================================================
Ship Data CLI Project
===============================================================================
Author: [ABHISAKH SARMA]

Description:
    This is a command-line interface (CLI) tool for exploring and analyzing
    a dataset of ships. It uses the dispatcher pattern to handle various
    commands related to ship metadata, such as country of origin, ship type,
    and movement data like speed and position.

    The tool is interactive and extensible, making it suitable for data
    exploration, preprocessing, and visualization in maritime data analysis
    projects.

Features:
    • help                - Show available commands
    • show_countries      - Display all unique countries in the dataset
    • top_countries <N>   - Show top N countries by number of ships
    • ships_by_types      - Display ship types and their counts
    • search_ship         - Search for ships by name (case-insensitive, partial)
    • speed_histogram     - Generate and save a histogram of ship speeds
    • draw_map            - Plot ship positions (LAT/LON) on a world map
    • exit                - Exit the CLI safely

Usage:
    Run the script and enter commands interactively.
    Example:
        > top_countries 5
        > search_ship
        > speed_histogram my_plot.png
        > draw_map ships_map.png

Requirements:
    • Python 3.x
    • matplotlib

Note:
    This CLI assumes a preloaded `all_data` dictionary structured like:
    {
        "data": [
            {
                "SHIPNAME": "Example",
                "COUNTRY": "USA",
                "TYPE_SUMMARY": "Cargo",
                "SPEED": "13.5",
                "LAT": "36.7783",
                "LON": "-119.4179"
            },
            ...
        ]
    }

DISPATCHER PATTERN IMPLEMENTATION:
-----------------------------------
In this program, we implemented the dispatcher pattern to handle user
commands instead of using traditional if-elif conditional statements.
The dispatcher is a dictionary that maps command strings to their
corresponding handler functions. This approach improves code readability,
scalability, and maintainability, making it easier to add, remove, or
update commands without modifying long blocks of conditional logic.
It also keeps the main loop clean and focused on input parsing and
execution flow.
===============================================================================
"""


#***************** IMPORT LIBRARY  ***************************************

import matplotlib.pyplot as plt
from load_data import load_data


#=========================== DEFINE WORKING FUNCTION ================================

def show_countries(all_data):
    """
    Extract a list of countries from the ship data.

    Args:
        all_data (dict): Dictionary containing ship data.

    Returns:
        tuple: (list of all countries, list of unique countries)
    """
    country_list = []
    for ship in all_data['data']:
        country_list.append(ship['COUNTRY'])
    country_unique = list(set(country_list))
    country_unique.sort()
    return country_list, country_unique


def count_country_ship(all_data):
    """
    Count how many ships are registered from each country.

    Args:
        all_data (dict): Dictionary containing ship data.

    Returns:
        dict: Dictionary with countries as keys and ship counts as values.
    """
    country_list, _ = show_countries(all_data)
    country_dict = {}

    for country in country_list:
        if country in country_dict:
            country_dict[country] += 1
        else:
            country_dict[country] = 1

    return country_dict


def top_countries(all_data, top=5):
    """
    Return a list of the top countries by number of ships.

    Args:
        all_data (dict): Dictionary containing ship data under 'data' key.
        top (int, optional): Number of top countries to return. Defaults to 5.

    Returns:
        list of tuples: Each tuple contains (country_name, ship_count),
                        sorted by ship count in descending order.
    """
    country_dict = count_country_ship(all_data)
    country_dict_sorted = sorted(
        country_dict.items(),
        key=lambda item: item[1],
        reverse=True
    )
    return country_dict_sorted[:top]


def count_ship_by_types(all_data):
    """
    Count ships by their general type.

    Args:
        all_data (dict): Dictionary containing ship data.

    Returns:
        dict: Dictionary with ship types as keys and counts as values.
    """
    ship_type_dict = {}

    for ship in all_data['data']:
        ship_type = ship.get('TYPE_SUMMARY', 'Unknown')
        if ship_type in ship_type_dict:
            ship_type_dict[ship_type] += 1
        else:
            ship_type_dict[ship_type] = 1

    return ship_type_dict


def search_ship(all_data):
    """
    Search for ships by name inputted by user and print matches.

    Args:
        all_data (dict): Dictionary containing ship data.
    """
    user_input = input("Type the name of the ship you are looking for: ").lower()
    found = False

    for ship in all_data['data']:
        ship_name = ship.get('SHIPNAME', '').lower()
        if user_input in ship_name:
            print(
                f"\nFound: {ship.get('SHIPNAME')} (Country: {ship.get('COUNTRY')},"
                f" Type: {ship.get('TYPE_SUMMARY')})"
            )
            found = True

    if not found:
        print("No ship found with that name.")


def create_speed_histogram(all_data, filename="ship_speed_histogram.png"):
    """
    Create and save a histogram of ship speeds.

    Args:
        all_data (dict): Ship data dictionary.
        filename (str): Output filename for the histogram image.
    """
    speeds = []
    skipped = 0
    total = 0

    for ship in all_data['data']:
        total += 1
        speed = ship.get("SPEED")
        if speed is not None:
            try:
                speed = float(speed)
                if speed >= 0:
                    speeds.append(speed)
                else:
                    skipped += 1
            except ValueError:
                skipped += 1
        else:
            skipped += 1

    if not speeds:
        print("No valid speed data found.")
        return

    print(f"Processed {total} ships.")
    print(f"Valid speed entries: {len(speeds)}")
    print(f"Skipped entries: {skipped}")

    plt.figure(figsize=(10, 6))
    plt.hist(speeds, bins=20, color='skyblue', edgecolor='black')
    plt.title("Histogram of Ship Speeds")
    plt.xlabel("Speed (knots)")
    plt.ylabel("Number of Ships")
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
    print(f"Histogram saved to '{filename}'")


def draw_ship_map(all_data, filename="ship_map.png"):
    """
    Plot ship positions on a scatter plot and save the map to a file.

    Args:
        all_data (dict): Dictionary containing ship data.
        filename (str): Output filename for the map image.
    """
    lats = []
    lons = []
    total = 0
    skipped = 0

    for ship in all_data['data']:
        total += 1
        lat = ship.get("LAT")
        lon = ship.get("LON")

        if lat is not None and lon is not None:
            try:
                lat = float(lat)
                lon = float(lon)
                lats.append(lat)
                lons.append(lon)
            except ValueError:
                skipped += 1
        else:
            skipped += 1

    if not lats or not lons:
        print("No valid ship position data available.")
        return

    print(f"Processed {total} ships.")
    print(f"Valid position entries: {len(lats)}")
    print(f"Skipped entries: {skipped}")

    plt.figure(figsize=(12, 6))
    plt.scatter(lons, lats, s=5, alpha=0.6, color="blue", label="Ships")
    plt.title("Ship Positions on Map")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.legend()
    plt.savefig(filename)
    plt.close()
    print(f"Ship map saved as '{filename}'")


#========================= Create the dispatcher-compatible handler ===========================

def call_help(_all_data, _args):
    """
    Display a list of all available CLI commands.

    This function provides users with an overview of the supported
    commands and their expected arguments. It does not require any input
    arguments and is intended to assist users in navigating the CLI tool.
    """
    print("Available commands:")
    print("  help")
    print("  show_countries")
    print("  top_countries <num_countries>")
    print("  ships_by_types")
    print("  search_ship")
    print("  speed_histogram")
    print("  draw_map")
    print("  exit")


def call_show_countries(all_data, _args):
    """
    Display a list of all unique countries in the ship dataset.

    This function extracts all country entries from the loaded dataset,
    removes duplicates, sorts them alphabetically, and prints them one
    per line. It does not accept additional arguments.
    """
    _, country_unique = show_countries(all_data)
    for country in country_unique:
        print(country)


def call_top_countries(all_data, args):
    """
    Display the top N countries by number of ships.

    Args:
        all_data (dict): Dictionary containing ship metadata.
        args (list): List containing a single integer argument indicating
                     how many top countries to display.

    Behavior:
        - If no argument or an invalid argument is provided, an error
          message is shown.
        - Otherwise, prints a list of the top N countries sorted by the
          number of ships registered under each.
    """
    if len(args) != 1:
        print("Usage: top_countries <num_countries>")
        return

    if not args[0].isdigit():
        print("Error: The argument must be a positive integer.")
        return

    top_ranking = int(args[0])

    try:
        top_list = top_countries(all_data, top_ranking)
        print(f"\nTop {top_ranking} Countries by Ship Count:\n")
        for country, count in top_list:
            print(f"{country}: {count}")
    except Exception as e:
        print(f"Error: {e}")


def call_show_ship_types(all_data, args):
    """
    Display counts of ships grouped by their general type.

    Args:
        all_data (dict): Dictionary containing ship metadata.
        args (list): Should be empty; no arguments are expected.

    Behavior:
        - Prints a list of ship types (e.g., Cargo, Tanker) and their
          respective counts, sorted in descending order of frequency.
        - If any arguments are passed, an error message is displayed.
    """
    if args:
        print("Usage: ships_by_types (no arguments)")
        return
    ship_type_dict = count_ship_by_types(all_data)
    for ship_type, count in sorted(ship_type_dict.items(), key=lambda x: x[1], reverse=True):
        print(f"{ship_type}: {count}")


def call_search_ship(all_data, args):
    """
    Search for ships by name using user-provided input.

    Args:
        all_data (dict): Dictionary containing ship metadata.
        args (list): Should be empty; this function prompts the user
                     for a ship name via input().

    Behavior:
        - Prompts the user to type part or full name of a ship.
        - Performs a case-insensitive substring search.
        - Prints all matching ship names with country and type.
        - Informs the user if no matches are found.
    """
    if args:
        print("Usage: search_ship (no arguments)")
        return
    search_ship(all_data)


def call_speed_histogram(all_data, args):
    """
    Generate and save a histogram of ship speeds.

    Args:
        all_data (dict): Dictionary containing ship metadata.
        args (list): Optional list with a single filename (e.g., my_plot.png).
                     If no filename is provided, defaults to
                     'ship_speed_histogram.png'.

    Behavior:
        - Extracts ship speed values, filters invalid entries,
          and generates a histogram.
        - Saves the plot as an image file and displays summary
          statistics (processed, valid, skipped entries).
    """
    filename = "ship_speed_histogram.png"
    if len(args) == 1:
        filename = args[0]
    create_speed_histogram(all_data, filename)


def call_draw_map(all_data, args):
    """
    Generate and save a scatter plot of ship positions on a map.

    Args:
        all_data (dict): Dictionary containing ship metadata.
        args (list): Optional list with a single filename (e.g., ships_map.png).
                     If no filename is provided, defaults to 'ship_map.png'.

    Behavior:
        - Extracts latitude and longitude values from the dataset.
        - Skips invalid or missing entries with a summary report.
        - Saves a scatter plot image showing global ship positions.
    """
    filename = "ship_map.png"
    if len(args) == 1:
        filename = args[0]
    draw_ship_map(all_data, filename)


def exit_cli(_all_data, _args):
    """
    Exit the CLI tool gracefully.

    This function terminates the command-line interface and
    exits the program cleanly. Typically triggered by the
    user typing 'exit'.

    No arguments are required.
    """
    print("Exiting CLI.")
    raise SystemExit


#================================== DEFINE VISUALIZE FUNCTION ===========================

def visualize_cli(all_data):
    """
    Command-line interface to interact with ship data.

    Args:
        all_data (dict): Ship data.
    """
    dispatcher = {
        "help": call_help,
        "show_countries": call_show_countries,
        "top_countries": call_top_countries,
        "ships_by_types": call_show_ship_types,
        "search_ship": call_search_ship,
        "speed_histogram": call_speed_histogram,
        "draw_map": call_draw_map,
        "exit": exit_cli
    }

    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")
    try:
        while True:
            user_input = input("> ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            handler = dispatcher.get(command)
            if handler:
                handler(all_data, args)
            else:
                print("Unknown command. Type 'help' to see available commands.")

    except KeyboardInterrupt:
        print("\nCLI interrupted. Exiting.")
    except SystemExit:
        pass  # clean exit from 'exit' command


#================================== DEFINE MAIN FUNCTION ===========================

def main():
    """
    Main entry point to load data and start CLI.
    """
    all_data = load_data()
    visualize_cli(all_data)


if __name__ == "__main__":
    main()


