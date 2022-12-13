from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

import requests
import json
import os
import datetime

caching_dir = f"E:/Coding/tubeapp/cache/"


def fetch_data(folder_name, url=None, get_fresh_data=False, caching=True):
    if cache_exists(folder_name) and not get_fresh_data:
        data = load_cache_data(folder_name)
    else:
        session = requests.get(url)
        data = json.loads(session.content)
        if caching:
            cache_data(data, folder_name)
    return data


def cache_exists(folder_name):
    file_name = create_file_path(folder_name)
    if os.path.isfile(file_name):
        return True
    else:
        return False


def cache_data(data, folder_name):
    json_object = json.dumps(data, indent=4)

    file_name = create_file_path(folder_name)
    if cache_exists(file_name):
        pass
    with open(file_name, "w") as outfile:
        outfile.write(json_object)


def load_cache_data(folder_name):

    file_name = create_file_path(folder_name)

    with open(file_name, 'r') as openfile:
        data = json.load(openfile)
    return data


def create_file_path(folder_name):
    today = datetime.date.today()
    date = today.strftime("%Y-%m-%d")
    file_name = f"{caching_dir}{folder_name}.{date}"

    return file_name


class MainApp(App):

    tube_colours = {
        "Bakerloo": "#B26300",
        "Central": "#DC241F",
        "Circle": "#FFD329",
        "District": "#007D32",
        "Hammersmith & City": "#F4A9BE",
        "Jubilee": "#A1A5A7",
        "Metropolitan": "#9B0058",
        "Northern": "#000000",
        "Piccadilly": "#0019A8",
        "Victoria":  "#0098D8",
        "Waterloo & City": "#93CEBA",
        "Elizabeth": "#9364CC",
    }

    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        tube_status_data = fetch_data(
            folder_name="tube_status", url='https://api.tfl.gov.uk/line/mode/tube/status', get_fresh_data=False)
        for line in tube_status_data:
            box = BoxLayout()
            button = Button(
                text=line["name"],
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                background_color=self.tube_colours[line["name"]]
            )
            button.bind(on_press=self.on_button_press)
            box.add_widget(button)
            main_layout.add_widget(box)

        return main_layout

    def on_button_press(self, instance):
        return 0


if __name__ == "__main__":
    app = MainApp()
    app.run()
