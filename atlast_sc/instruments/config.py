import importlib, inspect, os
from atlast_sc.utils import FileHelper
from atlast_sc.instrument import Instrument

class InstrumentConfig:
    """
    Class for loading available instrument files for calculator to use.
    """
    def __init__(self):

        path = 'instruments'
        python_package_dir = 'classes'

        default_instrument = {'class': 'Default.py', 'data': 'Default.yaml'}
        chai_instrument = {'class': 'Chai.py', 'data': 'Chai.yaml'}
        finer_instrument = {'class': 'Finer.py', 'data': 'Finer.yaml'}
        gltcam_instrument = {'class': 'GLTCam.py', 'data': 'GLTCam.yaml'}
        muscat_instrument = {'class': 'Muscat.py', 'data': 'Muscat.yaml'}
        sepia_instrument = {'class': 'Sepia.py', 'data': 'Sepia.yaml'}
        tifuun_instrument = {'class': 'Tifuun.py', 'data': 'Tifuun.yaml'}
        # TODO: Add your custom instrument here.
        
        available_instruments = [
            default_instrument,
            chai_instrument,
            finer_instrument,
            gltcam_instrument,
            muscat_instrument,
            sepia_instrument,
            tifuun_instrument
            # TODO: Add your custom instrument here.
        ]

        self._inst_classes = {}

        for details in available_instruments:
            # Load the instrument class and populate it with its relevant details.
            inst_name, inst_class = self.load_instrument_class(path, python_package_dir, details)

            # Add instrument class to the instrument classes dictionary with the instrument
            # name as the key.
            self._inst_classes[inst_name] = inst_class

    @property
    def instrument_classes(self):
        return self._inst_classes

    def load_instrument_class(self, path, python_package_dir, details):
        """
        (ASC-79)
        Loads the relative instrument class and populates the said class.

        :param path: path where instrument information live
        :type path: String
        :param python_package_dir: path where instrument python modules live
        :type python_package_dir: String
        :param details: details of instrument (eg. module name, YAML file name)
        :type details: dict

        :return: tuple of instrument class name and populated instance of instrument
        :rtype: String, atlast_sc.parameters.Instrument.[module_name]
        """
        module_name = os.path.splitext(details["class"])[0]
        
        # If this method is executed in the web client flow, we need to make
        # some changes to the path we supply to the method that will import
        # our instrument classes
        if 'web_client' in os.getcwd().split('/'):
            path = 'atlast_sc' + '.' + path

        module = importlib.import_module(path + '.' + python_package_dir + '.' + module_name)
        
        for name, cls in inspect.getmembers(module, inspect.isclass):
            # This will return all classes belonging to the module. We are
            # only interested in each child 'Instruments' class.
            if inspect.isclass(cls) and issubclass(cls, Instrument) and cls.__name__ != 'Instrument':
                inst_class_name = name 
                inst_class = self.populate_instrument_class(cls, name)

        return inst_class_name, inst_class
    
    def populate_instrument_class(self, inst_class_instance, module_name):
        """
        (ASC-79)
        Populates the instrument class with given name.

        :param inst_class_instance: instance of instrument
        :type inst_class_instance: String
        :param module_name: name of instrument module
        :type module_name: String

        :return: populated instance of instrument class
        :rtype: atlast_sc.parameters.Instrument.[module_name]
        """

        inst_data = FileHelper.read_instrument_file(module_name)
        inst_class = inst_class_instance(data=inst_data)

        return inst_class