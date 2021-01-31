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

## How to Play
* Two players are each assigned a "quantumon" which they control every round. Remember which one is yours!

* Every round, each quantumon picks one of six moves, specified by typing a number at the prompt. Which player goes first on any given round is determined randomly.

* When both players have picked, the combination of moves will affect the HP of the two quantumon. A quantumon's HP starts the game at the maximum value of 100 HP, and when one quantumon reaches 0 HP it will faint and its opponent will win.

* The moves that the player can choose are partly randomized, making each round slightly different! Try each of the moves and keep track of what their effects are, and see if you can uncover the true identity of each of the moves!

* As the game progresses, a mysterious feeling of "friendliness" begins to fill the air. What could this feeling be, and how does it affect the moves? In the quantum world, the power of "friendship" can work miracles!
## Inner Workings

```
          ┌─────────────┐┌───┐┌───┐┌───┐┌─────────┐
iontra_0: ┤0            ├┤ Y ├┤ X ├┤ Z ├┤0        ├
          │  Friendship │├───┤├───┤└───┘│  Battle │
dottum_0: ┤1            ├┤ X ├┤ Y ├─────┤1        ├
          └─────────────┘└───┘└───┘     └─────────┘
```
* The game works by running a quantum circuit with two qubits, one for each player. At the beginning of each turn, both qubits are initialized in the same state. Then, a two-qubit gate `J` is applied that changes into the game basis and partially entangles the two players according to a parameter `0 <= gamma <= pi/2`, which we term "friendliness". The two players' moves represent a set of single-qubit gates that are applied in sequence to their wires. Then, the operator `J` is inverted and we measure both qubits.

* Given a measurement distribution for one qubit, we interpret `|0>` as cooperation and `|1>` as defecting and compute the player's expected payoff with a fixed payoff matrix. The game then scores HP healing or damage with a simple formula involving the difference of the payoffs.

* As the game progresses, the parameter `gamma` is varied based on a formula involving the difference between the players' HP levels and how much HP has been lost by each player. Thus, the players are initially completely unentangled, and the more unbalanced the gameplay has become, the more entangled the players are. This gradually introduces the players to quantum effects and slowly moves the game from being classical to quantum.

* The first three moves that the player can take are always fixed. "Fight" corresponds to a unitary operator for "defect" and "Heal" corresponds to "cooperate" in the classical prisoner's dilemma. "Befriend" corresponds to the "supercooperate" option that is exclusive to the quantum prisoner's dilemma. Because supercooperation is usually advantageous over cooperation, "Heal" also unconditionally increases the player's HP by 5 before any other effects.

* To make things even more interesting, the remaining three moves randomly chain up to four single-qubit gates for an unpredictable effect. Try them out, observe the generated circuits, and see what they do!

* As in the quantum prisoner's dilemma, when both players choose to "Heal" or when both players choose to "Befriend", they are both rewarded with a large amount of HP recovered. If both players choose to "Fight", they will both take a small amount of damage.

* In practice, when entanglement is high, "Befriend" produces very interesting quantum effects. For example, the opponent's attack on a player who is choosing to "Befriend" may be reflected back on them. "Heal" can have unintuitive behavior against "Befriend", even possibly causing damage!

## Notable Results
* Exploration of supercooperation
* Running the circuit on different backends/simulators
*


## Next Steps
* IonQ backend compatibility: The game implements the mechanics of Prisoners' Dilemma as given in [arXiv:quant-ph/9806088](https://arxiv.org/abs/quant-ph/9806088), which uses the exponential of a two qubit gate. This cannot be directly implemented on IonQ, so, at the moment, we are running our game on the Qiskit simulator. However, [arXiv:quant-ph/0308006](https://arxiv.org/abs/quant-ph/0308006) provides means to write arbitarary two qubit gates in the form of elementary gates. Also, [arXiv:quant-ph/0007038](https://arxiv.org/abs/quant-ph/0007038) provides a slightly differnet implementation of the Prisoners' Dilemma which might be easier to decompose into elementary gates. One of these strategies can be adopted to make this game compatible with the IonQ backend.
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
* Ideally, we would have liked to implement this using Qiskit, but the language provides no simple way of storing and moving quantum states between circuits. Qiskit is made for predefining circuits and then running them; we needed to make measurements on the fly as the user gave input. Because of this, we use simple simulation with numpy matrices and vectors.
* For the most part, our qubits stay in 4 basic states: |0>, |1>, |+>, and |->. To simulate these, we have a Qubit class which stores state as a numpy vector. This class has a method to measure and probabilistically collapse a state. To simulate a measurement in another basis, you specify a change of basis to perform before and after the measurement.
* The bank is represented by a ledger and a single verification function
* Then, the majority of the code manages the user interface, providing educational menu selections and alerts for the user to respond to.
## Notable Results
*

## Next Steps
We planned on having 6 levels:
* Level 0: One qubit on each bill, centralized bank returns invalidated bills, unlimited attempts
  * Encouraged attack: guess qubit state
* Level 1: Many qubits, centralized bank returns invalidated bills, unlimited attempts
  * Encouraged attack: use information from changes due to bank measurement to determine state with certainty
* Level 2: Many qubits, centralized bank returns invalidated bills, limited wrong attempts
  * Encouraged attack: same but more carefully
* Level 3: Many qubits, centralized bank destroys invalidated bills and returns fresh bills, unlimited attempts
  * Encouraged attack: The Elizer Vaideman Bomb attack using R_theta gates with the user's choice of theta
* Level 4: Many qubits, public key money
* Level 5: Last resort level - do you take the risk and try your luck at breaking cryptographic problems, or do you retire in comfort with what you have?
Our next steps would be fully realizing all 6 levels, increasing the value of the bills being conterfeited until you're a millionaire.

## Citations
* https://www.scottaaronson.com/qclec.pdf

