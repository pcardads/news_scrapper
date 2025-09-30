from datamining import collecting_posts
from processing import saving_data, add_sentiment, data_presentation
import getpass

# Nome e matrícula dos membros da Equipe

# Nome: Erik Santos Bezerra
# Matrícula: 2424108
# Nome: Felipe Rocha Simiao
# Matrícula: 2514917
# Nome: Luiz Alberto Pessoa Júnior
# Matrícula: 2425141
# Nome: Maria Eduarda Menezes Oliveira
# Matrícula: 2415599
# Nome: Mateus Silvestre Estevam
# Matrícula: 2514879
# Nome: Paulo Cardoso Ferreira
# Matrícula: 2425190
# link do video: https://drive.google.com/file/d/1DVysPswPpawitPiDBxN8EiqPGR-M35yH/view?usp=sharing


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
        profile = "g1"

    url = f"https://x.com/{profile}"

    print(f"Iniciando a coleta em {url}. Aguarde...")
   
   #id="id__mmhakyzgvor" id de um tweet com ad

    data = collecting_posts(url, username, password, num_posts=30)
    if data:
        valid_comments = len([d for d in data if d['comment_text'].strip()])

        if valid_comments > 0:
            print(f"Concluído. {valid_comments} comentários encontrados.")
            print("\nProcessando dados...")
            csv_filename = f"dados_coletados_{profile}.csv"
            saving_data(data, csv_filename)
            df_updated = add_sentiment(csv_filename)
            data_presentation(df_updated)

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