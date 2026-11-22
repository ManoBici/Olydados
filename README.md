# 🏅 OlyDados — Olympic Games Data Explorer

A Python desktop application built to explore, filter, and visualize historical Olympic Games data (1896–2016) in a simple, clear, and objective way.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f6aa5?style=flat)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Charts-Matplotlib-11557c?style=flat)

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

- **Modern Home Interface (`pag_inicial.py`)**: Dark theme with custom-drawn Olympic rings, feature highlights, and quick navigation between modules.
- **Data Exploration & Filtering (`tela_exploracao_dados.py`)**:
  - Dynamically filter records by **Country**, **Sport**, **Medal Type** (`Gold`, `Silver`, `Bronze`, `NA`), and **Year**.
  - Color-coded medal cells and paginated results table (30 records per page) with live record counters.
- **Interactive Analytics Dashboard (`tela_dashboard.py`)**:
  - **Summary KPI Cards**: Total medals awarded, participating nations, sports competed, and athletes in the most recent edition.
  - **Games Evolution Chart**: Dual-axis line chart tracking athletes and participating countries over time.
  - **Gender Distribution**: Pie chart comparing unique male and female athletes.
  - **Top 10 Countries**: Grouped bar chart ranking nations by Gold, Silver, and Bronze medals.
  - **Interactive Host Cities Globe**: Orthographic world map with hover tooltips for Summer Olympics host cities *(powered by Cartopy, gracefully skipped if not installed)*.
  - **Top Sports & Recent Editions**: Dynamic SQLite breakdown of top medal-awarding sports, iconic Olympic highlights, and summaries of the latest editions.
- **CSV-to-SQLite Loader (`DATABASE.PY`)**: Automatically creates and populates the local `banco.db` SQLite database from `banco.csv`.
- **Flask Web Prototype (`app.PY`)**: Lightweight web interface for querying the same SQLite database by any column.

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Desktop UI:** CustomTkinter & Tkinter
- **Data Visualization:** Matplotlib, NumPy, Cartopy & Shapely *(optional, for the globe map)*
- **Database:** SQLite (`sqlite3`)
- **Web Prototype:** Flask (`app.PY` + `templates/index.html`)
- **Data Source:** Public Kaggle Olympic Games Dataset (1896–2016)

---

## 📂 Project Structure

```text
Olydados-main/
├── pag_inicial.py            # Main entry point (Home screen & navigation)
├── tela_exploracao_dados.py  # Paginated data exploration & multi-filter view
├── tela_dashboard.py         # Analytics dashboard with charts & world map
├── DATABASE.PY               # Script to convert banco.csv into banco.db (SQLite)
├── app.PY                    # Optional Flask web search interface
├── templates/
│   └── index.html            # HTML template for the Flask interface
├── dash.py                   # Standalone dashboard prototype
├── tabela_filtragem.py       # Standalone filter table prototype
└── lerdb.py                  # Early Tkinter SQLite viewer prototype
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- An Olympic Games CSV dataset named `banco.csv` placed in the project root (with columns such as `ano`, `edicao`, `cidade_sede`, `pais`, `delegacao`, `equipe`, `id_atleta`, `nome_atleta`, `sexo`, `idade`, `altura`, `peso`, `esporte`, `evento`, `medalha`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Olydados.git
   cd Olydados
   ```

2. Install the required dependencies:
   ```bash
   pip install customtkinter matplotlib numpy
   ```

3. *(Optional)* Install **Cartopy** and **Shapely** to enable the interactive host cities globe map in the dashboard:
   ```bash
   pip install cartopy shapely
   ```

4. Generate the SQLite database (`banco.db`) from `banco.csv`:
   ```bash
   python DATABASE.PY
   ```

### Running the Application

Launch the desktop application:
```bash
python pag_inicial.py
```

*(Optional)* To run the Flask web query prototype:
```bash
pip install flask
python app.PY
```

---

## 📄 License

This project is open source and available for educational and portfolio purposes.
