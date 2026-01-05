[app]
title = Camera Metadata
package.name = camerametadata
package.domain = com.photographer

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy==2.1.0,requests,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.gradle_dependencies = 

[buildozer]
log_level = 2
warn_on_root = 1
