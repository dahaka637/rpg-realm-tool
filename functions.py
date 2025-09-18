#XXXXXXXXXXXXXXXXXXXXXXXXXXXX
#XX COMEÇO DO FUNCTIONS.PY XX
#XXXXXXXXXXXXXXXXXXXXXXXXXXXX
import json
import os
import random
from PIL import Image
import customtkinter as ctk
from tkinter import ttk

################################
#                              #
#      File Operations         #
#                              #
################################
# RESUMO DO OPERADOR: Esta seção lida com as operações de arquivo, como carregar e salvar dados em JSON, 
# e garantir que o arquivo de dados seja inicializado corretamente.

def carregar_dados_json():
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'dados', 'dados.json')

    if not os.path.exists(caminho_arquivo):
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
        dados_iniciais = {
            "turno_atual": 1,
            "reinos": {},
            "banco": {}
        }
        with open(caminho_arquivo, 'w') as arquivo:
            json.dump(dados_iniciais, arquivo, indent=4)
        print(f"Arquivo {caminho_arquivo} criado com conteúdo inicial.")

    with open(caminho_arquivo, 'r') as arquivo:
        dados = json.load(arquivo)
    
    # Garantir que o banco esteja presente nos dados
    if "banco" not in dados:
        dados["banco"] = {}

    # Verifique se todas as tropas, incluindo Artilharia, estão presentes
    for reino in dados.get("reinos", {}).values():
        if "tropas" in reino:
            if "Artilharia" not in reino["tropas"]:
                reino["tropas"]["Artilharia"] = 0

    return dados




def salvar_dados_json(dados):
    """
    Salva os dados fornecidos no arquivo JSON.
    """
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'dados', 'dados.json')
    with open(caminho_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

################################
#                              #
#    Kingdom Management        #
#                              #
################################
# RESUMO DO OPERADOR: Esta seção cuida da criação e exclusão de reinos no jogo. 
# Inclui a inicialização de valores como população, tropas e economia.

def criar_reino(nome_reino, populacao_inicial):
    dados = carregar_dados_json()

    fundos_iniciais = round(populacao_inicial * random.uniform(0.01, 10.0), 2)

    novo_reino = {
        "populacao": populacao_inicial,
        "tropas": {
            "Infantaria_Leve": 0,
            "Infantaria_Pesada": 0,
            "Infantaria_Armada": 0,
            "Blindados_Leves": 0,
            "Blindados_Pesados": 0,
            "Fragatas": 0,
            "Couracados": 0,
            "Artilharia": 0  # Nova tropa
        },
        "fundos": fundos_iniciais,
        "economia": {
            "receita": {
                "receita_populacional": {
                    "valor": 0,
                    "turnos": "permanente"
                }
            },
            "despesa": {
                "manutencao_exercito": {
                    "valor": 0,
                    "turnos": "permanente"
                }
            }
        },
        "tecnologias": {},
        "fundos_previstos": 0.0
    }

    # Inicializar dados do banco para o novo reino
    if "banco" not in dados:
        dados["banco"] = {}

    dados["banco"][nome_reino] = {"poupanca": 0, "emprestimos": []}

    dados["reinos"][nome_reino] = novo_reino
    salvar_dados_json(dados)
    calcular_e_atualizar_economia()
    print(f"Reino '{nome_reino}' criado com sucesso com {fundos_iniciais} unidades de fundo inicial.")



def excluir_reino(nome_reino):
    dados = carregar_dados_json()
    if "reinos" in dados and nome_reino in dados["reinos"]:
        del dados["reinos"][nome_reino]
        salvar_dados_json(dados)

def atualizar_reino(nome_reino_atual, novo_nome, nova_populacao):
    """
    Atualiza os dados do reino existente.
    """
    dados = carregar_dados_json()

    if nome_reino_atual in dados["reinos"]:
        reino = dados["reinos"][nome_reino_atual]
        reino["populacao"] = nova_populacao
        if nome_reino_atual != novo_nome:
            dados["reinos"][novo_nome] = dados["reinos"].pop(nome_reino_atual)
        salvar_dados_json(dados)
        calcular_e_atualizar_economia()

################################
#                              #
#  Economic Calculations       #
#                              #
################################
# RESUMO DO OPERADOR: Esta seção é responsável por calcular e atualizar a economia dos reinos, 
# incluindo manutenção de tropas e previsão de fundos.

# Tabela de custos de manutenção para diferentes tipos de tropas
CUSTO_MANUTENCAO = {
    "Infantaria_Leve": 10,
    "Infantaria_Pesada": 50,
    "Infantaria_Armada": 100,
    "Blindados_Leves": 10000,
    "Blindados_Pesados": 8000,
    "Fragatas": 5000,
    "Couracados": 10000,
    "Artilharia": 1000
}

def calcular_e_atualizar_economia():
    dados = carregar_dados_json()
    alterado = False

    if "reinos" in dados:
        for nome_reino, reino in dados["reinos"].items():
            # Verificar se a receita populacional já existe
            if "receita_populacional" not in reino["economia"]["receita"]:
                # Gerar um fator aleatório entre 0.45 e 0.55
                fator_aleatorio = random.uniform(0.48, 0.52)
                
                # Calcular a receita populacional usando o fator aleatório
                receita_populacional = reino.get("populacao", 0) * fator_aleatorio
                reino["economia"]["receita"]["receita_populacional"] = {
                    "valor": receita_populacional,
                    "turnos": "permanente"
                }
                alterado = True  # Marcar como alterado se a receita populacional foi calculada

            manutencao_exercito = sum(
                reino["tropas"].get(tropa, 0) * CUSTO_MANUTENCAO.get(tropa, 0)
                for tropa in reino["tropas"]
            )

            if "manutencao_exercito" in reino["economia"]["despesa"]:
                reino["economia"]["despesa"]["manutencao_exercito"]["valor"] = manutencao_exercito
                alterado = True  # Marcar como alterado se a manutenção do exército foi calculada

            # Atualizar juros da poupança
            nome_receita = "Juros da Poupança"
            if nome_reino in dados["banco"]:
                valor_poupanca = dados["banco"][nome_reino]["poupanca"]
                valor_juros = valor_poupanca * 0.01
                if nome_receita in reino["economia"]["receita"]:
                    reino["economia"]["receita"][nome_receita]["valor"] = valor_juros
                    alterado = True  # Marcar como alterado se os juros foram calculados

            total_receitas = sum(receita["valor"] for receita in reino["economia"]["receita"].values())
            total_despesas = sum(despesa["valor"] for despesa in reino["economia"]["despesa"].values())
            total_previsto = total_receitas - total_despesas

            reino["fundos_previstos"] = total_previsto
            alterado = True  # Marcar como alterado se os fundos previstos foram calculados

    if alterado:
        salvar_dados_json(dados)
        print("Dados econômicos atualizados com sucesso.")




################################
#                              #
#  Turn Management             #
#                              #
################################
# RESUMO DO OPERADOR: Esta seção gerencia o avanço dos turnos no jogo, atualizando receitas, despesas 
# e fundos dos reinos a cada turno.


def processar_investimentos(nome_reino, reino):
    """
    Processa os investimentos em fazendas e indústrias para o reino, 
    calculando receitas baseadas na população e atualizando a economia do reino.
    """
    receitas_atuais = reino["economia"]["receita"]

    # Fatores de lucro baseados na população
    fator_fazendas = 0.01  # Base de 1% da população para fazendas
    fator_industrias = 0.03  # Base de 3% da população para indústrias

    # Configuração de aleatoriedade (faixa de multiplicadores)
    variacao_aleatoria_fazendas_n1 = (0.2, 1.5)
    variacao_aleatoria_fazendas_n2 = (0.5, 1.8)
    variacao_aleatoria_fazendas_n3 = (1.0, 2.0)
    variacao_aleatoria_fazendas_n4 = (2.8, 3.5)  # Nova variação para Fazendas IV

    variacao_aleatoria_industrias_n1 = (0.3, 1.6)
    variacao_aleatoria_industrias_n2 = (0.7, 1.9)
    variacao_aleatoria_industrias_n3 = (1.5, 2.5)
    variacao_aleatoria_industrias_n4 = (3.0, 4.8)  # Nova variação para Indústrias IV

    # Verificar e processar os investimentos em fazendas
    if "Fazendas IV" in reino["tecnologias"]:
        valor_fazendas = reino["populacao"] * fator_fazendas * 4 * random.uniform(*variacao_aleatoria_fazendas_n4)
        receitas_atuais["Receita Fazendas"] = {"valor": valor_fazendas, "turnos": "permanente"}
    elif "Fazendas III" in reino["tecnologias"]:
        valor_fazendas = reino["populacao"] * fator_fazendas * 3 * random.uniform(*variacao_aleatoria_fazendas_n3)
        receitas_atuais["Receita Fazendas"] = {"valor": valor_fazendas, "turnos": "permanente"}
    elif "Fazendas II" in reino["tecnologias"]:
        valor_fazendas = reino["populacao"] * fator_fazendas * 2 * random.uniform(*variacao_aleatoria_fazendas_n2)
        receitas_atuais["Receita Fazendas"] = {"valor": valor_fazendas, "turnos": "permanente"}
    elif "Fazendas I" in reino["tecnologias"]:
        valor_fazendas = reino["populacao"] * fator_fazendas * random.uniform(*variacao_aleatoria_fazendas_n1)
        receitas_atuais["Receita Fazendas"] = {"valor": valor_fazendas, "turnos": "permanente"}

    # Verificar e processar os investimentos em indústrias
    if "Industrias IV" in reino["tecnologias"]:
        valor_industrias = reino["populacao"] * fator_industrias * 4 * random.uniform(*variacao_aleatoria_industrias_n4)
        receitas_atuais["Receita Industrias"] = {"valor": valor_industrias, "turnos": "permanente"}
    elif "Industrias III" in reino["tecnologias"]:
        valor_industrias = reino["populacao"] * fator_industrias * 3 * random.uniform(*variacao_aleatoria_industrias_n3)
        receitas_atuais["Receita Industrias"] = {"valor": valor_industrias, "turnos": "permanente"}
    elif "Industrias II" in reino["tecnologias"]:
        valor_industrias = reino["populacao"] * fator_industrias * 2 * random.uniform(*variacao_aleatoria_industrias_n2)
        receitas_atuais["Receita Industrias"] = {"valor": valor_industrias, "turnos": "permanente"}
    elif "Industrias I" in reino["tecnologias"]:
        valor_industrias = reino["populacao"] * fator_industrias * random.uniform(*variacao_aleatoria_industrias_n1)
        receitas_atuais["Receita Industrias"] = {"valor": valor_industrias, "turnos": "permanente"}

    # Atualizar as receitas no reino
    reino["economia"]["receita"] = receitas_atuais





def verificar_e_inicializar_turno():
    """
    Verifica se o turno atual está inicializado no JSON, e se não estiver, inicializa-o.
    """
    dados = carregar_dados_json()
    if "turno_atual" not in dados:
        dados["turno_atual"] = 1
        salvar_dados_json(dados)





def processar_rolagem_de_turno():
    dados = carregar_dados_json()
    turno_atual = dados.get("turno_atual", 1)
    turno_atual += 1
    dados["turno_atual"] = turno_atual

    if "reinos" in dados:
        for nome_reino, reino in dados["reinos"].items():
            # Atualizar receita populacional com um valor aleatório entre 0.48 e 0.52
            taxa_populacional = random.uniform(0.48, 0.52)
            receita_populacional = reino.get("populacao", 0) * taxa_populacional
            reino["economia"]["receita"]["receita_populacional"]["valor"] = receita_populacional

            # Primeiro, aplique todas as receitas e despesas ao fundo do reino
            for tipo in ["receita", "despesa"]:
                entradas = reino["economia"].get(tipo, {})
                for descricao, detalhes in list(entradas.items()):
                    valor = detalhes["valor"]

                    if tipo == "receita":
                        # Aplicar receita ao fundo do reino
                        reino["fundos"] += valor

                    elif tipo == "despesa":
                        # Verificar se é uma dívida de empréstimo
                        if descricao.startswith("divida_emprestimo_"):
                            identificador = descricao.split("_")[2]  # Extrai o identificador único do empréstimo

                            if reino["fundos"] >= valor:
                                # Se o reino tiver fundos suficientes, descontar normalmente
                                reino["fundos"] -= valor
                            else:
                                # Se não houver fundos suficientes, aplicar juros de 8%
                                juros = valor * 0.08
                                novo_valor = valor + juros
                                detalhes["valor"] = novo_valor

                                # Exibir uma notificação ou registrar que o pagamento foi postergado
                                print(f"Reino '{nome_reino}' não tinha fundos suficientes para pagar a parcela de R$ {valor:.2f}. Juros de 8% aplicados. Novo valor da parcela: R$ {novo_valor:.2f}. Número de parcelas restantes: {detalhes['turnos']}")

                            # Verificar se é a última parcela antes de removê-la
                            if detalhes["turnos"] == 1:
                                # Contabilizar a última parcela antes de removê-la
                                reino["fundos"] -= valor
                                print(f"Reino '{nome_reino}' pagou a última parcela do empréstimo de R$ {valor:.2f}.")
                                # Remover a dívida após o pagamento
                                del entradas[descricao]
                            else:
                                # Reduzir o número de parcelas restantes
                                detalhes["turnos"] -= 1
                                # Atualizar a descrição da dívida para refletir o número de parcelas restantes
                                nova_descricao = f"divida_emprestimo_{identificador}_{detalhes['turnos']}_parcelas"
                                entradas[nova_descricao] = entradas.pop(descricao)

                        else:
                            # Descontar normalmente as outras despesas
                            reino["fundos"] -= valor

                    # Processar a rolagem de turnos para entradas não permanentes que não sejam de empréstimos
                    if detalhes["turnos"] != "permanente" and not descricao.startswith("divida_emprestimo_"):
                        detalhes["turnos"] -= 1
                        if detalhes["turnos"] <= 0:
                            # Remover a entrada da despesa
                            del entradas[descricao]
                        else:
                            nova_descricao = f"{descricao.split(' (')[0]} ({detalhes['turnos']} parcelas)"
                            entradas[nova_descricao] = entradas.pop(descricao)

            # Processar os investimentos
            processar_investimentos(nome_reino, reino)

            # Recalcular o total previsto após aplicar receitas e despesas
            total_receitas = sum(receita["valor"] for receita in reino["economia"]["receita"].values())
            total_despesas = sum(despesa["valor"] for despesa in reino["economia"]["despesa"].values())
            total_previsto = total_receitas - total_despesas

            reino["fundos_previstos"] = total_previsto
            reino["fundos"] += total_previsto

    salvar_dados_json(dados)
    return turno_atual













################################
#                              #
#  Interface Management        #
#                              #
################################
# RESUMO DO OPERADOR: Esta seção gerencia a interface gráfica, atualizando os componentes baseados nos dados 
# carregados ou quando não há reinos disponíveis.

class InterfaceManager:
    def __init__(self):
        self.seletor_reino = None
        self.label_populacao = None
        self.labels_tropas = []
        self.tabela_economia = None
        self.label_valor_fundos = None
        self.label_valor_esperado = None
        self.frame_tecnologias = None
        self.seletor_reino_esquerdo = None
        self.seletor_reino_direito = None
        self.on_select_reino_esquerdo = None 
        self.on_select_reino_direito = None

    def registrar_componentes(self, seletor_reino, label_populacao, labels_tropas, tabela_economia, label_valor_fundos, label_valor_esperado, frame_tecnologias, seletor_reino_esquerdo, seletor_reino_direito, on_select_reino_esquerdo, on_select_reino_direito):
        self.seletor_reino = seletor_reino
        self.label_populacao = label_populacao
        self.labels_tropas = labels_tropas
        self.tabela_economia = tabela_economia
        self.label_valor_fundos = label_valor_fundos
        self.label_valor_esperado = label_valor_esperado
        self.frame_tecnologias = frame_tecnologias
        self.seletor_reino_esquerdo = seletor_reino_esquerdo
        self.seletor_reino_direito = seletor_reino_direito
        self.on_select_reino_esquerdo = on_select_reino_esquerdo
        self.on_select_reino_direito = on_select_reino_direito




    def atualizar_interface(self, nome_reino=None):
        """
        Atualiza a interface com os dados do reino selecionado. Se não houver reinos, limpa a interface.
        """
        dados = carregar_dados_json()
        nomes_reinos = list(dados.get("reinos", {}).keys())
        self.seletor_reino.configure(values=nomes_reinos)

        if nome_reino is None:
            if self.seletor_reino.get() == "":
                if nomes_reinos:
                    self.seletor_reino.set(nomes_reinos[0])
                else:
                    self.limpar_interface()  # Limpa a interface se não houver reinos
                    return
            nome_reino = self.seletor_reino.get()

        reino_data = dados.get("reinos", {}).get(nome_reino, None)

        if reino_data:
            self.label_populacao.configure(text=str(reino_data.get("populacao", 0)))

            tropas = reino_data.get("tropas", {})
            for i, (nome_tropa, quantidade) in enumerate(tropas.items()):
                self.labels_tropas[i].configure(text=str(quantidade))

            self.tabela_economia.delete(*self.tabela_economia.get_children())
            economia = reino_data.get("economia", {})

            receitas = economia.get("receita", {})
            for descricao, detalhes in receitas.items():
                valor = detalhes["valor"]
                self.tabela_economia.insert("", "end", values=(descricao.replace('_', ' ').capitalize(), f"R$ {valor:,.2f}"), tags=('receita',))

            despesas = economia.get("despesa", {})
            for descricao, detalhes in despesas.items():
                valor = detalhes["valor"]
                self.tabela_economia.insert("", "end", values=(descricao.replace('_', ' ').capitalize(), f"R$ {valor:,.2f}"), tags=('despesa',))

            self.tabela_economia.tag_configure('receita', foreground='#90EE90')
            self.tabela_economia.tag_configure('despesa', foreground='red')

            fundos = reino_data.get("fundos", 0.0)
            fundos_previstos = reino_data.get("fundos_previstos", 0.0)

            # Formatar e exibir o valor dos fundos
            if fundos < 0:
                self.label_valor_fundos.configure(
                    text=f"- R$ {abs(fundos):,.2f}",
                    text_color="red",
                    font=("Arial", 14, "bold")
                )
            else:
                self.label_valor_fundos.configure(
                    text=f"R$ {fundos:,.2f}",
                    text_color="green",
                    font=("Arial", 14, "bold")
                )

            # Formatar o total previsto
            if fundos_previstos >= 0:
                self.label_valor_esperado.configure(
                    text=f"+ R$ {fundos_previstos:,.2f}",
                    text_color="green",
                    font=("Arial", 14, "bold")
                )
            else:
                self.label_valor_esperado.configure(
                    text=f"- R$ {abs(fundos_previstos):,.2f}",
                    text_color="red",
                    font=("Arial", 14, "bold")
                )

            # Atualizar a seção de tecnologias
            tecnologias = reino_data.get("tecnologias", {})
            self.atualizar_tecnologias_interface(tecnologias)
        else:
            self.limpar_interface()  # Limpa a interface se não houver dados do reino

        self.atualizar_seletores_combate(nomes_reinos)  # Atualiza os seletores de combate


    def atualizar_tecnologias_interface(self, tecnologias):
        """
        Atualiza a interface de tecnologias dentro da aba "Interno" do tabview.
        """
        for widget in self.frame_tecnologias.winfo_children():
            widget.destroy()  # Limpa o conteúdo existente no frame

        if tecnologias:
            for nome_tecnologia in tecnologias:
                label_tecnologia = ctk.CTkLabel(self.frame_tecnologias, text=nome_tecnologia, font=("Arial", 12, "bold"))
                label_tecnologia.pack(pady=2, padx=5, anchor="center")
        else:
            label_sem_tecnologia = ctk.CTkLabel(self.frame_tecnologias, text="Nenhuma\ntecnologia\npesquisada", font=("Arial", 14, "bold"))
            label_sem_tecnologia.pack(pady=2, padx=5, anchor="center")

    def atualizar_seletores_combate(self, nomes_reinos):
        """
        Atualiza os seletores de reinos na aba "Combate".
        """
        self.seletor_reino_esquerdo.configure(values=nomes_reinos)
        self.seletor_reino_direito.configure(values=nomes_reinos)
        
        if nomes_reinos:
            self.seletor_reino_esquerdo.set(nomes_reinos[0])
            self.seletor_reino_direito.set(nomes_reinos[0])
            self.on_select_reino_esquerdo(nomes_reinos[0])  
            self.on_select_reino_direito(nomes_reinos[0]) 
        else:
            self.seletor_reino_esquerdo.set("")
            self.seletor_reino_direito.set("")


    def limpar_interface(self):
        """
        Limpa ou reseta todos os componentes da interface.
        """
        self.label_populacao.configure(text="")
        for label in self.labels_tropas:
            label.configure(text="0")
        self.tabela_economia.delete(*self.tabela_economia.get_children())
        self.label_valor_fundos.configure(text="R$ 0,00", text_color="green", font=("Arial", 14, "bold"))
        self.label_valor_esperado.configure(text="R$ 0,00", text_color="green", font=("Arial", 14, "bold"))
        self.atualizar_tecnologias_interface({})  # Limpa a lista de tecnologias
        self.atualizar_seletores_combate([])  # Limpa os seletores de combate quando não há reinos




#######################
# OPERAÇÕES COMBATE   #
#######################



# Criação da instância do InterfaceManager
interface_manager = InterfaceManager()
