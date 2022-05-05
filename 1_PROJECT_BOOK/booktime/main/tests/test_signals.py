from django.test import TestCase
from main import models
from django.core.files.images import ImageFile
from decimal import Decimal


class TestSignal(TestCase):
    def test_thumbnails_are_generated_on_save(self):
        product = models.Product(name="The bible", price=Decimal("10.00"),)
        product.save()
        with open("main/fixtures/biblia.jpg") as f:
            image = models.ProductImage(product=product, image=ImageFile(f, name="tctb.jpg"), )
            with self.assertLogs("main", level="INFO") as cm:
                image.save()
            self.assertGreaterEqual(len(cm.output), 1)
            image.refresh_from_db()

            with open("main/fixtures/biblia.jpg", "rb",) as f:
                expended_content = f.read()
                assert image.image.delete(save=False)