import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="ticks")

#Aqui você deve clocar o caminho do seu diretório.
file_path = r''
#Ex: file_path = r'C:\Users\guilh\OneDrive\Desktop\Code\batutinhas.txt'

def process_whatsapp_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()

    messages = []
    dates = []
    authors = []
    
    for line in data:
        match = re.match(r'(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - (.*?): (.*)', line)
        if match:
            date_str, time_str, author, message = match.groups()
            datetime_str = f"{date_str} {time_str}"
            messages.append(message)
            dates.append(datetime_str)
            authors.append(author)

    df = pd.DataFrame({"Message": messages, "DateTime": dates, "Author": authors})
    df["DateTime"] = pd.to_datetime(df["DateTime"], format='%d/%m/%Y %H:%M')
    return df

chat_df = process_whatsapp_chat(file_path)

total_linhas = len(chat_df) 
print("Total de linhas no arquivo:", total_linhas)

if chat_df.empty:
    print("O DataFrame está vazio. Verifique o arquivo de entrada e o formato das mensagens.")
else:
    mensagens_por_pessoa = chat_df['Author'].value_counts()
    print("Mensagens por pessoa:\n", mensagens_por_pessoa)

    pessoa_mais_fala = mensagens_por_pessoa.idxmax()
    quantidade_mensagens = mensagens_por_pessoa.max()
    print(f"A pessoa que mais fala é {pessoa_mais_fala}, com {quantidade_mensagens} mensagens.")

    plt.figure(figsize=(10, 6))
    sns.barplot(x=mensagens_por_pessoa.index, y=mensagens_por_pessoa.values, palette="viridis")
    plt.title('Número de Mensagens por Pessoa')
    plt.xlabel('Pessoa')
    plt.ylabel('Número de Mensagens')
    plt.xticks(rotation=45)
    plt.show()

    df_mensagens_por_pessoa = mensagens_por_pessoa.reset_index()
    df_mensagens_por_pessoa.columns = ['Pessoa', 'Quantidade de Mensagens']

    total_mensagens = df_mensagens_por_pessoa['Quantidade de Mensagens'].sum()
    df_mensagens_por_pessoa.loc[len(df_mensagens_por_pessoa)] = ['Total', total_mensagens]

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=df_mensagens_por_pessoa.values, colLabels=df_mensagens_por_pessoa.columns, cellLoc='center', loc='center')
    ax.set_title('Quantidade de Mensagens')
    plt.show()

    all_messages = ' '.join(chat_df['Message']).lower()
    words = all_messages.split()
    words = [word for word in words if len(word) >= 4]
    
    word_series = pd.Series(words)
    word_counts = word_series.value_counts()
    
    word_counts = word_counts.nlargest(len(word_counts)).iloc[2:]

    most_common_words = word_counts.head(5)

    print("\n5 palavras mais usadas no grupo")
    for word, count in most_common_words.items():
        print(f"{word}: {count} vez(es)")

    if not most_common_words.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=most_common_words.index, y=most_common_words.values, palette="rocket")
        plt.title('5 Palavras Mais Usadas no Grupo')
        plt.xlabel('Palavras')
        plt.ylabel('Frequência')
        plt.xticks(rotation=45)
        plt.show()
    else:
        print("Não há palavras suficientes para exibir.")

    chat_df['Date'] = chat_df['DateTime'].dt.date
    mensagens_por_dia = chat_df.groupby('Date').size()

    plt.figure(figsize=(12, 6))
    sns.lineplot(x=mensagens_por_dia.index, y=mensagens_por_dia.values)
    plt.title('Nível de Interação por Dia')
    plt.xlabel('Data')
    plt.ylabel('Número de Mensagens')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

    mensagens_por_dia_pessoa = chat_df.groupby(['Date', 'Author']).size().unstack(fill_value=0)

    plt.figure(figsize=(14, 7))
    for pessoa in mensagens_por_dia_pessoa.columns:
        sns.lineplot(x=mensagens_por_dia_pessoa.index, y=mensagens_por_dia_pessoa[pessoa], label=pessoa)
    plt.title('Número de Mensagens por Dia e Pessoa')
    plt.xlabel('Data')
    plt.ylabel('Número de Mensagens')
    plt.xticks(rotation=45)
    plt.legend(title='Pessoa')
    plt.grid(True)
    plt.show()
