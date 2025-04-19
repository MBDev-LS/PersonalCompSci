#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import chess

# Unicode symbols for chess pieces.
UNICODE_PIECES = {
    'K': '\u2654', 'Q': '\u2655', 'R': '\u2656',
    'B': '\u2657', 'N': '\u2658', 'P': '\u2659',
    'k': '\u265A', 'q': '\u265B', 'r': '\u265C',
    'b': '\u265D', 'n': '\u265E', 'p': '\u265F'
}

# Modern color palette for the board.
LIGHT_SQUARE_COLOR = "#f0d9b5"   # light brown
DARK_SQUARE_COLOR = "#b58863"    # dark brown
HIGHLIGHT_COLOR = "#77DD77"      # a soft green highlight

# Size (in pixels) of each square.
SQUARE_SIZE = 72

class ChessGUI(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Set a modern theme.
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            # In case "clam" is not available, use default.
            pass

        self.master.title("Modern Chess")
        self.board = chess.Board()

        # A dictionary mapping square (0-63) to the canvas rectangle id.
        self.square_ids = {}
        # Dictionary mapping square to piece text id.
        self.piece_ids = {}

        # To keep track of drag & drop state.
        self.drag_data = {
            "piece": None,        # The Unicode symbol for the piece being dragged.
            "from_square": None,  # The board square (0-63) from which the drag started.
            "item": None,         # The canvas text item id of the piece being dragged.
            "offset_x": 0,        # Offset of mouse pointer from piece center.
            "offset_y": 0
        }
        # List to store highlight rectangle ids.
        self.highlight_ids = []

        self.create_widgets()
        self.draw_board()
        self.draw_pieces()

    def create_widgets(self):
        # Main container
        self.pack(fill="both", expand=True)

        # Create a Canvas widget for the chess board.
        canvas_size = SQUARE_SIZE * 8
        self.canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        # Bind mouse events for drag & drop.
        self.canvas.bind("<ButtonPress-1>", self.on_piece_press)
        self.canvas.bind("<B1-Motion>", self.on_piece_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_piece_release)

        # Status frame using ttk.
        status_frame = ttk.Frame(self)
        status_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        status_frame.columnconfigure(0, weight=1)

        self.status_label = ttk.Label(status_frame, text="", font=("Helvetica", 16))
        self.status_label.grid(row=0, column=0, sticky="w")
        self.update_status()

    def draw_board(self):
        """Draw the board squares."""
        self.canvas.delete("square")
        for rank in range(8):
            for file in range(8):
                # Top-left coordinates.
                x1 = file * SQUARE_SIZE
                y1 = rank * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE

                # Convert to chess board square.
                board_rank = 7 - rank  # rank 7 corresponds to chess rank 0, so flip the y-axis.
                square = chess.square(file, board_rank)

                color = LIGHT_SQUARE_COLOR if (file + board_rank) % 2 == 0 else DARK_SQUARE_COLOR
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags="square")
                self.square_ids[square] = rect_id

    def draw_pieces(self):
        """Draw chess pieces from the board state."""
        self.canvas.delete("piece")
        self.piece_ids = {}

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                symbol = UNICODE_PIECES.get(piece.symbol(), piece.symbol())
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                display_rank = 7 - rank
                x = file * SQUARE_SIZE + SQUARE_SIZE // 2
                y = display_rank * SQUARE_SIZE + SQUARE_SIZE // 2
                text_id = self.canvas.create_text(x, y, text=symbol, font=("Helvetica", 40), tags="piece")
                self.piece_ids[square] = text_id

    def update_status(self):
        """Update the status label to show turn or game over."""
        if self.board.is_game_over():
            if self.board.is_checkmate():
                winner = "Black" if self.board.turn == chess.WHITE else "White"
                status_text = f"Checkmate! {winner} wins!"
            elif self.board.is_stalemate():
                status_text = "Stalemate!"
            elif self.board.is_insufficient_material():
                status_text = "Draw due to insufficient material."
            else:
                status_text = "Game over."
        else:
            turn = "White" if self.board.turn == chess.WHITE else "Black"
            status_text = f"{turn}'s turn."
        self.status_label.config(text=status_text)

    def clear_highlights(self):
        """Remove all highlighted squares."""
        for hid in self.highlight_ids:
            self.canvas.delete(hid)
        self.highlight_ids = []

    def highlight_moves(self, from_square):
        """Highlight all legal destination squares for the piece on from_square."""
        self.clear_highlights()
        for move in self.board.legal_moves:
            if move.from_square == from_square:
                dest = move.to_square
                rect_id = self.square_ids.get(dest)
                if rect_id:
                    x1, y1, x2, y2 = self.canvas.coords(rect_id)
                    # Draw a dashed rectangle with a modern look.
                    hid = self.canvas.create_rectangle(x1+4, y1+4, x2-4, y2-4,
                                                       outline=HIGHLIGHT_COLOR,
                                                       width=3, dash=(6, 4), tags="highlight")
                    self.highlight_ids.append(hid)

    def on_piece_press(self, event):
        """Pick up a piece if one exists at the click location."""
        file = event.x // SQUARE_SIZE
        rank = event.y // SQUARE_SIZE
        board_rank = 7 - rank
        square = chess.square(file, board_rank)

        piece = self.board.piece_at(square)
        if not piece:
            return

        # Only allow moving pieces that match the turn.
        if piece.color != self.board.turn:
            return

        self.drag_data["from_square"] = square
        self.drag_data["piece"] = UNICODE_PIECES.get(piece.symbol(), piece.symbol())
        piece_id = self.piece_ids.get(square)
        if not piece_id:
            return
        self.drag_data["item"] = piece_id
        x, y = self.canvas.coords(piece_id)
        self.drag_data["offset_x"] = x - event.x
        self.drag_data["offset_y"] = y - event.y
        self.canvas.tag_raise(piece_id)
        self.highlight_moves(square)

    def on_piece_motion(self, event):
        """Move the dragged piece."""
        item = self.drag_data["item"]
        if item:
            new_x = event.x + self.drag_data["offset_x"]
            new_y = event.y + self.drag_data["offset_y"]
            self.canvas.coords(item, new_x, new_y)

    def on_piece_release(self, event):
        """Drop the piece on a square if legal."""
        from_square = self.drag_data["from_square"]
        if from_square is None:
            return

        file = event.x // SQUARE_SIZE
        rank = event.y // SQUARE_SIZE
        board_rank = 7 - rank
        to_square = chess.square(file, board_rank)

        # If dropped on the original square, cancel the drag.
        if to_square == from_square:
            self.reset_drag()
            return

        move = chess.Move(from_square, to_square)
        if move in self.board.legal_moves:
            self.board.push(move)
        else:
            messagebox.showerror("Illegal Move", "That move is not legal!")
        self.reset_drag()
        self.draw_pieces()
        self.update_status()

        if self.board.is_game_over():
            self.show_game_over()

    def reset_drag(self):
        """Reset drag state and clear move highlights."""
        self.drag_data = {"piece": None, "from_square": None, "item": None, "offset_x": 0, "offset_y": 0}
        self.clear_highlights()
        self.draw_pieces()

    def show_game_over(self):
        """Display a modern game-over screen with options to start a new game or exit."""
        # Create a transparent-ish overlay.
        overlay = tk.Toplevel(self.master)
        overlay.grab_set()  # Make the dialog modal.
        overlay.title("Game Over")
        overlay.geometry("300x200")
        overlay.resizable(False, False)
        # Center the window.
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - 150
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - 100
        overlay.geometry(f"+{x}+{y}")

        frame = ttk.Frame(overlay, padding=20)
        frame.pack(expand=True, fill="both")

        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            message = f"Checkmate!\n{winner} wins!"
        elif self.board.is_stalemate():
            message = "Stalemate!"
        elif self.board.is_insufficient_material():
            message = "Draw: Insufficient material."
        else:
            message = "Game Over."

        label = ttk.Label(frame, text=message, font=("Helvetica", 18), anchor="center")
        label.pack(expand=True)

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=(10, 0))

        new_game_btn = ttk.Button(button_frame, text="New Game", command=lambda: self.new_game(overlay))
        new_game_btn.grid(row=0, column=0, padx=5)

        exit_btn = ttk.Button(button_frame, text="Exit", command=self.master.destroy)
        exit_btn.grid(row=0, column=1, padx=5)

    def new_game(self, overlay):
        """Reset the board for a new game."""
        overlay.destroy()
        self.board.reset()
        self.draw_board()
        self.draw_pieces()
        self.update_status()

    def run(self):
        self.master.mainloop()

def main():
    root = tk.Tk()
    app = ChessGUI(master=root)
    app.run()

if __name__ == "__main__":
    main()
