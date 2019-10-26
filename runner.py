import os
import subprocess

IMAGE_FOLDER = "images"
INT_MAX = 2147483648

class Runner(object):
    def __init__(self, desired, size_multiplier = 1, open_on_save=False):
        self.width = 540 * size_multiplier
        self.height = 480 * size_multiplier
        self.desired = desired
        self.file_number = None
        self.current_run = 1
        self.saved_file_numbers = []
        self.open_on_save = open_on_save
        self.random_seeds = []
        self.noise_seeds = []

    def refresh(self):
        background(color(0, 0, 100, 0))
        self.set_seeds()

    def get_random_int(self):
        return int(random(-1 * INT_MAX, INT_MAX))

    def set_seeds(self):
        random_seed = self.get_random_int()
        self.random_seeds.append(random_seed)

        noise_seed = self.get_random_int()
        self.noise_seeds.append(noise_seed)

        randomSeed(random_seed)
        noiseSeed(noise_seed)

    def setup(self):
        colorMode(HSB, 360, 100, 100, 1.0)

    @staticmethod
    def get_cwd():
        return sketchPath("") + '/'

    def count_files(self):
        dir_list = os.listdir(self.get_cwd() + IMAGE_FOLDER)
        return len(dir_list)
            
    def get_padded_number(self, i, power = 3):
        string_i = "{}".format(i)
        
        if i < 10**(power):
            while len(string_i) < (power + 1):
                string_i = '0' + string_i
                
        return string_i

    def get_image_name(self, padded_number):
        return "{}/{}.png".format(IMAGE_FOLDER, padded_number)

    def commit_changes(self):
        runner_path = os.path.dirname(__file__)
        script_path = "{}/handle_commit.sh".format(runner_path)
        pluralization = '' if self.desired == 1 else 's'
        commit_message = "{} file{} generated".format(self.desired, pluralization)

        if self.desired == 1:
            commit_message += ", {}".format(self.saved_file_numbers[0])
        elif self.desired > 0:
            commit_message += ", from {} to {}".format(self.saved_file_numbers[0], self.saved_file_numbers[-1])
        subprocess.call([script_path, commit_message])

    def open_files(self):
        command = 'open'
        for file_number in self.saved_file_numbers:
            file_name = self.get_image_name(file_number)
            command += ' {}'.format(file_name)

        os.system(command)

    def make_directories(self):
        if self.current_run == 1:
            has_directory = os.path.exists(self.get_cwd() + IMAGE_FOLDER)
            if not has_directory:
                os.mkdir(IMAGE_FOLDER)

    def save_seeds(self):
        has_associated_image = self.desired > 0

        with open('seeds.txt', 'w') as file:
            for i in range(len(self.random_seeds)):
                random_seed = self.random_seeds[i]
                noise_seed = self.noise_seeds[i]

                if has_associated_image:
                    image_text = 'IMAGE {}'.format(self.saved_file_numbers[i])
                else:
                    image_text = 'RUN {}'.format(i)

                file.write('# {}\n'.format(image_text))
                file.write('RANDOM : {}\n'.format(random_seed))
                file.write('NOISE : {}\n\n'.format(noise_seed))

    def save_image(self):
        padded_number = self.get_padded_number(self.file_number + self.current_run) 
        self.saved_file_numbers.append(padded_number)
        saveFrame(self.get_image_name(padded_number))

    def handle_save(self):
        self.make_directories()

        if self.file_number is None:
            self.file_number = self.count_files()
        
        # save the image
        if self.desired > 0:
            self.save_image()
            self.current_run += 1
        
        # stop drawing
        if self.current_run > self.desired:
            noLoop()
            self.save_seeds()
            self.commit_changes()

            if self.open_on_save:
                self.open_files()

            exit()
