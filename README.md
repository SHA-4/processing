## Usage

In order to use in the Processing application itself, put `runner.py` and `handle_commit.sh` into `libraries/site-packages` inside your processing directory.

If running inside of vim, these should be in `libraries`.

You can use :make by specifying putting the following in `~.vim/ftplugin/pyde.vim`: `set makeprg=java\ -jar\ PATH/TO/JAR/FILE\ %`

## Pending
- Fix flash screen when running from command line
- Add separate message if code changed in commit or not
- Call size in setup according to https://processing.org/reference/settings_.html
  * This is what parses setup: https://github.com/processing/processing/blob/349f413a3fb63a75e0b096097a5b0ba7f5565198/java/src/processing/mode/java/tweak/SketchParser.java
  * Test monkey patching setup in Runner

