import json


def read_config_app():
    with open("config.json", "r") as data_file:
        json_data = json.load(data_file)

    return json_data


def write_config_app(width, height, font_family, font_size):
    json_data = {
            "text": {
                "font_family": font_family,
                "font_size": font_size
            },
            "window": {
                "height": height+20,
                "width": width
            }
    }

    with open("config.json", "w") as outfile:
        json.dump(json_data, outfile, sort_keys=True, indent=4)

    # with open('editor.conf', 'w') as f:
    #     f.write(f"WIDTH={width}\nHEIGHT={height+21}")

#
# with open("config.json", "w") as outfile:
#     json.dump(data, outfile, sort_keys=True, indent=4)
#
# with open("config.json", "r") as json_data_file:
#     data = json.load(json_data_file)