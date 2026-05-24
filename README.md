**The Simple Summary**
The best trainer for Ace-Step imo is Side-Step , it allows for a lot of adjustment and tweaking but it can be over-powering , so I made a calculator to help with the settings and with understanding the choices .

**NB for the best loras, it is essential that the side-car txt files are accurately and fully tagged . **

Think of this tool as a "Smart Map" for your training. Instead of guessing how to set up your AI training, you feed it your audio files, and the tool acts as an expert technician. It measures the quality of your audio, scans your computer's power (VRAM), and then gives you the exact "recipe" (settings) to get the best result without crashing your computer or wasting time training for too long.

The code will ask a series of questions and you answer them / show the code what dataset you wish to use and it'll analyse it and give the settings it recommends. I would advise using the User option on the first question as the options it gives do not work in the standard Side-Step .

<img width="594" height="157" alt="image" src="https://github.com/user-attachments/assets/d4d4cc98-64cf-4e08-bb14-b37f5c8d5084" />

1. Operation Framework Interface
Options: 1 (Standard User Mode), 2 (Developer Diagnostics Mode).

What they mean: Standard Mode utilizes pre-validated safe-guards. Developer Mode unlocks manual log-file integration and advanced optimizers (SOAP, C-Lion).

Choice: Time: Choose 1. Quality: Choose 2.

<img width="329" height="81" alt="image" src="https://github.com/user-attachments/assets/211f526a-f1d2-4ef4-be95-c45fa9b561da" />

2. Model Format
Options: 1 (LoRA), 2 (LoKRs).

What they mean: LoRA is the standard balance of speed and fidelity; LoKRs (Kronecker-factored) offer higher representational capacity for complex concepts.

Choice: Time: Choose 1. Quality: Choose 2 (best for multi-concept density).

<img width="298" height="98" alt="image" src="https://github.com/user-attachments/assets/bc3c5f99-6c88-4a2d-a2d7-f213b2fa1c1b" />

3. Training Objectives Mode
Options: 1 (Standard), 2 (Diagnostic Redo), 3 (Custom Override).

What they mean: 1 is your basic calculation. 2 allows you to input specific "faults" for the system to auto-correct & give amended settings. 3 allows manual control over Rank/Alpha.

Choice: Time: Choose 1. Quality: Choose 2 (to mitigate artifacts like sibilance/mud).

<img width="822" height="32" alt="image" src="https://github.com/user-attachments/assets/f9793e2e-4eb0-4703-bfa8-a64eb3875c82" />

It optimises the settings for the gpu you have (eg series 30/40) and its vram total (this is automatic)

It will then give you a file requestor and ask you to select the audio dataset that you wish to process

<img width="791" height="115" alt="image" src="https://github.com/user-attachments/assets/f8d91f3f-0588-47e2-9bb0-003ea3babf49" />

This is the start of the analysis of the dataset

<img width="694" height="186" alt="image" src="https://github.com/user-attachments/assets/9d1ea48d-cc2e-4b1d-b5f2-23625603ef8f" />
And the summary of it at the end . Trainers are better at processing chunks as it basically gets bored looking at full length songs and the chunks also help with separation of vocals from instruments. 

<img width="637" height="34" alt="image" src="https://github.com/user-attachments/assets/afb2983a-bff9-4a63-9bba-98536fcc9cde" />
A validation set is a % of your dataset that is kept aside and compared to the model , to see how it is doing and prevent overfitting. 

<img width="495" height="22" alt="image" src="https://github.com/user-attachments/assets/649da57a-8c0c-4773-bec0-7468ae3d820c" />
Number of singers is very important, each singer is a concept that the model needs extra time to learn - each singer you add , tweaks the settings to allow time for it to learn 
NB tag each singer fully and correctly

<img width="271" height="27" alt="image" src="https://github.com/user-attachments/assets/19c7dd41-8862-4db1-bf06-baa01fd1e7f5" />
If you are using a turbo model , it needs to change the settings to accomodate that

<img width="942" height="271" alt="image" src="https://github.com/user-attachments/assets/6b0b8b22-a63c-4a58-a6b8-ccaf4819eb75" />
The explanation for these is in the picture , there is a third option of 'AdamW 8-bit' to save vram with no quality penalty


<img width="776" height="168" alt="image" src="https://github.com/user-attachments/assets/758cfc9f-1e37-4eaf-94e5-7fe1ef57ccfb" />
It does a deep spectral analysis of the audio to determine its quality, similarity and as a whole dataset. All of these are weighting factors to adjust the settings and formulas for optimum results. 

**The Settings - input into the gui or wizard **
<img width="1108" height="217" alt="image" src="https://github.com/user-attachments/assets/d964378b-ea5c-420c-9718-0cda2427a6e2" />

<img width="387" height="341" alt="image" src="https://github.com/user-attachments/assets/02a76bc0-e239-4e08-a7d4-0a04098b554c" />
Two options for these settings , option A is less vram intensive , B is max performance (still under work)

And the final part - Side-Step has the option to add your own formula , the dataset and your choices will adjust the formulas in each to add/remove time to allow fuller learning of structure at the start and details afterwards . 
<img width="990" height="272" alt="image" src="https://github.com/user-attachments/assets/c9c6151a-a4d0-45b6-b2a9-ab1822aad30c" />

Paste the formula here in Side-Step >

<img width="931" height="529" alt="image" src="https://github.com/user-attachments/assets/d01bbf92-1a5e-438d-8913-1e5c979c4fb1" />

Finally, the calculator gives you a readout of the formulas that should be roughly the same as Side-Steps

<img width="1188" height="680" alt="image" src="https://github.com/user-attachments/assets/6fb5798f-5654-4877-bee5-26f098cf9c51" />














