#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2008  Ferraro Luciano (aka lux) <luciano.ferraro@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import pygame

from pil import *

class AnimatedSprite (pygame.sprite.Sprite):
    def __init__(self, core, x,y, image):
        pygame.sprite.Sprite.__init__(self)
        self.core = core
        self.speed = 2*self.core.scale
        
        self.delay, self._frames = load_gif(image)
        self.frames = [self._frames[:4], self._frames[4:8], self._frames[8:12], self._frames[12:16]] #giu destra sinistra sopra
        self.sprite = pygame.sprite.RenderPlain(self)
        
        self.moveto = [0,0]
        self.frame = [0,0]
        self.image = self.frames[0][0]
        
        self.rect = self.image.get_rect().move((x,y))
        self.clock = pygame.time.Clock()
        self.time = 0
        
    def GetPos (self, rect=None):
        if not rect:
            rect = self.rect
        a,b = rect.topleft,rect.bottomright
        x = ((b[0]-a[0])/2)+a[0]
        y = ((b[1]-a[1])/2)+a[1]
        return x,y
    def GetVirtualPos (self, rect=None):
        return self.core.pixel2vpos(*self.GetPos(rect))
        
    def goDown (self):
        self.frame[0] = 0
        self.moveto[1] = self.core.SpaceSize
    def goRight (self):
        self.frame[0] = 1
        self.moveto[0] = self.core.SpaceSize
    def goLeft (self):
        self.frame[0] = 2
        self.moveto[0] = -self.core.SpaceSize
    def goUp (self):
        self.frame[0] = 3
        self.moveto[1] = -self.core.SpaceSize

    def update (self):
        if any(self.moveto):
            self.time += self.clock.tick()
            if self.time >= self.delay:
                self.time = 0
                self.frame[1] += 1
                if self.frame[1] >= len(self.frames[self.frame[0]]):
                    self.frame[1] = 0
                self.image = self.frames[self.frame[0]][self.frame[1]]
                self.rect = self.image.get_rect().move(self.rect.topleft)
                self.colorkey = self.image.get_at((0,self.image.get_height()-1))
                self.image.set_colorkey(self.colorkey)
                
            moveto = [0,0]
            for count,mt in enumerate(self.moveto):
                if mt < 0:
                    self.moveto[count] += self.speed
                    if self.moveto[count] > 0:
                        self.moveto[count] = 0
                    moveto[count] = -self.speed
                elif mt > 0:
                    self.moveto[count] -= self.speed
                    if self.moveto[count] < 0:
                        self.moveto[count] = 0
                    moveto[count] = self.speed
                    
            if any(moveto):
                newrect = self.rect.move(moveto)
                collidepoints = (newrect.topright,newrect.topleft,newrect.bottomright,newrect.bottomleft)
                collide = all(map(lambda p: self.core.playingarea.collidepoint(p), collidepoints))
                #bombcollide = (self.GetVirtualPos(newrect) != self.core.Bomb.GetVirtualPos())
                bombcollide = True
                if collide and bombcollide:
                    self.rect = newrect
        pygame.event.pump()
        

def PlayerSprite (core, x,y):
    return AnimatedSprite(core, x,y, "sprites/player/red/animplayer.gif")