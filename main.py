
import math
import sys
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
from kivy.config import Config
from kivy.core.window import Window
from pidev.kivy import DPEAButton
from pidev.kivy import PauseScreen
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
from kivy.properties import ObjectProperty

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=50, speed=10)

s1 = stepper(port=1, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=2)

class MyApp(App):

    def build(self):
        self.title = "Robotic Arm"
        return sm


Builder.load_file('main.kv')
Window.clearcolor = (.1, .1, .1, 1)  # (WHITE)

cyprus.open_spi()

# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////

sm = ScreenManager()

class MainScreen(Screen):
    version = cyprus.read_firmware_version()
    #Slider.value = 0
    lastClick = time.clock()
    #Slider.value = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # self.initialize()

    def wiggle(self):
        s1.home(1)
        s1.start_relative_move(-3)

        s0.relative_move(-1)
        s0.relative_move(1)
        s0.relative_move(-2)
        s0.relative_move(2)
        s0.relative_move(-3)
        s0.relative_move(3)

    # if s0.get_position_in_units > 3.0 & s0.get_position_in_units < 112.0:
    def test_sticking(self):
        s0.get_position_in_units()
        x = s0.get_position_in_units
        if x > 3.0:
            if x < 112.0:
                self.wiggle()

        s0.home(1)
        s0.go_to_position(-28)
        self.wiggle()
        s0.go_to_position(-56)
        self.wiggle()
        s0.go_to_position(-84)
        self.wiggle()
        s0.go_to_position(-112)
        sleep(0.5)
        s0.go_to_position(-84)
        self.wiggle()
        s0.go_to_position(-56)
        self.wiggle()
        s0.go_to_position(-28)
        self.wiggle()
        s0.home(1)




sm.add_widget(MainScreen(name='main'))

# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
cyprus.close_spi()