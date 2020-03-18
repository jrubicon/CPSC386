import pygame as pg
from vector import Vector


class Ship:
    def __init__(self, game, vector=Vector()):
        self.game = game
        self.screen = game.screen
        self.velocity = vector
        self.screenRect = game.screen.get_rect()
        self.shipimage = pg.image.load('SOMESHIP.png')
        self.rect = self.shipimage.get_rect()
        self.rect.midbottom = self.screenRect.midbottom
        self.lasers = pg.sprite.Group()

    def center_ship(self):
        self.rect.midbottom = self.screenRect.midbottom

    def fire(self):
        laser = Laser(game=self.game)
        self.lasers.add(laser)

    def remove_lasers(self):
        self.lasers.remove()

    def move(self):
        if self.velocity == Vector():
            return
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y
        self.game.limit_on_screen(self.rect)

    def draw(self):
        self.screen.blit(self.shipimage, self.rect)

    def update(self):
        fleet = self.game.fleet
        self.move()
        self.draw()
        for laser in self.lasers.sprites():
            laser.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)
        aliens_hit = pg.sprite.groupcollide(fleet.aliens, self.lasers, False, True)
        if len(aliens_hit.keys()) > 0:
            print('{} aliens hit'.format(len(aliens_hit.keys())))
        for alien in aliens_hit:
            alien.hit()
            if alien.health <= 0:
                fleet.aliens.remove(alien)
        if not fleet.aliens:
            self.game.restart()


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector ({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__add__(-1 * other)

    def __rmul__(self, k: float):
        return Vector(k * self.x, k * self.y)

    def __mul__(self, k: float):
        return self.__rmul__(k)

    def __truediv__(self, k: float):
        return self.__rmul__(1.0/k)

    def __neg__(self):
        self.x *= -1
        self.y *= -1

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def test():
        v = Vector(x=5, y=5)
        u = Vector(x=4, y=4)
        print('v is {}'.format(v))
        print('u is {}'.format(u))
        print('uplusv is {}'.format(u + v))
        print('uminusv is {}'.format(u - v))
        print('ku is {}'.format(3 * u))
        print('-u is {}'.format(-1 * u))


def main():
    v = Vector()
    v.test()
