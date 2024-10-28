import tkinter as tk
from tkinter import messagebox
from typing import Optional
from easyAI import Negamax, Human_Player, AI_Player
from chomp_game.Chomp import Chomp

MIN_SIZE = 2
MAX_SIZE = 5
DEFAULT_COLOR = "#4CAF50"
PLAYER1_COLOR = "#BBEE22"
PLAYER2_COLOR = "#22FF00"

styles = {
    "default": {
        "font": ("Arial", 12),
        "width": 5
    },
    "button": {
        "font": ("Arial", 12),
        "bg": DEFAULT_COLOR,
        "fg": "white",
        "activebackground": "#45a049",
        "padx": 20,
        "pady": 10,
        "borderwidth": 2,
        "relief": "raised",
        "width": 20
    },
    "label": {
        "font": ("Arial", 14),
        "bg": "#e8f5e9"
    },
    "title_label": {
        "font": ("Arial", 24, "bold"),
        "bg": "#e8f5e9"
    }
}

class ChompGUI:
    def __init__(self, game: Chomp, window_width: int, window_height: int) -> None:
        """
        Initializes the main game window and sets up the buttons.

        Parameters:
        game (Chomp): The game object.
        window_width (int): Width of the window.
        window_height (int): Height of the window.
        """
        self.button_frame = None
        self.label = None
        self.game = game
        self.window = tk.Tk()
        self.window.title("Chomp Game")
        self.colors = {
            "default": DEFAULT_COLOR,
            "player1": PLAYER1_COLOR,
            "player2": PLAYER2_COLOR,
        }
        self.setup_window(window_width, window_height)
        self.create_widgets()
        self.update_buttons()
        self.window.mainloop()

    def setup_window(self, width: int, height: int) -> None:
        """
        Sets up the window's dimensions and position.

        Parameters:
        width (int): Width of the window.
        height (int): Height of the window.
        """
        self.window.geometry(f"{width}x{height}")
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")

    def create_widgets(self) -> None:
        """
        Creates the UI components of the game, including buttons and labels.
        """
        self.label = tk.Label(self.window, text=self.current_player_text(), **styles["label"])
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=10)

        self.buttons = [
            [self.create_button(x, y) for x in range(self.game.max_x)]
            for y in range(self.game.max_y)
        ]

        for x in range(self.game.max_x):
            self.button_frame.grid_columnconfigure(x, weight=1)

    def create_button(self, x: int, y: int) -> tk.Button:
        """
        Creates a button for the game board.

        Parameters:
        x (int): The x-coordinate for the button.
        y (int): The y-coordinate for the button.

        Returns:
        tk.Button: The created button.
        """
        button = tk.Button(self.button_frame, text="X",
                           command=lambda xy=f"{x + 1}{y + 1}": self.handle_button_click(xy),
                           **styles["button"])
        button.grid(row=y, column=x, padx=5, pady=5)
        return button

    def current_player_text(self) -> str:
        """
        Returns a string indicating the current player's turn.

        Returns:
        str: Text indicating the current player.
        """
        if isinstance(self.game.players[self.game.current_player - 1], AI_Player):
            return "Current Player: Computer"
        return f"Current Player: Player {self.game.current_player}"

    def update_buttons(self) -> None:
        """
        Updates the state of the buttons and the current player label.
        """
        for y in range(self.game.max_y):
            for x in range(self.game.max_x):
                if self.game.board[y][x] == 0:
                    self.buttons[y][x].config(text="X", state=tk.DISABLED, bg=self.colors["player1" if self.game.current_player == 1 else "player2"])
                else:
                    self.buttons[y][x].config(text="X", state=tk.NORMAL, bg=self.colors["default"])
        self.label.config(text=self.current_player_text())

    def handle_button_click(self, move: str) -> None:
        """
        Handles a button click event for a player's move.

        Parameters:
        move (str): The move made by the player in the format "xy".
        """
        if not self.game.is_over() and not isinstance(self.game.players[self.game.current_player - 1], AI_Player):
            self.game.make_move(move)
            self.update_buttons()
            self.switch_player_if_needed()

    def switch_player_if_needed(self) -> None:
        """
        Switches to the next player if the game is not over.
        """
        if not self.game.is_over():
            self.game.current_player = 2 if self.game.current_player == 1 else 1
            if isinstance(self.game.players[self.game.current_player - 1], AI_Player):
                self.update_buttons()
                self.window.after(1000, self.ai_move)
        if self.game.is_over():
            self.show_winner_message()

    def ai_move(self) -> None:
        """
        Executes the AI player's move and updates the game state accordingly.
        """
        self.lock_buttons()
        ai_move = self.game.players[self.game.current_player - 1].ask_move(self.game)
        self.game.make_move(ai_move)
        self.update_buttons()
        if self.game.is_over():
            self.show_winner_message()
        else:
            self.game.current_player = 2 if self.game.current_player == 1 else 1
            self.update_buttons()
        self.unlock_buttons()

    def lock_buttons(self) -> None:
        """
        Disables all buttons on the board.
        """
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)

    def unlock_buttons(self) -> None:
        """
        Enables the buttons on the board that are available for the move.
        """
        for y in range(self.game.max_y):
            for x in range(self.game.max_x):
                if self.game.board[y][x] == 1:
                    self.buttons[y][x].config(state=tk.NORMAL)

    def show_winner_message(self) -> None:
        """
        Displays a message indicating the winner and offers to restart the game.
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
        Restarts the game.
        """
        self.window.destroy()
        choose_game_mode()

def choose_game_mode(default_negamax_depth: int = 15) -> None:
    """
    Displays the game mode selection window.

    Parameters:
    default_negamax_depth (int): Default Negamax depth for AI player.
    """
    mode_window = tk.Tk()
    mode_window.title("Choose Game Mode")
    mode_window.configure(bg="#e8f5e9")

    window_width = 400
    window_height = 400
    mode_window.geometry(f"{window_width}x{window_height}")

    screen_width = mode_window.winfo_screenwidth()
    screen_height = mode_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    mode_window.geometry(f"+{x}+{y}")

    def start_game(is_ai: bool, negamax_depth: Optional[int]) -> None:
        """
        Starts the game based on the selected mode and board size.

        Parameters:
        is_ai (bool): Whether the game is played against AI.
        negamax_depth (Optional[int]): Negamax depth for AI.
        """
        try:
            width = int(x_entry.get())
            height = int(y_entry.get())
            if width < MIN_SIZE or height < MIN_SIZE:
                raise ValueError(f"Both dimensions must be at least {MIN_SIZE}.")
            if width > MAX_SIZE or height > MAX_SIZE:
                raise ValueError(f"Both dimensions must be at most {MAX_SIZE}.")
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

        label_height = 130 if height < 3 else 120
        label_width = 60 if width > 3 else 120
        if height >= 4:
            button_height = 12
        if height >= 5:
            button_height += 1
        if height >= 8:
            button_height += 1

        window_width = button_width * width * button_padding_x + label_width
        window_height = button_height * height * button_padding_y + label_height

        ChompGUI(game, window_width, window_height)

    title_label = tk.Label(mode_window, text="Chomp Game", **styles["title_label"])
    title_label.pack(pady=20)

    size_label = tk.Label(mode_window, text=f"Enter map size \n\n(width X height, min 2x2, max {MAX_SIZE}x{MAX_SIZE}):", **styles["label"])
    size_label.pack(pady=10)

    size_frame = tk.Frame(mode_window, bg="#e8f5e9")
    size_frame.pack(pady=10)

    x_entry = tk.Entry(size_frame, **styles["default"])
    x_entry.pack(side=tk.LEFT, padx=(0, 5))

    tk.Label(size_frame, text="X", font=("Arial", 12), bg="#e8f5e9").pack(side=tk.LEFT, padx=(0, 5))

    y_entry = tk.Entry(size_frame, **styles["default"])
    y_entry.pack(side=tk.LEFT)

    ai_button = tk.Button(mode_window, text="Play with AI", command=lambda: start_game(True, default_negamax_depth), **styles["button"])
    ai_button.pack(pady=10)

    player_button = tk.Button(mode_window, text="Play with another player", command=lambda: start_game(False, None), **styles["button"])
    player_button.pack(pady=10)

    mode_window.mainloop()

if __name__ == '__main__':
    choose_game_mode(15)
