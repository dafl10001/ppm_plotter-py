from typing import Callable
import time
import utils

class Renderer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.minBound = 0
        self.maxBound = 10
        self.step = 1

        self.frame = bytearray([0] * (width * height))

    def writeImage(self, path: str):
        header = f"P5\n{self.width} {self.height}\n255\n".encode("ascii")
        
        with open(path, "wb") as f:
            f.write(header)
            f.write(self.frame)

    def _drawLine(self, x0: int, y0: int, x1: int, y1: int, brightness: int = 255):
        """Standard Bresenham's Line Algorithm."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy

        while True:
            if 0 <= x0 < self.width and 0 <= y0 < self.height:
                self.frame[y0 * self.width + x0] = brightness
            
            if x0 == x1 and y0 == y1:
                break
                
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def renderFunction(self, func: Callable[[float], float]):
        i = self.minBound + 1

        scale = 1 / self.step

        prev = round(self.minBound * scale), round(self.height - func(self.minBound) * scale)

        while i < self.maxBound:
            px, py = prev
            curr = round(i * scale), round(self.height - func(i) * scale)
            cx, cy = curr
            self._drawLine(px, py, cx, cy)
            
            prev = curr

            i += self.step
    
    def renderShaderFunction(self, func: Callable[[float, float, float, float], float]):
        print()
        first = time.time()
        for y in range(self.height):
            for x in range(self.width):
                val = func(x, y, self.width, self.height)
                clampedVal = max(0, min(255, int(val)))
                self.frame[y * self.width + x] = clampedVal

                total_pixels = self.width * self.height

                frame = y * self.width + x + 1

                now = time.time()
                time_elapsed = now - first

                if time_elapsed > 0:
                    pps = frame / time_elapsed
                    pixels_remaining = total_pixels - frame
                    time_left = round(pixels_remaining / pps)
                else:
                    time_left = 0

                if frame % 1000 == 0 or frame == total_pixels:
                    print(f"\x1b[A{frame} / {total_pixels} [{'#' * (frame * 50 // total_pixels)}{'-' * (50 - frame * 50 // total_pixels)}] (ETA T-{utils.seconds_to_time(time_left * 1000)})    ")
        
        print(f"Rendering took {utils.seconds_to_time((now - first) * 1000, show_ms=True)}")