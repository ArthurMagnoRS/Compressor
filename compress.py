import zstandard as zstd
import os
import tarfile
import argparse
from tqdm import tqdm


def comprimir_arquivo_ou_pasta(caminho_origem):
    if not os.path.exists(caminho_origem):
        print("arquivo/pasta inexistente")
        return

        
    compressor = zstd.ZstdCompressor(level=3)
    tamanho = 0
    if os.path.isdir(caminho_origem):
        caminho_destino = caminho_origem + ".tar.zstd"
        for pasta_atual, _, arquivos in os.walk(caminho_origem):
            for arq in arquivos:
                tamanho+=os.path.getsize(os.path.join(pasta_atual,arq))
        
        with open (caminho_destino, 'wb') as arquivo_saida: # abre a pasta de destino no modo escrita como arquivo_saida
            with compressor.stream_writer(arquivo_saida) as funil_zstd: # abre um funil na pasta de destino arquivo_saida que esta no modo escrita para colocar zstd
                with tarfile.open(fileobj=funil_zstd, mode="w|") as tar: # cria um objeto de escrita no funil para escrever com extensao .tar
                    
                    with tqdm(total=tamanho, desc="Comprimindo pasta!") as barra: 
                    
                        for pasta_atual, _, arquivos in os.walk(caminho_origem): # os.walk retorna a pasta em que ele esta andando no momento, ____ e uma lista dos arquivos naquela pasta
                            tar.add(pasta_atual, arcname=os.path.relpath(pasta_atual, os.path.dirname(caminho_origem)), recursive=False) # adicionamos utilizando o objeto em modo escrita criado no funil a pasta dentro do .tar (arcHIVEname precisa ser um caminho, e utilizando os.path.relpath(pasta_atual,os.path.dirname(caminho_origem)))
                        
                            for arq in arquivos:
                                caminho_completo = os.path.join(pasta_atual, arq) # caminho completo para chegar no arquivo (junta-se a pasta em que o arquivo esta + o nome do arquivo = ufpi/pasta/arquivo com o join)
                                nome_relativo = os.path.relpath(caminho_completo, os.path.dirname(caminho_origem)) # o nome_relativo deve ser o nome do arquivo, sendo seu caminho sem a pasta origem
                                
                                tar.add(caminho_completo, arcname=nome_relativo, recursive=False)
                                barra.update(os.path.getsize(caminho_completo))    
       
       
        print(f"Pasta {caminho_origem} comprimida para {caminho_destino}")
        return
                    
                    #precisa comprimir com a extensaoOriginal.zstd
    caminho_destino = caminho_origem + ".zstd"
    tamanho = os.path.getsize(caminho_origem)                
    with open (caminho_origem, "rb") as arquivo_entrada:
        with open (caminho_destino, "wb") as arquivo_saida:
                with compressor.stream_writer(arquivo_saida) as funil_saida:
                   # stream reader apenas para ler arquivos comprimidos, stream writer para escrever em arquivos q serao comprimidos, copy_stream é usado para comprimir de uma vez um arquivo, assim n daria certo os chunks
                    with tqdm(total=tamanho, desc="Comprimindo arquivo!") as barra:
                        while True:
                            chunk = arquivo_entrada.read(65536) # le 64kb do arquivo original
                            if not chunk: # se o chunk nao receber nada, significa que todo o arquivo ja foi colocado
                                break
                            funil_saida.write(chunk)
                            barra.update(len(chunk)) # tamanho dos 64kb como um inteiro
    

        print(f"deu certo! arquivo {caminho_origem} comprimido e colocado como {caminho_destino}")


def descomprimir_arquivo_ou_pasta(caminho_origem):
    if not os.path.exists(caminho_origem):
        print("arquivo inexistente")
        return
    
    decompressor = zstd.ZstdDecompressor()
    if ".tar" in caminho_origem:
        with open (caminho_origem, 'rb') as arquivo_entrada: # abrindo o .tar.zstd
            with decompressor.stream_reader(arquivo_entrada) as funil_saida_zstd: # criando/lendo o funil que vai fazer extrair a pasta
                with tarfile.open(fileobj=funil_saida_zstd, mode='r|') as tar: # usando o tar para ler o que vem do funil criado pelo streamreader acima e colocando em 'tar'
                    tar.extractall(path=caminho_origem[:-9])
                    print(f"Pasta extraída com o nome de {caminho_origem[:-9]}!")
        return
    else:                
        caminho_destino = caminho_origem[:-5]          
        with open (caminho_origem, "rb") as arquivo_entrada:
            with open(caminho_destino, 'wb') as arquivo_saida:
                with decompressor.stream_reader(arquivo_entrada) as funil_saida:
                        with tqdm(total=os.path.getsize(caminho_origem), desc="Descomprimindo arquivo") as barra:
                            while True:
                                chunk = funil_saida.read(65536) # lendo o arquivo comprimido pela abertura que descomprime ele (a parte .zstd))
                                if not chunk: # ou seja, lendo parte do arquivo descomprimido
                                    break
                                arquivo_saida.write(chunk)
                                progresso = arquivo_entrada.tell()
                                barra.update(progresso - barra.n)
            print(f"deu certo! arquivo extraído e colocado como {caminho_destino}")
                               

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Programa para compactação e extração de arquivos com extensão .zstd e pastas .tar")
    parser.add_argument("acao", choices=["comprimir",'extrair'], help='o que quer fazer')
    parser.add_argument("alvo", help= "pasta/arquivo que sofrera a acao")
    
    argumentos = parser.parse_args()
    
    if argumentos.acao == "comprimir":
        print("comprimindo...")
        comprimir_arquivo_ou_pasta(argumentos.alvo)
        
    else:
        print("descomprimindo...")
        descomprimir_arquivo_ou_pasta(argumentos.alvo)

    
    

    
    
    
   