#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from upsonic import Upsonic, Upsonic_Remote, HASHES, console
from rich.progress import track
import copy

class Upsonic_Update:
    def __init__(self, cloud) -> None:
        self.cloud = cloud
        self.pre_update_dict = {}
    def pre_update(self, key):
        backup = copy.copy(self.cloud.force_encrypt)
        self.cloud.force_encrypt = None
        self.pre_update_dict[key] = self.cloud.get(key, encryption_key=None)
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
            console.log(f" {key}: [bold red]Failure")

        console.log("")
        if len(error) != 0:
            console.log("[bold red] Updating Complated With Error")
            console.log("") if not just_important else None
            return False
        else:
            console.log("[bold green] Updating Complated Without any Error")
            console.log("") if not just_important else None
            return True
        
