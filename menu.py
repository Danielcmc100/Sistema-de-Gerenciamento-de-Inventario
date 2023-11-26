import os


def ShowMenu(opcoes, titulo = None, final = None, apagar = True, opcao = True):
  """
  Cria um menu com titulo, opções e uma opção final
  """

  azul = "\033[34m"
  roxo = "\033[35m"

  if apagar:
    os.system('cls' if os.name == 'nt' else 'clear')
  if titulo is not None:
    espaçamento = 22
    if len(titulo) > espaçamento:
      espaçamento = len(titulo) + 4
    print(azul, end = '')
    print("=" * espaçamento)
    tamanho = len(titulo)
    espaços = int((espaçamento - tamanho) // 2)
    print(roxo, end = '') 
    if (tamanho % 2 == 0):
      print(" " * espaços + titulo + " " * espaços)
    else:
      print(" " * (espaços + 1) + titulo + " " * espaços)
    print(azul, end = '')
    print("=" * espaçamento)
  i = 0
  while i < len(opcoes):
    print(f"{roxo}{i + 1}{azul}-{opcoes[i]}")
    i += 1
  if final is not None:
    print(f"{roxo}*{azul}-{final}")
  if(opcao):
    opcao = input(f"\nDigite a opção{roxo}: {azul}")
  print("")
  return opcao