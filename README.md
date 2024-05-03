# open-speech-analytics

# To-Do List para o Repositório GitHub

- [x] 1. Criar uma lista de vídeos.
- [x] 2. Gerar lista de transcrições utilizando Whisper Local com e sem GPU.
- [x] 3. Elaborar lista de resumos.
- [ ] 4. Implementar categorização multiclasse com categorias pré-definidas (Zero Shot), como Renda Fixa, Ações, etc.
- [ ] 5. Desenvolver gráfico de série temporal com Streamlit para visualizar as categorias.
- [ ] 6. Desenvolver um chat que permite interação com dados e criação de novas categorias.
- [ ] 7. Integrar chat com resumos usando Langchain para testar categorias por prompt.
- [ ] 8. Feedback
     - [ ] a. Implementar funcionalidade para ouvir ligações com transcrição para validar categorias.
- [ ] 9. Escrever conclusão e incluir disclaimer.

# Organização do Repositório
## Estrutura de Pastas

```plaintext
projeto/
│
├── notebooks/                  # Jupyter notebooks para análise e demonstração
│   └── main.ipynb              # Notebook principal
│
├── src/                        # Códigos fonte do projeto
│   ├── chat/                   # Códigos para o chat
│   ├── categorization/         # Scripts para categorização
│   ├── visualization/          # Scripts para visualizações com Streamlit
│   ├── transcription/          # Scripts para transcrição com Whisper
│   └── utils/                  # Scripts utilitários
│
├── data/                       # Dados utilizados no projeto
│   ├── links/                  # Links de videos em .csv
│   ├── videos/                 # Vídeos para transcrição em .m4a
│   ├── transcripts/            # Transcrições geradas em .csv
│   └── summaries/              # Resumos dos vídeos
│
├── requirements.txt            # Dependências do Python
└── README.md                   # Documentação do projeto
└── setup.py                    # Este arquivo descreverá seu pacote e como instalá-lo.


