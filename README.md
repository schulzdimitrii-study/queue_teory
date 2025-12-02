# Queue Theory App

Aplicação web para cálculo e análise de **modelos de teoria de filas**, desenvolvida em Python com Flask e frontend interativo usando Alpine.js e Bootstrap.

## 📋 Descrição

Este projeto implementa diversos modelos clássicos de teoria de filas, permitindo calcular métricas de desempenho como taxa de utilização, tempo médio no sistema, número médio de clientes, entre outras.

## 🚀 Modelos Disponíveis

| Modelo | Notação | Descrição |
|--------|---------|-----------|
| MM1 | M/M/1 | Fila com chegadas Poisson, atendimento exponencial, 1 servidor |
| MMS | M/M/s | Fila com s servidores (s > 1) |
| MM1K | M/M/1/K | Fila M/M/1 com capacidade finita K |
| MM1N | M/M/1/N | Fila M/M/1 com população finita N |
| MMSK | M/M/s/K | Fila com s servidores e capacidade finita K |
| MMSN | M/M/s/N | Fila com s servidores e população finita N |
| MG1 | M/G/1 | Fila com chegadas Poisson e atendimento geral |
| MCPCI | M/M/c (Custo) | Modelo com análise de custo por cliente com capacidade infinita |
| MCPSI | M/M/c (Custo) | Modelo com análise de custo por servidor com capacidade infinita |

## 📊 Métricas Calculadas

| Símbolo | Descrição |
|---------|-----------|
| ρ (Rho) | Taxa de utilização do sistema |
| P₀ | Probabilidade do sistema estar vazio (não haver clientes) |
| Pₙ | Probabilidade de ter n clientes no sistema |
| Pᵣ | Probabilidade de ter r ou mais clientes no sistema |
| L | Número médio de clientes no sistema |
| Lq | Número médio de clientes na fila |
| W | Tempo médio no sistema |
| Wq | Tempo médio na fila |
| P(W > t) | Probabilidade do tempo no sistema exceder t |
| P(Wq > t) | Probabilidade do tempo na fila exceder t |

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3, Flask, Flask-CORS
- **Frontend**: HTML5, CSS3, Bootstrap 5, Alpine.js, HTMX
- **Testes**: Pytest

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/schulzdimitrii-study/queue_teory.git
cd queue_teory
```

2. Crie um ambiente virtual (recomendado):
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Execução

Para iniciar a aplicação:

```bash
python app.py
```

Acesse no navegador: `http://localhost:5000`

## 🧪 Testes

Para executar os testes:

```bash
pytest
```

## 📁 Estrutura do Projeto

```
queue_teory/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências do projeto
├── README.md              # Documentação
├── models/                # Modelos de filas
│   ├── base_queue.py      # Classe base abstrata
│   ├── mm1.py             # Modelo M/M/1
│   ├── mms.py             # Modelo M/M/s
│   ├── mm1k.py            # Modelo M/M/1/K
│   ├── mm1n.py            # Modelo M/M/1/N
│   ├── mmsk.py            # Modelo M/M/s/K
│   ├── mmsn.py            # Modelo M/M/s/N
│   ├── mg1.py             # Modelo M/G/1
│   ├── mcpci.py           # Modelo de custo por cliente
│   ├── mcpsi.py           # Modelo de custo por servidor
│   └── queue_factory.py   # Factory para criação de modelos
├── routes/                # Rotas da API
│   └── queues.py          # Endpoints de filas
├── templates/             # Templates HTML
│   ├── base.html          # Template base
│   └── home.html          # Página principal
└── static/                # Arquivos estáticos
    ├── css/
    │   └── style.css      # Estilos customizados
    └── js/
        └── form.js        # Scripts JavaScript
```

## 🔧 Parâmetros de Entrada

| Parâmetro | Símbolo | Descrição |
|-----------|---------|-----------|
| λ (lambda) | lamb | Taxa de chegada de clientes |
| μ (mu) | mu | Taxa de atendimento por servidor |
| s | s | Número de servidores |
| K | k | Capacidade máxima do sistema |
| N | N | Tamanho da população finita |
| n | n | Número de clientes para cálculo de Pₙ |
| r | r | Número de clientes para cálculo de Pᵣ |
| t | t | Tempo para cálculo de P(W > t) e P(Wq > t) |

## 📝 Licença

Este projeto é de uso acadêmico/educacional.

## 👤 Autor

Desenvolvido por [@schulzdimitrii-study](https://github.com/schulzdimitrii-study)