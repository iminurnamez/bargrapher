import pygame as pg

from .. import tools, prepare
from ..components.labels import Label
from ..components.bar_graph import PieChart, StackedBarGraph
from ..components.standings import STANDINGS, RANKED


class BargraphScreen(tools._State):
    def __init__(self):
        super(BargraphScreen, self).__init__()
        self.graph = StackedBarGraph((40, 20), 1240, 580,
                [(n, STANDINGS[n][::-1]) for n in RANKED],
                [pg.Color("goldenrod2"), pg.Color("gray60"), pg.Color("gold")],
                bg_color=pg.Color("gray5"))

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.done = True
                self.next = "TITLE"

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.graph.draw(surface)
