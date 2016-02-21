#!/usr/bin/env python3
import os, subprocess, tempfile, time, shutil, sys

# do the injection
print("ui_print *** Done. Now this won't hurt a bit...")
to_patch = "out/smali/android/content/pm/PackageParser.smali"

f = open(to_patch, "r")
old_contents = f.readlines()
f.close()

f = open("fillinsig.smali", "r")
fillinsig = f.readlines()
f.close()

# add fillinsig method
i = 0
contents = []
already_patched = False
in_function = False
right_line = False
start_of_line = None
done_patching = False
stored_register = "v11"
partially_patched = False

while i < len(old_contents):
    if ";->fillinsig" in old_contents[i]:
        already_patched = True
    if ".method public static fillinsig" in old_contents[i]:
        partially_patched = True
    if ".method public static generatePackageInfo(Landroid/content/pm/PackageParser$Package;[IIJJLjava/util/Set;Landroid/content/pm/PackageUserState;I)Landroid/content/pm/PackageInfo;" in old_contents[i]:
        in_function = True
    if ".method public static generatePackageInfo(Landroid/content/pm/PackageParser$Package;[IIJJLandroid/util/ArraySet;Landroid/content/pm/PackageUserState;I)Landroid/content/pm/PackageInfo;" in old_contents[i]:
        in_function = True
    if ".method public static generatePackageInfo(Landroid/content/pm/PackageParser$Package;[IIJJLjava/util/HashSet;Landroid/content/pm/PackageUserState;I)Landroid/content/pm/PackageInfo;" in old_contents[i]:
        in_function = True
    if ".end method" in old_contents[i]:
        in_function = False
    if in_function and ".line" in old_contents[i]:
        start_of_line = i + 1
    if in_function and "arraycopy" in old_contents[i]:
        right_line = True
    if in_function and "Landroid/content/pm/PackageInfo;-><init>()V" in old_contents[i]:
        stored_register = old_contents[i].split("{")[1].split("}")[0]
    if not already_patched and in_function and right_line and not done_patching:
        contents = contents[:start_of_line]
        contents.append("move-object/from16 v0, p0\n")
        contents.append("invoke-static {%s, v0}, Landroid/content/pm/PackageParser;->fillinsig(Landroid/content/pm/PackageInfo;Landroid/content/pm/PackageParser$Package;)V\n" % stored_register)
        done_patching = True
    else:
        contents.append(old_contents[i])
    i = i + 1

if not already_patched and not partially_patched:
    contents.extend(fillinsig)
elif partially_patched and not already_patched:
    print("ui_print ??? Previous failed patch attempt, not including the fillinsig method again...")
elif already_patched:
    print("ui_print ??? This framework.jar appears to already have been patched... Exiting.")
    sys.exit(2)

f = open(to_patch, "w")
contents = "".join(contents)
f.write(contents)
f.close()

# reassemble it
print("ui_print *** Injection successful.")
sys.exit(0)

# put classes.smali into framework.jar
#print(" *** Putting things back like nothing ever happened...")
#os.chdir("framework.jar.out/build/apk")
#subprocess.call(["zip", "-r", "../../../framework.jar", "classes.dex"])
