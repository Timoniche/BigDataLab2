import os
import pathlib
import sys

src_module_path = os.path.join(os.getcwd(), "src")
sys.path.insert(1, src_module_path)

from logger import Logger  # noqa: E402
from server import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


class FunctionalApiTest:

    def __init__(
            self,
            client: TestClient,
    ) -> None:
        logger = Logger(show=True)
        self.log = logger.get_logger(__name__)
        self.client = client

    def test_upload_photo(self):
        images_dir = str(pathlib.Path(__file__).resolve().parent.parent.parent)
        print(images_dir)
        img_path = images_dir + '/client_images/' + '000002.jpg'

        files = {
            'file': open(img_path, 'rb')
        }
        response = self.client.post(
            url='http://localhost:8000/upload/',
            files=files,
        )

        json = response.content.decode()

        assert response.status_code == 200
        self.log.info(f'Response json: {json}')
        ground_truth = '{"filename":"000002.jpg","is_male":"female"}'

        assert json == ground_truth, f'Expected {ground_truth}, got {json}'

        self.log.info('Test passed')


if __name__ == '__main__':
    mock_client = TestClient(app)
    api_test = FunctionalApiTest(mock_client)

    api_test.test_upload_photo()
