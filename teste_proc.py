import csv
import random
import os
from lista_ligada import LinkedList
from medidores import medir_tempo, get_pid, DesvioPadrao, memoria_fim, memoria_inicio, memoria_total_consumida
from multiprocessing import Process

def ler_arquivo(nome_arquivo):
    lista = []
    with open(nome_arquivo, "r") as arquivo_aberto:
        for number in arquivo_aberto:
            lista.append(number.strip())
    return lista

diretorio = './arquivos/'
arquivos = os.listdir(diretorio)

def executar_teste(arquivo):
    caminho_arquivo = os.path.join(diretorio, arquivo)

    pid = get_pid()
    #nome_arquivo = './arquivos/arranjo_100_mil.txt'

    lista = ler_arquivo(caminho_arquivo)
    tamanho_arranjo = len(lista)

    #instanciei
    lista_ligada = LinkedList()

    lista_ligada.comparacoes_totais = 0

    # Preenche a lista ligada
    for x in lista:
        lista_ligada.append(x)

    # Ordena Lista Ligada
    #lista_ligada.ordenar_lista_ligada()

    #ordena vetor chamado lista
    #lista.sort(reverse=False)

    #Escolhe os piores casos para teste
    pior_caso1 = -1
    pior_caso2 = -50
    pior_caso3 = -90
    #pior_caso3 = lista[-1] #funciona se a lista estiver ordenada

    '--------- Pior Cenário ---------'
    desvio = DesvioPadrao()

    inicio_tempo_pior = medir_tempo()
    inicio_memoria_pior = memoria_inicio()

    lista_ligada.busca_sequencial_lista_ligada(valor=pior_caso1)
    comparacoes_1 = lista_ligada.comparacoes_totais

    lista_ligada.comparacoes_totais = 0
    lista_ligada.busca_sequencial_lista_ligada(valor=pior_caso2)
    comparacoes_2 = lista_ligada.comparacoes_totais

    lista_ligada.comparacoes_totais = 0
    lista_ligada.busca_sequencial_lista_ligada(valor=pior_caso3)
    comparacoes_3 = lista_ligada.comparacoes_totais

    # Usando a classe DesvioPadrao
    total_comparacoes_pior = [comparacoes_1, comparacoes_2, comparacoes_3]
    desvio_padrao_resultado_pior = desvio.calcular(total_comparacoes_pior)

    fim_tempo_pior = medir_tempo()
    fim_memoria_pior = memoria_fim()

    tempo_pior = (fim_tempo_pior - inicio_tempo_pior) * 1000  # Convertendo para ms
    memoria_consumida_pior = memoria_total_consumida(inicio=inicio_memoria_pior, fim=fim_memoria_pior)

    # 100 números aleatórios da lista enviada

    '--------- 100 Números Aleatórios ---------'

    comparacoes_aleatorio_lista = []
    desvio = DesvioPadrao()
    lista_ligada.comparacoes_totais = 0
    total_de_buscas_aleatorias = 100
    numeros_aleatorios = random.sample(lista, total_de_buscas_aleatorias)

    inicio_tempo_aleatorio = medir_tempo()
    inicio_memoria_aleatorio = memoria_inicio()

    for x in numeros_aleatorios:
        lista_ligada.busca_sequencial_lista_ligada(valor=x)
        comparacoes_aleatorio_lista.append(lista_ligada.comparacoes_totais)
        lista_ligada.comparacoes_totais = 0

    desvio_padrao_resultado_aleatorio = desvio.calcular(comparacoes_aleatorio_lista)

    fim_tempo_aleatorio = medir_tempo()
    fim_memoria_aleatorio = memoria_fim()

    tempo_aleatorio = (fim_tempo_aleatorio - inicio_tempo_aleatorio) * 1000  # Convertendo para ms
    memoria_consumida_aleatorio = memoria_total_consumida(inicio=inicio_memoria_aleatorio, fim=fim_memoria_aleatorio)
    total_comparacoes_aleatorio = sum(comparacoes_aleatorio_lista)

    # Salva os resultados em um arquivo CSV
    nome_arquivo_csv = 'lista_ligada_nao_ordenada.csv'
    # Verifica se o arquivo CSV já existe
    arquivo_existe = os.path.isfile(nome_arquivo_csv)

    with open(nome_arquivo_csv, mode='a', newline='', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)

        # Escreve cabeçalhos apenas se o arquivo não existir
        if not arquivo_existe:
            escritor_csv.writerow(["Arranjo", "Tipo de Teste", "Tempo (ms)", "Memória Consumida (bytes)", "Comparações","Desvio Padrão Comparações"])

        # Adiciona os dados dos testes
        escritor_csv.writerow([tamanho_arranjo, "Pior Cenário", round(tempo_pior), memoria_consumida_pior, sum(total_comparacoes_pior), round(desvio_padrao_resultado_pior)])
        escritor_csv.writerow([tamanho_arranjo, "100 Números Aleatórios", round(tempo_aleatorio), memoria_consumida_aleatorio, total_comparacoes_aleatorio, round(desvio_padrao_resultado_aleatorio)])

    print("Novos resultados adicionados com sucesso no arquivo:", nome_arquivo_csv)

    del memoria_consumida_aleatorio,memoria_consumida_pior,fim_memoria_aleatorio,fim_memoria_pior,inicio_memoria_aleatorio,inicio_memoria_pior
    print("Teste Finalizado!!")

processos = []
for arquivo in arquivos:
    p = Process(target=executar_teste, args=(arquivo,))
    processos.append(p)
    p.start()

for processo in processos:
    processo.join()

print("Todos os testes finalizados!")