from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.config import ConfigParser, Config
from kivy.uix.settings import Settings
from kivy.logger import Logger
import jsonIO, twoismCrawler, time


def call_crawler(self):
    twoismCrawler.main()

class MainApp(App):
    
    config = ConfigParser()
    config.read('main.ini')
    print("seconds_in_file:" , config.getint('Time Settings','seconds_in_file'))
    seconds = config.getint('Time Settings', 'seconds_in_file')
    clocky = Clock.schedule_interval(call_crawler, seconds)

    def build(self):
        
        pass


    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('Time Settings', {'settings_from_list': '15 minutes'})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        settings.add_json_panel('Time Settings', self.config, 'crawler_config.json')

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))
    
        def reschedule_seconds(new_seconds):
            self.seconds = new_seconds
            config.set('Time Settings', 'seconds_in_file', new_seconds)
            config.write()
            clocky = Clock.schedule_interval(call_crawler, new_seconds)

        if section == "Time Settings":
            if key == "settings_from_list":
                Clock.unschedule(self.clocky)
                if value == '15 minutes':
                    reschedule_seconds(900)
                elif value == '30 minutes':
                    reschedule_seconds(1800)
                elif value == '1 hour':
                    reschedule_seconds(3600)
                elif value == '2 hours':
                    reschedule_seconds(7200)
                elif value == '4 hours':
                    reschedule_seconds(14400)
                elif value == '8 hours':
                    reschedule_seconds(28800)
                elif value == 'Daily':
                    reschedule_seconds(86400)
                elif value == '5 seconds':
                    reschedule_seconds(5)

if __name__ == '__main__':
    app = MainApp()
    app.run()
