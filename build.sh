#!/bin/bash

# TODO
app_link="https://www.apkmirror.com/wp-content/themes/APKMirror/download.php?id=5320087&key=5633073aa64fc131c8d940372a45c9dddcdeb74b&forcebaseapk=true"

if [[ -z "$3" ]]; then
  echo "Define tags for cli, pathces, integrations (order matter)"
  exit 1
fi

root=revanced

cli="revanced-cli-$1-all.jar"
patches="revanced-patches-$2.jar"
integrations="revanced-integrations-$3.apk"

cli_path="tools/cli"
pathces_path="tools/patches"
integrations_path="tools/integrations"

app_name="app.apk"

if [[ $(ls | grep $root) == "" ]]; then
  mkdir -p $root/$cli_path $root/$pathces_path $root/$integrations_path $root/apps $root/patched_apps
fi

cd $root

if [[ $(fd --full-path $cli_path | grep $1) == "" ]]; then
  rm -rf $cli_path/*
  wget https://github.com/ReVanced/revanced-cli/releases/download/v$1/$cli -P $cli_path
fi

if [[ $(fd --full-path $pathces_path | grep $2) == "" ]]; then
  rm -rf $pathces_path/*
  wget https://github.com/ReVanced/revanced-patches/releases/download/v$2/$patches -P $pathces_path
fi

if [[ $(fd --full-path $integrations_path | grep $3) == "" ]]; then
  rm -rf $integrations_path/*
  wget https://github.com/ReVanced/revanced-integrations/releases/download/v$3/$integrations -P $integrations_path
fi

rm -rf $root/apps/*

wget --user-agent="Mozzila" $app_link -O apps/$app_name

java -jar $cli_path/$cli patch \
  -b $pathces_path/$patches \
  -m $integrations_path/$integrations \
  -o patched_apps/$app_name \
  apps/app.apk

rm -rf revanced-resource-cache.

adb install patched_apps/$app_name
