from menu import ShowMenu
import uteis


def main():
  # INICIALIZAÇÃO DATAFRAMES

  produtosDataFrame, produtosPath = uteis.InicializaDataFrame(['codigo', 'descricao', 'quantidade'], "CONTROLE_ESTOQUE.csv")
  codigoProduto = 0
  precoDataFrame, precoPath = uteis.InicializaDataFrame(['codigo', 'preco'], "PRECO_PRODUTO.csv")
  vendasDataFrame, vendasPath = uteis.InicializaDataFrame(['codigo', 'valor', 'data'], "VENDAS.csv")
  codigoVenda = 0
  vendasProdutosDataFrame, vendasProdutosPath = uteis.InicializaDataFrame(['codigo_venda', 'codigo_produto', 'quantidade'], "PRODUTOS_VENDA.csv")

  # CARREGAR DATAFRAMES
  produtosDataFrame, codigoProduto = uteis.CarregarDataFrame(produtosDataFrame, produtosPath)
  precoDataFrame = uteis.CarregarDataFrame(precoDataFrame, precoPath)[0]
  vendasDataFrame, codigoVenda = uteis.CarregarDataFrame(vendasDataFrame, vendasPath)
  vendasProdutosDataFrame = uteis.CarregarDataFrame(vendasProdutosDataFrame, vendasProdutosPath)[0]

  # MENU
  while (True):
    opcao = ShowMenu(["CONTROLE DE ESTOQUE", "VENDAS", "RELATORIOS"], "MENU PRINCIPAL", "SAIR")
    match opcao:
      case "1":
        opcao = ShowMenu(["INSERIR", "PESQUISAR"], "CONTROLE DE ESTOQUE", "VOLTAR")
        match opcao:
          case "1":
            produtosDataFrame, codigoProduto = uteis.InserirProduto(codigoProduto, produtosDataFrame, produtosPath)
            precoDataFrame = uteis.InserirPreco(codigoProduto, precoDataFrame, precoPath)
          case "2":
            produtosDataFrame, codigoProduto = uteis.Pesquisar(produtosPath, produtosDataFrame, codigoProduto)
      case "2":
        opcao = ShowMenu(["PREÇO", "VENDA"], "VENDAS", "VOLTAR")
        match opcao:
          case "1":
            precoDataFrame = uteis.Preco(produtosDataFrame, produtosPath, precoDataFrame, precoPath, vendasPath)
          case "2":
            codigoVenda = uteis.Venda(produtosDataFrame, produtosPath, codigoVenda, precoDataFrame, vendasDataFrame, vendasProdutosDataFrame, vendasProdutosPath, vendasPath)
      case "3":
        uteis.Relatorios(vendasDataFrame, vendasProdutosDataFrame, produtosDataFrame)
      case default:
        break


if __name__ == "__main__":
  main()