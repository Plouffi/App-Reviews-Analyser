from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

from src.domain.services.i_plot_service import IPlotService

class ApplicationUtils():

	@staticmethod 
	def get_image_from_plot(plot_service: IPlotService, fig: Figure):
		image = io.BytesIO()
		FigureCanvas(fig).print_png(image)
		plot_service.refresh()
		return image