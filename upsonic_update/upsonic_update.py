#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from upsonic import console
from rich.progress import track
import copy

class Upsonic_Update:
    def __init__(self, cloud, pre_update_all=False, clear_olds=False) -> None:
        self.cloud = cloud
        self.pre_update_dict = {}
        self.pre_update_get_all = 0
        self.clear_olds = clear_olds

        if pre_update_all:
            self.pre_update_all()
    def pre_update(self, *key):
        backup = copy.copy(self.cloud.force_encrypt)
        backup_2 = copy.copy(self.cloud.cache)
        self.cloud.cache = False
        self.cloud.force_encrypt = None
        console.log(f"[bold white] Preparing to Update:")
    
        if type(key[0]) == tuple:
            key = key[0]

        for _key in track(key, description="           ", console=console):
            self.pre_update_dict[_key] = self.cloud.get(_key, encryption_key=None)
        self.pre_update_get_all = (self.cloud.get_all())
        self.cloud.force_encrypt = backup
        self.cloud.cache = backup_2
        self.start_time = time.time()





    def pre_update_all(self):
        backup = copy.copy(self.cloud.force_encrypt)
        backup_2 = copy.copy(self.cloud.cache)
        self.cloud.cache = False
        self.cloud.force_encrypt = None
        console.log(f"[bold white] Preparing to Update:")
        for key in track(self.cloud.get_all(), description="           ", console=console):
            if "_upsonic_" not in key:
                self.pre_update_dict[key] = self.cloud.get(key, encryption_key=None)
        self.pre_update_get_all = (self.cloud.get_all())                
        self.cloud.force_encrypt = backup
        self.cloud.cache = backup_2
        self.start_time = time.time()


    def update(self, just_important:bool=False) -> bool:
        console.log("") if not just_important else None
        console.log("[bold green] Update Started")if not just_important else None
        console.log("")if not just_important else None
        the_update_list = str(list(self.pre_update_dict))
        console.log(f"[bold white] Updating: {the_update_list}")
        error = []
        backup = copy.copy(self.cloud.force_encrypt)
        backup_2 = copy.copy(self.cloud.cache)
        self.cloud.cache = False
        self.cloud.force_encrypt = None
        new_get_all = self.cloud.get_all()
        if len(self.pre_update_get_all) != len(new_get_all):
            console.log("") if not just_important else None
            console.log("[bold green] New Keys Found")
            #print the new keys
            for key in new_get_all:
                if key not in self.pre_update_get_all:
                    console.log(f" {key}: [bold green]New Key")

        for key in track(self.pre_update_dict, description="           ", console=console):
            result = False
            currently = self.pre_update_dict[key]
            new = new = self.cloud.get(key, encryption_key=None)


            if currently != new:
                result = True
            
            
            if not result:
                error.append(key)
        self.cloud.force_encrypt = backup
        self.cloud.cache = backup_2        
        end_time = time.time()
        took_time = int(end_time - self.start_time)
        console.log(f" Update took {took_time}s")

        for key in error:
            the_error_message = f" {key}: [bold red]Failure"
            if self.clear_olds:
                self.cloud.delete(key)
                the_error_message += " [bold green]Cleared"
            console.log(the_error_message)

        console.log("")
        if len(error) != 0:
            console.log("[bold red] Updating Complated With Error")
            console.log("") if not just_important else None
            return False
        else:
            console.log("[bold green] Updating Complated Without any Error")
            console.log("") if not just_important else None
            return True
        
