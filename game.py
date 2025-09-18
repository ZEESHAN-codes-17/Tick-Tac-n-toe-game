import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sys

class TicTacToeGame:
    def __init__(self):
        # Configure CustomTkinter appearance
        ctk.set_appearance_mode("dark")  # "dark" or "light"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("Tic Tac Toe - Modern Edition")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Game state variables
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.buttons = []
        
        # Score tracking
        self.score_x = 0
        self.score_o = 0
        
        self.create_gui()
        
    def create_gui(self):
        # Title
        title_label = ctk.CTkLabel(
            self.root,
            text="Tic Tac Toe",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Current player indicator
        self.player_label = ctk.CTkLabel(
            self.root,
            text=f"Current Player: {self.current_player}",
            font=ctk.CTkFont(size=18)
        )
        self.player_label.pack(pady=10)
        
        # Score display
        self.score_frame = ctk.CTkFrame(self.root)
        self.score_frame.pack(pady=10, padx=20, fill="x")
        
        self.score_x_label = ctk.CTkLabel(
            self.score_frame,
            text=f"Player X: {self.score_x}",
            font=ctk.CTkFont(size=16)
        )
        self.score_x_label.pack(side="left", padx=20, pady=10)
        
        self.score_o_label = ctk.CTkLabel(
            self.score_frame,
            text=f"Player O: {self.score_o}",
            font=ctk.CTkFont(size=16)
        )
        self.score_o_label.pack(side="right", padx=20, pady=10)
        
        # Game board frame
        self.game_frame = ctk.CTkFrame(self.root)
        self.game_frame.pack(pady=20, padx=20)
        
        # Create game board buttons
        self.create_board()
        
        # Control buttons frame
        control_frame = ctk.CTkFrame(self.root)
        control_frame.pack(pady=20, padx=20, fill="x")
        
        # Reset game button
        reset_button = ctk.CTkButton(
            control_frame,
            text="New Game",
            font=ctk.CTkFont(size=16),
            command=self.reset_game,
            width=120,
            height=40
        )
        reset_button.pack(side="left", padx=20, pady=10)
        
        # Reset scores button
        reset_scores_button = ctk.CTkButton(
            control_frame,
            text="Reset Scores",
            font=ctk.CTkFont(size=16),
            command=self.reset_scores,
            width=120,
            height=40
        )
        reset_scores_button.pack(side="right", padx=20, pady=10)
        
        # Exit button
        exit_button = ctk.CTkButton(
            self.root,
            text="Exit Game",
            font=ctk.CTkFont(size=14),
            command=self.root.quit,
            width=100,
            height=35,
            fg_color="red",
            hover_color="darkred"
        )
        exit_button.pack(pady=10)
    
    def create_board(self):
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = ctk.CTkButton(
                    self.game_frame,
                    text="",
                    font=ctk.CTkFont(size=36, weight="bold"),
                    width=100,
                    height=100,
                    command=lambda r=i, c=j: self.button_click(r, c),
                    fg_color="gray20",
                    hover_color="gray30"
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)
    
    def button_click(self, row, col):
        if self.game_over or self.board[row][col] != "":
            return
        
        # Make move
        self.board[row][col] = self.current_player
        
        # Update button appearance
        color = "#4CAF50" if self.current_player == "X" else "#FF9800"
        self.buttons[row][col].configure(
            text=self.current_player,
            fg_color=color,
            hover_color=color
        )
        
        # Check for win or tie
        if self.check_winner():
            self.game_over = True
            winner = self.current_player
            if winner == "X":
                self.score_x += 1
            else:
                self.score_o += 1
            self.update_score_display()
            
            # Highlight winning combination
            self.highlight_winning_combination()
            
            # Show winner message after a short delay
            self.root.after(500, lambda: self.show_winner_message(winner))
            
        elif self.check_tie():
            self.game_over = True
            self.root.after(500, lambda: self.show_tie_message())
        else:
            # Switch players
            self.current_player = "O" if self.current_player == "X" else "X"
            self.update_player_display()
    
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                return True
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        
        return False
    
    def check_tie(self):
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True
    
    def highlight_winning_combination(self):
        # Check rows
        for i, row in enumerate(self.board):
            if row[0] == row[1] == row[2] != "":
                for j in range(3):
                    self.buttons[i][j].configure(fg_color="gold", hover_color="gold")
                return
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                for row in range(3):
                    self.buttons[row][col].configure(fg_color="gold", hover_color="gold")
                return
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            for i in range(3):
                self.buttons[i][i].configure(fg_color="gold", hover_color="gold")
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            for i in range(3):
                self.buttons[i][2-i].configure(fg_color="gold", hover_color="gold")
            return
    
    def show_winner_message(self, winner):
        messagebox.showinfo("Game Over", f"🎉 Player {winner} wins! 🎉")
    
    def show_tie_message(self):
        messagebox.showinfo("Game Over", "🤝 It's a tie! 🤝")
    
    def update_player_display(self):
        self.player_label.configure(text=f"Current Player: {self.current_player}")
    
    def update_score_display(self):
        self.score_x_label.configure(text=f"Player X: {self.score_x}")
        self.score_o_label.configure(text=f"Player O: {self.score_o}")
    
    def reset_game(self):
        # Reset game state
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        # Reset buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(
                    text="",
                    fg_color="gray20",
                    hover_color="gray30"
                )
        
        # Update display
        self.update_player_display()
    
    def reset_scores(self):
        self.score_x = 0
        self.score_o = 0
        self.update_score_display()
        self.reset_game()
    
    def run(self):
        self.root.mainloop()

# Main execution
if __name__ == "__main__":
    try:
        game = TicTacToeGame()
        game.run()
    except ImportError:
        print("Error: CustomTkinter is not installed.")
        print("Please install it using: pip install customtkinter")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)