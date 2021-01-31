# Quantumon(ey): A Pair of Quantum Games

Our team was so excited to make games, that we made two! Quantumon is a Pokemon spinoff that uses expected values from the quantum prisoners dilemma to determine the effect of attacks. This has practical applications in settings where we can use quantum set-ups to  encourage collaboration. Wiesner's Thievers is a more educational game, which teaches you Wiesner's Quantum Money scheme as you break various successively stronger versions of it. Both games are text-based, and can be played by running the respective Python scripts in a terminal: quantumon.py and wiesnermobile.py.

# Quantumon: Gotta Measure 'Em All!

In the lush quantum fields of Shor Town, your laid-back, classical lifestyle has suddenly been turned upside-down by a gang of newcomers with amazing,
local realism-violating abilities! You make fast friends with some of them, but the others threaten to entangle themselves in your affairs.
Do you have what it takes to become master of quantum gates and measure 'em all?
## Introduction
* Theoretical developments in quantum computing
* Classical game theory - the prisoner's dilemma problem
* Motivation: demonstrating the extra power of quantum systems when applied to traditional problems (supercooperation), in a fun way

## Rules of the Game
* Two player game
* Each player is randomly assigned a "quantumon"
* Each quantumon starts with 100 HP (health points)
* Every turn, both players can pick one of 6 moves to heal or deal damage
* As the game progresses, a mysterious `friendliness` value is updated
* The game ends when one of the quantumon reaches 0 HP and faints

## Inner Workings
* [Include illustration of circuit (?)]
* The game works by running a quantum circuit with two qubits, one for each player
* At the beginning of each turn, both qubits are initialized in the same state
* A two-qubit J_hat gate is applied [expand on what this does]
* Each move is a set of single-qubit gates
  * [Include unitary formula in terms of angles (?)]
  * The first two moves are equivalents of the options "defect" and "cooperate" in the classical prisoner's dilemma [list the angle values, gates]
  * The third move is a "supercooperate" option that is exclusive to a quantum version of the prisoner's dilemma [list the angle values, gates]
  * To make things even more interesting, the remaining three moves randomly combine the available single-qubit gates for an unpredictable effect
  *
*
* [Elaboration on the supercooperating "befriend" option]
*
* Mechanics of `friendliness`
  * Friendliness increases when a quantumon has lost considerable health
  * The higher the friendlines value, the more powerful the quantum aspect of the `befriend` option becomes
    * When `friendliness` is 0, the game is entirely separable (classical)
    * When `friendliness` reaches 1, the game becomes maximally entangled (quantum)
  * Purpose:
    * Gradually introduces the player to quantum mechanics
    * Transitions the game from a classical to a quantum one depending on the progress of the game
*
*

## Notable Results
* Exploration of supercooperation
* Running the circuit on different backends/simulators
*


## Next Steps
* [IonQ backend compatibility]
* []

## Citations


# Wiesner's Thievers: Fake It 'Til You Make It!

Wiesnerville has a counterfeiting problem. Luckily, the new mayor, a part-time quantum scientist, thinks they have a solution: quantum money. Since the no-cloning theorem prevents copying quantum states, if we put one in every dollar bill, bye bye counterfeits! Right? In this game, you work through various levels of increasing difficulty and try to cheat the bank out of as much money as you can without getting caught. Will you get away with it?
## Introduction
* Theoretical developments in quantum computing
* Classical game theory - the prisoner's dilemma problem
* Motivation: demonstrating the extra power of quantum systems when applied to traditional problems (supercooperation), in a fun way

## Rules of the Game
* 

## Inner Workings
* 

## Notable Results
* 


## Next Steps
* 

## Citations



_______________________________ Getting Started (Help Info)  _______________________________

# Welcome to iQuHACK 2021!
Check out some info in the [event's repository](https://github.com/iQuHACK/2021) to get started.

Having a README in your team's repository facilitates judging. A good README contains:
* a clear title for your project,
* a short abstract,
* the motivation/goals for your project,
* a description of the work you did, and
* proposals for future work.

You can find a potential README template in [one of last year's projects](https://github.com/iQuHACK/QuhacMan).

Feel free to contact the staff with questions over our [event's slack](https://iquhack.slack.com), or via iquhack@mit.edu.

Good luck!
