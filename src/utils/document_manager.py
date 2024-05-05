import pandas as pd
import ast
from langchain.schema import Document
import os
import shutil

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