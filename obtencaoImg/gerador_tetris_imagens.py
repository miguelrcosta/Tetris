
import pygame
import random
import os

pygame.init()

block_size = 30
cols = 10
rows = 20
width = cols * block_size
height = rows * block_size

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 0, 255),
    (128, 0, 128)
]

shapes = {
    1: [[1, 1, 0], [0, 1, 1]],
    2: [[0, 2, 2], [2, 2, 0]],
    3: [[3, 3, 3, 3]],
    4: [[4, 4], [4, 4]],
    5: [[0, 0, 5], [5, 5, 5]],
    6: [[6, 0, 0], [6, 6, 6]],
    7: [[0, 7, 0], [7, 7, 7]]
}

def draw_shape(grid, shape, x, y, shape_id):
    for row_idx, row in enumerate(shape):
        for col_idx, val in enumerate(row):
            if val:
                if 0 <= y + row_idx < rows and 0 <= x + col_idx < cols:
                    grid[y + row_idx][x + col_idx] = shape_id

output_dir = "tetris_scenes"
os.makedirs(output_dir, exist_ok=True)

num_images = 100
for img_id in range(num_images):
    screen = pygame.Surface((width, height))
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for y in range(rows - 5, rows):
        for x in range(cols):
            if random.random() < 0.3:
                grid[y][x] = random.randint(1, 7)

    shape_id = random.randint(1, 7)
    shape = shapes[shape_id]
    x_pos = random.randint(0, cols - len(shape[0]))
    y_pos = random.randint(0, 5)
    draw_shape(grid, shape, x_pos, y_pos, shape_id)

    for y in range(rows):
        for x in range(cols):
            color = colors[grid[y][x]]
            pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size))
            pygame.draw.rect(screen, (50, 50, 50), (x * block_size, y * block_size, block_size, block_size), 1)

    pygame.image.save(screen, os.path.join(output_dir, f"scene_{img_id:03}.png"))

pygame.quit()
