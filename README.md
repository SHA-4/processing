## Setup

### For the Processing Application
Copy `runner.py` and `handle_commit.sh` into `libraries/site-packages` inside your Processing directory.

### For Processing in Vim
Copy `runner.py` and `handle_commit.sh` into `libraries` inside your Processing directory.

You can use `:make` by downloading the Processing JAR file and specifying the following in `~.vim/ftplugin/pyde.vim`: `set makeprg=java\ -jar\ PATH_TO_JAR_FILE\ %`

## Usage
Below is a simple example of using Runner. What it does:
- Generates five new images based on the custom code
- Saves the images in an `images` folder in the repository
- Saves the seeds (random and noise) used for each image in a `seeds.txt` file in the repository
- Initializes a git repository (if necessary), adds all files (including the images, seeds file, and pyde file), and commits everything
```
from runner import Runner

desired_number = 5
runner = Runner(desired_number)

def setup():
    runner.setup()
    size(runner.width, runner.height)

def draw():
    runner.refresh()

    # CUSTOM CODE HERE

    runner.handle_save()
```

Runner also supports the following arguments:
- `size_multiplier` - to increase the size of the image from the default 540x480 size ratio
- `open_on_save` - to open the files that were saved after a run with the `os.open` function

## Pending
- Add support for custom sizes
- Add separate commit message if code changed in commit
- Fix flash screen when running from Vim
- Call size in setup according to https://processing.org/reference/settings_.html
- Remove explicit calls of runner functions

