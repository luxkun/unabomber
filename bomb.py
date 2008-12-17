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
    def __init__(self, core, image):
        pygame.sprite.Sprite.__init__(self)
        self.core = core
        self.speed = 5*self.core.scale
        
        self.delay, self.frames = load_gif(image, self.core.xscale,self.core.yscale)
        self.frames = load_gif(image)[1]
        self.sprite = pygame.sprite.RenderPlain(self)
        
    def GetPos (self, rect=None):
        if self.placed:
            if not rect:
                rect = self.rect
            a,b = rect.topleft,rect.bottomright
            x = ((b[0]-a[0])/2)+a[0]
            y = ((b[1]-a[1])/2)+a[1]
            print x,y, a,b
            return x,y
    def GetVirtualPos (self, rect=None):
        if self.placed:
            return self.core.pixel2vpos(*self.GetPos(rect))

    def Place (self, x,y):
        self.placed = True
        self.moveto = [0,0]
        self.frame = 0
        self.image = self.frames[0]
        
        self.rect = self.image.get_rect()
        x -= (self.rect.topright[0]/2)
        y -= (self.rect.bottomright[1]/2)
        self.rect = self.rect.move((x,y))
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
        if any(self.moveto):
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
                if all(map(lambda p: self.core.playingarea.collidepoint(p), collidepoints)):
                    self.rect = newrect
        pygame.event.pump()
        

def BombSprite (core):
    return AnimatedSprite(core, "sprites/bombs/animbomb.gif")