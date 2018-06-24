import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.bar_graph import PieChart, StackedBarGraph
from ..components.standings import STANDINGS


class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        cx = prepare.SCREEN_RECT.centerx
        self.title = Label("Olympics Results", {"midtop": (cx, 60)},
                    font_size=64)
        self.buttons = ButtonGroup()
        b_size = 180, 60
        Button({"midtop": (cx, 200)}, self.buttons, text="Stacked Bar",
                    button_size=b_size, fill_color="gray20",
                    call=self.to_state, args="BARGRAPH")
        Button({"midtop": (cx, 300)}, self.buttons, text="Pie Chart",
                    button_size=b_size, fill_color="gray20",
                    call=self.to_state, args="PIECHART")
        
    def to_state(self, state_name):
        self.done = True
        self.next = state_name
        
    def startup(self, persistent):
        self.persist = persistent
        
    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.buttons.get_event(event)
        
    def update(self, dt):
        self.buttons.update(pg.mouse.get_pos())

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.title.draw(surface)
        self.buttons.draw(surface)
        