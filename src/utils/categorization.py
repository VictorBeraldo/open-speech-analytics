import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
tqdm.pandas()

def process_text_and_train_model(df, text_column, label_column, additional_stopwords=None, max_depth=2, min_samples_leaf=10, random_state=0):
    """
    Filtra stopwords de uma coluna de texto em um DataFrame, treina um modelo de árvore de decisão e extrai regras de decisão.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    text_column (str): Nome da coluna de texto.
    label_column (str): Nome da coluna de rótulo.
    additional_stopwords (list, optional): Lista de stopwords adicionais. Default é None.
    max_depth (int, optional): Profundidade máxima da árvore de decisão. Default é 2.
    min_samples_leaf (int, optional): Número mínimo de amostras por folha. Default é 10.
    random_state (int, optional): Semente aleatória para reprodução. Default é 0.

    Retorna:
    tuple: Relatório de classificação, lista de regras da árvore de decisão e o modelo.
    """
    
    # Definir as stopwords em português e adicionar palavras personalizadas
    stop_words = set(stopwords.words('portuguese'))
    if additional_stopwords:
        stop_words.update(additional_stopwords)

    # Função para filtrar stopwords de um texto
    def filtrar_stopwords(texto):
        palavras = word_tokenize(texto)
        palavras_filtradas = [palavra for palavra in palavras if palavra.lower() not in stop_words]
        return ' '.join(palavras_filtradas)

    # Aplicar a função de filtragem com progresso
    df['Texto_Filtrado'] = df[text_column].progress_apply(filtrar_stopwords)

    # Pipeline de processamento de texto e modelo
    vectorizer = CountVectorizer()
    model = DecisionTreeClassifier(random_state=random_state, max_depth=max_depth, min_samples_leaf=min_samples_leaf)
    pipeline = make_pipeline(vectorizer, model)

    # Treinar modelo
    pipeline.fit(df['Texto_Filtrado'], df[label_column])

    # Mostrar relatório de classificação
    classification_rep = classification_report(df[label_column], pipeline.predict(df['Texto_Filtrado']))

    # Função para obter regras
    def get_rules(tree, feature_names, class_names):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        paths = []
        path = []

        def recurse(node, path, paths):
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                p1, p2 = list(path), list(path)
                p1 += [f"({name} <= {np.round(threshold, 3)})"]
                recurse(tree_.children_left[node], p1, paths)
                p2 += [f"({name} > {np.round(threshold, 3)})"]
                recurse(tree_.children_right[node], p2, paths)
            else:
                path += [(tree_.value[node], tree_.n_node_samples[node])]
                paths += [path]

        recurse(0, path, paths)

        # sort by samples count
        samples_count = [p[-1][1] for p in paths]
        ii = list(np.argsort(samples_count))
        paths = [paths[i] for i in reversed(ii)]

        rules = []
        for path in paths:
            rule = "if "
            for p in path[:-1]:
                if rule != "if ":
                    rule += " and "
                rule += str(p)
            rule += " then "
            if class_names is None:
                rule += "response: " + str(np.round(path[-1][0][0][0], 3))
            else:
                classes = path[-1][0][0]
                l = np.argmax(classes)
                rule += f"class: {class_names[l]} (proba: {np.round(100.0 * classes[l] / np.sum(classes), 2)}%)"
            rule += f" | based on {path[-1][1]:,} samples"
            rules += [rule]

        return rules

    # Obter e imprimir regras
    rules = get_rules(model, vectorizer.get_feature_names_out().tolist(), ['Não relevante', 'Relevante'])

    return classification_rep, rules, model