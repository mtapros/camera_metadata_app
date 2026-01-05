[app]
# (str) Title of your application
title = Camera Metadata App

# (str) Package name
package.name = camerametadataapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,ttf,otf,wav,mp3

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of inclusions using pattern matching
# source.include_patterns = assets/*,images/*.png

# (list) List of exclusions using pattern matching
# source.exclude_patterns = tests/*,docs/*

# (str) Application versioning (method 1)
version = 0.1.0

# (list) Application requirements
# IMPORTANT: add any extra libs your app imports, comma-separated.
requirements = python3,kivy

# (str) Presplash of the application (Android)
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0


[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0


[android]
# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) If True, then automatically accept SDK license agreements.
# This prevents CI from failing at "License android-sdk-license ... Accept? yN".
android.accept_sdk_license = True

# (str) Android NDK version to use (p4a often recommends 25b; your log shows r25b)
android.ndk = 25b

# (int) Android NDK API to use. Usually matches android.minapi.
android.ndk_api = 21

# (list) Permissions
# Add only what you really need.
android.permissions = INTERNET

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) Enable AndroidX (commonly needed by modern dependencies)
android.enable_androidx = True

# (str) The format used to package the app (apk or aab)
android.release_artifact = apk


# (Optional) If you build for multiple architectures, uncomment:
# android.archs = arm64-v8a,armeabi-v7a
