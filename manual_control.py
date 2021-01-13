#!/usr/bin/env python3

import time
import argparse
import numpy as np
import gym
import gym_minigrid
from gym_minigrid.wrappers import *
from gym_minigrid.window import Window
import random

def redraw(img):
    if not args.agent_view:
        img = env.render('rgb_array', tile_size=args.tile_size)

    window.show_img(img)

def observe():
    grid, _ = env.gen_obs_grid()
    return grid

def skill_get_key():
    # first need to explore and see where the key is
    grid = observe()
    while ('yellow', 'key') not in grid:
        move_action_list = [env.actions.left, env.actions.right, env.actions.forward]
        action = random.choice(move_action_list)
        print(action)
        step(action)
        grid = observe()
    # then go to the key
    idx = grid.where_is(('yellow', 'key'))
    while idx < 42 and idx != 38:
        step(env.actions.forward)
        grid = observe()
        idx = grid.where_is(('yellow', 'key'))
    if idx == 38:
        pass
    elif idx < 45:
        step(env.actions.left)
        grid = observe()
        idx = grid.where_is(('yellow', 'key'))
        while idx != 38:
            step(env.actions.forward)
            grid = observe()
            idx = grid.where_is(('yellow', 'key'))
    elif idx > 45:
        step(env.actions.right)
        grid = observe()
        idx = grid.where_is(('yellow', 'key'))
        while idx != 38:
            step(env.actions.forward)
            grid = observe()
            idx = grid.where_is(('yellow', 'key'))
    step(env.actions.pickup)

def skill_open_door():
    # first need to explore and see where the door is
    grid = observe()
    while ('yellow', 'door') not in grid:
        move_action_list = [env.actions.left, env.actions.right, env.actions.forward]
        action = random.choice(move_action_list)
        print(action)
        step(action)
        grid = observe()
    # then go to the door
    idx = grid.where_is(('yellow', 'door'))
    while idx < 42 and idx != 38:
        if grid.get(3,5) and grid.get(3,5).type == 'wall':
            if idx < 45:
                step(env.actions.left)
            else:
                step(env.actions.right)
            grid = observe()
            idx = grid.where_is(('yellow', 'door'))
            print(idx)
            continue
        step(env.actions.forward)
        grid = observe()
        idx = grid.where_is(('yellow', 'door'))
        print(idx)
    if idx == 38:
        pass
    elif idx < 45:
        step(env.actions.left)
        grid = observe()
        idx = grid.where_is(('yellow', 'door'))
        while idx != 38:
            step(env.actions.forward)
            grid = observe()
            idx = grid.where_is(('yellow', 'door'))
    elif idx > 45:
        step(env.actions.right)
        grid = observe()
        idx = grid.where_is(('yellow', 'door'))
        while idx != 38:
            step(env.actions.forward)
            grid = observe()
            idx = grid.where_is(('yellow', 'door'))
    step(env.actions.toggle)


def skill_cross_door():
    step(env.actions.forward)
    step(env.actions.forward)

def skill_goal():
    # first need to explore and see where the goal is
    grid = observe()
    while ('green', 'goal') not in grid:
        move_action_list = [env.actions.left, env.actions.right, env.actions.forward]
        action = random.choice(move_action_list)
        print(action)
        step(action)
        grid = observe()
    # then go to the goal
    idx = grid.where_is(('green', 'goal'))
    while idx < 42 and idx != 38:
        step(env.actions.forward)
        grid = observe()
        idx = grid.where_is(('green', 'goal'))
    if idx == 38:
        pass
    elif idx < 45:
        step(env.actions.left)
        grid = observe()
        idx = grid.where_is(('green', 'goal'))
        while idx != 38:
            step(env.actions.forward)
            grid = observe()
            idx = grid.where_is(('green', 'goal'))
    elif idx > 45:
        step(env.actions.right)
        grid = observe()
        idx = grid.where_is(('green', 'goal'))
        while idx != 38:
            step(env.actions.forward)
            grid = observe()
            idx = grid.where_is(('green', 'goal'))
    step(env.actions.forward)

def obs():
    grid = observe()
    grid_2d = np.array(grid.grid).reshape(grid.width, grid.height)

def reset():
    if args.seed != -1:
        env.seed(args.seed)

    obs = env.reset()

    if hasattr(env, 'mission'):
        print('Mission: %s' % env.mission)
        window.set_caption(env.mission)

    redraw(obs)

def step(action):
    obs, reward, done, info = env.step(action)
    print('step=%s, reward=%.2f' % (env.step_count, reward))

    if done:
        print('done!')
        reset()
    else:
        redraw(obs)

def key_handler(event):
    print('pressed', event.key)
    if event.key == 'i':
        print('inspecting')
        obs()
        return

    if event.key == '1':
        print('finding key')
        skill_get_key()
        return
    
    if event.key == '2':
        print('opening the door')
        skill_open_door()
        return

    if event.key == '3':
        print('crossing the door')
        skill_cross_door()
        return

    if event.key == '4':
        print('goal')
        skill_goal()
        return

    if event.key == 'escape':
        window.close()
        return

    if event.key == 'backspace':
        reset()
        return

    if event.key == 'left':
        step(env.actions.left)
        return
    if event.key == 'right':
        step(env.actions.right)
        return
    if event.key == 'up':
        step(env.actions.forward)
        return

    # Spacebar
    if event.key == ' ':
        step(env.actions.toggle)
        return
    if event.key == 'pageup':
        step(env.actions.pickup)
        return
    if event.key == 'pagedown':
        step(env.actions.drop)
        return

    if event.key == 'enter':
        step(env.actions.done)
        return

parser = argparse.ArgumentParser()
parser.add_argument(
    "--env",
    help="gym environment to load",
    default='MiniGrid-DoorKey-8x8-v0'
)
parser.add_argument(
    "--seed",
    type=int,
    help="random seed to generate the environment with",
    default=-1
)
parser.add_argument(
    "--tile_size",
    type=int,
    help="size at which to render tiles",
    default=32
)
parser.add_argument(
    '--agent_view',
    default=False,
    help="draw the agent sees (partially observable view)",
    action='store_true'
)

args = parser.parse_args()

env = gym.make(args.env)

if args.agent_view:
    env = RGBImgPartialObsWrapper(env)
    env = ImgObsWrapper(env)

window = Window('gym_minigrid - ' + args.env)
window.reg_key_handler(key_handler)

reset()

# Blocking event loop
window.show(block=True)
