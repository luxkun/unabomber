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
    justPlanted = False
    moving = False
    def __init__(self, core, vpos, image):
        pygame.sprite.Sprite.__init__(self)
        self.core = core
        self.speed = 2*self.core.scale
        
        self.delay, self._frames = load_gif(image, size=(self.core.xSpaceSize,self.core.ySpaceSize))
        self.frames = [self._frames[:4], self._frames[4:8], self._frames[8:12], self._frames[12:16]] #giu destra sinistra sopra
        self.sprite = pygame.sprite.RenderPlain(self)
        
        self.frame = [0,0]
        self.image = self.frames[0][0]
        
        self.rect = self.image.get_rect()
        self.DirectMove(vpos)
        self.clock = pygame.time.Clock()
        self.time = 0
    
    def DirectMove (self, vpos):
        self.moving = False
        self.vpos = self.fut_vpos = vpos
        self.rect = self.rect.fit(self.core.rects[vpos][1])
    
    def CollideDetector (self, fut_vpos):
        return any(((self.core.Bomb.vpos == fut_vpos), (fut_vpos not in self.core.rects)))
    def TryToMove (self, fut_vpos):
        if not self.CollideDetector(fut_vpos):
            self.moving = True
            self.fut_vpos = fut_vpos
        else:
            self.load_frame()
        
    def goDown (self):
        self.frame[0] = 0
        fut_vpos = (self.vpos[0],self.vpos[1]+1)
        self.TryToMove(fut_vpos)
    def goRight (self):
        self.frame[0] = 1
        fut_vpos = (self.vpos[0]+1,self.vpos[1])
        self.TryToMove(fut_vpos)
    def goLeft (self):
        self.frame[0] = 2
        fut_vpos = (self.vpos[0]-1,self.vpos[1])
        self.TryToMove(fut_vpos)
    def goUp (self):
        self.frame[0] = 3
        fut_vpos = (self.vpos[0],self.vpos[1]-1)
        self.TryToMove(fut_vpos)
    
    def load_frame (self):
        self.image = self.frames[self.frame[0]][self.frame[1]]
        self.rect = self.image.get_rect().move(self.rect.topleft)
        self.colorkey = self.image.get_at((0,self.image.get_height()-1))
        self.image.set_colorkey(self.colorkey)

    def update (self):
        if self.fut_vpos != self.vpos:
            if self.rect.contains(self.core.rects[self.fut_vpos][1]):
                self.DirectMove(self.fut_vpos)
            else:
                self.time += self.clock.tick()
                if self.time >= self.delay:
                    self.time = 0
                    self.frame[1] += 1
                    if self.frame[1] >= len(self.frames[self.frame[0]]):
                        self.frame[1] = 0
                    self.load_frame()
                    
                movetox,movetoy = 0,0
                if self.fut_vpos[1] > self.vpos[1]: #sotto
                    movetoy += self.speed
                elif self.fut_vpos[0] > self.vpos[0]: #destra
                    movetox += self.speed
                elif self.fut_vpos[0] < self.vpos[0]: #sinistra
                    movetox -= self.speed
                elif self.fut_vpos[1] < self.vpos[1]: #sotto
                    movetoy -= self.speed
                self.rect = self.rect.move((movetox,movetoy))
                
        pygame.event.pump()
        

def PlayerSprite (core, vpos):
    return AnimatedSprite(core, vpos, "sprites/player/red/animplayer.gif")