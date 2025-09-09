import re
import matplotlib.pyplot as plt
import pandas as pd
from LeIA import SentimentIntensityAnalyzer

def clean_text(text):
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'[^a-zA-Z\d\s]', '', text, flags=re.A)
    text = text.lower()
    text = re.sub(r'\s+', '', text)
    return text
    # ver README para detalhes


def saving_data(data, file_name='dados_coletados.csv'):
    if not data:
        print("Sem dados para mostrar/salvar.")
        return None
    
    #criando DataFrame:
    df = pd.DataFrame(data)

    print("Pré-processando os textos...")
    df['comment_text'] = df['comment_text'].apply(clean_text)

    df.to_csv(file_name, index=False)
    print(f"Dados salvos em {file_name}")
    return df


def sentiment_analyser(df, file_name='analise_sentimentos.csv'):
    if df is None:
        print("DataFrame inexistente; análise de sentimento não pode ser feita.")
        return None
    
    analyser = SentimentIntensityAnalyzer()
    
    def sentiment_classification(text):
        score = analyser.polarity_scores(text)

        if score['compound'] >= 0.05:
            return 'POSITIVO'
        elif score['compound'] <= -0.05:
            return 'NEGATIVO'
        else: 
            return 'NEUTRO'
        
    df['sentiment'] = df['comment_text'].apply(sentiment_classification)
    df_final = df[['post_code', 'news_channel', 'post_text', 'comment_text',
                    'sentiment']]

    df_final.to_csv(file_name, index=False)
    print(f"Análise de sentimento concluída com sucesso. \
          Arquivo CSV atualizado como '{file_name}'.")
    return df_final


def data_presentation(df):
    if df is None:
        print("DataFrame inexistente. Visualização cancelada.")
        return
    
    print("Gerando gráfico de resultados...")
    sentiments_counter = df.groupby(['post_code', 
                                     'sentiment']).size().unstack(fill_value=0)

    sentiments_counter.plot(kind='bar', stacked=False, figsize=(15,8),
                            color=['green', 'red', 'grey'])
    
    plt.title('Número de comentários por sentimento em cada postagem')
    plt.xlabel('Código da postagem')
    plt.ylabel('Número de comentários')
    plt.xticks(rotation=45)
    plt.legend(title='Sentimento')
    plt.tight_layout()
    plt.show()

