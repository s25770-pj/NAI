import tkinter as tk
from tkinter import messagebox
from typing import Optional

from easyAI import Negamax, Human_Player, AI_Player
from models import Chomp


class ChompGUI:
    """
    A GUI for the Chomp game that allows players to interact with the game board.

    Attributes:
        game (Chomp): An instance of the Chomp game.
        window (tk.Tk): The main application window.
        colors (dict): A dictionary of colors for the game UI.
        button_style (dict): A dictionary of styles for buttons.
        label (tk.Label): A label displaying the current player.
        buttons (list): A 2D list of buttons representing the game board.
    """

    def __init__(self, game: Chomp) -> None:
        """
        Initializes the ChompGUI with the given game.

        Args:
            game (Chomp): An instance of the Chomp game.
        """
        self.game = game
        self.window = tk.Tk()
        self.window.title("Chomp Game")

        self.colors: dict[str, str] = {
            "default": "#4CAF50",
            "player1": "#BBEE22",
            "player2": "#22FF00",
        }

        self.button_style: dict[str, str] = {
            "font": ("Arial", 12),
            "bg": self.colors["default"],
            "fg": "white",
            "activebackground": "#45a049",
            "padx": 20,
            "pady": 10,
            "borderwidth": 2,
            "relief": "raised",
            "width": 20,
            "height": 3
        }

        window_width = 600
        window_height = 600
        self.window.geometry(f"{window_width}x{window_height}")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.window.geometry(f"+{x}+{y}")

        self.label = tk.Label(self.window, text=self.current_player_text(), font=("Arial", 14))
        self.label.grid(row=0, column=0, columnspan=self.game.max_x, pady=10)

        self.buttons: list[list[tk.Button]] = []
        for y in range(self.game.max_y):
            row_buttons = []
            for x in range(self.game.max_x):
                button = tk.Button(self.window, text="X",
                                   command=lambda xy=f"{x + 1}{y + 1}": self.on_button_click(xy),
                                   **self.button_style)
                button.grid(row=y + 1, column=x, padx=10, pady=10)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        for x in range(self.game.max_x):
            self.window.grid_columnconfigure(x, weight=1)

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
        """
        Executes the AI player's move and updates the game state accordingly.
        """
        ai_move = self.game.players[self.game.current_player - 1].ask_move(self.game)
        self.game.make_move(ai_move)
        self.update_buttons()

        if self.game.is_over():
            self.show_winner_message()
        else:
            self.game.current_player = 2 if self.game.current_player == 1 else 1
            self.update_buttons()

    def show_winner_message(self) -> None:
        """
        Displays a message indicating the winner and prompts to play again.
        """
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
        """
        Restarts the game by closing the current window and opening the game mode selection.
        """
        self.window.destroy()
        choose_game_mode()


def choose_game_mode(default_negamax_depth:int =1) -> None:
    """
    Creates a new window for the player to choose the game mode.

    Returns:
        None
    """
    mode_window = tk.Tk()
    mode_window.title("Choose Game Mode")

    window_width = 400
    window_height = 300
    mode_window.geometry(f"{window_width}x{window_height}")

    screen_width = mode_window.winfo_screenwidth()
    screen_height = mode_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    mode_window.geometry(f"+{x}+{y}")

    def start_game(is_ai: bool, negamax_depth: Optional[int]) -> None:
        """
        Starts a new game with the selected mode.

        Args:
            is_ai (bool): Indicates whether to play against AI.
            negamax_depth (Optional[int]): The depth parameter for the Negamax algorithm, or None if playing against another player.
        """
        mode_window.destroy()
        ai = Negamax(negamax_depth) if is_ai else None
        players = [Human_Player(), AI_Player(ai)] if is_ai else [Human_Player(), Human_Player()]
        game = Chomp(players)
        ChompGUI(game)

    tk.Label(mode_window, text="Choose Game Mode:", font=("Arial", 16)).pack(pady=20)

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

    tk.Button(mode_window, text="Play with AI", command=lambda: start_game(True,default_negamax_depth), **button_style).pack(pady=10)
    tk.Button(mode_window, text="Play with another player", command=lambda: start_game(False,1), **button_style).pack(pady=10)

    mode_window.mainloop()


if __name__ == '__main__':
    choose_game_mode()
