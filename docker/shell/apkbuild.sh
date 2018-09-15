#!/usr/bin/sh
nr_cpus=$(nproc)
make_max="s@\bmake\b@make -j$nr_cpus@g"
sed -i "$make_max" $PWD/APKBUILD
sed -i 's@"all"@"x86_64"@' $PWD/APKBUILD

