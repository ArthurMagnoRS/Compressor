# Compressor

Um compressor e descompressor de arquivos e diretórios de alta performance, construído em Python. Este projeto utiliza o poderoso algoritmo **Zstandard (zstd)**, oferecendo um equilíbrio perfeito entre velocidade extrema e altas taxas de compressão.

## ✨ Funcionalidades

* **Compressão Inteligente:** Detecta automaticamente se o alvo é um arquivo único ou um diretório inteiro.
* **Empacotamento de Pastas:** Utiliza `tarfile` sob o capô para preservar a hierarquia exata de pastas (sem vazar os caminhos locais do seu computador).
* **Barras de Progresso Visuais:** Feedback em tempo real durante a compressão e extração utilizando a biblioteca `tqdm`.
* **Interface de Linha de Comando (CLI):** Fácil de usar direto pelo terminal, construída com `argparse`.
* **Adivinhação de Nomes:** Na extração de arquivos únicos, o sistema deduz automaticamente o nome original e a extensão do arquivo cortando o sufixo `.zst`.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Zstandard (`zstandard`):** Motor principal de compressão.
* **Tqdm (`tqdm`):** Para as barras de progresso animadas.
* **Bibliotecas Nativas:** `os`, `tarfile`, `argparse`.

## 📦 Instalação

1. Clone este repositório para a sua máquina:
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
   cd NOME_DO_REPOSITORIO
2. Instale as dependências necessárias:
   ```bash
   pip install zstandard tqdm
3. Como Usar
Abra o seu terminal e utilize os comandos abaixo. O script possui um menu de ajuda embutido que pode ser acessado com python compressor.py -h.

--Para Comprimir
Você pode passar um arquivo único ou uma pasta inteira:

# Comprimindo um arquivo
python compressor.py comprimir meu_relatorio.pdf
# Saída: meu_relatorio.pdf.zst

# Comprimindo uma pasta
python compressor.py comprimir minhas_fotos/
# Saída: minhas_fotos.tar.zst
--Para Extrair
# Extraindo um arquivo
python compressor.py extrair meu_relatorio.pdf.zst

# Extraindo uma pasta
python compressor.py extrair minhas_fotos.tar.zst

🚀 Próximas Atualizações (Roadmap)
Este projeto está em constante evolução! Algumas das melhorias planejadas incluem:

[ ] Adicionar níveis de compressão personalizáveis (rápido vs. máximo) via terminal.

[ ] Gerar um arquivo executável (.exe) para uso em computadores sem Python.

[ ] Implementar tratamento de erros avançado e logs.

[ ] Implementar a escolha entre zip e zstd como extensões de compressão.
