import pygame
import requests

#  !!!Интерфейс и загрузку мы делали вместе!!!

#  request = input('Введите коорндинаты места через запятую без пробелов.:\n').split(',')
#  delta = input('Введите масштаб:\n')

request = '37.530887,55.703118'.split(',')
delta = '0.002'

api_server = "http://static-maps.yandex.ru/1.x/"

lon, lat = request[0], request[1]


def load_arena():
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    response = requests.get(api_server, params=params)
    if not response:
        return False

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    image = pygame.image.load(map_file)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    return True


pygame.init()
pygame.display.set_caption('AAmaps')
screen = pygame.display.set_mode((450, 450))
load_arena()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
                delta = str(float(delta) - 0.01)
                if not load_arena():
                    delta = olddelta
            if event.key == pygame.K_PAGEDOWN:
                olddelta = delta
                delta = str(float(delta) + 0.01)
                if not load_arena():
                    delta = olddelta

pygame.quit()
