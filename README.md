# Quantumon(ey): A Entangled Pair of Quantum Games

Our team was so excited to make games, that we made two! Quantumon is a Pokemon spinoff that uses expected values from the quantum prisoners dilemma to determine the effect of attacks. This has practical applications in settings where we can use quantum set-ups to  encourage collaboration. Wiesner's Thievers is a more educational game, which teaches you Wiesner's Quantum Money scheme as you break various successively stronger versions of it. Both games are text-based, and can be played by running the respective Python scripts in a terminal: quantumon.py and wiesnermobile.py.

# Quantumon: Gotta Measure 'Em All!

In the lush quantum fields of Shor Town, your laid-back, classical lifestyle has suddenly been turned upside-down by a gang of newcomers with amazing,
local realism-violating abilities! You make fast friends with some of them, but the others threaten to entangle themselves in your affairs.
Do you have what it takes to become master of quantum gates and measure 'em all?
## Introduction
Game theory in its essence is communication of information between different parties. Classical game theory is a well established field, where the solutions are well-known. With the advent of quantum communication, we now have access to alternative solutions to these games. The ability to have entanglement in the initial states, and superposition of strategies on the initial states, makes game theory more interesting. Here we explore the quantum version of the classical prisoner's dilemma.
In classical prisoner's dilemma, the two parties choose to protect themselves, in other words maximize their gain (payoff) at the expense of the other participant. The catch is that even though it appears as the most optimal strategy to both parties, they end up doing worse. In [1] it has been showed that both parties can escape if they both use quantum strategies, which are quantum resources such as entanglement under unitary rotations. In particular, a "supercooperation" strategy emerges which is a Nash equilibrium in highly entangled games. Through our game we demonstrate a behavior where if both parties use quantum startegies, they can attain a higher payoff compared to their classical counterparts.

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

* While the game is initially identical to the classical prisoner's dilemma, as the game progresses, the rules and optimal moves become increasingly quantum. Although they don't know it, the players are essentially building entangled quantum circuits by playing the game. For players who have not worked with quantum systems before, this provides a gentle exposure to quantum mechanics in a fun and educational manner.
* The "supercooperation" feature of the game demonstrates the power of quantum mechanics when added to a classical system. In the classical version of the game, if an opponent chooses to "defect", the player can only choose to "cooperate" - thereby suffering a large loss - or "defect" in return - thereby causing punishing both players. However, with the intermediary quantum option of "supercooperation", it is possible to respond in a way that buffers the negative effect of an opponent who chooses to "defect" while simulatenously retaining a positive effect when an opponent chooses to "cooperate". As a result, this opens up new avenues for gameplay and provides it with greater depth.



## Next Steps

* IonQ backend compatibility: The game implements the mechanics of Prisoners' Dilemma as given in [arXiv:quant-ph/9806088](https://arxiv.org/abs/quant-ph/9806088), which uses the exponential of a two qubit gate. This cannot be directly implemented on IonQ, so, at the moment, we are running our game on the Qiskit simulator. However, [arXiv:quant-ph/0308006](https://arxiv.org/abs/quant-ph/0308006) provides means to write arbitrary two qubit gates in the form of elementary gates. Also, [arXiv:quant-ph/0007038](https://arxiv.org/abs/quant-ph/0007038) provides a slightly different implementation of the Prisoners' Dilemma which might be easier to decompose into elementary gates. One of these strategies can be adopted to make this game compatible with the IonQ backend.
* Optimizing gameplay: Ideally, we would spend more time experimenting with the game to find optimal values of the internal parameters to balance gameplay for both players (potentially compensating for certain “overpowered” strategies).
* More intricate battle system: To make the game more interesting, the moves aside from “Fight”, “Heal”, and “Befriend” could be given additional effects. For example, they might boost the damage dealt by “Fight”, heal additional health, or alter the “friendliness” parameter directly.


## Citations

1. Eisert, Jens, Martin Wilkens, and Maciej Lewenstein. "Quantum games and quantum strategies." Physical Review Letters 83.15 (1999): 3077. [arXiv:quant-ph/9806088](https://arxiv.org/abs/quant-ph/9806088)
2. Li, Angsheng, and Xi Yong. "[Entanglement guarantees emergence of cooperation in quantum prisoner's dilemma games on networks.](https://www.nature.com/articles/srep06286)" Scientific reports 4.1 (2014): 1-7
3. Benjamin, Simon C., and Patrick M. Hayden. "Multiplayer quantum games." Physical Review A 64.3 (2001): 030301.[arXiv:quant-ph/0007038](https://arxiv.org/abs/quant-ph/0007038)


# Wiesner's Thievers: Fake It 'Til You Make It!

## Introduction
Here in Wiesnerville, we had a rampant counterfeiting problem. The issue was that classical information is just too easy to copy, too easy to fake. We heard that the No-Cloning Theorem prevents anyone from copying a quantum state, and our scientists got to work. Now, every dollar bill has a monetary value ($1, $10, etc.), a unique serial number, AND a quantum state embedded in the fabric of the bill. Bada bing, bada boom: uncopiable money! Problem solved, right? 

The state on each bill comes in a special form: it will always be a product state composed of |0>, |1>, |+>, and |->. We don't want any fake bills being used, so every time a Wiesnerville resident tries to buy something, they have to mail their bill to the Wiesner Central Bank to verify that it's the real deal. After the bank checks the bill, we'll add money to your net worth if it's verified and send the bill back to you if isn't. 

At the bank, we keep a ledger - a list of every bill's serial number, and the secret true identity of the state on that bill. Here's what one row of that top-secret ledger might look like:

    Bill #0198308187: |1>|->|+>|0>|->

Now, your job is to get filthy rich. You found a few dollars on the floor and you happen to own a dollar printing factory - find a way to fool the bank into accepting fake bills!

## Rules of the Game
* There are multiple levels. In each one, you start off with a few dollar bills you found on the ground, and your goal is to increase your net_worth to some dollar figure by getting bills approved by the bank. 

* You are presented with a series of menus. You can select a bill and then choose to 
  1. Make a copy with the same serial number and your choice of qubits 
  2. Measure a specific qubit from the bill
  3. Send the bill to the bank for verification
  
* If you send a bill to the bank and it is approved, your net worth goes up by that bill's value and you lose the bill. If it is denied, various things happen depending on the level: you might initially get it back, but by the end of it, you get fresh bills back and you go to jail after a limited number of failures.

We planned on having 5 levels:
* Level 0: One qubit on each bill, centralized bank returns invalidated bills, unlimited attempts
  * Encouraged attack: guess qubit state
  
* Level 1: Many qubits, centralized bank returns invalidated bills, unlimited attempts
  * Encouraged attack: use information from changes due to bank measurement to determine state with certainty
  
* Level 2: Many qubits, centralized bank returns invalidated bills, limited wrong attempts
  * Encouraged attack: same but more carefully
  
* Level 3: Many qubits, centralized bank destroys invalidated bills and returns fresh bills, one wrong attempt
  * Encouraged attack: The Elizer Vaideman Bomb attack using R_theta gates with the user's choice of theta
  
* Level 4: Many qubits, public key money, one wrong attempt
  * Last resort level - do you take the risk and try your luck at breaking cryptographic problems, or do you retire in comfort with what you have?

## Inner Workings
* Ideally, we would have liked to implement this using Qiskit, but the language provides no simple way of storing and moving quantum states between circuits. Qiskit is made for predefining circuits and then running them; we needed to make measurements on the fly as the user gave input. Because of this, we use simple simulation with numpy matrices and vectors.
* For the most part, our qubits stay in 4 basic states: |0>, |1>, |+>, and |->. To simulate these, we have a Qubit class which stores state as a numpy vector. This class has a method to measure and probabilistically collapse a state. To simulate a measurement in another basis, you specify a change of basis to perform before and after the measurement.
* The bank is represented by a ledger and a single verification function
* Then, the majority of the code manages the user interface, providing educational menu selections and alerts for the user to respond to.

## Notable Results
* The game serves to introduce players to the concept of quantum money and then to build upon that knowledge. It is accessible to both players with no prior quantum computing exposure and players who are seeking a quantum computing challenge, and it aims to bridge the gap between the two. For this reason, the levels are intentionally designed in order of increasing difficulty, with the inclusion of a comprehensive tutorial at the beginning of the initial stage.  
* As an educational game, there weren't any new results uncovered by this, but we did notice that there aren't many quantum languages that can handle qubit operations on the fly, instead of working in the predefined circuit model. Perhaps this will improve as it becomes easier to store a quantum state coherently for longer durations.

## Next Steps
Our next steps would be fully realizing all 5 levels, increasing the value of the bills being conterfeited until the player becomes a millionaire. We especially wanted to make it possible for the player to come up with the EV Bomb attack themselves by leading them to the solution as they ran out of bills.

We also would like to make sure the pacing and difficulty is balanced well over the levels. Playtesting should help find the optimal goals and bill amounts per level.

## Citations
* https://www.scottaaronson.com/qclec.pdf

