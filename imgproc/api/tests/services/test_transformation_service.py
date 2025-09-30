import unittest
from ...services.transformation_service import TransformationService

class TestTransformationService(unittest.TestCase):
    def test_crop_transformation_service(self):
        trans_serv = TransformationService()
        transformation = {
            "x": 20,
            "y": 20,
            "width": 100,
            "height": 100
        }
        