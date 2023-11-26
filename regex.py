#Alunos: Kleber Daniel Mattos Viana, Lucas Cardia Quintan Valle

from re import compile


def FormatoData(data):
  """
  Verifica se uma data está no formato correto
  """
  padrao = compile(r'^(?:(\d{2})/(\d{2})/(\d{4}))$|^(?:(\d{2})/(\d{2}))$|^(?:(\d{2}))$')
  return padrao.match(data)