# 🚢 Ship Data CLI

A command-line interface (CLI) tool for exploring and analyzing maritime ship data. Built with Python, 
this tool allows you to search, summarize, and visualize ship metadata and movement data using simple commands.

---

## 📌 Features

- `help` — List all available commands
- `show_countries` — Display all unique countries represented in the dataset
- `top_countries <N>` — Show top N countries by number of ships
- `ships_by_types` — Display ship types and their respective counts
- `search_ship` — Search for ships by name (case-insensitive, partial match)
- `speed_histogram [filename]` — Generate and save a histogram of ship speeds
- `draw_map [filename]` — Plot ship positions (LAT/LON) on a world map
- `exit` — Exit the CLI

---

## 🗃️ Dataset Assumption

The tool assumes a preloaded dataset in the form of a Python dictionary structured like this:

```python
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
The data should be loaded via the load_data() function defined in a separate module called load_data.py.
```
## 🛠️ Installation

### 1.Clone the repository:
```python
git clone https://github.com/yourusername/ship-data-cli.git
cd ship-data-cli
```
### Install required dependencies:
```python
pip install matplotlib
```

## ▶️ Running the CLI

### 1.Run the main script:
```python
python main.py
```
Once inside the CLI, you can type any of the supported commands, such as:
```python
> help
> top_countries 5
> search_ship
> speed_histogram speeds.png
> draw_map map.png
```
## 💡 Implementation Highlights
- Dispatcher Pattern: The tool uses the dispatcher pattern instead of long if-elif chains, 
improving scalability and readability. Each command is mapped to a corresponding handler 
function through a centralized dispatcher dictionary.

- Interactive Design: The CLI is designed to be interactive, user-friendly, and 
extendable — ideal for iterative data exploration and prototyping.

- Data Visualization: Uses Matplotlib to generate and save histogram and map plots 
for better insights into ship speeds and global distribution.

## 📁 Project Structure
```python
ship-data-cli/
│
├── main.py               # Entry point to run the CLI
├── load_data.py          # Module to load ship data
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies (optional)
└── example_data.json     # Sample dataset (optional)

```
## 📋 Notes
- Ensure your dataset follows the expected format.
- The visual output files (e.g., ship_speed_histogram.png, ship_map.png) will be saved in
the current working directory.
- This tool is ideal for small-to-medium datasets. For larger datasets, consider optimizing
file loading and processing further.

## 🙋‍♂️ Author
**Abhisakh Sarma**  
GitHub: [https://github.com/abhisakh](https://github.com/abhisakh)  
_Contributions and feedback are always welcome!_
