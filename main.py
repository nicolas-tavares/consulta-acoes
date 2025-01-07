
# "pip install yfinance"
# "pip install matplotlib"

import yfinance as yf
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_stock_data():
    stock_code = entry.get().strip()
    if not stock_code:
        messagebox.showerror("Erro", "Por favor, insira um código de ação.")
        return

    try:
        stock = yf.Ticker(stock_code)
        stock_info = stock.info

        # Atualizar o texto no Treeview
        for i in tree.get_children():
            tree.delete(i)

        data = [
            ("Nome", stock_info.get("longName", "N/A")),
            ("Setor", stock_info.get("sector", "N/A")),
            ("Indústria", stock_info.get("industry", "N/A")),
            ("Capitalização de Mercado", stock_info.get("marketCap", "N/A")),
            ("ROE", stock_info.get("returnOnEquity", "N/A")),
            ("Dividend Yield", stock_info.get("dividendYield", "N/A")), # COLOCAR PERCENTUAL
            ("Crescimento dos Lucros", stock_info.get("earningsGrowth", "N/A")),
            ("PM Últimos 200 dias", stock_info.get("twoHundredDayAverage", "N/A"))
        ]

        for key, value in data:
            tree.insert("", "end", values=(key, value))

        # Gera o gráfico
        plot_stock_data(stock_code)

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível obter os dados: {e}")

def plot_stock_data(stock_code):
    try:
        stock_data = yf.download(stock_code, start="2018-01-01", end="2025-01-06", progress=False)
        if stock_data.empty:
            messagebox.showerror("Erro", "Não há dados históricos disponíveis para esta ação.")
            return

        # Cria a figura do gráfico
        fig, ax = plt.subplots(figsize=(10, 5))
        stock_data["Close"].plot(ax=ax)
        ax.set_xlabel("Ano")
        ax.set_ylabel("Valor em reais")
        ax.set_title(f"Histórico de Preços - {stock_code}")

        # Adiciona o gráfico na interface 
        for widget in graph_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível gerar o gráfico: {e}")

# Configuração da janela principal
root = tk.Tk()
root.title("Consulta de Ações Brasileiras")
root.state('zoomed')  # Define a janela para modo tela cheia

frame = tk.Frame(root)
frame.pack(pady=10)

# Entrada para o código da ação
label = tk.Label(frame, text="Digite o código da ação (ex: PETR4.SA):")
label.grid(row=0, column=0, padx=5)

entry = tk.Entry(frame, width=20)
entry.grid(row=0, column=1, padx=5)

button = tk.Button(frame, text="Buscar", command=fetch_stock_data)
button.grid(row=0, column=2, padx=5)

# Configuração do Treeview para exibir os dados
columns = ("Atributo", "Valor")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=250, anchor="center")

tree.pack(pady=20)

# Frame para o gráfico
graph_frame = tk.Frame(root)
graph_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
