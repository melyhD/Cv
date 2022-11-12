class Firmus:
    def __init__(self, block1, block2):
        self.block1 = block1
        self.block2 = block2

    def is_firmus(self):
        x1, x2 = [self.block1[0], self.block1[2]], [self.block2[0], self.block2[2]]
        y1, y2 = [self.block1[1], self.block1[3]], [self.block2[1], self.block2[3]]

        x_list = x1 + x2

        y_list = y1 + y2
        y_set = set(y_list)

        x1_max, x1_min, x2_max, x2_min = max(x1), min(x1), max(x2),min(x2)
        y1_max, y1_min, y2_max, y2_min = max(y1), min(y1), max(y2),min(y2)

        # Addendum Value

        if max(y_list) in y1:
            up_box, dwn_box = x1, [x2, y2]
        else:
            up_box, dwn_box = x2, [x1, y1]

        com = (up_box[0]+ up_box[1])/2

        if com > max(dwn_box[0]):
            add_x1, add_x2 = 2*max(dwn_box[0]) - max(up_box), min(up_box)
        else:
            add_x1, add_x2 = 2*min(dwn_box[0]) - min(up_box), max(up_box)

        add_box = [add_x2, max(dwn_box[1]), add_x1, max(y_list)]

        # Intersection Area

        inter_area = 0

        if ((x1_min < x2_max and x1_min > x2_min) or (x1_max < x2_max and x1_max > x2_min) or (x1_max > x2_max and x1_min < x2_min)) and (
            (y1_min < y2_max and y1_min > y2_min) or (y1_max < y2_max and y1_max > y2_min) or (y1_max > y2_max and y1_min < y2_min)):

            x_list.sort()
            x_inter = x_list[1] - x_list[2]

            y_list.sort()
            y_inter = y_list[1] - y_list[2]

            inter_area = x_inter*y_inter

        ###

        area = abs((x1[0] - x1[1])*(y1[0] - y1[1])) + abs((x2[0] - x2[1])*(y2[0] - y2[1]))

        if min(y_list) != 0 or (y1_max != y2_min and y2_max != y1_min) or x1_max < x2_min or len(y_list) == len(y_set):
            state = "DAMNARE"
            value = float(area - inter_area)
        elif com > max(dwn_box[0]) or com < min(dwn_box[0]):
            state = "ADDENDUM"
            value = add_box
        else:
            state = "FIRMUS"
            value = float(area)

        return [state, value]