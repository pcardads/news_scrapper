# -*- coding: utf-8 -*-

import time
import getpass
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
                username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                break
            except:
                continue

        # caso não encontre:
        if not username_field:
            print("👀Campo USERNAME não encontrado ainda.")
            return False
        
        # caso encontre o campo USERNAME:
        print(f'✏️Campo sendo preenchido: username({username})')
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
                password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                break
            except:
                continue
        
        # caso não encontre:
        if not password_field:
            print("👀Campo SENHA ainda não encontrado.")
            return False
        
        # caso encontre o campo SENHA:
        print(f'✏️Campo sendo preenchido: senha({password})')
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
            print("✅O login foi feito com sucesso!")
            return True
        else:
            print("❌Login falhou. Por favor, verifique usuário e senha novamente.")
            return False
        
    except Exception as e:
        print(f"❌Falha! Erro durante login: {e}")
        return False
