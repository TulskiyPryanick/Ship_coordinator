def coordinate_translator(coordinate: str) -> str:
    coordinate_lenght = len(coordinate)
    if coordinate_lenght < 2 or coordinate_lenght > 3:
        return None

    letters = {"а": 0,
               "б": 1,
               "в": 2,
               "г": 3,
               "д": 4,
               "е": 5,
               "ж": 6,
               "з": 7,
               "и": 8,
               "к": 9}

    for symbol in coordinate:
        if symbol.isalpha() is True:
            if symbol.lower() in letters.keys():
                vertical_coordinate = letters[symbol.lower()]
                break
    if coordinate_lenght == 2:
        for figure in coordinate:
            if figure.isdigit() is True and figure != '0':
                horizontally_coordinate = int(figure) - 1
    if coordinate_lenght == 3:
        if coordinate.count('10') == 1:
            horizontally_coordinate = 9
        else:
            return None
    try:
        return str(horizontally_coordinate) + str(vertical_coordinate)
    except UnboundLocalError:
        return None


def field_output(field: list):
    print('   А    Б    В    Г    Д    Е    Ж    З    И    К', end='\n\n')
    for num, line in enumerate(field):
        if num < 9:
            print(num + 1, end='  ')
            for cell in line:
                print(cell, end='    ')
            print('\n')
        else:
            print(num + 1, end=' ')
            for last_cell in line:
                print(last_cell, end='    ')
            print('\n')


def two_fields_output(field_left: list, field_right: list,
                      player_ships: list, bot_ships: list):
    print('   А    Б    В    Г    Д    Е    Ж    З    И    К', '\t\t',
          'А    Б    В    Г    Д    Е    Ж    З    И    К', end='\n\n')

    for line_num in range(10):
        if line_num < 9:
            print(line_num + 1, end='  ')
        else:
            print(line_num + 1, end=' ')

        for cells_l in field_left[line_num]:
            print(cells_l, end='    ')
        print('   |     ', end='')
        if line_num < 9:
            print(line_num + 1, end='  ')
        else:
            print(line_num + 1, end=' ')

        for cells_r in field_right[line_num]:
            print(cells_r, end='    ')
        print('\n')

        p_single_deck = 0
        p_double_deck = 0
        p_three_deck = 0
        p_four_deck = 0

        b_single_deck = 0
        b_double_deck = 0
        b_three_deck = 0
        b_four_deck = 0

    for p_ship in player_ships:
        if type(p_ship) is str:
            p_single_deck += 1
        else:
            if len(p_ship) == 2:
                p_double_deck += 1
            if len(p_ship) == 3:
                p_three_deck += 1
            if len(p_ship) == 4:
                p_four_deck += 1

    for b_ship in bot_ships:
        if type(b_ship) is str:
            b_single_deck += 1
        else:
            if len(b_ship) == 2:
                b_double_deck += 1
            if len(b_ship) == 3:
                b_three_deck += 1
            if len(b_ship) == 4:
                b_four_deck += 1
    print('Ваши корабли: | Корабли противника:')
    print(f'*: {p_single_deck}\t        *: {b_single_deck}')
    print(f'**: {p_double_deck}\t        **: {b_double_deck}')
    print(f'***: {p_three_deck}\t        ***: {b_three_deck}')
    print(f'****: {p_four_deck}\t        ****: {b_four_deck}')


def two_fields_shot(visible_field: list, hidden_field: list,
                    coordinate: str, spent_cartridges: list,
                    ship_zone: list, danger_zone: list):
    ff = int(coordinate[0])
    fl = int(coordinate[1])
    if coordinate not in spent_cartridges:
        cell = hidden_field[ff][fl]
        spent_cartridges.append(coordinate)
        if cell == '#':
            visible_field[ff][fl] = '0'
            return 'miss'
        elif cell == '*':
            visible_field[ff][fl] = 'x'
            for ship_num, ship in enumerate(ship_zone):
                if type(ship) is list:
                    for cell_num, ships_cell in enumerate(ship):
                        if ships_cell == coordinate:
                            ship_zone[ship_num][cell_num] = 'x'
                            if (len(ship_zone[ship_num]) ==
                                    ship_zone[ship_num].count('x')):
                                for ship_danger_cell in danger_zone[ship_num]:
                                    ff = int(ship_danger_cell[0])
                                    fl = int(ship_danger_cell[1])
                                    visible_field[ff][fl] = 'x'
                                    if (ship_danger_cell
                                            not in spent_cartridges):
                                        spent_cartridges.append(
                                            ship_danger_cell)
                                ship_zone.pop(ship_num)
                                danger_zone.pop(ship_num)
                                return 'blow_up'
                            else:
                                return 'alive'
                else:
                    if ship == coordinate:
                        for ship_danger_cell in danger_zone[ship_num]:
                            ff = int(ship_danger_cell[0])
                            fl = int(ship_danger_cell[1])
                            visible_field[ff][fl] = 'x'
                            if ship_danger_cell not in spent_cartridges:
                                spent_cartridges.append(ship_danger_cell)
                        ship_zone.pop(ship_num)
                        danger_zone.pop(ship_num)
                        return 'blow_up'
    else:
        return "no shot"


def field_shot(field: list, coordinate: str, coordinats: list,
               ship_zone: list, danger_zone: list):
    ff = int(coordinate[0])
    fl = int(coordinate[1])
    cell = field[ff][fl]
    if cell == '#':
        field[ff][fl] = '0'
        coordinats.remove(coordinate)
        return 'miss'
    elif cell == '*':
        field[ff][fl] = 'x'
        for ship_num, ship in enumerate(ship_zone):
            if type(ship) is list:
                for cell_num, ships_cell in enumerate(ship):
                    if ships_cell == coordinate:
                        ship_zone[ship_num][cell_num] = 'x'
                        if (len(ship_zone[ship_num]) ==
                                ship_zone[ship_num].count('x')):
                            for ship_danger_cell in danger_zone[ship_num]:
                                ff = int(ship_danger_cell[0])
                                fl = int(ship_danger_cell[1])
                                field[ff][fl] = 'x'
                                if (ship_danger_cell
                                        in coordinats):
                                    coordinats.remove(
                                        ship_danger_cell)
                            ship_zone.pop(ship_num)
                            danger_zone.pop(ship_num)
                            return 'blow_up'
                        else:
                            return 'alive'
            else:
                if ship == coordinate:
                    for ship_danger_cell in danger_zone[ship_num]:
                        ff = int(ship_danger_cell[0])
                        fl = int(ship_danger_cell[1])
                        field[ff][fl] = 'x'
                        if ship_danger_cell in coordinats:
                            coordinats.remove(ship_danger_cell)
                    ship_zone.pop(ship_num)
                    danger_zone.pop(ship_num)
                    return 'blow_up'
    coordinats.remove(coordinate)


def create_field() -> list:
    return [['#' for cell in range(10)] for line in range(10)]


def create_all_coordinates() -> list:
    return [str(cell) + str(line) for cell in range(10) for line in range(10)]


def near_cells(coordinate: str) -> list:
    ff = int(coordinate[0])
    fl = int(coordinate[1])
    cells = [
        coordinate,
        str(ff-1) + str(fl-1),
        str(ff-1) + str(fl),
        str(ff-1) + str(fl+1),
        str(ff) + str(fl-1),
        str(ff) + str(fl+1),
        str(ff+1) + str(fl-1),
        str(ff+1) + str(fl),
        str(ff+1) + str(fl+1)
    ]
    return [cell for cell in cells if len(cell) < 3]


def cross_near_cells(coordinate: str, coordinats: list) -> dict:
    ff = int(coordinate[0])
    fl = int(coordinate[1])
    cells = {
        'up': str(ff-1) + str(fl),
        'left': str(ff) + str(fl-1),
        'right': str(ff) + str(fl+1),
        'down': str(ff+1) + str(fl)
    }
    for direction, cell in list(cells.items()):
        if cell not in coordinats:
            del cells[direction]
    return cells


def cross_doble_cells(coordinate: str) -> list:
    ff = int(coordinate[0])
    fl = int(coordinate[1])
    cells = [
         str(ff-1) + str(fl),
         str(ff) + str(fl-1),
         str(ff) + str(fl+1),
         str(ff+1) + str(fl)
    ]
    return [cell for cell in cells if len(cell) < 3]


def check_coordinate(coordinate: str, danger_zone: list) -> bool:
    for zone in danger_zone:
        if coordinate in zone:
            return True
    return False


def check_long_coordinates(coordinate_1: str, coordinate_2: str,
                           danger_zone: list) -> bool:
    ship = []
    ff = int(coordinate_1[0])
    fl = int(coordinate_1[1])
    sf = int(coordinate_2[0])
    sl = int(coordinate_2[1])

    if ff > sf and fl == sl:  # down
        while str(ff)+str(fl) != str(sf)+str(sl):
            ship.append(str(ff) + str(fl))
            ff -= 1

    if ff < sf and fl == sl:  # up
        while str(ff)+str(fl) != str(sf)+str(sl):
            ship.append(str(ff) + str(fl))
            ff += 1

    if ff == sf and fl > sl:  # left
        while str(ff)+str(fl) != str(sf)+str(sl):
            ship.append(str(ff) + str(fl))
            fl -= 1

    if ff == sf and fl < sl:  # right
        while str(ff)+str(fl) != str(sf)+str(sl):
            ship.append(str(ff) + str(fl))
            fl += 1

    ship.append(coordinate_2)

    for ship_cell in ship:
        if type(ship) is list:
            for zone in danger_zone:
                if ship_cell in zone:
                    return True  # intersects
        else:
            if ship_cell in danger_zone:
                return True  # intersects
    return False  # not intersects


def create_ship(size: int, field: list, danger_zone: list, ship_zone: list,
                coordinate_1: str, coordinate_2=''):

    if coordinate_1 is None or coordinate_2 is None:
        return 'not created'

    if size < 2:
        if check_coordinate(coordinate_1, danger_zone):
            return 'not created'

        field[int(coordinate_1[0])][int(coordinate_1[1])] = '*'
        ship_zone.append(coordinate_1)
        danger_zone.append(near_cells(coordinate_1))
        return 'created'

    elif ((abs(int(coordinate_1[0]) - int(coordinate_2[0])) == size-1 and
          coordinate_1[1] == coordinate_2[1]) or
          (abs(int(coordinate_1[1]) - int(coordinate_2[1])) == size-1) and
          coordinate_1[0] == coordinate_2[0]):

        if check_long_coordinates(coordinate_1, coordinate_2, danger_zone):
            return 'not created'

        ship = []
        danger = []

        ff = int(coordinate_1[0])
        fl = int(coordinate_1[1])
        sf = int(coordinate_2[0])
        sl = int(coordinate_2[1])

        field[ff][fl] = "*"
        ship.append(coordinate_1)
        danger.append(near_cells(coordinate_1))

        if ff > sf and fl == sl:  # up
            for cell in range(size-1):
                ff -= 1
                field[ff][fl] = "*"
                down = str(ff) + str(fl)
                ship.append(down)
                danger.append(near_cells(down))

        if ff < sf and fl == sl:  # down
            for cell in range(size-1):
                ff += 1
                field[ff][fl] = "*"
                up = str(ff) + str(fl)
                ship.append(up)
                danger.append(near_cells(up))

        if ff == sf and fl > sl:  # left
            for cell in range(size-1):
                fl -= 1
                field[ff][fl] = "*"
                left = str(ff) + str(fl)
                ship.append(left)
                danger.append(near_cells(left))

        if ff == sf and fl < sl:  # right
            for cell in range(size-1):
                fl += 1
                field[ff][fl] = "*"
                right = str(ff) + str(fl)
                ship.append(right)
                danger.append(near_cells(right))

        if ship == []:
            return 'not created'
        ship_zone.append(ship)

        ship_danger_zone = []

        for zone in danger:
            for coordinate in zone:
                ship_danger_zone.append(coordinate)
        ship_danger_zone = set(ship_danger_zone)
        danger_zone.append(ship_danger_zone)
        return 'created'
    else:
        return 'not created'
