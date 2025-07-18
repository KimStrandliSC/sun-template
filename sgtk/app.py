import re
import sys
import pathlib

import sgtk

logger = sgtk.platform.get_logger(__name__)


class SgtkWrapper(sgtk.platform.Application):

    def init_app(self):
        logger.info('Running App init_app function')

        icon_path = pathlib.Path(__file__).parent / "button_icon.png"

        version = '?.?.?'
        with open(pathlib.Path(__file__).parent / "version.py", "r") as versionFile: 
            content = versionFile.read()
            findVersion = re.search('__version__ = "(.+)"', content)
            if findVersion:
                version = findVersion.group(1)

        # Add a command for opening the Main UI
        self.engine.register_command(
            name = f"Sun Template v{version}",
            callback = self.launch_app,
            properties = {
                "short_name": "sun_template_sgtk",
                "icon": str(icon_path),
            }
        )


        # Initialize the sitepackages for the app
        self.init_sitepackages()

    def app_python(self):
        return pathlib.Path(__file__).parent / f"python_{sys.version_info.major}.{sys.version_info.minor}"

    def init_sitepackages(self):
        # We dont have any local sitepackage needs for this app
        """
        # Grab a handler from the python bootstrap framework
        pythonBootstrapFramework = self.frameworks["sgtk-framework-sun-python"]
        bootstrap_handler = pythonBootstrapFramework.handler()

        # Resolve the local python folder for the App
        pythonFolder = self.app_python()

        # Grab the requirements file and install contents
        bootstrap_handler.install_requirements(
            pythonFolder / 'requirements.txt',
            pythonFolder
        )
        """
        pass

    def destroy_app(self):
        logger.info('Running destroy_app function')
        pass

    def launch_app(self):
        # Get the bootstrap framework
        pythonBootstrapFramework = self.frameworks["sgtk-framework-sun-python"]
        bootstrap_handler = pythonBootstrapFramework.handler()

        qtVersion = bootstrap_handler.qt_version()
        if bootstrap_handler.is_older_version(qtVersion, "6.5.8"):
            bootstrap_handler.show_update_dialog(self, "2.1.0")
            return

        launchFilePath = str(self.app_python() / "sun_premiere" / "ui" / "SunControllerUI" / "open_ui.pyc")

        # Include this apps own python folder
        # It has its "own" requirements(installed in init) thats not part of the bootstrap or shotgrid python env
        incl_paths = [
            str(self.app_python())
        ]

        # Launch our script though the handler
        bootstrap_handler.launch_app(
            launchFilePath,
            frameworks=self.frameworks,  # If we had more frameworks, pythonpaths from them would be added
            incl_paths=incl_paths,
            envvars={
                'sun_project_id': str(self.engine.context.to_dict().get('project')['id']),
            },
            logger=logger
        )
