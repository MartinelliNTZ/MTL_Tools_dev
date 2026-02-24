from qgis.core import QgsProcessingFeedback

class TaskFeedback(QgsProcessingFeedback):

    def __init__(self, task):
        super().__init__()
        self.task = task

    def isCanceled(self):
        return self.task.isCanceled()