# News Scrapper com Python, Selenium e outras bibliotecas
## ➡️ Fazendo login
A primeira função do nosso sistema é ```def login_twitter```, que serve para o usuário inserir as credenciais de acesso ao X. É uma função que espera receber três argumentos: driver, username e password.

Ela é composta por um bloco **try/except**, que tentará acessar a página principal da rede social X, encontrar os campos para preenchimento do nome de usuário com senha e acessar o feed de notícias. 

Agora, vamos analisar algumas linhas e blocos importantes dessa função.

```time.sleep(5)```
🔎Esta espera é importante para garantir que tanto o DOM básico como os elementos JavaScript, CSS e dinâmicos estejam carregados. ***DOM (Document Object Model)*** é a representação da página web que estamos acessando na memória do navegador. 

Apenas ela não é suficiente para termos certeza que um site complexo, como o X, que possui os campos de login criados dinamicamente, esteja pronto para o scrapping.

```wait = WebDriverWait(driver, 20)```
🔎Aqui, criamos um objeto de espera inteligente que serve para verificar repetidamente uma condição. Uma vez que ela é atendida, o objeto "para".

1. Encontrar campo username e inserir as informações do usuário;
Aqui, criamos uma lista com *seletores CSS*, que será percorrida através do loop **for**. O loop vai parar assim que o Selenium encontrar um elemento na página que contenha exatamente os mesmos valores e atributos fornecidos.

Por exemplo, ```'input[name="text"]'``` localiza um elemento <input> que possui o atributo *name* com o valor exato "password". ```'input[data-testid="ocfEnterTextTextInput"]'``` é criado especificamente para automação de testes, fornecendo um "gancho" estável, que não muda mesmo que o design ou a estrutura do backend sejam alterados.

Se após a varredura feita no loop nada for encontrado, o usuário é avisado que o campo username não foi encontrado, e a função termina retornando False. Se o scrapper achar nosso campo, o seguinte bloco de código será executado:

```
    print(f'✏️Campo sendo preenchido: username({username})')
    username_field.clear()
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(3)
```

*clear()* limpa algum placeholder que esteja presente no campo, *send_keys(username)* faz a inserção dos caracteres enviados pelo usuário e *send_keys(Keys.RETURN)* "pressiona" a tecla ENTER, do teclado.

2. Encontrar campo senha e inserir as informações do usuário;
Esse trecho funciona de forma semelhante ao que foi construído para encontrar o campo username. Uma lista com seletores css é criada para encontrar os elementos correspondentes à senha. Os seletores aqui são diferentes. ```'input[type="password"]'```, por exemplo, tem como principal característica o fato de esconder os caracteres digitados por pontinhos ou asteriscos quando a senha é digitada.

3. Certificando sucesso do login
O último passo para que a função esteja completa é garantir que o login tenha sido realizado com sucesso. Para isso, também criamos uma lista com seletores css que será percorrida pelo loop for. A função termina com a *Exception e*, que pode acontecer por problemas de conexão, do navegador ou outro erro inesperado.


## ➡️ Coletando os posts do perfil
Depois de fazer login, o programa deve acessar o perfil de notícias escolhido, rolar a página e captar os textos e os comentários de cada post. A função anterior precisou ser feita porque o X não permite o acesso aos comentários sem um login. 


Passamos para a configuração do Chrome através de algumas opções importantes:
✅options.add_argument('--no-sandbox')
Desativa o "sandbox" de segurança do Chrome, que é um recurso que isola os processos do navegador do resto do sistema, impedindo que sites maliciosos causem danos. Em muitos ambientes de servidor e contêineres, as restrições de permissões do sistema entram em conflito com o sandbox, impedindo o navegador de iniciar. 

✅options.add_argument('--disable-dev-shm-usage')
Navegadores baseados em Chromium usam o diretório de memória compartilhada *dev-shm* para armazenar arquivos temporários. O tamanho padrão desse diretório pode ser muito pequeno, o que pode fazer com que o navegador trave. Este argumento instrui o navegador a usar o diretório /tmp, que geralmente tem mais espaço disponível.

✅options.add_argument('--disable-blink-features=AutomationControlled')
Ao implementar essa linha de código, desativamos um recurso específico do motor de renderização *Blink*, que permite que sites verifiquem a propriedade **navigator.webdriver** no JavaScript. Quando um navegador é controlado pelo Selenium, navigator.webdriver geralmente retorna *true*. Ao desativar essa funcionalidade, a propriedade pode retornar *false*, fazendo com que o navegador pareça não estar automatizado.

✅options.add_experimental_option("excludeSwitches", ["enable-automation"])
Aqui estamos simplesmente removendo o switch que faz aparecer a barra de notificação "O Chrome está sendo controlado por um software de teste automatizado". 

✅options.add_experimental_option('useAutomationExtension', False)
E por fim pedimos que o Selenium não use uma extensão de automação interna que ele normalmente injeta no navegador. A presença dessa extensão pode ser outro sinal para os sistemas de detecção de que se trata de um bot.


Depois de fazer a instalação do driver, adicionamos mais uma camada de proteção contra detecção de automação através desta linha de código:
```driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")```
**driver.execute_script()**: método do Selenium que permite executar um código JavaScript direto no navegador.
**Object.defineProperty()**: função em JavaScript que permite modificar as propriedades de um objeto.
**navigator**: o objeto que iremos alterar.
**webdriver**: propriedade do objeto navigator, que em geral retorna True, pois de fato ele está sendo utilizado.
**{get: () => undefined}**: acionamos essa parte justamente para mudar esse True quando o script do site tentar ler (get) as propriedades de navigator.webdriver.


‼️Agora entramos no bloco *try* da nossa função. A primeira verificação a ser feita é se o login foi bem sucedido (lembrando que a função *login_twitter* retorna um *bool*). Em caso negativo, *collecting_posts* retorna uma lista vazia. 

Se o login tiver dado certo, vamos acessar a url e extrair seu nome através da função **split**, que retorna uma lista. Dividimos a url pelas barras (/) e pegamos o último elemento, que corresponde ao nome do portal que estamos acessando [-1].


Em seguida, setamos as variáveis que irão nortear nosso scrapper pelos posts. 
``collected_data = []``: uma lista de dicionários que irá armazenar o código da postagem, o nome do portal de notícias, o texto do post e o texto dos comentários.
``processed_posts = set()``: um conjunto que tem como principal objetivo evitar duplicatas. É que quando rolarmos a página várias vezes, os mesmos posts aparecerão, mas através do set garantimos que apenas os posts com id ainda não acessados sejam clicados.
``collected_posts = 0``: número de posts coletados.
``scrollings = 0``: número de rolagens na página.
``max_scrollings = 15``: número máximo permitido de rolagens.


O laço principal determina que enquanto o número de posts coletados for menor que o número determinados na função e o número de rolagens na página for menor que o máximo permitido os posts e comentários serão buscados.

```if not posts```: esse bloco será executado enquanto a página não carregar nenhum post. Note que se nenhum for encontrado até que o número de rolagens máximo permitido seja alcançado nenhum dado será exibido. O comando em JavaScript **"window.scrollTo(0, document.body.scrollHeight);"** serve para rolar a página até o final, já que em muitos casos somente após fazer isso o conteúdo irá aparecer. 


Agora, para cada post encontrado, iremos extrair o texto, criar ids únicos para evitar as repetições e coletar comentários. Antes, veja os seletores css utilizados:
✔️ *article[data-testid="tweet"]*: 'article' é a tag HMTL que identifica cada tweet, e o que está dentro dos colchetes é o atributo específico que o X usa para eles.
✔️ *[data-testid="tweetText"]*: conteúdo textual do tweet que estamos acessando.


### Stale Elements (StaleElementReferenceException)
Isso já aconteceu com todo mundo. Você liga o computador, espera a área de trabalho carregar e clica no ícone que representa o atalho para algum programa. Ao clicar, o sistema avisa que o software não pode ser executado porque foi excluído ou desinstalado. A exceção ***StaleElementReferenceException*** acontece de uma forma semelhante.

Um "Stale Element" (Elemento Obsoleto ou Vencido) é um elemento que o WebDriver encontrou com sucesso em um momento, mas que, por alguma razão, não está mais válido ou anexado à página no momento em que você tenta interagir com ele. Isso pode acontecer porque a página foi carregada, o elemento foi removido ou até porque o elemento foi alterado de forma dinâmica pelo JavaScript. 

Temos diversas formas para evitar isso, como a **WebDriverWait**, que já falamos anteriormente. Além disso, no nosso código, cada post possui um index (ver linhas 170 e 183), que servirão para identificar cada post de forma individual. 

```post_id = f'{post_index}_{hash(post_text)}'```
O *post_id* é uma string formada pelo *post_index*, que é a posição dele na página; e pelo hash do *post_text*. O hash é a representação em números inteiros de algum objeto. Cada um deles será armazenado no nosso set *processed_posts*. Assim, nosso laço não corre o risco de nos lançar numa exceção de Stale Element.

Na parte final desta função, coletamos os comentários (através de uma outra função cuja implementação iremos discutir a seguir) e fazemos o armazenamento dos conteúdos textuais na nossa lista de dicionários **collected_data**. Caso ocorra algum problema, lançamos uma exceção para fechar nosso try, e no bloco *finally* realizamos o logoff e fechamos a página. 


## Detalhamento da coleta de comentários
A função ```collecting_comments``` foi colocada à parte para organizar melhor o código, deixando ele mais claro e menos complexo. Além disso, podemos tratar de forma menos confusa possíveis erros que possam acontecer nessa parte, evitando assim que o programa quebre por completo ao deixar tudo dentro de uma só função. 

O funcionamento da função é simples: procuramos elementos clicáveis na página que possuem o nome *status* na url. Para isso, utilizamos o seletor ```'a[href*="/status/"]'```. Em redes sociais como o X, normalmente esse seletor aponta para atualizações de status e postagens. Depois de abrir o post, salvamos em uma lista todos os elementos que achamos.

Agora iteramos sobre a lista criada pulando o primeiro elemento, que é a postagem principal, e coletamos os comentários. Extraímos o texto do comentário e adicionamos o conteúdo na lista **comments** (que utilizamos na função ```collecting_posts```). Por fim voltamos para a página inicial a fim de coletar os comentários de mais posts.