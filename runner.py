import os
import subprocess
import sys

IMAGE_FOLDER = 'images'
INT_MAX = 2147483648

class Runner(object):
    def __init__(self, desired, size_multiplier = 1, open_on_save=False):
        self.make_directories()
        self.image_count = self.count_images()

        self.width = 540 * size_multiplier
        self.height = 480 * size_multiplier
        self.desired = desired
        self.current_run = 1
        self.saved_images = []
        self.open_on_save = open_on_save
        self.random_seeds = []
        self.noise_seeds = []

    @staticmethod
    def get_cwd():
        os_dir = os.getcwd()

        # file is an unsaved processing file
        if os_dir.startswith('/private/var/folders'):
            return sys.path[2] + '/'

        return ''

    @staticmethod
    def get_image_directory():
        return Runner.get_cwd() + IMAGE_FOLDER

    def make_directories(self):
        image_dir = self.get_image_directory()
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)

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

    def count_images(self):
        dir_list = os.listdir(self.get_image_directory())
        return len(dir_list)
            
    def get_padded_number(self, i, power = 3):
        string_i = '{}'.format(i)
        
        if i < 10**(power):
            while len(string_i) < (power + 1):
                string_i = '0' + string_i
                
        return string_i

    def get_image_path(self, image_name):
        return '{}/{}'.format(IMAGE_FOLDER, image_name)

    def commit_changes(self):
        runner_path = os.path.dirname(__file__)
        script_path = '{}/handle_commit.sh'.format(runner_path)
        pluralization = '' if self.desired == 1 else 's'
        commit_message = '{} image{} generated'.format(self.desired, pluralization)

        if self.desired == 1:
            commit_message += ', {}'.format(self.saved_images[0])
        elif self.desired > 0:
            commit_message += ', from {} to {}'.format(self.saved_images[0], self.saved_images[-1])
        subprocess.call([script_path, commit_message])

    def open_images(self):
        command = 'open'

        for image_name in self.saved_images:
            image_path = self.get_image_path(image_name)
            command += ' {}'.format(image_path)

        os.system(command)

    def save_seeds(self):
        has_associated_image = self.desired > 0

        with open('seeds.txt', 'w') as file:
            for i in range(len(self.random_seeds)):
                random_seed = self.random_seeds[i]
                noise_seed = self.noise_seeds[i]

                if has_associated_image:
                    image_text = 'IMAGE {}'.format(self.saved_images[i])
                else:
                    image_text = 'RUN {}'.format(i)

                file.write('# {}\n'.format(image_text))
                file.write('RANDOM : {}\n'.format(random_seed))
                file.write('NOISE : {}\n\n'.format(noise_seed))

    def save_image(self):
        padded_number = self.get_padded_number(self.image_count + self.current_run)
        image_name = '{}.png'.format(padded_number)
        self.saved_images.append(image_name)
        saveFrame(self.get_image_path(image_name))

    def handle_save(self):
        if self.desired > 0:
            self.save_image()
            self.current_run += 1

        # stop drawing
        if self.current_run > self.desired:
            noLoop()
            self.save_seeds()
            self.commit_changes()

            if self.open_on_save:
                self.open_images()

            exit()
