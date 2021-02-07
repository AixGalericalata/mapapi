import pygame
import requests

#  !!!Интерфейс и загрузку мы делали вместе!!!

#  request = input('Введите коорндинаты места через запятую без пробелов.:\n').split(',')
#  delta = input('Введите масштаб:\n')

request = '37.530887,55.703118'.split(',')
delta = '0.002'

api_server = "http://static-maps.yandex.ru/1.x/"

lon, lat = request[0], request[1]

params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": "map"
}


def load_arena():
    response = requests.get(api_server, params=params)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    image = pygame.image.load(map_file)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()


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
            time -= float(delta) * 2
            lat = str(time)
            params['ll'] = ",".join([lon, lat])
            load_arena()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            time = float(lat)
            time += float(delta) * 2
            lat = str(time)
            params['ll'] = ",".join([lon, lat])
            load_arena()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            time = float(lon)
            time -= float(delta) * 2
            lon = str(time)
            params['ll'] = ",".join([lon, lat])
            load_arena()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            time = float(lon)
            time += float(delta) * 2
            lon = str(time)
            params['ll'] = ",".join([lon, lat])
            load_arena()
        # !!!Это делал Лёша!!!
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if delta == '0.002':
                    continue
                delta = str(float(delta) - 0.01)
                params['spn'] = ",".join([delta, delta])
                load_arena()
            if event.key == pygame.K_PAGEDOWN:
                delta = str(float(delta) + 0.01)
                params['spn'] = ",".join([delta, delta])
                load_arena()

pygame.quit()
