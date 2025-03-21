import tkinter as tk
from tkinter import messagebox, ttk
import random

class Node:
    def __init__(self, number, human_score, computer_score, bank, parent=None):
        self.number = number
        self.human_score = human_score
        self.computer_score = computer_score
        self.bank = bank
        self.children = []
        self.parent = parent
        self.move = None

    def add_child(self, child_node):
        self.children.append(child_node)

class MultiplicationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mind-Bending Multiplication Duel")
        self.root.geometry("500x600")

        self.current_number = 0
        self.human_score = 0
        self.computer_score = 0
        self.bank = 0
        self.human_turn = True
        self.root_node = None
        self.current_node = None
        self.algorithm = "minimax"

        self.label = tk.Label(root, text="Multiplication Duel", font=("Arial", 14))
        self.label.pack(pady=10)

        self.start_label = tk.Label(root, text="Enter a number (25-40):")
        self.start_label.pack(pady=5)
        self.start_entry = tk.Entry(root)
        self.start_entry.pack(pady=5)

        self.player_label = tk.Label(root, text="Who starts?")
        self.player_label.pack(pady=5)
        self.player_var = tk.StringVar(value="human")
        tk.Radiobutton(root, text="Human", variable=self.player_var, value="human").pack()
        tk.Radiobutton(root, text="Computer", variable=self.player_var, value="computer").pack()

        self.algo_label = tk.Label(root, text="Choose algorithm:")
        self.algo_label.pack(pady=5)
        self.algo_var = tk.StringVar(value="minimax")
        tk.Radiobutton(root, text="Minimax", variable=self.algo_var, value="minimax").pack()
        tk.Radiobutton(root, text="Alpha-Beta", variable=self.algo_var, value="alpha_beta").pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.status_label = tk.Label(root, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.multiplier_label = tk.Label(root, text="")
        self.multiplier_label.pack(pady=5)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        self.mult_2_button = tk.Button(self.button_frame, text="x2", command=lambda: self.play_turn(2), state="disabled")
        self.mult_2_button.grid(row=0, column=0, padx=5)
        self.mult_3_button = tk.Button(self.button_frame, text="x3", command=lambda: self.play_turn(3), state="disabled")
        self.mult_3_button.grid(row=0, column=1, padx=5)
        self.mult_4_button = tk.Button(self.button_frame, text="x4", command=lambda: self.play_turn(4), state="disabled")
        self.mult_4_button.grid(row=0, column=2, padx=5)

        self.winner_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.winner_label.pack(pady=10)
        self.winner_label.pack_forget()
        self.play_again_button = tk.Button(root, text="Play Again", command=self.reset_game, state="disabled")
        self.play_again_button.pack(pady=10)
        self.play_again_button.pack_forget()

    def start_game(self):
        try:
            start_number = int(self.start_entry.get())
            if 25 <= start_number <= 40:
                self.current_number = start_number
                self.human_score = 0
                self.computer_score = 0
                self.bank = 1 if start_number % 10 in [0, 5] else 0
                self.human_turn = (self.player_var.get() == "human")
                self.algorithm = self.algo_var.get()
                self.root_node = Node(start_number, 0, 0, self.bank)
                self.current_node = self.root_node
                self.start_label.config(text="Duel Begins!")
                self.start_entry.config(state="disabled")
                self.start_button.config(state="disabled")
                self.update_status()
                if self.human_turn:
                    self.enable_buttons()
                else:
                    self.computer_move()
            else:
                messagebox.showerror("Error", "Enter a number between 25 and 40.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def update_status(self):
        status = (f"Number: {self.current_number}\n"
                  f"Your Score: {self.human_score}\n"
                  f"AI Score: {self.computer_score}\n"
                  f"Bank: {self.bank}")
        self.status_label.config(text=status)
        self.multiplier_label.config(text="Your Move!" if self.human_turn else "AI’s Turn...")

    def is_even(self, number):
        return number % 2 == 0

    def ends_in_0_or_5(self, number):
        return number % 10 in [0, 5]

    def update_scores_and_bank(self, result, player_score):
        # Enhanced twists: Bigger swings for odd/even and 0/5
        if self.is_even(result):
            player_score -= 3  # Crash for even
            self.status_label.config(text=self.status_label.cget("text") + "\nEven Crash: -3!")
        else:
            player_score += 3  # Soar for odd
            self.status_label.config(text=self.status_label.cget("text") + "\nOdd Boost: +3!")
        if self.ends_in_0_or_5(result):
            self.bank += 2  # Sneaky bank twist
            self.status_label.config(text=self.status_label.cget("text") + "\n0/5 Twist: Bank +2!")
        return player_score

    def heuristic(self, node):
        return node.human_score - node.computer_score - (node.bank * 0.5)

    def minimax(self, node, depth, maximizing_player):
        if depth == 0 or node.number >= 5000:
            return self.heuristic(node)
        if maximizing_player:
            max_eval = float('-inf')
            for multiplier in [2, 3, 4]:
                new_number = node.number * multiplier
                if new_number < 5000:
                    new_score = node.human_score if self.human_turn else node.computer_score
                    new_score = self.update_scores_and_bank(new_number, new_score)
                    child = Node(new_number, node.human_score, node.computer_score, node.bank)
                    child.human_score = node.human_score if not self.human_turn else new_score
                    child.computer_score = node.computer_score if self.human_turn else new_score
                    child.bank = self.bank
                    node.add_child(child)
                    eval = self.minimax(child, depth - 1, False)
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for multiplier in [2, 3, 4]:
                new_number = node.number * multiplier
                if new_number < 5000:
                    new_score = node.human_score if self.human_turn else node.computer_score
                    new_score = self.update_scores_and_bank(new_number, new_score)
                    child = Node(new_number, node.human_score, node.computer_score, node.bank)
                    child.human_score = node.human_score if not self.human_turn else new_score
                    child.computer_score = node.computer_score if self.human_turn else new_score
                    child.bank = self.bank
                    node.add_child(child)
                    eval = self.minimax(child, depth - 1, True)
                    min_eval = min(min_eval, eval)
            return min_eval

    def alpha_beta(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or node.number >= 5000:
            return self.heuristic(node)
        if maximizing_player:
            max_eval = float('-inf')
            for multiplier in [2, 3, 4]:
                new_number = node.number * multiplier
                if new_number < 5000:
                    new_score = node.human_score if self.human_turn else node.computer_score
                    new_score = self.update_scores_and_bank(new_number, new_score)
                    child = Node(new_number, node.human_score, node.computer_score, node.bank)
                    child.human_score = node.human_score if not self.human_turn else new_score
                    child.computer_score = node.computer_score if self.human_turn else new_score
                    child.bank = self.bank
                    node.add_child(child)
                    eval = self.alpha_beta(child, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for multiplier in [2, 3, 4]:
                new_number = node.number * multiplier
                if new_number < 5000:
                    new_score = node.human_score if self.human_turn else node.computer_score
                    new_score = self.update_scores_and_bank(new_number, new_score)
                    child = Node(new_number, node.human_score, node.computer_score, node.bank)
                    child.human_score = node.human_score if not self.human_turn else new_score
                    child.computer_score = node.computer_score if self.human_turn else new_score
                    child.bank = self.bank
                    node.add_child(child)
                    eval = self.alpha_beta(child, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def computer_move(self):
        # AI goes rogue 20% of the time with a random risky move
        if random.random() < 0.2:
            best_move = random.choice([2, 3, 4])
            self.status_label.config(text=self.status_label.cget("text") + "\nAI Goes Rogue!")
        else:
            depth = 3
            best_move = 2
            best_value = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            for multiplier in [2, 3, 4]:
                new_number = self.current_number * multiplier
                if new_number < 5000:
                    new_score = self.update_scores_and_bank(new_number, self.computer_score)
                    child = Node(new_number, self.human_score, new_score, self.bank)
                    self.current_node.add_child(child)
                    value = (self.minimax(child, depth - 1, False) if self.algorithm == "minimax"
                             else self.alpha_beta(child, depth - 1, alpha, beta, False))
                    if value > best_value:
                        best_value = value
                        best_move = multiplier
        self.play_turn(best_move)

    def play_turn(self, multiplier):
        if self.human_turn:
            self.current_number *= multiplier
            self.human_score = self.update_scores_and_bank(self.current_number, self.human_score)
            child = Node(self.current_number, self.human_score, self.computer_score, self.bank)
            self.current_node.add_child(child)
            self.current_node = child
        else:
            self.current_number *= multiplier
            self.computer_score = self.update_scores_and_bank(self.current_number, self.computer_score)
            child = Node(self.current_number, self.human_score, self.computer_score, self.bank)
            self.current_node.add_child(child)
            self.current_node = child

        self.check_endgame()
        if self.current_number < 5000:
            self.switch_turn()

    def switch_turn(self):
        self.human_turn = not self.human_turn
        self.update_status()
        if not self.human_turn:
            self.disable_buttons()
            self.root.after(1000, self.computer_move)
        else:
            self.enable_buttons()

    def enable_buttons(self):
        self.mult_2_button.config(state="normal")
        self.mult_3_button.config(state="normal")
        self.mult_4_button.config(state="normal")

    def disable_buttons(self):
        self.mult_2_button.config(state="disabled")
        self.mult_3_button.config(state="disabled")
        self.mult_4_button.config(state="disabled")

    def check_endgame(self):
        if self.current_number >= 5000:
            if self.human_turn:
                self.human_score += self.bank
                winner = "You Win!" if self.human_score > self.computer_score else "AI Wins!" if self.computer_score > self.human_score else "Draw!"
            else:
                self.computer_score += self.bank
                winner = "You Win!" if self.human_score > self.computer_score else "AI Wins!" if self.computer_score > self.human_score else "Draw!"
            self.status_label.config(text=f"Final:\nYou: {self.human_score}\nAI: {self.computer_score}")
            self.multiplier_label.config(text="Game Over!")
            self.winner_label.config(text=winner)
            self.winner_label.pack()
            self.disable_buttons()
            self.play_again_button.pack()
            self.play_again_button.config(state="normal")

    def reset_game(self):
        self.current_number = 0
        self.human_score = 0
        self.computer_score = 0
        self.bank = 0
        self.human_turn = (self.player_var.get() == "human")
        self.root_node = None
        self.current_node = None
        self.start_label.config(text="Enter a number (25-40):")
        self.start_entry.config(state="normal")
        self.start_entry.delete(0, tk.END)
        self.start_button.config(state="normal")
        self.status_label.config(text="")
        self.multiplier_label.config(text="")
        self.winner_label.pack_forget()
        self.button_frame.pack()
        self.play_again_button.pack_forget()
        self.play_again_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiplicationGame(root)
    root.mainloop()