# RPG Realm Tool

Ferramenta experimental desenvolvida em **Python** para gerenciamento de
reinos em cenários de RPG de fantasia.\
Este projeto **não segue boas práticas de programação** e **não está bem
organizado** --- foi feito de forma simples e direta, apenas para ser
minimamente funcional.\
Ele surgiu como uma ferramenta de uso pessoal, para diversão, e servia
como complemento a outros softwares como **[Azgaar's Fantasy Map
Generator](https://azgaar.github.io/Fantasy-Map-Generator/)** (para
mapas) e **People Playground** (para simulação visual de batalhas).

------------------------------------------------------------------------

## ⚙️ Funcionalidades

-   Criação, exclusão e atualização de **reinos**.
-   Gestão de **população, fundos e economia** (receitas, despesas,
    juros de poupança e empréstimos).
-   Sistema de **tecnologias** (proficiências militares, defesas,
    indústrias, fazendas, etc.).
-   Controle de **tropas** com manutenção financeira.
-   Simulação de **turnos** com atualização automática de
    receitas/despesas.
-   Interface gráfica feita em **CustomTkinter**, com tema definido em
    JSON.
-   Sistema de **banco interno** (poupança e empréstimos com juros).
-   Representação visual de tropas e combate básico.

------------------------------------------------------------------------

<img width="989" height="854" alt="image" src="https://github.com/user-attachments/assets/fa579a6f-ffcb-495a-a26c-adf115fb7e90" />

## 🏗️ Estrutura do Projeto

-   `main.py` → núcleo do aplicativo; inicializa a interface principal,
    abas e sistema de combate.
-   `menus.py` → janelas secundárias (economia, tropas, tecnologias,
    etc.).
-   `functions.py` → funções de backend (criação de reinos, economia,
    turnos, persistência em JSON).
-   `estilo_visual.json` → tema visual para os widgets da interface
    (cores, bordas, fontes).
-   `logo.ico` → ícone da aplicação.
-   `dados/` → pasta criada em tempo de execução para armazenar o
    arquivo `dados.json` com as informações dos reinos.

------------------------------------------------------------------------

<img width="980" height="841" alt="image" src="https://github.com/user-attachments/assets/9c3eba16-9bbe-4d2b-b218-e6f29968305d" />

## 🚀 Como Executar

Requisitos: - Python 3.10+\
- Bibliotecas: `bash   pip install customtkinter pillow`

Execução:

``` bash
python main.py
```

------------------------------------------------------------------------

## 🎯 Propósito

O objetivo principal era criar uma **ferramenta simples de apoio a
campanhas de RPG**: - Usar o **Azgaar's Fantasy Map Generator** para os
mapas e geopolítica. - Usar o **RPG Realm Tool** para gerenciar os
reinos, suas economias e tropas. - Exportar as batalhas para o **People
Playground**, que servia como "motor visual" para encenações.

Ou seja, este projeto funciona como uma **ponte entre ferramentas
externas**, permitindo mais imersão em cenários de RPG de mesa ou
narrativos.

------------------------------------------------------------------------

<img width="593" height="768" alt="image" src="https://github.com/user-attachments/assets/e1d6bddf-e148-4aa7-aa70-4d02cd6d082c" />

## ⚠️ Aviso

Este código **não foi escrito com foco em qualidade, organização ou boas
práticas**.\
Ele é cheio de gambiarras, inconsistências de nomenclatura e
acoplamentos fortes entre as funções.\
Ainda assim, foi uma ótima experiência prática e cumpriu seu papel como
projeto de diversão pessoal.

Se alguém quiser estudar, melhorar ou reaproveitar --- sinta-se livre.
🙂
