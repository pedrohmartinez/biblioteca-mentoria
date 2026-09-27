import json
from datetime import date
from pathlib import Path
from random import choice


ARQUIVO_DADOS = Path("biblioteca.json")


class Livro:
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo.strip()
        self.autor = autor.strip()
        self.ano = ano
        self.disponivel = True
        self.leitor = ""
        self.data_emprestimo = ""

    def emprestar(self, leitor):
        if not self.disponivel:
            return False

        self.disponivel = False
        self.leitor = leitor.strip()
        self.data_emprestimo = date.today().isoformat()

        return True

    def devolver(self):
        if self.disponivel:
            return False

        self.disponivel = True
        self.leitor = ""
        self.data_emprestimo = ""

        return True

    def para_dicionario(self):
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
        livro = cls(
            dados["titulo"],
            dados["autor"],
            dados["ano"]
        )

        livro.disponivel = dados["disponivel"]
        livro.leitor = dados["leitor"]
        livro.data_emprestimo = dados["data_emprestimo"]

        return livro


class Biblioteca:

    def __init__(self):
        self.livros = []

    def adicionar(self, livro):
        self.livros.append(livro)

    def buscar(self, texto):
        texto = texto.strip().lower()

        encontrados = []

        for livro in self.livros:
            titulo_corresponde = texto in livro.titulo.lower()
            autor_corresponde = texto in livro.autor.lower()

            if titulo_corresponde or autor_corresponde:
                encontrados.append(livro)

        return encontrados

    def estatisticas(self):
        total = len(self.livros)
        emprestados = 0

        for livro in self.livros:
            if not livro.disponivel:
                emprestados += 1

        disponiveis = total - emprestados

        return total, disponiveis, emprestados

    def salvar(self, caminho):
        dados = []

        for livro in self.livros:
            dados.append(livro.para_dicionario())

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=2
            )

    def carregar(self, caminho):
        if not caminho.exists():
            return

        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            for item in dados:
                self.livros.append(
                    Livro.de_dicionario(item)
                )

        except (json.JSONDecodeError, KeyError, TypeError):
            print(
                "Aviso: não foi possível ler "
                "o arquivo de dados."
            )