from PIL import Image
import os

"""
TODO:
- create import method
- create save method
- creat transform method
"""

class Clean_images:
    """
    Cleans the images within the folder to support TensorFlow image types

    Note
    ----
    Currently supports JPG and PNG conversion and cleaning only


    Attributes
    ---------
    path : str
        Absolute path to folder containing the images
    file_type : str, default: jpg
        The output type of all image types
    file : str
        The current file being worked on
    """
    
    def __init__(self, path: str, file_type: str = 'jpg'):
        """
        Parameters
        ----------
        path : str
            Absolute path to folder containing the images
        file_type : str, default: jpg
            The output type of all image types
        """

        __permitted_types = {'png', 'jpg'}

        if os.path.isdir(path):
            self.path = path
        else: 
            raise FileNotFoundError("'Path' is not a valid directory")
        
        if file_type in __permitted_types:
            self.file_type = file_type
        else:
            raise NotImplementedError(f"Methods to support {file_type} have not been implemented")
        
    def __change_type(self, iamge):
        pass