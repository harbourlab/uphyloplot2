# UPhyloPlot2 Version 1.0
# Stefan Kurtenbach
# Stefan.Kurtenbach@me.com


import csv
import math
import os
import copy

output = []
#colors = ["#8E8E8E", "#EA9898", "#71C2C6", "#EDB843", "#C270E8", "#6E5BDD", "#7FAD7F", "#8E8E8E", "#EA9898", "#71C2C6", "#EDB843", "#C270E8", "#6E5BDD", "#7FAD7F", "#8E8E8E", "#EA9898", "#71C2C6", "#EDB843", "#C270E8", "#6E5BDD", "#7FAD7F", "#8E8E8E", "#EA9898", "#71C2C6", "#EDB843", "#C270E8", "#6E5BDD", "#7FAD7F"]  # first is grey
colors = ["#C15A5B", "#9DABC5", "#81BED0", "#AAD1B6", "#6AAB73", "#E7E689", "#D89560", "#85593E", "#C55E7B", "#9F8272", "#365584", "#6582A2", "#6B8675", "#61497B", "#E7C665", "#E7C689", "#A89593"]
current_color = 0

overall_scale_factor = 1        # total size of everything
scale_factor_data = 2
radius_circles = 5.0
circle_color = "#C4C4C4"
rect_width = 10.0
angle_of_subclones = 30.0
start_pos = [60, 20]
space_between_plots = 110
additional_space_between_circles = 5 + (2 * radius_circles)

ABC = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "O", "P", "Q"]

filename = "output.svg"
if os.path.exists(filename):
    os.remove(filename)

def write_to_file(row):
    with open(filename, "a") as f:
        f.write(row)
        f.write("\n")


def draw_rect(x_coord, y_0, hight, opacity, angle, color):
    return '''<rect x="''' + str(x_coord + start_pos[0] - (rect_width/2) + plot_nr*space_between_plots) + '''" opacity="''' + str(opacity) + '''" y="''' + str(y_0 + start_pos[1] + 15) + '''" fill="''' + color + '''" width="''' + str(rect_width) + '''" height="''' + str(hight) + '''" transform="rotate(''' + str(-angle) + ''' ''' + str(x_coord + start_pos[0] + plot_nr*space_between_plots) + ''' ''' + str(y_0 + start_pos[1] + 15) + ''')"/>'''


def draw_circle(x_coord, y_coord):
    return '''<circle fill="''' + circle_color + '''" stroke="#000000" stroke-width="0" stroke-miterlimit="10" cx="''' + str(x_coord + start_pos[0] + plot_nr*space_between_plots) + ''' " cy=''' + '''"''' + str(y_coord + start_pos[1] + 15) + '''"''' + ''' r="''' + str(radius_circles) + '''"/>'''


plot_nr = -1
for working_file in os.listdir("./Inputs"):
    if working_file.endswith(".csv"):
        plot_nr += 1
        sample_name = working_file.split(".")[0]
        output.append('''<text x="''' + str(start_pos[0] + space_between_plots*plot_nr) + '''" y="''' + str(start_pos[1]) + '''" text-anchor='middle' font-family="'ArialMT'" font-size="">''' + sample_name + '''</text>''')
        with open("Inputs/" + working_file) as current_file:
### draw first two circles and bar as they are always the same
            output.append(draw_rect(0, 0, 100 + additional_space_between_circles, 100, 0, colors[0])) # rect  2 radius added to still have small spaces between circles for small numbers
            current_color = 1
            current_circles = [[1, 0, 100 + additional_space_between_circles, 0]]  # circle nr, x, y, nr of next branches (counter to know which angle)
            output.append(draw_circle(0, 0))  # circle 0
            output.append(draw_circle(current_circles[0][1], current_circles[0][2]))  # circle 1

            output.append('''<text text-anchor='middle' ><tspan x="''' + str(current_circles[0][1] + start_pos[0] + plot_nr * space_between_plots) + '''" y="''' + str(current_circles[0][2] + start_pos[1] + 15 + 3) + '''" font-family="'ArialMT'" font-size="8">A</tspan>''')
            output.append("</text>")

            reader = csv.reader(current_file, delimiter=",")
            input_data = list(reader)

            longest_tree = 0
            for data_row in input_data:
                if len(data_row[0].split(".")) > longest_tree:
                    longest_tree = len(data_row[0].split("."))

            for step in range(longest_tree):  # first circle is already placed
                next_circles = []

                for data_row in input_data:
                    #print(data_row)
                    if len(data_row[0].split(".")) == step + 2:  # if one of the next circles (starts with 1.1, 1.2 for ==step+2
                        for current_circle in current_circles:
                            if data_row[0][:len(str(current_circle[0]))] == str(current_circle[0]):  # is that a subsequent circle?
                                if step == 0: current_angle = 60
                                else: current_angle = angle_of_subclones
                                for iteration in range(current_circle[3]): # define which angle
                                    if current_angle < 0:
                                        current_angle -= angle_of_subclones
                                    current_angle *= -1
                                current_circle[3] += 1

                                delta_x = ((math.sin(math.radians(current_angle))) * (float(data_row[1]) * scale_factor_data + additional_space_between_circles)) * overall_scale_factor
                                delta_y = ((math.cos(math.radians(current_angle))) * (float(data_row[1]) * scale_factor_data + additional_space_between_circles)) * overall_scale_factor

                                output.append(draw_rect(current_circle[1], current_circle[2], float(data_row[1]) * scale_factor_data + additional_space_between_circles, 100, current_angle, colors[current_color]))
                                current_color += 1
                                output.append(draw_circle(current_circle[1] + delta_x, current_circle[2] + delta_y))
                                next_circles.append([data_row[0], current_circle[1] + delta_x, current_circle[2] + delta_y, 0])


                                text = str(data_row[0])
                                for rownr, row in enumerate(input_data):
                                    if row[0] == text:
                                        text = ABC[rownr]
                                        break


                                output.append('''<text text-anchor='middle' ><tspan x="''' + str(current_circle[1] + delta_x + start_pos[0] + plot_nr * space_between_plots) + '''" y="''' + str(current_circle[2] + delta_y + start_pos[1] + 15 + 3) + '''" font-family="'ArialMT'" font-size="8">''' + text + '''</tspan>''')
                                output.append("</text>")


                current_circles = copy.copy(next_circles)


write_to_file('''<svg viewBox="0 0 ''' + str(plot_nr*150) + ''' 300" xmlns="http://www.w3.org/2000/svg">''')
for i in output:
    if i[:5] == "<rect":  # make sure circles are always on top
        write_to_file(i)
for i in output:
    if i[:5] == "<circ":
        write_to_file(i)
for i in output:
    if i[:5] != "<circ" and i[:5] != "<rect":
        write_to_file(i)
write_to_file("</svg>")
