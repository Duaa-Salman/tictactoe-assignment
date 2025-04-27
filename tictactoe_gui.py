# tictactoe_gui.py

import tkinter as tk
from tkinter import messagebox
from tictactoe_ai import TicTacToe, AlphaBetaAI

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI (Alpha-Beta)")
        self.root.geometry("400x450")  # Slightly taller for Restart button
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")

        self.game = TicTacToe()
        self.ai = AlphaBetaAI()

        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.place(relx=0.5, rely=0.45, anchor="center")

        self.buttons = []
        for i in range(9):
            button = tk.Button(
                self.frame,
                text=' ',
                font=('Arial', 24, 'bold'),
                width=4,
                height=2,
                bg="#ffffff",
                fg="black",
                relief="solid",
                bd=1,
                command=lambda i=i: self.player_move(i)
            )
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)

        # Add Restart button below the game grid
        self.restart_button = tk.Button(
            self.root,
            text="Restart",
            font=('Arial', 14, 'bold'),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=self.restart_game,
            state='disabled'  # Initially disabled
        )
        self.restart_button.place(relx=0.5, rely=0.9, anchor="center")

    def player_move(self, index):
        if self.game.board[index] == ' ':
            self.buttons[index].config(text='X', state='disabled', fg='blue')
            self.game.make_move(index, 'X')

            if self.game.is_winner('X'):
                self.end_game("You win!")
                return
            elif self.game.is_draw():
                self.end_game("It's a draw!")
                return

            self.root.after(500, self.ai_move)

    def ai_move(self):
        best_move = self.ai.find_best_move(self.game)
        self.game.make_move(best_move, 'O')
        self.buttons[best_move].config(text='O', state='disabled', fg='green')

        if self.game.is_winner('O'):
            self.end_game("AI wins!")
        elif self.game.is_draw():
            self.end_game("It's a draw!")

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        for btn in self.buttons:
            btn.config(state='disabled')
        self.restart_button.config(state='normal')  # Enable Restart button

    def restart_game(self):
        self.game = TicTacToe()  # Reset the game logic
        for button in self.buttons:
            button.config(text=' ', state='normal', fg='black')
        self.restart_button.config(state='disabled')  # Disable again after restart

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
