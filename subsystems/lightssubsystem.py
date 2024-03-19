from enum import Enum, auto

import commands2
from wpilib import SmartDashboard
import phoenix5.led
import constants


class AnimationTypes(Enum):
    ColorFlow = 1,
    Fire = 2,
    Larson = 3,
    Rainbow = 4,
    RgbFade = 5,
    SingleFade = 6,
    Strobe = 7,
    Twinkle = 8,
    TwinkleOff = 9,
    SetAll = 10,


class Colors(Enum):
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Lime = (0, 255, 0)
    Blue = (0, 0, 255)
    Yellow = (255, 255, 0)
    Cyan = (0, 255, 255)
    Magenta = (255, 0, 255)
    Silver = (192, 192, 192)
    Gray = (128, 128, 128)
    Maroon = (128, 0, 0)
    Olive = (128, 128, 0)
    Green = (0, 128, 0)
    Purple = (128, 0, 128)
    Teal = (0, 128, 128)
    Navy = (0, 0, 128)
    Orange = (255, 165, 0)


class LightsSubsystem(commands2.Subsystem):
    candle = phoenix5.led.CANdle(constants.CANDLE_PORT)
    led_count = 300
    to_animate: phoenix5.led.Animation
    current_animation: AnimationTypes
    current_color: Colors

    class LightState(Enum):
        Prematch = auto()
        NoNote = auto()
        NoteInIntake = auto()
        ShooterUpToSpeed = auto()
        Celebrate = auto()
        Off = auto()

    def __init__(self):
        super().__init__()
        self.current_color = Colors.Blue
        self.change_animation(AnimationTypes.SetAll)
        config_all = phoenix5.led.CANdleConfiguration()
        config_all.statusLedOffWhenActive = True
        config_all.disableWhenLOS = False
        config_all.stripType = phoenix5.led.LEDStripType.GRB
        config_all.brightnessScalar = 0.1
        config_all.vBatOutputMode = phoenix5.led.VBatOutputMode.Modulated
        self.candle.configAllSettings(config_all, 100)
        self.set_colors(Colors.Red)

        self.state = self.LightState.Prematch
        SmartDashboard.putString("Light State:", str(self.state))

    def set_colors(self, color: Colors) -> None:
        self.change_animation(AnimationTypes.SetAll)
        self.current_color = color

    def config_brightness(self, percent: float) -> None:
        self.candle.configBrightnessScalar(percent, 0)

    def config_los(self, disable_when_los: bool) -> None:
        self.candle.configLOSBehavior(self, disable_when_los, 0)

    def config_led_type(self, type: phoenix5.led.LEDStripType) -> None:
        self.candle.configLEDType(type, 0)

    def config_status_led_behavior(self, off_when_active: bool) -> None:
        self.candle.configStatusLedState(off_when_active, 0)

    def change_animation(self, to_change: AnimationTypes) -> None:
        self.current_animation = to_change

        if to_change == AnimationTypes.ColorFlow:
            self.to_animate = phoenix5.led.ColorFlowAnimation(128, 20, 70, 0, 0.7, self.led_count,
                                                              phoenix5.led.ColorFlowAnimation.Direction.Forward)
        elif to_change == AnimationTypes.Fire:
            self.to_animate = phoenix5.led.FireAnimation(0.5, 0.7, self.led_count, 0.7, 0.5)
        elif to_change == AnimationTypes.Larson:
            self.to_animate = phoenix5.led.LarsonAnimation(0, 255, 46, 0, 1, self.led_count,
                                                           phoenix5.led.LarsonAnimation.BounceMode.Front, 3)
        elif to_change == AnimationTypes.Rainbow:
            self.to_animate = phoenix5.led.RainbowAnimation(1, 0.9, self.led_count)
        elif to_change == AnimationTypes.RgbFade:
            self.to_animate = phoenix5.led.RgbFadeAnimation(0.7, 0.4, self.led_count)
        elif to_change == AnimationTypes.SingleFade:
            self.to_animate = phoenix5.led.SingleFadeAnimation(50, 2, 200, 0, 0.5, self.led_count);
        elif to_change == AnimationTypes.Strobe:
            self.to_animate = phoenix5.led.StrobeAnimation(240, 10, 180, 0, 98.0 / 256.0, self.led_count);
        elif to_change == AnimationTypes.Twinkle:
            self.to_animate = phoenix5.led.TwinkleAnimation(30, 70, 60, 0, 0.8, self.led_count,
                                                            phoenix5.led.TwinkleAnimation.TwinklePercent.Percent6);
        elif to_change == AnimationTypes.TwinkleOff:
            self.to_animate = phoenix5.led.TwinkleOffAnimation(70, 90, 175, 0, 0.8, self.led_count,
                                                               phoenix5.led.TwinkleOffAnimation.TwinkleOffPercent.Percent100);
        else:
            self.to_animate = None

    def periodic(self) -> None:
        if self.state == self.LightState.Prematch:
            self.change_animation(AnimationTypes.Rainbow)
        elif self.state == self.LightState.NoNote:
            self.change_animation(AnimationTypes.SetAll)
            self.set_colors(Colors.Blue)
        elif self.state == self.LightState.NoteInIntake:
            self.change_animation(AnimationTypes.SetAll)
            self.set_colors(Colors.Orange)
        elif self.state == self.LightState.Celebrate:
            self.change_animation(AnimationTypes.Twinkle)
        elif self.state == self.LightState.ShooterUpToSpeed:
            self.change_animation(AnimationTypes.SetAll)
            self.set_colors(Colors.Lime)
        elif self.state == self.LightState.Off:
            self.change_animation(AnimationTypes.SetAll)
            self.set_colors(Colors.Black)
        else:
            self.change_animation(AnimationTypes.SetAll)
            self.set_colors(Colors.Black)

    def set_lights_prematch(self):
        self.state = self.LightState.Prematch

    def set_lights_no_note(self):
        self.state = self.LightState.NoNote

    def set_lights_note_in_intake(self):
        self.state = self.LightState.NoteInIntake

    def set_lights_celebrate(self):
        self.state = self.LightState.Celebrate

    def set_lights_shooter_up_to_speed(self):
        self.state = self.LightState.ShooterUpToSpeed

    def set_lights_off(self):
        self.state = self.LightState.Off

    def simulationPeriodic(self) -> None:
        pass
