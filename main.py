#XXXXXXXXXXXXXXXXXXXXXXX
#XX COMEÇO DO MAIN.PY XX
#XXXXXXXXXXXXXXXXXXXXXXX
import customtkinter as ctk
from tkinter import StringVar, ttk
from math import gcd
from PIL import Image
from threading import Thread
import random
import time
import os
from functions import (
    interface_manager,
    criar_reino,
    excluir_reino,
    carregar_dados_json,
    salvar_dados_json,
    processar_rolagem_de_turno,
    atualizar_reino,
    verificar_e_inicializar_turno
)
from menus import abrir_editar_tropas, abrir_economia, abrir_tecnologias

################################
#                              #
#  Initial Configuration       #
#                              #
################################

ctk.set_default_color_theme(os.path.join(os.path.dirname(__file__), "estilo_visual.json"))
verificar_e_inicializar_turno()

app = ctk.CTk()
app.title("PPG RPG")
app.geometry("970x850")

# Definir o ícone do aplicativo
app.iconbitmap(os.path.join(os.path.dirname(__file__), "logo.ico"))

def incrementar_turno():
    turno_atual = processar_rolagem_de_turno()
    label_turno_atual.configure(text=f"Turno {turno_atual}")
    interface_manager.atualizar_interface(seletor_reino.get())
    print("Turno incrementado e economia atualizada.")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", rowheight=25)
style.configure("Treeview.Heading", background="#1f1f1f", foreground="white", font=("Arial", 12, "bold"))
style.map('Treeview', background=[('selected', '#565656')], foreground=[('selected', 'white')])

dados = carregar_dados_json()
turno_atual = dados.get("turno_atual", 1)


tabview_principal = ctk.CTkTabview(app, width=850, height=700)
tabview_principal.pack(pady=10, padx=10, fill="both", expand=True)

tab_gerenciamento = tabview_principal.add("Gerenciamento")
tab_config = tabview_principal.add("Configurações")

################################
#                              #
#  Gerenciamento Tab           #
#                              #
################################

frame_gerenciamento = ctk.CTkFrame(tab_gerenciamento, width=760, height=700)
frame_gerenciamento.pack(pady=10, padx=10, fill="both", expand=True)

seletor_reino = ctk.CTkOptionMenu(frame_gerenciamento, values=[], command=lambda _: interface_manager.atualizar_interface(seletor_reino.get()))
seletor_reino.pack(pady=5)

frame_detalhes_zero = ctk.CTkFrame(frame_gerenciamento, width=220, height=380, fg_color="#1f1f1f", corner_radius=8)
frame_detalhes_zero.pack(pady=10, padx=10, side="left", fill="y")

tabview_detalhes_zero = ctk.CTkTabview(frame_detalhes_zero, width=220, height=360)
tabview_detalhes_zero.pack(pady=10, padx=10, fill="both", expand=True)

tab_tropas_zero = tabview_detalhes_zero.add("Tropas")
tab_interno_zero = tabview_detalhes_zero.add("Interno")

labels_tropas = []
for nome_tropa in ["Infantaria Leve", "Infantaria Pesada", "Infantaria Armada", "Blindados Leves", "Blindados Pesados", "Fragatas", "Couracados", "Artilharia"]:
    label_nome = ctk.CTkLabel(tab_tropas_zero, text=nome_tropa, font=("Arial", 14, "bold"))
    label_nome.pack(pady=1)
    label_quantidade = ctk.CTkLabel(tab_tropas_zero, text="0", corner_radius=5, width=30)
    label_quantidade.pack(pady=1)
    labels_tropas.append(label_quantidade)


label_populacao_titulo_zero = ctk.CTkLabel(tab_interno_zero, text="POPULAÇÃO", font=("Arial", 16, "bold"))
label_populacao_titulo_zero.pack(pady=2)

label_populacao_valor_zero = ctk.CTkLabel(tab_interno_zero, text="0", font=("Arial", 16, "bold"))
label_populacao_valor_zero.pack(pady=3)

separador_tecnologias = ctk.CTkLabel(tab_interno_zero, text="_________________", font=("Arial", 12, "bold"))
separador_tecnologias.pack(pady=2)

label_tecnologias_titulo_zero = ctk.CTkLabel(tab_interno_zero, text="TECNOLOGIAS", font=("Arial", 16, "bold"))
label_tecnologias_titulo_zero.pack(pady=2)

# Adicionar frame rolável para tecnologias
frame_tecnologias = ctk.CTkScrollableFrame(tab_interno_zero, width=100, height=200)
frame_tecnologias.pack(pady=0, padx=0, fill="both", expand=True)

frame_tabela_zero = ctk.CTkFrame(frame_gerenciamento, width=500, height=380)
frame_tabela_zero.pack(pady=10, padx=10, side="top", fill="both", expand=True)

tabela_zero = ttk.Treeview(frame_tabela_zero, columns=("col1", "col2"), show="headings", style="Treeview")
tabela_zero.pack(fill="both", expand=True)

tabela_zero.heading("col1", text="Descrição")
tabela_zero.heading("col2", text="Receita/Despesas")

tabela_zero.column("col1", width=250)
tabela_zero.column("col2", width=200)

frame_totais_zero = ctk.CTkFrame(frame_gerenciamento, fg_color="#1f1f1f")
frame_totais_zero.pack(pady=10, padx=10, side="top", fill="x")

label_total_fundos_zero = ctk.CTkLabel(frame_totais_zero, text="TOTAL DE FUNDOS: ", font=("Arial", 14, "bold"))
label_total_fundos_zero.grid(row=0, column=0, padx=10, pady=5, sticky="w")
label_valor_fundos_zero = ctk.CTkLabel(frame_totais_zero, text="R$ 0,00", font=("Arial", 14, "bold"))
label_valor_fundos_zero.grid(row=0, column=1, padx=10, pady=5, sticky="w")

label_total_esperado_zero = ctk.CTkLabel(frame_totais_zero, text="TOTAL PREVISTO: ", font=("Arial", 14, "bold"))
label_total_esperado_zero.grid(row=1, column=0, padx=10, pady=5, sticky="w")
label_valor_esperado_zero = ctk.CTkLabel(frame_totais_zero, text="R$ 0,00", font=("Arial", 14, "bold"))
label_valor_esperado_zero.grid(row=1, column=1, padx=10, pady=5, sticky="w")

frame_botoes_zero = ctk.CTkFrame(frame_gerenciamento)
frame_botoes_zero.pack(pady=10, padx=10, side="top", fill="x")

botao_editar_tropas_zero = ctk.CTkButton(frame_botoes_zero, text="Editar Tropas", width=120, command=lambda: abrir_editar_tropas(seletor_reino.get()))
botao_editar_tropas_zero.pack(pady=5, padx=5, side="left", expand=True)

botao_tecnologias_zero = ctk.CTkButton(frame_botoes_zero, text="Tecnologias", width=120, command=lambda: abrir_tecnologias(seletor_reino.get()))
botao_tecnologias_zero.pack(pady=5, padx=5, side="left", expand=True)

botao_economia_zero = ctk.CTkButton(frame_botoes_zero, text="Economia", width=120, command=lambda: abrir_economia(seletor_reino.get()))
botao_economia_zero.pack(pady=5, padx=5, side="left", expand=True)

################################
#                              #
# Combate Tab                  #
#                              #
################################

mapa_imagens_proeficiencia = {
    "Medieval": {
        None: "medieval.png",
        "Proeficiencia I": "medieval_proeficiencia_I.png",
        "Proeficiencia II": "medieval_proeficiencia_II.png",
        "Proeficiencia III": "medieval_proeficiencia_III.png",
        "Proeficiencia IV": "medieval_proeficiencia_IV.png",
        "Proeficiencia V": "medieval_proeficiencia_V.png",
        "Proeficiencia VI": "medieval_proeficiencia_VI.png"
    },
    "Medieval Pesado": {
        None: "medieval_pesado.png",
        "Proeficiencia I": "medieval_pesado_proeficiencia_I.png",
        "Proeficiencia II": "medieval_pesado_proeficiencia_II.png",
        "Proeficiencia III": "medieval_pesado_proeficiencia_III.png",
        "Proeficiencia IV": "medieval_pesado_proeficiencia_IV.png",
        "Proeficiencia V": "medieval_pesado_proeficiencia_V.png",
        "Proeficiencia VI": "medieval_pesado_proeficiencia_VI.png"
    },
    "Infantaria": {
        None: "infantaria.png",
        "Proeficiencia I": "infantaria_proeficiencia_I.png",
        "Proeficiencia II": "infantaria_proeficiencia_II.png",
        "Proeficiencia III": "infantaria_proeficiencia_III.png",
        "Proeficiencia IV": "infantaria_proeficiencia_IV.png",
        "Proeficiencia V": "infantaria_proeficiencia_V.png",
        "Proeficiencia VI": "infantaria_proeficiencia_VI.png"
    },
    "Torre": {
        None: "torre.png",
        "Torres I": "torre_I.png",
        "Torres II": "torre_II.png",
        "Torres III": "torre_III.png"
    },
    "Cerco": {
        None: "cerco.png",
        "Cercos I": "cerco_I.png",
        "Cercos II": "cerco_II.png",
        "Cercos III": "cerco_III.png"
    },
    "Blindado Leve": {
        None: "blindado_leve.png"
    },
    "Blindado Pesado": {
        None: "blindado_pesado.png"
    },
    "Fragata": {
        None: "fragata.png"
    },
    "Artilharia": {
        None: "artilharia.png"
    },
    "Couraçado": {
        None: "couracado.png"
    }
}


# Função para obter o nível máximo de Proeficiencia disponível
def obter_nivel_proeficiencia(tecnologias):
    niveis_proeficiencia = ["Proeficiencia I", "Proeficiencia II", "Proeficiencia III", "Proeficiencia IV", "Proeficiencia V"]
    for nivel in reversed(niveis_proeficiencia):
        if nivel in tecnologias:
            return nivel
    return None

def atualizar_imagem_tropas(frame, tropa, reino, inverter=False):
    diretorio_imagens = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tropas")
    tecnologias = reino.get("tecnologias", [])
    
    # Verifica se a tropa é Blindado Leve, Blindado Pesado, Couraçado ou Fragata
    if tropa in ["Blindado Leve", "Blindado Pesado", "Couraçado", "Fragata"]:
        nome_imagem = f"{tropa.lower().replace(' ', '_')}_02.png" if inverter else f"{tropa.lower().replace(' ', '_')}.png"

    # Se a tropa for Torre, usa a tecnologia de torres ao invés da proeficiência
    elif tropa == "Torre":
        niveis_torres = ["Torres III", "Torres II", "Torres I"]  # Ordem da mais avançada para a básica
        nivel_torre = next((nivel for nivel in niveis_torres if nivel in tecnologias), None)
        nome_imagem = mapa_imagens_proeficiencia["Torre"].get(nivel_torre, "torre.png") if nivel_torre else "torre.png"

    # Se a tropa for uma máquina de cerco, seleciona a imagem baseada na tecnologia de cercos
    elif tropa == "Cerco":
        niveis_cercos = ["Cercos III", "Cercos II", "Cercos I"]  # Ordem da mais avançada para a básica
        nivel_cerco = next((nivel for nivel in niveis_cercos if nivel in tecnologias), "Base")
        nome_imagem = mapa_imagens_proeficiencia["Cerco"].get(nivel_cerco, "cerco.png")

    # Verifica se a tropa é Infantaria
    elif tropa == "Infantaria":
        if "Armas Modernas" in tecnologias:
            nome_imagem = "infantaria_modern_02.png" if inverter else "infantaria_modern.png"
        elif "Armaduras Modulares" not in tecnologias and obter_nivel_proeficiencia(tecnologias):
            nome_imagem = "infantaria_padrao_02.png" if inverter else "infantaria_padrao_01.png"
        elif "Armaduras Modulares" not in tecnologias:
            nome_imagem = "infantaria.png"
        else:
            nivel_proeficiencia = obter_nivel_proeficiencia(tecnologias)
            nome_imagem = mapa_imagens_proeficiencia[tropa].get(nivel_proeficiencia, mapa_imagens_proeficiencia[tropa][None])

    # Lógica padrão de proeficiência para outras tropas
    else:
        nivel_proeficiencia = obter_nivel_proeficiencia(tecnologias)
        nome_imagem = mapa_imagens_proeficiencia.get(tropa, {}).get(nivel_proeficiencia, mapa_imagens_proeficiencia.get(tropa, {}).get(None, None))

    # Verificar se a imagem foi encontrada, caso contrário, usar a imagem padrão
    if nome_imagem:
        caminho_imagem = os.path.join(diretorio_imagens, nome_imagem)
        if not os.path.exists(caminho_imagem):
            nome_imagem = mapa_imagens_proeficiencia.get(tropa, {}).get(None, "default.png")
            caminho_imagem = os.path.join(diretorio_imagens, nome_imagem)

        # Verifica se o caminho da imagem existe antes de carregar
        if os.path.exists(caminho_imagem):
            imagem = Image.open(caminho_imagem)
            if inverter:
                imagem = imagem.transpose(Image.FLIP_LEFT_RIGHT)

            largura_fixa = 200
            altura_fixa = 200
            proporcao = min(largura_fixa / imagem.width, altura_fixa / imagem.height)
            nova_largura = int(imagem.width * proporcao)
            nova_altura = int(imagem.height * proporcao)

            imagem_resized = imagem.resize((nova_largura, nova_altura))
            img_ctk = ctk.CTkImage(imagem_resized, size=(nova_largura, nova_altura))
            
            for widget in frame.winfo_children():
                widget.destroy()
            
            label_imagem = ctk.CTkLabel(frame, image=img_ctk, text="")
            label_imagem.image = img_ctk
            label_imagem.pack(expand=True)
        else:
            print(f"Imagem '{nome_imagem}' não encontrada para a tropa {tropa}.")
    else:
        print(f"Nenhuma imagem disponível para a tropa: {tropa}.")





# Função para filtrar tecnologias e manter apenas as superiores
def filtrar_tecnologias(tecnologias):
    relevantes = [
        "Proeficiencia I", "Proeficiencia II", "Proeficiencia III", "Proeficiencia IV", "Proeficiencia V", "Proeficiencia VI",
        "Bandagem", "Armadura de placas", "Granadas", "Armas de Fogo I", "Armaduras Modulares", "Armas Modernas", "Armamento Anti-Tanque",
        "Torres I", "Torres II",  "Torres III", 
        "Cercos I", "Cercos II", "Cercos III",
        "Defesa I", "Defesa II", "Defesa III", "Defesa IV", "Defesa V", "Defesa VI"
    ]
    superiores = {"Proeficiencia": None, "Defesa": None, "Torres": None, "Cercos": None}
    
    filtradas = []
    for tecnologia in tecnologias:
        if tecnologia in relevantes:
            if "Proeficiencia" in tecnologia:
                superiores["Proeficiencia"] = max(superiores["Proeficiencia"], tecnologia) if superiores["Proeficiencia"] else tecnologia
            elif "Defesa" in tecnologia:
                superiores["Defesa"] = max(superiores["Defesa"], tecnologia) if superiores["Defesa"] else tecnologia
            elif "Torres" in tecnologia:
                superiores["Torres"] = max(superiores["Torres"], tecnologia) if superiores["Torres"] else tecnologia
            elif "Cercos" in tecnologia:
                superiores["Cercos"] = max(superiores["Cercos"], tecnologia) if superiores["Cercos"] else tecnologia
            else:
                filtradas.append(tecnologia)
    
    # Adiciona as tecnologias superiores ao final da lista filtrada
    if superiores["Proeficiencia"]:
        filtradas.append(superiores["Proeficiencia"])
    if superiores["Defesa"]:
        filtradas.append(superiores["Defesa"])
    if superiores["Torres"]:
        filtradas.append(superiores["Torres"])
    if superiores["Cercos"]:
        filtradas.append(superiores["Cercos"])

    return filtradas


# Função para configurar o estilo da tabela
def configurar_estilo_tabela(tabela):
    style = ttk.Style()
    style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"), anchor="center")
    tabela.tag_configure("Proeficiencia VI", foreground="#8000FF", font=("Arial", 12, "bold"), anchor="center")
    tabela.tag_configure("Proeficiencia V", foreground="#ffee03", font=("Arial", 12, "bold"), anchor="center")
    tabela.tag_configure("Proeficiencia IV", foreground="#ff0000", font=("Arial", 11, "bold"), anchor="center")
    tabela.tag_configure("Proeficiencia III", foreground="#ffae00", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Proeficiencia II", foreground="#00ff2a", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Proeficiencia I", foreground="#4287f5", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Bandagem", foreground="#f8fc86", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Armadura de placas", foreground="#bababa", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Granadas", foreground="#c6f74a", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Defesa VI", foreground="#8000FF", font=("Arial", 11, "bold"), anchor="center")
    tabela.tag_configure("Defesa V", foreground="#ffee03", font=("Arial", 11, "bold"), anchor="center")
    tabela.tag_configure("Defesa IV", foreground="#ff0000", font=("Arial", 11, "bold"), anchor="center")
    tabela.tag_configure("Defesa III", foreground="#ffae00", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Defesa II", foreground="#00ff2a", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Defesa I", foreground="#4287f5", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Armas de Fogo I", foreground="#36d8f5", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Armaduras Modulares", foreground="#36f5af", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Armas Modernas", foreground="#ff160a", font=("Arial", 11, "bold"), anchor="center")
    tabela.tag_configure("Armamento Anti-Tanque", foreground="#ff6159", font=("Arial", 11, "bold"), anchor="center")
    tabela.tag_configure("Torres I", foreground="#4287f5", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Torres II", foreground="#00ff2a", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Torres III", foreground="#ffae00", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Cercos I", foreground="#4287f5", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Cercos II", foreground="#00ff2a", font=("Arial", 10, "bold"), anchor="center")
    tabela.tag_configure("Cercos III", foreground="#ffae00", font=("Arial", 10, "bold"), anchor="center")




# Função para ordenar habilidades de forma que as mais importantes fiquem no topo
def ordenar_tecnologias(tecnologias):
    ordem_importancia = {
        "Proeficiencia V": 1,
        "Proeficiencia IV": 2,
        "Proeficiencia III": 3,
        "Proeficiencia II": 4,
        "Proeficiencia I": 5,
        "Defesa IV": 6,
        "Defesa III": 7,
        "Defesa II": 8,
        "Defesa I": 9
    }
    
    # Ordena as tecnologias por importância, depois por aquelas que são únicas
    tecnologias_ordenadas = sorted(
        tecnologias,
        key=lambda t: ordem_importancia.get(t, 100)  # As não listadas na ordem de importância ficam no final
    )
    return tecnologias_ordenadas

# Função para atualizar as habilidades na tabela da esquerda
def atualizar_habilidades_esquerdo(reino, dados, tabela_habilidades_esquerdo):
    tecnologias = dados["reinos"].get(reino, {}).get("tecnologias", [])
    tecnologias_filtradas = filtrar_tecnologias(tecnologias)
    tecnologias_ordenadas = ordenar_tecnologias(tecnologias_filtradas)
    tabela_habilidades_esquerdo.delete(*tabela_habilidades_esquerdo.get_children())

    # Inserir as tecnologias ordenadas na tabela
    for tecnologia in tecnologias_ordenadas:
        tabela_habilidades_esquerdo.insert("", "end", values=(tecnologia,), tags=(tecnologia,))

# Função para atualizar as habilidades na tabela da direita
def atualizar_habilidades_direito(reino, dados, tabela_habilidades_direito):
    tecnologias = dados["reinos"].get(reino, {}).get("tecnologias", [])
    tecnologias_filtradas = filtrar_tecnologias(tecnologias)
    tecnologias_ordenadas = ordenar_tecnologias(tecnologias_filtradas)
    tabela_habilidades_direito.delete(*tabela_habilidades_direito.get_children())

    # Inserir as tecnologias ordenadas na tabela
    for tecnologia in tecnologias_ordenadas:
        tabela_habilidades_direito.insert("", "end", values=(tecnologia,), tags=(tecnologia,))



# Funções de callback para os seletores
def on_select_reino_esquerdo(reino):
    dados = carregar_dados_json()
    atualizar_habilidades_esquerdo(reino, dados, tabela_habilidades_esquerdo)
    atualizar_imagem_tropas(frame_imagem_tropas_esquerdo, seletor_tropas_esquerdo.get(), dados["reinos"].get(reino, {}), inverter=True)


def on_select_reino_direito(reino):
    dados = carregar_dados_json()
    atualizar_habilidades_direito(reino, dados, tabela_habilidades_direito)
    atualizar_imagem_tropas(frame_imagem_tropas_direito, seletor_tropas_direito.get(), dados["reinos"].get(reino, {}), inverter=False)

def on_select_tropa_esquerdo(tropa):
    global hp_esquerdo
    reino_selecionado = seletor_reino_esquerdo.get()
    dados = carregar_dados_json()

    # Atualiza a imagem da tropa
    atualizar_imagem_tropas(frame_imagem_tropas_esquerdo, tropa, dados["reinos"].get(reino_selecionado, {}), inverter=True)

    # Atualiza o HP da tropa baseado em tecnologias
    tecnologias = dados["reinos"].get(reino_selecionado, {}).get("tecnologias", [])
    hp_esquerdo = calcular_hp(tecnologias, tropa)

    barra_hp_esquerdo.set(1)  # Define o HP visualmente no máximo
    atualizar_texto_hp("esquerdo")  # Atualiza o texto da barra

    # Se a tropa estava marcada como morta, remover o label "MORTO" e restaurar a barra
    label_morto_esquerdo.pack_forget()
    barra_hp_esquerdo.pack(pady=5)
    label_hp_esquerdo.pack(pady=5)


def on_select_tropa_direito(tropa):
    global hp_direito
    reino_selecionado = seletor_reino_direito.get()
    dados = carregar_dados_json()

    # Atualiza a imagem da tropa
    atualizar_imagem_tropas(frame_imagem_tropas_direito, tropa, dados["reinos"].get(reino_selecionado, {}), inverter=False)

    # Atualiza o HP da tropa baseado em tecnologias
    tecnologias = dados["reinos"].get(reino_selecionado, {}).get("tecnologias", [])
    hp_direito = calcular_hp(tecnologias, tropa)

    barra_hp_direito.set(1)  # Define o HP visualmente no máximo
    atualizar_texto_hp("direito")  # Atualiza o texto da barra

    # Se a tropa estava marcada como morta, remover o label "MORTO" e restaurar a barra
    label_morto_direito.pack_forget()
    barra_hp_direito.pack(pady=5)
    label_hp_direito.pack(pady=5)



# Função para simular a barra de progresso e executar a ação de movimentação
def executar_movimento():
    # Ocultar os botões e mostrar a barra de progresso
    botao_movimento.grid_remove()
    botao_atacar.grid_remove()
    frame_barra_progresso_movimento.grid()
    simular_barra_progresso_movimento(0)

# Função para simular a barra de progresso
def simular_barra_progresso_movimento(valor_atual):
    label_acao_texto_esquerdo.configure(text="Nenhuma", font=("Arial", 12), text_color="white")
    label_acao_texto_direito.configure(text="Nenhuma", font=("Arial", 12), text_color="white")
    if valor_atual <= 100:
        barra_progresso_movimento.set(valor_atual / 100.0)  # Atualiza a barra de progresso
        frame_barra_progresso_movimento.after(5, simular_barra_progresso_movimento, valor_atual + 1)  # Incremento para mover a barra
    else:
        # Após o carregamento, restaura os botões e oculta a barra de progresso
        frame_barra_progresso_movimento.grid_remove()

        lado = random.choice(["esquerdo", "direito"])
        
        if lado == "esquerdo":
            label_acao_texto_esquerdo.configure(text="MOVIMENTAR", font=("Arial", 16, "bold"), text_color="#1E90FF")  # Azul mais claro
            label_acao_texto_direito.configure(text="Nenhuma", font=("Arial", 12), text_color="white")
        else:
            label_acao_texto_direito.configure(text="MOVIMENTAR", font=("Arial", 16, "bold"), text_color="#1E90FF")  # Azul mais claro
            label_acao_texto_esquerdo.configure(text="Nenhuma", font=("Arial", 12), text_color="white")

        # Mostrar novamente os botões
        botao_movimento.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        botao_atacar.grid(row=0, column=1, padx=10, pady=10, sticky="ew")



############
#  ATAQUE  #
############


# Função para simular o ataque
def executar_ataque():
    # Ocultar os botões e mostrar a barra de progresso
    botao_movimento.grid_remove()
    botao_atacar.grid_remove()
    frame_barra_progresso_movimento.grid()
    simular_barra_progresso_ataque(0)

import random
import random

# ------------------------------
# 🔹 TABELAS DE ATRIBUTOS
# ------------------------------


# Tabela combinada de ataque e proficiência
TABELA_ATAQUE_PROEFICIENCIA = {
    "Medieval": {
        "Base": {"minimo": 10, "maximo": 100, "multiplicador": 1},
        "Proeficiencia I": {"minimo": 12, "maximo": 110, "multiplicador": 1.1},
        "Proeficiencia II": {"minimo": 18, "maximo": 115, "multiplicador": 1.2},
        "Proeficiencia III": {"minimo": 25, "maximo": 120, "multiplicador": 1.3},
        "Proeficiencia IV": {"minimo": 37, "maximo": 135, "multiplicador": 1.4},
        "Proeficiencia V": {"minimo": 42, "maximo": 140, "multiplicador": 1.5},
        "Proeficiencia VI": {"minimo": 50, "maximo": 180, "multiplicador": 1.6}
    },
    "Medieval Pesado": {
        "Base": {"minimo": 20, "maximo": 150, "multiplicador": 1},
        "Proeficiencia I": {"minimo": 25, "maximo": 160, "multiplicador": 1.1},
        "Proeficiencia II": {"minimo": 28, "maximo": 170, "multiplicador": 1.2},
        "Proeficiencia III": {"minimo": 30, "maximo": 190, "multiplicador": 1.3},
        "Proeficiencia IV": {"minimo": 35, "maximo": 200, "multiplicador": 1.4},
        "Proeficiencia V": {"minimo": 45, "maximo": 210, "multiplicador": 1.5},
        "Proeficiencia VI": {"minimo": 50, "maximo": 225, "multiplicador": 1.6}
    },
    "Infantaria": {
        "Base": {"minimo": 10, "maximo": 100, "multiplicador": 1},
        "Proeficiencia I": {"minimo": 12, "maximo": 110, "multiplicador": 1.1},
        "Proeficiencia II": {"minimo": 18, "maximo": 115, "multiplicador": 1.2},
        "Proeficiencia III": {"minimo": 25, "maximo": 120, "multiplicador": 1.3},
        "Proeficiencia IV": {"minimo": 37, "maximo": 135, "multiplicador": 1.4},
        "Proeficiencia V": {"minimo": 42, "maximo": 140, "multiplicador": 1.5},
        "Proeficiencia VI": {"minimo": 50, "maximo": 180, "multiplicador": 1.6}
    },
    "Torre":{
        "Base": {"minimo": 0, "maximo": 100, "multiplicador": 1},
        "Torres I": {"minimo": 0, "maximo": 135, "multiplicador": 1},
        "Torres II": {"minimo": 0, "maximo": 175, "multiplicador": 1.15},
        "Torres III": {"minimo": 0, "maximo": 300, "multiplicador": 1.2}
    },
    "Cerco":{
        "Base": {"minimo": 0, "maximo": 250, "multiplicador": 1},
        "Cercos I": {"minimo": 0, "maximo": 250, "multiplicador": 1},
        "Cercos II": {"minimo": 0, "maximo": 400, "multiplicador": 1.15},
        "Cercos III": {"minimo": 0, "maximo": 650, "multiplicador": 1.2}
    },
    "Blindado Leve": {
        "Base": {"minimo": 30, "maximo": 180, "multiplicador": 1},
        "Proeficiencia I": {"minimo": 35, "maximo": 190, "multiplicador": 1.1},
        "Proeficiencia II": {"minimo": 40, "maximo": 200, "multiplicador": 1.2},
        "Proeficiencia III": {"minimo": 50, "maximo": 220, "multiplicador": 1.3},
        "Proeficiencia IV": {"minimo": 60, "maximo": 240, "multiplicador": 1.4},
        "Proeficiencia V": {"minimo": 70, "maximo": 260, "multiplicador": 1.5},
        "Proeficiencia VI": {"minimo": 80, "maximo": 280, "multiplicador": 1.6}
    },
    "Blindado Pesado": {
        "Base": {"minimo": 40, "maximo": 200, "multiplicador": 1},
        "Proeficiencia I": {"minimo": 50, "maximo": 220, "multiplicador": 1.1},
        "Proeficiencia II": {"minimo": 60, "maximo": 240, "multiplicador": 1.2},
        "Proeficiencia III": {"minimo": 70, "maximo": 260, "multiplicador": 1.3},
        "Proeficiencia IV": {"minimo": 80, "maximo": 280, "multiplicador": 1.4},
        "Proeficiencia V": {"minimo": 90, "maximo": 300, "multiplicador": 1.5},
        "Proeficiencia VI": {"minimo": 100, "maximo": 320, "multiplicador": 1.6}
    },   
    "Fragata": {
        "Base": {"minimo": 25, "maximo": 170, "multiplicador": 1},
        "Proeficiencia I": {"minimo": 30, "maximo": 185, "multiplicador": 1.1},
        "Proeficiencia II": {"minimo": 35, "maximo": 200, "multiplicador": 1.2},
        "Proeficiencia III": {"minimo": 45, "maximo": 220, "multiplicador": 1.3},
        "Proeficiencia IV": {"minimo": 55, "maximo": 240, "multiplicador": 1.4},
        "Proeficiencia V": {"minimo": 65, "maximo": 260, "multiplicador": 1.5},
        "Proeficiencia VI": {"minimo": 75, "maximo": 280, "multiplicador": 1.6}
    },   
    "Artilharia": {
        "Base": {"minimo": 35, "maximo": 190, "multiplicador": 1},
        "Proeficiencia I": {"minimo": 40, "maximo": 210, "multiplicador": 1.1},
        "Proeficiencia II": {"minimo": 45, "maximo": 230, "multiplicador": 1.2},
        "Proeficiencia III": {"minimo": 55, "maximo": 250, "multiplicador": 1.3},
        "Proeficiencia IV": {"minimo": 65, "maximo": 270, "multiplicador": 1.4},
        "Proeficiencia V": {"minimo": 75, "maximo": 290, "multiplicador": 1.5},
        "Proeficiencia VI": {"minimo": 85, "maximo": 310, "multiplicador": 1.6}
    },   
    "Couraçado": {
        "Base": {"minimo": 50, "maximo": 210, "multiplicador": 1},
        "Proeficiencia I": {"minimo": 60, "maximo": 230, "multiplicador": 1.1},
        "Proeficiencia II": {"minimo": 70, "maximo": 250, "multiplicador": 1.2},
        "Proeficiencia III": {"minimo": 80, "maximo": 270, "multiplicador": 1.3},
        "Proeficiencia IV": {"minimo": 90, "maximo": 290, "multiplicador": 1.4},
        "Proeficiencia V": {"minimo": 100, "maximo": 310, "multiplicador": 1.5},
        "Proeficiencia VI": {"minimo": 110, "maximo": 330, "multiplicador": 1.6}
    },
}


# Tabela de tecnologias de defesa
TABELA_DEFESA = {
    "Defesa I": {"minimo": 5, "maximo": 60, "multiplicador": 1.05},
    "Defesa II": {"minimo": 10, "maximo": 75, "multiplicador": 1.08},
    "Defesa III": {"minimo": 20, "maximo": 90, "multiplicador": 1.1},
    "Defesa IV": {"minimo": 30, "maximo": 105, "multiplicador": 1.2},
    "Defesa V": {"minimo": 40, "maximo": 125, "multiplicador": 1.25}, 
    "Defesa VI": {"minimo": 50, "maximo": 150, "multiplicador": 1.3}
}




# Tabela de redução de dano com base na diferença
TABELA_DANO = {
    0.25: 0.01, 0.24: 0.02, 0.23: 0.03, 0.22: 0.04, 0.21: 0.05,
    0.20: 0.06, 0.19: 0.07, 0.18: 0.08, 0.17: 0.09, 0.16: 0.10, 
    0.15: 0.15, 0.14: 0.20, 0.13: 0.25, 0.12: 0.30, 0.11: 0.35,
    0.10: 0.40, 0.09: 0.42, 0.08: 0.44, 0.07: 0.46, 0.06: 0.48, 
    0.05: 0.55, 0.04: 0.56, 0.03: 0.57, 0.02: 0.58, 0.01: 0.59
}


# ------------------------------
# 🔹 FUNÇÃO PARA CALCULAR DEFESA
# ------------------------------

def calcular_defesa(tecnologias, tipo_tropa):
    """Calcula a defesa de uma tropa considerando apenas tecnologias de defesa."""

    # 🔹 Filtrar apenas tecnologias de defesa disponíveis
    tecnologias_defesa = [t for t in tecnologias if t in TABELA_DEFESA]

    # 🔹 Verifica a melhor tecnologia de defesa disponível
    melhor_tecnologia = max(tecnologias_defesa, key=lambda t: TABELA_DEFESA[t]["maximo"], default=None)

    if melhor_tecnologia:
        valores_defesa = TABELA_DEFESA[melhor_tecnologia]
        min_defesa, max_defesa = valores_defesa["minimo"], valores_defesa["maximo"]
        multiplicador_tecnologia = valores_defesa["multiplicador"]
    else:
        min_defesa, max_defesa = 0, 50  # Se não houver tecnologia, usa um valor padrão
        multiplicador_tecnologia = 1

    # 🔹 Gerar defesa aleatória e aplicar multiplicador da tecnologia
    defesa_final = random.randint(min_defesa, max_defesa) * multiplicador_tecnologia

    print(f"🛡️ Defesa de {tipo_tropa}: {defesa_final:.2f}")
    return defesa_final


# ------------------------------
# 🔹 FUNÇÃO PARA CALCULAR ATAQUE
# ------------------------------


def calcular_ataque(tecnologias, tipo_tropa, lado=""):
    """Calcula o poder de ataque de uma tropa com base no tipo e proficiência/tecnologia."""

    # Se for uma Torre, definir o nível com base na tecnologia em vez da proeficiência
    if tipo_tropa == "Torre":
        niveis_torres = ["Torres III", "Torres II", "Torres I"]  # Ordem da mais avançada para a básica
        nivel_atual = next((nivel for nivel in niveis_torres if nivel in tecnologias), "Base")
    
    elif tipo_tropa == "Cerco":
        niveis_cercos = ["Cercos III", "Cercos II", "Cercos I"]  # Ordem da mais avançada para a básica
        nivel_atual = next((nivel for nivel in niveis_cercos if nivel in tecnologias), "Base")

    else:
        # Obter o nível de proeficiência mais alto para tropas comuns
        niveis_proeficiencia = ["Proeficiencia VI", "Proeficiencia V", "Proeficiencia IV", 
                                 "Proeficiencia III", "Proeficiencia II", "Proeficiencia I"]
        
        nivel_atual = "Base"  # Padrão caso não tenha proeficiência
        for nivel in niveis_proeficiencia:
            if nivel in tecnologias:
                nivel_atual = nivel
                break

    # Buscar os valores da tabela unificada
    valores = TABELA_ATAQUE_PROEFICIENCIA.get(tipo_tropa, {}).get(nivel_atual, {"minimo": 10, "maximo": 100, "multiplicador": 1})

    min_ataque = valores["minimo"]
    max_ataque = valores["maximo"]
    multiplicador = valores["multiplicador"]

    # Gerar ataque aleatório baseado na proficiência/tecnologia
    ataque_base = random.randint(min_ataque, max_ataque) * multiplicador

    # Exibir informações do ataque
    if lado:
        print(f"⚔️ Ataque de {tipo_tropa} ({lado}) [{nivel_atual}]: {ataque_base:.2f}")
    else:
        print(f"⚔️ Ataque de {tipo_tropa} [{nivel_atual}]: {ataque_base:.2f}")

    return ataque_base




# ------------------------------
# 🔹 FUNÇÃO PARA CALCULAR DANO
# ------------------------------

def calcular_dano(ataque, defesa):
    """Calcula o dano sofrido com base na diferença entre ataque e defesa."""
    diferenca = ataque - defesa
    percentual = abs(diferenca) / ataque  # Percentual de diferença

    print(f"⚔️ Diferença entre ataque e defesa: {diferenca:.2f} ({percentual*100:.2f}%)")

    if diferenca > 0:
        # Se o ataque for maior que a defesa, dano total
        return diferenca  

    # Se a defesa for maior que 25% do ataque, ignora o dano completamente
    if percentual > 0.25:
        print(f"🛡️ Defesa foi muito maior ({percentual*100:.2f}%)! Nenhum dano recebido.")
        return 0

    # Aplicar redução de dano de acordo com a TABELA_DANO
    dano_reduzido = 1  # Começa com pelo menos 1 de dano mínimo
    for limite, multiplicador in sorted(TABELA_DANO.items(), reverse=True):
        if percentual >= limite:
            dano_reduzido = abs(diferenca) * multiplicador
            break  # Aplica o primeiro multiplicador correspondente

    dano_final = max(1, dano_reduzido)  # Garantir pelo menos 1 de dano mínimo

    return dano_final





# Estados do HP para cada lado
hp_ativo_esquerdo = False
hp_ativo_direito = False


# ------------------------------
# 📌 TABELAS DE HP DINÂMICO
# ------------------------------

# 🔹 HP base para cada tropa
TABELA_HP_BASE = {
    "Medieval": 100,
    "Medieval Pesado": 150,
    "Infantaria": 120,
    "Blindado Leve": 200,
    "Blindado Pesado": 300,
    "Fragata": 250,
    "Couraçado": 400,
    "Artilharia": 180
}

# 🔹 Tabela de multiplicadores de HP baseados no nível de Defesa
TABELA_DEFESA_HP = {
    "Base": 1.0,
    "Defesa I": 1.1,
    "Defesa II": 1.2,
    "Defesa III": 1.3,
    "Defesa IV": 1.4,
    "Defesa V": 1.5,
    "Defesa VI": 1.65
}

# 🔹 HP base para a Torre dependendo do nível da tecnologia
TABELA_HP_TORRE = {
    "Base": 1000,
    "Torres I": 1000,
    "Torres II": 2500,
    "Torres III": 5000
}

# 🔹 HP base para as unidades de Cerco dependendo do nível da tecnologia
TABELA_HP_CERCO = {
    "Base": 250,
    "Cercos I": 250,
    "Cercos II": 350,
    "Cercos III": 450
}

# ------------------------------
# 📌 FUNÇÃO PARA CALCULAR O HP DINÂMICO
# ------------------------------

def calcular_hp(tecnologias, tipo_tropa):
    """Calcula o HP da tropa com base no nível de Defesa, Torre ou Cerco."""

    # 🔹 Se for uma Torre, calcular HP baseado no nível da Torre
    if tipo_tropa == "Torre":
        niveis_torres = ["Torres III", "Torres II", "Torres I"]  # Ordem da mais avançada para a básica
        nivel_torre = next((nivel for nivel in niveis_torres if nivel in tecnologias), "Base")
        return TABELA_HP_TORRE[nivel_torre]

    # 🔹 Se for um Cerco, calcular HP baseado no nível da tecnologia de Cerco
    if tipo_tropa == "Cerco":
        niveis_cercos = ["Cercos III", "Cercos II", "Cercos I"]  # Ordem da mais avançada para a básica
        nivel_cerco = next((nivel for nivel in niveis_cercos if nivel in tecnologias), "Base")
        return TABELA_HP_CERCO[nivel_cerco]

    # 🔹 Para outras tropas, calcular HP baseado no nível de Defesa
    nivel_defesa = next((nivel for nivel in reversed(TABELA_DEFESA_HP.keys()) if nivel in tecnologias), "Base")
    
    hp_base = TABELA_HP_BASE.get(tipo_tropa, 100)  # Caso não tenha na tabela, usa um valor padrão
    multiplicador_defesa = TABELA_DEFESA_HP[nivel_defesa]

    hp_final = int(hp_base * multiplicador_defesa)
    
    return hp_final


hp_esquerdo = 100  # Valor inicial, atualizado depois conforme a tropa escolhida
hp_direito = 100

import threading

# Função otimizada para simular a barra de progresso do ataque
def simular_barra_progresso_ataque(valor_atual):
    """Simula a barra de progresso do ataque de forma otimizada, evitando travamentos."""
    
    # Resetar os textos das labels antes do ataque
    label_acao_texto_esquerdo.configure(text="Nenhuma", font=("Arial", 12), text_color="white")
    label_acao_texto_direito.configure(text="Nenhuma", font=("Arial", 12), text_color="white")

    if valor_atual <= 100:
        barra_progresso_movimento.set(valor_atual / 100.0)  # Atualiza a barra de progresso
        frame_barra_progresso_movimento.after(5, simular_barra_progresso_ataque, valor_atual + 2)  # Acelera o carregamento
    else:
        # Após o carregamento, processa o ataque em uma thread separada para evitar travamento da UI
        threading.Thread(target=processar_ataque, daemon=True).start()

        # Restaurar interface após o ataque
        frame_barra_progresso_movimento.grid_remove()
        botao_movimento.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        botao_atacar.grid(row=0, column=1, padx=10, pady=10, sticky="ew")


def processar_ataque():
    """Executa a lógica do ataque após o carregamento da barra, impedindo ataques de unidades mortas."""
    global hp_esquerdo, hp_direito

    reino_esquerdo = seletor_reino_esquerdo.get()
    reino_direito = seletor_reino_direito.get()
    os.system('cls' if os.name == 'nt' else 'clear')

    dados = carregar_dados_json()
    tecnologias_esquerdo = dados["reinos"].get(reino_esquerdo, {}).get("tecnologias", [])
    tecnologias_direito = dados["reinos"].get(reino_direito, {}).get("tecnologias", [])
    tipo_tropa_esquerdo = seletor_tropas_esquerdo.get()
    tipo_tropa_direito = seletor_tropas_direito.get()

    # 🔹 Verifica se alguma unidade está morta ANTES de calcular ataque
    if hp_esquerdo == 0:
        print(f"⚠️ {tipo_tropa_esquerdo} (esquerdo) está morto e não pode atacar!")
        return  # Cancela o ataque se a tropa estiver morta
    
    if hp_direito == 0:
        print(f"⚠️ {tipo_tropa_direito} (direito) está morto e não pode atacar!")
        return  # Cancela o ataque se a tropa estiver morta

    # Cálculo dos poderes de ataque
    poder_ataque_esquerdo = calcular_ataque(tecnologias_esquerdo, tipo_tropa_esquerdo)
    poder_ataque_direito = calcular_ataque(tecnologias_direito, tipo_tropa_direito)

    # Determinar atacante e vítima
    if poder_ataque_esquerdo > poder_ataque_direito:
        atacante, vitima = "esquerdo", "direito"
        tecnologias_vitima, tipo_tropa_vitima = tecnologias_direito, tipo_tropa_direito
        poder_ataque_atacante, poder_ataque_vitima = poder_ataque_esquerdo, poder_ataque_direito
        label_acao_texto_atacante, label_acao_texto_vitima = label_acao_texto_esquerdo, label_acao_texto_direito
        hp_vitima = hp_direito
        
    else:
        atacante, vitima = "direito", "esquerdo"
        tecnologias_vitima, tipo_tropa_vitima = tecnologias_esquerdo, tipo_tropa_esquerdo
        poder_ataque_atacante, poder_ataque_vitima = poder_ataque_direito, poder_ataque_esquerdo
        label_acao_texto_atacante, label_acao_texto_vitima = label_acao_texto_direito, label_acao_texto_esquerdo
        hp_vitima = hp_esquerdo

    # 🔹 Verifica se a vítima já está morta antes do ataque
    if hp_vitima == 0:
        print(f"⚠️ {tipo_tropa_vitima} ({vitima}) já está morto. Resetando unidade antes do ataque.")
        resetar_unidade(vitima)  # Reseta automaticamente antes do ataque
        
        # Atualiza o HP da vítima após o reset
        if vitima == "esquerdo":
            hp_vitima = hp_esquerdo
        else:
            hp_vitima = hp_direito

    # Cálculo de defesa
    valor_defesa = calcular_defesa(tecnologias_vitima, tipo_tropa_vitima)

    print(f"\n⚔️ {tipo_tropa_vitima} ({vitima}) está sendo atacado!")
    print(f"🔹 Poder de Ataque: {poder_ataque_atacante:.2f}")
    print(f"🛡️ Defesa Calculada: {valor_defesa:.2f}")

    # Lógica de dano e defesa
    diferenca = poder_ataque_atacante - valor_defesa
    percentual_diferenca = abs(diferenca) / poder_ataque_atacante  # Percentual de diferença

    if valor_defesa > poder_ataque_atacante:
        if percentual_diferenca <= 0.25:
            # Defesa parcial → Dano reduzido
            dano = calcular_dano(poder_ataque_atacante, valor_defesa)
            print(f"💔 Defesa parcial! Dano reduzido aplicado: {dano:.2f}")
            label_acao_texto_vitima.configure(text="DEFENDIDO", font=("Arial", 16, "bold"), text_color="#1E90FF")
        else:
            # Defesa total → Sem dano
            print(f"🛡️ Defesa total! Nenhum dano recebido.")
            dano = 0
            label_acao_texto_vitima.configure(text="BLOQUEADO", font=("Arial", 16, "bold"), text_color="#00CFFF")
    else:
        # Ataque bem-sucedido → Dano normal
        dano = calcular_dano(poder_ataque_atacante, valor_defesa)
        print(f"🔥 Ataque bem-sucedido! {tipo_tropa_vitima} recebeu dano.")
        print(f"💥 Dano causado: {dano:.2f} ({poder_ataque_atacante:.2f} - {valor_defesa:.2f})")
        label_acao_texto_vitima.configure(text="Nenhuma", font=("Arial", 12), text_color="white")

    # Aplicação do dano
    if dano > 0:
        reduzir_hp(vitima, dano)

    # Atualiza interface do jogo
    label_acao_texto_atacante.configure(text="ATACAR", font=("Arial", 16, "bold"), text_color="#FF4500")



def alternar_hp(lado):
    global hp_esquerdo, hp_direito, hp_ativo_esquerdo, hp_ativo_direito

    if lado == "esquerdo":
        hp_ativo_esquerdo = not hp_ativo_esquerdo

        # Ocultar todos os elementos antes de reorganizar
        label_morto_esquerdo.pack_forget()
        barra_hp_esquerdo.pack_forget()


        if hp_ativo_esquerdo:
            # Resetar HP e reaparecer na ordem correta
            hp_esquerdo = 100
            barra_hp_esquerdo.set(1)

            # Exibir na ordem correta
            barra_hp_esquerdo.pack(pady=5)

        else:
            # Exibir "MORTO" antes de qualquer outra coisa
            label_morto_esquerdo.pack(pady=5)


    elif lado == "direito":
        hp_ativo_direito = not hp_ativo_direito

        # Ocultar todos os elementos antes de reorganizar
        label_morto_direito.pack_forget()
        barra_hp_direito.pack_forget()


        if hp_ativo_direito:
            # Resetar HP e reaparecer na ordem correta
            hp_direito = 100
            barra_hp_direito.set(1)

            # Exibir na ordem correta
            barra_hp_direito.pack(pady=5)

        else:
            # Exibir "MORTO" antes de qualquer outra coisa
            label_morto_direito.pack(pady=5)



def atualizar_texto_hp(lado):
    """Atualiza o texto dentro da barra de HP conforme o valor atual."""
    dados = carregar_dados_json()

    if lado == "esquerdo":
        reino = seletor_reino_esquerdo.get()
        tecnologias = dados["reinos"].get(reino, {}).get("tecnologias", [])
        total_hp = calcular_hp(tecnologias, seletor_tropas_esquerdo.get())
        label_hp_esquerdo.configure(text=f"{int(hp_esquerdo)}/{int(total_hp)}")  # Remove casas decimais
    elif lado == "direito":
        reino = seletor_reino_direito.get()
        tecnologias = dados["reinos"].get(reino, {}).get("tecnologias", [])
        total_hp = calcular_hp(tecnologias, seletor_tropas_direito.get())
        label_hp_direito.configure(text=f"{int(hp_direito)}/{int(total_hp)}")  # Remove casas decimais


def chacoalhar_imagem(label):
    """Aplica um efeito de chacoalhada apenas na imagem dentro do label."""
    deslocamentos = [-2, 2, -2, 2, -1, 1, 0]  # Pequenos deslocamentos para frente e trás

    def animar(indice=0):
        if indice < len(deslocamentos):
            label.place_configure(relx=0.5, rely=0.5, anchor="center", x=deslocamentos[indice])  
            label.after(50, animar, indice + 1)  # Próxima iteração após 50ms

    animar()  # Inicia a animação


def reduzir_hp(lado, dano):
    global hp_esquerdo, hp_direito

    # Determinar tropa e reino correspondente
    if lado == "esquerdo":
        reino = seletor_reino_esquerdo.get()
        tipo_tropa = seletor_tropas_esquerdo.get()
        dados = carregar_dados_json()
        tecnologias = dados["reinos"].get(reino, {}).get("tecnologias", [])
        total_hp = calcular_hp(tecnologias, tipo_tropa)
        hp_atual = hp_esquerdo
        hp_label = label_hp_esquerdo
        barra_hp = barra_hp_esquerdo
        frame_imagem = frame_imagem_tropas_esquerdo
        label_morto = label_morto_esquerdo
    else:
        reino = seletor_reino_direito.get()
        tipo_tropa = seletor_tropas_direito.get()
        dados = carregar_dados_json()
        tecnologias = dados["reinos"].get(reino, {}).get("tecnologias", [])
        total_hp = calcular_hp(tecnologias, tipo_tropa)
        hp_atual = hp_direito
        hp_label = label_hp_direito
        barra_hp = barra_hp_direito
        frame_imagem = frame_imagem_tropas_direito
        label_morto = label_morto_direito

    # Verificar se a tecnologia "Bandagem" está ativa
    if dano >= hp_atual and "Bandagem" in tecnologias and random.random() < 0.15:
        hp_final = random.randint(1, 10)  # Sobrevive com 1 a 10 de HP
        print(f"🩸 Bandagem ativada! {tipo_tropa} sobreviveu com {hp_final} HP!")
    else:
        # Aplicar dano normalmente
        hp_final = max(0, hp_atual - dano)

    # Atualizar estado do HP
    if lado == "esquerdo":
        hp_esquerdo = hp_final
    else:
        hp_direito = hp_final

    # Atualizar a barra de HP e o texto correspondente
    barra_hp.set(hp_final / total_hp)
    hp_label.configure(text=f"{int(hp_final)}/{int(total_hp)}")

    # 💥 Chacoalhar a imagem ao receber dano
    for widget in frame_imagem.winfo_children():
        if isinstance(widget, ctk.CTkLabel):
            chacoalhar_imagem(widget)

    # Se a tropa morrer, remover a barra e exibir "MORTO"
    if hp_final == 0:
        barra_hp.pack_forget()
        hp_label.pack_forget()
        label_morto.pack(pady=5)


# Modificando a função resetar_unidade() para restaurar o HP na barra e no texto
def resetar_unidade(lado):
    """Reseta a unidade do lado especificado, restaurando HP, ação e elementos visuais."""
    global hp_esquerdo, hp_direito

    print(f"🔄 Resetando unidade do lado {lado}...")

    if lado == "esquerdo":
        # Esconder elementos relacionados à morte
        label_morto_esquerdo.pack_forget()
        barra_hp_esquerdo.pack_forget()
        label_hp_esquerdo.pack_forget()

        # Restaurar HP da tropa correspondente
        reino = seletor_reino_esquerdo.get()
        tipo_tropa = seletor_tropas_esquerdo.get()
        dados = carregar_dados_json()
        tecnologias = dados["reinos"].get(reino, {}).get("tecnologias", [])
        hp_esquerdo = calcular_hp(tecnologias, tipo_tropa)
        
        barra_hp_esquerdo.set(1)  # Restaurar a barra visualmente

        # Atualizar texto de HP
        atualizar_texto_hp("esquerdo")

        # Mostrar novamente a barra de HP e o texto
        barra_hp_esquerdo.pack(pady=5)
        label_hp_esquerdo.pack(pady=5)

        # 🔹 Resetar a ação da unidade (exibe "Nenhuma" para indicar que está pronta para nova ação)
        label_acao_texto_esquerdo.configure(text="Nenhuma", font=("Arial", 12), text_color="white")

    elif lado == "direito":
        # Esconder elementos relacionados à morte
        label_morto_direito.pack_forget()
        barra_hp_direito.pack_forget()
        label_hp_direito.pack_forget()

        # Restaurar HP da tropa correspondente
        reino = seletor_reino_direito.get()
        tipo_tropa = seletor_tropas_direito.get()
        dados = carregar_dados_json()
        tecnologias = dados["reinos"].get(reino, {}).get("tecnologias", [])
        hp_direito = calcular_hp(tecnologias, tipo_tropa)
        
        barra_hp_direito.set(1)  # Restaurar a barra visualmente

        # Atualizar texto de HP
        atualizar_texto_hp("direito")

        # Mostrar novamente a barra de HP e o texto
        barra_hp_direito.pack(pady=5)
        label_hp_direito.pack(pady=5)

        # 🔹 Resetar a ação da unidade (exibe "Nenhuma" para indicar que está pronta para nova ação)
        label_acao_texto_direito.configure(text="Nenhuma", font=("Arial", 12), text_color="white")

    print(f"✅ Unidade do lado {lado} foi resetada com sucesso!")



###############
# FIM ATAQUE  #
###############

# Criação da aba Combate
tab_combate = tabview_principal.add("Combate")

tipo_de_tropas = ["Medieval", "Medieval Pesado", "Infantaria", "Torre", "Cerco", "Blindado Leve", "Blindado Pesado", "Fragata", "Couraçado", "Artilharia"]
reinos_disponiveis = list(dados["reinos"].keys())

# Frame principal que conterá os dois frames lado a lado e o rodapé
frame_combate = ctk.CTkFrame(tab_combate, width=760, height=600)
frame_combate.grid(pady=10, padx=10, sticky="nsew")  # Usando grid para o frame principal

# Configurando o grid layout para frame_combate
frame_combate.columnconfigure(0, weight=1)
frame_combate.columnconfigure(1, weight=1)
frame_combate.rowconfigure(0, weight=1)
frame_combate.rowconfigure(1, weight=0)
tab_combate.grid_rowconfigure(0, weight=1)
tab_combate.grid_columnconfigure(0, weight=1)

# Primeiro frame (lado esquerdo)
frame_esquerdo = ctk.CTkFrame(frame_combate, width=370, height=500, fg_color="#1f1f1f", corner_radius=8)
frame_esquerdo.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")  # Posicionando com grid

# Frame para os textos (esquerda)
frame_textos_esquerdo = ctk.CTkFrame(frame_esquerdo, fg_color="#1f1f1f", corner_radius=0)
frame_textos_esquerdo.pack(pady=(5, 0), padx=5, fill="x")

label_reinos_esquerdo = ctk.CTkLabel(frame_textos_esquerdo, text="Reinos", font=("Arial", 14, "bold"))
label_reinos_esquerdo.pack(side="left", padx=5, pady=5)

label_tipos_esquerdo = ctk.CTkLabel(frame_textos_esquerdo, text="Tipo de Tropa", font=("Arial", 14, "bold"))
label_tipos_esquerdo.pack(side="right", padx=5, pady=5)

# Frame interno para alinhar os seletores lado a lado (esquerda) sem borda visível
frame_seletores_esquerdo = ctk.CTkFrame(frame_esquerdo, fg_color="transparent", corner_radius=0)
frame_seletores_esquerdo.pack(pady=(0, 5), padx=5, fill="x")

seletor_reino_esquerdo = ctk.CTkOptionMenu(frame_seletores_esquerdo, values=reinos_disponiveis, command=on_select_reino_esquerdo)
seletor_reino_esquerdo.pack(side="left", padx=5, pady=5)

seletor_tropas_esquerdo = ctk.CTkOptionMenu(frame_seletores_esquerdo, values=tipo_de_tropas, command=on_select_tropa_esquerdo)
seletor_tropas_esquerdo.set(tipo_de_tropas[0])
seletor_tropas_esquerdo.pack(side="right", padx=5, pady=5)

# Frame para a imagem das tropas (esquerda)
frame_imagem_tropas_esquerdo = ctk.CTkFrame(frame_esquerdo, height=250, fg_color="#2b2b2b", corner_radius=8)
frame_imagem_tropas_esquerdo.pack_propagate(False)
frame_imagem_tropas_esquerdo.pack(pady=(5, 5), padx=10, fill="x")

# Supondo que 'reino_selecionado' é o primeiro reino na lista disponível
reino_selecionado = reinos_disponiveis[0] if reinos_disponiveis else None
dados = carregar_dados_json()  # Carrega os dados necessários
atualizar_imagem_tropas(frame_imagem_tropas_esquerdo, tipo_de_tropas[0], dados["reinos"].get(reino_selecionado, {}), inverter=True)


# Frame para a tabela de habilidades (esquerda)
frame_habilidades_esquerdo = ctk.CTkFrame(frame_esquerdo, width=320, height=150, fg_color="#2b2b2b", corner_radius=8)
frame_habilidades_esquerdo.pack_propagate(False)
frame_habilidades_esquerdo.pack(pady=(5, 0), padx=10, fill="x")

# Criar a tabela de habilidades com uma única coluna
tabela_habilidades_esquerdo = ttk.Treeview(frame_habilidades_esquerdo, columns=("Habilidade"), show="headings", height=5, style="Custom.Treeview")
tabela_habilidades_esquerdo.heading("Habilidade", text="Habilidades", anchor="center")
tabela_habilidades_esquerdo.column("Habilidade", width=300, anchor="center")

configurar_estilo_tabela(tabela_habilidades_esquerdo)
tabela_habilidades_esquerdo.pack(fill="both", expand=True)

# Frame para ação da unidade (esquerda)
frame_acao_unidade_esquerdo = ctk.CTkFrame(frame_esquerdo, width=320, height=150, fg_color="#2b2b2b", corner_radius=8)
frame_acao_unidade_esquerdo.pack_propagate(False)
frame_acao_unidade_esquerdo.pack(pady=(0, 10), padx=10, fill="x")

label_acao_unidade_esquerdo = ctk.CTkLabel(frame_acao_unidade_esquerdo, text="Ação da Unidade", font=("Arial", 14, "bold"))
label_acao_unidade_esquerdo.pack(pady=(10, 5), padx=5)

label_acao_texto_esquerdo = ctk.CTkLabel(frame_acao_unidade_esquerdo, text="Nenhuma", font=("Arial", 12))
label_acao_texto_esquerdo.pack(pady=(0, 10), padx=5)

# Segundo frame (lado direito)
frame_direito = ctk.CTkFrame(frame_combate, width=370, height=500, fg_color="#1f1f1f", corner_radius=8)
frame_direito.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")  # Posicionando com grid

# Frame para os textos (direita)
frame_textos_direito = ctk.CTkFrame(frame_direito, fg_color="#1f1f1f", corner_radius=0)
frame_textos_direito.pack(pady=(5, 0), padx=5, fill="x")

label_reinos_direito = ctk.CTkLabel(frame_textos_direito, text="Reinos", font=("Arial", 14, "bold"))
label_reinos_direito.pack(side="left", padx=5, pady=5)

label_tipos_direito = ctk.CTkLabel(frame_textos_direito, text="Tipo de Tropa", font=("Arial", 14, "bold"))
label_tipos_direito.pack(side="right", padx=5, pady=5)

# Frame interno para alinhar os seletores lado a lado (direita)
frame_seletores_direito = ctk.CTkFrame(frame_direito, fg_color="transparent", corner_radius=0)
frame_seletores_direito.pack(pady=(0, 5), padx=5, fill="x")

seletor_reino_direito = ctk.CTkOptionMenu(frame_seletores_direito, values=reinos_disponiveis, command=on_select_reino_direito)
seletor_reino_direito.pack(side="left", padx=5, pady=5)

seletor_tropas_direito = ctk.CTkOptionMenu(frame_seletores_direito, values=tipo_de_tropas, command=on_select_tropa_direito)
seletor_tropas_direito.set(tipo_de_tropas[0])
seletor_tropas_direito.pack(side="right", padx=5, pady=5)

# Frame para a imagem das tropas (direita)
frame_imagem_tropas_direito = ctk.CTkFrame(frame_direito, height=250, fg_color="#2b2b2b", corner_radius=8)
frame_imagem_tropas_direito.pack_propagate(False)
frame_imagem_tropas_direito.pack(pady=(5, 5), padx=10, fill="x")

reino_selecionado = reinos_disponiveis[0] if reinos_disponiveis else None
dados = carregar_dados_json()  # Carrega os dados necessários
atualizar_imagem_tropas(frame_imagem_tropas_direito, tipo_de_tropas[0], dados["reinos"].get(reino_selecionado, {}), inverter=False)



# Frame para a tabela de habilidades (direita)
frame_habilidades_direito = ctk.CTkFrame(frame_direito, width=320, height=150, fg_color="#2b2b2b", corner_radius=8)
frame_habilidades_direito.pack_propagate(False)
frame_habilidades_direito.pack(pady=(5, 0), padx=10, fill="x")

tabela_habilidades_direito = ttk.Treeview(frame_habilidades_direito, columns=("Habilidade"), show="headings", height=5, style="Custom.Treeview")
tabela_habilidades_direito.heading("Habilidade", text="Habilidades", anchor="center")
tabela_habilidades_direito.column("Habilidade", width=300, anchor="center")

configurar_estilo_tabela(tabela_habilidades_direito)
tabela_habilidades_direito.pack(fill="both", expand=True)

# Frame para ação da unidade (direita)
frame_acao_unidade_direito = ctk.CTkFrame(frame_direito, width=320, height=150, fg_color="#2b2b2b", corner_radius=8)
frame_acao_unidade_direito.pack_propagate(False)
frame_acao_unidade_direito.pack(pady=(0, 10), padx=10, fill="x")

label_acao_unidade_direito = ctk.CTkLabel(frame_acao_unidade_direito, text="Ação da Unidade", font=("Arial", 14, "bold"))
label_acao_unidade_direito.pack(pady=(10, 5), padx=5)

label_acao_texto_direito = ctk.CTkLabel(frame_acao_unidade_direito, text="Nenhuma", font=("Arial", 12))
label_acao_texto_direito.pack(pady=(0, 10), padx=5)


# Criação de um sub-frame para os botões e a barra de progresso
frame_botoes_e_barra = ctk.CTkFrame(frame_combate, fg_color="#2b2b2b", corner_radius=8)
frame_botoes_e_barra.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")  # Posicionando com grid

frame_botoes_e_barra.columnconfigure(0, weight=1)
frame_botoes_e_barra.columnconfigure(1, weight=1)

# Botão de Movimento
botao_movimento = ctk.CTkButton(
    frame_botoes_e_barra, 
    text="Movimento", 
    fg_color="#00008B", 
    hover_color="#000066", 
    font=("Arial", 14, "bold"),
    command=executar_movimento
)
botao_movimento.grid(row=0, column=0, padx=10, pady=10, sticky="ew")  # Posicionando com grid

# Botão de Atacar
botao_atacar = ctk.CTkButton(
    frame_botoes_e_barra, 
    text="Atacar", 
    fg_color="#FF0000", 
    hover_color="#CC0000", 
    font=("Arial", 14, "bold"),
    command=executar_ataque
)
botao_atacar.grid(row=0, column=1, padx=10, pady=10, sticky="ew")  # Posicionando com grid

# Barra de progresso para simulação de carregamento (movimento)
frame_barra_progresso_movimento = ctk.CTkFrame(frame_botoes_e_barra, fg_color="transparent")
frame_barra_progresso_movimento.grid(row=1, column=0, columnspan=2, pady=(10, 5), padx=10, sticky="ew")
frame_barra_progresso_movimento.grid_remove()  # Inicialmente oculto

barra_progresso_movimento = ctk.CTkProgressBar(frame_barra_progresso_movimento, orientation="horizontal", width=200, height=20)
barra_progresso_movimento.pack(fill="both", expand=True)


# Inicializando as tabelas de habilidades com base no primeiro reino
if reinos_disponiveis:
    on_select_reino_esquerdo(reinos_disponiveis[0])
    on_select_reino_direito(reinos_disponiveis[0])



# Barra de HP
barra_hp_esquerdo = ctk.CTkProgressBar(frame_acao_unidade_esquerdo, orientation="horizontal", width=300, height=15)
barra_hp_direito = ctk.CTkProgressBar(frame_acao_unidade_direito, orientation="horizontal", width=300, height=15)

# Texto de MORTO
label_morto_esquerdo = ctk.CTkLabel(frame_acao_unidade_esquerdo, text="MORTO", font=("Arial", 16, "bold"), text_color="red")
label_morto_direito = ctk.CTkLabel(frame_acao_unidade_direito, text="MORTO", font=("Arial", 16, "bold"), text_color="red")


label_hp_esquerdo = ctk.CTkLabel(frame_acao_unidade_esquerdo, text="100/100", font=("Arial", 12, "bold"))
label_hp_direito = ctk.CTkLabel(frame_acao_unidade_direito, text="100/100", font=("Arial", 12, "bold"))


# Exibir as barras de HP desde o início
# Exibir as barras de HP desde o início e os labels dentro delas
barra_hp_esquerdo.set(hp_esquerdo / 100)
barra_hp_esquerdo.pack(pady=5)
label_hp_esquerdo.pack(pady=5)

barra_hp_direito.set(hp_direito / 100)
barra_hp_direito.pack(pady=5)
label_hp_direito.pack(pady=5)

# Adicionar evento de clique para resetar unidade quando clicar na barra de HP
barra_hp_esquerdo.bind("<Button-1>", lambda event: resetar_unidade("esquerdo"))
barra_hp_direito.bind("<Button-1>", lambda event: resetar_unidade("direito"))

# Adicionar evento de clique para resetar unidade quando clicar no texto "MORTO"
label_morto_esquerdo.bind("<Button-1>", lambda event: resetar_unidade("esquerdo"))
label_morto_direito.bind("<Button-1>", lambda event: resetar_unidade("direito"))


# Criando labels para exibir HP dentro da barra


################################
#                              #
#           OUTROS             #
#                              #
################################


# Adicionando a aba "Outros"
tab_outros = tabview_principal.add("Outros")

################################
#                              #
#   Calculador de Proporções   #
#                              #
################################

# Adicionando o Frame para o calculador de proporções dentro da aba "Outros"
frame_calculador_proporcoes = ctk.CTkFrame(tab_outros, fg_color="#2a2a2a", corner_radius=10)
frame_calculador_proporcoes.pack(pady=10, padx=10, fill="x")  # Reduzindo os paddings externos

# Título do Calculador de Proporções
label_calculador_titulo = ctk.CTkLabel(frame_calculador_proporcoes, text="Calculador de Proporções", font=("Arial", 18, "bold"))
label_calculador_titulo.pack(pady=5)  # Reduzindo o padding interno

# Frame para agrupar Lado A e Lado B
frame_lados = ctk.CTkFrame(frame_calculador_proporcoes, fg_color="transparent")
frame_lados.pack(pady=5, padx=5)

# Frame para Lado A
frame_lado_a = ctk.CTkFrame(frame_lados, fg_color="transparent")
frame_lado_a.pack(side="left", padx=5)

label_lado_a = ctk.CTkLabel(frame_lado_a, text="Lado A:", font=("Arial", 14))
label_lado_a.pack(pady=2)  # Reduzindo o padding interno

lado_a_var = StringVar(value="")
entry_lado_a = ctk.CTkEntry(frame_lado_a, width=150, font=("Arial", 14), justify="center", textvariable=lado_a_var)
entry_lado_a.pack(pady=2)  # Reduzindo o padding interno

# Frame para Lado B
frame_lado_b = ctk.CTkFrame(frame_lados, fg_color="transparent")
frame_lado_b.pack(side="left", padx=5)

label_lado_b = ctk.CTkLabel(frame_lado_b, text="Lado B:", font=("Arial", 14))
label_lado_b.pack(pady=2)  # Reduzindo o padding interno

lado_b_var = StringVar(value="")
entry_lado_b = ctk.CTkEntry(frame_lado_b, width=150, font=("Arial", 14), justify="center", textvariable=lado_b_var)
entry_lado_b.pack(pady=2)  # Reduzindo o padding interno

# Seletor de Opções
opcao_var = StringVar(value="Normal")
seletor_opcao = ctk.CTkOptionMenu(frame_calculador_proporcoes, variable=opcao_var, values=["Normal", "Reduzido", "Muito Reduzido", "Drasticamente Reduzido"], font=("Arial", 14))
seletor_opcao.pack(pady=5)  # Reduzindo o padding interno

# Label para exibir a proporção
label_proporcao = ctk.CTkLabel(frame_calculador_proporcoes, text="A proporção é de: ", font=("Arial", 16, "bold"))
label_proporcao.pack(pady=(10, 20))  # Reduzindo a margem inferior para 20 pixels



# Função para validar entradas (somente inteiros)
def validar_inteiro(valor):
    return valor.isdigit() or valor == ""

# Função para calcular o MDC (Máximo Divisor Comum)
def calcular_mdc(a, b):
    while b:
        a, b = b, a % b
    return a

# Função para calcular a proporção
def calcular_proporcao():
    lado_a = lado_a_var.get()
    lado_b = lado_b_var.get()

    if not lado_a.isdigit() or not lado_b.isdigit() or int(lado_a) == 0 or int(lado_b) == 0:
        exibir_notificacao("Por favor, insira valores válidos para ambos os lados.", "#FF0000")
        return

    lado_a = int(lado_a)
    lado_b = int(lado_b)
    opcao = opcao_var.get()

    # Calcular o MDC para simplificar a proporção
    divisor_comum = calcular_mdc(lado_a, lado_b)
    lado_a //= divisor_comum
    lado_b //= divisor_comum

    # Ajustar a proporção com base na opção selecionada
    if opcao == "Reduzido":
        lado_a = max(1, lado_a // 2)
        lado_b = max(1, lado_b // 2)
    elif opcao == "Muito Reduzido":
        lado_a = max(1, lado_a // 4)
        lado_b = max(1, lado_b // 4)
    elif opcao == "Drasticamente Reduzido":
        lado_a = max(1, lado_a // 8)
        lado_b = max(1, lado_b // 8)

    proporcao_texto = f"A proporção é de: {lado_a}:{lado_b}"

    label_proporcao.configure(text=proporcao_texto)

# Aplicando a validação de entrada
validate_cmd_a = frame_calculador_proporcoes.register(validar_inteiro)
entry_lado_a.configure(validate="key", validatecommand=(validate_cmd_a, "%P"))

validate_cmd_b = frame_calculador_proporcoes.register(validar_inteiro)
entry_lado_b.configure(validate="key", validatecommand=(validate_cmd_b, "%P"))

# Botão para Calcular a Proporção
botao_calcular = ctk.CTkButton(frame_calculador_proporcoes, text="Calcular", font=("Arial", 14), command=calcular_proporcao)
botao_calcular.pack(pady=5)  # Reduzindo o padding interno

################################
#                              #
#  Calculador de Remanescentes #
#                              #
################################

# Adicionando o Frame para o calculador de remanescentes abaixo do calculador de proporções
frame_calculador_remanescentes = ctk.CTkFrame(tab_outros, fg_color="#2a2a2a", corner_radius=10)
frame_calculador_remanescentes.pack(pady=10, padx=10, fill="x")  # Reduzindo os paddings externos

# Título do Calculador de Remanescentes
label_calculador_remanescentes_titulo = ctk.CTkLabel(frame_calculador_remanescentes, text="Calculador de Remanescentes", font=("Arial", 18, "bold"))
label_calculador_remanescentes_titulo.pack(pady=5)  # Reduzindo o padding interno

# Frame para os textos e entradas da regra de três
frame_regra_tres = ctk.CTkFrame(frame_calculador_remanescentes, fg_color="transparent", width=600, height=100, corner_radius=10)
frame_regra_tres.pack(pady=5, padx=5)  # Reduzindo os paddings internos

# "Se" <Entry1> "está para" <Entry2> "então" <Entry3> "está para" <Resultado>
entry1_var = StringVar(value="")
entry2_var = StringVar(value="")
entry3_var = StringVar(value="")

entry1 = ctk.CTkEntry(frame_regra_tres, width=100, font=("Arial", 14), justify="center", textvariable=entry1_var)
entry1.grid(row=0, column=0, padx=5)  # Reduzindo os paddings internos

label_estapara1 = ctk.CTkLabel(frame_regra_tres, text="está para", font=("Arial", 14))
label_estapara1.grid(row=0, column=1, padx=5)  # Reduzindo os paddings internos

entry2 = ctk.CTkEntry(frame_regra_tres, width=100, font=("Arial", 14), justify="center", textvariable=entry2_var)
entry2.grid(row=0, column=2, padx=5)  # Reduzindo os paddings internos

label_entao = ctk.CTkLabel(frame_regra_tres, text="então", font=("Arial", 14))
label_entao.grid(row=0, column=3, padx=5)  # Reduzindo os paddings internos

entry3 = ctk.CTkEntry(frame_regra_tres, width=100, font=("Arial", 14), justify="center", textvariable=entry3_var)
entry3.grid(row=0, column=4, padx=5)  # Reduzindo os paddings internos

label_estapara2 = ctk.CTkLabel(frame_regra_tres, text="está para", font=("Arial", 14))
label_estapara2.grid(row=0, column=5, padx=5)  # Reduzindo os paddings internos

label_resultado = ctk.CTkLabel(frame_regra_tres, text="Resultado", font=("Arial", 14, "bold"))
label_resultado.grid(row=0, column=6, padx=5)  # Reduzindo os paddings internos



# Texto de instruções
label_instrucoes = ctk.CTkLabel(frame_calculador_remanescentes, text="Instruções: Entry 01 - Soldados Fatorados, Entry 02 - Soldados TOTAL CHEIO, Entry 03 - Fatorado Restante", font=("Arial", 12))
label_instrucoes.pack(pady=5)  # Reduzindo o padding interno

# Função para calcular o resultado da regra de três
def calcular_regra_tres():
    if not entry1_var.get().isdigit() or not entry2_var.get().isdigit() or not entry3_var.get().isdigit():
        exibir_notificacao("Por favor, insira valores válidos para todos os campos.", "#FF0000")
        return

    valor_x = int(entry1_var.get())
    valor_y = int(entry2_var.get())
    valor_a = int(entry3_var.get())

    if valor_x == 0:
        exibir_notificacao("O valor de X não pode ser 0.", "#FF0000")
        return

    # Aplicar a regra de três para calcular o valor b
    resultado_b = (valor_a * valor_y) // valor_x

    # Atualizar o label com o resultado
    label_resultado.configure(text=str(resultado_b))

# Aplicando a validação de entrada
validate_cmd = frame_calculador_remanescentes.register(validar_inteiro)
entry1.configure(validate="key", validatecommand=(validate_cmd, "%P"))
entry2.configure(validate="key", validatecommand=(validate_cmd, "%P"))
entry3.configure(validate="key", validatecommand=(validate_cmd, "%P"))

# Botão para Calcular os Remanescentes
botao_calcular_remanescentes = ctk.CTkButton(frame_calculador_remanescentes, text="Calcular", font=("Arial", 14), command=calcular_regra_tres)
botao_calcular_remanescentes.pack(pady=10)  # Reduzindo o padding interno




################################
#                              #
#  Calculadora de Subtração e Adição #
#                              #
################################

# Adicionando o Frame para a calculadora de subtração e adição abaixo do calculador de remanescentes
frame_calculadora = ctk.CTkFrame(tab_outros, fg_color="#2a2a2a", corner_radius=10)
frame_calculadora.pack(pady=10, padx=10, fill="x")  # Reduzindo os paddings externos

# Título da Calculadora de Subtração e Adição
label_calculadora_titulo = ctk.CTkLabel(frame_calculadora, text="Calculadora de Subtração e Adição", font=("Arial", 18, "bold"))
label_calculadora_titulo.pack(pady=5)  # Reduzindo o padding interno

# Frame para os textos e entradas da subtração
frame_subtracao = ctk.CTkFrame(frame_calculadora, fg_color="transparent", width=600, height=100, corner_radius=10)
frame_subtracao.pack(pady=5, padx=5)  # Reduzindo os paddings internos

# Subtração: <Entry1> - <Entry2> = <Resultado>
entry_sub_a_var = StringVar(value="")
entry_sub_b_var = StringVar(value="")

entry_sub_a = ctk.CTkEntry(frame_subtracao, width=100, font=("Arial", 14), justify="center", textvariable=entry_sub_a_var)
entry_sub_a.grid(row=0, column=0, padx=5)  # Reduzindo os paddings internos

label_menos = ctk.CTkLabel(frame_subtracao, text="-", font=("Arial", 18, "bold"))
label_menos.grid(row=0, column=1, padx=5)  # Reduzindo os paddings internos

entry_sub_b = ctk.CTkEntry(frame_subtracao, width=100, font=("Arial", 14), justify="center", textvariable=entry_sub_b_var)
entry_sub_b.grid(row=0, column=2, padx=5)  # Reduzindo os paddings internos

label_igual_subtracao = ctk.CTkLabel(frame_subtracao, text="=", font=("Arial", 18, "bold"))
label_igual_subtracao.grid(row=0, column=3, padx=5)  # Reduzindo os paddings internos

label_resultado_subtracao = ctk.CTkLabel(frame_subtracao, text="Resultado", font=("Arial", 14, "bold"))
label_resultado_subtracao.grid(row=0, column=4, padx=5)  # Reduzindo os paddings internos



# Adição: <Entry3> + <Entry4> = <Resultado>
frame_adicao = ctk.CTkFrame(frame_calculadora, fg_color="transparent", width=600, height=100, corner_radius=10)
frame_adicao.pack(pady=5, padx=5)  # Reduzindo os paddings internos

entry_add_a_var = StringVar(value="")
entry_add_b_var = StringVar(value="")

entry_add_a = ctk.CTkEntry(frame_adicao, width=100, font=("Arial", 14), justify="center", textvariable=entry_add_a_var)
entry_add_a.grid(row=0, column=0, padx=5)  # Reduzindo os paddings internos

label_mais = ctk.CTkLabel(frame_adicao, text="+", font=("Arial", 18, "bold"))
label_mais.grid(row=0, column=1, padx=5)  # Reduzindo os paddings internos

entry_add_b = ctk.CTkEntry(frame_adicao, width=100, font=("Arial", 14), justify="center", textvariable=entry_add_b_var)
entry_add_b.grid(row=0, column=2, padx=5)  # Reduzindo os paddings internos

label_igual_adicao = ctk.CTkLabel(frame_adicao, text="=", font=("Arial", 18, "bold"))
label_igual_adicao.grid(row=0, column=3, padx=5)  # Reduzindo os paddings internos

label_resultado_adicao = ctk.CTkLabel(frame_adicao, text="Resultado", font=("Arial", 14, "bold"))
label_resultado_adicao.grid(row=0, column=4, padx=5)  # Reduzindo os paddings internos

# Função para calcular a subtração
def calcular_subtracao():
    if not entry_sub_a_var.get().isdigit() or not entry_sub_b_var.get().isdigit():
        exibir_notificacao("Por favor, insira valores válidos para ambos os campos.", "#FF0000")
        return

    valor_a = int(entry_sub_a_var.get())
    valor_b = int(entry_sub_b_var.get())

    # Calcular a subtração
    resultado = valor_a - valor_b

    # Atualizar o label com o resultado
    label_resultado_subtracao.configure(text=str(resultado))

# Função para calcular a adição
def calcular_adicao():
    if not entry_add_a_var.get().isdigit() or not entry_add_b_var.get().isdigit():
        exibir_notificacao("Por favor, insira valores válidos para ambos os campos.", "#FF0000")
        return

    valor_a = int(entry_add_a_var.get())
    valor_b = int(entry_add_b_var.get())

    # Calcular a adição
    resultado = valor_a + valor_b

    # Atualizar o label com o resultado
    label_resultado_adicao.configure(text=str(resultado))

# Aplicando a validação de entrada para subtração
entry_sub_a.configure(validate="key", validatecommand=(validate_cmd, "%P"))
entry_sub_b.configure(validate="key", validatecommand=(validate_cmd, "%P"))

# Aplicando a validação de entrada para adição
entry_add_a.configure(validate="key", validatecommand=(validate_cmd, "%P"))
entry_add_b.configure(validate="key", validatecommand=(validate_cmd, "%P"))

# Botão para Calcular a Adição
botao_calcular_adicao = ctk.CTkButton(frame_calculadora, text="Calcular Adição", font=("Arial", 14), command=calcular_adicao)
botao_calcular_adicao.pack(pady=5)  # Reduzindo o padding interno

# Botão para Calcular a Subtração
botao_calcular_subtracao = ctk.CTkButton(frame_calculadora, text="Calcular Subtração", font=("Arial", 14), command=calcular_subtracao)
botao_calcular_subtracao.pack(pady=5)  # Reduzindo o padding interno

#####################
# BOTÃO LIMPAR CAMPOS
#####################
# Função para limpar todos os campos
def limpar_campos():
    # Limpar campos do Calculador de Proporções
    lado_a_var.set("")
    lado_b_var.set("")
    label_proporcao.configure(text="A proporção é de: ")

    # Limpar campos do Calculador de Remanescentes
    entry1_var.set("")
    entry2_var.set("")
    entry3_var.set("")
    label_resultado.configure(text="Resultado")

    # Limpar campos da Calculadora de Subtração e Adição
    entry_sub_a_var.set("")
    entry_sub_b_var.set("")
    label_resultado_subtracao.configure(text="Resultado")
    entry_add_a_var.set("")
    entry_add_b_var.set("")
    label_resultado_adicao.configure(text="Resultado")

# Botão para Limpar Todos os Campos
botao_limpar_campos = ctk.CTkButton(tab_outros, text="Limpar Campos", font=("Arial", 16, "bold"), command=limpar_campos)
botao_limpar_campos.pack(pady=15, padx=20, fill="x")  # Ajustando o padding e tornando o botão mais largo




################################
#                              #
# ROLAGEM DE TURNO AUTOMÁTICA  #
#                              #
################################

# TODO: DEIXAR O FRAME FIXO E NÃO DINAMICO

# Variável para controlar o estado do auto-turno
auto_rolagem_ativa = False

# Variável para definir o tempo total de carregamento em segundos
tempo_carregamento = 15  # Defina aqui o tempo desejado em segundos

# Função para simular a barra de progresso com base no tempo definido
# Função para simular a barra de progresso com base no tempo definido
# Variável para controlar o estado do auto-turno
auto_rolagem_ativa = False

# Variável para definir o tempo total de carregamento em segundos
tempo_carregamento = 15  # Defina aqui o tempo desejado em segundos

# Função para simular a barra de progresso com base no tempo definido
def simular_barra_progresso(valor_atual=0):
    if auto_rolagem_ativa:
        barra_progresso.set(valor_atual / 100)  # Define o valor da barra entre 0 e 1

        if valor_atual < 100:
            # Calcula o delay baseado no tempo total de carregamento
            delay = int((tempo_carregamento * 1000) / 100)  # Delay em milissegundos
            app.after(delay, simular_barra_progresso, valor_atual + 1)
        else:
            incrementar_turno()
            barra_progresso.set(0)  # Reseta a barra de progresso após completar o progresso
            simular_barra_progresso()  # Recomeça o processo

# Função para controlar o estado da rolagem automática
def alternar_rolagem_automatica():
    global auto_rolagem_ativa
    auto_rolagem_ativa = checkbox_auto_rolagem.get() == 1

    if auto_rolagem_ativa:
        # Oculta o botão de próximo turno e mostra a barra de progresso
        botao_proximo_turno.pack_forget()
        barra_progresso.pack(side="top", pady=(10, 10), anchor="center")  # Use 'anchor="center"' para centralizar
        simular_barra_progresso()  # Inicia a barra de progresso
    else:
        # Mostra o botão de próximo turno e oculta a barra de progresso
        barra_progresso.pack_forget()
        botao_proximo_turno.pack(side="top", pady=(10, 10), anchor="center")


# Criação do frame que conterá todos os elementos da rolagem, ajustando para ocupar a largura total
frame_rolagem = ctk.CTkFrame(frame_gerenciamento, height=130)  # Definindo uma altura fixa
frame_rolagem.pack_propagate(False)  # Impedindo que o frame altere seu tamanho
frame_rolagem.pack(pady=(5, 5), padx=10, side="bottom", fill="x")  # Coloca o frame no final do tab de gerenciamento

# Empacotamento do checkbox de rolagem automática dentro do frame
checkbox_auto_rolagem = ctk.CTkCheckBox(frame_rolagem, text="Rolagem Automática de Turnos", command=alternar_rolagem_automatica)
checkbox_auto_rolagem.pack(pady=(0, 5), anchor="center")

# Inicialmente, a barra de progresso está oculta e empacotada dentro do frame
barra_progresso = ctk.CTkProgressBar(frame_rolagem, orientation="horizontal", width=200, height=20)

# Empacotamento da label que mostra o turno atual dentro do frame
label_turno_atual = ctk.CTkLabel(frame_rolagem, text=f"Turno {turno_atual}", font=("Arial", 20, "bold"))
label_turno_atual.pack(pady=(5, 5), anchor="center")

# Empacotamento do botão de próximo turno dentro do frame
botao_proximo_turno = ctk.CTkButton(frame_rolagem, text="PRÓXIMO TURNO", font=("Arial", 16, "bold"), width=180, height=40, command=incrementar_turno)
botao_proximo_turno.pack(pady=(5, 5), anchor="center")




################################
#                              #
#  Configuration Tab           #
#                              #
################################

def exibir_notificacao(mensagem, cor):
    notificacao = ctk.CTkLabel(app, text=mensagem, font=("Arial", 14), fg_color=cor, corner_radius=8, text_color="white")
    notificacao.place(relx=0.5, rely=0.9, anchor="center")
    notificacao.after(3000, notificacao.destroy)

def atualizar_dados():
    interface_manager.atualizar_interface(seletor_reino.get())

def atualizar_opcoes_reino():
    dados = carregar_dados_json()
    reinos = list(dados.get("reinos", {}).keys())

    if reinos:
        interface_manager.seletor_reino.configure(values=reinos)
        interface_manager.seletor_reino.set(reinos[0])
        interface_manager.atualizar_interface(reinos[0])

        # Atualizar também os seletores na aba Combate
        interface_manager.seletor_reino_esquerdo.configure(values=reinos)
        interface_manager.seletor_reino_direito.configure(values=reinos)
        interface_manager.seletor_reino_esquerdo.set(reinos[0])
        interface_manager.seletor_reino_direito.set(reinos[0])
        interface_manager.on_select_reino_esquerdo(reinos[0])
        interface_manager.on_select_reino_direito(reinos[0])
    else:
        interface_manager.seletor_reino.configure(values=[])
        interface_manager.seletor_reino.set("")
        interface_manager.limpar_interface()

        # Limpar também os seletores na aba Combate
        interface_manager.seletor_reino_esquerdo.configure(values=[])
        interface_manager.seletor_reino_direito.configure(values=[])
        interface_manager.seletor_reino_esquerdo.set("")
        interface_manager.seletor_reino_direito.set("")




def validar_populacao(valor):
    return valor.isdigit() or valor == ""

frame_config = ctk.CTkFrame(tab_config, width=760, height=580)
frame_config.pack(pady=10, padx=10, fill="both", expand=True)

frame_criacao_edicao = ctk.CTkFrame(frame_config, fg_color="#2b2b2b", corner_radius=8)
frame_criacao_edicao.pack(pady=10, padx=10, fill="x")

frame_criacao = ctk.CTkFrame(frame_criacao_edicao, fg_color="#2b2b2b", corner_radius=8)
frame_criacao.pack(pady=10, padx=10, side="left", fill="both", expand=True)

label_nome_reino = ctk.CTkLabel(frame_criacao, text="Nome do Reino:", font=("Arial", 14))
label_nome_reino.pack(pady=5)
entry_nome_reino = ctk.CTkEntry(frame_criacao, width=200, placeholder_text="Nome do Reino")
entry_nome_reino.pack(pady=5)

label_populacao_inicial = ctk.CTkLabel(frame_criacao, text="População Inicial:", font=("Arial", 14))
label_populacao_inicial.pack(pady=5)
entry_populacao_inicial = ctk.CTkEntry(frame_criacao, width=200, placeholder_text="População Inicial")
entry_populacao_inicial.pack(pady=5)

validate_cmd = frame_criacao.register(validar_populacao)
entry_populacao_inicial.configure(validate="key", validatecommand=(validate_cmd, "%P"))

def limpar_campos_criacao():
    entry_nome_reino.delete(0, "end")
    entry_populacao_inicial.delete(0, "end")

def criar_reino_com_validacao():
    nome_reino = entry_nome_reino.get()
    populacao_inicial = entry_populacao_inicial.get()

    if not nome_reino:
        exibir_notificacao("O nome do reino não pode estar vazio!", "#FF0000")
        return

    if not populacao_inicial:
        exibir_notificacao("A população inicial não pode estar vazia!", "#FF0000")
        return

    try:
        populacao_inicial = int(populacao_inicial)
    except ValueError:
        exibir_notificacao("População inicial deve ser um número válido!", "#FF0000")
        return

    criar_reino(nome_reino, populacao_inicial)
    atualizar_opcoes_reino()  # Atualiza todos os seletores após a criação do reino
    atualizar_seletor_exclusao()
    atualizar_seletor_edicao()
    limpar_campos_criacao()
    exibir_notificacao(f"Reino '{nome_reino}' criado com sucesso!", "#4CAF50")

def excluir_reino_e_atualizar():
    excluir_reino(seletor_reino_exclusao.get())
    atualizar_opcoes_reino()  # Atualiza todos os seletores após a exclusão do reino
    atualizar_seletor_exclusao()
    atualizar_seletor_edicao()
    exibir_notificacao(f"Reino '{seletor_reino_exclusao.get()}' excluído com sucesso!", "#FFC107")



botao_criar_reino = ctk.CTkButton(frame_criacao, text="Criar Reino", command=criar_reino_com_validacao)
botao_criar_reino.pack(pady=10)

frame_edicao = ctk.CTkFrame(frame_criacao_edicao, fg_color="#2b2b2b", corner_radius=8)
frame_edicao.pack(pady=10, padx=10, side="left", fill="both", expand=True)

label_selecionar_reino = ctk.CTkLabel(frame_edicao, text="Selecionar Reino para Editar:", font=("Arial", 14))
label_selecionar_reino.pack(pady=5)
seletor_reino_edicao = ctk.CTkOptionMenu(frame_edicao, values=[], command=lambda _: preencher_campos_edicao(seletor_reino_edicao.get()))
seletor_reino_edicao.pack(pady=5)

def preencher_campos_edicao(nome_reino):
    dados = carregar_dados_json()
    reino = dados.get("reinos", {}).get(nome_reino, {})
    entry_nome_edicao.delete(0, "end")
    entry_nome_edicao.insert(0, nome_reino)
    entry_populacao_edicao.delete(0, "end")
    entry_populacao_edicao.insert(0, reino.get("populacao", 0))

label_nome_edicao = ctk.CTkLabel(frame_edicao, text="Novo Nome do Reino:", font=("Arial", 14))
label_nome_edicao.pack(pady=5)
entry_nome_edicao = ctk.CTkEntry(frame_edicao, width=200, placeholder_text="Novo Nome do Reino")
entry_nome_edicao.pack(pady=5)

label_populacao_edicao = ctk.CTkLabel(frame_edicao, text="Nova População:", font=("Arial", 14))
label_populacao_edicao.pack(pady=5)
entry_populacao_edicao = ctk.CTkEntry(frame_edicao, width=200, placeholder_text="Nova População")
entry_populacao_edicao.pack(pady=5)

validate_cmd_edicao = frame_edicao.register(validar_populacao)
entry_populacao_edicao.configure(validate="key", validatecommand=(validate_cmd_edicao, "%P"))

def salvar_edicao_reino():
    nome_reino_atual = seletor_reino_edicao.get()
    novo_nome = entry_nome_edicao.get()
    nova_populacao = int(entry_populacao_edicao.get() or 0)

    if novo_nome and nova_populacao:
        atualizar_reino(nome_reino_atual, novo_nome, nova_populacao)
        atualizar_opcoes_reino()
        atualizar_seletor_exclusao()
        atualizar_seletor_edicao()
        exibir_notificacao(f"Reino '{nome_reino_atual}' atualizado com sucesso!", "#4CAF50")
    else:
        exibir_notificacao("Preencha todos os campos!", "#FF0000")

botao_salvar_edicao = ctk.CTkButton(frame_edicao, text="Salvar Alterações", command=salvar_edicao_reino)
botao_salvar_edicao.pack(pady=10)

def atualizar_seletor_edicao():
    dados = carregar_dados_json()
    reinos_para_edicao = list(dados.get("reinos", {}).keys())
    seletor_reino_edicao.configure(values=reinos_para_edicao)

    if reinos_para_edicao:
        seletor_reino_edicao.set(reinos_para_edicao[0])
        preencher_campos_edicao(reinos_para_edicao[0])
    else:
        seletor_reino_edicao.set("")
        entry_nome_edicao.delete(0, "end")
        entry_populacao_edicao.delete(0, "end")

atualizar_seletor_edicao()

frame_exclusao = ctk.CTkFrame(frame_config, fg_color="#2b2b2b", corner_radius=8)
frame_exclusao.pack(pady=10, padx=10, fill="x")

label_excluir_reino = ctk.CTkLabel(frame_exclusao, text="Excluir Reino:", font=("Arial", 14))
label_excluir_reino.pack(pady=5)
seletor_reino_exclusao = ctk.CTkOptionMenu(frame_exclusao, values=[])
seletor_reino_exclusao.pack(pady=5)

def atualizar_opcoes_reino_combate():
    reinos = list(dados.get("reinos", {}).keys())
    seletor_reino_esquerdo.configure(values=reinos)
    seletor_reino_direito.configure(values=reinos)

    if reinos:
        seletor_reino_esquerdo.set(reinos[0])
        seletor_reino_direito.set(reinos[0])
        on_select_reino_esquerdo(reinos[0])
        on_select_reino_direito(reinos[0])
    else:
        seletor_reino_esquerdo.set("")
        seletor_reino_direito.set("")


def excluir_reino_e_atualizar():
    excluir_reino(seletor_reino_exclusao.get())
    atualizar_opcoes_reino()  # Atualiza todos os seletores após a exclusão do reino
    atualizar_seletor_exclusao()
    atualizar_seletor_edicao()
    exibir_notificacao(f"Reino '{seletor_reino_exclusao.get()}' excluído com sucesso!", "#FFC107")


botao_excluir_reino = ctk.CTkButton(frame_exclusao, text="Excluir Reino", state="normal", command=excluir_reino_e_atualizar)
botao_excluir_reino.pack(pady=10)

def atualizar_seletor_exclusao():
    dados = carregar_dados_json()
    reinos_para_exclusao = list(dados.get("reinos", {}).keys())
    seletor_reino_exclusao.configure(values=reinos_para_exclusao)

    if reinos_para_exclusao:
        seletor_reino_exclusao.set(reinos_para_exclusao[0])
        seletor_reino_exclusao.configure(state="normal")
        botao_excluir_reino.configure(state="normal")
    else:
        seletor_reino_exclusao.set("")
        seletor_reino_exclusao.configure(state="disabled")
        botao_excluir_reino.configure(state="disabled")

atualizar_seletor_exclusao()

interface_manager.registrar_componentes(
    seletor_reino=seletor_reino,
    label_populacao=label_populacao_valor_zero,
    labels_tropas=labels_tropas,
    tabela_economia=tabela_zero,
    label_valor_fundos=label_valor_fundos_zero,
    label_valor_esperado=label_valor_esperado_zero,
    frame_tecnologias=frame_tecnologias,
    seletor_reino_esquerdo=seletor_reino_esquerdo,
    seletor_reino_direito=seletor_reino_direito,
    on_select_reino_esquerdo=on_select_reino_esquerdo,
    on_select_reino_direito=on_select_reino_direito
)


# Inicializar tropas e atualizar HP corretamente ao iniciar o jogo
if reinos_disponiveis:
    reino_padrao = reinos_disponiveis[0]  # Primeiro reino da lista
    seletor_reino_esquerdo.set(reino_padrao)
    seletor_reino_direito.set(reino_padrao)
    on_select_reino_esquerdo(reino_padrao)
    on_select_reino_direito(reino_padrao)

    tropa_padrao = tipo_de_tropas[0]  # Primeira tropa da lista
    seletor_tropas_esquerdo.set(tropa_padrao)
    seletor_tropas_direito.set(tropa_padrao)
    on_select_tropa_esquerdo(tropa_padrao)
    on_select_tropa_direito(tropa_padrao)

atualizar_dados()
atualizar_opcoes_reino()

app.mainloop()
