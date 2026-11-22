import customtkinter as ctk
import sqlite3
import math # Importado para math.ceil

DB_PATH = 'banco.db' # Certifique-se que este arquivo está no mesmo diretório

# Lista completa de esportes olímpicos (fallback)
MODALIDADES_OLIMPICAS_FALLBACK = ["Todos os Esportes", "Atletismo", "Badminton", "Basquete", "Boxe", "Breaking",
                                  "Canoagem de Velocidade", "Canoagem Slalom", "Ciclismo BMX Freestyle",
                                  "Ciclismo BMX Racing", "Ciclismo de Estrada", "Ciclismo de Pista",
                                  "Ciclismo Mountain Bike", "Escalada Esportiva", "Esgrima", "Futebol",
                                  "Ginástica Artística", "Ginástica de Trampolim", "Ginástica Rítmica", "Golfe",
                                  "Handebol", "Hipismo Adestramento", "Hipismo CCE", "Hipismo Saltos",
                                  "Hóquei sobre Grama", "Judô", "Levantamento de Peso", "Luta Estilo Livre",
                                  "Luta Greco-Romana", "Maratona Aquática", "Nado Artístico", "Natação",
                                  "Pentatlo Moderno", "Polo Aquático", "Remo", "Rugby Sevens", "Saltos Ornamentais",
                                  "Skate Park", "Skate Street", "Surfe", "Taekwondo", "Tênis", "Tênis de Mesa",
                                  "Tiro com Arco", "Tiro Esportivo", "Triatlo", "Vela", "Vôlei de Praia", "Voleibol"]

# Lista simplificada de países olímpicos (fallback)
PAISES_OLIMPICOS_FALLBACK = [
    "Todos os Países", "Afeganistão", "África do Sul", "Albânia", "Alemanha", "Andorra", "Angola", "Arábia Saudita", "Argélia", "Argentina",
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
ANOS_OLIMPICOS_FALLBACK = ["Todos os Anos", "1896", "1900", "1904", "1908", "1912", "1920", "1924", "1928", "1932", "1936", "1948", "1952", "1956", "1960", "1964", "1968",
                           "1972", "1976", "1980", "1984", "1988", "1992", "1996", "2000", "2004", "2008", "2012", "2016", "2020", "2024"]

class DataExplorerView(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Resultados Olímpicos - Exploração de Dados")
        self.geometry("1000x750")
        self.resizable(True, True)
        self.configure(fg_color="#0E131F")
        self.grab_set()

        self.colunas_db_para_exibir = {
            "ano": "ANO",
            "pais": "PAÍS",
            "esporte": "ESPORTE",
            "evento": "EVENTO",
            "medalha": "MEDALHA",
            "nome_atleta": "ATLETA"
        }

        # Atributos para paginação
        self.current_page = 1
        self.items_per_page = 30 
        self.all_filtered_data = [] 
        self.page_buttons = [] 
        self.max_page_buttons_to_show = 5 

        self.verificar_nomes_colunas_db() 

        self.filtros_frame = ctk.CTkFrame(self, fg_color="#D2FF28", corner_radius=15, height=150)
        self.filtros_frame.pack(fill="x", padx=18, pady=(18, 10))
        self.filtros_frame.grid_columnconfigure((0,1,2,3,4), weight=0)
        self.filtros_frame.grid_columnconfigure(5, weight=1)

        label_filtros = ctk.CTkLabel(self.filtros_frame, text="Filtragem de dados olímpicos", font=("Arial", 18, "bold"), text_color="black")
        label_filtros.grid(row=0, column=0, columnspan=5, sticky="w", padx=(20,0), pady=(12, 10))

        ctk.CTkLabel(self.filtros_frame, text="País", font=("Arial", 12), text_color="black").grid(row=1, column=0, sticky="w", padx=(20,2), pady=(8,0))
        self.combo_pais = ctk.CTkComboBox(self.filtros_frame, width=180, values=self.carregar_valores_distintos_db('pais', PAISES_OLIMPICOS_FALLBACK))
        self.combo_pais.set("Todos os Países")
        self.combo_pais.grid(row=2, column=0, padx=(20,8), pady=(2,8))

        ctk.CTkLabel(self.filtros_frame, text="Esporte", font=("Arial", 12), text_color="black").grid(row=1, column=1, sticky="w", padx=(12,2), pady=(8,0))
        self.combo_esporte = ctk.CTkComboBox(self.filtros_frame, width=180, values=self.carregar_valores_distintos_db('esporte', MODALIDADES_OLIMPICAS_FALLBACK))
        self.combo_esporte.set("Todos os Esportes")
        self.combo_esporte.grid(row=2, column=1, padx=8, pady=(2,8))

        ctk.CTkLabel(self.filtros_frame, text="Tipo de Medalha", font=("Arial", 12), text_color="black").grid(row=1, column=2, sticky="w", padx=(12,2), pady=(8,0))
        self.combo_medalha = ctk.CTkComboBox(self.filtros_frame, width=150, values=["Todas as Medalhas", "Gold", "Silver", "Bronze", "NA"])
        self.combo_medalha.set("Todas as Medalhas")
        self.combo_medalha.grid(row=2, column=2, padx=8, pady=(2,8))

        ctk.CTkLabel(self.filtros_frame, text="Ano", font=("Arial", 12), text_color="black").grid(row=1, column=3, sticky="w", padx=(12,2), pady=(8,0))
        self.combo_ano = ctk.CTkComboBox(self.filtros_frame, width=150, values=self.carregar_valores_distintos_db('ano', ANOS_OLIMPICOS_FALLBACK, order_desc=True))
        self.combo_ano.set("Todos os Anos")
        self.combo_ano.grid(row=2, column=3, padx=8, pady=(2,8))

        self.botao_aplicar = ctk.CTkButton(self.filtros_frame, text="Aplicar Filtros", width=130, fg_color="#0E131F", hover_color="#1A202C", text_color="white", command=self.aplicar_filtros_e_resetar_pagina)
        self.botao_reset = ctk.CTkButton(self.filtros_frame, text="Redefinir Filtros", width=130, fg_color="#0E131F", hover_color="#1A202C", text_color="white", border_width=1, border_color="#124117", command=self.resetar_filtros_e_atualizar)
        self.botao_aplicar.grid(row=2, column=4, padx=(18,20), pady=(2,8))
        self.botao_reset.grid(row=3, column=0, columnspan=2, padx=(20,0), pady=(5,20), sticky="w")

        self.tabela_bg_frame = ctk.CTkFrame(self, fg_color="#0E131F", corner_radius=15)
        self.tabela_bg_frame.pack(pady=(0,10), fill="both", expand=True, padx=18)

        self.info_tabela_frame = ctk.CTkFrame(self.tabela_bg_frame, fg_color="transparent")
        self.info_tabela_frame.pack(fill="x", padx=10, pady=(10,5))

        self.label_titulo_tabela = ctk.CTkLabel(self.info_tabela_frame, text="Resultados Olímpicos", font=("Arial", 14, "bold"), text_color="white")
        self.label_titulo_tabela.pack(side="left")

        self.label_resultados_contador = ctk.CTkLabel(self.info_tabela_frame, text="Resultados: 0", font=("Arial", 12), text_color="white")
        self.label_resultados_contador.pack(side="right")

        self.scrollable_tabela_frame = ctk.CTkScrollableFrame(self.tabela_bg_frame, fg_color="#FFFFFF", corner_radius=10)
        # ALTERADO: fill="both" para preencher o espaço e expand=True
        self.scrollable_tabela_frame.pack(pady=(0,10), padx=20, fill="both", expand=True) 
        
        self.paginacao_frame = ctk.CTkFrame(self.tabela_bg_frame, fg_color="transparent")
        self.paginacao_frame.pack(pady=(5,10)) 
        self.label_registros_paginacao = ctk.CTkLabel(self.paginacao_frame, text="Mostrando 0 até 0 de 0 registros", font=("Arial", 10), text_color="white")
        self.label_registros_paginacao.pack(side="left", padx=(0, 10)) 
        
        self.btn_prev_page = ctk.CTkButton(self.paginacao_frame, text="<", width=40, 
                                           fg_color="#FFFFFF", text_color="#000000", 
                                           hover_color="#E0E0E0",
                                           command=lambda: self.go_to_page(self.current_page - 1))
        self.btn_prev_page.pack(side="left", padx=(0, 5))

        self.dynamic_page_buttons_frame = ctk.CTkFrame(self.paginacao_frame, fg_color="transparent")
        self.dynamic_page_buttons_frame.pack(side="left", padx=2)

        self.btn_next_page = ctk.CTkButton(self.paginacao_frame, text=">", width=40, 
                                           fg_color="#FFFFFF", text_color="#000000",
                                           hover_color="#E0E0E0",
                                           command=lambda: self.go_to_page(self.current_page + 1))
        self.btn_next_page.pack(side="left", padx=5)
        
        self.criar_cabecalho_tabela()
        self.atualizar_tabela_com_filtros() 


    def verificar_nomes_colunas_db(self):
        print("--- DEBUG: Verificando nomes das colunas no banco de dados 'banco' ---")
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(banco)")
            colunas_info = cursor.fetchall()
            conn.close()
            if colunas_info:
                nomes_reais = [info[1] for info in colunas_info]
                print(f"Nomes REAIS das colunas na tabela 'banco': {nomes_reais}")
                print("Compare estes nomes com as CHAVES (primeiro item) em self.colunas_db_para_exibir:")
                for chave_usada, titulo_gui in self.colunas_db_para_exibir.items():
                    if chave_usada not in nomes_reais:
                        print(f"  AVISO: A chave '{chave_usada}' (para '{titulo_gui}') NÃO EXISTE nos nomes reais das colunas do DB!")
                    else:
                        print(f"  OK: A chave '{chave_usada}' (para '{titulo_gui}') existe no DB.")
            else:
                print("AVISO: Não foi possível obter informações da tabela 'banco'. Ela existe e não está vazia?")
        except sqlite3.Error as e:
            print(f"ERRO SQL ao tentar verificar nomes das colunas: {e}")
        print("--------------------------------------------------------------------")

    def carregar_valores_distintos_db(self, nome_coluna, fallback_lista, order_desc=False):
        nome_coluna_sql = f'"{nome_coluna}"'
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            order_clause = "DESC" if order_desc else "ASC"
            query = f"SELECT DISTINCT CAST({nome_coluna_sql} AS TEXT) FROM banco WHERE {nome_coluna_sql} IS NOT NULL AND TRIM({nome_coluna_sql}) != '' ORDER BY CAST({nome_coluna_sql} AS TEXT) {order_clause}"
            cursor.execute(query)
            valores = [str(row[0]) for row in cursor.fetchall()] 
            conn.close()
            if fallback_lista and fallback_lista[0].startswith("Todos"):
                return [fallback_lista[0]] + valores if valores else fallback_lista
            return valores if valores else fallback_lista[1:]
        except sqlite3.Error as e:
            print(f"Erro ao carregar '{nome_coluna}' do banco (query: {query}): {e}")
            return fallback_lista

    def criar_cabecalho_tabela(self):
        # ALTERADO: Configura as colunas do grid para expandir
        # O peso (weight) determina a proporção do espaço extra que cada coluna recebe
        self.scrollable_tabela_frame.grid_columnconfigure(0, weight=1)  # ANO
        self.scrollable_tabela_frame.grid_columnconfigure(1, weight=3)  # PAÍS
        self.scrollable_tabela_frame.grid_columnconfigure(2, weight=3)  # ESPORTE
        self.scrollable_tabela_frame.grid_columnconfigure(3, weight=5)  # EVENTO
        self.scrollable_tabela_frame.grid_columnconfigure(4, weight=2)  # MEDALHA
        self.scrollable_tabela_frame.grid_columnconfigure(5, weight=5)  # ATLETA

        headers = list(self.colunas_db_para_exibir.values())
        for i, header_text in enumerate(headers):
            # Removido width=... para permitir que o grid controle a largura
            label = ctk.CTkLabel(self.scrollable_tabela_frame, text=header_text, font=("Arial", 14, "bold"),
                                 text_color="#787878", anchor="center") 
            label.grid(row=0, column=i, padx=(8 if i==0 else 2, 2), pady=(12,4), sticky="ew")
        print("DEBUG: Cabeçalho da tabela criado.")

    def aplicar_filtros_e_resetar_pagina(self):
        self.current_page = 1
        self.atualizar_tabela_com_filtros()

    def atualizar_tabela_com_filtros(self):
        print("\nDEBUG: Iniciando atualizar_tabela_com_filtros (busca completa)...")
        
        select_cols_keys = list(self.colunas_db_para_exibir.keys())
        select_cols_str = ", ".join([f'"{col}"' for col in select_cols_keys])
        
        query = f"SELECT {select_cols_str} FROM banco WHERE 1=1"
        params = []

        if self.combo_pais.get() != "Todos os Países": query += f' AND "pais" = ?'; params.append(self.combo_pais.get())
        if self.combo_esporte.get() != "Todos os Esportes": query += f' AND "esporte" = ?'; params.append(self.combo_esporte.get())
        if self.combo_medalha.get() != "Todas as Medalhas": query += f' AND "medalha" = ?'; params.append(self.combo_medalha.get())
        if self.combo_ano.get() != "Todos os Anos": query += f' AND "ano" = ?'; params.append(self.combo_ano.get())
        
        query += ' ORDER BY CAST("ano" AS INTEGER) DESC, "nome_atleta"'
        print(f"DEBUG: Query SQL (busca completa): {query}")
        print(f"DEBUG: Parâmetros: {params}")

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(query, params)
            self.all_filtered_data = cursor.fetchall()
            conn.close()
            print(f"DEBUG: {len(self.all_filtered_data)} linhas TOTAIS obtidas do banco para os filtros.")
        except sqlite3.Error as e:
            print(f"ERRO SQL ao buscar dados filtrados: {e}")
            self.all_filtered_data = [] 
            for widget in self.scrollable_tabela_frame.winfo_children(): 
                if widget.grid_info()['row'] > 0: widget.destroy()
            error_label = ctk.CTkLabel(self.scrollable_tabela_frame, text=f"Erro ao buscar dados:\n{e}", text_color="red", wraplength=self.scrollable_tabela_frame.winfo_width()-30)
            error_label.grid(row=1, column=0, columnspan=len(self.colunas_db_para_exibir), pady=10, sticky="ew")
            self.label_resultados_contador.configure(text="Resultados: Erro")
            return
        
        self.label_resultados_contador.configure(text=f"Resultados: {len(self.all_filtered_data)}")
        self.display_page_data() 
        self.update_pagination_ui_buttons() 

    def display_page_data(self):
        print(f"DEBUG: Exibindo página {self.current_page}...")
        for widget in self.scrollable_tabela_frame.winfo_children():
            if widget.grid_info()['row'] > 0: 
                widget.destroy()

        if not self.all_filtered_data:
            print("DEBUG: Nenhum dado filtrado para exibir na página.")
            no_data_label = ctk.CTkLabel(self.scrollable_tabela_frame, text="Nenhum resultado encontrado.", text_color="#787878")
            no_data_label.grid(row=1, column=0, columnspan=len(self.colunas_db_para_exibir), pady=10, sticky="ew")
            if hasattr(self, 'label_registros_paginacao'):
                self.label_registros_paginacao.configure(text="Mostrando 0 até 0 de 0 registros")
            self.scrollable_tabela_frame.update_idletasks()
            return

        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        page_data_to_display = self.all_filtered_data[start_index:end_index]

        print(f"DEBUG: Exibindo {len(page_data_to_display)} registros nesta página (índices {start_index}-{end_index-1}).")

        medal_bg_colors = {
            "Gold": "#FFD700",   
            "Silver": "#C0C0C0", 
            "Bronze": "#CD7F32"  
        }
        default_text_color = "#101010"
        medal_text_color = "#000000" 

        for row_idx_gui, row_data in enumerate(page_data_to_display, start=1): 
            for col_idx, cell_value in enumerate(row_data):
                cell_text = str(cell_value if cell_value is not None else "")
                current_col_name = list(self.colunas_db_para_exibir.keys())[col_idx] 
                
                fg_color_cell = ["#FFFFFF", "#F0F0F0"][row_idx_gui % 2] 
                text_color_cell = default_text_color

                if current_col_name == "medalha":
                    medal_type = cell_text
                    if medal_type in medal_bg_colors:
                        fg_color_cell = medal_bg_colors[medal_type]
                        text_color_cell = medal_text_color 
                
                # Removido wraplength para permitir que o grid controle o tamanho
                label = ctk.CTkLabel(self.scrollable_tabela_frame, 
                                     text=cell_text, font=("Arial", 13),
                                     text_color=text_color_cell, fg_color=fg_color_cell,
                                     anchor="center")
                if col_idx < len(self.colunas_db_para_exibir):
                     label.grid(row=row_idx_gui, column=col_idx, padx=2, pady=0, sticky="ew") # sticky="ew" para expandir horizontalmente
        
        total_records = len(self.all_filtered_data)
        start_record_num = min(start_index + 1, total_records) if total_records > 0 else 0
        end_record_num = min(end_index, total_records)
        
        if hasattr(self, 'label_registros_paginacao'):
            self.label_registros_paginacao.configure(text=f"Mostrando {start_record_num} até {end_record_num} de {total_records} registros")
        
        self.scrollable_tabela_frame.update_idletasks()
        if self.master: self.master.update_idletasks()
        print(f"DEBUG: Fim de display_page_data para página {self.current_page}.")


    def go_to_page(self, page_num):
        print(f"DEBUG: go_to_page chamada com page_num: {page_num}")
        total_pages = math.ceil(len(self.all_filtered_data) / self.items_per_page)
        if total_pages == 0: total_pages = 1 

        if 1 <= page_num <= total_pages:
            self.current_page = page_num
            self.display_page_data()
            self.update_pagination_ui_buttons()
        else:
            print(f"DEBUG: Tentativa de ir para página inválida {page_num}. Total de páginas: {total_pages}")


    def update_pagination_ui_buttons(self):
        for btn in self.page_buttons:
            btn.destroy()
        self.page_buttons.clear()

        total_pages = math.ceil(len(self.all_filtered_data) / self.items_per_page)
        if total_pages == 0: total_pages = 1

        print(f"DEBUG: Atualizando UI dos botões de paginação. Página atual: {self.current_page}, Total de páginas: {total_pages}")

        start_page_num_display = max(1, self.current_page - (self.max_page_buttons_to_show // 2))
        end_page_num_display = min(total_pages, start_page_num_display + self.max_page_buttons_to_show - 1)

        if end_page_num_display - start_page_num_display + 1 < self.max_page_buttons_to_show and total_pages >= self.max_page_buttons_to_show :
            start_page_num_display = max(1, end_page_num_display - self.max_page_buttons_to_show + 1)
        
        for i in range(start_page_num_display, end_page_num_display + 1):
            btn = ctk.CTkButton(self.dynamic_page_buttons_frame, text=str(i), width=30,
                                command=lambda p=i: self.go_to_page(p))
            if i == self.current_page:
                btn.configure(fg_color="#D2FF28", text_color="black")
            else:
                btn.configure(fg_color="#F5F5F5", text_color="black")
            btn.pack(side="left", padx=2)
            self.page_buttons.append(btn)
        
        if self.current_page == 1:
            self.btn_prev_page.configure(state="disabled")
        else:
            self.btn_prev_page.configure(state="normal")

        if self.current_page == total_pages or total_pages == 0 :
            self.btn_next_page.configure(state="disabled")
        else:
            self.btn_next_page.configure(state="normal")


    def resetar_filtros_e_atualizar(self):
        self.combo_pais.set("Todos os Países")
        self.combo_esporte.set("Todos os Esportes")
        self.combo_medalha.set("Todas as Medalhas")
        self.combo_ano.set("Todos os Anos")
        self.aplicar_filtros_e_resetar_pagina()

if __name__ == "__main__":
    test_root = ctk.CTk()
    test_root.title("Teste Tela Exploração")
    test_root.geometry("300x200")
    def open_explorer():
        explorer = DataExplorerView(test_root)
    btn_open = ctk.CTkButton(test_root, text="Abrir Tela de Exploração", command=open_explorer)
    btn_open.pack(pady=20, padx=20)
    test_root.mainloop()
