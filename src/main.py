import renderer as r
import os

def mandelbrot_shader(x, y, width, height):
    # Map pixel (x, y) to complex plane (cx, cy)
    # This centers the set and zooms out to fit it
    cx = (x / width) * 3.5 - 2.5  # Scales based on current width
    cy = (y / height) * 2.0 - 1.0  # Scales based on current height
    
    zx, zy = 0.0, 0.0
    max_iter = 100
    
    for i in range(max_iter):
        # z = z^2 + c
        # (zx + zy*i)^2 = zx^2 - zy^2 + 2*zx*zy*i
        new_zx = zx*zx - zy*zy + cx
        new_zy = 2*zx*zy + cy
        zx, zy = new_zx, new_zy
        
        # Check if magnitude squared |z|^2 > 4 (escaped)
        if zx*zx + zy*zy > 4:
            return int((i / max_iter) * 255)
            
    return 0 # Point is inside the set

def sierpinski_shader(x, y, w, h):
    ry = h - y 
    
    h_ratio = 0.866
    base_w = h / h_ratio
    
    side_padding = (w - base_w) / 2
    
    size = 1024
    
    ny = ry * (size / h)
    
    scale = size / h
    tx = int((x - side_padding) * scale - (ny * 0.5))
    ty = int(ny)

    if 0 <= tx < size and 0 <= ty < size:
        if (tx & ty) == 0:
            return 255
            
    return 0

if __name__ == "__main__":
    renderer = r.Renderer(3840, 2160)

    renderer.maxBound = 10
    renderer.minBound = 0
    renderer.step = 0.1

    renderer.renderShaderFunction(mandelbrot_shader)
    renderer.writeImage("test.ppm")

    os.system("convert test.ppm result.png")