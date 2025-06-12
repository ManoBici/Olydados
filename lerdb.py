import sqlite3
import tkinter as tk
from tkinter import ttk

# === Função para buscar dados com filtros ===
def buscar_dados():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()

    filtros = []
    valores = []

    pais = combo_pais.get()
    if pais != "Todos":
        filtros.append("pais = ?")
        valores.append(pais)

    esporte = combo_esporte.get()
    if esporte != "Todos":
        filtros.append("esporte = ?")
        valores.append(esporte)

   

    query = "SELECT * FROM nome_atleta"
    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    cursor.execute(query, valores)
    registros = cursor.fetchall()
    atualizar_tabela(registros)
    conn.close()

# === Função para atualizar a tabela ===
def atualizar_tabela(registros):
    for item in tree.get_children():
        tree.delete(item)
    for row in registros:
        tree.insert("", "end", values=row)

        
# === Interface gráfica ===
root = tk.Tk()
root.title("Análise Olímpica")
root.geometry("600x400")

# --- Filtro por país ---
tk.Label(root, text="Filtrar por país:").pack()
combo_pais = ttk.Combobox(root, values=["Todos", 'Australia', 'Austria', 'Denmark', 'France', 'Germany', 'Greece',
        'Hungary', 'Italy', 'Sweden', 'Switzerland', 'UK', 'USA',
        'Argentina', 'Belgium', 'Brazil', 'Canada', 'Colombia', 'Cuba',
        'Czech Republic', 'Haiti', 'India', 'Iran', 'Luxembourg', 'Mexico',
        'Netherlands', 'New Zealand', 'Norway', 'Peru', 'Romania',
        'Russia', 'Spain', 'South Africa', 'Egypt', 'Finland', 'Turkey',
        'Iceland', 'Chile', 'Japan', 'Poland', 'Portugal', 'Serbia',
        'Estonia', 'Monaco', 'Bulgaria', 'Ecuador', 'Ireland', 'Latvia',
        'Lithuania', 'Philippines', 'Uruguay', 'Nepal', 'Malta', 'Panama',
        'Zimbabwe', 'China', 'El Salvador', 'Guatemala', 'Venezuela',
        'Afghanistan', 'Bermuda', 'Boliva', 'Costa Rica', 'Liechtenstein',
        'Guyana', 'Iraq', 'Jamaica', 'Lebanon', 'Myanmar', 'Pakistan',
        'Puerto Rico', 'South Korea', 'Sri Lanka', 'Syria', 'Trinidad',
        'Bahamas', 'Curacao', 'Ghana', 'Indonesia', 'Israel', 'Nigeria',
        'Thailand', 'Vietnam', 'Cambodia', 'Ethiopia', 'Fiji', 'Kenya',
        'Liberia', 'Malaysia', 'Taiwan', 'Uganda', 'Morocco', 'San Marino',
        'Sudan', 'Tunisia', 'Algeria', 'Cameroon', 'Chad',
        'Dominican Republic', 'Ivory Coast', 'Madagascar', 'Mali',
        'Mongolia', 'Niger', 'Republic of Congo', 'Senegal', 'Tanzania',
        'Zambia', 'North Korea', 'Barbados', 'Belize',
        'Central African Republic', 'Democratic Republic of the Congo',
        'Guinea', 'Honduras', 'Kuwait', 'Libya', 'Nicaragua', 'Paraguay',
        'Sierra Leone', 'Suriname', 'Virgin Islands, US', 'Albania',
        'Benin', 'Burkina Faso', 'Gabon', 'Lesotho', 'Malawi',
        'Saudi Arabia', 'Somalia', 'Swaziland', 'Togo', 'Andorra',
        'Antigua', 'Cayman Islands', 'Papua New Guinea', 'Angola',
        'Botswana', 'Cyprus', 'Jordan', 'Laos', 'Mozambique', 'Seychelles',
        'Bahrain', 'Bangladesh', 'Bhutan', 'Djibouti', 'Equatorial Guinea',
        'Gambia', 'Grenada', 'Mauritania', 'Mauritius', 'Oman', 'Qatar',
        'Rwanda', 'Samoa', 'Solomon Islands', 'Tonga',
        'United Arab Emirates', 'Virgin Islands, British', 'Yemen',
        'American Samoa', 'Aruba', 'Cook Islands', 'Guam', 'Maldives',
        'Saint Vincent', 'Vanuatu', 'Bosnia and Herzegovina', 'Croatia',
        'Individual Olympic Athletes', 'Namibia', 'Slovenia', 'Armenia',
        'Belarus', 'Georgia', 'Kazakhstan', 'Kyrgyzstan', 'Moldova',
        'Slovakia', 'Ukraine', 'Uzbekistan', 'Azerbaijan', 'Brunei',
        'Burundi', 'Cape Verde', 'Comoros', 'Dominica', 'Guinea-Bissau',
        'Macedonia', 'Nauru', 'Palestine', 'Saint Kitts', 'Saint Lucia',
        'Sao Tome and Principe', 'Tajikistan', 'Turkmenistan', 'Eritrea',
        'Micronesia', 'Palau', 'Kiribati', 'Timor-Leste',
        'Marshall Islands', 'Montenegro', 'Kosovo', 'South Sudan'])
combo_pais.current(0)
combo_pais.pack()

# --- Filtro por esporte ---
tk.Label(root, text="Filtrar por esporte:").pack()
combo_esporte = ttk.Combobox(root, values=["Todos", 'Athletics', 'Tennis', 'Swimming', 'Cycling', 'Fencing',
        'Gymnastics', 'Shooting', 'Weightlifting', 'Wrestling',
        'Equestrianism', 'Rowing', 'Water Polo', 'Football', 'Archery',
        'Tug-Of-War', 'Rugby', 'Sailing', 'Cricket', 'Croquet', 'Polo',
        'Golf', 'Basque Pelota', 'Lacrosse', 'Diving', 'Boxing', 'Roque',
        'Figure Skating', 'Hockey', 'Motorboating', 'Racquets',
        'Jeu De Paume', 'Modern Pentathlon', 'Art Competitions',
        'Ice Hockey', 'Alpinism', 'Speed Skating', 'Bobsleigh',
        'Nordic Combined', 'Military Ski Patrol', 'Ski Jumping',
        'Cross Country Skiing', 'Curling', 'Skeleton', 'Handball',
        'Canoeing', 'Basketball', 'Aeronautics', 'Alpine Skiing',
        'Biathlon', 'Judo', 'Volleyball', 'Luge', 'Synchronized Swimming',
        'Rhythmic Gymnastics', 'Table Tennis', 'Badminton', 'Baseball',
        'Freestyle Skiing', 'Short Track Speed Skating',
        'Beach Volleyball', 'Softball', 'Snowboarding', 'Trampolining',
        'Triathlon', 'Taekwondo', 'Rugby Sevens'])
combo_esporte.current(0)
combo_esporte.pack()

# --- Botão buscar ---
btn_buscar = tk.Button(root, text="Buscar", command=buscar_dados)
btn_buscar.pack(pady=10)

# --- Tabela de resultados ---
colunas = ("ID", "Nome", "Esporte", "País", "Medalhas")
tree = ttk.Treeview(root, columns=colunas, show="headings")
for col in colunas:
    tree.heading(col, text=col)
tree.pack(expand=True, fill='both')

buscar_dados()  # Carrega tudo no início
root.mainloop()
