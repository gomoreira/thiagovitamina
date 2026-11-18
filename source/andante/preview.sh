#!/bin/sh
# Prévia de revisão: gera /andante/original e /andante/vitamina a partir do mesmo código.
set -e
cd "$(dirname "$0")"
ROOT=../../andante
rm -rf "$ROOT"; mkdir -p "$ROOT"
ANDANTE_VARIANT=original ANDANTE_BASE=/andante/original ANDANTE_OUT=$ROOT/original python3 build.py
ANDANTE_VARIANT=vitamina ANDANTE_BASE=/andante/vitamina ANDANTE_OUT=$ROOT/vitamina python3 build.py
python3 comparar.py "$ROOT"
