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
        all_data (dict): Dictionary containing ship data.
        filename (str, optional): Output file name. Defaults to "ship_speed_histogram.png".
    """
    speeds = []

    for ship in all_data['data']:
        speed = ship.get("SPEED")
        if speed is not None:
            try:
                speed = float(speed)
                if speed >= 0:  # skip invalid negative speeds
                    speeds.append(speed)
            except ValueError:
                continue  # skip non-numeric speed values

    if not speeds:
        print("No valid speed data found.")
        return

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
    Plot ship positions on a scatter plot map and save to a file.

    Args:
        all_data (dict): Dictionary containing ship data.
        filename (str, optional): Output file name. Defaults to "ship_map.png".
    """
    lats = []
    lons = []

    for ship in all_data['data']:
        lat = ship.get("LAT")
        lon = ship.get("LON")

        if lat is not None and lon is not None:
            try:
                lat = float(lat)
                lon = float(lon)
                lats.append(lat)
                lons.append(lon)
            except ValueError:
                continue

    if not lats or not lons:
        print("No valid ship position data available.")
        return

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
    """Print list of available commands."""
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
    """Print all unique countries."""
    _, country_unique = show_countries(all_data)
    for country in country_unique:
        print(country)


def call_top_countries(all_data, args):
    """Print top countries by number of ships."""
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
    """Print counts of ships by type."""
    if args:
        print("Usage: ships_by_types (no arguments)")
        return
    ship_type_dict = count_ship_by_types(all_data)
    for ship_type, count in sorted(ship_type_dict.items(), key=lambda x: x[1], reverse=True):
        print(f"{ship_type}: {count}")


def call_search_ship(all_data, args):
    """Prompt for ship name and search."""
    if args:
        print("Usage: search_ship (no arguments)")
        return
    search_ship(all_data)


def call_speed_histogram(all_data, args):
    """Create a speed histogram and save to file."""
    filename = "ship_speed_histogram.png"
    if len(args) == 1:
        filename = args[0]
    create_speed_histogram(all_data, filename)


def call_draw_map(all_data, args):
    """Draw ship map and save to file."""
    filename = "ship_map.png"
    if len(args) == 1:
        filename = args[0]
    draw_ship_map(all_data, filename)


def exit_cli(_all_data, _args):
    """Exit the CLI."""
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


