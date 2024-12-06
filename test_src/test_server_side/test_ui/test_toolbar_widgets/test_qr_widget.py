from unittest.mock import patch
import pytest
import qrcode
from PIL.Image import Image
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel
from pytestqt.qtbot import QtBot

from src.server_side.ui.toolbar_widgets.qr_widget import QrWidget


@pytest.fixture
def qr_fix(qtbot: QtBot) -> QrWidget:
    qr_widget = QrWidget()
    qtbot.addWidget(qr_widget)
    return qr_widget


class TestQrWidget:

    def test_set_qr_code(self, qr_fix: QrWidget) -> None:
        """

        """
        with patch.object(qr_fix, 'generate_qr_image') as patch_image:
            with patch.object(qr_fix, 'convert_to_pixmap') as patch_convert:
                with patch.object(qr_fix.qr_label, 'setPixmap') as patch_set:
                    patch_image.return_value = 'PilImage'
                    patch_convert.return_value = QPixmap()
                    qr_fix.set_qr_code('python.org')
                    patch_convert.assert_called_once_with(patch_image.return_value)
                    patch_set.assert_called_once_with(patch_convert.return_value)

    def test_generate_qr_image(self, qr_fix: QrWidget) -> None:
        """

        """
        with patch('qrcode.make') as patch_make:
            patch_make.return_value = 'PilImage'
            image = qr_fix.generate_qr_image('python.org')
            patch_make.assert_called_once_with('python.org')
            assert image is patch_make.return_value

    def test_convert_to_pixmap(self, qr_fix: QrWidget) -> None:
        """

        """
        test_image = qrcode.make('python.org')
        with patch('PIL.Image.Image.convert') as patch_convert:
            with patch('PIL.Image.Image.tobytes') as patch_to_bytes:
                with patch('PyQt5.QtGui.QImage.__new__') as patch_q:
                    with patch('PyQt5.QtGui.QPixmap.fromImage') as patch_from:
                        patch_convert.return_value = Image()
                        patch_to_bytes.return_value = b'patch_to_bytes_return'
                        patch_q.return_value = QImage()
                        patch_from.return_value = QPixmap()
                        pixmap = qr_fix.convert_to_pixmap(test_image)
                        patch_convert.assert_called_once()
                        patch_to_bytes.assert_called_once()
                        patch_q.assert_called()
                        patch_from.assert_any_call(patch_q.return_value)
                        assert pixmap is patch_from.return_value

    def test_qr_label_getter(self, qr_fix: QrWidget) -> None:
        """

        """
        assert qr_fix._qr_label is qr_fix.qr_label
        assert isinstance(qr_fix.qr_label, QLabel)


if __name__ == "__main__":
    pass
