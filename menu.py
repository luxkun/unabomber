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

class Core:
    color = (0,0,0)
    selected_color = (255,255,255)
    running = True
    def __init__ (self, core, res, scale):
        self.core = core
        self.sx = res[0]/2.2
        self.sy = res[1]/3
        
        self.selected = -1
        self.choices = 2
        self.text = "New\nLoad\nQuit"
        self.mode = 0
        
        self.font = pygame.font.Font("freesansbold.ttf", int(36*scale))
        self.line_size = self.font.get_linesize()
    
    def OnKeyDown (self, event):
        if (event.key == pygame.K_DOWN) and (self.selected != self.choices):
            self.selected += 1
        elif (event.key == pygame.K_UP) and (self.selected > 0):
            self.selected -= 1
        elif event.key == pygame.K_RETURN:
            if self.mode == 0:
                if self.selected == 0:
                    self.core.redraw()
                    self.text = "HARD\nMEDIUM\nEASY"
                    self.selected = 0
                    self.choices = 2
                    self.mode = 1
                elif self.selected == 1:
                    pass
                elif self.selected == 2:
                    self.core.running = False
            elif self.mode == 1:
                self.core.OnMenu(self.selected)
                self.running = False
                self.core.redraw()
            
            
        
    def update (self):        
        self.rects = []
        for count,line in enumerate(self.text.splitlines()):
            if not line: continue
            if count == self.selected:
                color = self.selected_color
            else:
                color = self.color
            txt = self.font.render(line, 1, color)
            self.rects.append([txt, [self.sx,self.sy+(count*self.line_size)]])
        self.rect = pygame.rect.Rect(self.rects[0][1]+self.rects[-1][1])
    
    def draw (self, screen):
        if self.running:
            for rect in self.rects:
                screen.blit(*rect)