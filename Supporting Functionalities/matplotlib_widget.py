from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.web_view = QWebEngineView(self)
        self.layout.addWidget(self.web_view)

    def plot_data(self, data, chart_type='line', title="Chart"):
        fig = None
        if chart_type == 'line':
            fig = go.Figure(data=go.Scatter(y=data))
        elif chart_type == 'bar':
            fig = go.Figure(data=go.Bar(y=data))
        elif chart_type == 'scatter':
            fig = go.Figure(data=go.Scatter(y=data, mode='markers'))
        elif chart_type == 'pie':
            fig = px.pie(values=data, names=[str(x) for x in range(len(data))])
        elif chart_type == 'histogram':
            fig = px.histogram(x=data)

        if fig:
            fig.update_layout(title=title)
            plot_div = plot(fig, output_type='div', include_plotlyjs='cdn')
            self.web_view.setHtml(plot_div)

    # Additional plotting methods can be added here
    # Example: Time series, heatmaps, box plots, etc.

# Example usage
# widget = MatplotlibWidget()
# widget.plot_data([1, 2, 3, 4], 'line', 'Sample Line Chart')
