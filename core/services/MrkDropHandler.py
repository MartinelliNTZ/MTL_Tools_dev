# -*- coding: utf-8 -*-
import os

from qgis.core import (
    QgsApplication,
    QgsDataItem,
    QgsDataItemProvider,
    QgsDataProvider,
    QgsMimeDataUtils,
)
from qgis.gui import QgsCustomDropHandler
from qgis.PyQt.QtCore import QFileInfo

from ...i18n.TranslationManager import STR
from ...utils.QgisMessageUtil import QgisMessageUtil
from ..io.MrkDropHandler import MrkDropHandler as MrkDropIO
from .DroneCoordinatesRunner import DroneCoordinatesRunner


class MrkDropHandler(QgsCustomDropHandler):
    PROVIDER_KEY = "cadmus_mrk"

    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.runner = DroneCoordinatesRunner(iface)

    def handleFileDrop(self, file):
        if not MrkDropIO.is_mrk_file(file):
            return False

        QgisMessageUtil.bar_info(self.iface, STR.MRK_DROP_START, duration=3)
        return bool(self.runner.run_mrk_file(file))

    def customUriProviderKey(self):
        return self.PROVIDER_KEY

    def handleCustomUriDrop(self, uri):
        if not uri:
            return
        self.handleFileDrop(uri.uri)


class MrkBrowserItem(QgsDataItem):
    def __init__(self, parent, path, handler: MrkDropHandler):
        super().__init__(QgsDataItem.Type.Custom, parent, QFileInfo(path).baseName(), path)
        self._handler = handler
        self.setState(QgsDataItem.State.Populated)
        self.setToolTip(path)

    def hasDragEnabled(self):
        return True

    def handleDoubleClick(self):
        return self._handler.handleFileDrop(self.path())

    def mimeUri(self):
        uri = QgsMimeDataUtils.Uri()
        uri.layerType = "custom"
        uri.providerKey = self._handler.customUriProviderKey()
        uri.name = self.name()
        uri.uri = self.path()
        return uri


class MrkBrowserItemProvider(QgsDataItemProvider):
    def __init__(self, handler: MrkDropHandler):
        super().__init__()
        self._handler = handler

    def name(self):
        return MrkDropHandler.PROVIDER_KEY

    def capabilities(self):
        return QgsDataProvider.DataCapability.File

    def createDataItem(self, path, parentItem):
        if not MrkDropIO.is_mrk_file(path):
            return None
        if not os.path.isfile(path):
            return None
        return MrkBrowserItem(parentItem, path, self._handler)


class MrkDropRegistration:
    """Registro central do handler oficial de drop do QGIS."""

    def __init__(self, iface):
        self.iface = iface
        self.drop_handler = MrkDropHandler(iface)
        self.item_provider = MrkBrowserItemProvider(self.drop_handler)
        self._registered = False

    def register(self):
        if self._registered:
            return
        self.iface.registerCustomDropHandler(self.drop_handler)
        QgsApplication.dataItemProviderRegistry().addProvider(self.item_provider)
        self._registered = True

    def unregister(self):
        if not self._registered:
            return
        self.iface.unregisterCustomDropHandler(self.drop_handler)
        QgsApplication.dataItemProviderRegistry().removeProvider(self.item_provider)
        self._registered = False
