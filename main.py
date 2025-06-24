import click
import csv
from rich.console import Console
from rich.table import Table

categorias = ["Alimentação", "Transporte", "Moradia", "Saúde", "Outros"]

def data_valida(dia,mes,ano):
    if len(dia) > 2 or dia.isdigit() == False or int(dia) > 31:
        return False
    if len(mes) > 2 or mes.isdigit() == False or int(mes) > 12:
        return False
    if len(ano)!= 4 or ano.isdigit() == False:
        return False
    return True

@click.group()
def cli():
    pass

@cli.command()
def add():
    """Adicionar uma nova despesa."""
    id_atual = 1
    try:
        with open("despesas.csv", "r") as arquivo:
            dados = csv.DictReader(arquivo)
            for linha in dados:
               if int(linha["ID"]) > id_atual:
                   id_atual = int(linha["ID"])
    except FileNotFoundError:
        click.echo("Pasta não encontrada")

    id_atual+=1
    dia = ""
    mes = ""
    ano = ""
    descricao = ""
    valor = ""
    categoria = ""
    while True:
        try:
            data = click.prompt("Digite a data (DD/MM/YYYY)")
            dia,mes,ano = data.split("/")
            if not data_valida(dia,mes,ano):
                print("Valor inválido! Use DD/MM/YYYY")
                continue
            else:
                break
        except:
            print("Valor inválido! Use DD/MM/YYYY")
    
    descricao = click.prompt("Digite a descrição")
    while True:
        valor = click.prompt("Digite o valor")
        try:
            valor = float(valor)
            if valor < 0:
                print("Valor inválido, digite um valor positivo")
                continue
            else:
                break
        except:
            print("Valor inválido, digite um valor positivo")
            continue

    click.echo("Escolha a categoria:")
    click.echo("1. Alimentação")
    click.echo("2. Transporte")
    click.echo("3. Moradia")
    click.echo("4. Saúde")
    click.echo("5. Outros")
    while True:
        categoria = click.prompt("Digite o número correspondente")
        if categoria.isdigit() == False or int(categoria)>5 or int(categoria)<1:
            print("Valor inválido, digite um numeral positivo de 1 a 5")
            continue
        else:
            break
    click.echo("Despesa com ID {} adicionada com sucesso!".format(id_atual))

    try:
        with open("despesas.csv", "a") as arquivo:
            dados = csv.writer(arquivo, lineterminator='\n')
            dados.writerow([id_atual,"{}/{}/{}".format(dia,mes,ano),descricao,valor,categorias[int(categoria)-1]])
    except FileNotFoundError:
        click.echo("Pasta não encontrada")

@cli.command()
@click.argument("id_editado")
def edit(id_editado):
    """Editar uma despesa existente."""
    click.echo("Editando despesa com ID: {}".format(id_editado))
    gasto_atual={}
    dados = []
    linhas_editadas = []
    id_nao_encontrado = True
    try:
        with open("despesas.csv", "r") as arquivo:
            dados = csv.DictReader(arquivo)
            for linha in dados:
                
                if linha["ID"] == id_editado:
                    id_nao_encontrado=False
                    gasto_atual = linha
                    click.echo("Data atual: {}.".format(gasto_atual["Data"]), nl=False)
                    nova_data =click.prompt("Digite a nova data (DD/MM/YYYY) ou pressione Enter para manter ", default="", show_default=False)
                    try:
                        d,m,a=nova_data.split("/")
                        if(data_valida(d,m,a)):
                            linha["Data"] = nova_data
                    except:
                        pass

                    click.echo("Descrição atual: {}.".format(gasto_atual["Descricao"]), nl=False)
                    nova_descricao =click.prompt("Digite a nova descrição ou pressione Enter para manter ", default="", show_default=False)
                    if len(nova_descricao)>1:
                        linha["Descricao"] = nova_descricao
                    
                    click.echo("Valor atual: {:.2f}.".format(float(gasto_atual["Valor"])), nl=False)
                    novo_valor =click.prompt("Digite o novo valor ou pressione Enter para manter ", default="", show_default=False)
                    try:
                        aux = float(novo_valor)
                        if aux > 0 and novo_valor!="":
                            linha["Valor"] = novo_valor
                    except:
                        pass
                    
                    click.echo("Categoria atual: {}.".format(gasto_atual["Categoria"]), nl=False)
                    click.echo("Escolha uma nova categoria ou pressione Enter para manter:")
                    click.echo("1. Alimentação")
                    click.echo("2. Transporte")
                    click.echo("3. Moradia")
                    click.echo("4. Saúde")
                    click.echo("5. Outros")
                    nova_categoria = click.prompt("Digite o número correspondente ", default="", show_default=False)
                    try:
                        aux = int(nova_categoria)
                        if aux > 0 and aux<6:
                            linha["Categoria"] = categorias[int(nova_categoria)-1]
                    except:
                        pass
                linhas_editadas.append(linha)

    except FileNotFoundError:
        click.echo("Pasta não encontrada")
    if id_nao_encontrado:
        click.echo("Nenhuma despesa encontrada com o ID fornecido.")
    else:
        try:
            with open("despesas.csv", "w") as arquivo:
                dados = csv.DictWriter(arquivo, fieldnames=["ID","Data","Descricao","Valor","Categoria"], lineterminator='\n')
                dados.writeheader()
                for linha in linhas_editadas:
                    dados.writerow(linha)
                click.echo("Despesa editada com sucesso!")
        except FileNotFoundError:
            click.echo("Pasta não encontrada")

@cli.command()
@click.argument("id_deletado")
def delete(id_deletado):
    """Deletar uma despesa existente."""
    id_nao_encontrado = True
    linhas_editadas = []
    try:
        with open("despesas.csv", "r") as arquivo:
            dados = csv.DictReader(arquivo)
            for linha in dados:
                if linha["ID"] == id_deletado:
                    id_nao_encontrado= False
                    continue
                linhas_editadas.append(linha)
    except FileNotFoundError:
        click.echo("Pasta não encontrada")
    if id_nao_encontrado:
        click.echo("Nenhuma despesa encontrada com o ID fornecido.")
    else:
        try:
            with open("despesas.csv", "w") as arquivo:
                dados = csv.DictWriter(arquivo, fieldnames=["ID","Data","Descricao","Valor","Categoria"], lineterminator='\n')
                dados.writeheader()
                for linha in linhas_editadas:
                    dados.writerow(linha)
                click.echo("Despesa com ID {} removida com sucesso!".format(id_deletado))
        except FileNotFoundError:
            click.echo("Pasta não encontrada")

@cli.command()
@click.option("--category", default = None,help="Filtra as despesas por categoria.")
@click.option("--month-year", default = None,help="Filtra as despesas de um mês/ano específico(formato MM/YYYY).")
def list(category,month_year):
    """Listar todas as despesas registradas."""
    soma = 0.0
    linhas_listadas = []
    if category and not category in categorias:
        click.echo("esta categoria não existe")
        exit()

    if month_year and (not month_year[0:2].isdigit() or not month_year[3:7].isdigit()):
        click.echo("formato de data invalido, use MM/YYYY")
        exit()


    try:
        with open("despesas.csv", "r") as arquivo:
            dados = csv.DictReader(arquivo)
            for linha in dados:
                if category and linha["Categoria"] != category:
                    continue

                if month_year:
                    if len(month_year) == 7 and month_year[2] == "/":
                        mm, yyyy = month_year.split("/")
                        data = linha["Data"]
                        if data[3:5] != mm or data[6:10] != yyyy:
                            continue
                linhas_listadas.append(linha)
    except FileNotFoundError:
        click.echo("Pasta não encontrada")
    
    console = Console()
    tabela = Table(title="Lista de Despesas")
    tabela.add_column("ID")
    tabela.add_column("Data")
    tabela.add_column("Descrição")
    tabela.add_column("Valor (R$)")
    tabela.add_column("Categoria ")

    for linha in linhas_listadas:
        tabela.add_row(linha["ID"],linha["Data"],linha["Descricao"],linha["Valor"],linha["Categoria"])
        soma+=float(linha["Valor"])
    tabela.add_row("─"*9,"─"*13,"─"*12,"─"*13,"─"*13)
    tabela.add_row("Total","","",f"{soma:.2f}","")
    console.print(tabela)

@cli.command()
@click.argument("data_resumo")
def resume(data_resumo):
    """Exibir o resumo financeiro mensal."""
    meses_extenso=["Janeiro","Fevereiro", "Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    participacao_categorias = {cat: 0.0 for cat in categorias}
    try:
        data_resumo = data_resumo.strip()
        mes_resumo,ano_resumo = data_resumo.split("/")
        if len(mes_resumo) != 2 or len(ano_resumo) != 4 or not mes_resumo.isdigit() or not ano_resumo.isdigit():
            click.echo("Formato inválido! Use o formato MM/YYYY.")
            return
        
        try:
            with open("despesas.csv", "r") as arquivo:
                dados = csv.DictReader(arquivo)
                for linha in dados:
                    mes = linha["Data"][3:5]
                    ano = linha["Data"][6:10] 
                    if mes == mes_resumo and ano == ano_resumo:
                        participacao_categorias[linha["Categoria"]] += float(linha["Valor"])
        except FileNotFoundError:
            click.echo("Pasta não encontrada")

        total = 0
        for i in range(5):
            total+=participacao_categorias[categorias[i]]

        if total == 0:
            click.echo(f"Nenhuma despesa encontrada para {data_resumo}.")
            return

        console = Console()
        tabela = Table(title="Resumo Financeiro: {}/{}".format(meses_extenso[int(mes_resumo)-1],ano_resumo))
        tabela.add_column("Categoria")
        tabela.add_column("Valor (R$)")
        tabela.add_column("Percentual")
        for cat in categorias:
            valor = participacao_categorias[cat]
            if valor > 0:
                percentual = (valor / total) * 100
                tabela.add_row(cat, f"{valor:.2f}", f"{percentual:.1f}%")
        tabela.add_row("─"*14,"─"*13,"─"*13)
        tabela.add_row("Total Geral",f"{total:.2f}","100.0%")
        console.print(tabela)

    except:
        click.echo("Formato inválido! Use o formato MM/YYYY.")

if __name__ == '__main__':
    cli()
