from eppy.modeleditor import IDF
from eppy.idf_helpers import getidfobjectlist


class EnergyPlusHelper:
    """ A class for the EnergyPlus communicator
    """

    def __init__(self,
                 idf_file,
                 idd_file=None,
                 weather_file=None,
                 output_path=None,
                 ):
        """ New instance of the `EnergyPlusHelper` class

        Parameters
        ----------
        idf_file : string
            the file name with extension (.idf) of the input file to simulate. With a relative path if not in the same
            running directory.
        idd_file : string
            the Input data dictionary path (.idd)
        weather_file : string
            the weather file path. (.epw)
        output_path : string
            the directory to output the result files in. Default is the same directory
        Examples
        ----------
        >>> from EPinterface.EPHelper import EnergyPlusHelper
        >>> ep = EnergyPlusHelper(idf_file="D:/F/uniopt/EP/singleZonePurchAir_template.idf",
        >>>                         idd_file="D:/F/uniopt/EP/E+.idd",weather_file="D:/F/uniopt/EP/in.epw")
        """
        self.idf_file = idf_file
        self.idd_file = idd_file
        self.weather_file = weather_file
        self.output_path = output_path

        # IDF.setiddname(idf_file) if self.idf_file else 1
        # TODO : get the path of E+ install as the default .idd is needed.
        IDF.setiddname("D:/F/uniopt/EP/Energy+.idd")
        self.idf = IDF(self.idf_file, self.weather_file) if self.weather_file else IDF(idf_file)

    def get_all_objects(self):
        """ returns all the idf file objects

        Returns
        -------
        Iterable
            list of idf objects

        """
        return getidfobjectlist(self.idf)

    def get_object_fields(self, obj_name):
        """ returns the list of all object fields

        Parameters
        ----------
        obj_name : string
            name of the object to get the fields for

        Returns
        -------
        Iterable
            list of the fields of the object.
            TODO : Handle the return of multiple objects if they have the same name in the UI.
            https://eppy.readthedocs.io/en/latest/Main_Tutorial.html#working-with-e-objects
        """
        objects = self.idf.idfobjects[obj_name]
        fields = []
        for obj in objects:
            for field in obj.fieldnames:
                fields.append({field: getattr(obj, field)})
        return fields

    def get_field_val(self, obj_name, fld_name):
        """ get multiple fields of multiple objects at once

        Parameters
        ----------
        obj_name : list
            list of the objects names
        fld_name : list
            list of fields names

        Returns
        -------
        Iterable
            list of values


        """
        for obj_name, fld_name in zip(obj_name, fld_name):
            fields = []
            for field in obj_name.fieldnames:
                fields.append(getattr(obj_name, field))

        return fields

    def set_field_val(self, obj_name, fld_name, val):
        """ set multiple fields of multiple objects at once

        Parameters
        ----------
        obj_name : list
            list of the objects names
        fld_name : list
            list of fields names
        val : list
            list of values.

        Examples
        ----------
        >>> from EPinterface.EPHelper import EnergyPlusHelper
        >>> ep = EnergyPlusHelper(idf_file="D:/F/uniopt/EP/singleZonePurchAir_template.idf",
        >>>                         idd_file="D:/F/uniopt/EP/E+.idd",weather_file="D:/F/uniopt/EP/in.epw")
        >>> ep.set_field_val(obj_name=['BUILDING','MATERIAL'], fld_name=['North_Axis', 'Thickness'], val=[32.,0.02])

        """
        for obj_name, fld_name, val in zip(obj_name, fld_name, val):
            objects = self.idf.idfobjects[obj_name]
            # Loop to handle multiple objects of the same object
            for obj in objects:
                setattr(obj, fld_name, val)

