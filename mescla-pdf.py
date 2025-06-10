import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione a pasta dos PDFs")
    if pasta:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, pasta)
        listar_pdfs()


def listar_pdfs():
    lista_arquivos.delete(0, tk.END)
    pasta = entry_pasta.get()
    if os.path.exists(pasta):
        arquivos = sorted([f for f in os.listdir(
            pasta) if f.lower().endswith('.pdf')])
        for arq in arquivos:
            lista_arquivos.insert(tk.END, arq)


def mesclar_pdfs():
    pasta = entry_pasta.get()
    saida = entry_saida.get().strip()
    if not saida:
        saida = "PDF Final.pdf"
    if not saida.lower().endswith('.pdf'):
        saida += ".pdf"
    selecionados = lista_arquivos.curselection()
    if not selecionados:
        messagebox.showwarning(
            "Aviso", "Selecione ao menos um PDF para mesclar.")
        return
    merger = PyPDF2.PdfMerger()
    try:
        for idx in selecionados:
            arquivo = lista_arquivos.get(idx)
            caminho = os.path.join(pasta, arquivo)
            merger.append(caminho)
        merger.write(saida)
        merger.close()
        messagebox.showinfo("Sucesso", f"PDF final salvo como: {saida}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao mesclar PDFs: {e}")


# Interface Tkinter
root = tk.Tk()
root.title("Mesclar PDFs")

tk.Label(root, text="Pasta dos PDFs:").grid(row=0, column=0, sticky="w")
entry_pasta = tk.Entry(root, width=40)
entry_pasta.grid(row=0, column=1, padx=5)
btn_pasta = tk.Button(root, text="Selecionar", command=selecionar_pasta)
btn_pasta.grid(row=0, column=2, padx=5)

tk.Label(root, text="Arquivos PDF encontrados:").grid(
    row=1, column=0, columnspan=3, sticky="w")
lista_arquivos = tk.Listbox(root, selectmode=tk.MULTIPLE, width=60, height=10)
lista_arquivos.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

tk.Label(root, text="Nome do PDF final:").grid(row=3, column=0, sticky="w")
entry_saida = tk.Entry(root, width=40)
entry_saida.insert(0, "PDF Final.pdf")
entry_saida.grid(row=3, column=1, padx=5)

btn_mesclar = tk.Button(root, text="Mesclar PDFs", command=mesclar_pdfs)
btn_mesclar.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
