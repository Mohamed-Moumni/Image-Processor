import unittest
from ...services.minio_service import MinioService
import os

class TestMinioService(unittest.TestCase):
    # def test_instantiation(self):
    #     with self.assertRaises(ValueError):
    #         minio_service = MinioService()

    def test_create_bucket(self):
        bucket_name = "test-bucket"
        minio_service = MinioService()
        result = minio_service.create_bucket(bucket_name)
        self.assertEqual(result, True)
    

    def test_add_blob_to_bucket(self):
        minio_service = MinioService()
        bucket_name = "test-bucket"
        username = "user1"
        with open("file_test.txt", "w") as blob:
            blob.write("Hello this a file for testing")
        
        with open("file_test.txt", "rb") as f:
            result = minio_service.add_blob_to_bucket(bucket_name, f, username)
            self.assertEqual(result, True)
    
    def test_get_blob_from_bucket(self):
        minio_service = MinioService()
        bucket_name = "test-bucket"
        blob_name = "user1-file_test.txt"

        with open("file_test.txt", "rb") as file:
            result = minio_service.get_blob_from_bucket(bucket_name, blob_name)
            object_data = result.read()
            data = file.read()
            result.close()
            result.release_conn()
            self.assertEqual(object_data, data)
    
    def test_remove_blob_from_bucket(self):
        minio_service = MinioService()
        bucket_name = "test-bucket"
        blob_name = "user1-file_test.txt"
        minio_service.remove_blob_from_bucket(bucket_name, blob_name)
        self.assertEqual(minio_service.blob_exist_in_bucket(bucket_name, blob_name), False)