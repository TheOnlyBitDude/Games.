import pygame

pygame.init()

screen = pygame.display.set_mode((720, 480))

clock = pygame.time.Clock()


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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.rect.y -= self.fall_counter
            self.fall_counter += 0.75
            if pygame.sprite.collide_rect(self, floor):
                self.fall_counter = 4

        if self.fall_counter >= 8:
            self.fall_counter = 8
        elif self.fall_counter <= -15:
            self.fall_counter = -15

        if pygame.sprite.collide_rect(self, roof):
            self.rect.y = 25
            self.fall_counter = 0

        if not keys[pygame.K_SPACE]:
            self.fall_counter -= 0.75
            self.rect.y -= self.fall_counter
            if pygame.sprite.collide_rect(self, floor):
                self.fall_counter = 0
                self.rect.y = 405
            if pygame.sprite.collide_rect(self, roof):
                self.rect.y = 26

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            if pygame.sprite.collide_rect(self, wall_left):
                self.rect.x += self.speed

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            if pygame.sprite.collide_rect(self, wall_right):
                self.rect.x -= self.speed

        self.update()

    def update(self):
        screen.blit(self.image, self.rect)


floor = GameSprite("placeholder.png", (2000, 25), (0, 455))
roof = GameSprite("placeholder.png", (2000, 25), (0, 0))
wall_left = GameSprite("placeholder.png", (25, 480), (0, 0))
wall_right = GameSprite("placeholder.png", (25, 480), (1975, 0))

player = PlayerSprite("placeholder_player.png", (50, 50), (50, 0))

stage_list = [floor, roof, wall_left, wall_right]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 10, 255))

    player.move()

    for sprite in stage_list:
        sprite.update()

    pygame.display.update()

    clock.tick(60)

pygame.quit()
