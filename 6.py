import customtkinter as ctk
from tkinter import messagebox
import time
import threading


class Card:
    def __init__(self, balance=50000):
        self.balance = balance

    def pay(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False


class Passenger:
    def __init__(self, name, card):
        self.name = name
        self.card = card



class Sensor:
    def __init__(self):
        self.detected = False

    def detect(self):
        self.detected = True

    def clear(self):
        self.detected = False


class Motor:
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False


class Gate:
    def __init__(self):
        self.is_open = False
        self.motor = Motor()

    def open_gate(self):
        self.motor.start()
        self.is_open = True

    def close_gate(self):
        self.motor.start()
        self.is_open = False


class MetroGateGUI:

    FARE = 7000

    def __init__(self):

        self.card = Card()
        self.passenger_count = 0

        self.sensor = Sensor()
        self.gate = Gate()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.geometry("1100x700")
        self.root.title("Metro Gate Simulator")

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self.root,
            text="🚇 METRO GATE SIMULATOR",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        self.info = ctk.CTkLabel(
            self.root,
            text="",
            font=("Arial",18)
        )
        self.info.pack()

        self.canvas = ctk.CTkCanvas(
            self.root,
            width=900,
            height=350,
            bg="#1b1b1b",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        self.draw_gate()

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        ctk.CTkButton(
            frame,
            text="💳 Tap Card",
            width=200,
            command=self.tap_card
        ).grid(row=0,column=0,padx=10)

        ctk.CTkButton(
            frame,
            text="🚶 Passenger Entry",
            width=200,
            command=self.passenger_enter
        ).grid(row=0,column=1,padx=10)

        ctk.CTkButton(
            frame,
            text="🚶 Passenger Exit",
            width=200,
            command=self.passenger_exit
        ).grid(row=0,column=2,padx=10)

        self.update_labels()

    def update_labels(self):

        state = "OPEN" if self.gate.is_open else "CLOSED"

        self.info.configure(
            text=
            f"Balance: {self.card.balance} Toman     |     "
            f"Passengers: {self.passenger_count}     |     "
            f"Sensor: {'ACTIVE' if self.sensor.detected else 'OFF'}     |     "
            f"Gate: {state}"
        )

    def draw_gate(self):

        self.canvas.delete("all")

        self.canvas.create_rectangle(
            50,100,850,250,
            outline="white",
            width=3
        )

        self.canvas.create_rectangle(
            430,100,
            450-self.left_pos,
            250,
            fill="cyan",
            outline=""
        )

        self.canvas.create_rectangle(
            450+self.right_pos,
            100,
            470,
            250,
            fill="cyan",
            outline=""
        )

        color = "lime" if self.sensor.detected else "red"

        self.canvas.create_oval(
            300,70,330,100,
            fill=color
        )

        self.canvas.create_text(
            315,
            55,
            text="Sensor",
            fill="white"
        )

    left_pos = 0
    right_pos = 0

    def animate_open(self):

        self.gate.open_gate()

        for i in range(40):

            self.left_pos = i
            self.right_pos = i

            self.draw_gate()

            self.root.update()
            time.sleep(0.02)

        self.update_labels()

    def animate_close(self):

        for i in range(40, -1, -1):

            self.left_pos = i
            self.right_pos = i

            self.draw_gate()

            self.root.update()
            time.sleep(0.02)

        self.gate.close_gate()

        self.update_labels()

    def tap_card(self):

        if self.card.pay(self.FARE):

            threading.Thread(
                target=self.open_sequence
            ).start()

        else:

            messagebox.showerror(
                "Error",
                "Insufficient Balance!"
            )

    def open_sequence(self):

        self.animate_open()

        time.sleep(3)

        self.animate_close()

    def passenger_enter(self):

        self.sensor.detect()

        self.passenger_count += 1

        self.draw_gate()
        self.update_labels()

        self.root.after(
            1500,
            self.clear_sensor
        )

    def passenger_exit(self):

        self.sensor.detect()

        if self.passenger_count > 0:
            self.passenger_count -= 1

        self.draw_gate()
        self.update_labels()

        self.root.after(
            1500,
            self.clear_sensor
        )

    def clear_sensor(self):

        self.sensor.clear()
        self.draw_gate()
        self.update_labels()



if __name__ == "__main__":
    MetroGateGUI()