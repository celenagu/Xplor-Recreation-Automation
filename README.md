# Xplor-Recreation-Automation

This repository contains several tools designed to streamline and automate repetitive tasks within the City of Brampton's Xplor Recreation Software. It logs all changes to a CSV file for easy tracking and reference. 

Automations for adding and removing outdated fees were built upon an existing implementation ([link](https://github.com/Mintches/City-of-Brampton-Recreation)), which has been modified and optimized to improve functionality and meet new project requirements. Changes made to the original project are documented in `changelog.md`.

## Setup
1. Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt

2. If in LIVE mode, set the `USERNAME` constant variable to a valid brampton email 

## Automation Features 
### Adding and Deleting Fees
* *Automate the updating of 2025 Affiliated/BOED fees for COB fields and ball diamonds*
* Automates the addition of new fees
* Removes outdates fees from the system
* Logs all changes (added and deleted fees) in their respective CSV file

> #### Instructions
> 1. Set the `TEST` constant variable to `True` or `False`
> 2. Run the file
> 3. Log into the Xplor Software Platform
> 4. Navigate to the "Manage Facilities" section
> 5. Enter `ENTER` in the terminal to begin the automation process
> 6. Follow the prompts in the terminal to provide automation specifications

### Updating Barcodes
* *Support March 2025 advanced registration timelines shift, automating updates to registration timelines for single booking (drop-in) events*
* Automates process of updating end dates of recurring activities (when given CSV file of activities to be updated)
* Logs all changes (updated activities) in a CSV file

> #### Instructions
> 1. Ensure there is a valid csv file containing activities with `EventIDs` in the same folder
> 2. Set the `TEST` constant variable to `True` or `False`
> 3. Run the file
> 4. Log into the Xplor Software Platform
> 5. Navigate to "Activities" -> "Registration"
> 6. Ensure all search filters are set to default
> 7. Press `ENTER` to begin the automation process

### Validating Account Verification
* *Support updated resident-first registration process, pre-verifying clients under organizational accounts*
* Processes all clients under organization-type accounts, confirming validation and prventing future revalidation prompts
* Logs all changes (updated clients) in a CSV file

> #### Instructions
> 1. Set the `TEST` constant variable to `True` or `False`
> 2. Run the file
> 3. Log into the Xplor Software Platform
> 4. Navigate to "Clients" -> "Manage Accounts"
> 5. Navigate to the desired view
> 6. Enter `ENTER` in the terminal to begin the automation process
> 7. Follow the prompts in the terminal to provide automation specifications

## Additional Notes:
* Ensure you have the necessary permissions to edit fees and dates within the Xplor Software
