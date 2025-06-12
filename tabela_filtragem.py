import customtkinter as ctk

# Lista completa de esportes olímpicos
modalidades_olimpicas = ["Atletismo", "Badmiton", "Basquete", "Boxe", "Boxe","Breaking", "Canoagem de velocidade", "Canoagem Slalom",
                         "Canoagem de velocidade", "Ciclismo", "Escalada", "Esgrima", "Futebol",
                         "Ginastica Artistica", "Gisnastica de Trampolim", "Ginástica Ritímica", "Golfe", "Handeb", "Hipismo",
                         "Hoquei sobre grama", "Judô", "Levantamento de Peso", "Luta", "Maratona Aquática", "Nado Artístico", "Natação",
                         "Pentatlo moderno", "Polo aquático", "Remo", "Rugby sevens","Saltos ornamentais", "Skate", "Surfe", "Taekwondo",
                         "Tênis", "Tênis de mesa", "Tiro com arco", "Tiro Esportivo", "Triatlo", "Vela", "Vôlei", "Vôlei de praia"]

# Lista simplificada de países olímpicos
paises_olimpicos = [
    "Afeganistão", "África do Sul", "Albânia", "Alemanha", "Andorra", "Angola", "Arábia Saudita", "Argélia", "Argentina",
    "Armênia", "Austrália", "Áustria", "Azerbaijão", "Bahamas", "Bangladesh", "Barbados", "Bahrein", "Bélgica",
    "Belize", "Benin", "Bermudas", "Bielorrússia", "Bolívia", "Bósnia e Herzegovina", "Botsuana", "Brasil", "Brunei",
    "Bulgária", "Burkina Faso", "Burundi", "Butão", "Cabo Verde", "Camarões", "Camboja", "Canadá", "Catar", "Cazaquistão",
    "Chile", "China", "Chipre", "Colômbia", "Comores", "Congo", "Coreia do Norte", "Coreia do Sul", "Costa do Marfim",
    "Costa Rica", "Croácia", "Cuba", "Dinamarca", "Djibuti", "Dominica", "Egito", "El Salvador", "Emirados Árabes Unidos",
    "Equador", "Eritreia", "Eslováquia", "Eslovênia", "Espanha", "Estados Unidos", "Estônia", "Etiópia", "Fiji", "Filipinas",
    "Finlândia", "França", "Gabão", "Gâmbia", "Gana", "Geórgia", "Granada", "Grécia", "Guatemala", "Guiana", "Guiné",
    "Guiné-Bissau", "Guiné Equatorial", "Haiti", "Holanda", "Honduras", "Hungria", "Iémen", "Ilhas Cook", "Ilhas Fiji",
    "Ilhas Maldivas", "Ilhas Marshall", "Ilhas Maurício", "Ilhas Salomão", "Ilhas Seychelles", "Índia", "Indonésia",
    "Irã", "Iraque", "Irlanda", "Islândia", "Israel", "Itália", "Jamaica", "Japão", "Jordânia", "Kiribati", "Kosovo",
    "Kuwait", "Laos", "Lesoto", "Letônia", "Líbano", "Libéria", "Líbia", "Liechtenstein", "Lituânia", "Luxemburgo",
    "Macedônia do Norte", "Madagáscar", "Malásia", "Malawi", "Mali", "Malta", "Marrocos", "Mauritânia", "México",
    "Micronésia", "Moldávia", "Mônaco", "Mongólia", "Montenegro", "Moçambique", "Myanmar", "Namíbia", "Nauru", "Nepal",
    "Nicarágua", "Níger", "Nigéria", "Noruega", "Nova Zelândia", "Omã", "Países Baixos", "Palau", "Palestina", "Panamá",
    "Papua-Nova Guiné", "Paquistão", "Paraguai", "Peru", "Polônia", "Portugal", "Porto Rico", "Qatar", "Quênia",
    "Quirguistão", "Reino Unido", "República Centro-Africana", "República Checa", "República Democrática do Congo",
    "República Dominicana", "Romênia", "Ruanda", "Rússia", "Samoa", "San Marino", "Santa Lúcia", "São Cristóvão e Nevis",
    "São Tomé e Príncipe", "São Vicente e Granadinas", "Senegal", "Serra Leoa", "Sérvia", "Singapura", "Síria", "Somália",
    "Sri Lanka", "Suazilândia", "Sudão", "Sudão do Sul", "Suécia", "Suíça", "Suriname", "Tailândia", "Taiwan", "Tajiquistão",
    "Tanzânia", "Timor-Leste", "Togo", "Tonga", "Trinidad e Tobago", "Tunísia", "Turcomenistão", "Turquia", "Tuvalu",
    "Ucrânia", "Uganda", "Uruguai", "Uzbequistão", "Vanuatu", "Vaticano", "Venezuela", "Vietnã", "Zâmbia", "Zimbábue"
]

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Resultados Olímpicos")
root.geometry("900x700")
root.resizable(True, True)
root.configure(fg_color="#0E131F")

#PAINEL DE FILTROS
filtros_frame = ctk.CTkFrame(root, fg_color="#D2FF28", corner_radius=15, height=120)
filtros_frame.pack(fill="x", padx=18, pady=(18, 10))

label_filtros = ctk.CTkLabel(filtros_frame, text="Filtragem de dados olímpicos", font=("Arial", 18, "bold"), text_color="black")
label_filtros.grid(row=0, column=0, columnspan=5, sticky="w", padx=(20,0), pady=(12, 10))

ctk.CTkLabel(filtros_frame, text="País", font=("Arial", 12), text_color="black", fg_color="transparent").grid(row=1, column=0, sticky="w", padx=(20,2), pady=(8,0))
ctk.CTkLabel(filtros_frame, text="Esporte", font=("Arial", 12), text_color="black", fg_color="transparent").grid(row=1, column=1, sticky="w", padx=(12,2), pady=(8,0))
ctk.CTkLabel(filtros_frame, text="Tipo de Medalha", font=("Arial", 12), text_color="black", fg_color="transparent").grid(row=1, column=2, sticky="w", padx=(12,2), pady=(8,0))
ctk.CTkLabel(filtros_frame, text="Ano", font=("Arial", 12), text_color="black", fg_color="transparent").grid(row=1, column=3, sticky="w", padx=(12,2), pady=(8,0))

combo_pais = ctk.CTkComboBox(filtros_frame, width=180, values=["Todos os Países"] + paises_olimpicos)
combo_pais.set("Todos os Países")
combo_pais.grid(row=2, column=0, padx=(20,8), pady=(2,8))

combo_esporte = ctk.CTkComboBox(filtros_frame, width=180, values=["Todos os Esportes"] + modalidades_olimpicas)
combo_esporte.set("Todos os Esportes")
combo_esporte.grid(row=2, column=1, padx=8, pady=(2,8))

combo_medalha = ctk.CTkComboBox(filtros_frame, width=150, values=["Todas as Medalhas", "Ouro", "Prata", "Bronze"])
combo_medalha.set("Todas as Medalhas")
combo_medalha.grid(row=2, column=2, padx=8, pady=(2,8))

combo_ano = ctk.CTkComboBox(filtros_frame, width=150, values=["Todos os Anos", "1896", "1900", "1904", "1908", "1912", "1920", "1924", "1928", "1932", "1936", "1948", "1952", "1956", "1960", "1964", "1968",
    "1972", "1976", "1980", "1984", "1988", "1992", "1996", "2000", "2004", "2008", "2012", "2016", "2020"])
combo_ano.set("Todos os Anos")
combo_ano.grid(row=2, column=3, padx=8, pady=(2,8))

botao_aplicar = ctk.CTkButton(filtros_frame, text="Aplicar Filtros", width=130, fg_color="#0E131F", hover_color="darkblue", text_color="white")
botao_aplicar.grid(row=2, column=4, padx=(18,0), pady=(2,8))

botao_reset = ctk.CTkButton(filtros_frame, text="Redefinir Filtros", width=120, fg_color="#0E131F", hover_color="darkblue", text_color="white", border_width=1, border_color="#124117")
botao_reset.grid(row=3, column=0, padx=(20,0), pady=(0,30), sticky="w")

#TABELA CENTRALIZADA
tabela_bg_frame = ctk.CTkFrame(root, fg_color="#0E131F", corner_radius=15)
tabela_bg_frame.pack(pady=(0,0), fill="both", expand=True, padx=18)

tabela_frame = ctk.CTkFrame(tabela_bg_frame, fg_color="#FFFFFF", corner_radius=10, width=850)
tabela_frame.place(relx=0.5, rely=0.18, anchor="n")

label_titulo = ctk.CTkLabel(tabela_bg_frame, text="Resultados Olímpicos", font=("Arial", 14, "bold"), text_color="white", fg_color="transparent")
label_titulo.place(x=10, y=12)

label_resultados = ctk.CTkLabel(tabela_bg_frame, text="Resultados: 40", font=("Arial", 12), text_color="white", fg_color="transparent")
label_resultados.place(relx=0.97, y=12, anchor="ne")


headers = ["ANO", "PAÍS", "ESPORTE", "EVENTO", "MEDALHA", "ATLETA"]
col_widths = [60, 170, 180, 220, 120, 150]

for i, header in enumerate(headers):
    label = ctk.CTkLabel(tabela_frame, text=header, font=("Arial", 11, "bold"), text_color="#787878", width=col_widths[i], anchor="w")
    label.grid(row=0, column=i, padx=(8 if i==0 else 2, 2), pady=(12,4), sticky="w")

# Exemplo de dados (nome do atleta)
dados = [
    ["2008", "Estados Unidos", "Natação", "8 Medalhas de Ouro", "🥇 Ouro", "Michael Phelps"],
    ["2008", "Jamaica", "Atletismo", "100m Recorde Mundial", "🥇 Ouro", "Usain Bolt"],
    ["2008", "China", "Atletismo", "110m com barreiras", "🥉 Bronze", "Liu Xiang"],
    ["2008", "Rússia", "Atletismo", "Salto com vara", "🥇 Ouro", "Yelena Isinbayeva"],
    ["2008", "Estados Unidos", "Ginástica Artística", "Individual geral", "🥈 Prata", "Shawn Johnson"],
    ["2008", "Estados Unidos", "Ginástica Artística", "Trave", "🥇 Ouro", "Nastia Liukin"],
    ["2008", "Estados Unidos", "Natação", "200m Peito", "🥇 Ouro", "Rebecca Soni"],
    ["2008", "Estados Unidos", "Basquete", "Torneio masculino", "🥇 Ouro", "Kobe Bryant"],
    ["2008", "Espanha", "Basquete", "Torneio masculino", "🥈 Prata", "Pau Gasol"],
    ["2008", "Argentina", "Basquete", "Torneio masculino", "🥉 Bronze", "Manu Ginóbili"],
]

linha_cores = ["#FFFFFF", "#F6F7F9"]
medalha_cores = {"Ouro": "#FEFCAD", "Prata": "#DFDFE2", "Bronze": "#FFDEAD"}

for row_idx, row in enumerate(dados, start=1):
    bg = linha_cores[row_idx % 2]
    for col_idx, value in enumerate(row):
        if col_idx == 4:
            medalha = value.split()[-1]
            cor = medalha_cores.get(medalha, bg)
            label = ctk.CTkLabel(tabela_frame, text=value, font=("Arial", 11), text_color="#8C6B00" if medalha=="Ouro" else "#787878", fg_color=cor, width=col_widths[col_idx], anchor="w")
        else:
            label = ctk.CTkLabel(tabela_frame, text=value, font=("Arial", 11, "bold" if col_idx==0 else "normal"), text_color="#2E2E2E", fg_color=bg, width=col_widths[col_idx], anchor="w")
        label.grid(row=row_idx, column=col_idx, padx=(8 if col_idx==0 else 2, 2), pady=2, sticky="w")

# PAGINAÇÃO
paginacao_frame = ctk.CTkFrame(tabela_bg_frame, fg_color="transparent")
paginacao_frame.place(relx=0.5, rely=0.92, anchor="center")

label_registros = ctk.CTkLabel(paginacao_frame, text="Mostrando 1 até 10 de 40 registros", font=("Arial", 10), text_color="white", fg_color="transparent")
label_registros.pack(side="left", padx=(0, 20))

for i in range(1, 6):
    if i == 1:
        btn = ctk.CTkButton(paginacao_frame, text=str(i), width=30, fg_color="#D2FF28", text_color="black", hover_color="darkblue")
    else:
        btn = ctk.CTkButton(paginacao_frame, text=str(i), width=30, fg_color="#F5F5F5", text_color="black", hover_color="#E0E0E0")
    btn.pack(side="left", padx=2)

root.mainloop()
