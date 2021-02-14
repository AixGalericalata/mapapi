import pygame
import requests

#  !!!Интерфейс и загрузку мы делали вместе!!!

#  request = input('Введите коорндинаты места через запятую без пробелов.:\n').split(',')
#  delta = input('Введите масштаб:\n')

request = '37.530887,55.703118'.split(',')
delta = '0.002'

api_server = "http://static-maps.yandex.ru/1.x/"

width, height = 450, 450

poi = None
lon, lat = request[0], request[1]
mode = 'map'


def search(text):
    global lon, lat, delta, poi
    print(text)
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": text,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        return

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    #  lower_corner = toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
    #  upper_corner = toponym["boundedBy"]["Envelope"]["upperCorner"].split()

    #  delta_longitude = float(upper_corner[0]) - float(lower_corner[0])
    #  delta_latitude = float(upper_corner[1]) - float(lower_corner[1])
    poi = toponym["Point"]["pos"].split()
    lon = poi[0]
    lat = poi[1]
    delta = '0.002'
    load_arena()
    draw()


class InputBox:
    def __init__(self, x, y, width, height, callback):
        self.isactive = False
        self.rect = pygame.Rect(x, y, width, height)
        self.txt_surface = None
        self.text = ''
        self.callback = callback

    def draw(self):
        pygame.draw.rect(screen, pygame.Color('white'), self.rect)
        if self.txt_surface:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, pygame.Color('lightskyblue3') if self.isactive else (30, 30, 30),
                         self.rect, 2)

    def on_mouse_event(self, pos):
        if self.rect.collidepoint(pos):
            self.isactive = not self.isactive
            return True
        else:
            if self.isactive:
                self.isactive = False
                return True
            return False

    def on_key_event(self, key, unicode):
        if not self.isactive:
            return False
        if key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            self.txt_surface = myfont.render(self.text, True, pygame.Color('black'))
        if key == pygame.K_RETURN:
            self.callback(self.text)
            return False
        if unicode:
            self.text += unicode
            self.txt_surface = myfont.render(self.text, True, pygame.Color('black'))
        return True


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
    global map_image
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": mode
    }
    if poi:
        params['pt'] = f"{poi[0]},{poi[1]},pm2dgl"

    response = requests.get(api_server, params=params)
    if not response:
        return False

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    map_image = pygame.image.load(map_file)
    return True


def draw():
    screen.blit(map_image, (0, 0))
    for button in buttons:
        button.draw()
    input_box.draw()
    pygame.display.flip()


pygame.font.init()
myfont = pygame.font.SysFont('Arial', 15)

map_image = None
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
input_box = InputBox(0, height - 30, width, 30, search)

pygame.init()
pygame.display.set_caption('AAmaps')
screen = pygame.display.set_mode((width, height))
load_arena()
running = True
wantdraw = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = event.pos
            for button in buttons:
                if button.click(pos):
                    wantdraw = True
                    break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.on_mouse_event(event.pos):
                wantdraw = True
        # !!!Это делал Артём!!!
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            time = float(lat)
            time -= float(delta) * 0.5
            lat = str(time)
            load_arena()
            wantdraw = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            time = float(lat)
            time += float(delta) * 0.5
            lat = str(time)
            load_arena()
            wantdraw = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            time = float(lon)
            time -= float(delta) * 0.5
            lon = str(time)
            load_arena()
            wantdraw = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            time = float(lon)
            time += float(delta) * 0.5
            lon = str(time)
            load_arena()
            wantdraw = True
        # !!!Это делал Лёша!!!
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                olddelta = delta
                delta = str(float(delta) / 2)
                if not load_arena():
                    delta = olddelta
                else:
                    wantdraw = True
            if event.key == pygame.K_PAGEDOWN:
                olddelta = delta
                delta = str(float(delta) * 2)
                if not load_arena():
                    delta = olddelta
                else:
                    wantdraw = True
            if input_box.on_key_event(event.key, event.unicode):
                wantdraw = True
    if wantdraw:
        draw()
        wantdraw = False

pygame.quit()
