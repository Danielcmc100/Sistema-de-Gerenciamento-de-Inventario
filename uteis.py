#Alunos: Kleber Daniel Mattos Viana, Lucas Cardia Quintan Valle

import os
from menu import ShowMenu
import pandas
import matplotlib.pyplot 
import seaborn 
from datetime import datetime
from regex import FormatoData



def InserirProduto(codigoProduto, produtosDataFrame, produtosPath):
  ShowMenu([],"ADICIONANDO PRODUTO", opcao=False)
  descricao = input("Digite a descrição: ")
  quantidade = int(input("Digite a quantidade: "))

  codigoProduto += 1

  produto = {
      "descricao": descricao,
      "quantidade": quantidade,
      "codigo": codigoProduto
  }

  produtosDataFrame = produtosDataFrame._append(produto, ignore_index=True)
  SalvarDataFrame(produtosDataFrame, produtosPath)
  return produtosDataFrame, codigoProduto 


def Pesquisar(produtosPath, produtosDataFrame, codigoProduto):
  resultado = PesquisarProduto(produtosDataFrame, produtosPath)

  if resultado is None:
    print("Estoque vazio\n")
  else:
    if (resultado.empty):
      opcao = ShowMenu(["INSERIR"],"NENHUM PRODUTO ENCONTRADO", final="SAIR")
      if opcao == 1:
        produtosDataFrame, codigoProduto = InserirProduto(codigoProduto, produtosDataFrame, produtosPath)
    else:

      print(resultado.to_string(index=False))

      opcao = ShowMenu(["EDITAR", "REMOVER"], final="SAIR", apagar=False)

      if (opcao != "1") and (opcao != "2"):
        print("")
      else:
        if opcao == "1":
          descricao = input("Digite a descrição: ")
          quantidade = int(input("Digite a quantidade: "))

          produtosDataFrame.loc[resultado.index, 'descricao'] = descricao
          produtosDataFrame.loc[resultado.index, 'quantidade'] = quantidade

          print("Alterado com sucesso\n")
        elif opcao == "2":
          produtosDataFrame = produtosDataFrame.drop(resultado.index)
          print("Removido com sucesso\n")
        SalvarDataFrame(produtosDataFrame, produtosPath)
  Continuar()
  return produtosDataFrame, codigoProduto


def PesquisarProduto(produtosDataFrame, produtosPath):
  if os.path.exists(produtosPath):
    while (True):
      opcao = ShowMenu(["POR DESCRIÇÃO", "POR CÓDIGO"], "PESQUISAR PRODUTO")
      if opcao == "1":
        descricao = input("Digite a descrição: ")
        resultado = produtosDataFrame.loc[produtosDataFrame['descricao'] == descricao]
        break
      elif opcao == "2":
        descricao = int(input("Digite a código: "))
        resultado = produtosDataFrame.loc[produtosDataFrame['codigo'] == descricao]
        break
      else:
        print("Opção invalida\n")
        Continuar()
    return resultado
  else:
    return None


def InserirPreco(codigo, precoDataFrame, precoPath):
  preco = {'codigo': codigo, 'preco': float(0)}

  precoDataFrame = precoDataFrame._append(preco, ignore_index=True)
  SalvarDataFrame(precoDataFrame, precoPath)
  return precoDataFrame


def Preco(produtosDataFrame, produtosPath, precoDataFrame, precoPath, vendasPath):
  resultado = PesquisarProduto(produtosDataFrame, produtosPath)

  if resultado is None:
    print("Estoque vazio\n")
  else:
    if (resultado.empty):
      print("Nenhum produto encontrado\n")
    else:
      print(resultado.to_string(index=False))
      opcao = ShowMenu(["EDITAR"], final="VOLTAR", apagar=False)

      if opcao == "1":
        preco = float(input("Digite o preço: "))
        precoDataFrame.loc[resultado.index, 'preco'] = preco
        SalvarDataFrame(precoDataFrame, precoPath)

  Continuar()
  return precoDataFrame

def Venda(produtosDataFrame, produtosPath, codigoVenda, precoDataFrame, vendasDataFrame, vendasProdutosDataFrame, vendasProdutosPath, vendasPath):

  produtos = []
  valorTotal = 0
  codigoVenda += 1
  while True:
    produto, valor, produtosDataFrame, mensagem = AdicionarProdutoNaVenda(produtosDataFrame, produtosPath, codigoVenda, precoDataFrame)

    if len(produto) != 0:
      produtos.append(produto)
      valorTotal += valor

    opcao = ShowMenu(["CONTINUAR VENDA", "CONCLUIR VENDA"],mensagem, final="ENCERRAR VENDA")
    encerrarVenda = False
    match opcao:
      case "1":
        continue
      case "2":
        break
      case defalt:
        encerrarVenda = True
        break

  if len(produtos) == 0:
    print("Nenhum produto adiconado\n")
  elif encerrarVenda:
    print("Venda encerrada\n")
  else:
    vendasProdutosDataFrame = vendasProdutosDataFrame._append(produtos, ignore_index=True)
    SalvarDataFrame(vendasProdutosDataFrame, vendasProdutosPath)

    SalvarDataFrame(produtosDataFrame, produtosPath)

    dataVenda = datetime.now()
    dataVenda = dataVenda.strftime("%Y%m%d%H%M%S")

    venda = {
      'codigo': codigoVenda,
      'valor': valorTotal,
      'data': dataVenda
    }
    vendasDataFrame = vendasDataFrame._append(venda, ignore_index=True)
    SalvarDataFrame(vendasDataFrame, vendasPath)
    # print(vendasDataFrame.to_string(index=False))
    #print(venda)

    print(f"Venda realizada com sucesso\nCódigo da venda: {codigoVenda}")
    Continuar()
    return codigoVenda
  Continuar()
  return codigoVenda - 1


def AdicionarProdutoNaVenda(produtosDataFrame, produtosPath, codigoVenda, precoDataFrame):
  produto = {}
  resultado = PesquisarProduto(produtosDataFrame, produtosPath)
  valor = 0
  msg = 'Mensagem Padrão'
  if resultado is None:
    msg = ("Estoque vazio")
  else:
    if (resultado.empty):
      msg = ("Nenhum produto encontrado")
    else:
      print(resultado.to_string(index=False))

      quantidade = int(input("Digite a quantidade: "))
      quantidadeEmEstoque = produtosDataFrame.loc[resultado.index,'quantidade'].iloc[0]

      if quantidade > quantidadeEmEstoque:
        opcao = ShowMenu(["EDITAR ESTOQUE"],"Quantidade insuficiente", "CANCELAR INSERÇÃO")

        if opcao == "1":
          novaQuantidade = int(input("Digite a nova quantidade: "))
          produtosDataFrame.loc[resultado.index,'quantidade'] = novaQuantidade
          msg = ("Quantidade alterada")
        else:
          msg = ("Inserção cancelada")
      else:
        preco = precoDataFrame.loc[resultado.index, 'preco'].iloc[0]
        valor = preco * quantidade

        codigoProduto = produtosDataFrame.loc[resultado.index,'codigo'].iloc[0]

        produto = {
            'codigo_venda': codigoVenda,
            'codigo_produto': codigoProduto,
            'quantidade': quantidade
        }  

        produtosDataFrame.loc[resultado.index, 'quantidade'] = quantidadeEmEstoque - quantidade
        msg = ("Produto adiconado")
  return produto, valor, produtosDataFrame, msg


def Relatorios(vendasDataFrame, vendasProdutosDataFrame, produtosDataFrame):
  formato ="%d/%m/%Y"
  dataInicialN = InputData("Digite a data inicial das vendas\nFormato dd/mm/aaaa ou dd/mm ou dd: ")
  dataInicial = dataInicialN.strftime(formato)
  dataFinalN = InputData("Digite a data final das vendas\nFormato dd/mm/aaaa ou dd/mm ou dd: ")
  dataFinal = dataFinalN.strftime(formato)

  produtosNoPeriodo = FiltarVendas(vendasDataFrame, vendasProdutosDataFrame, produtosDataFrame, dataInicialN, dataFinalN)

  CriarGrafico(produtosNoPeriodo, dataInicial, dataFinal)
  ShowMenu([],f"Vendas no periodo {dataInicial} até {dataFinal}", opcao = False)
  print(produtosNoPeriodo.to_string(index=False))
  Continuar()


def FiltarVendas(vendasDataFrame, vendasProdutosDataFrame, produtosDataFrame, dataInicialN, dataFinalN):
  vendasDataFrame['data'] = pandas.to_datetime(vendasDataFrame['data'], format="%Y%m%d%H%M%S")
  vendasNoPeriodo = vendasDataFrame.loc[(vendasDataFrame['data'] >= dataInicialN) & (vendasDataFrame['data'] <= dataFinalN)]
  produtosNoPeriodo = vendasProdutosDataFrame[vendasProdutosDataFrame['codigo_venda'].isin(vendasNoPeriodo['codigo'])].copy()
  produtosNoPeriodo = produtosNoPeriodo.groupby('codigo_produto', as_index=False)['quantidade'].sum()
  EstoqueProdutosDataFrame = produtosDataFrame.drop(columns=['quantidade'])
  EstoqueProdutosDataFrame = EstoqueProdutosDataFrame.rename(columns={'codigo': 'codigo_produto'})
  produtosNoPeriodo = pandas.merge(produtosNoPeriodo, EstoqueProdutosDataFrame, on='codigo_produto')
  return produtosNoPeriodo


def CriarGrafico(produtosNoPeriodo, dataInicial, dataFinal):
  figura, grafico = matplotlib.pyplot.subplots(figsize=(10, 6))
  seaborn.barplot(x="descricao", y="quantidade", hue="descricao", palette="husl", data=produtosNoPeriodo, legend=False)
  matplotlib.pyplot.ylabel("Quantidade")
  matplotlib.pyplot.xlabel("")
  matplotlib.pyplot.title(f"Quantidade de itens vendidos no período entre {dataInicial} e {dataFinal}")
  matplotlib.pyplot.tight_layout()
  figura.savefig("relatorio.png")
  matplotlib.pyplot.close(figura)


def InputData(frase):
  ShowMenu([],"VENDAS POR PERÍODO", opcao = False)
  while(True):
    data = input(frase)
    if FormatoData(data):
      data = InputDataTime(data)
      break
    else:
      print("Formato invalido, tente novamente")
  return data


def InicializaDataFrame(colunas, path):
  dataframe = pandas.DataFrame(columns=colunas)
  pastaDataFrames = "dataFrames/"
  path = pastaDataFrames + path
  return dataframe, path


def SalvarDataFrame(dataFrame, path):
  dataFrame.to_csv(path, index=False)


def CarregarDataFrame(dataFrame, path):
  codigo = 0
  if (os.path.exists(path)):
    dataFrame = pandas.read_csv(path)
    if 'codigo' in dataFrame.columns:
      codigo = dataFrame['codigo'].max()
  return dataFrame, codigo


def Continuar():
  input("Digite qualquer tecla para continuar...")


def InputDataTime(data):
    try:
        # Tentar converter a string em um objeto datetime
        data = datetime.strptime(data, "%d/%m/%Y")
        return data
    except ValueError:
        try:
            # Se não tiver ano e mês, adicionar o ano e mês atuais
            dataSemAno = datetime.strptime(data, "%d/%m")
            anoAtual = datetime.now().year
            dataCompleta = dataSemAno.replace(year=anoAtual)
            return dataCompleta
        except ValueError:
            # Se não tiver ano, adicionar o ano atual
            dataSemAnoMes = datetime.strptime(data, "%d")
            anoAtual = datetime.now().year
            mesAtual = datetime.now().month
            dataCompleta = dataSemAnoMes.replace(year=anoAtual, month=mesAtual)
            return dataCompleta