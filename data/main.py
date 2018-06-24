from . import prepare,tools
from .states import title_screen, bargraph_screen, piechart_screen

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"TITLE": title_screen.TitleScreen(),
                   "BARGRAPH": bargraph_screen.BargraphScreen(),
                   "PIECHART": piechart_screen.PieChartScreen()}
    controller.setup_states(states, "TITLE")
    controller.main()
