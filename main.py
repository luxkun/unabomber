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

import menu
import playground

class Core:
    running = True
    pause = False
    menu_mode = True
    def_res = (1280,1024)
    FPS = 90
    def __init__ (self, res):
        self.res = res
        if not self.res:
            self.res = self.def_res
        self.xscale = self.res[0]/self.def_res[0]
        self.yscale = self.res[1]/self.def_res[1]
        self.scale = min(self.xscale, self.yscale)
        
        pygame.init()

        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("UnaBomber v1")
        
        self.menu = menu.Core(self, self.res, self.scale)

        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    def redraw (self):
        self.screen.blit(self.background, self.background.get_rect())
    def clear (self, rects):
        for rect in rects:
            if not isinstance(rect, pygame.rect.Rect):
                rect = pygame.rect.Rect(rect[1], rect[1])
            self.screen.blit(self.background, rect, rect)
            
    def OnMenu (self, diff_level, level=0):
        self.diff_level = (diff_level, ("hard", "medium", "easy")[diff_level])
        self.menu_mode = False
        self.StartLevel(level)
        
    def StartLevel (self, level):
        self.playground = playground.Core(self, self.res, self.scale)
        
    def run (self):
        update_text = True
        self.background = pygame.transform.scale(pygame.image.load("pixmaps/background.png").convert_alpha(), self.res)
        self.redraw()
        pygame.display.flip()
        while self.running == True:
            #self.fps = int(self.clock.get_fps())
            if self.menu_mode:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                            continue
                        self.menu.OnKeyDown(event)
                self.menu.update()
                self.clear(self.menu.rects)
                self.menu.draw(self.screen)
            
            else:
                if not self.pause:
                    self.clear(self.playground.GetRects())
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                            continue
                        self.playground.OnKeyDown(event)
                    elif event.type == pygame.KEYUP:
                        self.playground.OnKeyUp(event)
                    elif (event.type == pygame.USEREVENT) and (not self.pause):
                        self.playground.OnDelayEvent(event)
                if not self.pause:
                    self.playground.Updates()
                    if update_text:
                        #update_text
                        pass
                        
                    self.playground.Draws()
                    pass
                
            pygame.display.flip()
            self.clock.tick(self.FPS)