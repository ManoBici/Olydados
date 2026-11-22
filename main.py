import customtkinter as ctk
import tkinter as tk
from data_explorer import DataExplorerView
from dashboard import DashboardView


# Cores do layout
COR_AZUL_ESCURO = "#0E131F"
COR_VERDE_LIMAO = "#D2FF28"
COR_BOTAO = "#D2FF28"
ICON_COLOR = "#D6FF1C"  # Neon amarelo



blocks = [
    ("🔽", "Filtre por atletas,\npaíses, modalidades\ne medalhas"),
    ("📈", "Visualize dados históricos\natravés de gráficos"),
    ("🏅", "Descubra recordes e\ncuriosidades históricas"),
    ("📊", "Compare\ndesempenhos entre\nedições e nações"),
]


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("OlyDados")
root.geometry("800x700")
root.resizable(True, True)
root.configure(fg_color=COR_AZUL_ESCURO)

# Variáveis para armazenar as instâncias das janelas
tela_exploracao_instance = None
tela_dashboard_instance = None

# --- Funções para abrir as janelas ---
def abrir_tela_explorar_dados():
    global tela_exploracao_instance
    if tela_exploracao_instance is None or not tela_exploracao_instance.winfo_exists():
        tela_exploracao_instance = DataExplorerView(root)
        tela_exploracao_instance.focus()
    else:
        tela_exploracao_instance.lift()
        tela_exploracao_instance.focus()

def abrir_tela_dashboard():
    global tela_dashboard_instance
    if tela_dashboard_instance is None or not tela_dashboard_instance.winfo_exists():
        tela_dashboard_instance = DashboardView(root)
        tela_dashboard_instance.focus()
    else:
        tela_dashboard_instance.lift()
        tela_dashboard_instance.focus()

# Barra de Navegação Superior
nav_frame = ctk.CTkFrame(root, fg_color="#D2FF28", height=80, corner_radius=0)
nav_frame.pack(fill="x", side="top")
nav_frame.grid_rowconfigure(0, weight=1)
nav_frame.grid_columnconfigure(1, weight=1) # Espaço para centralizar

btn_home = ctk.CTkButton(nav_frame, text="Home", fg_color="#2A2D34", hover_color="#003459",
                         text_color="white", width=80, height=40, corner_radius=3)
btn_home.grid(row=0, column=0, padx=(20, 5), pady=20, sticky="w")

btn_filtragem = ctk.CTkButton(nav_frame, text="Filtragem", fg_color="transparent", hover_color="#C0E020",
                              text_color="black", width=100, height=40, corner_radius=3,
                              command=abrir_tela_explorar_dados) # Comando para a tela de filtragem
btn_filtragem.grid(row=0, column=2, padx=5, pady=20)

# ALTERADO: O comando do botão "Dashboard" (antes "Curiosidades") agora abre a tela de gráficos.
btn_dashboard = ctk.CTkButton(nav_frame, text="Dashboard", fg_color="transparent", hover_color="#C0E020",
                               text_color="black", width=120, height=40, corner_radius=3,
                               command=abrir_tela_dashboard) # Comando para a tela do dashboard
btn_dashboard.grid(row=0, column=3, padx=(5, 20), pady=20, sticky="e")

#Área Central
main_frame = ctk.CTkFrame(root, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

#Logo dos Anéis Olímpicos
canvas_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
canvas_frame.place(relx=0.5, rely=0.15, anchor="n")
canvas = tk.Canvas(canvas_frame, width=320, height=140, bg=COR_AZUL_ESCURO, bd=0, highlightthickness=0, relief='ridge')
canvas.pack()
cores_aneis = ["#0081C8", "#000000", "#EE334E", "#FECB00", "#009F3D"]
posicoes = [(20, 30), (100, 30), (180, 30), (60, 57), (140, 57)]
for i in range(5):
    x, y = posicoes[i]
    canvas.create_oval(x, y, x+80, y+80, width=7, outline=cores_aneis[i])

# Título, Subtítulo e Botão
label_titulo = ctk.CTkLabel(main_frame, text="OlyDados", font=("Arial", 38, "bold"), text_color="white", fg_color="transparent")
label_titulo.place(relx=0.5, rely=0.35, anchor="center")

label_subtitulo = ctk.CTkLabel(
    main_frame, text="Explore dados históricos, estatísticas e curiosidades sobre os\njogos olímpicos",
    font=("Arial", 16), text_color="white", fg_color="transparent", justify="center")
label_subtitulo.place(relx=0.5, rely=0.45, anchor="center")

botao_explorar = ctk.CTkButton(
    main_frame, text="Explorar Dados", font=("Arial", 16, "bold"), fg_color=COR_BOTAO,
    hover_color="#B0D924", text_color="black", width=180, height=45, corner_radius=8,
    command=abrir_tela_explorar_dados)
botao_explorar.place(relx=0.5, rely=0.57, anchor="center")

#frames quadrados para os blocos de informação
blocos_container_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
blocos_container_frame.place(relx=0.5, rely=0.83, anchor="center")

# Criação dos blocos (agora são apenas visuais, sem comandos)
for i, (emoji, text) in enumerate(blocks):
    bloco = ctk.CTkFrame(
        blocos_container_frame, width=180, height=160,
        fg_color="#141924", corner_radius=15, border_width=0)
    bloco.grid(row=0, column=i, padx=10, pady=10)

    icon_label = ctk.CTkLabel(
        bloco, text=emoji, font=("Segoe UI Emoji", 36, "bold"),
        text_color=ICON_COLOR, anchor="center")
    icon_label.pack(pady=(18, 10))

    text_label = ctk.CTkLabel(
        bloco, text=text, font=("Segoe UI", 14), text_color="white",
        anchor="center", justify="center", wraplength=160)
    text_label.pack(padx=10, pady=(0, 15), fill="x", expand=True)

root.mainloop()
