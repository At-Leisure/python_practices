from pathlib import Path
_img_root = Path('./assets/flappy_bird')



class _ResourcePath:
    def __init__(self) -> None:
        self.img = {
            'sky': _img_root/'sky.png',
            'pause': _img_root/'pause.png',
            'pipe': _img_root/'pipe.png',
            'blue_bird-1': _img_root/'blue_bird-1.png',
            'blue_bird-2': _img_root/'blue_bird-2.png',
            'blue_bird-3': _img_root/'blue_bird-3.png',
            'score': tuple(_img_root/f'score/{i}.png' for i in range(10))
        }
        #self._check()

    def _check(self, name, path: Path | str):
        """ 检查资源文件是否存在 """
        if isinstance(path, Path | str):
            if not Path(path).is_file():
                raise FileNotFoundError(name, path)
        elif isinstance(path, tuple | list):
            for i in range(len(path)):
                self._check(i, path[i])


resource = _ResourcePath()