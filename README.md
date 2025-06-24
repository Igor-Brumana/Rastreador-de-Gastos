# Rastreador-de-Gastos

Um aplicativo de linha de comando (CLI) em Python para registrar, listar, editar, excluir e resumir suas despesas com praticidade e organização.

## 🚀 Funcionalidades

- **Adicionar despesas** com data, descrição, valor e categoria
- **Listar todas as despesas** com filtro opcional por categoria ou mês/ano
- **Editar** qualquer despesa pelo ID
- **Deletar** despesas indesejadas
- **Gerar resumo financeiro** mensal com valores e percentuais por categoria
- Interface bonita com **Rich** (tabelas organizadas)

---

## 📂 Estrutura dos Dados

As despesas são armazenadas no arquivo `despesas.csv` com as seguintes colunas:

- `ID`: identificador único da despesa
- `Data`: no formato `DD/MM/YYYY`
- `Descricao`: texto livre
- `Valor`: valor da despesa (float)
- `Categoria`: Alimentação, Transporte, Moradia, Saúde ou Outros

---

## 🧱 Pré-requisitos

- Python 3.10 ou superior
- Biblioteca `click` e `rich`

Você pode instalar as dependências com:

- pip install click rich


🧪 Como usar

Adicionar uma nova despesa
`python main.py add`

Listar todas as despesas
`python main.py list`

Filtrar por categoria:
`python main.py list --category Transporte`

Filtrar por mês e ano:
`python main.py list --month-year MM/YYYY`

Editar uma despesa pelo ID
`python main.py edit <ID>`

Deletar uma despesa pelo ID
`python main.py delete <ID>`

Ver resumo financeiro de um mês/ano
`python main.py resume MM/YYYY`


📌 Categorias disponíveis:
Alimentação

Transporte

Moradia

Saúde

Outros

📃 Licença
Conferir arquivo LICENSE.

👨‍💻 Autor
Igor Brumana de Lima
Desenvolvedor iniciante segundo projeto em python.

