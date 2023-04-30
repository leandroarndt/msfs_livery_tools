import unittest, shutil
from pathlib import Path
from . import Project

path = 'teste/test_project'
parser_key = Path(path, 'livery.ini').as_posix()

class ProjectTestCase(unittest.TestCase):
    def test_0_creation(self):
        if Path(path).is_dir():
            shutil.rmtree(path)
        p = Project(path)
        self.assertTrue(Path(path, 'livery.ini').is_file(), '"livery.ini" has not been created!')
        self.assertTrue(Path(path, 'model').is_dir(), 'Model directory has not been created!')
        self.assertTrue(Path(path, 'panel').is_dir(), 'Panel directory has not been created!')
        self.assertTrue(Path(path, 'sound').is_dir(), 'Sound directory has not been created!')
        self.assertFalse(Path(path, 'texture').is_dir(),
            f'Texture directory has been created while join_model_and_textures == {p.join_model_and_textures}!')
    
    def test_1_creation_with_texture_dir(self):
        path_texture = '_'.join((path, 'texture'))
        if Path(path_texture).is_dir():
            shutil.rmtree(path_texture)
        p = Project(path_texture, join_model_and_textures=False)
        self.assertTrue(Path(path_texture, 'livery.ini').is_file(), '"livery.ini" has not been created!')
        self.assertTrue(Path(path_texture, 'model').is_dir(), 'Model directory has not been created!')
        self.assertTrue(Path(path_texture, 'panel').is_dir(), 'Panel directory has not been created!')
        self.assertTrue(Path(path_texture, 'sound').is_dir(), 'Sound directory has not been created!')
        self.assertTrue(Path(path_texture, 'texture').is_dir(),
            f'Texture directory has not been created while join_model_and_textures == {p.join_model_and_textures}!')
    
    def test_2_ini_structure(self):
        p = Project(path)
        for section in ('PROJECT', 'AIRCRAFT', 'PANEL', 'TEXTURES'):
            self.assertIn(section, p._parsers[parser_key].sections())
    
    def test_instance_sharing(self):
        p1 = Project(path)
        p1.airplane_folder = 'TEST_PLANE'
        p2 = Project(path)
        self.assertEqual(p1.airplane_folder, p2.airplane_folder)
        p2.airplane_folder = 'PLANE_TEST'
        self.assertEqual(p2.airplane_folder, p1.airplane_folder)
    
    def test_origin(self):
        p = Project(path)
        p.origin = Path(path, 'aircraft_origin')
        self.assertEqual(p.origin, str(Path(path, 'aircraft_origin')))
        self.assertEqual(p.base_container, f'..\{Path(path, "aircraft_origin").name}')
        self.assertEqual(p.origin, Project._parsers[parser_key]['PROJECT']['origin'])
        self.assertEqual(p.base_container, Project._parsers[parser_key]['AIRCRAFT']['base_container'])
    
    def test_base_container(self):
        """Tests if base_container is read only."""
        p = Project(path)
        p.origin = Path(path, 'aircraft_origin')
        with self.assertRaises(AttributeError):
            p.base_container = 'abc'
        self.assertEqual(p.base_container, r'..\aircraft_origin')
        self.assertEqual(p.base_container, Project._parsers[parser_key]['AIRCRAFT']['base_container'])
    
    def test_title(self):
        p = Project(path)
        p.title = 'Project Title'
        self.assertEqual(p.title, 'Project Title')
        self.assertEqual(p.title, Project._parsers[parser_key]['PROJECT']['title'])
    
    def test_airplane_folder(self):
        p = Project(path)
        p.airplane_folder = 'AIRPLANE_Folder'
        self.assertEqual(p.airplane_folder, 'AIRPLANE_Folder')
        self.assertEqual(p.airplane_folder, Project._parsers[parser_key]['PROJECT']['airplane_folder'])
    
    def test_manufacturer(self):
        p = Project(path)
        p.manufacturer = 'Manufacturer'
        self.assertEqual(p.manufacturer, 'Manufacturer')
        self.assertEqual(p.manufacturer, Project._parsers[parser_key]['PROJECT']['manufacturer'])
    
    def test_creator(self):
        p = Project(path)
        p.creator = 'fswt'
        self.assertEqual(p.creator, 'fswt')
        self.assertEqual(p.creator, Project._parsers[parser_key]['PROJECT']['creator'])
    
    def test_version(self):
        p = Project(path)
        p.version = '1.2.3'
        self.assertEqual(p.version, '1.2.3')
        self.assertEqual(p.version, Project._parsers[parser_key]['PROJECT']['version'])
    
    def test_minimum_game_version(self):
        p = Project(path)
        p.minimum_game_version = '1.2.3'
        self.assertEqual(p.minimum_game_version, '1.2.3')
        self.assertEqual(p.minimum_game_version, Project._parsers[parser_key]['PROJECT']['minimum_game_version'])
    
    def test_suffix(self):
        p = Project(path)
        p.suffix = 'fswt'
        self.assertEqual(p.suffix, 'fswt')
        self.assertEqual(p.suffix, Project._parsers[parser_key]['AIRCRAFT']['suffix'])
    
    def test_tail_number(self):
        p = Project(path)
        p.tail_number = 'YT-FSWT'
        self.assertEqual(p.tail_number, 'YT-FSWT')
        self.assertEqual(p.tail_number, Project._parsers[parser_key]['AIRCRAFT']['tail_number'])
    
    def test_model(self):
        p = Project(path)
        p.include_model = True
        self.assertEqual(p.include_model, True)
        self.assertEqual(str(p.include_model), Project._parsers[parser_key]['AIRCRAFT']['model'])
    
    def test_panel(self):
        p = Project(path)
        p.include_panel = True
        self.assertEqual(p.include_panel, True)
        self.assertEqual(str(p.include_panel), Project._parsers[parser_key]['AIRCRAFT']['panel'])
    
    def test_sound(self):
        p = Project(path)
        p.include_sound = True
        self.assertEqual(p.include_sound, True)
        self.assertEqual(str(p.include_sound), Project._parsers[parser_key]['AIRCRAFT']['sound'])
    
    def test_texture(self):
        p = Project(path)
        p.include_texture = True
        self.assertEqual(p.include_texture, True)
        self.assertEqual(str(p.include_texture), Project._parsers[parser_key]['AIRCRAFT']['texture'])
    
    def test_registration_font_color(self):
        p = Project(path)
        p.registration_font_color = 'black'
        self.assertEqual(p.registration_font_color, 'black')
        self.assertEqual(p.registration_font_color, Project._parsers[parser_key]['PANEL']['font_color'])
    
    def test_registration_stroke_color(self):
        p = Project(path)
        p.registration_stroke_color = 'black'
        self.assertEqual(p.registration_stroke_color, 'black')
        self.assertEqual(p.registration_stroke_color, Project._parsers[parser_key]['PANEL']['stroke_color'])
    
    def test_registration_stroke_size(self):
        p = Project(path)
        p.registration_stroke_size = 20
        self.assertEqual(p.registration_stroke_size, 20)
        self.assertEqual(str(p.registration_stroke_size), Project._parsers[parser_key]['PANEL']['stroke_size'])
    
    def test_z_save(self):
        Project(path).save()
        del Project._parsers[parser_key]
        p = Project(path)
        keys = {
            'PROJECT': (
                'join_model_and_textures',
                'origin',
                'title',
                'airplane_folder',
                'manufacturer',
                'creator',
                'version',
                'minimum_game_version',
            ),
            'AIRCRAFT': (
                'base_container',
                'suffix',
                'tail_number',
                'model',
                'panel',
                'sound',
                'texture',
            ),
            'PANEL': (
                'font_color',
                'stroke_color',
                'stroke_size',
            ),
            'TEXTURES': (),
        }
        for section, settings in keys.items():
            for setting in settings:
                self.assertIn(setting, Project._parsers[parser_key][section])
