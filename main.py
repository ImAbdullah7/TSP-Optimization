import tkinter as tk
import tkintermapview
from PIL import ImageTk, Image

from time import time

import map
import data_model
import lexicographic_order
import hill_climbing
import random_restart_hill_climbing
import simulated_annealing
import genetic_algorithm

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def delete_place_clicked(name):
    info = [(idx, button) for idx, button in enumerate(selected_places) if button['text'] == name]
    button = info[0][1]
    button.grid_forget()
    index = info[0][0]
    selected_places.pop(index)
    places_menu['menu'].add_command(label=name, command=lambda: place_choice.set(name))
    place_choice.set(name)
    update_selected_places()
    map.delete_lines()
    map.delete_vertex(name)
    global last_result
    last_result = None

def add_place_clicked():
    menu = places_menu['menu']
    if menu.index('end') is None:
        print('ERROR: Menu is empty')
        return
    
    name = place_choice.get()
    name_index = get_index_of_option(menu, name)

    if name_index is None:
        print(f'ERROR: {name} not found in the menu')
        return

    button = tk.Button(selected_places_frame, text=name, width=8, command=lambda: delete_place_clicked(name))
    selected_places.append(button)
    menu.delete(name_index)

    if menu.index('end') is None:
        place_choice.set(None)
    else:
        place_choice.set(menu.entrycget(0,"label"))

    update_selected_places()
    map.add_vertex(name)
    global last_result
    last_result = None

def update_selected_places():
    text_lbl.configure(text='') if len(selected_places) > 0 else text_lbl.configure(text='No cities added yet')

    for idx, item in enumerate(selected_places):
        item.grid(row=int(idx/5), column=idx%5, padx=2)
   
def get_index_of_option(menu, name):
    for i in range(menu.index('end')+1):
        if menu.entrycget(i, 'label') == name:
            return i
    return None


def perform():
    result_txt.configure(state=tk.NORMAL)
    result_txt.delete(1.0, tk.END)
    result_txt.configure(state=tk.DISABLED)

    specific_iteration = None
    gas_efficiency = None

    #TODO: - Find another way,
    # or possibly make a module to handle it like Swift language handling it.

    try:
        specific_iteration = int(iteration_num_field.get())
    except:
        pass

    try:
        gas_efficiency = int(gas_efficiency_field.get())
    except:
        pass

    result = None
    s_time = time()

    if strategy_choice.get() == 'Try All':
        result = lexicographic_order.perform(map, specific_iteration, animate_flag.get())
        chart_it('Brute Force', 'iteration', 'evaluation', result.chart_data, result.iterations)
    elif strategy_choice.get() == 'Hill Climbing':
        result = hill_climbing.perform(map, specific_iteration, animate_flag.get())
    elif strategy_choice.get() == 'Random Restart Hill Climbing':
        result = random_restart_hill_climbing.perform(map, specific_iteration, animate_flag.get())
        chart_it('Random Restart Hill Climbing', 'iteration', 'evaluation', result.chart_data, result.iterations)
    elif strategy_choice.get() == 'Simulated Annealing':
        result = simulated_annealing.perform(map, specific_iteration, animate_flag.get())
        chart_it('Simulated Annealing', 'iteration', 'evaluation', result.chart_data, result.iterations)
    elif strategy_choice.get() == 'GA':
        result = genetic_algorithm.perform(map, specific_iteration, animate_flag.get())
        chart_it('Genetic Algorithm', 'generation', 'fitness', result.chart_data, result.iterations)

    result.gas_efficiency = gas_efficiency if gas_efficiency is not None else 15
    result.verticies = map.verticies
    global last_result
    last_result = result
    print(result)
    print(f'{len(map.verticies)}! : {result.iterations} iterations in {time() - s_time:.5}s')

    map.draw_lines(result.best_state)
    
    result_txt.configure(state=tk.NORMAL)
    result_txt.insert(tk.END, result)
    result_txt.configure(state=tk.DISABLED)


last_can = None
def chart_it(main_title, x_title, y_title, data, iterations):
    # fr = tk.Frame(frame, bg='red')
    # fr.grid(row=1, column=1, pady=2, sticky=tk.SW)
    
    f = Figure(figsize=(6.44, 3.5), dpi=120)

    ax = f.add_subplot(111)
    ax.set(xlabel=x_title, ylabel= y_title, title= main_title)

    x_data, y_data = zip(*data)
    x_data = list(x_data)
    y_data = list(y_data)
    if x_data[-1] != iterations:
        y_data.append(y_data[-1])
        x_data.append(iterations)

    ax.plot(x_data, y_data)
    
    # ax2 = f.add_subplot(212)
    # ax2.set(xlabel='time (s)', ylabel='voltage (mV)',title='About as simple as it gets, folks')
    # ax2.plot(info)

    f.tight_layout()

    global last_can
    last_can.get_tk_widget().destroy()
    last_can = FigureCanvasTkAgg(f, frame)
    # last_can.draw()
    last_can.get_tk_widget().grid(row=0, column=0, sticky=tk.NS)

def create_empty_chart(main_title, x_title, y_title,):
    # fr = tk.Frame(canvas_frame, bg='red')
    # fr.grid(row=1, column=1, pady=2, sticky=tk.SW)
    
    f = Figure(figsize=(6.44, 3), dpi=120)

    ax = f.add_subplot(111)
    ax.set(xlabel=x_title, ylabel= y_title, title= main_title)
    f.tight_layout()
    global last_can
    last_can = FigureCanvasTkAgg(f, frame)
    # last_can.draw()
    last_can.get_tk_widget().grid(row=0, column=0, sticky=tk.NS)

def open_map_window():

    map_window = tk.Toplevel(root)
    map_window.title("Maps")
    map_window.geometry("900x700")

    map_widget = tkintermapview.TkinterMapView(map_window, width=500, height=500, corner_radius=0)
    map_widget.pack(fill=tk.BOTH, expand=1)
    map_widget.set_address('sa')
    map_widget.set_zoom(5)

    for m in map.verticies:
        c = data_model.get_coordinate_of(m[0])
        map_widget.set_marker(c[1], c[0])

    if last_result:
        p = []
        for s in last_result.best_state:
            c = data_model.get_coordinate_of(s[0])
            p.append((c[1], c[0]))
        p.append(p[0])
        map_widget.set_path(p)



root = tk.Tk()
root.title('TSP')
# root.geometry('1420x1200')
root.geometry('1600x1250')
root.configure(bg='white')
# root.resizable(width=False, height=False)

# path = os.path.join(sys._MEIPASS, 'datafiles/placesfinal.xlsx')
path = 'datafiles/placesfinal.xlsx'
data_model.read(path)

# img_path = os.path.join(sys._MEIPASS, 'datafiles/map.png')
img_path = 'datafiles/map.png'

options = data_model.get_options()
selected_places = []

strategies = ['Try All', 'Random Restart Hill Climbing', 'Simulated Annealing', 'GA']

strategy_choice = tk.StringVar()
strategy_choice.set(strategies[0])

place_choice = tk.StringVar()
place_choice.set(options[0])

result_str = tk.StringVar()

animate_flag = tk.BooleanVar()

last_result = None


root_frame = tk.Frame(root)
root_frame.pack(fill=tk.BOTH, expand=1)

root_canvas = tk.Canvas(root_frame, bg='white', highlightthickness=0)
root_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

my_scrollbar = tk.Scrollbar(root_frame, orient=tk.VERTICAL, command=root_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root_canvas.configure(yscrollcommand=my_scrollbar.set)
root_canvas.bind('<Configure>', lambda e: root_canvas.configure(scrollregion = root_canvas.bbox("all")))

second_frame = tk.Frame(root_canvas, bg='white')

root_canvas.create_window((0,0), window=second_frame, anchor="nw")

frame = tk.LabelFrame(second_frame, width=1060, height=950, borderwidth=0)
frame.pack(side=tk.RIGHT, fill=tk.Y, padx=68)

canvas = tk.Canvas(second_frame, width=760, height=650, bg='white', highlightthickness=0)
canvas.pack(pady=160, padx=100)

result_lbl = tk.Label(frame, bg='systemTextBackgroundColor')
result_lbl.grid(row=1, column=0, sticky=tk.NS)

result_txt = tk.Text(result_lbl, state=tk.DISABLED, height=20, highlightbackground='systemTextBackgroundColor', highlightthickness=0)
result_txt.grid()

result_sb = tk.Scrollbar(result_lbl, orient='vertical', command=result_txt.yview)
result_sb.grid(row=0, column=2, sticky=tk.NSEW)

result_txt.configure(yscrollcommand=result_sb.set)

create_empty_chart('Optimization problem', 'iteration', 'evaluation')


map = map.Map(canvas)

img = ImageTk.PhotoImage(Image.open(img_path))  
canvas.create_image(0, 0, anchor=tk.NW, image=img)

main_frame = tk.LabelFrame(frame)
main_frame.grid(row=2, column=0, sticky=tk.NS)

selected_places_frame = tk.LabelFrame(frame, padx=5, pady=5)
selected_places_frame.grid(row=3, column=0, sticky=tk.EW)

text_lbl = tk.Label(selected_places_frame, text='No cities added yet', font=('Helvatical bold',17), width=50, height=14)
text_lbl.grid(rowspan=100, columnspan=100)

tk.Label(main_frame).grid(row=0, column=0, ipady=10)

places_menu = tk.OptionMenu(main_frame, place_choice, *options)
places_menu.grid(row=1, column=2, padx=0, pady=10)

cities_title_lbl = tk.Label(main_frame, text='City', font=('Helvatical bold',17), width=11, anchor='w')
cities_title_lbl.grid(row=1, column=1, padx=0)

strategy_menu = tk.OptionMenu(main_frame, strategy_choice, *strategies)
strategy_menu.grid(row=3, column=2, padx=30, pady=10)

strategy_title_lbl = tk.Label(main_frame, text='Algorithm', font=('Helvatical bold',17), width=11, anchor='w')
strategy_title_lbl.grid(row=3, column=1, padx=30)

gas_efficiency_field = tk.Entry(main_frame, width=8)
gas_efficiency_field.grid(row=4, column=2, padx=30, pady=10)

gas_efficiency_lbl = tk.Label(main_frame, text='Gas Efficiency', font=('Helvatical bold',17), width=11, anchor='w')
gas_efficiency_lbl.grid(row=4, column=1, padx=30)

iteration_num_field = tk.Entry(main_frame, width=8)
iteration_num_field.grid(row=5, column=2, padx=30, pady=10)

literation_title_lbl = tk.Label(main_frame, text='Logged Iteration', font=('Helvatical bold',17), width=11, anchor='w')
literation_title_lbl.grid(row=5, column=1, padx=30)


animate_cb = tk.Checkbutton(main_frame, variable=animate_flag, onvalue=True, offvalue=False, height=2, width=2)
animate_cb.grid(row=6, column=2, padx=128, pady=10)

animate_title_lbl = tk.Label(main_frame, text='Animation', font=('Helvatical bold',17), width=11, anchor='w')
animate_title_lbl.grid(row=6, column=1, padx=78)

add_btn = tk.Button(main_frame, text='add', width=5, command=add_place_clicked)
add_btn.grid(row=2, column=2, padx=5, pady=10)

perform_btn = tk.Button(main_frame, text='perform', command=perform)
perform_btn.grid(row=7, column=2, pady=30)

m_btn = tk.Button(main_frame, text='open maps', command=open_map_window)
m_btn.grid(row=7, column=1, pady=30)

tk.Label(main_frame).grid(row=0, column=0, rowspan=7, ipadx=3)

root.mainloop()