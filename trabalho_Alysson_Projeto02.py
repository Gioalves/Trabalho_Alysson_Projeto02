from flask import Flask, jsonify
import requests
import time
import unicodedata

app = Flask(__name__)

# Função para obter a lista de cidades brasileiras da API do IBGE
def obter_lista_de_cidades():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    response = requests.get(url)
    cidades = response.json()
    return cidades

# Função para remover a acentuação de uma string
def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

# Algoritmo de Selection Sort
def selection_sort(cidades):
    n = len(cidades)
    comp = 0
    for i in range(n):
        min = i
        for j in range(i+1, n):
            comp += 1
            if cidades[j]["nome_sem_acentos"] < cidades[min]["nome_sem_acentos"]:
                min = j
        cidades[i], cidades[min] = cidades[min], cidades[i]
    return comp

# Algoritmo de Bubble Sort
def bubble_sort(cidades):
    n = len(cidades)
    comp = 0
    for i in range(n):
        for j in range(0, n-i-1):
            comp += 1
            if cidades[j]["nome_sem_acentos"] > cidades[j+1]["nome_sem_acentos"]:
                cidades[j], cidades[j+1] = cidades[j+1], cidades[j]
    return comp

# Algoritmo de Insertion Sort
def insertion_sort(cidades):
    comp = 0
    for i in range(1, len(cidades)):
        chave = cidades[i]
        j = i - 1
        while j >=0 and cidades[j]["nome_sem_acentos"] > chave["nome_sem_acentos"]:
            comp += 1
            cidades[j + 1] = cidades[j]
            j -= 1
        cidades[j + 1] = chave
    return comp

# Função para medir o tempo de execução de um algoritmo de ordenação
def medir_tempo_de_execucao_e_comparacoes(algoritmo, cidades):
    inicio = time.time()
    comp = algoritmo(cidades)
    fim = time.time()
    tempo = fim - inicio
    return tempo, comp

# Rota para comparar o tempo de execução dos algoritmos e exibir as cidades em ordem alfabética
@app.route('/comparar-algoritmos')
def comparar_algoritmos():
    # Obter a lista de cidades brasileiras
    cidades = obter_lista_de_cidades()

    # Remover a acentuação dos nomes das cidades
    for cidade in cidades:
        cidade["nome_sem_acentos"] = remover_acentos(cidade["nome"]).lower()

    # Realizar a cópia da lista de cidades para cada algoritmo
    cidades_selection = cidades.copy()
    cidades_bubble = cidades.copy()
    cidades_insertion = cidades.copy()

    # Medir o tempo de execução de cada algoritmo e contar o número de comparações
    tempo_selection, comp_selection = medir_tempo_de_execucao_e_comparacoes(selection_sort, cidades_selection)
    tempo_bubble, comp_bubble = medir_tempo_de_execucao_e_comparacoes(bubble_sort, cidades_bubble)
    tempo_insertion, comp_insertion = medir_tempo_de_execucao_e_comparacoes(insertion_sort, cidades_insertion)

    # Criar uma lista de cidades ordenadas alfabeticamente
    cidades_ordenadas = sorted(cidades, key=lambda x: x["nome_sem_acentos"])

    # Criar o dicionário com os resultados
    resultados = {
        "Selection Sort": {"tempo_execucao": tempo_selection, "num_comparacoes": comp_selection},
        "Bubble Sort": {"tempo_execucao": tempo_bubble, "num_comparacoes": comp_bubble},
        "Insertion Sort": {"tempo_execucao": tempo_insertion, "num_comparacoes": comp_insertion},
        "Cidades_ordenadas": [cidade["nome"] for cidade in cidades_ordenadas]
    }

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
