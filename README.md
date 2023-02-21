# Watermelon
Program that finds the optimal route in a graph from the eyes of an agent.

The problem is modeled as a graph that represents a map, with given types of nodes and possible actions, and the goal is to minimize the time that each agent takes to accomplish a certain task, considering that it must charge its battery.

# How to get
## Build from source
### Linux
To build the code from source, recursively clone the repository by running
```bash
git clone --recursive https://github.com/case-ev/watermelon
```

Then, run
```bash
cd watermelon
sys/build.sh
```
to build the code using the default behavior. You can also call `sys/build.sh -d` instead, which also builds the documentation (**WARNING**: Read the [Building docs](#building-docs) section before building the documentation).

## Building docs
Building the documentation requires [mdBook](https://github.com/rust-lang/mdBook). To install it, you can

- Use *Cargo*, which is available in the [following](https://www.rust-lang.org/learn/get-started) page. If you have *Cargo* installed, simply install *mdBook* by running
```bash
cargo install mdbook
```
- Download the precompiled binaries, available in the [following](https://github.com/rust-lang/mdBook/releases) page.

Once you have *mdBook* installed, run
```bash
sys/doc.sh
```
which will build the documentation and do any pre/post-processing that might be necessary. You can also run `sys/doc.sh -s`, which will start a localhost server and allow you to view the documentation in your browser.
