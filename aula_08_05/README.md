1 - Instruções de execução
    - No CMD, já com a pasta aberta...
    - Criar o ambiente virtual: py -m venv env
    - Ativar o ambiente virtual: .\env\Scripts\activate
    - Instalar o Flask: pip install flask
    - Abrir o VS Code: code .
    - Iniciar seu aplicativo Flask no modo de depuração: flask run --debug
        - Ele vai te dar o endereço onde seu app está disponível.
        - Após isso, é só você digitar esse endereço no navegador.


2 - Explicações sobre como os recursos foram utilizados
    Funções:
        - render_template: Prepara o HTML para ser enviado.
        - set_cookie: Serve para enviar um cookie para o usuário.
        - max_age: Serve para definir por quanto tempo (em segundos) o cookie vai permanecer válido no navegador do usuário.
        - request.args.get: Serve para acessar parâmetros passados na URL
        - url_for: Indincando que um endereço válido seja gerado para a rota que possui a view.
        - request.form.get e request.form: Lê os dados enviados por um formulário via método POST.
        - redirect: Redireciona o usuário para outra rota.
        - make_response: Cria uma resposta HTTP personalizada.
        - request.cookies.get: Lê o valor de um cookie.

    Rotas:
        - index: Serve para redirecionar para a página inicial (/).

        - cadastro: Carrega uma página HTML para que a pessoa preencha o formulário que está nela.

        - processar_preferencias: Quando o usuário envia o formulário, os dados são lidos via POST e salvos em cookies por 7 dias. Em seguida, ele é redirecionado para outra rota que estará mostrando as suas preferências.

        - preferencias: Recupera os dados contidos nos cookies. Se o nome estiver vazio, significa que a pessoa não se cadastrou, por isso redireciona ela para uma página onde estará o link para o cadastro. Caso contrário, redireciona para visualizacao.html com as preferências do usuário.

        - recomendar: Recebe o parâmetro genero via string de consulta pela URL, busca uma lista de filmes compatíveis com esse gênero no dicionário filmes_por_genero e exibe a lista na página recomendar.html.
