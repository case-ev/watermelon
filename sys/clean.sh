#!/bin/bash

# Clean the directory

rm -rf ./.pytest_cache ./build ./logs ./src/watermelon.egg-info ./dist
find . -name __pycache__ -exec rm -rf {} +
