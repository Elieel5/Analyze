📊 Dashboard de Análise de Vendas
Este projeto oferece uma aplicação interativa usando Streamlit para visualizar e acompanhar o desempenho de vendas ao longo do tempo. Ele permite o upload de arquivos CSV, filtra por produtos e datas, e exibe gráficos claros sobre evolução e crescimento percentual.


🚀 Funcionalidades
- Upload de arquivo .csv com dados de vendas
- Filtro por produtos e intervalo de datas
- Cálculo automático de métricas:
- Total vendido
- Média mensal
- Crescimento total percentual
- Gráficos interativos:
- Vendas mensais
- Crescimento percentual
- Gráfico combinado (vendas + crescimento)
- Botão para download dos gráficos gerados

🛠️ Tecnologias Utilizadas
- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn

📁 Estrutura de Arquivos
📦 projeto-analise-vendas/
* ┣ 📜 app.py                # Código principal do dashboard
* ┣ 📜 requirements.txt      # Lista de dependências
* ┣ 📜 .gitignore            # Ignora arquivos desnecessários, como `.venv/`
* ┗ 📁 .venv/                # Ambiente virtual (não incluído no repositório)



⚙️ Como Rodar o Projeto Localmente
- Clone o repositório
git clone https://github.com/seu-usuario/projeto-analise-vendas.git
cd projeto-analise-vendas
- Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
- Instale as dependências
pip install -r requirements.txt
- Execute o aplicativo
streamlit run app.py



📦 Como preparar seu arquivo CSV
Certifique-se de que o CSV contenha pelo menos as seguintes colunas:
- Data: formato de data (DD/MM/YYYY ou YYYY-MM-DD)
- Produto
- Venda_Total: valor numérico das vendas

📑 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

