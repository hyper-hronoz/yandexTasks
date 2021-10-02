import sys
import os
from typing import MappingView
from PyQt5 import QtGui, QtWidgets
from view.MainView import MainView, PopUpError
from PIL import Image
from res.dist.img import resources
from PIL.ImageQt import ImageQt


class ImageFile:
    PIL_IMAGE = None

    def __init__(self, context) -> None:
        self.context = context

    def getMutableImage(self, callback=lambda x: x):
        filePath = self._getFile()
        return Image.open(callback(filePath))

    def setMutableImage(self, image, callback=lambda: None):
        pixmap = self._pil2pixmap(image)
        self._setImagePixmap(pixmap)
        callback()

    def _pil2pixmap(self, image):
        if image.mode == "RGB":
            r, g, b = image.split()
            image = Image.merge("RGB", (b, g, r))
        elif image.mode == "RGBA":
            r, g, b, a = image.split()
            image = Image.merge("RGBA", (b, g, r, a))
        elif image.mode == "L":
            image = image.convert("RGBA")
        im2 = image.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qim = QtGui.QImage(
            data, image.size[0], image.size[1], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(qim)
        return pixmap

    def _getFile(self):
        return QtWidgets.QFileDialog.getOpenFileName(self.context._view, 'Выбрать картинку', '', 'Картинка (*.jpg);;Картинка (*.jpg);;Все файлы (*)')[0]

    def _setImagePixmap(self, pixmap):
        self.context._view.setImage(pixmap)


class MainController:
    def __init__(self) -> None:
        self._app = QtWidgets.QApplication(sys.argv)
        self._view = MainView()
        self.imageFile = ImageFile(self)

    def _checkIfPathEmpty(self, path: str):
        if (path.strip() == ""):
            path = os.path.abspath(
                "./res/src/img/Darth_Maul_Cosplayer_at_MCM_Comic_Con_October_2016.jpg")
        return path

    def _init(self):
        self.mutableImage = self.imageFile.getMutableImage(
            self._checkIfPathEmpty)

        self.imageCopy = self.mutableImage.copy()

        self.imageFile.setMutableImage(self.mutableImage)

        self._initInstance()

        self._initMethods()

    def _setMutableImage(self, image):
        self.mutableImage = image 

    def _initInstance(self):
        self.redImageChanger = ImageChangerRed(self.mutableImage)
        self.blueImageChanger = ImageChangerBlue(self.mutableImage)
        self.greenImageChanger = ImageChangerGreen(self.mutableImage)
        self.defaultImageChanger = ImageChangerDefault(self.mutableImage, self.imageCopy)
        self.counterWiseClockChanger = ImageChangerCounterClockWiseRotation(
            self.mutableImage)
        self.wiseClockChanger = ImageChangerClockWiseRotation(
            self.mutableImage)
        self.imageChangerCurrentAngel = ImageChangerSetCurrentAngle(self.mutableImage)

    def _initMethods(self):

        self._view.window.redColorButton.clicked.connect(lambda: self.defaultImageChanger.change())
        self._view.window.redColorButton.clicked.connect(lambda: self.redImageChanger.change())
        self._view.window.redColorButton.clicked.connect(lambda: self.imageChangerCurrentAngel.change(lambda image: self.imageFile.setMutableImage(image)))

        self._view.window.blueColorButton.clicked.connect(lambda: self.defaultImageChanger.change())
        self._view.window.blueColorButton.clicked.connect(lambda: self.blueImageChanger.change())
        self._view.window.blueColorButton.clicked.connect(lambda: self.imageChangerCurrentAngel.change(lambda image: self.imageFile.setMutableImage(image)))
 
        self._view.window.greenColorButton.clicked.connect(lambda: self.defaultImageChanger.change())
        self._view.window.greenColorButton.clicked.connect(lambda: self.greenImageChanger.change())
        self._view.window.greenColorButton.clicked.connect(lambda: self.imageChangerCurrentAngel.change(lambda image: self.imageFile.setMutableImage(image)))

        self._view.window.allColorButton.clicked.connect(lambda: self.defaultImageChanger.change(lambda: self.imageFile.setMutableImage(self.mutableImage)))
        self._view.window.allColorButton.clicked.connect(lambda: AngelHolder.setAngle(0))

        self._view.window.counterClockwise.clicked.connect(lambda: self.counterWiseClockChanger.change(lambda x: self.imageFile.setMutableImage(x)))
        self._view.window.clockWise.clicked.connect(lambda: self.wiseClockChanger.change(lambda x: self.imageFile.setMutableImage(x)))

    def run(self):
        self._view.show()
        self._init()
        return self._app.exec_()


class ImageChanger:
    def __init__(self, image) -> None:
        self.image = image
        self.image_data = image.load()
        self.height, self.width = image.size
        pass

    def change(self, callback=lambda: None):
        print("Вы не можетевызвать меня так как я говногодер")
        raise Exception("Разаботчик долбоящер!")


class ImageChangerRed(ImageChanger):
    def __init__(self, image) -> None:
        super().__init__(image)

    def change(self, callback=lambda: None):
        print("На красное меняем...")
        for i in range(self.height):
            for j in range(self.width):
                r, g, b = self.image_data[i, j]
                self.image_data[i, j] = r, g // 2, b // 2
        return callback()


class ImageChangerBlue(ImageChanger):

    def __init__(self, image) -> None:
        super().__init__(image)

    def doNothing(self):
        pass

    def change(self, callback=lambda: None):
        print("На голубое меняем...")
        for i in range(self.height):
            for j in range(self.width):
                r, g, b = self.image_data[i, j]
                self.image_data[i, j] = r // 2, g // 2, b
        return callback()


class ImageChangerGreen(ImageChanger):
    def __init__(self, image) -> None:
        super().__init__(image)

    def change(self, callback=lambda: None):
        print("На зеленое меняем...")
        for i in range(self.height):
            for j in range(self.width):
                r, g, b = self.image_data[i, j]
                self.image_data[i, j] = r // 2, g, b // 2
        return callback()


class ImageChangerDefault(ImageChanger):
    def __init__(self, image, imageCopy) -> None:
        super().__init__(image)
        self.imageCopy = imageCopy.load()

    def change(self, callback=lambda: None):
        print("Восстанавливаем")
        for i in range(self.height):
            for j in range(self.width):
                self.image_data[i, j] = self.imageCopy[i, j]
        return callback()


class AngelHolder:
    angel = 0

    @staticmethod
    def setAngle(angle):
        AngelHolder.angel = angle


class ImageChangerClockWiseRotation(ImageChanger):
    def __init__(self, image) -> None:
        super().__init__(image)

    def change(self, callback=lambda: None):
        print("Вращаем по часовой")
        AngelHolder.angel += -90
        return callback(self.image.rotate(AngelHolder.angel))


class ImageChangerCounterClockWiseRotation(ImageChanger):
    def __init__(self, image) -> None:
        super().__init__(image)

    def change(self, callback=lambda: None):
        print("Вращаем против часовой")
        AngelHolder.angel += 90
        return callback(self.image.rotate(AngelHolder.angel))

class ImageChangerSetCurrentAngle(ImageChanger):
    def __init__(self, image) -> None:
        super().__init__(image)

    def change(self, callback=lambda : None):
        print("Устнавливаем тукущий угол")
        return callback(self.image.rotate(AngelHolder.angel))