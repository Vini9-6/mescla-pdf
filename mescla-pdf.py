import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


# funcao para selecionar a pasta onde estao os pdfs
def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione a pasta dos PDFs")
    if pasta:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, pasta)
        listar_pdfs()  # atualiza a lista de arquivos pdf


# funcao para listar os arquivos pdf da pasta selecionada
def listar_pdfs():
    lista_arquivos.delete(0, tk.END)
    pasta = entry_pasta.get()
    if os.path.exists(pasta):
        # filtra apenas arquivos com extensao .pdf
        arquivos = sorted([f for f in os.listdir(
            pasta) if f.lower().endswith('.pdf')])
        for arq in arquivos:
            lista_arquivos.insert(tk.END, arq)


# funcao para mesclar os pdfs selecionados
def mesclar_pdfs():
    pasta = entry_pasta.get()
    saida = entry_saida.get().strip()
    if not saida:
        saida = "PDF Final.pdf"
    if not saida.lower().endswith('.pdf'):
        saida += ".pdf"
    selecionados = lista_arquivos.curselection()
    if not selecionados:
        # exibe aviso se nenhum arquivo for selecionado
        messagebox.showwarning(
            "Aviso", "Selecione ao menos um PDF para mesclar.")
        return
    merger = PyPDF2.PdfMerger()
    try:
        # adiciona cada pdf selecionado ao merger
        for idx in selecionados:
            arquivo = lista_arquivos.get(idx)
            caminho = os.path.join(pasta, arquivo)
            merger.append(caminho)
        # salva o pdf final
        merger.write(saida)
        merger.close()
        messagebox.showinfo("Sucesso", f"PDF final salvo como: {saida}")
    except Exception as e:
        # exibe mensagem de erro caso ocorra algum problema
        messagebox.showerror("Erro", f"Erro ao mesclar PDFs: {e}")


# configuracao da interface grafica principal
root = tk.Tk()
root.title("Mesclar PDFs")

# campo para selecionar a pasta dos pdfs
tk.Label(root, text="Pasta dos PDFs:").grid(row=0, column=0, sticky="w")
entry_pasta = tk.Entry(root, width=40)
entry_pasta.grid(row=0, column=1, padx=5)
btn_pasta = tk.Button(root, text="Selecionar", command=selecionar_pasta)
btn_pasta.grid(row=0, column=2, padx=5)

# lista de arquivos pdf encontrados
tk.Label(root, text="Arquivos PDF encontrados:").grid(
    row=1, column=0, columnspan=3, sticky="w")
lista_arquivos = tk.Listbox(root, selectmode=tk.MULTIPLE, width=60, height=10)
lista_arquivos.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

# campo para definir o nome do pdf final
tk.Label(root, text="Nome do PDF final:").grid(row=3, column=0, sticky="w")
entry_saida = tk.Entry(root, width=40)
entry_saida.insert(0, "PDF Final.pdf")
entry_saida.grid(row=3, column=1, padx=5)

# botao para executar a mesclagem dos pdfs
btn_mesclar = tk.Button(root, text="Mesclar PDFs", command=mesclar_pdfs)
btn_mesclar.grid(row=4, column=0, columnspan=3, pady=10)

# inicia o loop principal da interface grafica
root.mainloop()
