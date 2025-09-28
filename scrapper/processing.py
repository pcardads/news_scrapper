import re
import matplotlib.pyplot as plt
import pandas as pd
import os

from LeIA import SentimentIntensityAnalyzer

#pré processando o texto(nesse caso os comentários) através de expressões regulares
def clean_text(text):
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\@\w+|\#', '', text)
    #text = re.sub(r'[^a-zA-Z\d\s]', '', text, flags=re.A)
    text = text.lower()
    return text
    # ver README para detalhes

# salvandos os dados coletados em collecting_posts e collecting_comments
# assim como também se o arquivo csv já existe e também pré-processando os
# dados 
def saving_data(data, csv_filename='dados_coletados.csv'):
    if not data:
        print("Sem dados para mostrar/salvar.")
        return None
    
    # verificando se há um arquivo csv existente(de uma execução prévia) caso exista será deletado 
    if os.path.isfile(csv_filename):
        try:
            os.remove(csv_filename)
            #print(f"O arquivo '{csv_filename}' já existia(devido a uma execução anterior), portanto será deletado o antigo e criado um novo.")
        except Exception as e:
            print(f"Erro ao deleletar o arquivo '{csv_filename}': {e}")

    #criando DataFrame:
    df = pd.DataFrame(data)

    print("Pré-processando os textos...")
    df['comment_text'] = df['comment_text'].apply(clean_text)

    df.to_csv(csv_filename, index=False)
    print(f"Dados salvos em {csv_filename}")
    


def sentiment_analyser(text):
    if not (isinstance(text, str)):
        return
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(text)            
    if score['compound'] >= 0.05:
        return 'POSITIVO'
    elif score['compound'] <= -0.05:
        return 'NEGATIVO'
    else: 
        return 'NEUTRO'

# adiciona a coluna sentimento no arquivo .csv lendo os dados coletados do arquivo através
# do pandas e análisa cada elemento da coluna de comentários(comment_text) através da análise
# de sentimento(sentiment_analyser) que utiliza a biblioteca leIA e salva todas as alterações 
# do arquivo .csv através do pandas(df.to_csv)
def add_sentiment(csv_filename='dados_coletados.csv' ):
    df = pd.read_csv(csv_filename)
    if df is None:
        print("DataFrame inexistente; análise de sentimento não pode ser feita.")
        return None
    df['sentiment'] = df['comment_text'].apply(sentiment_analyser)
    df.to_csv(csv_filename, index=False)
    print(f"Análise de sentimento concluída com sucesso. \n Arquivo CSV atualizado como '{csv_filename}'.")
    return df

#criação do gráfico através do matplolib baseada na contagem do número de comentários por postagem  
def data_presentation(df):
    if df is None:
        print("DataFrame inexistente. Visualização cancelada.")
        return
    
    print("Gerando gráfico de resultados...")
    sentiments_counter = df.groupby(['post_code', 
                                     'sentiment']).size().unstack(fill_value=0)

    sentiments_counter.plot(kind='bar', stacked=False, figsize=(15,8),
                            color=['red', 'grey', 'green'])
    
    plt.title('Número de comentários por sentimento em cada postagem')
    plt.xlabel('Código da postagem')
    plt.ylabel('Número de comentários')
    plt.xticks(rotation=45)
    plt.legend(title='Sentimento')
    plt.tight_layout()
    plt.show()

