import sys
import numpy as np
import pygame

# ==============================================================================
# KONFIGURASI KANVAS PYGAME
# ==============================================================================
WIDTH, HEIGHT = 800, 600
FPS = 60

# Warna (RGB)
COLOR_BG = (20, 24, 33)
COLOR_GRID = (35, 42, 58)
COLOR_PLANE_FILL = (41, 128, 185)
COLOR_PLANE_OUTLINE = (52, 152, 219)
COLOR_NOSE = (231, 76, 60)
COLOR_TEXT = (236, 240, 241)
COLOR_HUD_BG = (30, 36, 48)

# ==============================================================================
# REPRESENTASI OBJEK PESAWAT 2D (LOKAL ORIGIN (0,0))
# ==============================================================================
# Model pesawat 2D terdiri dari 10 vertex yang terdefinisi pada origin lokal.
# Menggunakan koordinat homogen,
ORIGINAL_VERTICES = np.array([
    [0.0, -50.0, 1.0],   # 0: Hidung pesawat (Nose)
    [15.0, -10.0, 1.0],  # 1: Sayap kanan atas
    [40.0, 10.0, 1.0],   # 2: Ujung sayap kanan
    [8.0, 10.0, 1.0],    # 3: Badan kanan bawah
    [20.0, 45.0, 1.0],   # 4: Ekor kanan
    [0.0, 35.0, 1.0],    # 5: Ekor tengah
    [-20.0, 45.0, 1.0],  # 6: Ekor kiri
    [-8.0, 10.0, 1.0],   # 7: Badan kiri bawah
    [-40.0, 10.0, 1.0],  # 8: Ujung sayap kiri
    [-15.0, -10.0, 1.0]  # 9: Sayap kiri atas
])

# ==============================================================================
# FUNGSI MATRIKS TRANSFORMASI GEOMETRI 2D (NUMPY 3x3)
# ==============================================================================
def create_translation_matrix(tx, ty):
    """Membuat matriks translasi homogen 3x3."""
    return np.array([
        [1.0, 0.0,  tx],
        [0.0, 1.0,  ty],
        [0.0, 0.0, 1.0]
    ])

def create_rotation_matrix(angle_degrees):
    """Membuat matriks rotasi homogen 3x3 terhadap titik origin (0,0)."""
    rad = np.radians(angle_degrees)
    cos_theta = np.cos(rad)
    sin_theta = np.sin(rad)
    return np.array([
        [cos_theta, -sin_theta, 0.0],
        [sin_theta,  cos_theta, 0.0],
        [0.0,        0.0,       1.0]
    ])

def create_scaling_matrix(sx, sy):
    """Membuat matriks penskalaan (scaling) homogen 3x3."""
    return np.array([
        [ sx, 0.0, 0.0],
        [0.0,  sy, 0.0],
        [0.0, 0.0, 1.0]
    ])

# ==============================================================================
# FUNGSI PENDUKUNG RENDERING & HUD
# ==============================================================================
def draw_grid(surface):
    """Menggambar grid latar belakang kanvas."""
    surface.fill(COLOR_BG)
    grid_size = 40
    for x in range(0, WIDTH, grid_size):
        pygame.draw.line(surface, COLOR_GRID, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, grid_size):
        pygame.draw.line(surface, COLOR_GRID, (0, y), (WIDTH, y), 1)

def draw_hud(surface, font, pos_x, pos_y, angle, scale):
    """Menampilkan informasi kontrol dan status variabel pada layar."""
    hud_rect = pygame.Rect(10, 10, 260, 150)
    pygame.draw.rect(surface, COLOR_HUD_BG, hud_rect, border_radius=8)
    pygame.draw.rect(surface, COLOR_PLANE_OUTLINE, hud_rect, 2, border_radius=8)

    lines = [
        "--- KONTROL TRANSFORMASI ---",
        "Arrow Keys : Move (Translasi)",
        "A / D      : Rotate (Rotasi)",
        "+ / -      : Scale (Ukuran)",
        "R          : Reset State",
        f"Posisi (X, Y) : ({int(pos_x)}, {int(pos_y)})",
        f"Rotasi        : {int(angle % 360)}°",
        f"Skala         : {scale:.2f}x"
    ]

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, COLOR_TEXT)
        surface.blit(text_surface, (20, 18 + i * 16))

# ==============================================================================
# PROGRAM UTAMA (MAIN LOOP)
# ==============================================================================
def main():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tugas 2 Grafkom - Transformasi Geometri 2D Pesawat")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 12)

    # State Parameter Transformasi Awal
    pos_x, pos_y = WIDTH // 2, HEIGHT // 2
    angle = 0.0
    scale = 1.0

    # Kecepatan Perubahan Parameter
    MOVE_SPEED = 4.0
    ROTATE_SPEED = 3.0
    SCALE_SPEED = 0.02
    MIN_SCALE, MAX_SCALE = 0.3, 3.5

    running = True
    while running:
        # 1. Handling Event Single Key Press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Reset variabel ke kondisi awal
                    pos_x, pos_y = WIDTH // 2, HEIGHT // 2
                    angle = 0.0
                    scale = 1.0

        # 2. Handling Continuous Key Press (Interaktif Real-Time)
        keys = pygame.key.get_pressed()
        
        # Translasi (Arrow Keys)
        if keys[pygame.K_LEFT]:
            pos_x -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            pos_x += MOVE_SPEED
        if keys[pygame.K_UP]:
            pos_y -= MOVE_SPEED
        if keys[pygame.K_DOWN]:
            pos_y += MOVE_SPEED

        # Rotasi (Tombol A / D)
        if keys[pygame.K_a]:
            angle -= ROTATE_SPEED
        if keys[pygame.K_d]:
            angle += ROTATE_SPEED

        # Penskalaan (Tombol + / -)
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
            scale = min(MAX_SCALE, scale + SCALE_SPEED)
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            scale = max(MIN_SCALE, scale - SCALE_SPEED)

        # 3. Kalkulasi Matriks Transformasi Komposisi (NumPy)
        # Urutan Operasi: S (Scaling) -> R (Rotation) -> T (Translation)
        S = create_scaling_matrix(scale, scale)
        R = create_rotation_matrix(angle)
        T = create_translation_matrix(pos_x, pos_y)

        # Matriks Komposisi M = T @ R @ S
        M = T @ R @ S

        # Transposisi & Perkalian Vektor Matriks
        transformed_vertices = (M @ ORIGINAL_VERTICES.T).T

        # Ambil koordinat 2D (x, y) untuk kebutuhan rendering poligon
        pixel_points = transformed_vertices[:, :2]

        # 4. Rendering Kanvas & Objek
        draw_grid(screen)

        # Gambar Body Poligon Pesawat
        pygame.draw.polygon(screen, COLOR_PLANE_FILL, pixel_points)
        pygame.draw.polygon(screen, COLOR_PLANE_OUTLINE, pixel_points, width=2)
        
        # Indikator Hidung Pesawat
        pygame.draw.circle(screen, COLOR_NOSE, (int(pixel_points[0][0]), int(pixel_points[0][1])), max(3, int(4 * scale)))

        # Gambar UI HUD Control
        draw_hud(screen, font, pos_x, pos_y, angle, scale)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()