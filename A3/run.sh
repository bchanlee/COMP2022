#! /usr/bin/env bash

# This code was provided by the COMP2022 tutors.

language=Python
# language=Java
# language=C
# language=C++
# language=Haskell

case $language in
  Python )
    python3 main.py
    ;;
  Java )
    java Main
    ;;
  C )
    ./main
    ;;
  C++ )
    ./main
    ;;
  Haskell )
    ./main
    ;;
  * )
    echo "(run.sh) Error: language not specified. You need to edit run.sh"
    exit 1
esac
