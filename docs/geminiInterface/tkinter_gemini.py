import tkinter as tk
from google.generativeai import configure, GenerativeModel

# Configuração do Gemini
configure(api_key="SUA_API_KEY")
model = GenerativeModel("gemini-pro")

def enviar_pergunta():
    pergunta = entrada.get()
    resposta = model.generate_content(pergunta)
    saida.config(state=tk.NORMAL)
    saida.delete(1.0, tk.END)
    saida.insert(tk.END, resposta.text)
    saida.config(state=tk.DISABLED)

# Criar a janela
janela = tk.Tk()
janela.title("Gemini GUI")

# Campo de entrada
entrada = tk.Entry(janela, width=50)
entrada.pack(pady=10)

# Botão de envio
botao = tk.Button(janela, text="Perguntar", command=enviar_pergunta)
botao.pack()

# Área de resposta
saida = tk.Text(janela, height=20, width=60, state=tk.DISABLED)
saida.pack(pady=10)

janela.mainloop()