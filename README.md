# Graphoire
An open-source collection of graph-theory elements and magical formulae.

---
## What Is Graphoire?

Graphoire is a collection of software tools for graph theory exploration and research.

There are four qualitative goals guiding Graphoire development. The author wants to build a graph-theory platform that is ***expressive***, ***comprehensive***, ***versatile***, and ***performant/efficient***, 
in that order.

* ***expressive***
	* The software will use familiar terms, verbose labeling of functions and data structures, and clearly-identified alternative implementation approaches to support conceptually clear, readable implementation code.
* ***comprehensive***
	* This project will continually grow, to furnish a comprehensive library of data structures and algorithms suitable for general graph theory research.
* ***versatile***
	* Rather than build on a single approach to representation of graph theory data and algorithms, this library will be versatile by providing alternative implementations suited for different investigations: for example, representation of graphs as either set-theoretic collections, linked node-edge structures, or as sparse matrices, with facilities to convert between these alternative representations.
* ***performant/efficient***
	* Ultimately it *is* a goal to have this library provide production-quality algorithm implementations optimized for both performance and memory use, and also to include performance-analysis capabilities; however this goal is initially lower-priority than the preceding goals.

### Programming Language: python (...)

Graphoire is initially being developed in python but other language ports are possible.

### Dependencies

Some features of Graphoire rely on the **numpy** and **scipy** libraries - in particular,
sparse matrix and linear-algebra features.

### No drawing or visualization (yet)

The Graphoire effort does not currently include graph drawing or visualization.

### *Not yet for production!*

There are many graph theory toolsets out there, and in particular if you are looking for
production-quality graph analysis code for machine learning, data visualization, or 
similar, Graphoire is *not* a good choice at present.

Graphoire's design and source code organization ***will change regularly*** during its
inception phase, and its priority will be on conceptual structure rather than production
quality during this phase.

With that disclaimer made, you are welcome to use this code for your own purposes under the terms of the Apache 2.0 open source license.

---
# Documentation

This will be manifest eventually!

For now: you can explore Graphoire in a python environment by downloading the source and adding the `pyhon-src` directory to your `$PYTHONPATH`. 

---
Author: Christopher Corbell  
Last updated: 7 March 2021


