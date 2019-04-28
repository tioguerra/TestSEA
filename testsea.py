#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import numpy as np

# This is the sinuidal amplitude in degrees
# The sine wave will vary between -AMPLITUDE
# and +AMPLITUDE (a span of 2xAMPLITUDE)
# This is motor goal angle
AMPLITUDE = np.deg2rad(45.0)

# Initial period of the sine wave in seconds
# This will also determine the width of the window
# in seconds
PERIOD = 10.0

# Offset between the two motor goal positions
# in degrees
OFFSET = np.deg2rad(30.0)

# Framerate (frequency)
FPS = 40.0
SAMPLE_PERIOD = 1.0 / FPS

# Graph lookback window in seconds
GRAPH_WINDOW = 1.0
GRAPH_WINDOW_SIZE = int(PERIOD * GRAPH_WINDOW / SAMPLE_PERIOD)

# Screen size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Graph drawing parameters
HEIGHT_SCALE = - float(SCREEN_HEIGHT) / (3*np.pi)
GRAPH_VERT_OFFSET = int(0.75*SCREEN_HEIGHT)
GRAPH_LINE_WIDTH = 1

# Colors
BACKGROUND_COLOR = (64, 64, 64)
GRAPH0_COLOR = (255, 128, 128)
GRAPH1_COLOR = (128, 128, 255)
OFFSET_COLOR = (128, 255, 128)
PERIOD_COLOR = (255, 255, 128)
AMPLITUDE0_COLOR = (255, 160, 160)
AMPLITUDE1_COLOR = (160, 160, 255)
AMPLITUDE_COLOR = (200, 200, 200)
INSTRUCTIONS_COLOR = (0,0,0)

# For the GUI
AMPLITUDE_INCREMENT = np.deg2rad(10.0)
OFFSET_INCREMENT = np.deg2rad(10.0)
PERIOD_INCREMENT = 1.0
LABEL_XOFFSET = -250
LABEL_YOFFSET = -15
ARROW_UP_OFFSET = 100
ARROW_DOWN_OFFSET = 50

class Point:
    # constructed using a normal tupple
    def __init__(self, point_t = (0,0)):
        self.x = float(point_t[0])
        self.y = float(point_t[1])
    # define all useful operators
    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y))
    def __sub__(self, other):
        return Point((self.x - other.x, self.y - other.y))
    def __mul__(self, scalar):
        return Point((self.x*scalar, self.y*scalar))
    def __div__(self, scalar):
        return Point((self.x/scalar, self.y/scalar))
    def __len__(self):
        return int(np.sqrt(self.x**2 + self.y**2))
    # get back values in original tuple format
    def get(self):
        return (self.x, self.y)

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    origin = Point(start_pos)
    target = Point(end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement*(1.0/length)

    for index in range(0, int(length/dash_length), 2):
        start = origin + (slope *    index    * dash_length)
        end   = origin + (slope * (index + 1) * dash_length)
        pygame.draw.line(surf, color, start.get(), end.get(), width)

def draw_arrow(screen, color, start, end):
    pygame.draw.line(screen,color,start,end,2)
    rotation = np.degrees(np.arctan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, color, \
                        ((end[0]+0*np.sin(np.radians(rotation)),
                          end[1]+0*np.cos(np.radians(rotation))),\
                         (end[0]+20*np.sin(np.radians(rotation-150)),\
                          end[1]+20*np.cos(np.radians(rotation-150))),\
                         (end[0]+20*np.sin(np.radians(rotation+150)),\
                          end[1]+20*np.cos(np.radians(rotation+150)))))

def draw_double_arrow(screen, color, start_pos, end_pos):
    start = Point(start_pos)
    end = Point(end_pos)
    middle = start + (end - start) * 0.5
    draw_arrow(screen, color, middle.get(), end.get())
    draw_arrow(screen, color, middle.get(), start.get())

class TestSEA():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.font.init()
        self.myfont = pygame.font.SysFont('ubuntumono', 30)
        self.is_done = False
        self.amplitude = AMPLITUDE
        self.period = PERIOD
        self.offset = OFFSET
        self.clock = pygame.time.Clock()
        self.theta = 0.0
        self.history_out0 = [0.0] * GRAPH_WINDOW_SIZE
        self.history_out1 = [0.0] * GRAPH_WINDOW_SIZE
        self._update()
        self.label_instructions = \
        self.myfont.render('PAGE-UP PAGE-DOWN ARROW-UP ARROW-DOWN ARROW-LEFT ARROW-RIGHT',\
                           False, INSTRUCTIONS_COLOR)
    def step(self):
        if not self.is_done:
            self._update()
            self._handleEvents()
            self._draw()
        self.clock.tick(FPS)
    def _update(self):
        if self.period > 0.0:
            self.theta = self.theta + (2.0*np.pi / self.period) * SAMPLE_PERIOD
        else:
            self.theta = 0.0
        self.out0 = self.amplitude * np.sin(self.theta)
        self.out1 = self.out0 + self.offset
        self.history_out0 = self.history_out0[1:] + [self.out0]
        self.history_out1 = self.history_out1[1:] + [self.out1]
    def _draw(self):
        indexes = [int(x) for x in
                   np.linspace(0.0,GRAPH_WINDOW_SIZE-1,SCREEN_WIDTH)]
        points0 = []
        points1 = []
        for i, index in enumerate(indexes):
            points0.append((i,int(HEIGHT_SCALE*self.history_out0[index]+GRAPH_VERT_OFFSET)))
            points1.append((i,int(HEIGHT_SCALE*self.history_out1[index]+GRAPH_VERT_OFFSET)))
        label_out0 = self.myfont.render('%.0f deg' % np.rad2deg(self.out0), False, GRAPH0_COLOR)
        label_out1 = self.myfont.render('%.0f deg' % np.rad2deg(self.out1), False, GRAPH1_COLOR)
        label_offset = self.myfont.render('Offset: %.0f deg' % \
                                        np.rad2deg(self.out1 - self.out0), False, OFFSET_COLOR)
        label_period = self.myfont.render('Period: %.0f s' % \
                                        self.period, False, PERIOD_COLOR)
        label_amplitude = self.myfont.render('Amplitude: %.0f deg' % \
                                        np.rad2deg(self.amplitude), False, AMPLITUDE_COLOR)
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.lines(self.screen, GRAPH0_COLOR, False, points0, GRAPH_LINE_WIDTH)
        pygame.draw.lines(self.screen, GRAPH1_COLOR, False, points1, GRAPH_LINE_WIDTH)
        self.screen.blit(label_out0, (points0[-1][0] + LABEL_XOFFSET \
                                      - label_out0.get_width(), \
                                      points0[-1][1] + LABEL_YOFFSET))
        self.screen.blit(label_out1, (points1[-1][0] + LABEL_XOFFSET \
                                      - label_out1.get_width(), \
                                      points1[-1][1] + LABEL_YOFFSET))
        self.screen.blit(label_offset, \
                         (points1[-1][0] + int(LABEL_XOFFSET/2.0) \
                          - int(label_offset.get_width()/2.0), \
                          points1[-1][1]-ARROW_UP_OFFSET+2*LABEL_YOFFSET))
        self.screen.blit(label_period, (int(SCREEN_WIDTH/2.0 \
                                        - label_period.get_width()/2.0),100))
        self.screen.blit(label_amplitude, (int(SCREEN_WIDTH/2.0 \
                                        - label_amplitude.get_width()/2.0),
                                           int((self.amplitude + self.offset) * HEIGHT_SCALE \
                                               + GRAPH_VERT_OFFSET) - 60))
        self.screen.blit(self.label_instructions, (0, SCREEN_HEIGHT-30))
        draw_dashed_line(self.screen, GRAPH0_COLOR, (points0[-1][0] \
                                    + LABEL_XOFFSET, points0[-1][1]), points0[-1])
        draw_dashed_line(self.screen, GRAPH1_COLOR, (points1[-1][0] \
                                    + LABEL_XOFFSET, points1[-1][1]), points1[-1])
        draw_arrow(self.screen, OFFSET_COLOR, \
                   (points1[-1][0] + int(LABEL_XOFFSET/2.0), points1[-1][1]-ARROW_UP_OFFSET),
                   (points1[-1][0] + int(LABEL_XOFFSET/2.0), points1[-1][1]))
        draw_arrow(self.screen, OFFSET_COLOR, \
                   (points0[-1][0] + int(LABEL_XOFFSET/2.0), points0[-1][1]+ARROW_DOWN_OFFSET),
                   (points0[-1][0] + int(LABEL_XOFFSET/2.0), points0[-1][1]))
        draw_double_arrow(self.screen, PERIOD_COLOR, \
                   (int(SCREEN_WIDTH / 2.0 - (self.period / PERIOD)*SCREEN_WIDTH/2.0), 85),
                   (int(SCREEN_WIDTH / 2.0 + (self.period / PERIOD)*SCREEN_WIDTH/2.0), 85))
        point0_amplitude0 = (int(SCREEN_WIDTH / 2.0 - 50) , \
                    int(self.amplitude * HEIGHT_SCALE + GRAPH_VERT_OFFSET))
        point1_amplitude0 = (int(SCREEN_WIDTH / 2.0 - 50) , \
                    int(- self.amplitude * HEIGHT_SCALE + GRAPH_VERT_OFFSET))
        point0_amplitude1 = (int(SCREEN_WIDTH / 2.0 + 50) , \
                    int((self.amplitude + self.offset) * HEIGHT_SCALE + GRAPH_VERT_OFFSET))
        point1_amplitude1 = (int(SCREEN_WIDTH / 2.0 + 50) , \
                    int(- (self.amplitude - self.offset) * HEIGHT_SCALE + GRAPH_VERT_OFFSET))

        draw_double_arrow(self.screen, AMPLITUDE0_COLOR, \
                    point0_amplitude0, point1_amplitude0)
        draw_double_arrow(self.screen, AMPLITUDE1_COLOR, \
                    point0_amplitude1, point1_amplitude1)
        draw_dashed_line(self.screen, AMPLITUDE0_COLOR, \
                    (point0_amplitude0[0] - 100, point0_amplitude0[1]),
                    (point0_amplitude0[0] + 100, point0_amplitude0[1]))
        draw_dashed_line(self.screen, AMPLITUDE0_COLOR, \
                    (point1_amplitude0[0] - 100, point1_amplitude0[1]),
                    (point1_amplitude0[0] + 100, point1_amplitude0[1]))
        draw_dashed_line(self.screen, AMPLITUDE1_COLOR, \
                    (point0_amplitude1[0] - 100, point0_amplitude1[1]),
                    (point0_amplitude1[0] + 100, point0_amplitude1[1]))
        draw_dashed_line(self.screen, AMPLITUDE1_COLOR, \
                    (point1_amplitude1[0] - 100, point1_amplitude1[1]),
                    (point1_amplitude1[0] + 100, point1_amplitude1[1]))

        pygame.display.flip()
    def _handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_done = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_PLUS \
                   or event.key == pygame.K_PAGEUP:
                    self.amplitude += AMPLITUDE_INCREMENT
                elif event.key == pygame.K_MINUS \
                   or event.key == pygame.K_PAGEDOWN:
                    self.amplitude -= AMPLITUDE_INCREMENT
                elif event.key == pygame.K_DOWN:
                    if self.offset > 0.0:
                        self.offset -= OFFSET_INCREMENT
                        if self.offset < 0.0:
                            self.offset = 0.0
                elif event.key == pygame.K_UP:
                    self.offset += OFFSET_INCREMENT
                elif event.key == pygame.K_RIGHTBRACKET \
                    or event.key == pygame.K_RIGHT:
                    self.period += PERIOD_INCREMENT
                elif event.key == pygame.K_LEFTBRACKET \
                    or event.key == pygame.K_LEFT:
                    if self.period > 0.0:
                        self.period -= PERIOD_INCREMENT
                        if self.period < 0.0:
                            self.period = 0.0
                elif event.key == pygame.K_ESCAPE:
                    self.is_done = True
ts = TestSEA()
while not ts.is_done:
    ts.step()

