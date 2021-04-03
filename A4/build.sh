#! /usr/bin/env bash

# This code was provided by the COMP2022 tutors.

language=Python
# language=Java
# language=C
# language=C++
# language=Haskell

case $language in
  Python )
    #for Python, there's nothing to compile, leave this blank
    ;;
  Java )
    javac *.java
    ;;
  C )
    clang main.c -o main
    ;;
  C++ )
    clang++ main.cpp -o main
    ;;
  Haskell )
    ghc main.hs
    ;;
  * )
    echo "(build.sh) Error: language not specified. You need to edit build.sh"
    exit 1
esac
