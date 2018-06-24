from math import pi, degrees

import pygame as pg

from ..components.angles import project
from ..components.labels import Label


class StackedBarGraph(object):
    #values = [("America", (10, 5, 4)), ("China", (4, 9, 3))]
    #colors = [gold, silver, bronze]
    def __init__(self, topleft, width, height, values, colors, graduation=5,
                show_graduation_lines=True, graduation_line_weight=1,
                bg_color=pg.Color("black"), frame_color=pg.Color("gray80"),
                frame_weight=1, graduation_line_color=pg.Color("gray80")):
        self.width = width - (frame_weight * 2)
        self.height = height - (frame_weight * 2)
        self.rect = pg.Rect(topleft, (width, height))
        self.show_graduation_lines = show_graduation_lines
        self.graduation_line_weight = graduation_line_weight
        self.graduation_line_color = graduation_line_color
        self.bg_color = bg_color
        self.frame_color = frame_color
        self.frame_weight = frame_weight

        totals = [sum(x[1]) for x in values]
        high = max(totals)
        top_scale = ((high // graduation) + 1) * graduation
        scale_nums = list(range(0, top_scale + 1, graduation))
        y_scale = self.height / float(top_scale)
        x_spacing = self.width / float(len(values))
        bar_width = int(x_spacing * .9)
        left, top = topleft[0] + frame_weight, topleft[1] + frame_weight
        bottom = top + self.height
        self.bars = []
        self.labels = []
        self.scale_labels = []
        for name, vals in values:
            bar = StackedBar(vals, colors, bar_width, y_scale, left, bottom)
            self.bars.append(bar)
            label = Label(name, {"topleft": (0, 0)})
            img = pg.transform.rotate(label.image, 315)
            rect = img.get_rect(top=bottom, left=left)
            self.labels.append((img, rect))
            left = int(left + x_spacing)

        self.graduation_lines = []
        for x in scale_nums:
            left_side = (topleft[0], bottom - int(y_scale * x))
            right_side = self.rect.right, left_side[1]
            scale_label = Label("{}".format(x), {"midright": left_side})
            self.scale_labels.append(scale_label)
            if self.show_graduation_lines:
                self.graduation_lines.append((left_side, right_side))

    def draw(self, surface):
        surface.fill(self.bg_color, self.rect)
        pg.draw.rect(surface, self.frame_color, self.rect, self.frame_weight)
        for line in self.graduation_lines:
            pg.draw.line(surface, self.graduation_line_color, line[0], line[1],
                        self.graduation_line_weight)
        for bar in self.bars:
            bar.draw(surface)
        for label, rect in self.labels:
            surface.blit(label, rect)
        for scale_label in self.scale_labels:
            scale_label.draw(surface)


class StackedBar(object):
    def __init__(self, values, colors, bar_width, y_scale, left, bottom):
        self.rects = []
        for val, color in zip(values, colors):
            if val:
                h = int(val * y_scale)
                bottom -= h
                rect = pg.Rect(left, bottom, bar_width, h)
                self.rects.append((rect, color))

    def draw(self, surface):
        for rect, color in self.rects:
            pg.draw.rect(surface, color, rect)


class PieChart(object):
    def __init__(self, topleft, radius, values_dict, pie_colors, text_color="white"):
        self.topleft = topleft
        total = sum(values_dict.values())
        scale = (2*pi) / total
        start_angle = 0
        self.image = pg.Surface((radius*2, radius*2))
        cover = self.image.copy()
        center = radius, radius
        for name, color in zip(values_dict.keys(), pie_colors):
            p1 = project(center, start_angle, radius * 1.5)
            rads = values_dict[name] * scale
            end_angle = start_angle + rads
            p2 = project(center, end_angle, radius * 1.5)
            pg.draw.polygon(self.image, color, [center, p1, p2])

            label = Label(name, {"topleft": (0, 0)}, font_size=16, text_color=text_color)
            middle_angle = start_angle + (rads / 2.)
            middle_pos = project(center, middle_angle, int(radius * .75))
            if .5 * pi <= middle_angle <= 1.5 * pi:
                middle_angle += pi
            tag = pg.transform.rotate(label.image, degrees(middle_angle))

            r = tag.get_rect(center=middle_pos)
            self.image.blit(tag, r)
            start_angle = end_angle
        pg.draw.circle(cover, pg.Color("white"), center, radius)
        cover.set_colorkey(pg.Color("white"))
        self.image.blit(cover, (0, 0))

    def draw(self, surface):
        surface.blit(self.image, self.topleft)
