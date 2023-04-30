"""Functions to manipulate panel.cfg"""
import configparser
from pathlib import Path
from .cfg_tools import get_section, get_section_with_info, get_next_section_number

def create_empty(file_name):
    """Creates almost empty panel.cfg with [VARIATION] section.
    """
    Path(file_name).write_text("""[VARIATION]
override_base_container = 0
""")

def copy_original(output_file:str, input_file:str, variation:bool=True):
    """Copies a panel.cfg file. Includes a [VARIATION] section by default.

    Args:
        output_file (str): destination file path.
        input_file (str): original file path.
        variation (bool, optional): whether to include [VARIATION] section
            with "override_base_container = 0". Defaults to True.
    """
    panel = configparser.ConfigParser(comment_prefixes=(';', '//'))
    panel.read(input_file)
    if variation:
        var_section = get_section('VARIATION', panel)
        var_section['override_base_container'] = '0'
    output = Path(output_file).open('w', encoding='utf8')
    panel.write(output)
    output.close()

def set_registration_colors(file_name:str, font:str='black', stroke:str='',
                            stroke_size:int=30):
    """Sets font and stroke color at external registration marks.

    Args:
        file_name (str): panel.cfg file path.
        font (str, optional): font color. Defaults to 'black'.
        stroke (str, optional): stroke color. Defaults to no stroke ('').
        stroke_size (int, optional): stroke size. Defaults to 30.
    """
    if not font:
        raise ValueError('Font color must not be void.')
    panel:configparser.ConfigParser = configparser.ConfigParser(comment_prefixes=(';', '//'))
    panel.read(file_name)
    try:
        registration = get_section_with_info('VPainting', panel,
                                        value_contains={'texture': 'registration'},
                                        value_equal={'location': 'exterior'})
    except ValueError:
        number = get_next_section_number('VPainting', panel)
        panel.add_section(f'VPainting{number:02x}')
        registration = panel[f'VPainting{number:02x}']
    registration['painting00'] = f'Registration/Registration.html?font_color={font}\
{"&stroke_size=" + str(stroke_size) if stroke else ""}{"&stroke_color=" if stroke else ""}\
{stroke}, 0, 0, {registration["size_mm"]}'
    file = Path(file_name).open('w', encoding='utf8')
    panel.write(file)
    file.close()
