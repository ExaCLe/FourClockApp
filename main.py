import csv
import time
import tkinter as tk


class ClockColor:
    def __init__(self, background, foreground):
        self.background = background
        self.foreground = foreground


index_mapping: dict[str, int] = {
    'top-left': 0,
    'top-right': 1,
    'bottom-left': 2,
    'bottom-right': 3
}


def read_colors() -> list[ClockColor]:
    """
    Reads the colors from a .csv file for each clock and returns them as a list
    :return: the list of colors
    """
    colors = [ClockColor('white', 'black') for _ in range(4)]
    with open('colors.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            background = rgb_to_hex(str_to_tuple(row['background (r,g,b)']))
            foreground = rgb_to_hex(str_to_tuple(row['foreground (r,g,b)']))
            index = index_mapping[row['position']]
            colors[index] = ClockColor(background, foreground)
    return colors


class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)  # Set fullscreen mode
        self.root.bind('<Escape>', self.quit)  # Exit fullscreen on Escape key
        self.root.bind('<space>', self.toggle_timer)

        self.start_time = None  # time.time() when timer started
        self.passed_time = 0.0

        text_size = self.root.winfo_screenheight() // 5  # this size fits well until about 1000 seconds
        self.labels = []
        self.frames = []
        self.setup_clocks(text_size)

    def setup_clocks(self, text_size):
        """
        Handles the initial setup for the clocks
        :param text_size:
        :return:
        """
        # container frames for positioning the clocks
        top = tk.Frame(self.root, bg='orange')
        top.pack(expand=True, fill='both')
        bottom = tk.Frame(self.root, bg='orange')
        bottom.pack(expand=True, fill='both')

        colors = read_colors()

        # frames for the clocks
        for i in range(4):
            frame = tk.Frame(top if i < 2 else bottom, bg=colors[i].background)
            frame.pack(expand=True, fill='both', side='left' if i % 2 == 0 else 'right')
            self.frames.append(frame)

        # labels for the clocks
        for index, frame in enumerate(self.frames):
            clock_label = tk.Label(frame, font=('Helvetica', 100, 'bold'), bg=colors[index].background,
                                   fg=colors[index].foreground)
            clock_label.pack(expand=True)
            self.labels.append(clock_label)

            clock_label.config(font=('Helvetica', text_size, 'bold'))
        self.update_time()

    def update_time(self):
        """
        Updates all the clock labels and calls itself each millisecond
        :return:
        """
        if self.start_time is None:
            current_time = self.passed_time
        else:
            current_time = self.passed_time + time.time() - self.start_time

        time_string = f"{current_time:.3f}"
        for label in self.labels:
            label.config(text=time_string)
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
    string = string.strip().strip('()')
    return tuple(map(int, string.split(',')))


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """
    Converts a tuple of rgb values to a hex string
    :param rgb: the tuple to convert
    :return: the hex string
    """
    return '#%02x%02x%02x' % rgb


if __name__ == '__main__':
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()
