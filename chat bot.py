import tkinter as tk
from tkinter import scrolledtext
import datetime
import random

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot Assistente")
        self.root.geometry("500x500")
        self.root.configure(bg="#f0f0f0")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', 
                                                   bg="#1e1e1e", fg="#00ff00", font=("Arial", 10))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_msg = tk.Entry(root, bg="#333333", fg="#ffffff", insertbackground="#ffffff", font=("Arial", 10))
        self.entry_msg.pack(padx=10, pady=(0,10), fill=tk.X)
        self.entry_msg.bind("<Return>", self.enviar_mensagem)

        self.lembrete = None
        self.dicas = [
            "Beba bastante água ao longo do dia!",
            "Faça pequenas pausas durante o estudo para descansar a mente.",
            "Organize suas tarefas para ser mais produtivo.",
            "Pratique exercícios físicos regularmente.",
            "Durma pelo menos 7-8 horas por noite para recarregar a energia."
        ]

        self.pausado = False

        self.escrever_bot("Olá! Sou seu assistente pessoal. Pergunte o que quiser ou digite 'sair' para encerrar.")

    def escrever_bot(self, mensagem):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, "Bot: " + mensagem + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def escrever_usuario(self, mensagem):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, "Você: " + mensagem + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def enviar_mensagem(self, event=None):
        msg = self.entry_msg.get().strip()
        if msg == "":
            return
        self.escrever_usuario(msg)
        self.entry_msg.delete(0, tk.END)
        self.processar_mensagem(msg.lower())

    def processar_mensagem(self, msg):
        if self.pausado:
            if "continuar" in msg:
                self.pausado = False
                self.escrever_bot("Obrigado por voltar! Em que posso ajudar?")
            else:
                self.escrever_bot("Estou pausado. Digite 'continuar' para voltar.")
            return

        if "pausar" in msg:
            self.pausado = True
            self.escrever_bot("Pausando a conversa. Digite 'continuar' quando quiser retomar.")
        elif "oi" in msg or "olá" in msg:
            self.escrever_bot("Oi! Como posso ajudar?")
        elif "horas" in msg or "que horas" in msg:
            agora = datetime.datetime.now().strftime("%H:%M")
            self.escrever_bot(f"Agora são {agora}.")
        elif "lembrete" in msg:
            if self.lembrete:
                self.escrever_bot(f"Seu lembrete atual é: {self.lembrete}")
            else:
                self.escrever_bot("Você ainda não tem lembretes.")
        elif "guardar lembrete" in msg or "anotar" in msg:
            self.escrever_bot("O que você quer que eu lembre? (Digite e pressione Enter)")
            self.entry_msg.bind("<Return>", self.guardar_lembrete)
        elif "dica" in msg:
            self.escrever_bot(random.choice(self.dicas))
        elif "sair" in msg:
            self.escrever_bot("Até mais! Boa sorte no seu dia.")
            self.root.after(2000, self.root.destroy)
        else:
            self.escrever_bot("Desculpa, não entendi. Pode tentar outra coisa?")

    def guardar_lembrete(self, event=None):
        lembrete_msg = self.entry_msg.get().strip()
        if lembrete_msg == "":
            self.escrever_bot("Lembrete vazio. Tente novamente.")
        else:
            self.lembrete = lembrete_msg
            self.escrever_bot("Lembrete guardado!")
        self.entry_msg.delete(0, tk.END)
        self.entry_msg.bind("<Return>", self.enviar_mensagem)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
