## Future-Of-Blockchain

#  dAirBnB
## A decentralised accomodation rental market on the Tezos blockchain



This project is about a proof of concept smart contract for the decentralised negotiation of rental agreements. 

dAirBnB is described in more detail in the associated paper dAirBnB.pdf. 

Herbert, an host, and Gaia, a guest, freely negotiate the terms of their rental agreement. Such an agreement is then encoded in a Tezos smart contract which guarantees that the agreed terms can not be modified or tampered with, even in the presence of dishonest participants. A double escrow framework (both H and G pay a deposit) incentivates participants to bring the contract to a successful end.

G and H can negotiate fairer conditions. The market becomes more efficient. The technology, with incentives, reputations and the blockchain warranty of untamperable execution, provide the trust framework.

This is an experiment to assess the viability and security of such decentralised market.

dAirBnB consists of a smart contract deployed on Tezos and a set of web applications as front-end for the participants, which include G and H, but also a smart home system, managing the actual connection with the real world of the rented flat through an Internet-Of-Things approach.

The smart contract is deployed to the Tezos Cartaghenet testnet, and developed in smartPy, a dialect of Python supporting Tezos smart contract development, with an IDE, a simulator and (forthcoming) a verification framework.

The web applications are developped using the ConseilJs framework on top of HTML5 and JavaScript, which allow interfacing with the smart contract. Prototype interfaces for H, G and the smart home system are provided. 

## Test dAirBnB on the Smart.Py simulator:
- copy the code in DAirBnB.py to the editor at https://smartpy.io/dev/ 
- compile/run it (you may want to change the testing scenario).

## Deploy dAirBnB on the Tezos Carthagenet test net:
- copy the code in DAirBnB.py to the editor at https://smartpy.io/dev/ 
- compile/run the code, on Michelson click deploy Contract
- follow the instraction to originate and deploy the contract on the testnet
- you may use an explorer to observe the smart contract at the deployed address on the testnet, eg.

  https://carthagenet.tzstats.com/KT18pDcpc91w9uyTASnECL911kyrJAW9XpcB


## Execute the dAirBnB agreement protocol using web applications:
- clone the project (you need .html + .js)
- run DAirBnB.html on your Browser (run it in three windows and launch the different interfaces)
- start playing with the contract using the three interfaces
- open the console to track the transaction
- you may use an explorer to observe the smart contract at the deployed address on the testnet, eg.

  https://carthagenet.tzstats.com/KT18pDcpc91w9uyTASnECL911kyrJAW9XpcB

## Watch a demo: 
 (in case of problems you may want to download the file and use your preferred mp4 viewer)
 
 - demo 1: <a  href="http://www.cs.stir.ac.uk/~abb/video_1.mp4" target ="_">Introducing the decentralized AirBnB protocol </a>
 - demo 2: <a  href="http://www.cs.stir.ac.uk/~abb/video_2.mp4" target ="_">Presenting the smart contract (SmartPy)</a>
 - demo 3: <a  href="http://www.cs.stir.ac.uk/~abb/video_3.mp4" target ="_">Presenting the web applications ( HTML 5 & JavaScript)</a>
 - demo 4: <a  href="http://www.cs.stir.ac.uk/~abb/video_4.mp4" target ="_">Presenting the interaction between the user interface & contract using ConseilJs </a>



### Contacts
abracciali@gmail.com

sihamlamssaoui@gmail.com




<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
