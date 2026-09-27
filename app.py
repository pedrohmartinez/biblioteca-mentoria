"""
Aplicação web da Biblioteca Pessoal.

Este arquivo é responsável apenas pela INTERFACE do programa.

A lógica da biblioteca continua no arquivo:
    biblioteca.py

Para executar:
    streamlit run app.py
"""


# ============================================================
# IMPORTAÇÕES
# ============================================================

# Importamos o Streamlit e damos a ele o apelido "st".
#
# O Streamlit é a biblioteca que permite criar uma
# interface web usando Python.
import streamlit as st


# Importamos as classes e a constante que criamos
# no arquivo biblioteca.py.
#
# Biblioteca -> representa nossa biblioteca.
# Livro      -> representa um livro.
# ARQUIVO_DADOS -> caminho do arquivo biblioteca.json.
from biblioteca import Biblioteca, Livro, ARQUIVO_DADOS


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

# st.set_page_config() configura algumas características
# da página do navegador.
#
# page_title:
# define o título que aparece na aba do navegador.
#
# page_icon:
# define o ícone da página.
#
# layout="wide":
# permite utilizar uma área maior da tela.
st.set_page_config(
    page_title="Biblioteca Pessoal",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# CARREGAMENTO DA BIBLIOTECA
# ============================================================

# O Streamlit pode executar o arquivo novamente sempre que
# o usuário interage com algum componente da interface.
#
# Por isso, usamos @st.cache_resource para informar ao
# Streamlit que queremos reutilizar o objeto criado.
#
# Pense no cache como:
#
# "Se a biblioteca já foi criada, não precisamos criar
# outra toda vez que a página for atualizada."
@st.cache_resource
def carregar_biblioteca():

    # Criamos um objeto da classe Biblioteca.
    biblioteca = Biblioteca()

    # Tentamos carregar os livros que estão salvos
    # no arquivo biblioteca.json.
    #
    # Se o arquivo não existir, o método carregar()
    # simplesmente deixará a biblioteca vazia.
    biblioteca.carregar(ARQUIVO_DADOS)

    # Retornamos o objeto Biblioteca.
    return biblioteca


# Chamamos a função para obter nossa biblioteca.
#
# A variável "biblioteca" será utilizada pelo restante
# da aplicação.
biblioteca = carregar_biblioteca()


# ============================================================
# FUNÇÃO AUXILIAR
# ============================================================

def salvar_biblioteca():
    """
    Salva os livros atuais no arquivo JSON.
    """

    # Chamamos o método salvar() que já existe
    # na classe Biblioteca.
    #
    # Dessa forma, o app.py não precisa saber como
    # o JSON funciona internamente.
    biblioteca.salvar(ARQUIVO_DADOS)


# ============================================================
# CABEÇALHO
# ============================================================

# st.title() cria o título principal da página.
st.title("📚 Biblioteca Pessoal")


# st.write() escreve um texto na página.
#
# É parecido com o print() que utilizávamos no terminal,
# mas aqui o texto aparece na interface web.
st.write(
    "Sistema didático desenvolvido para praticar "
    "fundamentos de Python."
)


# ============================================================
# MENU LATERAL
# ============================================================

# st.sidebar cria uma área lateral na aplicação.
#
# Dentro dela colocamos um menu para o usuário escolher
# qual parte da biblioteca deseja utilizar.
#
# st.radio() cria opções de seleção.
#
# O valor escolhido pelo usuário será armazenado
# na variável "opcao".
opcao = st.sidebar.radio(
    "Menu",
    [
        "📖 Livros",
        "➕ Cadastrar",
        "🔎 Buscar",
        "📤 Emprestar",
        "📥 Devolver",
        "📊 Estatísticas",
        "🎲 Sugerir leitura",
    ]
)


# ============================================================
# OPÇÃO — LISTAR LIVROS
# ============================================================

# Verificamos qual opção o usuário escolheu.
#
# Se ele escolheu "📖 Livros", executamos este bloco.
if opcao == "📖 Livros":

    # Cria um título menor dentro da página.
    st.header("Livros cadastrados")


    # Verificamos se a lista de livros está vazia.
    #
    # Uma lista vazia é considerada False em Python.
    #
    # Portanto:
    #
    # if not biblioteca.livros
    #
    # significa:
    #
    # "se não existem livros".
    if not biblioteca.livros:

        # st.info() mostra uma mensagem informativa.
        st.info("Nenhum livro cadastrado.")


    # Caso existam livros, executamos o else.
    else:

        # Percorremos todos os livros da biblioteca.
        #
        # A variável "livro" representa um objeto Livro
        # a cada repetição do loop.
        for livro in biblioteca.livros:

            # st.container() cria uma área para agrupar
            # os elementos de cada livro.
            #
            # border=True adiciona uma borda visual.
            with st.container(border=True):

                # Criamos duas colunas.
                #
                # A primeira terá tamanho 3.
                # A segunda terá tamanho 1.
                #
                # Isso significa que a primeira coluna
                # ocupará mais espaço.
                col1, col2 = st.columns([3, 1])


                # Tudo dentro deste bloco será colocado
                # na primeira coluna.
                with col1:

                    # Mostramos o título do livro.
                    st.subheader(livro.titulo)

                    # Mostramos o autor.
                    #
                    # **Autor:** cria texto em negrito
                    # no Markdown utilizado pelo Streamlit.
                    st.write(
                        f"**Autor:** {livro.autor}"
                    )

                    # Mostramos o ano.
                    st.write(
                        f"**Ano:** {livro.ano}"
                    )


                # Tudo dentro deste bloco será colocado
                # na segunda coluna.
                with col2:

                    # Verificamos se o livro está disponível.
                    if livro.disponivel:

                        # st.success() mostra uma mensagem
                        # visualmente positiva.
                        st.success("Disponível")

                    else:

                        # Caso esteja emprestado, mostramos
                        # o nome do leitor.
                        st.warning(
                            f"Emprestado para "
                            f"{livro.leitor}"
                        )


# ============================================================
# OPÇÃO — CADASTRAR LIVRO
# ============================================================

# Se a opção escolhida for "Cadastrar".
elif opcao == "➕ Cadastrar":

    st.header("Cadastrar livro")


    # st.text_input() cria um campo onde o usuário
    # pode digitar um texto.
    #
    # O conteúdo digitado será armazenado na variável
    # "titulo".
    titulo = st.text_input("Título")


    # Criamos outro campo para o autor.
    autor = st.text_input("Autor")


    # st.number_input() cria um campo para números.
    #
    # min_value:
    # menor valor permitido.
    #
    # max_value:
    # maior valor permitido.
    #
    # step:
    # determina de quanto em quanto o número aumenta.
    ano = st.number_input(
        "Ano de publicação",
        min_value=1,
        max_value=2100,
        step=1
    )


    # st.button() cria um botão.
    #
    # O resultado será:
    #
    # True  -> botão foi clicado.
    # False -> botão não foi clicado.
    #
    # type="primary" destaca visualmente o botão.
    if st.button(
        "Cadastrar livro",
        type="primary"
    ):

        # Verificamos se o título está vazio.
        #
        # strip() remove espaços antes e depois do texto.
        #
        # Exemplo:
        #
        # "   ".strip()
        #
        # resulta em:
        #
        # ""
        if not titulo.strip():

            # Mostramos uma mensagem de erro.
            st.error("Informe o título.")


        # Se o título estiver preenchido, verificamos
        # se o autor também foi informado.
        elif not autor.strip():

            st.error("Informe o autor.")


        # Se chegamos ao else, significa que os dados
        # obrigatórios foram preenchidos.
        else:

            # Criamos um novo objeto Livro.
            #
            # A classe Livro está no arquivo biblioteca.py.
            livro = Livro(
                titulo,
                autor,
                int(ano)
            )


            # Adicionamos o novo livro à biblioteca.
            biblioteca.adicionar(livro)


            # Depois de alterar os dados, salvamos a biblioteca
            # no arquivo JSON.
            salvar_biblioteca()


            # Mostramos uma mensagem de sucesso.
            st.success(
                f'Livro "{titulo}" cadastrado com sucesso!'
            )


# ============================================================
# OPÇÃO — BUSCAR LIVRO
# ============================================================

elif opcao == "🔎 Buscar":

    st.header("Buscar livro")


    # Criamos um campo para o usuário digitar
    # o título ou autor que deseja procurar.
    termo = st.text_input(
        "Digite parte do título ou autor"
    )


    # Só fazemos a busca quando o usuário
    # tiver digitado alguma coisa.
    #
    # Uma string vazia é considerada False.
    if termo:

        # Chamamos o método buscar() da classe Biblioteca.
        #
        # Ele retorna uma lista contendo os livros
        # encontrados.
        encontrados = biblioteca.buscar(termo)


        # Verificamos se encontramos algum livro.
        #
        # Uma lista com elementos é considerada True.
        if encontrados:

            # len() informa quantos livros foram encontrados.
            st.write(
                f"{len(encontrados)} livro(s) encontrado(s)."
            )


            # Percorremos os resultados da busca.
            for livro in encontrados:

                # Criamos um container para cada resultado.
                with st.container(border=True):

                    # Mostramos o título.
                    st.subheader(livro.titulo)

                    # Mostramos o autor.
                    st.write(
                        f"**Autor:** {livro.autor}"
                    )

                    # Mostramos o ano.
                    st.write(
                        f"**Ano:** {livro.ano}"
                    )


                    # Verificamos a situação do livro.
                    if livro.disponivel:

                        st.success("Disponível")

                    else:

                        st.warning(
                            f"Emprestado para "
                            f"{livro.leitor}"
                        )


        # Caso a busca não encontre nenhum resultado.
        else:

            st.info("Nenhum livro encontrado.")


# ============================================================
# OPÇÃO — EMPRESTAR LIVRO
# ============================================================

elif opcao == "📤 Emprestar":

    st.header("Emprestar livro")


    # Criamos uma nova lista contendo somente
    # os livros disponíveis.
    #
    # Esta é uma "list comprehension".
    #
    # É uma forma compacta de criar uma lista
    # a partir de outra lista.
    disponiveis = [
        livro
        for livro in biblioteca.livros
        if livro.disponivel
    ]


    # Se não existir nenhum livro disponível,
    # não podemos realizar um empréstimo.
    if not disponiveis:

        st.info(
            "Não existem livros disponíveis."
        )


    # Caso existam livros disponíveis.
    else:

        # st.selectbox() cria uma caixa de seleção.
        #
        # O usuário poderá escolher um dos livros
        # disponíveis.
        livro = st.selectbox(
            "Livro",
            disponiveis,

            # format_func define como cada objeto
            # será mostrado para o usuário.
            #
            # O objeto continua sendo um Livro.
            # Apenas sua aparência no selectbox muda.
            format_func=lambda livro: (
                f"{livro.titulo} — {livro.autor}"
            )
        )


        # Campo para informar o nome do leitor.
        leitor = st.text_input(
            "Nome do leitor"
        )


        # Botão responsável por confirmar o empréstimo.
        if st.button(
            "Registrar empréstimo",
            type="primary"
        ):

            # Primeiro verificamos se o nome foi informado.
            if not leitor.strip():

                st.error(
                    "Informe o nome do leitor."
                )


            # Caso exista um nome, chamamos o método
            # emprestar() da classe Livro.
            #
            # O método retorna:
            #
            # True  -> empréstimo realizado.
            # False -> livro já estava emprestado.
            elif livro.emprestar(leitor):

                # Salvamos a alteração no JSON.
                salvar_biblioteca()


                # Mostramos uma mensagem de sucesso.
                st.success(
                    f'"{livro.titulo}" foi '
                    f'emprestado para {leitor}.'
                )


# ============================================================
# OPÇÃO — DEVOLVER LIVRO
# ============================================================

elif opcao == "📥 Devolver":

    st.header("Devolver livro")


    # Criamos uma lista contendo apenas os livros
    # que estão atualmente emprestados.
    #
    # not livro.disponivel significa:
    #
    # "o livro NÃO está disponível".
    emprestados = [
        livro
        for livro in biblioteca.livros
        if not livro.disponivel
    ]


    # Se não existem livros emprestados,
    # não temos nada para devolver.
    if not emprestados:

        st.info(
            "Não existem livros emprestados."
        )


    else:

        # Mostramos somente os livros emprestados
        # em uma caixa de seleção.
        livro = st.selectbox(
            "Livro",
            emprestados,

            # Mostramos o título e quem está com o livro.
            format_func=lambda livro: (
                f"{livro.titulo} — "
                f"{livro.leitor}"
            )
        )


        # Botão para confirmar a devolução.
        if st.button(
            "Registrar devolução",
            type="primary"
        ):

            # Chamamos o método devolver().
            #
            # Ele retorna True se a devolução
            # foi realizada.
            if livro.devolver():

                # Salvamos a alteração no arquivo JSON.
                salvar_biblioteca()


                # Mostramos uma mensagem de sucesso.
                st.success(
                    f'"{livro.titulo}" foi devolvido.'
                )


# ============================================================
# OPÇÃO — ESTATÍSTICAS
# ============================================================

elif opcao == "📊 Estatísticas":

    st.header("Estatísticas")


    # O método estatisticas() retorna três valores:
    #
    # total
    # disponiveis
    # emprestados
    #
    # Podemos colocar cada valor diretamente
    # em uma variável utilizando desempacotamento.
    total, disponiveis, emprestados = (
        biblioteca.estatisticas()
    )


    # Criamos três colunas para mostrar
    # as estatísticas lado a lado.
    col1, col2, col3 = st.columns(3)


    # Primeira coluna.
    with col1:

        # st.metric() mostra um valor destacado.
        st.metric(
            "Total de livros",
            total
        )


    # Segunda coluna.
    with col2:

        st.metric(
            "Disponíveis",
            disponiveis
        )


    # Terceira coluna.
    with col3:

        st.metric(
            "Emprestados",
            emprestados
        )


# ============================================================
# OPÇÃO — SUGERIR LEITURA
# ============================================================

elif opcao == "🎲 Sugerir leitura":

    st.header("Sugestão de leitura")


    # Criamos uma lista somente com livros disponíveis.
    #
    # Não queremos sugerir um livro que já esteja
    # emprestado.
    disponiveis = [
        livro
        for livro in biblioteca.livros
        if livro.disponivel
    ]


    # Se não houver nenhum livro disponível,
    # não podemos fazer uma sugestão.
    if not disponiveis:

        st.info(
            "Não existem livros disponíveis "
            "para sugerir."
        )


    else:

        # Importamos o módulo random.
        #
        # Ele possui funções relacionadas
        # a escolhas aleatórias.
        import random


        # random.choice() escolhe aleatoriamente
        # um elemento da lista.
        #
        # Portanto, cada vez que a opção for executada,
        # um dos livros disponíveis poderá ser escolhido.
        livro = random.choice(disponiveis)


        # Mostramos uma mensagem indicando
        # que encontramos uma sugestão.
        st.success(
            "📚 Sua sugestão de leitura:"
        )


        # Mostramos as informações do livro escolhido.
        st.subheader(livro.titulo)

        st.write(
            f"**Autor:** {livro.autor}"
        )

        st.write(
            f"**Ano:** {livro.ano}"
        )

