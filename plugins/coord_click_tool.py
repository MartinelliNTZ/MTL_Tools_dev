from qgis.gui import QgsMapTool
from qgis.core import QgsApplication
import sip

from ..utils.reverse_geocoding_task import ReverseGeocodeTask
from ..utils.altimetry_task import AltimetriaTask
from ..utils.crs_utils import get_coord_info
from ..dialogs.coord_result_dialog import CoordResultDialog


class CoordClickTool(QgsMapTool):

    def __init__(self, iface):
        super().__init__(iface.mapCanvas())
        self.iface = iface
        self.canvas = iface.mapCanvas()

        self.dialog = None
        self.address_task = None
        self.alt_task = None

    def canvasReleaseEvent(self, event):
        snap = self.canvas.snappingUtils().snapToMap(event.pos())
        point = snap.point() if snap.isValid() else self.toMapCoordinates(event.pos())

        info = get_coord_info(
            point,
            self.canvas.mapSettings().destinationCrs()
        )

        # -----------------------------
        # VIEW
        # -----------------------------
        if not self.dialog or not self.dialog.isVisible():
            self.dialog = CoordResultDialog(self.iface, info)
            self.dialog.show()
        else:
            self.dialog.update_info(info)

        # -----------------------------
        # Cancela tasks antigas
        # -----------------------------
        self._cancel_task(self.address_task)
        self._cancel_task(self.alt_task)

        lat, lon = info["lat"], info["lon"]

        # -----------------------------
        # Reverse Geocode (MODEL)
        # -----------------------------
        def on_address(result, error):
            if error:
                self.dialog.set_address(None)
                self.iface.messageBar().pushWarning(
                    "Geocodificação", error
                )
            else:
                self.dialog.set_address(result)

        self.address_task = ReverseGeocodeTask(lat, lon, on_address)
        QgsApplication.taskManager().addTask(self.address_task)

        # -----------------------------
        # Altimetria (MODEL)
        # -----------------------------
        def on_altitude(value, error):
            if error:
                self.dialog.set_altitude(None)
                self.iface.messageBar().pushWarning(
                    "Altimetria", error
                )
            else:
                self.dialog.set_altitude(value)

        self.alt_task = AltimetriaTask(lat, lon, on_altitude)
        QgsApplication.taskManager().addTask(self.alt_task)

    # --------------------------------------------------
    # Utils
    # --------------------------------------------------
    def _cancel_task(self, task):
        if task and not sip.isdeleted(task):
            if not task.isCanceled():
                task.cancel()
