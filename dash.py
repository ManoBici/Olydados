import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Ativa o modo escuro do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Dados das edições dos Jogos Olímpicos (para gráfico de linha)
anos_olimpiadas = [1896, 1900, 1904, 1908, 1912, 1920, 1924, 1928, 1932, 1936,
                   1948, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984,
                   1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016]

atletas = [241, 1226, 651, 2008, 2407, 2626, 3089, 2883, 1332, 3963, 4104,
           4955, 3314, 5338, 5151, 5516, 7134, 6084, 5179, 6829, 8391, 9356,
           10318, 10651, 10625, 10942, 10568, 11238]

paises_olimpiadas = [14, 26, 12, 22, 28, 29, 44, 46, 37, 49, 59, 69, 72, 83,
                     93, 112, 121, 92, 80, 140, 159, 169, 197, 199, 201, 204,
                     204, 207]

# Dados para gráfico de barras de medalhas por país
paises = [
    "Estados Unidos", "União Soviética", "Grã-Bretanha", "França", "China",
    "Itália", "Alemanha", "Hungria", "Alemanha Oriental", "Rússia"
]
ouro = [1022, 395, 263, 212, 224, 206, 191, 175, 153, 149]
prata = [795, 319, 295, 241, 167, 178, 194, 147, 129, 125]
bronze = [705, 296, 293, 263, 155, 193, 230, 169, 127, 154]

# Cores da interface
bg_color = "#181C27"  # Cor do fundo da janela e gráfico
card_color = "#232737"

# Criação da janela principal
app = ctk.CTk()
app.title("Painel de Dados Olímpicos")
app.geometry("1200x900")  # Ajustado para melhor proporção
app.state("zoomed")  # Maximiza janela ao abrir (Windows)

# Frame rolável
scrollable_frame = ctk.CTkScrollableFrame(master=app, fg_color=bg_color)
scrollable_frame.pack(fill="both", expand=True)

#Rodapé

#expansão das colunas do scrollable_frame
for col in range(4):
    scrollable_frame.columnconfigure(col, weight=1)

# Rodapé
footer_frame = ctk.CTkFrame(scrollable_frame, height=100, fg_color="#1a2233", corner_radius=0)
footer_frame.grid(row=999, column=0, columnspan=4, sticky="ew", pady=0, padx=0)

# Canvas dos anéis olímpicos
canvas_aneis = tk.Canvas(footer_frame, width=280, height=80, bg="#1a2233", highlightthickness=0)
canvas_aneis.pack(side="left", padx=10, pady=20)

# Parâmetros dos anéis
raio = 20
espaco = 10
y = 35  # altura central dos círculos

cores = ["#0085C7", "#000000", "#DF0024", "#F4C300", "#009F3D"]
posicoes_x = [raio, raio*2 + espaco, raio*4 + espaco*2, raio*3 + espaco, raio*5 + espaco*3]
espessura = 4

canvas_aneis.create_oval(posicoes_x[0]-raio, y-raio, posicoes_x[0]+raio, y+raio, outline=cores[0], width=espessura)
canvas_aneis.create_oval(posicoes_x[1]-raio, y-raio, posicoes_x[1]+raio, y+raio, outline=cores[1], width=espessura)
canvas_aneis.create_oval(posicoes_x[2]-raio, y-raio, posicoes_x[2]+raio, y+raio, outline=cores[2], width=espessura)
canvas_aneis.create_oval(posicoes_x[3]-raio, y+10-raio, posicoes_x[3]+raio, y+10+raio, outline=cores[3], width=espessura)
canvas_aneis.create_oval(posicoes_x[4]-raio, y+10-raio, posicoes_x[4]+raio, y+10+raio, outline=cores[4], width=espessura)

# Texto do rodapé
footer_text = "© 2025 Painel Olímpico - Todos os direitos reservados\n Dados coletados pelo dataset olímpico público (1896-2016) do kaggle"
footer_label = ctk.CTkLabel(footer_frame, text=footer_text,
                            font=("Arial", 11),
                            text_color="#A7FF4E",
                            fg_color="transparent")
footer_label.pack(side="left", padx=15, pady=10)


#titulo da pagina inical
label_titulo = ctk.CTkLabel(scrollable_frame, text="Painel de dados olímpicos",
                            font=("Arial", 20, "bold"), text_color="#D2FF28",
                            fg_color="transparent")
label_titulo.grid(row=0, column=0, columnspan=4, pady=(35, 30), padx=(50, 0), sticky="w")

# Cards de métricas
card_data = [
    ("Medalhas Distruídas", "15.683", "Desde 1896"),
    ("Países", "206", "Participando"),
    ("Esportes", "42", "em 2016"),
    ("Atletas", "100.000+", "Desde 1896")
]

for i, (title, value, desc) in enumerate(card_data):
    frame = ctk.CTkFrame(scrollable_frame, width=250, height=90,
                         fg_color=card_color, corner_radius=10)
    # Adiciona padx=50 na primeira coluna para alinhar com o título
    if i == 0:
        frame.grid(row=1, column=i, padx=(50, 10), sticky="w")
    else:
        frame.grid(row=1, column=i, padx=10, sticky="w")
    ctk.CTkLabel(frame, text=title, font=("Arial", 14, "bold"),
                 text_color="white", fg_color="transparent").place(x=15, y=10)
    ctk.CTkLabel(frame, text=value, font=("Arial", 26, "bold"),
                 text_color="#D2FF28" if i == 0 else "#A7FF4E" if i == 1 else "#D2FF28",
                 fg_color="transparent").place(x=15, y=35)
    ctk.CTkLabel(frame, text=desc, font=("Arial", 11), text_color="gray",
                 fg_color="transparent").place(x=15, y=65)

# Frame container para os gráficos lado a lado (2 colunas)
frame_graficos = ctk.CTkFrame(scrollable_frame, fg_color=bg_color)
frame_graficos.grid(row=2, column=0, columnspan=4, pady=(90, 20), padx=50, sticky="nsew")
frame_graficos.grid_columnconfigure(0, weight=1)
frame_graficos.grid_columnconfigure(1, weight=1)
frame_graficos.grid_rowconfigure(0, weight=1)

#Gráfico 2: evolução dos Jogos Olímpicos (anos, atletas, países) com eixo y duplo ---
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fig2 = Figure(figsize=(7.5, 6), dpi=100)
ax2 = fig2.add_subplot(111)

cor_atletas = '#D2FF28'  # Amarelo-limão
cor_paises = 'orange'    # Laranja

l1, = ax2.plot(anos_olimpiadas, atletas, marker='o', label="Número de Atletas", color=cor_atletas)
ax2.set_ylabel("Número de Atletas", color=cor_atletas)
ax2.tick_params(axis='y', colors=cor_atletas)

ax3 = ax2.twinx()
l2, = ax3.plot(anos_olimpiadas, paises_olimpiadas, marker='s', label="Número de Países", color=cor_paises)
ax3.set_ylabel("Número de Países", color=cor_paises)
ax3.tick_params(axis='y', colors=cor_paises)

ax2.set_title("Evolução do Número de Atletas e Países Participantes", color='white')
ax2.set_xlabel("Ano", color='white')
ax2.tick_params(axis='x', colors='white')

fig2.patch.set_facecolor(bg_color)
ax2.set_facecolor(bg_color)
ax3.set_facecolor(bg_color)

lines = [l1, l2]
labels = [line.get_label() for line in lines]
ax2.legend(lines, labels, facecolor=card_color, edgecolor='white', labelcolor='white')

ax2.grid(True, color='gray', linestyle='--', alpha=0.3)

fig2.tight_layout()

canvas2 = FigureCanvasTkAgg(fig2, master=frame_graficos)
canvas2.draw()
canvas2.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# --- Gráfico 1: barras por país ---
x = np.arange(len(paises))
width = 0.2

fig1, ax1 = plt.subplots(figsize=(7.5, 6), dpi=100)
bars_ouro = ax1.bar(x - width, ouro, width, label='Ouro', color='gold')
bars_prata = ax1.bar(x, prata, width, label='Prata', color='silver')
bars_bronze = ax1.bar(x + width, bronze, width, label='Bronze', color='#cd7f32')

fig1.patch.set_facecolor(bg_color)
ax1.set_facecolor(bg_color)
ax1.set_title("Distribuição de medalhas por país", color='white')
ax1.set_ylabel('Número de Medalhas', color='white')
ax1.set_xticks(x)
ax1.set_xticklabels(paises, rotation=45, ha='right', color='white')
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')
ax1.legend(facecolor=card_color, edgecolor='white', labelcolor='white')

fig1.tight_layout()

canvas1 = FigureCanvasTkAgg(fig1, master=frame_graficos)
canvas1.draw()
canvas1.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=(230, 0))

# mapa
frame_mapa = ctk.CTkFrame(scrollable_frame, fg_color=bg_color)
frame_mapa.grid(row=3, column=0, columnspan=4, pady=(40, 60), padx=(50, 0), sticky="w")
frame_mapa.grid_columnconfigure(0, weight=1)
frame_mapa.grid_rowconfigure(0, weight=1)

#mapa com Cartopy usando projeção ortográfica (globo)
fig_map = plt.figure(figsize=(8, 7), dpi=100)  # largura maior, altura menor para ampliar horizontalmente
ax_map = fig_map.add_subplot(1, 1, 1, projection=ccrs.Orthographic(central_longitude=0, central_latitude=25))

ax_map.set_global()
ax_map.coastlines()
ax_map.add_feature(cfeature.BORDERS, edgecolor='gray')
ax_map.add_feature(cfeature.LAND, facecolor='lightgray')
ax_map.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax_map.add_feature(cfeature.LAKES, facecolor='lightblue')
ax_map.add_feature(cfeature.RIVERS, edgecolor='lightblue')

# Lista das cidades-sede dos Jogos Olímpicos de Verão e suas coordenadas aproximadas
cidades = {
    "Atenas": (37.9838, 23.7275),
    "Paris": (48.8566, 2.3522),
    "St. Louis": (38.6270, -90.1994),
    "Londres": (51.5074, -0.1278),
    "Estocolmo": (59.3293, 18.0686),
    "Antuérpia": (51.2194, 4.4025),
    "Amsterdã": (52.3676, 4.9041),
    "Los Angeles": (34.0522, -118.2437),
    "Berlim": (52.5200, 13.4050),
    "Helsinque": (60.1695, 24.9354),
    "Melbourne": (-37.8136, 144.9631),
    "Roma": (41.9028, 12.4964),
    "Tóquio": (35.6895, 139.6917),
    "Cidade do México": (19.4326, -99.1332),
    "Munique": (48.1351, 11.5820),
    "Montreal": (45.5017, -73.5673),
    "Moscou": (55.7558, 37.6173),
    "Seul": (37.5665, 126.9780),
    "Barcelona": (41.3851, 2.1734),
    "Atlanta": (33.7490, -84.3880),
    "Sydney": (-33.8688, 151.2093),
    "Pequim": (39.9042, 116.4074),
    "Rio de Janeiro": (-22.9035, -43.2096)  # Coordenadas corrigidas
}

# Deslocamentos maiores para evitar sobreposição dos nomes (graus)
offsets = {
    "Atenas": (10, 5),
    "Paris": (10, 10),
    "St. Louis": (15, 7),
    "Londres": (10, -8),
    "Estocolmo": (8, 5),
    "Antuérpia": (10, 2),
    "Amsterdã": (10, -7),
    "Los Angeles": (15, 8),
    "Berlim": (10, 8),
    "Helsinque": (8, -8),
    "Melbourne": (15, 5),
    "Roma": (15, 5),
    "Tóquio": (10, 5),
    "Cidade do México": (10, -7),
    "Munique": (10, -8),
    "Montreal": (15, -5),
    "Moscou": (15, 5),
    "Seul": (10, -5),
    "Barcelona": (15, 7),
    "Atlanta": (18, 5),
    "Sydney": (15, -7),
    "Pequim": (18, -5),
    "Rio de Janeiro": (15, -7)
}

for cidade, (lat, lon) in cidades.items():
    ax_map.plot(lon, lat, marker='o', color='red', markersize=8, transform=ccrs.Geodetic())
    dx, dy = offsets.get(cidade, (5, 3))
    ax_map.text(lon + dx, lat + dy, cidade, fontsize=10, fontweight='bold', color='darkred', transform=ccrs.Geodetic())

ax_map.set_title('Cidades que Sediaram os Jogos Olímpicos de Verão (1896-2016)', fontsize=16, color='black')

fig_map.patch.set_facecolor(bg_color)
ax_map.set_facecolor(bg_color)

canvas_map = FigureCanvasTkAgg(fig_map, master=frame_mapa)
canvas_map.draw()
canvas_map.get_tk_widget().pack(fill="both", expand=True, anchor="w")

#Bloco de cards

# Frame container principal para os cards e destaques
frame_cards_destaques = ctk.CTkFrame(scrollable_frame, fg_color=bg_color)
frame_cards_destaques.grid(row=4, column=0, columnspan=4, pady=(10, 0), padx=(50, 0), sticky="w")

# Esportes com mais medalhas
frame_esportes = ctk.CTkFrame(frame_cards_destaques, fg_color=card_color, width=620, height=370, corner_radius=10)
frame_esportes.grid(row=0, column=0, padx=(30, 30), pady=(0,10), sticky="nw")
ctk.CTkLabel(frame_esportes, text="Esportes com mais medalhas", font=("Arial", 15, "bold"),
             text_color="#D2FF28", fg_color="transparent").place(x=15, y=10)

# Tabela dos esportes
esportes = [
    ("Atletismo", "125", "3.952"),
    ("Natação", "77", "2.932"),
    ("Ginástica", "58", "1.214"),
    ("Esqui Cross-Country", "42", "987"),
    ("Patinação de Velocidade", "39", "923")
]
ctk.CTkLabel(frame_esportes, text="ESPORTE", font=("Arial", 12, "bold"), text_color="white", width=120, anchor="w").place(x=15, y=47)
ctk.CTkLabel(frame_esportes, text="EVENTOS", font=("Arial", 12, "bold"), text_color="white", width=70, anchor="w").place(x=160, y=47)
ctk.CTkLabel(frame_esportes, text="MEDALHAS", font=("Arial", 12, "bold"), text_color="white", width=90, anchor="w").place(x=260, y=47)
for i, (esp, ev, med) in enumerate(esportes):
    y = 72+ i*40
    ctk.CTkLabel(frame_esportes, text=esp, font=("Arial", 12), text_color="white", width=120, anchor="w").place(x=15, y=y)
    ctk.CTkLabel(frame_esportes, text=ev, font=("Arial", 12), text_color="white", width=70, anchor="w").place(x=160, y=y)
    ctk.CTkLabel(frame_esportes, text=med, font=("Arial", 12), text_color="white", width=90, anchor="w").place(x=260, y=y)
    if i < len(esportes):
        linha = tk.Canvas(frame_esportes, width=570, height=1, bg=card_color, highlightthickness=0)
        linha.create_line(0, 0, 570, 0, fill="#31374a", width=1)
        linha.place(x=15, y=y + 28)



# Destaques Olímpicos
frame_destaques = ctk.CTkFrame(frame_cards_destaques, fg_color=card_color, width=620, height=370, corner_radius=10)
frame_destaques.grid(row=0, column=1, padx=(90, 0), pady=0, sticky="nw")
ctk.CTkLabel(frame_destaques, text="Destaques Olímpicos", font=("Arial", 15, "bold"),
             text_color="#D2FF28", fg_color="transparent").place(x=15, y=10)

destaques = [
    ("Michael Phelps", "28 medalhas (23 de ouro) em Natação"),
    ("Usain Bolt", "8 medalhas de ouro no Atletismo"),
    ("Seleção Brasileira Feminina", "Primeiro ouro olímpico em Tóquio 2020"),
    ("Nadia Comăneci", "Primeiro 10 perfeito em Ginástica (1976)")
]
for i, (nome, desc) in enumerate(destaques):
    y_nome = 50 + i*55  # espaçamento vertical aumentado para 55
    y_desc = 70 + i*55
    ctk.CTkLabel(frame_destaques, text=nome, font=("Arial", 13, "bold"), text_color="#D2FF28").place(x=15, y=y_nome)
    ctk.CTkLabel(frame_destaques, text=desc, font=("Arial", 11), text_color="white").place(x=15, y=y_desc)
    if i < len(destaques):
        linha = tk.Canvas(frame_destaques, width=570, height=1, bg=card_color, highlightthickness=0)
        linha.create_line(0, 0, 570, 0, fill="#31374a", width=1)
        linha.place(x=15, y=y_desc + 25)


#Eventos Olímpicos Recentes
frame_eventos = ctk.CTkFrame(scrollable_frame, fg_color=bg_color)
frame_eventos.grid(row=5, column=0, columnspan=4, pady=(20, 40), padx=(82, 0), sticky="w")

ctk.CTkLabel(frame_eventos, text="Eventos Olímpicos", font=("Arial", 15, "bold"),
             text_color="#D2FF28", fg_color="transparent").grid(row=0, column=0, columnspan=3, sticky="w", pady=(30, 10))

# Cards dos eventos
eventos = [
    # (Título, Subtítulo, Detalhes, Cor do card)
    ("Pequim 2008", "302 eventos em 28 esportes\n08 de agosto - 24 de agosto 2008", "204 Países  10.942 Atletas  958 Medalhas", "#1a2233"),
    ("Londres 2012", "302 eventos em 26 esportes\n27 de julho- 12 de agosto 2012", "204 Países 10.568 Atletas 961 Medalhas", "#1a2233"),
    ("Rio de Janeiro 2016", "306 eventos em 28 esportes\n05 de agosto- 21 de agosto 2016", "207 Países 11.238 Atletas 4.924 Medalhas", "#232737")
]
for i, (titulo, subtitulo, detalhes, cor) in enumerate(eventos):
    card = ctk.CTkFrame(frame_eventos, fg_color=cor, width=437, height=200, corner_radius=10)
    card.grid(row=1, column=i, padx=(0,25), pady=(20,35))
    ctk.CTkLabel(card, text=titulo, font=("Arial", 16, "bold"), text_color="#D2FF28").place(x=12, y=20)
    ctk.CTkLabel(card, text=subtitulo, font=("Arial", 13), text_color="gray").place(x=15, y=60)

    # Separação dos dados numéricos e os nomes
    if i == 0:
        # Exemplo para Tóquio 2020: "206 Países  11.656 Atletas  1.080 Medalhas"
        numeros = ["204", "10.942", "958"]
        nomes = ["Países", "Atletas", "Medalhas"]
    elif i == 1:
        # Pequim 2022: "91 Países2.871 Atletas327 Medalhas" (corrigindo espaços)
        numeros = ["204", "10.568", "961"]
        nomes = ["Países", "Atletas", "Medalhas"]
    else:
        # Paris 2024: "? Países10.500 Atletas? Medalhas" (exemplo com interrogações)
        numeros = ["207", "11.238", "4.924"]
        nomes = ["Países", "Atletas", "Medalhas"]

    #posições horizontais para cada grupo
    x_positions = [15, 150, 300]
    y_num = 120
    y_nome = 150

    for x, num, nome in zip(x_positions, numeros, nomes):
        ctk.CTkLabel(card, text=num, font=("Arial", 20, "bold"), text_color="#A7FF4E", fg_color="transparent").place(x=x, y=y_num)
        ctk.CTkLabel(card, text=nome, font=("Arial", 11), text_color="gray", fg_color="transparent").place(x=x, y=y_nome)


# Iniciar loop da aplicação
app.mainloop()
