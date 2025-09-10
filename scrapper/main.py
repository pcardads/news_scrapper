from datamining import collecting_posts
from processing import saving_data, sentiment_analyser, data_presentation
import getpass

def scrapper():
    print("INICIANDO SCRAPPING E DATAMINING NO X...")
    print("=" * 50)
    print("- Utilize uma conta válida do X.")
    print("- Para mais segurança, utilize uma conta secundária.")
    print("- Uso de conta principal pode resultar em block.")
    print("=" * 50)

    print("\nDigite as credenciais:")
    username = input("Username/Email: ").strip()
    password = getpass.getpass("Senha: ")

    if not username or not password:
        print("Username e senha são obrigatórios.")
        return
    
    print("Perfil para analisar: ")
    profile = input("Digite o nome do perfil para analisar sem o '@': ").strip()

    if not profile:
        profile = "folha"

    url = f"https://x.com/{profile}"

    print(f"Iniciando a coleta em {url}. Aguarde...")

    data = collecting_posts(url, username, password, num_posts=10)
    if data:
        valid_comments = len([d for d in data if d['comment_text'].strip()])

        if valid_comments > 0:
            print(f"COncluído. {valid_comments} comentários encontrados.")
            print("\nProcessando dados...")
            df = saving_data(data, f"dados_coletados_{profile}.csv")
            df_final = sentiment_analyser(df, 
                                          f"analise_sentimentos_{profile}.csv")
            data_presentation(df_final)

        else:
            print("Nenhum comentário encontrado.")
            print("Perfil pode ter comentários desabilitados ou X \
                  detectou automação.")
            
    else:
        print("Nenhum dado coletado no momento; verifique o login.")

if __name__ == "__main__":
    print("MINERANDO DADOS DO X")
    print("=" * 50)

    answer = input("Executar coleta com login? (s/n): ").strip().lower()
    if answer in ['s', 'sim', 'y', 'yes']:
        scrapper()
    else:
        print("Sair do programa...")