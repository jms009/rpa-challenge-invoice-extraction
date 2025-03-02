
# 🐍 RPA Challenge OCR Invoice Extraction - Python

This project automates the process of extracting invoice details from the **RPA Challenge OCR website**: [https://rpachallengeocr.azurewebsites.net/](https://rpachallengeocr.azurewebsites.net/). It uses **Playwright** for web automation to interact with the website, and **Tesseract OCR** for optical character recognition (OCR) to extract text from invoice images. The extracted data is then structured into a CSV file and uploaded back to the website for processing.

### Key Features:
- **Automated Web Navigation**: Uses Playwright to navigate and interact with the web pages.
- **Invoice Image Extraction**: Downloads invoice images from the website for further processing.
- **OCR Processing**: Tesseract OCR extracts text from the downloaded invoice images.
- **Data Parsing**: Extracts relevant invoice details using regex.
- **CSV Generation**: Saves extracted data in a structured format.
- **Automated Submission**: Uploads the CSV file back to the site.

---

## Process Overview

### 1. **Launch Browser**:
   - The program begins by launching a Chromium browser instance using Playwright.
   - The browser navigates to the **RPA Challenge OCR website**, where it can interact with various elements to extract data.

### 2. **Invoice Data Extraction**:
   - The program searches the website for invoices that are due for processing.
   - For each invoice, the program clicks on the corresponding link to open the invoice details in a popup window.
   
### 3. **Image Download**:
   - The invoice image URL is extracted from the webpage, and the image is downloaded using the `requests` library.
   - The image is saved locally in the `temp/invoices` folder to be processed later. This ensures that images are organized and easily accessible.

### 4. **OCR Processing**:
   - **Tesseract OCR** is used to extract text from the downloaded invoice image.
   - The extracted text is then processed using **regular expressions (regex)** to identify the necessary details, such as:
     - **Invoice Number**: The unique identifier for the invoice.
     - **Invoice Date**: The date the invoice was issued.
     - **Company Name**: The name of the company issuing the invoice.
     - **Total Due**: The total amount due on the invoice.

### 5. **Data Structuring**:
   - The extracted data is stored in a structured format using **pandas** DataFrame.
   - The DataFrame is then converted into a CSV file, which contains the following columns:
     - **Invoice ID**: Unique ID of the invoice.
     - **Due Date**: The due date of the invoice.
     - **Invoice Number**: Extracted invoice number.
     - **Invoice Date**: Extracted invoice date.
     - **Company Name**: Extracted company name.
     - **Total Due**: Extracted total due amount.
   - The generated CSV file is saved in the `temp` folder, specifically in the `temp/invoices.csv` file.

### 6. **Upload Data**:
   - The generated CSV file is automatically uploaded back to the website for processing. This is done by interacting with the appropriate input field on the site using Playwright.

---

## Tech Stack and Dependencies

This project utilizes **Python** and the following key libraries:

| Package        | Purpose |
|----------------|---------|
| `playwright`   | Automates browser interactions for web scraping and automation. |
| `pytesseract`  | Performs OCR to extract text from invoice images. |
| `pandas`       | Used for data processing, structuring, and saving the extracted data in CSV format. |
| `Pillow`       | Provides image processing utilities (used for opening and handling images). |
| `requests`     | Downloads invoice images from URLs. |

### Dependencies Installation:
To install the required dependencies, make sure you have **Python** installed, then use the following command to install them:

```bash
pip install -r requirements.txt

```

---


### License
This project is licensed under the **MIT License**. Please see the `LICENSE` file for more details.