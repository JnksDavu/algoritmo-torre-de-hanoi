import tkinter as tk
import time

class TorreDeHanoiGUI:
    def __init__(self, pinos, movimentos_log):
        self.janela = tk.Tk()
        self.janela.title("Torre de Hanói")

        self.canvas = tk.Canvas(self.janela, width=900, height=500, bg="white")
        self.canvas.pack()

        self.pinos = pinos
        self.movimentos_log = movimentos_log
        self.peca_altura = 20
        self.peca_largura_base = 30
        self.peca_largura_inc = 20

        self.desenhar_hastes()
        self.desenhar_pecas_iniciais()
        self.janela.update()
        self.janela.after(1000)

    def desenhar_hastes(self):
        for i in range(3):
            x = 150 + i * 300
            self.canvas.create_line(x, 100, x, 400, width=6)

    def desenhar_pecas_iniciais(self):
        for idx, pilha in enumerate(self.pinos):
            altura = len(pilha)
            for i, valor in enumerate(reversed(pilha)):
                self.desenhar_peca(idx, altura - i - 1, valor)

    def desenhar_peca(self, haste_idx, pos, tamanho):
        x_centro = 150 + haste_idx * 300
        largura = self.peca_largura_base + tamanho * self.peca_largura_inc
        y = 400 - pos * self.peca_altura
        self.canvas.create_rectangle(x_centro - largura // 2, y - self.peca_altura,
                                     x_centro + largura // 2, y,
                                     fill="skyblue", outline="black")

    def atualizar_canvas(self):
        self.canvas.delete("all")
        self.desenhar_hastes()
        for idx, pilha in enumerate(self.pinos):
            altura = len(pilha)
            for i, valor in enumerate(reversed(pilha)):
                self.desenhar_peca(idx, altura - i - 1, valor)
        self.janela.update()
        time.sleep(0.5)

    def iniciar_interface(self):
        self.janela.mainloop()

def hanoi(n, origem, destino, auxiliar, pinos, gui, origem_idx, destino_idx, auxiliar_idx, movimentos):
    if n == 1:
        disco = pinos[origem_idx].pop()
        pinos[destino_idx].append(disco)
        movimentos.append(f"Movendo disco {disco} de {origem} para {destino}")
        print(movimentos[-1])
        gui.atualizar_canvas()
        return

    hanoi(n - 1, origem, auxiliar, destino, pinos, gui, origem_idx, auxiliar_idx, destino_idx, movimentos)
    hanoi(1, origem, destino, auxiliar, pinos, gui, origem_idx, destino_idx, auxiliar_idx, movimentos)
    hanoi(n - 1, auxiliar, destino, origem, pinos, gui, auxiliar_idx, destino_idx, origem_idx, movimentos)

def main():
    nomes_hastes = ['A', 'B', 'C']
    while True:
        haste_inicial = input("Informe a haste inicial (A, B ou C): ").upper()
        if haste_inicial in nomes_hastes:
            break
        print("Valor inválido. Tente novamente.")

    while True:
        haste_final = input("Informe a haste final (A, B ou C): ").upper()
        if haste_final in nomes_hastes and haste_final != haste_inicial:
            break
        print("Valor inválido ou igual à haste inicial. Tente novamente.")

    while True:
        try:
            num_discos = int(input("Informe o número de peças (≥ 1): "))
            if num_discos >= 1:
                break
        except ValueError:
            pass
        print("Valor inválido. Digite um número inteiro maior ou igual a 1.")

    pinos = [[], [], []]
    idx_inicial = nomes_hastes.index(haste_inicial)
    idx_final = nomes_hastes.index(haste_final)
    idx_aux = 3 - idx_inicial - idx_final  # O índice restante é o auxiliar

    # Monta os discos na haste inicial (maior = num_discos no fundo)
    pinos[idx_inicial] = list(range(num_discos, 0, -1))

    movimentos_log = []
    gui = TorreDeHanoiGUI(pinos, movimentos_log)

    hanoi(num_discos,
          haste_inicial, haste_final, nomes_hastes[idx_aux],
          pinos, gui,
          idx_inicial, idx_final, idx_aux,
          movimentos_log)

    print(f"\nTotal de movimentos: {len(movimentos_log)}")

    gui.iniciar_interface()

if __name__ == "__main__":
    main()
