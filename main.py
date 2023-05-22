import sys
import os
import  time, random

import linsimpy

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font

tse = None

env_count = 0
user_count = 0
device_count = 0

def create_env(ts):
    messages = []
    users = []
    devices = []

    global env_count
    env_count += 1
    env_name = "amb" + str(env_count)
    ts.out(("AMBIENTE", env_name, tuple(messages)))
    ts.out(("AMB_USUARIOS", env_name, tuple(users)))
    ts.out(("AMB_DISPOSITIVOS", env_name, tuple(devices)))


    envs = ts.inp(("AMBIENTES", object))
    temp = list(envs[1])
    temp.append(env_name)
    ts.out(("AMBIENTES", tuple(temp)))

def create_user(ts):
    enviroment = ""

    global user_count
    user_count += 1
    user_name = "user" + str(user_count)

    users = list(ts.inp(("USUARIOS", object))[1])
    users.append(user_name)
    ts.out(("USUARIOS", tuple(users)))

def create_device(ts):
    enviroment = ""

    global device_count
    device_count += 1
    device_name = "disp" + str(device_count)

    devices = list(ts.inp(("DISPOSITIVOS", object))[1])
    devices.append(device_name)
    ts.out(("DISPOSITIVOS", tuple(devices)))

def delete_empty_envs(ts):
    all_envs = list(ts.inp(("AMBIENTES", object))[1])
    empty_envs = []

    for env in all_envs:
        env_users = list_env_users(ts, env)
        env_devices = list_env_devices(ts, env)
        print(env)
        print(env_users)
        print(env_devices)
        if env_users == [] and env_devices == []:
            empty_envs.append(env)

    for env in empty_envs:
        all_envs.remove(env)
    ts.out(("AMBIENTES", tuple(all_envs)))

def move_user_to_env(ts, user_name, old_env_name, new_env_name):
    if old_env_name != "":
        old_env_users = list_env_users(ts, old_env_name)
        if user_name in old_env_users:
            env_users = list(ts.inp(("AMB_USUARIOS", old_env_name, object))[2])
            env_users.remove(user_name)
            ts.out(("AMB_USUARIOS", old_env_name, tuple(env_users)))
    
    new_env_users = list_env_users(ts, new_env_name)
    if user_name not in new_env_users:
        env_users = list(ts.inp(("AMB_USUARIOS", new_env_name, object))[2])
        env_users.append(user_name)
        ts.out(("AMB_USUARIOS", new_env_name, tuple(env_users)))
        

def move_device_to_env(ts, device_name, old_env_name, new_env_name):
    if old_env_name != "":
        old_env_devices = list_env_devices(ts, old_env_name)
        if device_name in old_env_devices:
            env_devices = list(ts.inp(("AMB_DISPOSITIVOS", old_env_name, object))[2])
            env_devices.append(device_name)
            ts.out(("AMB_DISPOSITIVOS", old_env_name, tuple(env_devices)))
    
    new_env_devices = list_env_devices(ts, new_env_name)
    if device_name not in new_env_devices:
        env_devices = list(ts.inp(("AMB_DISPOSITIVOS", new_env_name, object))[2])
        env_devices.append(device_name)
        ts.out(("AMB_DISPOSITIVOS", new_env_name, tuple(env_devices)))

def send_messages(ts, env_name, user_name, mensagem):
    messages = list(ts.inp(("AMBIENTE", env_name, object))[2])
    messages.append("[" + user_name + "]:" + mensagem)
    ts.out(("AMBIENTE", env_name, tuple(messages)))

def read_messages(ts, env_name):
    return list(ts.rdp(("AMBIENTE", env_name, object))[2])

def list_envs(ts):
    return list(ts.rdp(("AMBIENTES", object))[1])

def list_env_users(ts, name):
    return list(ts.rdp(("AMB_USUARIOS", name, object))[2])

def list_env_devices(ts, name):
    return list(ts.rdp(("AMB_DISPOSITIVOS", name, object))[2])

def list_users(ts):
    return list(ts.rdp(("USUARIOS", object))[1])

def list_devices(ts):
    return list(ts.rdp(("DISPOSITIVOS", object))[1])

if __name__ == "__main__":
    tse = linsimpy.TupleSpaceEnvironment()

    envs = []
    users = []
    devices = []
    tse.out(("AMBIENTES", tuple(envs)))
    tse.out(("USUARIOS", tuple(users)))
    tse.out(("DISPOSITIVOS", tuple(devices)))


    create_env(tse)
    create_env(tse)
    create_env(tse)
    create_user(tse)
    create_user(tse)
    create_user(tse)
    create_device(tse)
    create_device(tse)
    create_device(tse)


    print(list_envs(tse))
    print(list_users(tse))
    print(list_devices(tse))

    move_user_to_env(tse, "user2", "", "amb2")
    move_user_to_env(tse, "user1", "", "amb2")
    move_user_to_env(tse, "user1", "amb2", "amb1")
    move_device_to_env(tse, "disp1", "", "amb1")

    delete_empty_envs(tse)

    print(list_envs(tse))

    send_messages(tse, "amb1", "user1", "teste")
    send_messages(tse, "amb2", "user2", "teste2")

    print(read_messages(tse, "amb1"))
    print(read_messages(tse, "amb2"))