import asyncio
import logging
from app.config.config import Config
from app.models import CommandLineArgs
from flask import Flask, url_for
from app.calendar.routes import calendar_bp, create_routes_from_config
from app.services.data_repository_service import DataRepositoryService
from app.services.file_watcher_service import FileWatcherService

class Host:
    def __init__(self, args: CommandLineArgs):
        """
        Initialize the Host class with command line arguments and configuration.

        Parameters:
        args (CommandLineArgs): Command line arguments passed to the script.
        """
        self.args = args
        self.config = Config()
        self.file_watcher_service = FileWatcherService()
        self.config.set_server_host(args.server)
        self.config.set_server_port(args.port)   
        if args.config:
            self.config.load_config(args.config)
            self.config.data_repository_service = DataRepositoryService(self.config.configurations) 
            self.start_file_watcher([ep.file for ep in self.config.configurations])          
        self.logger = logging.getLogger(__name__)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.register_blueprint(calendar_bp)

        # Dynamically add routes based on configuration
        create_routes_from_config(self.app, self.config)        

      
    def start_file_watcher(self, file_paths):
        """
        Start the file watcher to monitor changes to the specified files.
        """
        self.file_watcher_service.start_watching(file_paths)      
    
    def run(self):
        """
        Run the asynchronous run_async method.
        """
        return asyncio.run(self.run_async())

    async def run_async(self):
        """
        Asynchronous method to perform the main logic.
        """
        self.logger.info("Starting host process.")
        
        # Start Flask server in an asynchronous loop
        loop = asyncio.get_event_loop()
        server = loop.create_task(self.start_flask_server())

        # Perform other asynchronous tasks here
        # await self.other_async_tasks()

        await server  # Keep the server running

    async def start_flask_server(self):
        """
        Start Flask server in a separate thread.
        """
        from werkzeug.serving import run_simple
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(
            None,
            lambda: run_simple(self.config.server_host, self.config.server_port, self.app, use_debugger=True),
        )        
        await future
        

# if __name__ == '__main__':
#     # Setup logging configuration
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     )

#     # Example usage, adjust how args are passed in your actual implementation
#     args = CommandLineArgs()
#     host = Host(args)
#     host.run()
