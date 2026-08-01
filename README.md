# AI Agent - RAG System with Local LLM

## Sobre o projeto

Este projeto implementa um **AI Agent baseado em RAG (Retrieval-Augmented Generation)**, permitindo realizar perguntas utilizando informações extraídas de documentos 
PDF. A aplicação utiliza uma arquitetura onde os documentos são processados, transformados em vetores semânticos e armazenados em um banco vetorial. Durante uma 
consulta, o sistema recupera os trechos mais relevantes da base de conhecimento e envia essas informações para um modelo de linguagem local, que gera a resposta baseada
exclusivamente no conteúdo encontrado. O projeto foi desenvolvido com foco em **IA generativa, processamento de documentos, embeddings, busca semântica e execução 
local de modelos de linguagem**, evitando dependência de APIs externas.

---

## Tecnologias utilizadas

* Python 3.14

## Frameworks e bibliotecas

### LangChain

Framework utilizado para construção do pipeline de inteligência artificial, gerenciamento de prompts, integração com modelos de linguagem e manipulação de documentos.

### ChromaDB

Banco de dados vetorial responsável pelo armazenamento dos embeddings gerados a partir dos documentos. Utilizado para realizar buscas por similaridade semântica.

### HuggingFace Embeddings

Responsável pela criação dos vetores numéricos dos documentos utilizando o modelo:

```
sentence-transformers/all-MiniLM-L6-v2
```

Esse modelo transforma textos em representações vetoriais capazes de capturar significado e contexto.

### Ollama

Servidor local utilizado para execução do Large Language Model (LLM).

Modelo utilizado:

```
llama3.1
```

A utilização de um modelo local elimina custos de API e permite execução sem envio de dados para serviços externos.

### PyPDF

Biblioteca utilizada para leitura e extração de conteúdo de arquivos PDF.

---

## Arquitetura do projeto

O projeto segue o conceito de **RAG (Retrieval-Augmented Generation)**.

Fluxo da aplicação:

```
                PDF Documents
                     |
                     v
          Document Loader (PyPDF)
                     |
                     v
        Text Splitter (Chunking)
                     |
                     v
        HuggingFace Embeddings
                     |
                     v
              ChromaDB
          (Vector Database)


                     |
                     v

              User Question
                     |
                     v
          Semantic Search Retriever
                     |
                     v
          Relevant Document Chunks
                     |
                     v
              Prompt Template
                     |
                     v
            Ollama - Llama 3.1
                     |
                     v
              Generated Answer
```

---

## Estrutura do projeto

```
AIAgent
│
├── app
│   └── __main__.py
├── database
    └── create_database.py
├── base
│   └── .gitkeep.pdf
│
├── chroma_db
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
```

---

## Funcionamento

## 1. Criação da base vetorial

O arquivo `create_database.py` é responsável por:

* Carregar documentos PDF
* Dividir o texto em pequenos blocos
* Criar embeddings
* Armazenar os vetores no ChromaDB

Processo:

```python
PDF
 ↓
Document Loader
 ↓
Text Splitter
 ↓
Embeddings
 ↓
Vector Database
```

---

## 2. Adicionando documentos

Para utilizar o agente, adicione seus arquivos PDF dentro da pasta:

base/

Exemplo:

base/
└── meu_documento.pdf

Após adicionar os documentos, execute novamente o processo de criação do banco vetorial:

python app/create_database.py

---

## 3. Recuperação de informações

Quando o usuário realiza uma pergunta:

1. A pergunta é convertida em vetor.
2. O sistema busca os documentos semanticamente mais próximos.
3. Os trechos encontrados são adicionados ao contexto do prompt.

Configuração utilizada:

```python
search_kwargs={"k":4}
```

Isso significa que os 4 documentos mais relevantes são recuperados.

---

## 4. Geração da resposta

O modelo recebe:

* Pergunta do usuário
* Contexto recuperado do banco vetorial
* Regras definidas no prompt

O modelo deve responder utilizando apenas a informação encontrada na base.

Caso não encontre informação:

```
I could not find this information in the knowledge base.
```

---

## Estratégia de Prompt

O sistema utiliza um prompt restritivo:

```
Answer the user's question using ONLY the information contained in the knowledge base.
```

Essa abordagem reduz respostas inventadas pelo modelo (**hallucinations**) e mantém a resposta baseada nos documentos fornecidos.

---

## Instalação

## Clone o projeto

```bash
git clone https://github.com/seu-usuario/AIAgent.git
```

Acesse o diretório:

```bash
cd AIAgent
```

---

## Criar ambiente virtual

Windows:

```powershell
python -m venv .venv
```

Ativar:

```powershell
.\.venv\Scripts\Activate
```

---

## Instalar dependências

```powershell
pip install -r requirements.txt
```

---

## Configuração do Ollama

Instale o Ollama e baixe o modelo:

```bash
ollama pull llama3.1
```

Inicie o servidor:

```bash
ollama serve
```

O Ollama será executado localmente em:

```
http://localhost:11434
```

---

## Executando o projeto

## Criar banco vetorial

Adicione seus PDFs dentro da pasta:

```
base/
```

Execute:

```powershell
python app/create_database.py
```

Resultado esperado:

```
Vector database created successfully.
```

---

## Fazer perguntas ao agente

Execute:

```powershell
python app/__main__.py
```

Exemplo:

```
Write your question:
What is this document about?
```

Resposta:

```
AI Response:

The document describes...
```

---

## Privacidade e custos

Este projeto utiliza processamento local:

✅ Sem necessidade de API Key
✅ Sem envio de documentos para serviços externos
✅ Sem custos por requisição
✅ Controle total sobre os dados

O modelo de linguagem é executado através do Ollama localmente.

---

## Conceitos aplicados

* Generative AI
* Large Language Models (LLM)
* Retrieval-Augmented Generation (RAG)
* Vector Database
* Semantic Search
* Embeddings
* Prompt Engineering
* Document Processing
* Local AI Deployment
