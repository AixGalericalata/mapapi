import pygame
import requests

#  !!!Интерфейс и загрузку мы делали вместе!!!

#  request = input('Введите коорндинаты места через запятую без пробелов.:\n').split(',')
#  delta = input('Введите масштаб:\n')

request = '37.530887,55.703118'.split(',')
delta = '0.002'

api_server = "http://static-maps.yandex.ru/1.x/"

lon, lat = request[0], request[1]
mode = 'map'


class Button:
    def __init__(self, name, x, y, color, mode):
        self.x = x
        self.y = y
        self.color = color
        self.mode = mode
        self.surface = myfont.render(name, False, (0, 0, 0))

    def get_width(self):
        return self.surface.get_width()

    def draw(self):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.surface.get_width(), self.surface.get_height()))
        screen.blit(self.surface, (self.x, self.y))

    def click(self, pos):
        global mode
        x = pos[0]
        y = pos[1]
        if self.x <= x < self.x + self.surface.get_width() and self.y <= y < self.y + self.surface.get_height():
            mode = self.mode
            load_arena()
            return True
        return False


def load_arena():
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": mode
    }
    response = requests.get(api_server, params=params)
    if not response:
        return False

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    image = pygame.image.load(map_file)
    screen.blit(pygame.image.load(map_file), (0, 0))
    for button in buttons:
        button.draw()
    pygame.display.flip()
    return True


pygame.font.init()
myfont = pygame.font.SysFont('Arial', 15)

buttons = []
x = 0
map = Button('Схема', x, 0, pygame.Color('red'), 'map')
buttons.append(map)
x += map.get_width()
sat = Button('Спутник', x, 0, pygame.Color('blue'), 'sat')
buttons.append(sat)
x += sat.get_width()
hybrid = Button('Гибрид', x, 0, pygame.Color('green'), 'sat,skl')
buttons.append(hybrid)

pygame.init()
pygame.display.set_caption('AAmaps')
screen = pygame.display.set_mode((450, 450))
load_arena()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.click(pos):
                    break
        # !!!Это делал Артём!!!
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            time = float(lat)
            time -= float(delta) * 0.5
            lat = str(time)
            load_arena()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            time = float(lat)
            time += float(delta) * 0.5
            lat = str(time)
            load_arena()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            time = float(lon)
            time -= float(delta) * 0.5
            lon = str(time)
            load_arena()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            time = float(lon)
            time += float(delta) * 0.5
            lon = str(time)
            load_arena()
        # !!!Это делал Лёша!!!
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                olddelta = delta
                delta = str(float(delta) / 2)
                if not load_arena():
                    delta = olddelta
            if event.key == pygame.K_PAGEDOWN:
                olddelta = delta
                delta = str(float(delta) * 2)
                if not load_arena():
                    delta = olddelta

pygame.quit()
