#!/bin/sh
cd "$(dirname "$0")"
patch_name="fakesig"

cd tar
tar cf ../needle.tar *
cd ..
zip -r9 needle-$patch_name.zip META-INF needle.tar
rm needle.tar
