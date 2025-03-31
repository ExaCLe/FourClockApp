import csv
import time
import tkinter as tk


class ClockColor:
    def __init__(self, background, foreground):
        self.background = background
        self.foreground = foreground


def read_colors() -> ClockColor:
    """
    Reads the colors from a .csv file for the clock
    :return: the clock colors
    """
    # Default colors
    clock_color = ClockColor("white", "black")

    try:
        with open("colors.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            # Just use the first row from the CSV
            for row in reader:
                background = rgb_to_hex(str_to_tuple(row["background (r,g,b)"]))
                foreground = rgb_to_hex(str_to_tuple(row["foreground (r,g,b)"]))
                clock_color = ClockColor(background, foreground)
                break
    except Exception as e:
        print(f"Error reading colors: {e}")

    return clock_color


class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)  # Set fullscreen mode
        self.root.bind("<Escape>", self.quit)  # Exit fullscreen on Escape key
        self.root.bind("<space>", self.toggle_timer)

        self.start_time = None  # time.time() when timer started
        self.passed_time = 0.0

        text_size = self.root.winfo_screenheight() // 3
        self.setup_clock(text_size)

    def setup_clock(self, text_size):
        """
        Handles the initial setup for the clock
        :param text_size:
        :return:
        """
        colors = read_colors()

        # Single frame for the clock
        self.frame = tk.Frame(self.root, bg=colors.background)
        self.frame.pack(expand=True, fill="both")

        # Single label for the clock
        self.clock_label = tk.Label(
            self.frame,
            font=("Helvetica", text_size, "bold"),
            bg=colors.background,
            fg=colors.foreground,
        )
        self.clock_label.pack(expand=True)

        self.update_time()

    def update_time(self):
        """
        Updates the clock label and calls itself each millisecond
        :return:
        """
        if self.start_time is None:
            current_time = self.passed_time
        else:
            current_time = self.passed_time + time.time() - self.start_time

        time_string = f"{current_time:.3f}"
        self.clock_label.config(text=time_string)
        self.root.after(1, self.update_time)

    def toggle_timer(self, event=None):
        """
        Start or stop the timer
        :param event:
        :return:
        """
        if self.start_time is None:
            self.start_time = time.time()
        else:
            self.passed_time += time.time() - self.start_time
            self.start_time = None

    def quit(self, event=None):
        self.root.destroy()


def str_to_tuple(string: str) -> tuple[int, ...]:
    """
    Converts a string to a tuple of integers. The string can contain brackets, so '(255, 0, 0)' or '255, 0, 0' are valid
    :param string: string to convert
    :return: converted tuple
    """
    string = string.strip().strip("()")
    return tuple(map(int, string.split(",")))


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """
    Converts a tuple of rgb values to a hex string
    :param rgb: the tuple to convert
    :return: the hex string
    """
    return "#%02x%02x%02x" % rgb


if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()
