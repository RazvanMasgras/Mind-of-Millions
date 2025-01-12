import pygame, textwrap

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

    def change_image(self, new_image):
        self.image = new_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        

def render_text_box(screen, text, box_rect, font_name="arial", max_font_size=50, min_font_size=20, wrap_limit=5):
    x, y, box_width, box_height = box_rect

    # Attempt to find the best font size
    font_size = max_font_size
    font = pygame.font.SysFont(font_name, font_size)

    while font_size > min_font_size:
        # Wrap text based on box width
        wrapped_text = textwrap.fill(text, width=box_width // (font_size // 2))
        lines = wrapped_text.splitlines()

        # Check if the wrapped text fits within the height
        line_height = font.size("Tg")[1]
        total_text_height = line_height * len(lines)
        if len(lines) <= wrap_limit and total_text_height <= box_height:
            break

        # Decrease font size and try again
        font_size -= 1
        font = pygame.font.SysFont(font_name, font_size)

    # Render each line and draw it centered on the screen
    font = pygame.font.SysFont(font_name, font_size)
    wrapped_text = textwrap.fill(text, width=box_width // (font_size // 2))
    lines = wrapped_text.splitlines()

    total_text_height = font.size("Tg")[1] * len(lines)
    start_y = y + (box_height - total_text_height) // 2  # Center vertically

    for line in lines:
        text_surface = font.render(line, True, "white")
        text_width, text_height = font.size(line)
        start_x = x + (box_width - text_width) // 2  # Center horizontally
        screen.blit(text_surface, (start_x, start_y))
        start_y += text_height
