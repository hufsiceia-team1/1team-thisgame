import pygame

#pygame.mixer.pre_init (44100, -16, 1, 2512)
pygame.mixer.init()

# 대기화면에 나오는 효과음
pygame.mixer.music.load ('music/Pacman_Introduction_Music-KP-826387403.wav')

# 게임할 때 나는 효과음
game = pygame.mixer.music.load('music/Challenge_Mode.mp3')

# Life 하나씩 떨어질 때마다 나는 효과음
fall = pygame.mixer.music.load('music/arcade_game_fall_tone_003 (online-audio-converter.com).ogg')

# 게임 끝날 때 나는 효과음
end = pygame.mixer.music.load('music/arcade_game_alarm_long.mp3')

# 2p 잡으면 나는 효과음
win = pygame.mixer.music.load('music/little_robot_sound_factory_Jingle_Win_Synth_05.mp3')

# 카운트다운 효과음
countdown = pygame.mixer.music.load('music/countdown (online-audio-converter.com).ogg')