import customtkinter as ctk
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import sqlite3

# Tenta importar o cartopy, se não conseguir, desativa o mapa
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from shapely.geometry import Point # Importação necessária para o hover
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False
    print("AVISO: Biblioteca Cartopy não encontrada. O mapa não será exibido.")
    print("Para instalar, tente: pip install cartopy shapely")


DB_PATH = 'banco.db'

class TelaDashboard(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Painel de Dados Olímpicos")
        self.geometry("1200x900")
        self.state("zoomed")
        self.grab_set()

        # Cores da interface
        self.bg_color = "#181C27"
        self.card_color = "#232737"
        self.text_color = "#FFFFFF"
        self.highlight_color = "#D2FF28"

        self.configure(fg_color=self.bg_color)

        # Atributos para interatividade do mapa
        self.city_annotations = []
        self.city_artists = []

        # Frame rolável para todo o conteúdo
        self.scrollable_frame = ctk.CTkScrollableFrame(master=self, fg_color=self.bg_color)
        self.scrollable_frame.pack(fill="both", expand=True)
        # Configura o grid para 4 colunas
        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Título
        label_titulo = ctk.CTkLabel(self.scrollable_frame, text="Painel de Dados Olímpicos",
                                    font=("Arial", 22, "bold"), text_color=self.highlight_color)
        label_titulo.grid(row=0, column=0, columnspan=4, pady=(20, 10), padx=20, sticky="w")
        
        # Carrega os dados do banco e exibe os elementos
        self.carregar_e_exibir_cards()
        self.criar_grafico_evolucao()
        self.criar_grafico_genero() # Gráfico de Gênero agora na linha de cima
        self.criar_mapa_cidades_sede()
        self.criar_grafico_medalhas() # Gráfico de Medalhas agora na linha de baixo
        self.criar_secao_destaques_e_esportes()
        self.criar_secao_eventos_recentes()
        self.criar_rodape()

    def carregar_e_exibir_cards(self):
        """Carrega dados agregados do DB e exibe nos cards."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM banco WHERE medalha IN ('Gold', 'Silver', 'Bronze')")
            total_medalhas = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT pais) FROM banco")
            total_paises = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT esporte) FROM banco")
            total_esportes = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT nome_atleta) FROM banco WHERE ano = (SELECT MAX(ano) FROM banco)")
            total_atletas_recente = cursor.fetchone()[0]
            
            conn.close()
            
            card_data = [
                ("Medalhas Distribuídas", f"{total_medalhas:,}", "Desde 1896"),
                ("Nações Participantes", f"{total_paises}", "Em todas as edições"),
                ("Esportes Disputados", f"{total_esportes}", "Em todas as edições"),
                ("Atletas (Edição Mais Recente)", f"{total_atletas_recente:,}", "")
            ]
        except sqlite3.Error as e:
            print(f"Erro ao carregar dados para os cards: {e}")
            card_data = [("Medalhas", "Erro", ""), ("Países", "Erro", ""), ("Esportes", "Erro", ""), ("Atletas", "Erro", "")]
        
        for i, (title, value, desc) in enumerate(card_data):
            frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self.card_color, corner_radius=10)
            frame.grid(row=1, column=i, padx=10, pady=10, sticky="nsew") 
            ctk.CTkLabel(frame, text=title, font=("Arial", 14, "bold"), text_color=self.text_color).pack(pady=(10, 0), padx=15, anchor="w")
            ctk.CTkLabel(frame, text=value, font=("Arial", 28, "bold"), text_color=self.highlight_color).pack(pady=(0, 0), padx=15, anchor="w")
            ctk.CTkLabel(frame, text=desc, font=("Arial", 11), text_color="gray").pack(pady=(0, 10), padx=15, anchor="w")


    def criar_grafico_evolucao(self):
        """Cria o gráfico de linha da evolução dos jogos com dados do DB."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT CAST(ano AS INTEGER), COUNT(DISTINCT nome_atleta), COUNT(DISTINCT pais) FROM banco GROUP BY ano ORDER BY ano")
            dados = cursor.fetchall()
            conn.close()
            
            anos = [d[0] for d in dados]
            atletas = [d[1] for d in dados]
            paises = [d[2] for d in dados]

        except sqlite3.Error as e:
            print(f"Erro ao carregar dados para o gráfico de evolução: {e}")
            anos, atletas, paises = [], [], []

        fig = Figure(figsize=(6, 4.5), dpi=100)
        ax1 = fig.add_subplot(111)

        l1, = ax1.plot(anos, atletas, marker='o', label="Atletas", color=self.highlight_color)
        ax1.set_ylabel("Número de Atletas", color=self.highlight_color)
        ax1.tick_params(axis='y', labelcolor=self.highlight_color)
        
        ax2 = ax1.twinx()
        l2, = ax2.plot(anos, paises, marker='s', label="Países", color='orange')
        ax2.set_ylabel("Número de Países", color='orange')
        ax2.tick_params(axis='y', labelcolor='orange')

        ax1.set_title("Evolução dos Jogos Olímpicos", color=self.text_color)
        ax1.set_xlabel("Ano", color=self.text_color)
        ax1.tick_params(axis='x', labelcolor=self.text_color)
        fig.patch.set_facecolor(self.bg_color)
        ax1.set_facecolor(self.card_color)
        ax1.legend([l1, l2], ["Atletas", "Países"], loc='upper left', facecolor=self.card_color, edgecolor='white', labelcolor='white')
        ax1.grid(True, color='gray', linestyle='--', alpha=0.3)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")

    def criar_grafico_medalhas(self):
        """Cria o gráfico de barras das medalhas por país com dados do DB."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pais,
                       SUM(CASE WHEN medalha = 'Gold' THEN 1 ELSE 0 END) as Ouro,
                       SUM(CASE WHEN medalha = 'Silver' THEN 1 ELSE 0 END) as Prata,
                       SUM(CASE WHEN medalha = 'Bronze' THEN 1 ELSE 0 END) as Bronze
                FROM banco
                WHERE medalha IN ('Gold', 'Silver', 'Bronze')
                GROUP BY pais
                ORDER BY Ouro DESC, Prata DESC, Bronze DESC
                LIMIT 10
            """)
            dados = cursor.fetchall()
            conn.close()

            paises = [d[0] for d in dados]
            ouro = [d[1] for d in dados]
            prata = [d[2] for d in dados]
            bronze = [d[3] for d in dados]

        except sqlite3.Error as e:
            print(f"Erro ao carregar dados para o gráfico de medalhas: {e}")
            paises, ouro, prata, bronze = [], [], []

        fig = Figure(figsize=(6, 4.5), dpi=100)
        ax = fig.add_subplot(111)

        x = np.arange(len(paises))
        width = 0.25
        ax.bar(x - width, ouro, width, label='Ouro', color='gold')
        ax.bar(x, prata, width, label='Prata', color='silver')
        ax.bar(x + width, bronze, width, label='Bronze', color='#CD7F32')

        fig.patch.set_facecolor(self.bg_color)
        ax.set_facecolor(self.card_color)
        ax.set_title("Top 10 Países por Medalhas de Ouro", color=self.text_color)
        ax.set_ylabel('Número de Medalhas', color=self.text_color)
        ax.set_xticks(x)
        ax.set_xticklabels(paises, rotation=45, ha='right', color=self.text_color)
        ax.tick_params(axis='y', labelcolor=self.text_color)
        ax.legend(facecolor=self.card_color, edgecolor='white', labelcolor='white')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas.draw()
        # ALTERADO: Posição do gráfico de medalhas
        canvas.get_tk_widget().grid(row=3, column=2, columnspan=2, pady=20, padx=20, sticky="nsew")
        
    def criar_mapa_cidades_sede(self):
        """Cria um mapa de globo com as cidades-sede marcadas e com hover."""
        if not CARTOPY_AVAILABLE:
            frame_mapa_aviso = ctk.CTkFrame(self.scrollable_frame, fg_color=self.card_color)
            frame_mapa_aviso.grid(row=3, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")
            ctk.CTkLabel(frame_mapa_aviso, text="Mapa Indisponível", font=("Arial", 16, "bold")).pack(pady=10)
            ctk.CTkLabel(frame_mapa_aviso, text="A biblioteca 'cartopy' não foi encontrada.").pack(pady=10, padx=10)
            return

        cidades = {
            "Atenas": (37.98, 23.72), "Paris": (48.85, 2.35), "St. Louis": (38.62, -90.19),
            "Londres": (51.50, -0.12), "Estocolmo": (59.32, 18.06), "Antuérpia": (51.21, 4.40),
            "Amsterdã": (52.36, 4.90), "Los Angeles": (34.05, -118.24), "Berlim": (52.52, 13.40),
            "Helsinque": (60.16, 24.93), "Melbourne": (-37.81, 144.96), "Roma": (41.90, 12.49),
            "Tóquio": (35.68, 139.69), "Cidade do México": (19.43, -99.13), "Munique": (48.13, 11.58),
            "Montreal": (45.50, -73.56), "Moscou": (55.75, 37.61), "Seul": (37.56, 126.97),
            "Barcelona": (41.38, 2.17), "Atlanta": (33.74, -84.38), "Sydney": (-33.86, 151.20),
            "Pequim": (39.90, 116.40), "Rio de Janeiro": (-22.90, -43.20)
        }

        self.fig_map = Figure(figsize=(7, 6), dpi=100)
        self.fig_map.patch.set_facecolor(self.bg_color)
        self.ax_map = self.fig_map.add_subplot(1, 1, 1, projection=ccrs.Orthographic(central_longitude=0, central_latitude=25))
        self.ax_map.set_facecolor(self.card_color)

        self.ax_map.set_global()
        self.ax_map.add_feature(cfeature.LAND, facecolor='#666666', zorder=0)
        self.ax_map.add_feature(cfeature.OCEAN, facecolor='#444455', zorder=0)
        self.ax_map.add_feature(cfeature.COASTLINE, edgecolor='white', linewidth=0.5, zorder=1)
        self.ax_map.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='white', linewidth=0.5, zorder=1)
        
        self.city_artists.clear()
        self.city_annotations.clear()

        for cidade, (lat, lon) in cidades.items():
            point, = self.ax_map.plot(lon, lat, marker='o', color=self.highlight_color, 
                                      markersize=8, transform=ccrs.Geodetic(), zorder=2, picker=5)
            self.city_artists.append(point)

            annotation = self.ax_map.text(lon, lat, f"  {cidade}", 
                                          fontsize=9, fontweight='bold', color='white', 
                                          transform=ccrs.Geodetic(), zorder=3, visible=False,
                                          bbox=dict(boxstyle="round,pad=0.3", fc="black", ec="none", alpha=0.7))
            self.city_annotations.append(annotation)

        self.ax_map.set_title('Cidades-Sede dos Jogos de Verão', color=self.text_color, pad=20)
        self.fig_map.tight_layout()

        self.canvas_map = FigureCanvasTkAgg(self.fig_map, master=self.scrollable_frame)
        self.canvas_map.draw()
        self.canvas_map.get_tk_widget().grid(row=3, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")
        self.fig_map.canvas.mpl_connect("motion_notify_event", self.on_city_hover)

    def on_city_hover(self, event):
        if not self.city_annotations: return

        visible_found_this_time = False
        for i, artist in enumerate(self.city_artists):
            is_over, _ = artist.contains(event)
            annotation = self.city_annotations[i]
            
            if is_over and not annotation.get_visible():
                annotation.set_visible(True)
                visible_found_this_time = True
            elif not is_over and annotation.get_visible():
                annotation.set_visible(False)
                visible_found_this_time = True
        
        if visible_found_this_time:
            self.canvas_map.draw_idle()

    def criar_grafico_genero(self):
        """Cria um gráfico de pizza da distribuição de gênero dos atletas com dados do DB."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT sexo, COUNT(DISTINCT nome_atleta) FROM banco WHERE sexo IN ('M', 'F') GROUP BY sexo")
            dados = cursor.fetchall()
            conn.close()

            labels = []
            sizes = []
            gender_data = dict(dados)
            if 'M' in gender_data:
                labels.append('Homens')
                sizes.append(gender_data['M'])
            if 'F' in gender_data:
                labels.append('Mulheres')
                sizes.append(gender_data['F'])

        except sqlite3.Error as e:
            print(f"Erro ao carregar dados para o gráfico de gênero: {e}")
            labels, sizes = [], []

        fig = Figure(figsize=(5, 4.5), dpi=100)
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor(self.bg_color)

        colors = ['cyan', self.highlight_color]
        explode = (0, 0.05) if len(sizes) > 1 else (0,)

        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                          autopct='%1.1f%%', shadow=True, startangle=90,
                                          textprops=dict(color=self.text_color))

        ax.axis('equal')
        ax.set_title("Distribuição de Gênero (Atletas Únicos)", color=self.text_color)
        plt.setp(autotexts, size=10, weight="bold", color="black")

        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=2, columnspan=2, pady=20, padx=20, sticky="nsew")
        
    def criar_secao_destaques_e_esportes(self):
        """Cria os cards de destaques e esportes com mais medalhas."""
        frame_cards_destaques = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        frame_cards_destaques.grid(row=4, column=0, columnspan=4, pady=(10, 0), padx=20, sticky="nsew")
        frame_cards_destaques.grid_columnconfigure((0,1), weight=1)

        # --- Esportes com mais medalhas (dinâmico) ---
        frame_esportes = ctk.CTkFrame(frame_cards_destaques, fg_color=self.card_color, corner_radius=10)
        frame_esportes.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        ctk.CTkLabel(frame_esportes, text="Esportes com mais medalhas", font=("Arial", 15, "bold"),
                     text_color=self.highlight_color).pack(anchor="w", padx=15, pady=(10,5))
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT esporte, COUNT(DISTINCT evento), COUNT(*) as total_medalhas
                FROM banco WHERE medalha IN ('Gold', 'Silver', 'Bronze')
                GROUP BY esporte
                ORDER BY total_medalhas DESC LIMIT 5
            """)
            esportes_data = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao carregar dados dos esportes: {e}")
            esportes_data = []

        # Cabeçalho da tabela de esportes
        header_frame = ctk.CTkFrame(frame_esportes, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(header_frame, text="ESPORTE", font=("Arial", 12, "bold"), text_color="white", anchor="w").pack(side="left", expand=True)
        ctk.CTkLabel(header_frame, text="EVENTOS", font=("Arial", 12, "bold"), text_color="white", width=70, anchor="e").pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text="MEDALHAS", font=("Arial", 12, "bold"), text_color="white", width=90, anchor="e").pack(side="left")

        for i, (esporte, eventos, medalhas) in enumerate(esportes_data):
            linha_frame = ctk.CTkFrame(frame_esportes, fg_color="transparent")
            linha_frame.pack(fill="x", padx=15, pady=2)
            ctk.CTkLabel(linha_frame, text=esporte, font=("Arial", 12), text_color=self.text_color, anchor="w").pack(side="left", expand=True)
            ctk.CTkLabel(linha_frame, text=f"{eventos}", font=("Arial", 12), text_color=self.text_color, width=70, anchor="e").pack(side="left", padx=10)
            ctk.CTkLabel(linha_frame, text=f"{medalhas:,}", font=("Arial", 12, "bold"), text_color=self.text_color, width=90, anchor="e").pack(side="left")
            if i < len(esportes_data) - 1:
                ctk.CTkFrame(frame_esportes, height=1, fg_color="#31374a").pack(fill="x", padx=15, pady=2)
        
        # --- Destaques Olímpicos (estático) ---
        frame_destaques = ctk.CTkFrame(frame_cards_destaques, fg_color=self.card_color, corner_radius=10)
        frame_destaques.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        ctk.CTkLabel(frame_destaques, text="Destaques Olímpicos", font=("Arial", 15, "bold"),
                     text_color=self.highlight_color).pack(anchor="w", padx=15, pady=(10,5))

        destaques = [
            ("Michael Phelps", "28 medalhas (23 de ouro) em Natação"),
            ("Usain Bolt", "8 medalhas de ouro no Atletismo"),
            ("Nadia Comăneci", "Primeiro 10 perfeito em Ginástica (1976)")
        ]
        for i, (nome, desc) in enumerate(destaques):
            destaque_frame = ctk.CTkFrame(frame_destaques, fg_color="transparent")
            destaque_frame.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(destaque_frame, text=nome, font=("Arial", 13, "bold"), text_color=self.highlight_color, anchor="w").pack(fill="x")
            ctk.CTkLabel(destaque_frame, text=desc, font=("Arial", 11), text_color=self.text_color, anchor="w", wraplength=400, justify="left").pack(fill="x")
            if i < len(destaques) - 1:
                ctk.CTkFrame(frame_destaques, height=1, fg_color="#31374a").pack(fill="x", padx=15, pady=5)

    def criar_secao_eventos_recentes(self):
        """Cria os cards dos eventos olímpicos recentes."""
        frame_eventos_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        frame_eventos_container.grid(row=5, column=0, columnspan=4, pady=20, padx=20, sticky="nsew")
        ctk.CTkLabel(frame_eventos_container, text="Resumo das Últimas Edições", font=("Arial", 15, "bold"),
                     text_color=self.highlight_color).pack(anchor="w", pady=(10, 5))
        
        frame_eventos = ctk.CTkFrame(frame_eventos_container, fg_color="transparent")
        frame_eventos.pack(fill="x")

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT ano FROM banco ORDER BY ano DESC LIMIT 3")
            anos_recentes = [row[0] for row in cursor.fetchall()]

            for i, ano in enumerate(anos_recentes):
                frame_eventos.grid_columnconfigure(i, weight=1)
                
                cursor.execute("SELECT cidade_sede, COUNT(DISTINCT pais), COUNT(DISTINCT nome_atleta), COUNT(*) FROM banco WHERE ano = ? AND medalha IN ('Gold','Silver','Bronze') GROUP BY cidade_sede", (ano,))
                dados_edicao = cursor.fetchone()
                
                if dados_edicao:
                    cidade, paises, atletas, medalhas = dados_edicao
                    card = ctk.CTkFrame(frame_eventos, fg_color=self.card_color, corner_radius=10)
                    card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
                    
                    ctk.CTkLabel(card, text=f"{cidade} {ano}", font=("Arial", 16, "bold"), text_color=self.highlight_color).pack(pady=(15,5))
                    
                    details_frame = ctk.CTkFrame(card, fg_color="transparent")
                    details_frame.pack(fill="x", expand=True, padx=20, pady=10)
                    details_frame.grid_columnconfigure((0,1,2), weight=1)
                    
                    details_data = [
                        (f"{paises}", "Países"),
                        (f"{atletas:,}", "Atletas"),
                        (f"{medalhas:,}", "Medalhas")
                    ]

                    for j, (num, nome) in enumerate(details_data):
                        num_label = ctk.CTkLabel(details_frame, text=num, font=("Arial", 20, "bold"), text_color="#A7FF4E")
                        num_label.grid(row=0, column=j)
                        nome_label = ctk.CTkLabel(details_frame, text=nome, font=("Arial", 11), text_color="gray")
                        nome_label.grid(row=1, column=j)
            
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao carregar dados dos eventos recentes: {e}")

    def criar_rodape(self):
        """Cria o rodapé da aplicação."""
        footer_frame = ctk.CTkFrame(self.scrollable_frame, height=80, fg_color=self.card_color, corner_radius=0)
        footer_frame.grid(row=6, column=0, columnspan=4, sticky="ew", pady=(40, 0))

        canvas_aneis = tk.Canvas(footer_frame, width=150, height=60, bg=self.card_color, highlightthickness=0)
        canvas_aneis.pack(side="left", padx=20, pady=10)

        raio = 15; espaco = 5; y = 25; espessura = 3
        cores = ["#0085C7", "#000000", "#DF0024", "#F4C300", "#009F3D"]
        posicoes_x = [raio, raio*2 + espaco, raio*4 + espaco*2, raio*3 + espaco, raio*5 + espaco*2]
        
        for i in range(3): canvas_aneis.create_oval(posicoes_x[i]-raio, y-raio, posicoes_x[i]+raio, y+raio, outline=cores[i], width=espessura)
        for i in range(3, 5): canvas_aneis.create_oval(posicoes_x[i]-raio, y+raio-espaco, posicoes_x[i]+raio, y+raio*2-espaco, outline=cores[i], width=espessura)

        footer_text = "© 2025 Painel Olímpico\nDados públicos do Kaggle (1896-2016)"
        ctk.CTkLabel(footer_frame, text=footer_text, font=("Arial", 11), text_color="gray", justify="left").pack(side="left", padx=15)


if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    dashboard = TelaDashboard(app)
    dashboard.mainloop()

