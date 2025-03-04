import os

try:
    import pygame
except ModuleNotFoundError:
    os.system("pip install --upgrade pip")
    os.system("pip install pygame")

import pygame

pygame.init()

screen = pygame.display.set_mode((720, 480))

clock = pygame.time.Clock()

# Stage boundaries for scrolling
start_X = 0  # Leftmost X for stage
end_X = -1275  # Rightmost X for stage (adjust based on your stage size)
stage_offset = 0  # Track how much the stage has been shifted
player_locked = False  # Track if player is locked at center
initial_lock_pos = 0  # Track initial stage X when player gets locked


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_file, size, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_file), size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class PlayerSprite(GameSprite):
    def __init__(self, image_file, size, pos):
        super().__init__("placeholder.png", size, pos)
        self.speed = 5
        self.image = pygame.transform.scale(pygame.image.load(image_file), size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.fall_counter = 0

    def move(self):
        global player_locked, initial_lock_pos

        keys = pygame.key.get_pressed()

        if self.fall_counter >= 7:
            self.fall_counter = 7
        elif self.fall_counter <= -15:
            self.fall_counter = -15

        if keys[pygame.K_w]:
            self.rect.y -= self.fall_counter
            if pygame.sprite.collide_rect(self, roof):
                self.fall_counter = 0
                self.rect.top = roof.rect.bottom
            else:
                self.fall_counter += 0.75
            if pygame.sprite.collide_rect(self, floor):
                self.fall_counter = 1
                self.rect.bottom = floor.rect.top

        if not keys[pygame.K_w]:
            self.rect.y -= self.fall_counter
            if pygame.sprite.collide_rect(self, floor):
                self.fall_counter = 0
                self.rect.bottom = floor.rect.top
            else:
                self.fall_counter -= 0.75
            if pygame.sprite.collide_rect(self, roof):
                self.fall_counter = -1
                self.rect.top = roof.rect.bottom

        # Horizontal movement
        if keys[pygame.K_a]:
            if not player_locked and self.rect.centerx <= 360 and stage_offset <= end_X:
                player_locked = True
            if player_locked:
                # Unlock if the player moves back to or past the initial lock position
                if stage_offset >= initial_lock_pos:
                    player_locked = False
                else:
                    scroll_stage(self.speed)
            else:
                self.rect.x -= self.speed

            if pygame.sprite.collide_rect(self, wall_left):
                self.rect.left = wall_left.rect.right

        if keys[pygame.K_d]:
            if self.rect.centerx >= 360 and not player_locked:
                if stage_offset == 0:
                    # Lock the player and start scrolling the stage
                    player_locked = True
                    initial_lock_pos = stage_offset

            if self.rect.centerx >= 360 and stage_offset <= end_X and player_locked:
                player_locked = False

            if player_locked:
                scroll_stage(-self.speed)
            else:
                self.rect.x += self.speed

            if pygame.sprite.collide_rect(self, wall_left):
                self.rect.right = wall_left.rect.left

        self.update()

    def update(self):
        screen.blit(self.image, self.rect)


def scroll_stage(offset_x):
    global stage_offset
    new_offset = stage_offset + offset_x

    # Check if the new offset is within bounds
    if start_X >= new_offset >= end_X:
        stage_offset = new_offset
        for sprite in stage_list:
            sprite.rect.x += offset_x
        background.rect.x += offset_x * 0.7


# Create stage elements
background = GameSprite("bg.jpg", (2560, 1440), (0, 0))
floor = GameSprite("placeholder.png", (2000, 25), (0, 455))
roof = GameSprite("placeholder.png", (2000, 25), (0, 0))
wall_left = GameSprite("placeholder.png", (25, 480), (0, 0))
wall_right = GameSprite("placeholder.png", (25, 480), (1975, 0))
block = GameSprite("placeholder.png", (50, 50), (785, 220))

player = PlayerSprite("placeholder_player.png", (50, 50), (50, 0))

stage_list = [floor, roof, wall_left, wall_right, block]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 10, 255))

    background.update()

    player.move()

    for sprite in stage_list:
        sprite.update()
    print(stage_offset)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
