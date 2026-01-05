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
android.permissions = INTERNET
android.private_storage = True
android.enable_androidx = True
android.release_artifact = apk
