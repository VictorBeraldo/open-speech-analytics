import pandas as pd
import ast
from langchain.schema import Document
import os
import shutil
from langchain_community.document_loaders import DataFrameLoader
from unidecode import unidecode


def save_docs_to_csv(docs, file_path):
    """Salva uma lista de documentos LangChain em um arquivo CSV."""
    # Converter documentos para um formato que pode ser salvo em CSV
    data = [{
        "content": doc.page_content,
        "metadata": str(doc.metadata)  # Convertendo metadados em string
    } for doc in docs]

    # Criar DataFrame
    df = pd.DataFrame(data)

    # Salvar DataFrame como CSV
    df.to_csv(file_path, index=False)

    print(f"Documentos salvos em {file_path}")



def load_docs_from_csv(file_path):
    """Carrega documentos de um arquivo CSV para o formato LangChain Document."""
    # Carregar DataFrame de CSV
    df_loaded = pd.read_csv(file_path)

    # Converter os dados carregados de volta para o formato de documento LangChain
    docs_loaded = [
        Document(
            page_content=row['content'],
            metadata=ast.literal_eval(row['metadata'])  # Convertendo string para dicionário
        )
        for index, row in df_loaded.iterrows()
    ]

    print(f"Documentos carregados de {file_path}")
    return docs_loaded


def delete_contents(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            



def normalizar_string(texto):
    """
    Normaliza uma string removendo acentos e caracteres especiais.

    Args:
        texto (str): O texto a ser normalizado.

    Returns:
        str: O texto normalizado.
    """
    return ''.join(
        unidecode(char) if not char.isalpha() else char
        for char in texto
    )

def carregar_dados(caminho_resumos, caminho_links):
    """
    Carrega dados de arquivos CSV, normaliza strings e mescla dataframes.

    Args:
        caminho_resumos (str): Caminho para o arquivo CSV contendo os resumos.
        caminho_links (str): Caminho para o arquivo CSV contendo os links.

    Returns:
        pd.DataFrame: DataFrame mesclado e processado.
    """
    df_summary = pd.read_csv(caminho_resumos)
    df_links = pd.read_csv(caminho_links)
    
    df_summary["Source"] = df_summary["Source"].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
    df_summary['Source'] = df_summary['Source'].apply(normalizar_string)
    df_links['titulo'] = df_links['titulo'].apply(normalizar_string)
    
    df = pd.merge(df_summary, df_links, left_on="Source", right_on="titulo")
    df = df.dropna(axis=1)
    df = df.drop('keywords', axis=1)
    
    return df