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

import player
import bomb

class Core:
    rects = {}
    def __init__ (self, core, res, xscale,yscale,scale):
        self.core = core
        self.res = res
        self.xscale,self.yscale,self.scale = xscale,yscale,scale
        
        self.CreateRects(20, 13)
        self.Player = player.PlayerSprite(self, (0,0))
        self.Bomb = bomb.BombSprite(self)
        self.player_move = -1
        self.box = pygame.transform.scale(pygame.image.load("sprites/testbox.gif"), (self.xSpaceSize,self.ySpaceSize))
        
        self.playingarea = pygame.Rect([0,0] + list(res))
        
    def CreateRects (self, xspaces, yspaces):
        self.xSpaceSize, self.ySpaceSize = self.res[0]/xspaces, self.res[1]/yspaces
        for xs in xrange(xspaces):
            for ys in xrange(yspaces):
                area = (xs*self.xSpaceSize, ys*self.ySpaceSize, self.xSpaceSize, self.ySpaceSize)
                rect = pygame.Rect(area)
                self.rects[(xs, ys)] = (area, rect)
        
    def pixel2rect (self, x,y):
        for rect in self.rects:
            if rect.collidepoint(x) and rect.collidepoint(y):
                return rect
    def vpos2pixel (self, xs, ys):
        return (xs*self.xSpaceSize+(self.xSpaceSize/2), ys*self.ySpaceSize+(self.ySpaceSize/2))
    def pixel2vpos (self, x, y):
        return (x/self.xSpaceSize, y/self.ySpaceSize)
            
    def GetRects (self):
        rects = [self.Player.rect]
        if self.Bomb.placed:
            rects.append(self.Bomb.rect)
        return rects
    
    def Updates (self):
        if (self.player_move != -1) and (not self.Player.moving):
            if self.player_move == 0:
                self.Player.goDown()
            if self.player_move == 1:
                self.Player.goRight()
            if self.player_move == 2:
                self.Player.goLeft()
            if self.player_move == 3:
                self.Player.goUp()
        elif (self.player_move == -1) and (not self.Player.moving) and (self.Player.frame[1]):
            self.Player.frame[1] = 0
            self.Player.load_frame()
        self.Bomb.update()
        self.Player.update()
    
    def Draws (self):
        for rect in self.rects.values():
            self.core.screen.blit(self.box, rect[1])
        if self.Bomb.placed:
            self.Bomb.sprite.draw(self.core.screen)
        self.Player.sprite.draw(self.core.screen)
            
    def OnKeyDown (self, event):
        key = event.key
        if key == pygame.K_DOWN:
            self.player_move = 0
        elif key == pygame.K_RIGHT:
            self.player_move = 1
        elif key == pygame.K_LEFT:
            self.player_move = 2
        elif key == pygame.K_UP:
            self.player_move = 3
    def OnKeyUp (self, event):
        key = event.key
        if (key == pygame.K_DOWN) and (self.player_move == 0):
            self.player_move = -1
        elif (key == pygame.K_RIGHT) and (self.player_move == 1):
            self.player_move = -1
        elif (key == pygame.K_LEFT) and (self.player_move == 2):
            self.player_move = -1
        elif (key == pygame.K_UP) and (self.player_move == 3):
            self.player_move = -1
        elif key == pygame.K_SPACE:
            if not self.Bomb.placed:
                self.Player.justPlanted = True
                self.Bomb.Place(self.Player.vpos)
    
    def OnDelayEvent (self, event):
        pass
    