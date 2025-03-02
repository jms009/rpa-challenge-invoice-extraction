import os
import re
import pytesseract
import pandas as pd
import requests
from PIL import Image
from datetime import datetime
from playwright.sync_api import sync_playwright

# Set path to Tesseract executable (update this if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Output directories
invoice_dir = "temp/invoices"
csv_file = "temp/invoices.csv"

# Ensure directories exist
os.makedirs(invoice_dir, exist_ok=True)

def launch_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://rpachallengeocr.azurewebsites.net/")
    return p, browser, page

def extract_text_from_image(invoice_page, invoice_id):
    image_url = invoice_page.locator("img[src*='jpg']").get_attribute("src")
    image_path = os.path.join(invoice_dir, f"{invoice_id}.jpg")
    image_response = requests.get(image_url)
    with open(image_path, "wb") as file:
        file.write(image_response.content)

    print(f"Image saved for Invoice {invoice_id}")
    extracted_text = pytesseract.image_to_string(Image.open(image_path)).strip()
    return extracted_text

def invoice_jpg_details(extracted_text):
    invoice_no_match = re.search(r"Invoice\s*(?:#\s*)?(\d+)", extracted_text)
    invoice_no = invoice_no_match.group(1) if invoice_no_match else None

    invoice_date_match = re.search(r"(\d{4}-\d{2}-\d{2})", extracted_text)
    invoice_date = invoice_date_match.group(1) if invoice_date_match else None

    company_name_match = re.search(r"(.*?)\s+INVOICE", extracted_text)
    company_name = company_name_match.group(1).strip() if company_name_match else None

    total_due_match = re.search(r"Total\s+([\d,.]+)", extracted_text)
    total_due = total_due_match.group(1) if total_due_match else None

    return invoice_no, invoice_date, company_name, total_due

def extract_invoice_data(page):
    invoices_data = []

    while True:
        rows = page.locator("table tbody tr").all()

        for row in rows:
            columns = row.locator("td").all()
            invoice_id = columns[1].inner_text().strip()
            due_date_str = columns[2].inner_text().strip()

            due_date = datetime.strptime(due_date_str, "%d-%m-%Y")
            if due_date <= datetime.today():
                with page.expect_popup() as popup_info:
                    row.get_by_role("link").click()
                invoice_page = popup_info.value

                extracted_text = extract_text_from_image(invoice_page, invoice_id)
                invoice_page.close()

                invoice_no, invoice_date, company_name, total_due = invoice_jpg_details(extracted_text)
                invoices_data.append([invoice_id, due_date_str, invoice_no, invoice_date, company_name, total_due])

        next_button = page.locator(".paginate_button.next")
        if "disabled" in next_button.get_attribute("class"):
            break
        next_button.click()

    df = pd.DataFrame(invoices_data, columns=["ID", "DueDate", "InvoiceNo", "InvoiceDate", "CompanyName", "TotalDue"])
    df["DueDate"] = pd.to_datetime(df["DueDate"], format="%d-%m-%Y").dt.strftime("%d-%m-%Y")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%Y-%m-%d").dt.strftime("%d-%m-%Y")
    df.to_csv(csv_file, index=False)

def main():
    p, browser, page = launch_browser()
    page.get_by_role("button", name="START").click()
    page.wait_for_timeout(1000)

    extract_invoice_data(page)

    file_input = page.locator('input[type="file"][name="csv"]')
    file_input.set_input_files(csv_file)

    print(f"Extraction complete. Data saved to {csv_file} and submitted.")
    input("Press Enter to close...")
    browser.close()
    p.stop()

if __name__ == "__main__":
    main()
