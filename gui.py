import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

# Constants for traffic light states
GREEN, YELLOW, RED, OFF = range(4)

# Constants for traffic light colors
LIGHT_COLORS = ["green", "yellow", "red", "gray"]

# Constants for time intervals in milliseconds
GREEN_TIME = 15000
YELLOW_TIME = 15000


def determine_range(input_values, range_lists):
    for i, ranges in enumerate(range_lists):
        for range_str in ranges:
            range_parts = range_str.split(',')
            start1, end1 = map(int, range_parts[0].strip('[]').split('-'))
            start2, end2 = map(int, range_parts[1].strip('[]').split('-'))

            if start1 <= input_values[0] <= end1 and start2 <= input_values[1] <= end2:
                return i

    return -1


range_lists = [
    ['[0-25, 0-25]', '[0-25, 26-50]', '[26-50, 0-25]', '[26-50, 26-50]'],
    ['[0-25, 51-75]', '[0-25, 76-100]', '[26-50, 51-75]', '[26-50, 76-100]'],
    ['[51-75, 26-50]', '[76-100, 0-25]', '[76-100, 26-50]', '[51-75, 51-75]'],
    ['[51-75, 51-75]', '[51-75, 76-100]', '[76-100, 51-75]', '[76-100, 76-100]']
]

messages = [
    "Citizen, you're fortunate! Good to go with the Green Light for Road. You've waited patiently for this moment. Drive safely!",
    "Yellow for 15 sec, and then it's your turn. You've waited 15 seconds for this green light. Get ready to roll!",
    "Yellow for 30 sec, and now you're good to go with the Green for the road. You've waited half a minute for this. Drive safely!",
    "Our apologies for the extended wait. Red light, then a brief pause, and now you're good to go. You waited for a total of 60 seconds. Enjoy your ride!",
]


def change_traffic_light_colors(state):
    for i, light in enumerate([red_light, yellow_light, green_light]):
        canvas.itemconfig(light, fill=LIGHT_COLORS[i] if state == i else "gray")


def control_traffic_light_cycle(range_index):
    if range_index == 0:
        change_traffic_light_colors(GREEN)
    elif range_index == 1:
        change_traffic_light_colors(YELLOW)
        window.after(GREEN_TIME, lambda: change_traffic_light_colors(GREEN))
    elif range_index == 2:
        change_traffic_light_colors(YELLOW)
        window.after(GREEN_TIME, lambda: change_traffic_light_colors(GREEN))
    elif range_index == 3:
        change_traffic_light_colors(RED)
        window.after(YELLOW_TIME, lambda: change_traffic_light_colors(YELLOW))
        window.after(GREEN_TIME, lambda: change_traffic_light_colors(GREEN))


def determine_and_display_message():
    try:
        input_value1 = int(entry1.get())
        input_value2 = int(entry2.get())

        if input_value1 + input_value2 > 200:
            result_label.config(text="Sum of inputs exceeds 200. Please enter new inputs.")
            return

        if input_value2 >= 100:
            result_label.config(text="Attention, fellow travelers! We regret to inform you of a 100% road block ahead. Stay calm, stay safe, and we'll work to get you moving again as soon as possible. \n Your patience is greatly appreciated during this unexpected delay. \n To explore alternative routes, please click the designated button for real-time navigation assistance")
            blink_traffic_lights()
            return
        if input_value2 >= 95:
            with open('data.txt','a') as f:
                f.write('Dear Sir/Madam,PLease take needed Action ASAP. The road is blocked by 95% of encroachment/repair/accident\n')
                f.write('\n')
        input_values = [input_value1, input_value2]
        range_index = determine_range(input_values, range_lists)

        if range_index != -1:
            result_label.config(text=messages[range_index])
            control_traffic_light_cycle(range_index)
        else:
            result_label.config(text=messages[-1])
            change_traffic_light_colors(RED)
    except ValueError:
        result_label.config(text="Invalid input. Please enter valid integers.")
        change_traffic_light_colors(RED)


def blink_traffic_lights():
    for _ in range(10):  # 10 blinks
        for state in [RED, YELLOW, GREEN]:
            change_traffic_light_colors(state)
            window.update_idletasks()
            window.after(100)  # Blinking interval is 100 milliseconds (10 times per second)


def open_image():
    file_path = "123.jpg"  # Specify the image file path
    image = Image.open(file_path)
    image = image.resize((500, 500))
    photo = ImageTk.PhotoImage(image)
    image_window = tk.Toplevel(window)
    image_label = tk.Label(image_window, image=photo)
    image_label.image = photo
    image_label.pack()


# Create the tkinter window
window = tk.Tk()
window.title("Road Status Checker")

# Calculate the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the window width and height
window_width = 400
window_height = 400

# Calculate the x and y coordinates to center the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

bg_image = Image.open("Firefly background image for traffic managment system 62603.jpg")
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
window.title("Road Status Checker")

label1 = tk.Label(window, text="Percentage of Road Covered by Vehicles:")
entry1 = tk.Entry(window)
label2 = tk.Label(window, text="Percentage of Road Covered by Encroachment/Repair/Accident:")
entry2 = tk.Entry(window)

check_button = tk.Button(window, text="Check", command=determine_and_display_message)

result_label = tk.Label(window, text="")

# Create a canvas with an initial size
canvas = tk.Canvas(window, width=50, height=150, bg="white")

# Create the ovals representing traffic lights
red_light = canvas.create_oval(10, 10, 40, 40, fill="gray")
yellow_light = canvas.create_oval(10, 50, 40, 80, fill="gray")
green_light = canvas.create_oval(10, 90, 40, 120, fill="gray")

canvas_width = 50
canvas_height = 130

canvas.config(width=canvas_width, height=canvas_height)
label1.pack()
entry1.pack()
label2.pack()
entry2.pack()
check_button.pack()
result_label.pack()
canvas.pack()

open_image_button = tk.Button(window, text="Show Alternate Routes", command=open_image)
open_image_button.pack()

window.mainloop()
