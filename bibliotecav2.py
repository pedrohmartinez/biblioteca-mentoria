
"""
Sistema de Biblioteca Pessoal.

Projeto didático para praticar, em conjunto, os fundamentos de Python.
Execute com: python biblioteca.py
"""

# ============================================================
# IMPORTAÇÕES
# ============================================================

# json é um módulo da biblioteca padrão do Python.
# Ele permite converter dados Python para JSON e vice-versa.
# Neste projeto, usamos JSON para salvar os livros em um arquivo.
import json

# date permite trabalhar com datas.
# Aqui será usado para registrar a data em que um livro foi emprestado.
from datetime import date

# Path representa caminhos de arquivos e diretórios de forma
# mais segura e orientada a objetos do que trabalhar apenas com strings.
from pathlib import Path

# choice escolhe aleatoriamente um elemento de uma sequência.
# Será usado para sugerir um livro disponível.
from random import choice


# ============================================================
# CONSTANTES
# ============================================================

# Define o nome/caminho do arquivo onde os dados serão armazenados.
#
# Path("biblioteca.json") cria um objeto Path representando
# o arquivo "biblioteca.json".
ARQUIVO_DADOS = Path("biblioteca.json")


# Tupla contendo as opções que aparecerão no menu.
#
# Uma tupla é uma sequência imutável:
# depois de criada, não podemos adicionar/remover elementos.
#
# Por convenção, constantes são escritas em LETRAS_MAIÚSCULAS.
OPCOES_MENU = (
    "Cadastrar livro",
    "Listar livros",
    "Buscar livro",
    "Emprestar livro",
    "Devolver livro",
    "Mostrar estatísticas",
    "Sugerir uma leitura",
    "Sair",
)


# ============================================================
# CLASSE LIVRO
# ============================================================

class Livro:
    """Representa um livro e as ações que podem ser feitas com ele."""

    # __init__ é o método construtor da classe.
    #
    # Ele é executado automaticamente quando criamos um objeto:
    #
    # livro = Livro("1984", "George Orwell", 1949)
    #
    # self representa o próprio objeto que está sendo criado.
    def __init__(self, titulo, autor, ano):

        # strip() remove espaços desnecessários no começo e no final
        # do texto.
        #
        # Exemplo:
        # "  1984  ".strip() -> "1984"
        self.titulo = titulo.strip()

        self.autor = autor.strip()

        # O ano é armazenado diretamente.
        # Neste projeto, ele já foi validado pela função ler_ano().
        self.ano = ano

        # Todo livro começa disponível.
        self.disponivel = True

        # Quando o livro não está emprestado, não existe leitor.
        # Por isso utilizamos uma string vazia.
        self.leitor = ""

        # Da mesma forma, inicialmente não existe data de empréstimo.
        self.data_emprestimo = ""


    def emprestar(self, leitor):
        """Empresta o livro se ele estiver disponível."""

        # Se o livro já estiver emprestado, não podemos emprestá-lo
        # novamente.
        #
        # O operador "not" inverte o valor booleano:
        #
        # True  -> False
        # False -> True
        if not self.disponivel:

            # False indica que a operação não foi realizada.
            return False

        # O livro deixa de estar disponível.
        self.disponivel = False

        # Guardamos o nome da pessoa que pegou o livro.
        # strip() remove espaços extras.
        self.leitor = leitor.strip()

        # date.today() obtém a data atual.
        #
        # isoformat() transforma a data em texto no formato:
        # YYYY-MM-DD
        #
        # Exemplo:
        # "2026-09-27"
        self.data_emprestimo = date.today().isoformat()

        # True indica que o empréstimo foi realizado com sucesso.
        return True


    def devolver(self):
        """Registra a devolução se o livro estiver emprestado."""

        # Se o livro já estiver disponível, não existe
        # empréstimo para devolver.
        if self.disponivel:

            # False indica que nenhuma devolução foi realizada.
            return False

        # O livro volta a ficar disponível.
        self.disponivel = True

        # Como não há mais empréstimo, apagamos o nome do leitor.
        self.leitor = ""

        # Também apagamos a data do empréstimo.
        self.data_emprestimo = ""

        # True indica que a devolução foi realizada.
        return True


    def para_dicionario(self):
        """Transforma o objeto em dicionário para salvá-lo no arquivo."""

        # JSON não sabe salvar diretamente um objeto Livro.
        #
        # Por isso transformamos o objeto em um dicionário.
        #
        # Depois esse dicionário poderá ser convertido para JSON.
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "disponivel": self.disponivel,
            "leitor": self.leitor,
            "data_emprestimo": self.data_emprestimo,
        }


    @classmethod
    def de_dicionario(cls, dados):
        """Cria um Livro a partir de um dicionário lido do arquivo."""

        # @classmethod faz com que o método receba a própria classe
        # como primeiro argumento.
        #
        # Por convenção, esse argumento é chamado de cls.
        #
        # cls(...) equivale a criar um novo objeto da classe.
        livro = cls(
            dados["titulo"],
            dados["autor"],
            dados["ano"]
        )

        # O construtor inicialmente cria o livro como disponível.
        # Porém, estamos carregando um livro que já existia no arquivo.
        #
        # Portanto precisamos restaurar seu estado anterior.
        livro.disponivel = dados["disponivel"]
        livro.leitor = dados["leitor"]
        livro.data_emprestimo = dados["data_emprestimo"]

        # Retornamos o objeto Livro reconstruído.
        return livro


# ============================================================
# CLASSE BIBLIOTECA
# ============================================================

class Biblioteca:
    """Guarda uma lista de livros e oferece operações sobre ela."""

    def __init__(self):

        # Cria uma lista vazia para armazenar objetos Livro.
        #
        # Depois teremos algo como:
        #
        # self.livros = [
        #     Livro(...),
        #     Livro(...),
        #     Livro(...)
        # ]
        self.livros = []


    def adicionar(self, livro):

        # append() adiciona um elemento ao final da lista.
        self.livros.append(livro)


    def buscar(self, texto):
        """Busca por título ou autor, sem diferenciar maiúsculas de minúsculas."""

        # strip() remove espaços externos.
        # lower() transforma o texto em letras minúsculas.
        #
        # Isso permite fazer uma busca sem diferenciar:
        # "Python", "PYTHON" e "python".
        texto = texto.strip().lower()

        # Lista que armazenará os livros encontrados.
        encontrados = []


        # Percorremos todos os livros da biblioteca.
        for livro in self.livros:

            # Verificamos se o texto pesquisado aparece
            # dentro do título.
            titulo_corresponde = texto in livro.titulo.lower()

            # Fazemos a mesma coisa com o autor.
            autor_corresponde = texto in livro.autor.lower()


            # Se o texto aparecer no título OU no autor,
            # adicionamos o livro aos resultados.
            if titulo_corresponde or autor_corresponde:
                encontrados.append(livro)


        # Retornamos a lista de resultados.
        return encontrados


    def estatisticas(self):

        # len() retorna a quantidade de elementos da lista.
        total = len(self.livros)

        # Começamos o contador de empréstimos em zero.
        emprestados = 0


        # Percorremos todos os livros.
        for livro in self.livros:

            # Se o livro NÃO estiver disponível,
            # significa que está emprestado.
            if not livro.disponivel:
                emprestados += 1


        # Se temos o total e sabemos quantos estão emprestados,
        # podemos descobrir quantos estão disponíveis.
        disponiveis = total - emprestados

        # Retornamos três valores.
        #
        # Em Python, isso é possível graças ao desempacotamento:
        #
        # total, disponiveis, emprestados = biblioteca.estatisticas()
        return total, disponiveis, emprestados


    def salvar(self, caminho):

        # Lista que receberá os dados dos livros em formato
        # de dicionário.
        dados = []


        # Percorremos todos os objetos Livro.
        for livro in self.livros:

            # Convertemos cada objeto Livro em dicionário.
            dados.append(livro.para_dicionario())


        # with garante que o arquivo será fechado automaticamente
        # depois que terminarmos de utilizá-lo.
        #
        # "w" significa write (escrita).
        #
        # encoding="utf-8" permite trabalhar corretamente
        # com caracteres como ç, ã, é etc.
        with open(caminho, "w", encoding="utf-8") as arquivo:

            # json.dump() escreve os dados diretamente no arquivo.
            #
            # ensure_ascii=False:
            # mantém caracteres acentuados normalmente.
            #
            # indent=2:
            # deixa o JSON formatado e mais fácil de ler.
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=2
            )


    def carregar(self, caminho):

        # exists() verifica se o arquivo realmente existe.
        #
        # Se ainda não existir, simplesmente começamos
        # com uma biblioteca vazia.
        if not caminho.exists():
            return


        # try permite tentar executar um código que pode gerar
        # uma exceção.
        try:

            # "r" significa read (leitura).
            with open(caminho, "r", encoding="utf-8") as arquivo:

                # json.load() lê o conteúdo JSON e transforma
                # os dados novamente em estruturas Python.
                #
                # JSON:
                # [...]
                #
                # Python:
                # list
                dados = json.load(arquivo)


            # Cada item representa um livro salvo.
            for item in dados:

                # Reconstruímos um objeto Livro a partir
                # do dicionário.
                self.livros.append(
                    Livro.de_dicionario(item)
                )


        # Capturamos possíveis problemas com o arquivo.
        #
        # JSONDecodeError:
        # o arquivo não contém um JSON válido.
        #
        # KeyError:
        # faltou alguma chave esperada.
        #
        # TypeError:
        # os dados possuem um tipo inesperado.
        except (json.JSONDecodeError, KeyError, TypeError):

            print("Aviso: não foi possível ler o arquivo de dados.")
            print("A biblioteca será iniciada sem os dados salvos.")


# ============================================================
# FUNÇÕES DE ENTRADA DE DADOS
# ============================================================

def ler_texto(mensagem):
    """Lê texto obrigatório e impede entradas vazias."""

    # while True cria um loop infinito.
    #
    # Ele só terminará quando encontrarmos um return.
    while True:

        # input() recebe dados digitados pelo usuário.
        #
        # strip() remove espaços antes e depois do texto.
        texto = input(mensagem).strip()


        # Strings vazias são consideradas False em um contexto
        # booleano.
        #
        # Portanto:
        #
        # ""      -> False
        # "Python" -> True
        if texto:
            return texto


        # Se chegar aqui, significa que o usuário
        # não informou nenhum texto.
        print("Digite uma informação válida. O campo não pode ficar vazio.")


def ler_ano():
    """Lê um ano inteiro em intervalo razoável e trata ValueError."""

    # Obtém o ano atual.
    ano_atual = date.today().year


    # Repetiremos até o usuário fornecer um ano válido.
    while True:

        # try será usado porque int() pode gerar ValueError
        # caso o usuário digite algo que não seja um número inteiro.
        try:

            # input() sempre retorna uma string.
            #
            # int() tenta converter essa string para um inteiro.
            ano = int(input("Ano de publicação: "))


            # O ano precisa ser:
            #
            # maior que 0
            # E
            # menor ou igual ao ano atual
            if 0 < ano <= ano_atual:
                return ano


            # f-string permite inserir variáveis dentro do texto.
            print(f"Digite um ano entre 1 e {ano_atual}.")


        # Se int() não conseguir converter a entrada,
        # teremos um ValueError.
        except ValueError:
            print("Digite o ano usando apenas números inteiros.")


# ============================================================
# FUNÇÕES DE EXIBIÇÃO
# ============================================================

def mostrar_livro(livro, indice=None):
    """Exibe as informações de um livro de modo padronizado."""

    # Se não recebemos índice, não exibimos número.
    #
    # Se recebemos, criamos algo como:
    #
    # "1. "
    #
    # O operador ternário possui a estrutura:
    #
    # valor_se_verdadeiro if condição else valor_se_falso
    numero = "" if indice is None else f"{indice}. "


    # Outro exemplo de expressão condicional.
    #
    # Se estiver disponível:
    # "Disponível"
    #
    # Caso contrário:
    # "Emprestado para Pedro"
    situacao = (
        "Disponível"
        if livro.disponivel
        else f"Emprestado para {livro.leitor}"
    )


    # Exibe título, autor e ano.
    print(
        f"{numero}{livro.titulo} — "
        f"{livro.autor} ({livro.ano})"
    )

    # Exibe a situação atual do livro.
    print(f"   Situação: {situacao}")


def escolher_livro(biblioteca, mensagem):
    """Mostra livros e retorna o escolhido; retorna None se não houver livros."""

    # Verificamos se a lista está vazia.
    #
    # len(lista) == 0 funciona, mas:
    #
    # if not lista
    #
    # é uma forma mais idiomática em Python.
    if len(biblioteca.livros) == 0:

        print("Ainda não há livros cadastrados.")

        # None significa ausência de valor.
        return None


    # enumerate() permite percorrer a lista obtendo:
    #
    # índice + elemento
    #
    # start=1 faz a numeração começar em 1 em vez de 0.
    for indice, livro in enumerate(
        biblioteca.livros,
        start=1
    ):
        mostrar_livro(livro, indice)


    # Continuamos perguntando até receber uma escolha válida.
    while True:

        # Novamente utilizamos try porque int()
        # pode gerar ValueError.
        try:

            escolha = int(input(mensagem))


            # O usuário vê números começando em 1.
            #
            # Porém, listas Python começam em 0.
            #
            # Por isso depois utilizaremos:
            # escolha - 1
            if 1 <= escolha <= len(biblioteca.livros):
                return biblioteca.livros[escolha - 1]


            print("Escolha um número exibido na lista.")


        except ValueError:
            print("Digite apenas o número do livro.")


# ============================================================
# OPERAÇÕES DA BIBLIOTECA
# ============================================================

def cadastrar_livro(biblioteca):

    print("\n--- Cadastro de livro ---")

    # Recebemos os dados através das funções de validação.
    titulo = ler_texto("Título: ")
    autor = ler_texto("Autor: ")
    ano = ler_ano()


    # Criamos um novo objeto Livro.
    #
    # Depois enviamos esse objeto para a biblioteca.
    biblioteca.adicionar(
        Livro(titulo, autor, ano)
    )


    print("Livro cadastrado com sucesso.")


def listar_livros(biblioteca):

    print("\n--- Livros cadastrados ---")


    # Uma lista vazia é considerada False.
    #
    # Portanto:
    #
    # if not biblioteca.livros
    #
    # significa:
    # "se não houver livros".
    if not biblioteca.livros:

        print("Nenhum livro cadastrado.")
        return


    # Mostramos todos os livros.
    for indice, livro in enumerate(
        biblioteca.livros,
        start=1
    ):
        mostrar_livro(livro, indice)


def buscar_livro(biblioteca):

    print("\n--- Busca ---")

    # Pedimos ao usuário o termo que deseja pesquisar.
    termo = ler_texto(
        "Digite parte do título ou do autor: "
    )


    # A própria classe Biblioteca possui a lógica da busca.
    encontrados = biblioteca.buscar(termo)


    # Uma lista com elementos é considerada True.
    if encontrados:

        print(
            f"Foram encontrados "
            f"{len(encontrados)} livro(s):"
        )


        for livro in encontrados:
            mostrar_livro(livro)

    else:

        print("Nenhum livro encontrado.")


def emprestar_livro(biblioteca):

    print("\n--- Empréstimo ---")


    # Mostramos os livros e permitimos que o usuário escolha um.
    livro = escolher_livro(
        biblioteca,
        "Número do livro a emprestar: "
    )


    # None significa que não havia livros.
    if livro is None:
        return


    # Só podemos emprestar um livro disponível.
    if livro.disponivel:

        # Pedimos o nome do leitor.
        leitor = ler_texto(
            "Nome de quem vai levar o livro: "
        )


        # Chamamos o método emprestar() do objeto Livro.
        livro.emprestar(leitor)

        print("Empréstimo registrado.")

    else:

        # Se já estiver emprestado, informamos quem está com ele.
        print(
            f"Este livro já está emprestado "
            f"para {livro.leitor}."
        )


def devolver_livro(biblioteca):

    print("\n--- Devolução ---")


    livro = escolher_livro(
        biblioteca,
        "Número do livro a devolver: "
    )


    if livro is None:
        return


    # O método devolver() retorna True ou False.
    #
    # Isso permite verificar diretamente se a operação
    # foi realizada.
    if livro.devolver():

        print("Devolução registrada.")

    else:

        print(
            "Este livro já está disponível "
            "na biblioteca."
        )


def mostrar_estatisticas(biblioteca):

    # Aqui temos um exemplo de desempacotamento.
    #
    # O método retorna:
    #
    # (total, disponiveis, emprestados)
    #
    # E cada valor é colocado na variável correspondente.
    total, disponiveis, emprestados = biblioteca.estatisticas()


    print("\n--- Estatísticas ---")
    print(f"Total de livros: {total}")
    print(f"Disponíveis: {disponiveis}")
    print(f"Emprestados: {emprestados}")


def sugerir_leitura(biblioteca):

    # Criamos uma lista apenas com livros disponíveis.
    disponiveis = []


    # Percorremos todos os livros.
    for livro in biblioteca.livros:

        # Só adicionamos livros que podem ser emprestados.
        if livro.disponivel:
            disponiveis.append(livro)


    # Se não houver nenhum livro disponível,
    # não podemos fazer uma sugestão.
    if not disponiveis:

        print("Não há livros disponíveis para sugerir.")
        return


    # choice() escolhe aleatoriamente um elemento da lista.
    livro = choice(disponiveis)


    print("\nSugestão de leitura:")

    # Reutilizamos a função responsável pela apresentação
    # padronizada dos livros.
    mostrar_livro(livro)


# ============================================================
# MENU
# ============================================================

def mostrar_menu():

    # "\n" adiciona uma quebra de linha antes do menu.
    #
    # "*" repete uma string.
    #
    # "=" * 38
    #
    # produz uma string com 38 sinais de igual.
    print("\n" + "=" * 38)

    print("      BIBLIOTECA PESSOAL")

    print("=" * 38)


    # enumerate() fornece o número e o texto da opção.
    #
    # start=1 faz a contagem começar em 1.
    for numero, opcao in enumerate(
        OPCOES_MENU,
        start=1
    ):

        print(f"{numero}. {opcao}")


# ============================================================
# FUNÇÃO PRINCIPAL DO PROGRAMA
# ============================================================

def executar():

    # Criamos o objeto principal da aplicação.
    biblioteca = Biblioteca()


    # Tentamos carregar os livros previamente salvos.
    #
    # Se o arquivo não existir, a biblioteca simplesmente
    # começará vazia.
    biblioteca.carregar(ARQUIVO_DADOS)


    # Dicionário que relaciona a opção digitada pelo usuário
    # com a função que deverá ser executada.
    #
    # Por exemplo:
    #
    # "1" -> cadastrar_livro
    # "2" -> listar_livros
    #
    # Importante:
    # não usamos cadastrar_livro(biblioteca) aqui.
    #
    # Estamos armazenando a própria função.
    acoes = {
        "1": cadastrar_livro,
        "2": listar_livros,
        "3": buscar_livro,
        "4": emprestar_livro,
        "5": devolver_livro,
        "6": mostrar_estatisticas,
        "7": sugerir_leitura,
    }


    # Loop principal da aplicação.
    #
    # O programa continuará funcionando até o usuário
    # escolher a opção 8.
    while True:

        # Exibe o menu.
        mostrar_menu()


        # Lê a opção escolhida.
        #
        # strip() remove espaços extras.
        opcao = input(
            "Escolha uma opção: "
        ).strip()


        # ====================================================
        # OPÇÃO 8 — SAIR
        # ====================================================

        if opcao == "8":

            # Antes de sair, salvamos os dados no arquivo JSON.
            biblioteca.salvar(ARQUIVO_DADOS)

            print(
                "Dados salvos. Até a próxima leitura!"
            )

            # break encerra o while True.
            break


        # ====================================================
        # OPÇÕES 1 A 7
        # ====================================================

        elif opcao in acoes:

            # Recuperamos a função correspondente no dicionário.
            #
            # Exemplo:
            #
            # opcao = "1"
            #
            # acoes["1"]
            #
            # retorna:
            # cadastrar_livro
            #
            # Depois chamamos a função passando a biblioteca.
            acoes[opcao](biblioteca)


        # ====================================================
        # OPÇÃO INVÁLIDA
        # ====================================================

        else:

            print(
                "Opção inválida. "
                "Escolha um número de 1 a 8."
            )


# ============================================================
# PONTO DE ENTRADA DO PROGRAMA
# ============================================================

# __name__ é uma variável especial criada pelo Python.
#
# Quando executamos diretamente:
#
# python biblioteca.py
#
# o Python define:
#
# __name__ == "__main__"
#
# Portanto, executar() será chamado.
#
# Porém, se outro arquivo fizer:
#
# import biblioteca
#
# __name__ não será "__main__".
#
# Nesse caso, executar() não será chamado automaticamente.
#
# Esse padrão é muito importante em programas Python.
if __name__ == "__main__":
    executar()
