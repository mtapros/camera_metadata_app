[app]
title = Camera Metadata App
package.name = camerametadataapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,ttf,otf,wav,mp3,xml
source.main = main.py
version = 0.1.0
requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.manifest.application_attrs = android:usesCleartextTraffic="true",android:networkSecurityConfig="@xml/network_security_config"

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 31
android.minapi = 21

android.accept_sdk_license = True

android.ndk = 25b
android.ndk_api = 21

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE
android.private_storage = True
android.enable_androidx = True
android.release_artifact = apk

# This tells Buildozer to copy the templates folder
android.add_src = templates
