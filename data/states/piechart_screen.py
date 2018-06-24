import pygame as pg

from .. import tools, prepare
from ..components.labels import Label
from ..components.bar_graph import PieChart, StackedBarGraph
from ..components.standings import TOTALS, PIE_COLORS


class PieChartScreen(tools._State):
    def __init__(self):
        super(PieChartScreen, self).__init__()
        self.chart = PieChart((290, 10), 350, TOTALS, PIE_COLORS)
        
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
        self.chart.draw(surface)
        