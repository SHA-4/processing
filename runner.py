import os
import subprocess

# TODO - add separate message if code changed in commit or not
# TODO - save the seed to a file, commit the changes each save
# TODO - make an images directory if it doesn't exist
# TODO - see if I can call size in setup 

# Useful to set up a saving infrastructure
# (saving the seed, code, and photos)

class Runner(object):
    def __init__(self, desired, size_multiplier = 1):
        self.width = 540 * size_multiplier
        self.height = 480 * size_multiplier
        self.desired = desired
        self.file_number = None
        self.current_run = 1

    def setup(self):
        colorMode(HSB, 360, 100, 100, 1.0)
        background(color(0, 0, 100, 0))

    def count_files(self):
        cwd = sketchPath("")
        dir_list = os.listdir(cwd + "images")
        return len(dir_list)
            
    def get_padded_number(self, i, power = 3):
        string_i = "{}".format(i)
        
        if i < 10**(power):
            while len(string_i) < (power + 1):
                string_i = '0' + string_i
                
        return string_i
    
    def commit_changes(self, last_number_saved):
        runner_path = os.path.dirname(__file__)
        script_path = "{}/handle_commit.sh".format(runner_path)
        pluralization = '' if self.desired == 1 else 's'
        commit_message = "{} file{} generated".format(self.desired, pluralization)

        if self.desired == 1:
            commit_message += ", {}".format(last_number_saved)
        elif self.desired > 0:
            commit_message += ", from {} to {}".format(self.get_padded_number(self.file_number + 1), last_number_saved)
        subprocess.call([script_path, commit_message])

    def handle_save(self):
        # Because sketchPath("") returns /Applications/ when outside draw() function
        if self.file_number is None:
            self.file_number = self.count_files()
        
        # save the image
        if self.desired > 0:
            padded_number = self.get_padded_number(self.file_number + self.current_run) 
            saveFrame("images/try-{}.png".format(padded_number))
            self.current_run += 1
        
        # stop drawing
        if self.current_run > self.desired:
            noLoop()
            last_number_saved = padded_number if self.desired > 0 else None
            self.commit_changes(last_number_saved)
