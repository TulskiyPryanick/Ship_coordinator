import os
import time
import random
import auxiliary_functions as af


def clean_console():
    os.system('cls')


def delay(sec: int):
    time.sleep(sec)


player_field = af.create_field()  # пустое поле игрока
bot_visible_field = af.create_field()  # пустое поле бота для выстрелов
bot_real_field = af.create_field()  # пустое поле бота для кораблей

player_ship_zone = []  # корабли игрока
player_danger_zone = []  # опасные для расстановки кораблей зоны
spent_cartridges = []  # стреляные координаты игрока

bot_ship_zone = []  # корабли бота
bot_danger_zone = []  # опасные для расстановки кораблей зоны
bot_spent_cartridges = []  # стреляные координаты бота

bots_cor = af.create_all_coordinates()


def players_shot():
    while True:
        shot_coordinate = af.coordinate_translator(
                          input("Введите координату выстрела:"))
        if shot_coordinate is not None:
            break
        else:
            print('Не верная координата!')
            delay(1)
    shot_status = af.two_fields_shot(bot_visible_field, bot_real_field,
                                     shot_coordinate, spent_cartridges,
                                     bot_ship_zone, bot_danger_zone)
    if shot_status == 'miss':
        clean_console()
        af.two_fields_output(player_field, bot_visible_field,
                             player_ship_zone, bot_ship_zone)
        print("Промах")
    elif shot_status == 'alive':
        clean_console()
        af.two_fields_output(player_field, bot_visible_field,
                             player_ship_zone, bot_ship_zone)
        print("Корабль подбит!")
        players_shot()
    elif shot_status == 'blow_up':
        clean_console()
        af.two_fields_output(player_field, bot_visible_field,
                             player_ship_zone, bot_ship_zone)
        print("Корабль уничтожен!")
        players_shot()
    elif shot_status == 'no_shot':
        print("Вы уже стреляли в эту клетку")
        delay(2)
        clean_console()
        af.two_fields_output(player_field, bot_visible_field,
                             player_ship_zone, bot_ship_zone)
        players_shot()


def first_bot_shot() -> str:
    coordinate = random.choice(bots_cor)
    shot_info = af.field_shot(player_field, coordinate, bots_cor,
                              player_ship_zone, player_danger_zone)
    if shot_info == 'blow_up':
        if len(player_ship_zone) > 0:
            bots_shot()
    elif shot_info == 'alive':
        return coordinate


def second_bot_shot(coordinate: str):
    directions = af.cross_near_cells(coordinate, bots_cor)
    for direc in list(directions.keys()):
        if directions[direc] not in bots_cor:
            del directions[direc]
    while True:
        direction = random.choice(list(directions.keys()))
        shot_info = af.field_shot(player_field,
                                  directions[direction], bots_cor,
                                  player_ship_zone, player_danger_zone)
        if shot_info == 'blow_up':
            if len(player_ship_zone) > 0:
                bots_shot()
            break
        elif shot_info == 'alive':
            return [direction, directions[direction], coordinate]
            break
        elif shot_info == 'miss':
            del directions[direction]
            players_shot()


def third_fourth_bot_shot(dir_coord: list):
    direction = dir_coord[0]
    dir_coordinate = dir_coord[1]
    original_coordinate = dir_coord[2]

    directions = af.cross_near_cells(dir_coordinate, bots_cor)
    if direction in directions:
        shot_info = af.field_shot(player_field,
                                  directions[direction], bots_cor,
                                  player_ship_zone, player_danger_zone)
        if shot_info == 'blow_up':
            if len(player_ship_zone) > 0:
                bots_shot()
        elif shot_info == 'alive':
            return [direction, directions[direction], original_coordinate]
        elif shot_info == 'miss':
            players_shot()
            if direction == 'up':
                new_direction = 'down'
            if direction == 'down':
                new_direction = 'up'
            if direction == 'right':
                new_direction = 'left'
            if direction == 'left':
                new_direction = 'right'
            return [new_direction, original_coordinate, '']
    else:
        new_directions = af.cross_near_cells(original_coordinate, bots_cor)
        if direction == 'up':
            new_direction = 'down'
        if direction == 'down':
            new_direction = 'up'
        if direction == 'right':
            new_direction = 'left'
        if direction == 'left':
            new_direction = 'right'
        shot_info = af.field_shot(player_field,
                                  new_directions[new_direction], bots_cor,
                                  player_ship_zone, player_danger_zone)
        if shot_info == 'blow_up':
            if len(player_ship_zone) > 0:
                bots_shot()
        elif shot_info == 'alive':
            return [new_direction, new_directions[new_direction], '']


def bots_shot():
    first_shot = first_bot_shot()
    if first_shot:
        clean_console()
        af.two_fields_output(player_field, bot_visible_field,
                             player_ship_zone, bot_ship_zone)
        delay(2)
        second_shot = second_bot_shot(first_shot)
        if second_shot:
            clean_console()
            af.two_fields_output(player_field, bot_visible_field,
                                 player_ship_zone, bot_ship_zone)
            delay(2)
            third_shot = third_fourth_bot_shot(second_shot)
            if third_shot:
                clean_console()
                af.two_fields_output(player_field, bot_visible_field,
                                     player_ship_zone, bot_ship_zone)
                delay(2)
                fourth_shot = third_fourth_bot_shot(third_shot)
                if fourth_shot:
                    clean_console()
                    af.two_fields_output(player_field, bot_visible_field,
                                         player_ship_zone, bot_ship_zone)
                    delay(2)
                    third_fourth_bot_shot(fourth_shot)
    clean_console()
    af.two_fields_output(player_field, bot_visible_field,
                         player_ship_zone, bot_ship_zone)
    delay(2)


af.field_output(player_field)
print('Расставляй корабли, юнга!\n')

single_deck = 4
double_deck = 3
three_deck = 2
four_deck = 1


while single_deck:
    coordinate = af.coordinate_translator(
      input(f"Координата однопалубного корабля ({4-single_deck}/4):"))
    if af.create_ship(1, player_field, player_danger_zone, player_ship_zone,
                      coordinate) == 'created':
        single_deck -= 1
        delay(1)
        clean_console()
        af.field_output(player_field)
    else:
        print("Неверная координата!")
        delay(2)
        clean_console()
        af.field_output(player_field)

while double_deck:
    coordinate_1 = af.coordinate_translator(
      input(f"Координата носа двухпалубного корабля ({3 - double_deck}/3):"))
    coordinate_2 = af.coordinate_translator(
      input(f"Координата кормы двухпалубного корабля ({3 - double_deck}/3):"))
    if af.create_ship(2, player_field, player_danger_zone, player_ship_zone,
                      coordinate_1, coordinate_2) == 'created':
        double_deck -= 1
        delay(1)
        clean_console()
        af.field_output(player_field)
    else:
        print("Неверные координаты!")
        delay(2)
        clean_console()
        af.field_output(player_field)

while three_deck:
    coordinate_1 = af.coordinate_translator(
      input(f"Координата носа трёхпалубного корабля ({2 - three_deck}/2):"))
    coordinate_2 = af.coordinate_translator(
      input(f"Координата кормы трёхпалубного корабля ({2 - three_deck}/2):"))
    if af.create_ship(3, player_field, player_danger_zone, player_ship_zone,
                      coordinate_1, coordinate_2) == 'created':
        three_deck -= 1
        delay(1)
        clean_console()
        af.field_output(player_field)
    else:
        print("Неверные координаты!")
        delay(2)
        clean_console()
        af.field_output(player_field)

while four_deck:
    coordinate_1 = af.coordinate_translator(
      input(f"Координата носа четырёхпалубного корабля ({1 - four_deck}/1):"))
    coordinate_2 = af.coordinate_translator(
      input(f"Координата кормы четырёхпалубного корабля ({1 - four_deck}/1):"))
    if af.create_ship(4, player_field, player_danger_zone, player_ship_zone,
                      coordinate_1, coordinate_2) == 'created':
        four_deck -= 1
        delay(1)
        clean_console()
        af.field_output(player_field)
    else:
        print("Неверные координаты!")
        delay(2)
        clean_console()
        af.field_output(player_field)


bots_single_deck = 4
bots_double_deck = 3
bots_three_deck = 2
bots_four_deck = 1

while bots_single_deck:
    coordinate = random.choice(bots_cor)
    if af.create_ship(1, bot_real_field, bot_danger_zone, bot_ship_zone,
       coordinate) == 'created':
        bots_single_deck -= 1

while bots_double_deck:
    coordinate_1 = random.choice(bots_cor)
    coordinate_2 = random.choice(af.cross_doble_cells(coordinate_1))
    if af.create_ship(2, bot_real_field, bot_danger_zone, bot_ship_zone,
       coordinate_1, coordinate_2) == 'created':
        bots_double_deck -= 1

while bots_three_deck:
    coordinate_1 = random.choice(bots_cor)
    coordinate_2 = random.choice(bots_cor)
    if af.create_ship(3, bot_real_field, bot_danger_zone, bot_ship_zone,
       coordinate_1, coordinate_2) == 'created':
        bots_three_deck -= 1

while bots_four_deck:
    coordinate_1 = random.choice(bots_cor)
    coordinate_2 = random.choice(bots_cor)
    if af.create_ship(4, bot_real_field, bot_danger_zone, bot_ship_zone,
       coordinate_1, coordinate_2) == 'created':
        bots_four_deck -= 1

print("Корабли расставлены!В бой!")
delay(2)
clean_console()
af.two_fields_output(player_field, bot_visible_field,
                     player_ship_zone, bot_ship_zone)

if random.choice(['bot', 'player']) == 'player':
    print("Ваш ход")
    players_shot()


while len(player_ship_zone) > 0 and len(bot_ship_zone) > 0:
    bots_shot()
    if len(player_ship_zone) == 0 or len(bot_ship_zone) == 0:
        break
    players_shot()

if len(player_ship_zone) == 0:
    print('Вы проиграли!\nИгра окончена')

if len(bot_ship_zone) == 0:
    print('Вы победили!\nИгра окончена')
