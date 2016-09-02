High Integrity Artificial Intelligence Systems
----------------------------------------------


Overview
--------

The High Integrity Artificial Intelligence (HIAI) project is an attempt to
bootstrap an open source Software Support Environment (SSE) targeted at the
development and through-life-cycle support of distributed intelligent sensor
systems in applications that demand both rapid development and consideration
given to safety-integrity and security risks.

This project integrates various open-source software development tools and
is intended to supply the software and procedural elements of a Developmental
Software Support Environment (DSSE) and a Life Cycle Software Support
Environment (LCSSE) as defined in DOD-STD-1467 paragraph 3.7.

A Software Support Environment (SSE) is "A host computer system, plus other
related equipment and procedures located in a facility that provides a total
support capability for the software of a target computer system (or a set of
functionally and physically related target computer systems).

The SSE enables the performance of a full range of services in support
of the software:

 1. Performance evaluation.
 2. System and software generation.
 3. Development and testing of changes.
 4. Simulation, emulation.
 5. Training.
 6. Software integration.
 7. Configuration management.
 8. Operational distribution.

The HIAI SSE is intended to support the future development of a line of
distributed intelligent sensor systems products. I.e. systems involving
networked embedded sensors connected to back-end processes handling data
aggregation and analysis. As such, it integrates tools from the "data science"
and "big data" communities together with those from the embedded software
development community, and ties the two together with common configuration
management, requirements engineering and quality assurance tools to a
level that is intended to meet the requireemnts of commonly accepted
software engineering best practices (iso-15504 SPICE; CMMI)

It is hoped that the free availability of such tools will lower the barriers
to entry; encourage competition and thereby drive improvements in the safety,
security and quality of the products available in this space.


Features
--------

 * Requirements management tools integration.
 * Task management tools integration.
 * Static analysis tools integration.
 * Test tools integration.
 * Traceability.
 * Proof of completeness.


Getting Started
---------------

This system is not yet in a state where it can be easily used. The first
usable pre-release version will be released around Q4 2017.

    git clone https://github.com/hiai-systems/b0_dev ~/dev/b0_dev
    cd ~/dev/b0_dev
    ./da build dependencies
    ./da build


Contributing
------------

Send a message to wtpayne@gmail.com to discuss possible contributions.


Author
------

William Payne 2016-04-14
https://github.com/hiai-systems/b0_dev
