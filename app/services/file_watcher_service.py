import logging

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from app.config.config import Config

logger = logging.getLogger(__name__)


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.data_repository_service = Config().data_repository_service

    # def on_moved(self, event):
    #     if event.src_path in self.file_paths:
    #         logger.info("File has been moved: %s", event.src_path)
    #         config = Config()
    #         config.load_today_data(event.src_path)

    # def on_created(self, event):
    #     if event.src_path in self.file_paths:
    #         logger.info("File has been created: %s", event.src_path)
    #         config = Config()
    #         config.load_today_data(event.src_path)

    def on_modified(self, event):
        if event.src_path in self.file_paths:
            logger.info("Detected change in file: %s", event.src_path)
            config = Config()
            for ep in config.configurations:
                if ep.file == event.src_path:
                    self.data_repository_service.reload_data(event.src_path)

    # def on_deleted(self, event):
    #     if event.src_path in self.file_paths:
    #         logger.info("File has been deleted: %s", event.src_path)
    #         # config = Config()
    #         # config.load_today_data(event.src_path)


class FileWatcherService:
    def __init__(self):
        self.observer = Observer()
        self.event_handler = None

    def start_watching(self, file_paths):
        self.event_handler = FileChangeHandler(file_paths)
        for file_path in file_paths:
            self.observer.schedule(self.event_handler, path=file_path, recursive=True)
        self.observer.start()
        logger.info("Started monitoring files: %s", file_paths)

    def stop_watching(self):
        self.observer.stop()
        self.observer.join()
