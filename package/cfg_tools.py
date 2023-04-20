"""Functions to manipulate generic .cfg files."""
import configparser, re

def get_section(section:str, config:configparser.ConfigParser,
                create:bool=True)->configparser.SectionProxy:
    """Get or create section on config file, case insensitve.
    
    Args:
        section (str): config section name (case insensitive)
        config (configparser.ConfigParser): configuration object
        create (bool, optional): create section if it does not exist. Defaults to True.

    Raises:
        ValueError: section not found and _create_ is False.

    Returns:
        configparser.SectionProxy: existing or new config section.
    """
    for s in config.sections():
        if s.upper() == section.upper():
            return config[s]
    
    # Create section if it doesn't exist
    if create:
        config.add_section(section)
        return config[section]
    raise ValueError(f'Section {section} does not exist.')

def get_section_with_info(section_type:str, config:configparser.ConfigParser,
                            value_contains:dict={}, value_equal:dict={})->configparser.SectionProxy:
    """Gets a config section of type "section_type" with the given setting-value pair.
    Does not create a new section.

    Args:
        section_type (str): section base name ("VPainting" for "VPainting01",
            "VPainting02", "fltsim" for "FLTSIM.0", FLTSIM.1" etc.).
        config (configparser.ConfigParser): configuration object.
        value_contains (dict, optional): optional dictionary containing setting-value pairs
            where the value is a string expected to be contained in the configuration value
            (eg: "registration" will match "$Registration", "$RegistrationNumber" etc.)
        value_equal (dict, optional): similar to "value_contains", but requires exact
            (case insensitive) value match (eg: "$registration" will match "$Registration" or
            "$REGISTRATION").
        
    Raises:
        ValueError: section not found and _create_ is False.

    Returns:
        configparser.SectionProxy: first found section matching arguments.
    """
    re_section = re.compile(f'^{section_type}[\\d\\.]\\d$', re.IGNORECASE)
    for section in config.sections():
        if re_section.match(section):
            matches = True
            for item, value in value_contains.items():
                try:
                    if value.upper() not in config[section][item].upper():
                        matches = False
                        break
                except KeyError:
                    matches = False
                    break
            
            for item, value in value_equal.items():
                try:
                    if value.upper().strip('"') != config[section][item].upper().strip('"'):
                        matches = False
                        break
                except KeyError:
                    matches = False
                    break
            
            if matches:
                return config[section]
    
    raise ValueError('No matching section.')
