import os

# TODO - make an images directory if it doesn't exist
# Useful to set up a saving infrastructure
# (saving the seed, code, and photos)

class Runner(object):
    def __init__(self, desired):
        self.desired = desired
        self.file_number = None
        self.current_run = 1
        
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
    
    def handle_save(self):
        # Because sketchPath("") returns /Applications/ when outside draw() function
        if self.file_number is None:
            self.file_number = self.count_files()
        
        # save the file
        if self.desired > 0:
            padded_number = self.get_padded_number(self.file_number + self.current_run) 
            saveFrame("images/try-{}.png".format(padded_number))
            self.current_run += 1
        
        # stop drawing
        if self.current_run > self.desired:
            noLoop()

