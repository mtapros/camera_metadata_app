[app]
title = Camera Metadata App
package.name = camerametadataapp
package.domain = org.example
source.dir = .
source.include_exts = py
source.main = main.py
version = 0.1.0
requirements = python3,kivy

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 31
android.minapi = 21
android.accept_sdk_license = True
android.ndk = 25b
android.ndk_api = 21

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE

# Force through p4a
p4a.bootstrap = sdl2
p4a.extra_args = --permission INTERNET --permission ACCESS_NETWORK_STATE --permission ACCESS_WIFI_STATE --permission CHANGE_WIFI_STATE

android.private_storage = False
android.enable_androidx = True
android.release_artifact = apk
