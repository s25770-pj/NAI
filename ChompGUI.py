import tkinter as tk
from tkinter import messagebox
from typing import Optional
from easyAI import Negamax, Human_Player, AI_Player
from models import Chomp


class ChompGUI:
    def __init__(self, game: Chomp, window_width: int, window_height: int) -> None:
        self.game = game
        self.window = tk.Tk()
        self.window.title("Chomp Game")

        self.colors = {
            "default": "#4CAF50",
            "player1": "#BBEE22",
            "player2": "#22FF00",
        }

        self.window.geometry(f"{window_width}x{window_height}")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.window.geometry(f"+{x}+{y}")

        self.label = tk.Label(self.window, text=self.current_player_text(), font=("Arial", 14))
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(self.window)  # Frame for buttons
        self.button_frame.pack(pady=10)

        self.buttons = []
        for y in range(self.game.max_y):
            row_buttons = []
            for x in range(self.game.max_x):
                button = tk.Button(self.button_frame, text="X",
                                   command=lambda xy=f"{x + 1}{y + 1}": self.on_button_click(xy),
                                   font=("Arial", 12), bg=self.colors["default"], width=4, height=2)
                button.grid(row=y, column=x, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        for x in range(self.game.max_x):
            self.button_frame.grid_columnconfigure(x, weight=1)

        self.update_buttons()
        self.window.mainloop()

    def current_player_text(self) -> str:
        """
        Returns a string indicating the current player's turn.

        Returns:
            str: The current player's status message.
        """
        if isinstance(self.game.players[self.game.current_player - 1], AI_Player):
            return "Current Player: Computer"
        else:
            return f"Current Player: Player {self.game.current_player}"

    def update_buttons(self) -> None:
        """
        Updates the state of the buttons and the current player label.
        """
        for y in range(self.game.max_y):
            for x in range(self.game.max_x):
                if self.game.board[y][x] == 0:
                    if self.game.current_player == 1:
                        self.buttons[y][x].config(text="X", state=tk.DISABLED, bg=self.colors["player1"])
                    else:
                        self.buttons[y][x].config(text="X", state=tk.DISABLED, bg=self.colors["player2"])
                else:
                    self.buttons[y][x].config(text="X", state=tk.NORMAL, bg=self.colors["default"])

        self.label.config(text=self.current_player_text())

    def on_button_click(self, move: str) -> None:
        """
        Handles a button click event for a player's move.

        Args:
            move (str): The move made by the player.
        """
        if not self.game.is_over() and not isinstance(self.game.players[self.game.current_player - 1], AI_Player):
            self.game.make_move(move)
            self.update_buttons()

            if not self.game.is_over():
                self.game.current_player = 2 if self.game.current_player == 1 else 1

                if isinstance(self.game.players[self.game.current_player - 1], AI_Player):
                    self.update_buttons()
                    self.window.after(1000, lambda: self.ai_move())

            if self.game.is_over():
                self.show_winner_message()

    def ai_move(self) -> None:
        """Executes the AI player's move and updates the game state accordingly."""
        ai_move = self.game.players[self.game.current_player - 1].ask_move(self.game)
        self.game.make_move(ai_move)
        self.update_buttons()

        if self.game.is_over():
            self.show_winner_message()
        else:
            self.game.current_player = 2 if self.game.current_player == 1 else 1
            self.update_buttons()

    def show_winner_message(self) -> None:
        winner = f"Player {2 if self.game.current_player == 1 else 1}"
        message = f"{winner} won!\nDo you want to play again?"
        if isinstance(self.game.players[1], AI_Player) and self.game.current_player == 1:
            winner = "Computer"
            message = f"Oh.. {winner} won!\nDo you want to play again?"

        result = messagebox.askyesno("Game Over", message)

        if result:
            self.restart_game()
        else:
            self.window.destroy()

    def restart_game(self) -> None:
        self.window.destroy()
        choose_game_mode()


def choose_game_mode(default_negamax_depth: int = 1) -> None:
    mode_window = tk.Tk()
    mode_window.title("Choose Game Mode")

    window_width = 400
    window_height = 350
    mode_window.geometry(f"{window_width}x{window_height}")

    screen_width = mode_window.winfo_screenwidth()
    screen_height = mode_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    mode_window.geometry(f"+{x}+{y}")

    def start_game(is_ai: bool, negamax_depth: Optional[int]) -> None:
        try:
            width = int(x_entry.get())
            height = int(y_entry.get())
            if width < 2 or height < 2:
                raise ValueError("Both dimensions must be at least 2.")
            if width > 10 or height > 10:
                raise ValueError("Both dimensions must be at most 10.")
        except ValueError as e:
            messagebox.showerror("Invalid Size", str(e))
            return

        mode_window.destroy()
        players = [Human_Player(), AI_Player(Negamax(negamax_depth))] if is_ai else [Human_Player(), Human_Player()]
        game = Chomp(players, width, height)

        button_width = 10
        button_height = 11
        button_padding_x = 5
        button_padding_y = 4


        label_height = 130  if height < 3 else 120
        label_width = 60 if width > 3 else 120
        if height >= 4:
            button_height = 12
        if height >= 5:
            button_height+=1
        if height >= 8:
            button_height += 1
        # Obliczenia
        window_width = button_width * width * button_padding_x + label_width
        window_height = button_height * height * button_padding_y + label_height

        print(f"{window_width}, {window_height}")
        ChompGUI(game, window_width, window_height)

    tk.Label(mode_window, text="Chomp game", font=("Arial", 24)).pack(pady=10)
    tk.Label(mode_window, text="Enter map size (width X height):", font=("Arial", 12)).pack(pady=10)

    size_frame = tk.Frame(mode_window)
    size_frame.pack(pady=10)

    x_entry = tk.Entry(size_frame, font=("Arial", 12), width=5)
    x_entry.pack(side=tk.LEFT, padx=(0, 5))

    tk.Label(size_frame, text="X", font=("Arial", 12)).pack(side=tk.LEFT, padx=(0, 5))

    y_entry = tk.Entry(size_frame, font=("Arial", 12), width=5)
    y_entry.pack(side=tk.LEFT)

    button_style: dict[str, str] = {
        "font": ("Arial", 12),
        "bg": "#4CAF50",
        "fg": "white",
        "activebackground": "#45a049",
        "padx": 20,
        "pady": 10,
        "borderwidth": 2,
        "relief": "raised",
        "width": 20
    }

    tk.Label(mode_window, text="Choose mode:", font=("Arial", 12)).pack(pady=10)
    tk.Button(mode_window, text="Play with AI", command=lambda: start_game(True, default_negamax_depth),
              **button_style).pack(pady=10)
    tk.Button(mode_window, text="Play with another player", command=lambda: start_game(False, 1), **button_style).pack(
        pady=10)

    mode_window.mainloop()


if __name__ == '__main__':
    choose_game_mode()
