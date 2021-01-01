# Alpha_Particles
Version: 2.0

Alpha Particles 2.0 is a non-relativistic simulator of alpha particle beams.

The program tries to answer the following questions:
* How far do alpha particles of a given initial kinetic energy travel in given media in the case when they all have the same initial kinetic energy?
* What properties must an alpha particle beam have for being used to deliver a particular absorbed dose of radiation to human tissue? This question is related to radiotherapy.

The program also quizzes the user about the attenuation of an alpha particle beam through given materials.

The program is useful for getting a rough idea of some of the physical properties of a beam of alpha particles. However, it is limited in that the probability of interaction between an alpha particle and atomic electrons in the materials is not correct but is an approximation of the reality. Also, the calculations are less accurate for relativistic kinetic energies because the program uses a non-relativistic model for simulating the alpha particles' interactions with atomic electrons.

The program is still to be improved. Please see Section 4.2 of my documentation for a detailed description of how the program can be improved. The documentation file is Documentation_AlphaParticles2.pdf.

Contributions from users are welcome and are subject to review.

This project is licensed under the terms of the MIT license.

The files for running the program are in the Program directory. Sample outputs of the program are in the SampleOutputs directory. The TimingStudies directory contains files that were used for the experiments mentioned in the documentation for improving the program's performance.

Kyrollos Iskandar

Author of Alpha Particles 1.0 and 2.0
