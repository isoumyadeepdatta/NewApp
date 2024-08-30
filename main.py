from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.garden.graph import Graph, LinePlot
import serial

class SerialPlot(BoxLayout):
    def __init__(self, **kwargs):
        super(SerialPlot, self).__init__(**kwargs)

        # Initialize serial connection
        self.ser = serial.Serial('COM3', 9600, timeout=1)

        # Setup graph
        self.graph = Graph(xlabel='Time', ylabel='Value', x_ticks_minor=5,
                           x_ticks_major=25, y_ticks_major=0.25,
                           y_grid_label=True, x_grid_label=True,
                           padding=0.5, xlog=False, ylog=False,
                           x_grid=True, y_grid=True, xmin=0, xmax=100, ymin=-2, ymax=2)
        self.plot = LinePlot(line_width=1.5, color=[1, 0, 0, 1])
        self.graph.add_plot(self.plot)
        self.add_widget(self.graph)

        # Schedule the plot update
        Clock.schedule_interval(self.update_plot, 1.0 / 60.0)  # 60 Hz refresh rate

        self.data_points = []

    def update_plot(self, dt):
        if self.ser.in_waiting:
            data = self.ser.readline().decode('utf-8').strip()
            try:
                value = float(data)
                self.data_points.append(value)

                # Keep only the latest 100 points
                if len(self.data_points) > 100:
                    self.data_points.pop(0)

                self.plot.points = [(i, self.data_points[i]) for i in range(len(self.data_points))]
            except ValueError:
                pass  # Handle invalid data

class SerialPlotApp(App):
    def build(self):
        return SerialPlot()

if __name__ == '__main__':
    SerialPlotApp().run()
