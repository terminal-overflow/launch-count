from datetime import datetime
import pytz
from enum import Enum
from math import floor
import tkinter as tk

from parse import ParseInfo

UTC_LT_TZ = [
    "Atlantic/Cape_Verde",
    "Atlantic/South_Georgia",
    "America/Godthab",
    "Atlantic/Bermuda",
    "America/New_York",
    "America/Chicago",
    "America/Denver",
    "America/Los_Angeles",
    "America/Juneau",
    "Pacific/Honolulu",
]

UTC_GT_TZ = [
    "Atlantic/Reykjavik",
    "Europe/London",
    "Europe/Paris",
    "Europe/Moscow",
    "Asia/Kolkata",
    "Asia/Almaty",
    "Asia/Shanghai",
    "Asia/Tokyo",
    "Australia/Sydney",
    "Pacific/Auckland",
]


class TZ_TRANSLATIONS_LT(Enum):
    CAPE_VERDE = UTC_LT_TZ[0]
    SOUTH_GEORGIA = UTC_LT_TZ[1]
    GREENLAND = UTC_LT_TZ[2]
    FRENCH_GUIANA = UTC_LT_TZ[3]
    NEW_YORK = UTC_LT_TZ[4]
    CHICAGO = UTC_LT_TZ[5]
    DENVER = UTC_LT_TZ[6]
    LOS_ANGELES = UTC_LT_TZ[7]
    ALASKA = UTC_LT_TZ[8]
    HAWAII = UTC_LT_TZ[9]


class TZ_TRANSLATIONS_GT(Enum):
    REYKJAVIK = UTC_GT_TZ[0]
    LONDON = UTC_GT_TZ[1]
    FRANCE = UTC_GT_TZ[2]
    MOSCOW = UTC_GT_TZ[3]
    INDIA = UTC_GT_TZ[4]
    KAZAKHSTAN = UTC_GT_TZ[5]
    CHINA = UTC_GT_TZ[6]
    JAPAN = UTC_GT_TZ[7]
    AUSTRALIA = UTC_GT_TZ[8]
    NEW_ZEALAND = UTC_GT_TZ[9]


class MainApp(tk.Tk):
    """
    The Main App class.
    Initialises the `Tk` superclass.
    Adds configuration for the window and the frames enclosed.
    """

    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Date Countdown Timer")
        self.configure(background="black")
        self.wm_minsize(1200, 400)
        # Ensure rows and columns grow and shrink
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, minsize=200)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Keybinds
        self.bind("q", self.close)
        self.bind("f", self.fullscreen_toggle)
        self.bind("<Escape>", self.fullscreen_close)
        self.bind("r", self.resize_fonts)

        self.fs = False
        self.dates = ParseInfo().dates

        # Timer display frame
        self.timer_display = CountTimerDisplay(self, self.dates)
        self.timer_display.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Timezone frames
        self.left_zones = TimeDisplay(self, TZ_TRANSLATIONS_LT)
        self.left_zones.grid(padx=20, pady=10, row=1, column=0, sticky="nsew")

        self.right_zones = TimeDisplay(self, TZ_TRANSLATIONS_GT)
        self.right_zones.grid(padx=20, pady=10, row=1, column=2, sticky="nsew")

    def close(self, event):
        self.destroy()

    def fullscreen_toggle(self, event):
        self.fs = not self.fs
        self.wm_attributes("-fullscreen", self.fs)
        self.resize_fonts(event)
        self.update_idletasks()

    def fullscreen_close(self, event):
        self.fs = False
        self.wm_attributes("-fullscreen", "false")
        self.resize_fonts(event)
        # Prevents overlapping of labels on resize
        self.update_idletasks()

    def resize_fonts(self, event):
        """Resize label fonts based on the window size."""
        widget_width = self.winfo_width()
        # Calculate new font size based on window width
        small_font_size = max(20, int(widget_width / 60))
        # medium_font_size = max(20, int(widget_width / 60))
        large_font_size = max(40, int(widget_width / 30))

        # Update the frames
        self.timer_display.update_font_size(large_font_size)
        self.left_zones.update_font_size(small_font_size)
        self.right_zones.update_font_size(small_font_size)


class CountTimerDisplay(tk.Frame):
    """The Tk Frame for the counter."""

    def __init__(self, parent: MainApp, dates: list[datetime]):
        super().__init__(parent, background="black")

        # Ensure the frame columns expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.timer = CountTimer(self, dates)

        # Count label
        self.count_label = tk.Label(
            self,
            text="--:--:--",
            font=("Arial", 40),
            foreground="white",
            background="black",
        )
        self.count_label.grid(pady=20, row=0, column=1, sticky="nsew")

        # Target date label
        self.date_label = tk.Label(
            self,
            text="--/--/--",
            font=("Arial", 25),
            foreground="white",
            background="black",
        )
        self.date_label.grid(pady=20, row=0, column=0, sticky="nsew")

        # Target time label
        self.time_label = tk.Label(
            self,
            text="--:--:--",
            font=("Arial", 25),
            foreground="white",
            background="black",
        )
        self.time_label.grid(pady=20, row=0, column=2, sticky="nsew")

        # Start countup/down
        self.timer.start(self.update_display)

    def update_display(self, time_str, color: str = "blue"):
        """A callback that updates the label with the time string passed in."""
        self.count_label.config(text=f"{time_str}", foreground=color)

    def update_font_size(self, font_size):
        self.count_label.config(font=("Arial", font_size))
        self.date_label.config(font=("Arial", int(font_size / 1.6)))
        self.time_label.config(font=("Arial", int(font_size / 1.6)))


class CountTimer:
    """Updates the Count with the correct time string representation."""

    def __init__(self, display: CountTimerDisplay, dates: list[datetime]):
        self.display = display
        self.dates = dates
        self.target_date: None | datetime = None
        self.is_counting_up = False

    def start(self, update_callback):
        """Initialises the count."""
        self.update_callback = update_callback
        self.find_next_date()
        self.count()

    def find_next_date(self):
        """
        Gets the target date - the closest date in the future.
        If one is not present, the most recent date is used as a reference and
        the timer should start counting up.
        """
        now = datetime.now()
        self.target_date = next((d for d in self.dates if d > now), None)
        if not self.target_date:
            # All dates are in the past; start counting up from the last date
            self.target_date = self.dates[-1]
            self.is_counting_up = True
        else:
            self.is_counting_up = False

    def count(self):
        """
        Calculates the remaining/elapsed time and updates the display accordingly.
        Updates every 1000ms
        """
        now = datetime.now()
        if self.is_counting_up:
            elapsed = now - self.target_date
            time_str = f"+{str(elapsed).split('.')[0]}"
        else:
            remaining = self.target_date - now
            if remaining.total_seconds() > 0:
                time_str = f"-{str(remaining).split('.')[0]}"
            else:
                self.find_next_date()
                self.count()
                return

        # Update the display
        self.update_callback(time_str, self.get_colour())

        # Update date and time
        self.display.date_label.config(text=f"{self.target_date.strftime('%Y/%m/%d')}")
        self.display.time_label.config(text=f"{self.target_date.strftime('%H:%M:%S')}")

        self.display.after(1000, self.count)

    def get_colour(self):
        """
        Returns the colour for the count.
        Counting up: GREEN.
        Less than 10 seconds and odd numbers: DARK RED.
        Less than 1 hour: RED.
        More than one hour: BLUE.
        """
        remaining = self.target_date - datetime.now()
        remaining_seconds = floor(remaining.total_seconds())
        if self.is_counting_up:
            return "green"
        elif remaining_seconds < 10 and remaining_seconds % 2 == 1:
            return "darkred"
        elif remaining.total_seconds() // 3600 < 1:
            return "red"
        else:
            return "blue"


class TimeDisplay(tk.Frame):
    """
    The Tk Frame for the Timezone displays.
    Also handles the logic to highlight and update the times.
    """

    def __init__(self, parent, tz_translations: Enum):
        super().__init__(parent, background="black")
        self.tz_translations = tz_translations
        self.locations = ParseInfo().locations
        self.update_interval = 1000
        self.labels = []  # Store labels for updating

        # Set up initial labels for each timezone
        for row, tz_translation in enumerate(self.tz_translations):
            # Get the standard timezone name. Replace '_' with ' ' from the Enum.
            tz_name: str = tz_translation.name.replace("_", " ").lower()

            if tz_name in self.locations:
                time_colour = "yellow"
            else:
                time_colour = "green"

            label_name = tk.Label(
                self,
                text=tz_name.title(),
                foreground="white",
                background="black",
                font=("Arial", 25),
                padx=20,
                pady=10,
            )
            label_name.grid(row=row, column=0, sticky="w")

            label_time = tk.Label(
                self,
                text="",
                foreground=time_colour,
                background="black",
                font=("Arial", 25),
                padx=20,
                pady=10,
            )
            label_time.grid(row=row, column=1, sticky="w")
            self.labels.append((label_name, label_time))
            self.grid_rowconfigure(row, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Start updating the times
        self.update_times()

    def update_times(self):
        """
        Get the current time for the timezone and update each label.
        Updates every 1000ms
        """
        utc_now = datetime.now(pytz.utc)

        # Update each timezone's displayed time
        for (label_name, label_time), tz_translation in zip(
            self.labels, self.tz_translations
        ):
            tz = pytz.timezone(tz_translation.value)
            current_time = utc_now.astimezone(tz).strftime("%d:%m:%Y %H:%M:%S %Z %z")
            label_time.config(text=current_time)

        # Schedule the next update
        self.after(self.update_interval, self.update_times)

    def update_font_size(self, font_size):
        for label_name, label_time in self.labels:
            label_name.config(font=("Arial", font_size))
            label_time.config(font=("Arial", font_size))


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
