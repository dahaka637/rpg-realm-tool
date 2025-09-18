#XXXXXXXXXXXXXXXXXXXXXXXX
#XX COMEÇO DO MENUS.PY XX
#XXXXXXXXXXXXXXXXXXXXXXXX
import customtkinter as ctk
from tkinter import StringVar, ttk, Menu
from PIL import Image
import os
import time
from functions import carregar_dados_json, salvar_dados_json, interface_manager, calcular_e_atualizar_economia
import random
import string


################################
#                              #
#   Utility Functions          #
#                              #
################################
# RESUMO DO OPERADOR: Esta seção contém funções utilitárias para exibir notificações e 
# para cálculos usados em diferentes partes da interface.

def verificar_tecnologia_bancos(nome_reino):
    """
    Verifica se o reino possui a tecnologia de Bancos.
    Retorna True se possuir, caso contrário, retorna False.
    """
    dados = carregar_dados_json()
    reino = dados["reinos"].get(nome_reino, {})
    return "Bancos" in reino.get("tecnologias", {})

def gerar_identificador():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

def exibir_notificacao(popup, mensagem, cor):
    """
    Exibe uma notificação temporária no popup fornecido.
    """
    notificacao = ctk.CTkLabel(popup, text=mensagem, font=("Arial", 14), fg_color=cor, corner_radius=8, text_color="white")
    notificacao.place(relx=0.5, rely=0.9, anchor="center")
    notificacao.after(3000, notificacao.destroy)

def validar_valor(valor):
    """
    Valida se a entrada de valor é numérica, permitindo um ponto decimal.
    """
    return valor.replace('.', '', 1).isdigit() or valor == ""

################################
#                              #
#  Financial Management        #
#                              #
################################
# RESUMO DO OPERADOR: Esta seção lida com a gestão financeira do reino, permitindo ao usuário 
# adicionar receitas ou despesas e atualizar o saldo e as previsões financeiras.

def movimentar_caixa(nome_reino, tipo, nome_movimentacao, valor, turnos):
    """
    Adiciona uma movimentação de caixa (lucro ou despesa) ao reino especificado.
    """
    dados = carregar_dados_json()
    
    if "reinos" in dados and nome_reino in dados["reinos"]:
        reino = dados["reinos"][nome_reino]

        # Verificar se é um lucro ou despesa e atualizar os dados corretamente
        if tipo == "Lucro":
            if nome_movimentacao in reino["economia"]["receita"]:
                reino["economia"]["receita"][nome_movimentacao]["valor"] += valor
                reino["economia"]["receita"][nome_movimentacao]["turnos"] += turnos
            else:
                reino["economia"]["receita"][nome_movimentacao] = {"valor": valor, "turnos": turnos}
        elif tipo == "Despesa":
            if nome_movimentacao in reino["economia"]["despesa"]:
                reino["economia"]["despesa"][nome_movimentacao]["valor"] += valor
                reino["economia"]["despesa"][nome_movimentacao]["turnos"] += turnos
            else:
                reino["economia"]["despesa"][nome_movimentacao] = {"valor": valor, "turnos": turnos}

        # Recalcular os fundos previstos com base nas receitas e despesas atualizadas
        total_receitas = sum(receita["valor"] for receita in reino["economia"]["receita"].values())
        total_despesas = sum(despesa["valor"] for despesa in reino["economia"]["despesa"].values())
        reino["fundos_previstos"] = total_receitas - total_despesas

        salvar_dados_json(dados)
        interface_manager.atualizar_interface(nome_reino)
        print(f"Movimentação '{nome_movimentacao}' de {tipo} adicionada com sucesso ao reino '{nome_reino}' por {turnos} turno(s).")
    else:
        print(f"Reino '{nome_reino}' não encontrado.")
        exibir_notificacao(None, f"Reino '{nome_reino}' não encontrado!", "#FF0000")


def abrir_economia(nome_reino):
    """
    Abre a interface de gerenciamento de economia, permitindo ao usuário adicionar movimentações financeiras.
    """
    # Criação do popup para economia
    popup = ctk.CTkToplevel()
    popup.title("Economia")
    popup.geometry("460x620")
    popup.grab_set()  # Mantém o popup no topo
    popup.iconbitmap(os.path.join(os.path.dirname(__file__), "logo.ico"))  

    # Criação do TabView
    tabview_economia = ctk.CTkTabview(popup, width=580, height=550)
    tabview_economia.pack(pady=10, padx=10, fill="both", expand=True)

    # Adicionando a aba "Lançamentos"
    tab_lancamentos = tabview_economia.add("Lançamentos")

    # Label de título
    label_titulo = ctk.CTkLabel(tab_lancamentos, text="Gerar Movimentação de Caixa", font=("Arial", 18, "bold"))
    label_titulo.pack(pady=20)

    # Opção de Tipo: Despesa ou Lucro
    tipo_var = StringVar(value="Despesa")
    frame_tipo = ctk.CTkFrame(tab_lancamentos, fg_color="#2a2a2a", corner_radius=10)
    frame_tipo.pack(pady=10, padx=20, fill="x")
    ctk.CTkLabel(frame_tipo, text="Tipo:", font=("Arial", 14)).pack(side="left", padx=10, pady=10)
    ctk.CTkRadioButton(frame_tipo, text="Despesa", variable=tipo_var, value="Despesa", font=("Arial", 12)).pack(side="left", padx=5)
    ctk.CTkRadioButton(frame_tipo, text="Lucro", variable=tipo_var, value="Lucro", font=("Arial", 12)).pack(side="left", padx=5)

    # Função para mostrar ou esconder o campo de turnos
    def mostrar_turnos(mostrar):
        if mostrar:
            frame_turnos.pack(pady=5, padx=20, fill="x", after=frame_frequencia)
        else:
            frame_turnos.pack_forget()

    # Opção de Frequência: Único ou Consecutivo
    frequencia_var = StringVar(value="Único")
    frame_frequencia = ctk.CTkFrame(tab_lancamentos, fg_color="#2a2a2a", corner_radius=10)
    frame_frequencia.pack(pady=10, padx=20, fill="x")
    ctk.CTkLabel(frame_frequencia, text="Frequência:", font=("Arial", 14)).pack(side="left", padx=10, pady=10)
    ctk.CTkRadioButton(frame_frequencia, text="Único", variable=frequencia_var, value="Único", font=("Arial", 12), command=lambda: mostrar_turnos(False)).pack(side="left", padx=5)
    ctk.CTkRadioButton(frame_frequencia, text="Consecutivo", variable=frequencia_var, value="Consecutivo", font=("Arial", 12), command=lambda: mostrar_turnos(True)).pack(side="left", padx=5)

    # Entrada para o número de turnos (aparece logo abaixo da frequência)
    turnos_var = StringVar(value="1")
    frame_turnos = ctk.CTkFrame(tab_lancamentos, fg_color="#2a2a2a", corner_radius=10)
    frame_turnos.pack(pady=5, padx=20, fill="x")
    ctk.CTkLabel(frame_turnos, text="Turnos:", font=("Arial", 14)).pack(side="left", padx=10, pady=10)
    entry_turnos = ctk.CTkEntry(frame_turnos, width=50, textvariable=turnos_var, font=("Arial", 12))
    entry_turnos.pack(side="left", padx=5)
    frame_turnos.pack_forget()  # Escondido por padrão, aparece somente se "Consecutivo" for selecionado

    # Entrada para o nome do tipo de movimentação
    nome_movimentacao_var = StringVar()
    frame_nome_movimentacao = ctk.CTkFrame(tab_lancamentos, fg_color="#2a2a2a", corner_radius=10)
    frame_nome_movimentacao.pack(pady=10, padx=20, fill="x")
    ctk.CTkLabel(frame_nome_movimentacao, text="Nome da Movimentação:", font=("Arial", 14)).pack(side="left", padx=10, pady=10)
    entry_nome_movimentacao = ctk.CTkEntry(frame_nome_movimentacao, width=200, textvariable=nome_movimentacao_var, font=("Arial", 12))
    entry_nome_movimentacao.pack(side="left", padx=5)

    # Entrada para o valor da movimentação
    valor_var = StringVar()
    frame_valor = ctk.CTkFrame(tab_lancamentos, fg_color="#2a2a2a", corner_radius=10)
    frame_valor.pack(pady=10, padx=20, fill="x")
    ctk.CTkLabel(frame_valor, text="Valor:", font=("Arial", 14)).pack(side="left", padx=10, pady=10)
    entry_valor = ctk.CTkEntry(frame_valor, width=200, textvariable=valor_var, font=("Arial", 12))
    entry_valor.pack(side="left", padx=5)

    # Aplicando a validação de valor
    validate_cmd = popup.register(validar_valor)
    entry_valor.configure(validate="key", validatecommand=(validate_cmd, "%P"))

    # Função para gerar a movimentação
    def gerar_movimentacao():
        valor = valor_var.get().strip()
        if valor == "" or not validar_valor(valor):
            exibir_notificacao(popup, "Por favor, insira um valor válido.", "#FF0000")
            return
        
        movimentar_caixa(
            nome_reino, 
            tipo_var.get(), 
            f"{nome_movimentacao_var.get()} ({turnos_var.get()} parcelas)" if frequencia_var.get() == "Consecutivo" else nome_movimentacao_var.get(),
            float(valor),
            int(turnos_var.get()) if frequencia_var.get() == "Consecutivo" else 1
        )

    # Botão para gerar a movimentação
    botao_gerar = ctk.CTkButton(tab_lancamentos, text="Gerar Movimentação", font=("Arial", 14), command=gerar_movimentacao)
    botao_gerar.pack(pady=20)

    ################################
    # Banco - Interface Visual     #
    ################################

    # Adicionando a aba "Banco"
    tab_banco = tabview_economia.add("Banco")


    ####################################
    #       SEÇÃO DO BANCO             #
    ####################################
    dados = carregar_dados_json()
    montante_poupanca = dados["banco"].get(nome_reino, {}).get("poupanca", 0.0)

    # Criação do Sub-TabView para separar Poupança e Empréstimos
    sub_tabview_banco = ctk.CTkTabview(tab_banco, width=560, height=480)
    sub_tabview_banco.pack(pady=10, padx=10, fill="both", expand=True)

    # Adicionando a sub-aba "Poupança"
    tab_poupanca = sub_tabview_banco.add("Poupança")

    # Texto indicando o total depositado
    label_total_depositado = ctk.CTkLabel(tab_poupanca, text="Total Depositado: R$ 0,00", font=("Arial", 14, "bold"))
    label_total_depositado.pack(pady=10)
    label_total_depositado.configure(text=f"Total Depositado: R$ {montante_poupanca:,.2f}")

    # Identificador e entrada para valor de depósito
    label_valor_deposito = ctk.CTkLabel(tab_poupanca, text="Valor para Depósito:", font=("Arial", 12), anchor="center")
    label_valor_deposito.pack(pady=5, padx=5)

    entry_valor_deposito = ctk.CTkEntry(tab_poupanca, width=200, font=("Arial", 12))
    entry_valor_deposito.pack(pady=5, padx=5)

    # Aplicando validação para permitir apenas números
    def validar_numeros(valor):
        return valor.isdigit() or valor == ""

    validate_cmd_deposito = tab_poupanca.register(validar_numeros)
    entry_valor_deposito.configure(validate="key", validatecommand=(validate_cmd_deposito, "%P"))

    # Funções de Depósito e Saque
    def executar_deposito():
        if not verificar_tecnologia_bancos(nome_reino):
            exibir_notificacao(tab_poupanca, "Você não possui a tecnologia de Bancos!", "#FF0000")
            return
        
        valor = float(entry_valor_deposito.get())
        sucesso, mensagem = depositar_poupanca(nome_reino, valor)
        if sucesso:
            label_total_depositado.configure(text=f"Total Depositado: R$ {carregar_dados_json()['banco'][nome_reino]['poupanca']:,.2f}")
            interface_manager.atualizar_interface(nome_reino)
        exibir_notificacao(tab_poupanca, mensagem, "#00FF00" if sucesso else "#FF0000")


    def executar_saque():
        if not verificar_tecnologia_bancos(nome_reino):
            exibir_notificacao(tab_poupanca, "Você não possui a tecnologia de Bancos!", "#FF0000")
            return
        
        valor = float(entry_valor_deposito.get())
        sucesso, mensagem = sacar_poupanca(nome_reino, valor)
        if sucesso:
            label_total_depositado.configure(text=f"Total Depositado: R$ {carregar_dados_json()['banco'][nome_reino]['poupanca']:,.2f}")
            interface_manager.atualizar_interface(nome_reino)
        exibir_notificacao(tab_poupanca, mensagem, "#00FF00" if sucesso else "#FF0000")


    # Botões para Sacar e Depositar, posicionados logo abaixo da entrada de valor e mais próximos entre si
    frame_botoes_poupanca = ctk.CTkFrame(tab_poupanca, fg_color="transparent")
    frame_botoes_poupanca.pack(pady=10, padx=5, anchor="center")

    botao_sacar = ctk.CTkButton(frame_botoes_poupanca, text="Sacar", font=("Arial", 14), width=100, command=executar_saque)
    botao_sacar.pack(side="left", padx=5)

    botao_depositar = ctk.CTkButton(frame_botoes_poupanca, text="Depositar", font=("Arial", 14), width=100, command=executar_deposito)
    botao_depositar.pack(side="left", padx=5)

    ##########################################
    # Adicionando a sub-aba "Empréstimos"
    ##########################################

    tab_emprestimos = sub_tabview_banco.add("Empréstimos")

    # Tabela de Empréstimos com três colunas
    label_emprestimos = ctk.CTkLabel(tab_emprestimos, text="Empréstimos Ativos:", font=("Arial", 14, "bold"))
    label_emprestimos.pack(pady=5)

    # Frame para tabela de empréstimos e barra de rolagem
    frame_tabela_emprestimos = ctk.CTkFrame(tab_emprestimos, fg_color="transparent")
    frame_tabela_emprestimos.pack(fill="x", padx=10, pady=5)

    tabela_emprestimos = ttk.Treeview(frame_tabela_emprestimos, columns=("col1", "col2", "col3"), show="headings", height=3, style="Treeview")
    tabela_emprestimos.pack(side="left", fill="both", expand=True)

    scrollbar_emprestimos = ttk.Scrollbar(frame_tabela_emprestimos, orient="vertical", command=tabela_emprestimos.yview)
    tabela_emprestimos.configure(yscrollcommand=scrollbar_emprestimos.set)
    scrollbar_emprestimos.pack(side="right", fill="y")

    tabela_emprestimos.heading("col1", text="Empréstimo")
    tabela_emprestimos.heading("col2", text="Parcelas")
    tabela_emprestimos.heading("col3", text="Valor Total (R$)")

    tabela_emprestimos.column("col1", width=120)
    tabela_emprestimos.column("col2", width=100)
    tabela_emprestimos.column("col3", width=120)

    # Identificador e entrada para valor de empréstimo
    label_valor_emprestimo = ctk.CTkLabel(tab_emprestimos, text="Valor do Empréstimo:", font=("Arial", 12), anchor="center")
    label_valor_emprestimo.pack(pady=5, padx=5)
    entry_valor_emprestimo = ctk.CTkEntry(tab_emprestimos, width=200, font=("Arial", 12), justify="center")
    entry_valor_emprestimo.pack(pady=5, padx=5)




    # Função para limitar o valor das parcelas
    def limitar_parcelas(event):
        """
        Limita o valor das parcelas no Entry para um máximo de 60.
        """
        valor = entry_parcelas.get()
        if valor.isdigit():
            numero = int(valor)
            if numero > NUMERO_MAXIMO_PARCELAS:
                entry_parcelas.delete(0, "end")
                entry_parcelas.insert(0, str(NUMERO_MAXIMO_PARCELAS))

    # Entrada para o número de parcelas
    label_parcelas = ctk.CTkLabel(tab_emprestimos, text="Número de Parcelas:", font=("Arial", 12), anchor="center")
    label_parcelas.pack(pady=5, padx=5)
    entry_parcelas = ctk.CTkEntry(tab_emprestimos, width=200, font=("Arial", 12), justify="center")
    entry_parcelas.pack(pady=5, padx=5)
    entry_parcelas.insert(0, "1")  # Começar com 1 parcela

    # Associando o evento de limitação ao campo de parcelas
    entry_parcelas.bind("<KeyRelease>", limitar_parcelas)

    


    # Aplicando validação para permitir apenas números
    validate_cmd_emprestimo = tab_emprestimos.register(validar_numeros)
    entry_valor_emprestimo.configure(validate="key", validatecommand=(validate_cmd_emprestimo, "%P"))
    entry_parcelas.configure(validate="key", validatecommand=(validate_cmd_emprestimo, "%P"))

    # Texto Dinâmico para mostrar as informações do empréstimo
    label_info_emprestimo = ctk.CTkLabel(tab_emprestimos, text="Informações do Empréstimo:", font=("Arial", 12, "italic"))
    label_info_emprestimo.pack(pady=5, padx=5)

    # Detalhes do Empréstimo
    label_detalhes_emprestimo = ctk.CTkLabel(tab_emprestimos, text="Juros: 2%\nValor da Parcela: R$ 0,00\nValor Total a Pagar: R$ 0,00", font=("Arial", 12))
    label_detalhes_emprestimo.pack(pady=5)



    ####################
    # BACKEND DO BANCO #
    # EMPRÉSTIMOS      #
    ####################


    NUMERO_MAXIMO_PARCELAS = 60  # Limite de 60 parcelas
    TAXA_JUROS_BASE = 0.08  # 8% de juros ao mês como base
    FATOR_JUROS = 0.0035  # Fator multiplicador para aumentar a taxa de juros com base nas parcelas

    # Função para quitar um empréstimo
    def quitar_emprestimo():
        selected_item = tabela_emprestimos.selection()
        if selected_item:
            idx = tabela_emprestimos.index(selected_item[0])
            dados = carregar_dados_json()
            emprestimo = dados["banco"][nome_reino]["emprestimos"][idx]
            identificador = emprestimo["identificador"]
            
            if dados["reinos"][nome_reino]["fundos"] >= emprestimo["valor_total"]:
                # Remover o valor total dos fundos do reino
                dados["reinos"][nome_reino]["fundos"] -= emprestimo["valor_total"]
                
                # Remover o empréstimo dos dados do banco
                del dados["banco"][nome_reino]["emprestimos"][idx]
                
                # Identificar e remover a dívida correspondente na contabilidade do reino
                chave_divida_base = f"divida_emprestimo_{identificador}"
                chaves_despesa = list(dados["reinos"][nome_reino]["economia"]["despesa"].keys())

                for chave in chaves_despesa:
                    if chave.startswith(chave_divida_base):
                        del dados["reinos"][nome_reino]["economia"]["despesa"][chave]
                        break  # Remover apenas a primeira correspondência encontrada

                # Atualizar os dados e a interface
                salvar_dados_json(dados)
                calcular_e_atualizar_economia()
                interface_manager.atualizar_interface(nome_reino)
                atualizar_tabela_emprestimos()
                exibir_notificacao(tab_emprestimos, "Empréstimo quitado com sucesso!", "#00FF00")
            else:
                exibir_notificacao(tab_emprestimos, "Fundos insuficientes para quitar o empréstimo!", "#FF0000")



    # Criação do menu contextual
    menu_contextual = Menu(tabela_emprestimos, tearoff=0)
    menu_contextual.add_command(label="Quitar Empréstimo", command=quitar_emprestimo)

    # Função para exibir o menu contextual
    def exibir_menu_contextual(event):
        try:
            selected_item = tabela_emprestimos.identify_row(event.y)
            tabela_emprestimos.selection_set(selected_item)
            menu_contextual.post(event.x_root, event.y_root)
        finally:
            menu_contextual.grab_release()

    # Associando o menu contextual à tabela de empréstimos
    tabela_emprestimos.bind("<Button-3>", exibir_menu_contextual)



    # Função para calcular a taxa de juros gradativa
    def calcular_taxa_juros(num_parcelas):
        return TAXA_JUROS_BASE + (FATOR_JUROS * num_parcelas)
    

    
    def calcular_maximo_emprestimo(dados_reino, dados_banco):
        """
        Calcula o valor máximo de empréstimo baseado em múltiplos fatores do reino:
        - População
        - Fundos totais
        - Quantidade total de tropas
        - Quantidade de tecnologias adquiridas
        - Dinheiro depositado na poupança

        Retorna o valor máximo disponível para empréstimo.
        """
        populacao = dados_reino["populacao"]
        fundos_totais = dados_reino["fundos"]
        tropas_totais = sum(dados_reino["tropas"].values())
        tecnologias_totais = len(dados_reino.get("tecnologias", {}))
        poupanca = dados_banco.get("poupanca", 0.0)

        # Definindo pesos para cada fator
        peso_populacao = 3.5
        peso_fundos = 0.1  # Peso reduzido para fundos, dando mais importância à poupança
        peso_tropas = 0.1
        peso_tecnologias = 2.0
        peso_poupanca = 0.5  # Peso dado à poupança

        # Calculando a contribuição de cada fator para o valor máximo de empréstimo
        contribuicao_populacao = populacao * peso_populacao
        contribuicao_fundos = fundos_totais * peso_fundos
        contribuicao_tropas = tropas_totais * peso_tropas
        contribuicao_tecnologias = tecnologias_totais * peso_tecnologias
        contribuicao_poupanca = poupanca * peso_poupanca

        # Valor máximo de empréstimo é a soma das contribuições
        maximo_emprestimo = contribuicao_populacao + contribuicao_fundos + contribuicao_tropas + contribuicao_tecnologias + contribuicao_poupanca

        # Garantir que o valor máximo de empréstimo não seja negativo
        return max(maximo_emprestimo, 0)




    # Atualizar a função para exibir as informações do empréstimo
    def simular_emprestimo():
        valor_emprestimo = float(entry_valor_emprestimo.get() or 0)
        num_parcelas = int(entry_parcelas.get() or 0)
        
        dados = carregar_dados_json()
        dados_reino = dados["reinos"][nome_reino]
        dados_banco = dados["banco"].get(nome_reino, {})

        # Passando dados_reino e dados_banco para a função calcular_maximo_emprestimo
        maximo_emprestimo = calcular_maximo_emprestimo(dados_reino, dados_banco)
        
        r = calcular_taxa_juros(num_parcelas) / 12  # Taxa de juros mensal
        if num_parcelas > 0:
            valor_parcela = round(valor_emprestimo * (r * (1 + r) ** num_parcelas) / ((1 + r) ** num_parcelas - 1), 2)
        else:
            valor_parcela = 0

        # Garantir que valor_parcela não seja menor que zero
        valor_parcela = max(valor_parcela, 0)

        valor_total = round(valor_parcela * num_parcelas, 2)

        # Garantir que valor_total não seja menor que zero
        valor_total = max(valor_total, 0)

        # Atualizar a interface em tempo real com os valores simulados
        label_detalhes_emprestimo.configure(
            text=f"Juros: {r*12*100:.2f}% ao ano\nValor da Parcela: R$ {valor_parcela:,.2f}\nValor Total a Pagar: R$ {valor_total:,.2f}\nMáximo Disponível: R$ {maximo_emprestimo:,.2f}"
        )

        return valor_parcela, valor_total, maximo_emprestimo
    
    simular_emprestimo()

    # Atualizar os valores ao digitar
    entry_valor_emprestimo.bind("<KeyRelease>", lambda event: simular_emprestimo())
    entry_parcelas.bind("<KeyRelease>", lambda event: simular_emprestimo())

    # Atualizar a função para solicitar empréstimo com a validação do valor máximo
    def solicitar_emprestimo():
        if not verificar_tecnologia_bancos(nome_reino):
            exibir_notificacao(tab_emprestimos, "Você não possui a tecnologia de Bancos!", "#FF0000")
            return

        valor_emprestimo = entry_valor_emprestimo.get().strip()
        num_parcelas = entry_parcelas.get().strip()

        # Verifica se ambos os campos estão preenchidos
        if not valor_emprestimo or not num_parcelas:
            exibir_notificacao(tab_emprestimos, "Por favor, preencha todos os campos.", "#FF0000")
            return

        # Converte os valores para float e int, respectivamente
        valor_emprestimo = float(valor_emprestimo)
        num_parcelas = int(num_parcelas)

        valor_parcela, valor_total, maximo_emprestimo = simular_emprestimo()

        # Verifica se o valor solicitado é maior que o máximo permitido
        if valor_emprestimo > maximo_emprestimo:
            exibir_notificacao(tab_emprestimos, f"Valor excede o máximo permitido!\n Máximo disponível: R$ {maximo_emprestimo:,.2f}", "#db8400")
            return

        dados = carregar_dados_json()
        identificador = gerar_identificador()

        if nome_reino not in dados["banco"]:
            dados["banco"][nome_reino] = {"poupanca": 0, "emprestimos": []}
        
        # Adicionar o empréstimo ao banco com o identificador
        dados["banco"][nome_reino]["emprestimos"].append({
            "identificador": identificador,
            "valor_emprestimo": valor_emprestimo,
            "num_parcelas": num_parcelas,
            "valor_parcela": valor_parcela,
            "valor_total": valor_total
        })

        # Adicionar o valor emprestado aos fundos do reino
        dados["reinos"][nome_reino]["fundos"] += valor_emprestimo

        # Registrar a dívida na contabilidade do reino com o identificador
        if "despesa" not in dados["reinos"][nome_reino]["economia"]:
            dados["reinos"][nome_reino]["economia"]["despesa"] = {}

        dados["reinos"][nome_reino]["economia"]["despesa"][f"divida_emprestimo_{identificador}"] = {
            "valor": valor_parcela,
            "turnos": num_parcelas
        }

        salvar_dados_json(dados)
        calcular_e_atualizar_economia()
        interface_manager.atualizar_interface(nome_reino)
        exibir_notificacao(tab_emprestimos, f"Empréstimo de R$ {valor_emprestimo:,.2f} solicitado com sucesso!", "#00FF00")
        atualizar_tabela_emprestimos()



    # Botão para solicitar o empréstimo, posicionado abaixo das informações
    botao_solicitar_emprestimo = ctk.CTkButton(tab_emprestimos, text="Solicitar Empréstimo", font=("Arial", 14), command=solicitar_emprestimo)
    botao_solicitar_emprestimo.pack(pady=10, padx=20)

    # Função para atualizar a tabela de empréstimos
    def atualizar_tabela_emprestimos():
        tabela_emprestimos.delete(*tabela_emprestimos.get_children())
        dados = carregar_dados_json()
        emprestimos = dados["banco"].get(nome_reino, {}).get("emprestimos", [])
        despesas_reino = dados["reinos"][nome_reino]["economia"]["despesa"]

        # Verificar consistência dos empréstimos
        emprestimos_validos = []
        for idx, emprestimo in enumerate(emprestimos):
            identificador = emprestimo["identificador"]
            chave_divida_base = f"divida_emprestimo_{identificador}"
            
            # Se a dívida correspondente não existir, o empréstimo é inconsistente
            if any(chave.startswith(chave_divida_base) for chave in despesas_reino.keys()):
                emprestimos_validos.append(emprestimo)
            else:
                print(f"Empréstimo {identificador} removido por falta de dívida correspondente no reino.")
        
        # Atualizar os dados do banco apenas com os empréstimos válidos
        dados["banco"][nome_reino]["emprestimos"] = emprestimos_validos
        salvar_dados_json(dados)

        # Atualizar a tabela de empréstimos na interface
        for idx, emprestimo in enumerate(emprestimos_validos, start=1):
            tabela_emprestimos.insert("", "end", values=(f"Empréstimo {idx}", emprestimo["num_parcelas"], f"R$ {emprestimo['valor_total']:,.2f}"))

    # Atualizar a tabela ao abrir a aba de empréstimos
    atualizar_tabela_emprestimos()



   
    ####################
    # BACKEND DO BANCO #
    # DEPOSITOS        #
    ####################
    def depositar_poupanca(nome_reino, valor):
        dados = carregar_dados_json()
        juros_taxa = 0.0065  # Taxa de juros de 0,65%

        if nome_reino not in dados["banco"]:
            dados["banco"][nome_reino] = {"poupanca": 0, "emprestimos": []}
        
        if dados["reinos"][nome_reino]["fundos"] < valor:
            print("Fundos insuficientes para realizar o depósito.")
            return False, "Fundos insuficientes para realizar o depósito."
        
        # Atualizar fundos do reino e valor da poupança
        dados["reinos"][nome_reino]["fundos"] -= valor
        dados["banco"][nome_reino]["poupanca"] += valor

        # Recalcular os juros com base no valor total da poupança
        nome_receita = "juros_poupanca"
        valor_juros = dados["banco"][nome_reino]["poupanca"] * juros_taxa

        # Atualizar ou criar a receita de juros da poupança
        if nome_receita in dados["reinos"][nome_reino]["economia"]["receita"]:
            dados["reinos"][nome_reino]["economia"]["receita"][nome_receita]["valor"] = valor_juros
        else:
            dados["reinos"][nome_reino]["economia"]["receita"][nome_receita] = {"valor": valor_juros, "turnos": "permanente"}

        salvar_dados_json(dados)
        calcular_e_atualizar_economia()
        print(f"Depósito de R$ {valor:,.2f} realizado com sucesso na poupança de {nome_reino}.")
        return True, f"Depósito de R$ {valor:,.2f} realizado com sucesso."


    def sacar_poupanca(nome_reino, valor):
        dados = carregar_dados_json()

        if nome_reino not in dados["banco"]:
            dados["banco"][nome_reino] = {"poupanca": 0, "emprestimos": []}
        
        if dados["banco"][nome_reino]["poupanca"] < valor:
            print("Fundos insuficientes na poupança para realizar o saque.")
            return False, "Fundos insuficientes na poupança para realizar o saque."
        
        # Atualizar valor da poupança e fundos do reino
        dados["banco"][nome_reino]["poupanca"] -= valor
        dados["reinos"][nome_reino]["fundos"] += valor

        # Recalcular os juros com base no valor total restante da poupança
        nome_receita = "juros_poupanca"
        if dados["banco"][nome_reino]["poupanca"] == 0:
            # Se todo o valor foi retirado, remover a receita de juros
            if nome_receita in dados["reinos"][nome_reino]["economia"]["receita"]:
                del dados["reinos"][nome_reino]["economia"]["receita"][nome_receita]
        else:
            novo_valor_juros = dados["banco"][nome_reino]["poupanca"] * 0.01
            dados["reinos"][nome_reino]["economia"]["receita"][nome_receita] = {"valor": novo_valor_juros, "turnos": "permanente"}

        salvar_dados_json(dados)
        calcular_e_atualizar_economia()
        print(f"Saque de R$ {valor:,.2f} realizado com sucesso da poupança de {nome_reino}.")
        return True, f"Saque de R$ {valor:,.2f} realizado com sucesso."







################################
#                              #
#  Troop Management            #
#                              #
################################
# RESUMO DO OPERADOR: Esta seção trata da gestão das tropas, incluindo recrutamento e baixa,
# com custos de manutenção e custos de recrutamento.

# Custos de manutenção e recrutamento
CUSTO_MANUTENCAO = {
    "Infantaria_Leve": 10,
    "Infantaria_Pesada": 50,
    "Infantaria_Armada": 100,
    "Blindados_Leves": 10000,
    "Blindados_Pesados": 100000,
    "Fragatas": 150000,
    "Couracados": 250000,
    "Artilharia": 50000
}

CUSTOS_RECRUTAMENTO = {
    "Infantaria Leve": 100,
    "Infantaria Pesada": 500,
    "Infantaria Armada": 1000,
    "Blindados Leves": 10000,
    "Blindados Pesados": 100000,
    "Fragatas": 150000,
    "Couracados": 250000,
    "Artilharia": 60000
}



# Atualização em tempo real do custo previsto
def atualizar_custo_previsto(movimento, entradas_tropas, label_custo_total, label_custos):
    if movimento == "Recrutamento":
        total_custo = 0
        for nome_tropa, entrada in entradas_tropas.items():
            quantia = entrada.get()
            if quantia.isdigit():
                total_custo += int(quantia) * CUSTOS_RECRUTAMENTO[nome_tropa]
        label_custo_total.configure(text=f"R$ {total_custo:,.2f}")
        label_custos.pack()  # Mostrar custo previsto
        label_custo_total.pack()  # Mostrar custo total
    else:
        label_custos.pack_forget()  # Esconder custo previsto
        label_custo_total.pack_forget()  # Esconder custo total

# Função para aplicar a movimentação das tropas
def aplicar_movimentacao_tropas(nome_reino, movimento, entradas_tropas):
    dados = carregar_dados_json()
    
    if "reinos" not in dados or nome_reino not in dados["reinos"]:
        return False, f"Reino '{nome_reino}' não encontrado!"
    
    reino = dados["reinos"][nome_reino]
    total_custo = 0

    for nome_tropa, entrada in entradas_tropas.items():
        quantia = entrada.get()
        if quantia.isdigit():
            quantia = int(quantia)
            if movimento == "Recrutamento":
                custo_tropa = quantia * CUSTOS_RECRUTAMENTO[nome_tropa]
                total_custo += custo_tropa
                if reino["fundos"] < total_custo:
                    return False, "Fundos insuficientes para recrutamento!"
                reino["tropas"][nome_tropa.replace(" ", "_")] += quantia
            elif movimento == "Baixa":
                if reino["tropas"][nome_tropa.replace(" ", "_")] >= quantia:
                    reino["tropas"][nome_tropa.replace(" ", "_")] -= quantia
                else:
                    return False, f"Não há tropas suficientes de {nome_tropa} para baixa!"

    if movimento == "Recrutamento":
        reino["fundos"] -= total_custo
        movimentar_caixa(nome_reino, "Despesa", f"Recrutamento ({quantia} {nome_tropa})", total_custo, 1)

    salvar_dados_json(dados)
    calcular_e_atualizar_economia()
    interface_manager.atualizar_interface(nome_reino)
    
    return True, f"{movimento} de tropas realizado com sucesso!"


# Função para criar campos de entrada para as tropas
def criar_campo_tropa(popup, nome_reino, nome_tropa, movimento_var, entradas_tropas, label_custo_total, label_custos):
    frame_tropa = ctk.CTkFrame(popup, fg_color="#2a2a2a", corner_radius=10)
    frame_tropa.pack(pady=5, padx=20, fill="x")
    ctk.CTkLabel(frame_tropa, text=nome_tropa, font=("Arial", 14)).pack(side="left", padx=10, pady=10)
    
    # Verificar se o reino possui a tecnologia necessária para essa tropa
    dados = carregar_dados_json()
    reino = dados["reinos"][nome_reino]
    
    # Mapeamento entre tropas e tecnologias necessárias
    tecnologias_necessarias = {
        "Infantaria Pesada": "Infantaria Pesada",
        "Infantaria Armada": "Armas de Fogo I",
        "Blindados Leves": "Blindados Leves",
        "Blindados Pesados": "Blindados Pesados",
        "Fragatas": "Fragatas",
        "Couracados": "Couracados",
        "Artilharia": "Artilharia"
    }
    
    tecnologia_requerida = tecnologias_necessarias.get(nome_tropa)

    if tecnologia_requerida and tecnologia_requerida not in reino.get("tecnologias", {}):
        # Tecnologia não desbloqueada, mostrar mensagem e desabilitar entrada
        label_bloqueio = ctk.CTkLabel(frame_tropa, text="Bloqueado: Tecnologia não disponível", font=("Arial", 12, "bold"), text_color="orange")
        label_bloqueio.pack(side="left", padx=10, fill="x", expand=True)
        return None  # Não criar campo de entrada
    else:
        entry_tropa = ctk.CTkEntry(frame_tropa, width=100, font=("Arial", 12))
        entry_tropa.pack(side="left", padx=10, fill="x", expand=True)
        
        # Adiciona a função de atualização em tempo real ao campo de entrada
        entry_tropa.bind("<KeyRelease>", lambda event: atualizar_custo_previsto(movimento_var.get(), entradas_tropas, label_custo_total, label_custos))
        
        return entry_tropa

# Atualizar a função para criar campos de tropas com base na tecnologia
def abrir_editar_tropas(nome_reino):
    dados = carregar_dados_json()

    if "reinos" not in dados or nome_reino not in dados["reinos"]:
        exibir_notificacao(None, f"Reino '{nome_reino}' não encontrado!", "#FF0000")
        return
    
    reino = dados["reinos"][nome_reino]

    popup = ctk.CTkToplevel()
    popup.title(f"Editar Tropas - {nome_reino}")
    popup.geometry("450x750")
    popup.grab_set()
    popup.iconbitmap(os.path.join(os.path.dirname(__file__), "logo.ico"))  

    label_reino = ctk.CTkLabel(popup, text=f"Reino: {nome_reino}", font=("Arial", 16, "bold"))
    label_reino.pack(pady=2)

    label_titulo = ctk.CTkLabel(popup, text="Movimentar Tropas", font=("Arial", 18, "bold"))
    label_titulo.pack(pady=10)

    movimento_var = StringVar(value="Baixa")
    frame_movimento = ctk.CTkFrame(popup, fg_color="#2a2a2a", corner_radius=10)
    frame_movimento.pack(pady=10, padx=20, fill="x")
    ctk.CTkLabel(frame_movimento, text="Movimentação:", font=("Arial", 14)).pack(side="left", padx=10, pady=10)
    ctk.CTkRadioButton(frame_movimento, text="Baixa", variable=movimento_var, value="Baixa", font=("Arial", 12)).pack(side="left", padx=5)
    ctk.CTkRadioButton(frame_movimento, text="Recrutamento", variable=movimento_var, value="Recrutamento", font=("Arial", 12)).pack(side="left", padx=5)

    label_custos = ctk.CTkLabel(popup, text="CUSTOS PREVISTOS:", font=("Arial", 14, "bold"))
    label_custos.pack(pady=10)
    label_custos.pack_forget()

    label_custo_total = ctk.CTkLabel(popup, text="R$ 0,00", font=("Arial", 14, "bold"), text_color="green")
    label_custo_total.pack(pady=5)
    label_custo_total.pack_forget()

    # Definindo entradas_tropas antes de seu uso
    entradas_tropas = {}

    # Agora criamos os campos de entrada, garantindo que apenas entradas válidas sejam adicionadas
    def adicionar_entrada_tropa(nome_tropa):
        entrada = criar_campo_tropa(popup, nome_reino, nome_tropa, movimento_var, entradas_tropas, label_custo_total, label_custos)
        if entrada:
            entradas_tropas[nome_tropa] = entrada

    adicionar_entrada_tropa("Infantaria Leve")
    adicionar_entrada_tropa("Infantaria Pesada")
    adicionar_entrada_tropa("Infantaria Armada")
    adicionar_entrada_tropa("Blindados Leves")
    adicionar_entrada_tropa("Blindados Pesados")
    adicionar_entrada_tropa("Fragatas")
    adicionar_entrada_tropa("Couracados")
    adicionar_entrada_tropa("Artilharia")

    def aplicar_movimentacao_interface():
        sucesso, mensagem = aplicar_movimentacao_tropas(nome_reino, movimento_var.get(), entradas_tropas)
        if not sucesso:
            exibir_notificacao(popup, mensagem, "#FF0000")
        else:
            exibir_notificacao(popup, mensagem, "#00FF00")

    botao_movimentar = ctk.CTkButton(popup, text="Movimentar", font=("Arial", 14), command=aplicar_movimentacao_interface)
    botao_movimentar.pack(pady=20)



################################
#                              #
#  Technology Management       #
#                              #
################################
# RESUMO DO OPERADOR: Esta seção lida com a exibição e gerenciamento das tecnologias 
# disponíveis para cada reino.


#//////////////////////////////////
#/////TECNOLOGIAS DISPONÍVEIS/////
#////////////////////////////////


# Diretório onde os ícones das tecnologias estão localizados
# Diretório onde os ícones das tecnologias estão localizados
diretorio_icones = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icones")

# Tecnologias disponíveis
tecnologias = {
    "Armadura de placas": {
        "descrição": "Aprimora a defesa das tropas com armaduras de placas básicas.",
        "custo": 325000,
        "requisitos": None,
        "turno": 0,
        "categoria": "Tecnologia",
        "icone": "armadura.png"
    },
    "Defesa I": {
        "descrição": "Aumenta a chance de defesa/esquiva em combates corpo-a-corpo.",
        "custo": 2500000,
        "requisitos": None,
        "turno": 0,
        "categoria": "Skill",
        "icone": "defesa_01.png"
    },
    "Defesa II": {
        "descrição": "Melhora a chance de defesa/esquiva em combates corpo-a-corpo.",
        "custo": 6500000,
        "requisitos": "Defesa I",
        "turno": 5,
        "categoria": "Skill",
        "icone": "defesa_02.png"
    },
    "Defesa III": {
        "descrição": "Fortalece significativamente a defesa/esquiva em combates corpo-a-corpo.",
        "custo": 15000000,
        "requisitos": "Defesa II",
        "turno": 10,
        "categoria": "Skill",
        "icone": "defesa_03.png"
    },
    "Defesa IV": {
        "descrição": "Alcança a maestria em defesa e esquiva com habilidade refinada.",
        "custo": 45000000,
        "requisitos": "Defesa III",
        "turno": 15,
        "categoria": "Skill",
        "icone": "defesa_04.png"
    },
    "Defesa V": {
        "descrição": "Domina técnicas avançadas de defesa e esquiva, antecipando os movimentos do inimigo para minimizar danos em combate.",
        "custo": 70000000,
        "requisitos": "Defesa IV",
        "turno": 20,
        "categoria": "Skill",
        "icone": "defesa_05.png"
    },
    "Defesa VI": {
        "descrição": "A defesa definitiva. Torna-se praticamente impenetrável.",
        "custo": 100000000,
        "requisitos": "Defesa V",
        "turno": 25,
        "categoria": "Skill",
        "icone": "defesa_06.png"
    },
    "Armas de Fogo I": {
        "descrição": "Introduz armas de fogo antigas ao exército.",
        "custo": 100000000,
        "requisitos": None,
        "turno": 200,
        "categoria": "Tecnologia",
        "icone": "firearms.png"
    },
    "Bancos": {
        "descrição": "Permite acesso e investimentos em bancos.",
        "custo": 750000,
        "requisitos": None,
        "turno": 5,
        "categoria": "Finanças",
        "icone": "bank.png"
    },
    "Infantaria Pesada": {
        "descrição": "Desbloqueia o treinamento de tropas de Infantaria Pesada.",
        "custo": 500000,
        "requisitos": "Armadura de placas",
        "turno": 0,
        "categoria": "Tropas",
        "icone": "inf_heavy.png"
    },
    "Engenharia": {
        "descrição": "Habilita a construção de veículos e máquinas.",
        "custo": 100000000,
        "requisitos": None,
        "turno": 250,
        "categoria": "Tecnologia",
        "icone": "engenharia.png"
    },
    "Engenharia Naval": {
        "descrição": "Especializa-se na construção de navios.",
        "custo": 5500000,
        "requisitos": None,
        "turno": 25,
        "categoria": "Tecnologia",
        "icone": "eng_nav.png"
    },
    "Blindados Leves": {
        "descrição": "Desbloqueia a produção de Blindados Leves.",
        "custo": 50000000,
        "requisitos": "Engenharia",
        "turno": 200,
        "categoria": "Tropas",
        "icone": "blindados_leves.png"
    },
    "Blindados Pesados": {
        "descrição": "Desbloqueia a produção de Blindados Pesados.",
        "custo": 10000000,
        "requisitos": "Blindados Leves",
        "turno": 250,
        "categoria": "Tropas",
        "icone": "blindados_pesados.png"
    },
    "Fragatas": {
        "descrição": "Desbloqueia a construção de Fragatas navais.",
        "custo": 3000000,
        "requisitos": "Engenharia Naval",
        "turno": 25,
        "categoria": "Tropas",
        "icone": "fragatas.png"
    },
    "Couracados": {
        "descrição": "Desbloqueia a construção de Navios Couraçados.",
        "custo": 75000000,
        "requisitos": "Fragatas",
        "turno": 200,
        "categoria": "Tropas",
        "icone": "couracados.png"
    },
    "Artilharia": {
        "descrição": "Desbloqueia a produção de Artilharia pesada.",
        "custo": 2500000,
        "requisitos": "Engenharia",
        "turno": 150,
        "categoria": "Tropas",
        "icone": "artilharia.png"
    },
    "Armas Modernas": {
        "descrição": "Desbloqueia o uso de armas de fogo modernas.",
        "custo": 100000000,
        "requisitos": ["Engenharia", "Armas de Fogo I"],
        "turno": 300,
        "categoria": "Tecnologia",
        "icone": "firearms_modern.png"
    },
    "Armaduras Modulares": {
        "descrição": "Desbloqueia a produção de armaduras balísticas modulares.",
        "custo": 75000000,
        "requisitos": ["Armas de Fogo I", "Armadura de placas"],
        "turno": 200,
        "categoria": "Tecnologia",
        "icone": "balistic_armor.png"
    },
    "Torres I": {
        "descrição": "Constrói torres básicas de defesa.",
        "custo": 50000,
        "requisitos": None,
        "turno": 0,
        "categoria": "Tecnologia",
        "icone": "torres_I.png"
    },
    "Torres II": {
        "descrição": "Constrói torres de defesa reforçadas.",
        "custo": 5000000,
        "requisitos": "Torres I",
        "turno": 25,
        "categoria": "Tecnologia",
        "icone": "torres_II.png"
    },
    "Torres III": {
        "descrição": "Constrói torres de defesa altamente resistentes.",
        "custo": 10000000,
        "requisitos": "Torres II",
        "turno": 75,
        "categoria": "Tecnologia",
        "icone": "torres_III.png"
    },
    "Bandagem": {
        "descrição": "Disponibiliza bandagens médicas para as tropas.",
        "custo": 250000,
        "requisitos": None,
        "turno": 0,
        "categoria": "Skill",
        "icone": "bandagem.png"
    },
    "Granadas": {
        "descrição": "Desbloqueia o uso de granadas de mão pelas tropas.",
        "custo": 2000000,
        "requisitos": "Armas de Fogo I",
        "turno": 175,
        "categoria": "Skill",
        "icone": "granadas.png"
    },
    "Armamento Anti-Tanque": {
        "descrição": "Desbloqueia armamento especializado para combate contra tanques.",
        "custo": 3500000,
        "requisitos": "Armas Modernas",
        "turno": 275,
        "categoria": "Skill",
        "icone": "antitank.png"
    },
    "Proeficiencia I": {
        "descrição": "Aumenta a chance de ataque em 5%.",
        "custo": 1000000,
        "requisitos": None,
        "turno": 0,
        "categoria": "Skill",
        "icone": "proeficiencia_01.png"
    },
    "Proeficiencia II": {
        "descrição": "Aumenta a chance de ataque em 12%.",
        "custo": 20000000,
        "requisitos": "Proeficiencia I",
        "turno": 5,
        "categoria": "Skill",
        "icone": "proeficiencia_02.png"
    },
    "Proeficiencia III": {
        "descrição": "Aumenta a chance de ataque em 25%.",
        "custo": 50000000,
        "requisitos": "Proeficiencia II",
        "turno": 10,
        "categoria": "Skill",
        "icone": "proeficiencia_03.png"
    },
    "Proeficiencia IV": {
        "descrição": "Aumenta a chance de ataque em 35%.",
        "custo": 150000000,
        "requisitos": "Proeficiencia III",
        "turno": 15,
        "categoria": "Skill",
        "icone": "proeficiencia_04.png"
    },
    "Proeficiencia V": {
        "descrição": "Aumenta a chance de ataque em 50%.",
        "custo": 350000000,
        "requisitos": "Proeficiencia IV",
        "turno": 20,
        "categoria": "Skill",
        "icone": "proeficiencia_05.png"
    },
    "Proeficiencia VI": {
        "descrição": "Aprimora ao máximo as habilidades ofensivas, permitindo ataques rápidos e precisos.",
        "custo": 500000000,
        "requisitos": "Proeficiencia V",
        "turno": 25,
        "categoria": "Skill",
        "icone": "proeficiencia_06.png"
    },
    "Fazendas I": {
        "descrição": "Investimento básico em fazendas para gerar lucro constante.",
        "custo": 850000,
        "requisitos": None,
        "turno": 0,
        "categoria": "Finanças",
        "icone": "fazendas_01.png"
    },
    "Fazendas II": {
        "descrição": "Expande as fazendas para aumentar o lucro gerado.",
        "custo": 25000000,
        "requisitos": "Fazendas I",
        "turno": 25,
        "categoria": "Finanças",
        "icone": "fazendas_02.png"
    },
    "Fazendas III": {
        "descrição": "Desenvolve uma extensa rede de fazendas altamente lucrativas.",
        "custo": 50000000,
        "requisitos": "Fazendas II",
        "turno": 50,
        "categoria": "Finanças",
        "icone": "fazendas_03.png"
    },
    "Fazendas IV": {
        "descrição": "Implementa técnicas agrícolas avançadas, maximizando a produção e garantindo a sustentabilidade econômica.",
        "custo": 100000000,
        "requisitos": "Fazendas III",
        "turno": 75,
        "categoria": "Finanças",
        "icone": "fazendas_04.png"
    },
    "Industrias I": {
        "descrição": "Investimento básico em indústrias para aumentar o lucro do reino.",
        "custo": 25000000,
        "requisitos": None,
        "turno": 50,
        "categoria": "Finanças",
        "icone": "industrias_01.png"
    },
    "Industrias II": {
        "descrição": "Expande as indústrias para gerar maior lucro.",
        "custo": 75000000,
        "requisitos": "Industrias I",
        "turno": 100,
        "categoria": "Finanças",
        "icone": "industrias_02.png"
    },
    "Industrias III": {
        "descrição": "Desenvolve uma infraestrutura industrial poderosa e altamente lucrativa.",
        "custo": 150000000,
        "requisitos": "Industrias II",
        "turno": 150,
        "categoria": "Finanças",
        "icone": "industrias_03.png"
    },
    "Industrias IV": {
        "descrição": "Revolução industrial total, otimizando ao máximo a produção e garantindo a hegemonia econômica.",
        "custo": 300000000,
        "requisitos": "Industrias III",
        "turno": 200,
        "categoria": "Finanças",
        "icone": "industrias_04.png"
    },
    "Cercos I": {
        "descrição": "Desenvolve torres de cerco básicas.",
        "custo": 500000,
        "requisitos": None,
        "turno": 20,
        "categoria": "Tecnologia",
        "icone": "cerco_01.png"
    },
    "Cercos II": {
        "descrição": "Aprimora as técnicas de cerco com aríetes reforçados.",
        "custo": 15000000,
        "requisitos": "Cercos I",
        "turno": 50,
        "categoria": "Tecnologia",
        "icone": "cerco_02.png"
    },
    "Cercos III": {
        "descrição": "Introduz artilharia pesada para demolir fortificações.",
        "custo": 45000000,
        "requisitos": "Cercos II",
        "turno": 100,
        "categoria": "Tecnologia",
        "icone": "cerco_03.png"
    }
}




def carregar_tecnologias_disponiveis(nome_reino, turno_atual):
    dados = carregar_dados_json()
    reino = dados["reinos"][nome_reino]
    tecnologias_compradas = reino.get("tecnologias", {})

    tecnologias_disponiveis = []
    tecnologias_bloqueadas = []
    tecnologias_pesquisadas = {}

    for nome, info in tecnologias.items():
        if nome in tecnologias_compradas:
            tecnologias_pesquisadas[nome] = info
        else:
            requisitos_nao_atendidos = []
            requisitos = info.get("requisitos")
            if requisitos:
                if isinstance(requisitos, list):
                    requisitos_nao_atendidos = [requisito for requisito in requisitos if requisito not in tecnologias_compradas]
                else:
                    requisitos_nao_atendidos = [requisitos] if requisitos not in tecnologias_compradas else []

            if requisitos_nao_atendidos or info.get("turno", 0) > turno_atual:
                tecnologias_bloqueadas.append((nome, info, requisitos_nao_atendidos))
            else:
                tecnologias_disponiveis.append((nome, info))

    # Ordenar por disponibilidade (disponíveis primeiro, bloqueadas depois)
    tecnologias_disponiveis.sort(key=lambda x: x[1]['custo'])
    tecnologias_bloqueadas.sort(key=lambda x: x[1]['custo'])

    return tecnologias_disponiveis + tecnologias_bloqueadas, tecnologias_pesquisadas



def desenvolver_tecnologia(tecnologia_info, nome_reino, nome_tecnologia, popup_tecnologias, tabview_tecnologias, turno_atual):
    dados = carregar_dados_json()
    reino = dados["reinos"][nome_reino]

    custo_tecnologia = tecnologia_info['custo']
    turno_minimo = tecnologia_info.get('turno', 0)

    # Verificar se o turno atual é suficiente para desenvolver a tecnologia
    if turno_atual < turno_minimo:
        exibir_notificacao(popup_tecnologias, f"Tecnologia disponível a partir do turno {turno_minimo}.", "#9370DB")  # Cor roxa clara
        return

    # Verificar fundos suficientes
    if reino['fundos'] < custo_tecnologia:
        exibir_notificacao(popup_tecnologias, "Fundos insuficientes!", "#FF0000")
        return

    # Deduzir os fundos do reino e adicionar a tecnologia pelo nome
    reino['fundos'] -= custo_tecnologia
    if "tecnologias" not in reino:
        reino['tecnologias'] = {}

    # Adiciona a tecnologia como uma chave no dicionário, marcando-a como adquirida
    reino['tecnologias'][nome_tecnologia] = True  # Indica que a tecnologia foi adquirida

    # Salvar os dados atualizados
    salvar_dados_json(dados)

    # Atualizar a interface para refletir a compra e atualizar as tecnologias
    interface_manager.atualizar_interface(nome_reino)
    atualizar_tecnologias(popup_tecnologias, tabview_tecnologias, nome_reino, turno_atual)
    exibir_notificacao(popup_tecnologias, "Tecnologia adquirida com sucesso!", "#397a00")


def atualizar_tecnologias(popup_tecnologias, tabview_tecnologias, nome_reino, turno_atual):
    """
    Atualiza o conteúdo do popup com as tecnologias disponíveis e pesquisadas.
    """
    # Remover o antigo Tabview
    tabview_tecnologias.pack_forget()
    tabview_tecnologias.destroy()

    # Criar um novo Tabview
    tabview_tecnologias = ctk.CTkTabview(popup_tecnologias, width=580, height=400)
    tabview_tecnologias.pack(pady=10, padx=10, fill="both", expand=True)

    tecnologias_disponiveis, tecnologias_pesquisadas = carregar_tecnologias_disponiveis(nome_reino, turno_atual)
    dados = carregar_dados_json()
    reino = dados["reinos"][nome_reino]

    categorias = {}

    # Adicionar tecnologias pesquisadas
    if tecnologias_pesquisadas:
        tab_categoria_pesquisadas = tabview_tecnologias.add("Tecnologias Pesquisadas")
        frame_categoria_pesquisadas = ctk.CTkScrollableFrame(tab_categoria_pesquisadas)
        frame_categoria_pesquisadas.pack(fill="both", expand=True)

        for nome, info in tecnologias_pesquisadas.items():
            frame_tecnologia = ctk.CTkFrame(frame_categoria_pesquisadas, corner_radius=8)
            frame_tecnologia.pack(pady=10, padx=10, fill="x", expand=True)

            carregar_detalhes_tecnologia(nome, info, frame_tecnologia)

            label_adquirida = ctk.CTkLabel(frame_tecnologia, text="Tecnologia já adquirida", font=("Arial", 14), text_color="green")
            label_adquirida.pack(pady=2)

    # Adicionar tecnologias disponíveis e bloqueadas
    for nome, info, *requisitos_nao_atendidos in tecnologias_disponiveis:
        categoria = info["categoria"]
        if categoria not in categorias:
            tab_categoria = tabview_tecnologias.add(categoria)
            frame_categoria = ctk.CTkScrollableFrame(tab_categoria)
            frame_categoria.pack(fill="both", expand=True)
            categorias[categoria] = frame_categoria
        else:
            frame_categoria = categorias[categoria]

        frame_tecnologia = ctk.CTkFrame(frame_categoria, corner_radius=8)
        frame_tecnologia.pack(pady=10, padx=10, fill="x", expand=True)

        carregar_detalhes_tecnologia(nome, info, frame_tecnologia)

        turno_minimo = info.get('turno', 0)
        if requisitos_nao_atendidos or turno_minimo > turno_atual:
            if turno_minimo > turno_atual:
                label_turno = ctk.CTkLabel(frame_tecnologia, text=f"Disponível a partir do turno {turno_minimo}", font=("Arial", 14), text_color="#9370DB")  # Cor roxa clara
                label_turno.pack(pady=2)
            if requisitos_nao_atendidos:
                requisitos_texto = ", ".join(requisitos_nao_atendidos[0])
                label_requisitos = ctk.CTkLabel(frame_tecnologia, text=f"Requisitos não atendidos: {requisitos_texto}", font=("Arial", 14), text_color="orange")
                label_requisitos.pack(pady=2)
        else:
            if reino['fundos'] < info['custo']:
                label_custo = ctk.CTkLabel(
                    frame_tecnologia,
                    text=f"Custo: R$ {info['custo']:,}",
                    font=("Arial", 14, "bold"),
                    text_color="red"
                )
                label_custo.pack(pady=2)
            else:
                label_custo = ctk.CTkLabel(frame_tecnologia, text=f"Custo: R$ {info['custo']:,}", font=("Arial", 14))
                label_custo.pack(pady=2)

                botao_desenvolver = ctk.CTkButton(frame_tecnologia, text="Pesquisar Tecnologia")
                botao_desenvolver.pack(pady=5)

                botao_desenvolver.configure(command=lambda info=info, nome=nome: desenvolver_tecnologia(info, nome_reino, nome, popup_tecnologias, tabview_tecnologias, turno_atual))

    # Certificar que o botão de fechar está presente e corretamente posicionado
    if not hasattr(popup_tecnologias, "botao_fechar"):
        popup_tecnologias.botao_fechar = ctk.CTkButton(popup_tecnologias, text="Fechar", command=popup_tecnologias.destroy)
    popup_tecnologias.botao_fechar.pack_forget()
    popup_tecnologias.botao_fechar.pack(pady=10, side="bottom")




def carregar_turno_atual():
    dados = carregar_dados_json()
    return dados.get("turno_atual", 1)  # Padrão é 1 caso não exista

def abrir_tecnologias(nome_reino, popup_tecnologias=None):
    """
    Abre a interface para exibir as tecnologias do reino, sempre carregando o turno atual.
    """
    turno_atual = carregar_turno_atual()

    if popup_tecnologias is not None:
        popup_tecnologias.destroy()

    # Criação do popup para a interface de tecnologias
    popup_tecnologias = ctk.CTkToplevel()
    popup_tecnologias.title(f"Tecnologias - {nome_reino}")
    popup_tecnologias.geometry("600x600")
    popup_tecnologias.grab_set()  # Mantém o popup no topo
    popup_tecnologias.iconbitmap(os.path.join(os.path.dirname(__file__), "logo.ico"))

    # Título do popup
    label_titulo = ctk.CTkLabel(popup_tecnologias, text=f"Tecnologias de {nome_reino}", font=("Arial", 18, "bold"))
    label_titulo.pack(pady=10)

    # Criação do Tabview
    tabview_tecnologias = ctk.CTkTabview(popup_tecnologias, width=580, height=400)
    tabview_tecnologias.pack(pady=10, padx=10, fill="both", expand=True)

    # Carregar as tecnologias inicialmente
    atualizar_tecnologias(popup_tecnologias, tabview_tecnologias, nome_reino, turno_atual)




def carregar_detalhes_tecnologia(nome, info, frame_tecnologia):
    # Verificação e carregamento do ícone da tecnologia
    caminho_icone = os.path.join(diretorio_icones, info["icone"])
    if os.path.exists(caminho_icone):
        try:
            imagem = Image.open(caminho_icone)
            icone_tecnologia = ctk.CTkImage(imagem, size=(64, 64))
            label_icone = ctk.CTkLabel(frame_tecnologia, image=icone_tecnologia, text="")
            label_icone.pack(pady=5)
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")
            label_erro = ctk.CTkLabel(frame_tecnologia, text="Erro ao carregar a imagem.", font=("Arial", 14), text_color="red")
            label_erro.pack(pady=5)
    else:
        print(f"Arquivo de ícone não encontrado: {caminho_icone}")
        label_erro = ctk.CTkLabel(frame_tecnologia, text="Ícone não encontrado.", font=("Arial", 14), text_color="red")
        label_erro.pack(pady=5)

    label_nome = ctk.CTkLabel(frame_tecnologia, text=nome, font=("Arial", 16, "bold"))
    label_nome.pack(pady=2)

    label_descricao = ctk.CTkLabel(frame_tecnologia, text=info["descrição"], font=("Arial", 14), wraplength=400)
    label_descricao.pack(pady=2)


################################
#                              #
#  End of Code                 #
#                              #
################################
