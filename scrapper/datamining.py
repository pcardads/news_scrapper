# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

#Função que serve para o usuário do programa fazer login no X
def login_twitter(driver, username, password):
    try:
        print("Por favor, aguarde. Preparando ambiente... ⌛")
        driver.get("https://x.com/i/flow/login")
        time.sleep(5) # para dar tempo de carregar a página (ver documentação)

        wait = WebDriverWait(driver, 20)

        # encontrando campo para usuário inserir USERNAME
        username_selectors = [
            'input[name="text"]',
            'input[autocomplete="username"]',
            'input[data-testid="ocfEnterTextTextInput"]',
            'input[placeholder*="email"]',
            'input[placeholder*="username"]'
        ]
        # a lista acima possui uma série de seletores CSS utilizados para
        # interagir com os campos de usuário de um site (ver documentação)

        username_field = None
        for selector in username_selectors:
            try:
                username_field = wait.until(EC.presence_of_element_located
                                            ((By.CSS_SELECTOR, selector)))
                break
            except:
                continue

        # caso não encontre:
        if not username_field:
            print("Campo USERNAME não encontrado.")
            return False
        
        # caso encontre o campo USERNAME:
        print(f'Campo sendo preenchido: username')
        username_field.clear()
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)
        time.sleep(3)

        # encontrando campo para usuário inserir SENHA:
        password_selectors = [
            'input[name="password"]',
            'input[type="password"]',
            'input[data-testid="ofcEnterTextTextInput"]',
            'input[placeholder*="password"]'
        ]
        # a lista acima possui uma série de seletores CSS utilizados para
        # interagir com os campos de senha de um site (ver documentação)

        password_field = None
        for selector in password_selectors:
            try:
                password_field = wait.until(EC.presence_of_element_located
                                            ((By.CSS_SELECTOR, selector)))
                break
            except:
                continue
        
        # caso não encontre:
        if not password_field:
            print("Campo SENHA não encontrado.")
            return False
        
        # caso encontre o campo SENHA:
        print(f'Campo sendo preenchido: senha')
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        # agora, falta somente verificar se o login deu certo ou não
        login_indicators = [
            '[data-testid="SideNav_AccountSwitcher_Button"]',
            '[data-testid="AppTabBar_Home_Link"]',
            '[aria-label="Home"]',
            'a[href="/home"]'
        ]

        logged_in = False
        for indicator in login_indicators:
            try:
                element = driver.find_element(By.CSS_SELECTOR, indicator)
                if element:
                    logged_in = True
                    break
            except:
                continue

        if logged_in:
            print("O login foi feito com sucesso!")
            return True
        else:
            print("Login falhou. Por favor, verifique usuário e senha " \
            "novamente.")
            return False
        
    except Exception as e:
        print(f"Falha! Erro durante login: {e}")
        return False

def collecting_posts(url, username, password, num_posts=5):
    
    # configs do navegador (ver README)
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Tenta usar chromedriver já instalado, se não conseguir, baixar
    try:
        driver = webdriver.Chrome(options=options)
    except:
        # Fallback para o ChromeDriverManager se o driver não estiver no PATH
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                                  options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', " \
    "{get: () => undefined})")

    try:
        if not login_twitter(driver, username, password):
            print("Erro! Não foi possível fazer o login.")
            return []
        
        print(f"Acessando: {url}")
        driver.get(url)
        time.sleep(8)

        # extraindo só o nome do portal de notícias:
        news_channel = url.split('/')[-1] if url.split('/')[-1] \
                       else url.split('/')[-2]
        
        if not news_channel.startswith('@'):
            news_channel = '@' + news_channel

        collected_data = []
        processed_posts = set() # para evitar repetições (ver README)
        collected_posts = 0
        scrollings = 0
        max_scrollings = 60

        print(f'Coletando dados do portal {news_channel}')
        #print(f'numposts = {num_posts}, max_scrollings = {max_scrollings}') 
        while collected_posts < num_posts and scrollings < max_scrollings:
            print(f'colletcted_posts = {collected_posts}, scrollings = {scrollings}') 
            # começa a busca pelos posts
            posts = driver.find_elements(By.CSS_SELECTOR, 
                                         'article[data-testid="tweet"]')
            
            if not posts:
                print("Nenhum post foi encontrado na página.")
                driver.execute_script("window.scrollTo"
                "(0, document.body.scrollHeight);")
                time.sleep(5)
                scrollings += 1
                continue

            print(f'Foram encontrados {len(posts)} posts na página.')
            posts_on_iteration = 0

            for post_index in range(len(posts)):
                if collected_posts >= num_posts:
                    break

                try:
                    # realiza nova busca para evitar stale elements (ver README)
                    posts_now = driver.find_elements(
                        By.CSS_SELECTOR, 'article[data-testid="tweet"]'
                        )
                    
                    if post_index >= len(posts_now): # posição na página
                        continue

                    post = posts_now[post_index]

                    text_elements = post.find_elements(
                        By.CSS_SELECTOR, '[data-testid="tweetText"]'
                        )
                    post_text = ""
                    if text_elements:
                        post_text = text_elements[0].text

                    if not post_text.strip():
                        continue

                    #verificando posts (buscas) duplicados:
                    post_id = f'{post_index}_{hash(post_text)}'
                    if post_id in processed_posts:
                        continue

                    processed_posts.add(post_id)
                    posts_on_iteration += 1
                    post_code = collected_posts + 1

                    print(f'Post {post_code}: {post_text[:50]}...')

                    # coleta de comentários
                    comments = collecting_comments(driver, post, post_index)

                    if not comments:
                        comments = [""]

                    for comment in comments:
                        collected_data.append({
                            "post_code": post_code,
                            "news_channel": news_channel,
                            "post_text": post_text,
                            "comment_text": comment
                        })

                    valid_comments = len([c for c in comments if c.strip()])
                    print(f"Foram coletados {valid_comments} comentários.")

                    collected_posts += 1

                except Exception as e:
                    print(f'Erro no post {post_index}: {e}')
                    continue

            if collected_posts < num_posts:
                print(f"Rolando a página... ({collected_posts}/{num_posts})")
                driver.execute_script("window.scrollTo"
                "(0, document.body.scrollHeight);")
                time.sleep(5)
                scrollings += 1

    except Exception as e:
        print(f'Falha! Erro durante a coleta: {e}')

    finally:
        print("Fazendo logout e fechando o navegador...")
        try:
            driver.get("https://x.com/logout")
            time.sleep(2)
        except Exception as e:
            print("Não conseguiu fazer logout.")
        driver.quit()

    comments_finded = len([d for d in collected_data if d['comment_text'].strip()])
    print("Finalizamos a coleta!")
    print(f"Foram coletados {len(collected_data)} posts, " \
          f"sendo {comments_finded} com comentários.")

    return collected_data

def collecting_comments(driver, post, post_index):
    comments = []
    comments_id = []
    try:
        clickable_elements = post.find_elements(By.CSS_SELECTOR, 
                                                'a[href*="/status/"]')
        print("clickable elements: ", len(clickable_elements))
        if clickable_elements:
            original_url = driver.current_url

            driver.execute_script("arguments[0].click();", 
                                  clickable_elements[0])
            print(f"Abrindo um post...")
            time.sleep(6)

            
            searching_comments = True
            #contador para comentários duplicados dentro de um post, 
            # assim comparando os ids únicos(snowflake id)
            duplicate_comment = 0 
            while(searching_comments):

                # 3 é o número de rolagens que vamos fazer, para 
                # carregar mais comentários
                for i in range(4): 
                    driver.execute_script("window.scrollTo(0, " \
                    "window.scrollY + 800);")
                    time.sleep(3)
                

                comment_elements = driver.find_elements(
                    By.CSS_SELECTOR, 
                    'article[data-testid="tweet"]'
                )  
                if(len(comment_elements) <= 1):
                    break
                print(f"Encontrados {len(comment_elements)} elementos.")
                

                for comment_index, comment_element in enumerate(
                    comment_elements[1:], 1
                ):
                    try:
                        comment_text_elements = comment_element.find_elements(
                            By.CSS_SELECTOR, 
                            '[data-testid="tweetText"]'
                        )
                        comment_links = comment_element.find_elements(
                            By.CSS_SELECTOR, 
                            'a'
                        )
                        # comment_spans = comment_element.find_elements(
                        #     By.CSS_SELECTOR, 'span'
                        # )   
                        
                        # for i in range(len(comment_spans)):
                        #     print("SPANS: ", comment_spans[i].text)
                        



                        if comment_text_elements: 
                            #id único de um post no x, é a numeração que aparece no link de um post                  
                            snowflake_id = 0
                            for i in range(len(comment_links)):
                              comment_link = comment_links[i].get_attribute("href").split('/')
                              #print("URL:", comment_link)
                              if(len(comment_link) >= 6 and comment_link[5].isdigit()):
                                snowflake_id = comment_link[5]
                                #print("SNOWFLAKE_ID: ", snowflake_id)
                                break
                              
                            #print("CURRENT URL: ", comment_snowflake_ids[i].get_attribute("href").split('/'))

                            commentary_text = comment_text_elements[0].text
                            #print("comentario atual", comment_text_elements[0].text)
                            
                            if snowflake_id in comments_id:
                                duplicate_comment  += 1
                                print("procurando comentários duplicados com base no snowflake id(necessário 3 para parar a coleta), " +  
                                "contador de cometário duplicado: ", duplicate_comment)
                                if(duplicate_comment >= 1 and duplicate_comment <= 2):
                                    continue
                                print("comentário duplicado identificado, parando a coleta de comentários")
                                searching_comments = False
                                break
                            if commentary_text.strip() and len(commentary_text) > 5:
                                duplicate_comment = 0
                                comments.append(commentary_text)
                                comments_id.append(snowflake_id)
                                #print(f"Comentário {comment_index}: {commentary_text[:40]}...")
                        else:
                            searching_comments = False
                            break      
                    except Exception as e:
                        print(f"Erro no comentário {comment_index}: {e}.")
                        continue
            
            # voltando para a página inicial
            driver.back()
            time.sleep(3)
        
        else:
            print(f"Post não encontrado.")

    except Exception as e:
        print(f"Erro ao coletar os comentários da postagem: {e}.")
    
    for i in range(len(comments)):
        comment_counter = i+1
        print(f"Comentário {comment_counter}: {comments[i][:40]}...")

    return comments
