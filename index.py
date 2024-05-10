import tkinter as tk
from tkinter import Frame, Label, Button, Entry, OptionMenu, ttk, messagebox
import json
import os

class Application:
    def __init__(self, master=None):
        self.master = master
        self.master.geometry("800x500+0+0")  # Definindo a geometria da janela
        self.master.title("Controle de Funcionários")
        self.widget1 = Frame(master, bg="#f0f0f0")
        self.widget1.pack(expand=True, fill='both', padx=10, pady=10)  # Expande para preencher todo o espaço disponível

        # Campos de entrada e rótulos
        labels_texts = ["Nome:", "Número de telefone:", "IMEI/Serial Number:", "Função:"]
        self.entries = {}
        for i, text in enumerate(labels_texts):
            label = Label(self.widget1, text=text, bg="#f0f0f0", font=("Calibri", 12))
            label.grid(row=i, column=0, sticky="e", padx=10, pady=(10, 5))
            entry = Entry(self.widget1, font=("Calibri", 12), bd=2, relief="solid")
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=(10, 5))
            self.entries[text] = entry

        # Rótulo para a caixa de seleção de Dispositivos
        dispositivo_label = Label(self.widget1, text="Dispositivo:", bg="#f0f0f0", font=("Calibri", 12))
        dispositivo_label.grid(row=len(labels_texts), column=0, sticky="e", padx=10, pady=(10, 5))

        # Opção para selecionar entre celular e notebook
        tipo_options = ["Celular", "Notebook"]
        self.tipo_var = tk.StringVar()
        self.tipo_var.set(tipo_options[0])  # Define o valor padrão para "Celular"
        tipo_menu = OptionMenu(self.widget1, self.tipo_var, *tipo_options)
        tipo_menu.config(font=("Calibri", 10), bg="#f0f0f0", bd=2, relief="solid")
        tipo_menu.grid(row=len(labels_texts), column=1, sticky="ew", padx=10, pady=(10, 5))

        # Rótulo para a caixa de seleção de Setor
        setor_label = Label(self.widget1, text="Setor:", bg="#f0f0f0", font=("Calibri", 12))
        setor_label.grid(row=len(labels_texts) + 1, column=0, sticky="e", padx=10, pady=(5, 10))

        # Opção para selecionar o setor
        setor_options = ["Comercial-GV1", "Comercial-GV2", "Comercial-GV3", "Comercial-GV4", "ENTREGA", "ARMAZEM", "ADM"]
        self.setor_var = tk.StringVar()
        self.setor_var.set(setor_options[0])  # Define o valor padrão para "GV1"
        setor_menu = OptionMenu(self.widget1, self.setor_var, *setor_options)
        setor_menu.config(font=("Calibri", 10), bg="#f0f0f0", bd=2, relief="solid")
        setor_menu.grid(row=len(labels_texts) + 1, column=1, sticky="ew", padx=10, pady=(5, 10))

        # Botões para salvar e buscar por setor
        self.salvar = Button(self.widget1, text="Salvar", font=("Calibri", 10), bd=2, relief="raised", command=self.salvar_informacoes)
        self.salvar.grid(row=len(labels_texts) + 2, column=0, padx=10, pady=10)

        self.buscar_por_setor = Button(self.widget1, text="Buscar por Setor", font=("Calibri", 10), bd=2, relief="raised", command=self.buscar_por_setor)
        self.buscar_por_setor.grid(row=len(labels_texts) + 2, column=1, padx=10, pady=10)

        # Tabela de preenchimento
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = labels_texts
        self.tree["show"] = "headings"
        self.tree.heading("#0", text="ID", anchor="center")
        for text in labels_texts:
            self.tree.heading(text, text=text, anchor="center")
            self.tree.column(text, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Carregar dados ao iniciar o aplicativo
        self.carregar_dados()

    def carregar_dados(self):
        setor = self.setor_var.get()
        arquivo = f"{setor.lower().replace(' ', '_')}.json"

        if os.path.exists(arquivo):
            with open(arquivo, "r") as f:
                dados = json.load(f)
                self.mostrar_resultados(dados)
        else:
            self.mostrar_mensagem("Nenhum dado encontrado para este setor.")

    def salvar_informacoes(self):
        informacoes = {}
        for label, entry in self.entries.items():
            informacoes[label[:-1].lower().replace(" ", "_")] = entry.get()  # Remove os dois pontos dos rótulos
            entry.delete(0, tk.END)  # Limpa o campo de entrada

        tipo = self.tipo_var.get()
        setor = self.setor_var.get()

        arquivo = f"{setor.lower().replace(' ', '_')}.json"

        if os.path.exists(arquivo):
            with open(arquivo, "r") as f:
                dados = json.load(f)
            if not isinstance(dados, list):
                dados = []
        else:
            dados = []

        informacoes["tipo"] = tipo
        informacoes["setor"] = setor

        dados.append(informacoes)

        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
        print("Salvo com sucesso!")
        self.mostrar_mensagem("Salvo com sucesso!")
        self.carregar_dados()

    def buscar_por_setor(self):
        setor_selecionado = self.setor_var.get()
        arquivo = f"{setor_selecionado.lower().replace(' ', '_')}.json"

        if os.path.exists(arquivo):
            with open(arquivo, "r") as f:
                dados = json.load(f)
            if isinstance(dados, list):
                self.mostrar_resultados(dados)
        else:
            self.mostrar_mensagem("Nenhum dado encontrado para este setor.")

    def mostrar_resultados(self, dados):
        self.tree.delete(*self.tree.get_children())
        for i, pessoa in enumerate(dados, start=1):
            self.tree.insert("", "end", text=i, values=[pessoa.get(label[:-1].lower().replace(" ", "_"), "") for label in self.entries])

    def mostrar_mensagem(self, mensagem):
        messagebox.showinfo("Mensagem", mensagem)

root = tk.Tk()
app = Application(root)
root.mainloop()
