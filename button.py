import pygame

class Button():
    def __init__(self, image, x, y, text_input, font):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_input = text_input
        self.font = font
        self.text = font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] > self.rect.topleft[0] and position[0] < self.rect.bottomright[0]:
            if position[1] > self.rect.topleft[1] and position[1] < self.rect.bottomright[1]:
                return True
            
    def change_color(self, position):
        if position[0] > self.rect.topleft[0] and position[0] < self.rect.bottomright[0]:
            if position[1] > self.rect.topleft[1] and position[1] < self.rect.bottomright[1]:
                self.text = self.font.render(self.text_input, True, "grey")
            else:
                self.text = self.font.render(self.text_input, True, "white")
        