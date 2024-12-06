from PIL.Image import Image
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QVBoxLayout
import qrcode
from qrcode.image.pil import PilImage


class QrWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self._qr_label: QLabel = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self._qr_label)
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def set_qr_code(self, url: str) -> None:
        """
        Set the QR code image in label

        Args:
            url: The public URL

        Returns:

        """
        qr_image = self.generate_qr_image(url)
        pixmap = self.convert_to_pixmap(qr_image)
        self.qr_label.setPixmap(pixmap)

    @staticmethod
    def generate_qr_image(url: str) -> PilImage:
        """
        Make the qr image

        Args:
            url: The public url to make qr for

        Returns:
             The qr image
        """
        qr_image = qrcode.make(url)
        return qr_image

    @staticmethod
    def convert_to_pixmap(qr_code_image: PilImage) -> QPixmap:
        """
        Convert the image to a QPixmap for label

        Args:
            qr_code_image: The image to convert

        Returns:
             The QPixmap for label
        """
        qr_code_image: Image = qr_code_image.convert('RGB')
        data: bytes = qr_code_image.tobytes("raw", "RGB")
        width, height = qr_code_image.size
        q_image = QImage(data, width, height, width * 3, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)

    @property
    def qr_label(self) -> QLabel:
        """

        Returns:
             The label to show the qr in
        """
        return self._qr_label


if __name__ == "__main__":
    pass
