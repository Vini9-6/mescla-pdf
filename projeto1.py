import PyPDF2
import os

# Verifica se a pasta existe
pasta = "arquivos"
if not os.path.exists(pasta):
    print(f"Pasta '{pasta}' não encontrada.")
    exit()

merger = PyPDF2.PdfMerger()

# Lista e ordena apenas arquivos PDF
lista_arquivos = sorted(
    [f for f in os.listdir(pasta) if f.lower().endswith('.pdf')])
print("Arquivos encontrados:", lista_arquivos)

for arquivo in lista_arquivos:
    caminho = os.path.join(pasta, arquivo)
    try:
        merger.append(caminho)
        print(f"Adicionado: {arquivo}")
    except Exception as e:
        print(f"Erro ao adicionar {arquivo}: {e}")

# Salva o PDF final
saida = "PDF Final.pdf"
merger.write(saida)
merger.close()
print(f"PDF final salvo como: {saida}")
