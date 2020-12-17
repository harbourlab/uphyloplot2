#!/usr/bin/env python
# Stefan Kurtenbach
# Stefan.Kurtenbach@me.com
def main():
    version = "2.2"
    print("UPhyloplot2 version " + version)
    import csv
    import math
    import os
    import copy
    import shutil
    import argparse

######### GENERATING CSV Files starts here

    parser = argparse.ArgumentParser(description='UPhyloPlot2_args')
    parser.add_argument('-c','--cutoff', help='define cutoff of clones, default is 5', required=False, type=int, default=5)
    args = vars(parser.parse_args())

    cutoff = args["cutoff"]


    if os.path.exists("CNV_files"):
        shutil.rmtree("CNV_files")
    os.mkdir("CNV_files")

    nr_of_inputs = 0
    for working_file in os.listdir("./Inputs/"):
        if working_file.endswith(".cell_groupings"):
            nr_of_inputs += 1
            with open("./Inputs/" + working_file) as groupings_file:
                subclones = [] # these are the subclones directly from the file, can be used to calculate percentages
                for x, line in enumerate(groupings_file):
                    subclone_concatenated = ""
                    if x > 0:
                        line_split = line.split("\t")[0]
                        line_split = line_split.split(".")
                        subclone = []
                        for i in line_split:
                            if len(i) == 1:
                                try:
                                    subclone.append(int(i))
                                except:
                                    pass

                        for j in subclone:
                            if subclone_concatenated == "":
                                subclone_concatenated = str(j)
                            else:
                                subclone_concatenated += "."
                                subclone_concatenated += str(j)
                        subclones.append(subclone_concatenated)

        ### remove all subclones with lower than cutoff percentage
            total_cells = len(subclones)
            subclones_cutoffed = []
            for i in subclones:
                percentage = subclones.count(i) * 100 / total_cells
                if percentage >= cutoff:
                    subclones_cutoffed.append(i)

        ### add all missing subclones, (which will have 0 percent cells). 1.1.1.1 needs 1.1.1, 1.1, and 1 too, which is missing in the data sometimes
            subclones_with_branches = copy.copy(subclones_cutoffed)
            temp = []
            for i in subclones_with_branches:
                try:
                    x = i
                    while len(x) > 2:
                        x = x[:-2]
                        temp.append(x) # will create a lot of duplicates but doesn't matter here as they are filtered later
                except:
                    pass
            for i in temp:
                subclones_with_branches.append(i)

        ########## the following is neccessary to sort the list correctly, makes all entries same length
            expanded_unique_subclones = [] #unique subclones including branches
            for i in subclones_with_branches:
                x = i
                while len(x) < 7:
                    x += (".0")
                expanded_unique_subclones.append(x)
            unique_subclones = sorted(list(set(expanded_unique_subclones)))
        # now remove all .0 again
            unique_subclones_final = []
            for i in unique_subclones:
                x = i
                while x[-2:] == ".0":
                    x = x[:-2]
                unique_subclones_final.append(x)
        ###########

        #### determine percentages and remove cells with cutoff
            clones_percentages = [] # [[Clone, Percentage], ...]
            for i in unique_subclones_final:
                percentage = subclones.count(i) * 100/total_cells
                clones_percentages.append([i, percentage])

            with open("./CNV_files/"+working_file+'.csv', mode='w') as output:
                writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in clones_percentages:
                    writer.writerow(i)



######### PLOTTING STARTS HERE

    clones_IDs = []  # list of clones, and their letter in the plot [[clone, letter], ..]
    output = []
#colors = ["#8E8E8E", "#EA9898", "#71C2C6", "#EDB843", "#C270E8", "#6E5BDD", "#7FAD7F", "#8E8E8E", "#EA9898", "#71C2C6", "#EDB843", "#C270E8", "#6E5BDD", "#7FAD7F", "#8E8E8E", "#EA9898", "#71C2C6", "#EDB843", "#C270E8", "#6E5BDD", "#7FAD7F", "#8E8E8E", "#EA9898", "#71C2C6", "#EDB843", "#C270E8", "#6E5BDD", "#7FAD7F"]  # first is grey
    colors = ["#C15A5B", "#9DABC5", "#81BED0", "#AAD1B6", "#6AAB73", "#E7E689", "#D89560", "#85593E", "#C55E7B", "#9F8272", "#365584", "#6582A2", "#6B8675", "#61497B", "#E7C665", "#E7C689", "#A89593", "#C15A5B", "#9DABC5", "#81BED0", "#AAD1B6", "#6AAB73", "#E7E689", "#D89560", "#85593E", "#C55E7B", "#9F8272", "#365584", "#6582A2", "#6B8675", "#61497B", "#E7C665", "#E7C689", "#A89593", "#C15A5B", "#9DABC5", "#81BED0", "#AAD1B6", "#6AAB73", "#E7E689", "#D89560", "#85593E", "#C55E7B", "#9F8272", "#365584", "#6582A2", "#6B8675", "#61497B", "#E7C665", "#E7C689", "#A89593", "#C15A5B", "#9DABC5", "#81BED0", "#AAD1B6", "#6AAB73", "#E7E689", "#D89560", "#85593E", "#C55E7B", "#9F8272", "#365584", "#6582A2", "#6B8675", "#61497B", "#E7C665", "#E7C689", "#A89593"]
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

    ABC = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "@", "#", "$", "%", "^", "&", "*", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
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
    for working_file in os.listdir("./CNV_files"):
            if working_file.endswith(".csv"):
                plot_nr += 1
                sample_name = working_file.split(".")[0]
                output.append('''<text x="''' + str(start_pos[0] + space_between_plots*plot_nr) + '''" y="''' + str(start_pos[1]) + '''" text-anchor='middle' font-family="'ArialMT'" font-size="">''' + sample_name + '''</text>''')
                with open("CNV_files/" + working_file) as current_file:
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
                                                if [row[0], text] not in clones_IDs:
                                                    clones_IDs.append([row[0], text])
                                                break
                                        output.append('''<text text-anchor='middle' ><tspan x="''' + str(current_circle[1] + delta_x + start_pos[0] + plot_nr * space_between_plots) + '''" y="''' + str(current_circle[2] + delta_y + start_pos[1] + 15 + 3) + '''" font-family="'ArialMT'" font-size="8">''' + text + '''</tspan>''')
                                        output.append("</text>")
                        current_circles = copy.copy(next_circles)


    write_to_file('''<svg viewBox="0 0 ''' + str(nr_of_inputs*150) + ''' 300" xmlns="http://www.w3.org/2000/svg">''')

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


##############  Replace all CSV files, and add which letter was assigned to the clones

    for working_file in os.listdir("./CNV_files"):
        if working_file.endswith(".csv"):
            with open("./CNV_files/" + working_file) as current_file:
                reader = csv.reader(current_file, delimiter=",")
                input_data = list(reader)
                for x, i in enumerate(input_data):
                    for p, q in enumerate(clones_IDs):
                        if i[0] == q[0]:
                            input_data[x].append(clones_IDs[p][1])

            with open("./CNV_files/"+working_file, mode='w') as output:
                writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in input_data:
                    writer.writerow(i)

if __name__ == '__main__':
    main()
