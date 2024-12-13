import contextlib
import threading
import time

import kiln_server.server as kiln_server
import uvicorn
from kiln_ai.datamodel import set_strict_mode

from app.desktop.studio_server.data_gen_api import connect_data_gen_api
from app.desktop.studio_server.finetune_api import connect_fine_tune_api
from app.desktop.studio_server.prompt_api import connect_prompt_api
from app.desktop.studio_server.provider_api import connect_provider_api
from app.desktop.studio_server.repair_api import connect_repair_api
from app.desktop.studio_server.settings_api import connect_settings
from app.desktop.studio_server.webhost import connect_webhost

# Our app server runs in strict mode
set_strict_mode(True)


def make_app():
    app = kiln_server.make_app()
    connect_provider_api(app)
    connect_prompt_api(app)
    connect_repair_api(app)
    connect_settings(app)
    connect_data_gen_api(app)
    connect_fine_tune_api(app)

    # Important: webhost must be last, it handles all other URLs
    connect_webhost(app)
    return app


def server_config(port=8757):
    return uvicorn.Config(
        make_app(),
        host="127.0.0.1",
        port=port,
        log_level="warning",
        use_colors=False,
    )


class ThreadedServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        self.stopped = False
        thread = threading.Thread(target=self.run_safe, daemon=True)
        thread.start()
        try:
            while not self.started and not self.stopped:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()

    def run_safe(self):
        try:
            self.run()
        finally:
            self.stopped = True

    def running(self):
        return self.started and not self.stopped


def run_studio():
    uvicorn.run(kiln_server.app, host="127.0.0.1", port=8757, log_level="warning")


def run_studio_thread():
    thread = threading.Thread(target=run_studio)
    thread.start()
    return thread
