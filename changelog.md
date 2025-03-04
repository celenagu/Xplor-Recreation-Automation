# Changelog:

### delete_fees.py: 

* Added 2023 to list of years to remove fees for.

* Delete buttons were previously accessed by creating a list of all icons of class "pm-plain-button" and a list of all fee fields across the webpage. This list should be 1:1, but was not since there are several elements that are of class "pm-plain-button" outside of the fees list, causing inconsistencies between the fees that were indicated to have been deleted (deleted_fees.csv) and the fees that were actually deleted. Changed so that delete_buttons strictly includes icons of class "pm-plain-button" within the div "field-control-wrapper add-multiple-fee" (container for the fees list).

* Added fetched data to physical JSON file for debugging. (Remove later)

* Added ability to continuously specify start and end indices for facilities to update without having to refresh (debugging purposes).

* Optimized page navigation -> avoids navigating back to overview page when accessing facilities.

* delete_fees.csv is better formatted for viewing. 

### add_fees.py

* Added ability to continuously specify start and end indices for facilities to update without having to refresh (debugging purposes).

* Optimized page navigation -> avoids navigating back to overview page when accessing facilities.

* add_fees.py is better formatted for viewing.

* If fee already exists under facility, that the price is updated instead of added.

* Currently optimized to add Affiliated/BOED tournament fees for Minor, Mini, and School fields. 

