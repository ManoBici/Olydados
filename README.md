# 🏅 OlyDados — Olympic Games Data Explorer

A Python desktop application built to explore, filter, and visualize historical Olympic Games data (1896–2016) in a simple, clear, and objective way.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f6aa5?style=flat)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Charts-Matplotlib-11557c?style=flat)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📖 About the Project

**OlyDados** transforms public Olympic Games historical data into an intuitive dark-mode desktop experience. From the home screen, users can jump straight into a paginated data explorer to filter individual records or open an analytical dashboard for a high-level visual overview of Olympic history.

---

## 📸 Preview

### Home Screen
![Home Screen](https://github.com/user-attachments/assets/ce8206de-37a3-4900-8172-94ff28ae97b4)

### Data Explorer & Interactive Dashboard
![Data Explorer](https://github.com/user-attachments/assets/b089fc9e-69a9-4aee-90c8-40150ce74c2b)

![Analytics Dashboard](https://github.com/user-attachments/assets/fba367ce-bfaf-41c3-b6f6-5b3454089b30)

---

## ✨ Features

- **Modern Home Interface (`main.py`)**: Dark theme with custom-drawn Olympic rings, feature highlights, and quick navigation between modules.
- **Data Exploration & Filtering (`data_explorer.py`)**:
  - Dynamically filter records by **Country**, **Sport**, **Medal Type** (`Gold`, `Silver`, `Bronze`, `NA`), and **Year**.
  - Color-coded medal cells and paginated results table (30 records per page) with live record counters.
- **Interactive Analytics Dashboard (`dashboard.py`)**:
  - **Summary KPI Cards**: Total medals awarded, participating nations, sports competed, and athletes in the most recent edition.
  - **Games Evolution Chart**: Dual-axis line chart tracking athletes and participating countries over time.
  - **Gender Distribution**: Pie chart comparing unique male and female athletes.
  - **Top 10 Countries**: Grouped bar chart ranking nations by Gold, Silver, and Bronze medals.
  - **Interactive Host Cities Globe**: Orthographic world map with hover tooltips for Summer Olympics host cities *(powered by Cartopy, gracefully skipped if not installed)*.
  - **Top Sports & Recent Editions**: Dynamic SQLite breakdown of top medal-awarding sports, iconic Olympic highlights, and summaries of the latest editions.
- **CSV-to-SQLite Loader (`database.py`)**: Automatically creates and populates the local `banco.db` SQLite database from `banco.csv`.
- **Flask Web Interface (`app.py`)**: Lightweight web interface for querying the same SQLite database by any column.

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Desktop UI:** CustomTkinter & Tkinter
- **Data Visualization:** Matplotlib, NumPy, Cartopy & Shapely *(optional, for the globe map)*
- **Database:** SQLite (`sqlite3`)
- **Web Interface:** Flask (`app.py` + `templates/index.html`)
- **Data Source:** Public Kaggle Olympic Games Dataset (1896–2016)

---

## 📂 Project Structure

```text
Olydados/
├── main.py              # Main entry point (Home screen & navigation)
├── data_explorer.py     # Paginated data exploration & multi-filter view
├── dashboard.py         # Analytics dashboard with charts & world map
├── database.py          # Script to convert banco.csv into banco.db (SQLite)
├── app.py               # Optional Flask web search interface
├── templates/
│   └── index.html       # HTML template for the Flask interface
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
└── README.md            # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- An Olympic Games CSV dataset named `banco.csv` placed in the project root (with columns such as `ano`, `edicao`, `cidade_sede`, `pais`, `delegacao`, `equipe`, `id_atleta`, `nome_atleta`, `sexo`, `idade`, `altura`, `peso`, `esporte`, `evento`, `medalha`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ManoBici/Olydados.git
   cd Olydados
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** `cartopy` and `shapely` are optional and only required for the interactive host cities globe map on the dashboard. If they are unavailable on your system, you can install the core packages with `pip install customtkinter matplotlib numpy flask`.

3. Generate the SQLite database (`banco.db`) from `banco.csv`:
   ```bash
   python database.py
   ```

### Running the Application

Launch the desktop application:
```bash
python main.py
```

*(Optional)* Run the Flask web search interface:
```bash
python app.py
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
