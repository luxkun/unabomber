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
    placed = False
    vpos = None
    def __init__(self, core, image):
        pygame.sprite.Sprite.__init__(self)
        self.core = core
        self.speed = 5*self.core.scale
        
        self.delay, self.frames = load_gif(image, self.core.xscale,self.core.yscale)
        self.frames = load_gif(image)[1]
        self.sprite = pygame.sprite.RenderPlain(self)

    def DirectMove (self, vpos):
        self.vpos = vpos
        self.rect = self.rect.fit(self.core.rects[vpos][1])
        
    def Place (self, vpos):
        self.placed = True
        self.frame = 0
        self.image = self.frames[0]
        
        self.rect = self.image.get_rect()
        self.DirectMove(vpos)
        self.clock = pygame.time.Clock()
        self.time = 0
    
    def Explode (self):
        ################
        self.placed = False
    
    def update (self):
        if not self.placed:
            return
        
        self.time += self.clock.tick()
        if self.time >= self.delay:
            self.time = 0
            self.frame += 1
            if self.frame >= len(self.frames):
                self.Explode()
                return
            self.image = self.frames[self.frame]
            self.rect = self.image.get_rect().move(self.rect.topleft)
            self.colorkey = self.image.get_at((0,self.image.get_height()-1))
            self.image.set_colorkey(self.colorkey)
        pygame.event.pump()
        

def BombSprite (core):
    return AnimatedSprite(core, "sprites/bombs/animbomb.gif")