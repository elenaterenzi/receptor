# Receptor
Receipt OCR Date and Amount detector

## Project Description
OCR for Handwritten and Printed Receipts

## Challenge Statement
Create a Bot that can identify and extract date and amount data for handwritten and printed receipts for data entry with four key benefits:
* Enabling working professionals to easily input date and amount data for handwritten and printed receipts into accounting systems and save valuable time and effort for customer engagements and initiatives.
* Creating a technical use case that can be utilized for industries that utilizes OCR technologies including banking, education, finance, government, retail, and medical.
* Building technical capabilities to capitalize on market potential. (OCR Market – US$25,1B by 2025, Business Account Software Market – US$4.1B by 2021)

## Architectural Diagram and Process Flow
![Architecture Diagram](https://github.com/elenaterenzi/receptor/blob/master/Architecture%20Diagram.PNG)
![Overall Process Flow](https://github.com/elenaterenzi/receptor/blob/master/Overall%20Process%20Flow.PNG)
![Web Service Creation Process Flow](https://github.com/elenaterenzi/receptor/blob/master/Web%20Service%20Creation%20Process%20Flow.PNG)

## Lessons Learned
* Technical Learnings:
  * Limitations for image size and dimension: Needed to ensure all receipt images are within stipulated limits in technical documentation (Less than 4MB, greater than 50 x 50 pixels).
  * Utilization of bounding boxes to read and segment data in receipts: Discussed multiple options for extracting receipt data and concluded that the most appropriate method is still reading and segmenting receipts into bounding boxes with data.
  * Validation of data contained in bounding boxes: Discussed the various challenges in deciphering receipts with no fixed pattern or format and concluded that there is a need to perform manual validation of data contained in bounding boxes to classify whether the boxes contain valid date and amount information for feature engineering and training.  
  * Challenges in building fuzzy logic to perform data labelling:  Needed to locate an appropriate receipt parser (https://github.com/mre/receipt-parser) and to test its effectiveness for labelling the data.
* Project Management:
  * Conducting a pre-project kickoff helps to set the tone and expectations of the project:
    * Create the user story.
    * Breakdown the user story into tasks.
    * Create and assign tasks to team members.
    * Conduct preparations for the project including GitHub and communications with stakeholders.
  * Conducting a project kickoff at 1st day helps to clarify doubts, breakdown assumptions, and ensure that every team member understands the project and the tasks to be completed:
    * Create architectural diagram.
    * Create overall process flows.
* Project Agile Development:
  * Using a single sprint for a four-day hack is conducive for the project team as it allows the team members to focus on the tasks without overmanaging the project within a short project duration of only 15 hours:
    * Each day separated into 2 sessions (AM and PM).
    * Each session is 3 hours.
    * Before start of each day, 10 min stand-up where each member shares work performed and work to be completed for the day.
    * At end of each day, 10 min stand-up where each member wraps up the day's work.
