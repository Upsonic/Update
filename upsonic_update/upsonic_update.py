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
        self.pre_update_count = 0
        self.clear_olds = clear_olds

        if pre_update_all:
            self.pre_update_all()
    def pre_update(self, key):
        backup = copy.copy(self.cloud.force_encrypt)
        self.cloud.force_encrypt = None
        self.pre_update_dict[key] = self.cloud.get(key, encryption_key=None)
        self.pre_update_count = len(self.cloud.get_all())
        self.cloud.force_encrypt = backup
        self.start_time = time.time()


    def pre_update_all(self):
        backup = copy.copy(self.cloud.force_encrypt)
        self.cloud.force_encrypt = None
        for key in self.cloud.get_all():
            if "_upsonic_" not in key:
                self.pre_update_dict[key] = self.cloud.get(key, encryption_key=None)
        self.pre_update_count = len(self.cloud.get_all())                
        self.cloud.force_encrypt = backup
        self.start_time = time.time()


    def update(self, just_important:bool=False) -> bool:
        console.log("") if not just_important else None
        console.log("[bold green] Update Started")if not just_important else None
        console.log("")if not just_important else None
        the_update_list = str(list(self.pre_update_dict))
        console.log(f"[bold white] Updating: {the_update_list}")
        error = []
        backup = copy.copy(self.cloud.force_encrypt)
        self.cloud.force_encrypt = None

        if self.pre_update_count != len(self.cloud.get_all()):
            console.log("") if not just_important else None
            console.log("[bold green] New Keys Found")

        for key in track(self.pre_update_dict, description="           ", console=console):
            result = False
            currently = self.pre_update_dict[key]
            new = new = self.cloud.get(key, encryption_key=None)


            if currently != new:
                result = True
            
            
            if not result:
                error.append(key)
        self.cloud.force_encrypt = backup
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
        
