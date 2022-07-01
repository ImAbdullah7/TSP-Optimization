import data_model

class Map:
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        self.verticies = []
        self.lines = []

    def delete_vertex(self, name):
         vi = [i for i, item in enumerate(self.verticies) if item[0] == name][0]
         v = self.verticies.pop(vi)
         self.canvas.delete(v[1])
         self.canvas.update()

    def add_vertex(self, name):
        lat, lon = data_model.get_coordinate_of(name)
        x, y = self.get_xy(lat, lon)
        dot = self.canvas.create_oval(x-4, y-4, x+4, y+4, fill='red', width=0)
        self.verticies.append((name, dot, x, y))
        # print(f'x: {x}, y:{y}')

    def delete_lines(self):
        for l in self.lines:
            self.canvas.delete(l)
        self.lines.clear()

    def draw_lines(self, ver):
        self.delete_lines()
        for i in range(len(ver)):
            l = self.canvas.create_line(ver[i-1][2], ver[i-1][3], ver[i][2], ver[i][3], fill='white', width=2)
            self.lines.append(l)
        self.canvas.update()

    def get_xy(self, lat, lon):
        # x
        # x_lower_limit = 35
        x_lower_limit = 18
        lat_lower_limit = 34.9451498
        # x_range = 430
        x_range = 522
        lat_range = 15.2519883


        current_lat_range = lat - lat_lower_limit
        current_x_pr = current_lat_range / lat_range
        additional_x = x_range * current_x_pr

        x =  x_lower_limit + additional_x

        # y
        # y_lower_limit = 500
        y_lower_limit = 590
        lon_lower_limit = 16.5279447
        # y_range = 483
        y_range = 555
        lon_range = 15.1381328

        current_lon_range = lon - lon_lower_limit
        current_y_pr = current_lon_range / lon_range
        additional_y = y_range * current_y_pr

        y = y_lower_limit - additional_y

        return (x, y)





















    # canvas.create_oval(137, 15, 141, 19, fill='red')
    # x = 35
    # y = 93
    # x = 465
    # y = 195
    # canvas.create_oval(x-2, y-2, x+2, y+2, fill='red')