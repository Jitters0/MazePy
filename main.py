import config
import random
import json
import logging
import os.path


def savewrite():
    raw_data = {
        'coords': (Player.x, Player.y),
        'power': Player.power,
        'health': Player.health,
        'has_key': Player.has_key,
        'wand_charges': Player.wand_charges,
    }
    data = json.loads(str(json.dumps(raw_data)))
    with open('save.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
        logging.info('Сохранение было записано')
        print('Сохранение было записано!')
        quit()


def saveread():
    with open('save.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        Player.x, Player.y = data['coords']
        Player.power = data['power']
        Player.health = data['health']
        Player.has_key = data['has_key']
        Player.wand_charges = data['wand_charges']
        print('Сохранение было восстановленно!')
        logging.info("Было восстановленно сохранение")


class Blocks:
    final_block = (8, 4)
    base_blocks = ((1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (4, 1), (5, 1), (6, 1), (6, 2), (6, 3), (6, 4), (7, 4))
    heal_blocks = ((5, 4), (7, 2))
    key_block = (3, 3)
    restore_power_block = (5, 2)

    def __init__(self, current_block):
        self.current_block = current_block
        self.check()

    def check(self):
        if self.current_block in self.base_blocks:
            rand_base_blocks = random.sample(self.base_blocks, 4)
            print('Горящими клетками были: ', end='')
            logging.info(f"Созданы горящие клетки: {rand_base_blocks}")
            for el in rand_base_blocks:
                print(f'{el[0]}/{el[1]} ', end='')
            print('')
            if self.current_block in rand_base_blocks:
                Player.health -= 1
                logging.info("Игрок попал на горящую клетку")
                print('Пол под вами загорелся\nВы потеряли одну жизнь')

        if self.current_block in self.heal_blocks:
            Player.health = 5
            logging.info("Игрок восстановил здоровье")
            print('Вы восстановили все здоровье!')

        if self.current_block == self.key_block:
            logging.info("Игрок нашел клетку с ключем")
            question = input('Вы нашли ключ!\nХотите его подобрать? Y/N: ')
            if question.upper() == 'Y':
                Player.has_key = 1
                Player.power -= 1
                self.key_block = ()
                print('Вы подобрали ключ!')
                logging.info("Игрок взял ключ")
            else:
                logging.info("Игрок решил не брать ключ")
                print('Вы решили не брать ключ')

        if self.current_block == self.restore_power_block:
            Player.power = 15
            print('Вы восстановили всю энергию!')
            logging.info("Игрок восстановил всю энергию")

        if self.current_block == self.final_block:
            if Player.has_key == 0:
                Player.died = 1
            elif Player.has_key == 1:
                Player.win = 1


class Player:
    x = 1
    y = 1
    step = 1
    power = 15
    health = 5
    has_key = 0
    wand_charges = 3
    died = 0
    win = 0

    def move_right(self):
        possible_ways = config.maze[(self.x, self.y)]
        try_way = (self.x + self.step, self.y)
        tries = 0
        for el in possible_ways:
            if try_way == el:
                self.x = self.x + self.step
                print('Вы сделали шаг вправо')
                logging.info("Игрок сделал шаг вправо")
                Blocks((self.x, self.y))
                break
            else:
                if tries >= 1:
                    self.hit_the_wall()
                    logging.info("Игрок попытался сделать шаг вправо, но ударился об стену")
                else:
                    tries += 1

    def move_left(self):
        possible_ways = config.maze[(self.x, self.y)]
        try_way = (self.x - self.step, self.y)
        tries = 0
        for el in possible_ways:
            if try_way == el:
                self.x = self.x - self.step
                print('Вы сделали шаг влево')
                logging.info("Игрок сделал шаг влево")
                Blocks((self.x, self.y))
                break
            else:
                if tries >= 1:
                    self.hit_the_wall()
                    logging.info("Игрок попытался сделать шаг влево, но ударился об стену")
                else:
                    tries += 1

    def move_up(self):
        possible_ways = config.maze[(self.x, self.y)]
        try_way = (self.x, self.y + self.step)
        tries = 0
        for el in possible_ways:
            if try_way == el:
                self.y = self.y + self.step
                print('Вы сделали шаг вперед')
                logging.info("Игрок сделал шаг вперед")
                Blocks((self.x, self.y))
                break
            else:
                if tries >= 1:
                    self.hit_the_wall()
                    logging.info("Игрок попытался сделать шаг вперед, но ударился об стену")
                else:
                    tries += 1

    def move_down(self):
        possible_ways = config.maze[(self.x, self.y)]
        try_way = (self.x, self.y - self.step)
        tries = 0
        for el in possible_ways:
            if try_way == el:
                self.y = self.y - self.step
                print('Вы сделали шаг назад')
                logging.info("Игрок сделал шаг назад")
                Blocks((self.x, self.y))
                break
            else:
                if tries >= 1:
                    self.hit_the_wall()
                    logging.info("Игрок попытался сделать шаг назад, но ударился об стену")
                else:
                    tries += 1

    def heal(self):
        if self.wand_charges > 0:
            self.health += 1
            self.power -= 1
            self.wand_charges -= 1
            print('Вы восстановили 1 жизнь')
            logging.info("Игрок восстановил 1 хм с помощью жезла")
        else:
            print('У вас закончились заряды в жезле лечения')
            logging.info("Игрок попытался восстановить 1 хп с помощью жезла, но использования закончились")

    def restore_power(self):
        self.power = 15

    def hit_the_wall(self):
        print('Вы ударились об стену и потеряли одну жизнь!')
        self.health -= 1


class Input:
    def __init__(self):
        self.player = Player()

    def execute(self):  # TODO: Вывод кол-ва хп и энергии
        while True:
            print('------------------------------------------')
            print(f'Сейчас вы находитесь на координатах: {self.player.x}/{self.player.y}')
            print(f'Ваше текущее количество жизней: {self.player.health}')
            print(f'Ваще текущее количество энергии: {self.player.power}')
            if self.player.health < 1:
                print('У вас закончили жизни! Ваш герой погиб!')
                logging.info("У игрока закончили жизни и он погиб")
                break
            elif self.player.power < 1:
                print('У вас закончилась энергия! Вы уснули и голем нашел вас в лабиринте! Вы погибли!')
                logging.info("У игрока закончилась энергия и он погиб")
                break
            elif self.player.died == 1:
                print('Вы попали в руки голема!\nВы не смогли сбежать так как у вас не было ключа и вы погибли')
                logging.info("Игрок попал к голему без ключа")
                break
            elif self.player.win == 1:
                print('Вы победили!')
                logging.info("Игрок победил")
                break
            else:
                move_input = input()
                if move_input.upper() == 'W':
                    logging.info("Была нажата кнопка 'W'")
                    self.player.move_up()

                if move_input.upper() == 'S':
                    logging.info("Была нажата кнопка 'S'")
                    self.player.move_down()

                if move_input.upper() == 'A':
                    logging.info("Была нажата кнопка 'A'")
                    self.player.move_left()

                if move_input.upper() == 'D':
                    logging.info("Была нажата кнопка 'D'")
                    self.player.move_right()

                if move_input.upper() == 'H':
                    logging.info("Была нажата кнопка 'H'")
                    self.player.heal()

                if move_input.upper() == 'E':
                    logging.info("Была нажата кнопка 'E'")
                    savewrite()


def main():
    pl = Input()
    pl.execute()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="maze.log", encoding='UTF-8')
    print('Приветствую в игре "Лабиринт"')
    print('Для выхода используйте кнопку "E"')
    print('Для передвижения используйте "WASD"')
    print('Вы можете вылечить себя 3 раза кнопкой "H"')
    print('Правила игры можно прочитать на странице проэкта')
    if os.path.isfile('save.json'):
        ask = input('Было найдено сохранение, хотите его восстановить? Y/N: ')
        if ask.upper() == 'Y':
            saveread()
        else:
            os.remove('save.json')
    main()
