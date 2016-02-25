# Framework Patcher for Android
This patches the framework.jar for applications to fake their signature (Useful for microG GMSCore)

## Based on:
https://github.com/moosd/Needle
https://github.com/mar-v-in/freecyngn (CM 11 Version)

## How to use:
You can download the zip that's already made, or you can modify the contents, then run:
```
sh make-zip.sh
```
Then, flash the zip in recovery (will take a while, be patient), or, if you want to run it while in android, you can extract "update-binary" from the zip, then in a terminal emulator run it like this:
```
mount -o rw,remount /
sh /path/to/update-binary none none /path/to/needle-fakesig.zip
```
Please note that you must restart for the changes to take effect.
