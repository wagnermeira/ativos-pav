# Ativos PAV

Este repositório contém a aplicação web Flask para gerenciamento e atualização da planilha de ativos do prédio PAV. Técnicos podem preencher informações diretamente pela interface sem precisar de credenciais, e o sistema grava as alterações na própria planilha.

## Descrição do Projeto

- Leitura e escrita de planilha Excel (`ativos.xlsx`) usando **pandas** e **openpyxl**.
- Interface web leve em **Flask** com formulário único para todas as categorias de equipamento.
- Bloqueio de arquivo durante gravação para evitar corrupção por acessos simultâneos.
- Hospedagem em subdomínio, com deploy via Gunicorn e Nginx.

## Estrutura do Diretório

```
ativos-pav/
├── app.py             # Aplicação Flask principal
├── utils.py           # Funções de leitura/escrita com locking
├── templates/         # Templates Jinja2 (HTML)
│   └── form.html      # Formulário de preenchimento
├── static/            # Arquivos estáticos (CSS, JS)
├── ativos.xlsx        # Planilha original de ativos
└── README.md          # Este arquivo de documentação
```

## Pré-requisitos

- Python 3.8 ou superior
- pip

## Instalação e Execução Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/wagnermeira/ativos-pav.git
   cd ativos-pav
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação Flask em modo de desenvolvimento:
   ```bash
   flask run
   ```
5. Acesse `http://127.0.0.1:5000` no navegador.

## Deploy em Produção

- Configure Gunicorn e Nginx para servir `app:create_app()` no subdomínio desejado.
- Utilize Certbot para HTTPS.

## Contribuindo

1. Abra uma _issue_ para sugerir melhorias ou reportar bugs.
2. Crie uma _branch_ para sua feature ou correção:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. Faça commit das suas alterações e abra um _pull request_.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

