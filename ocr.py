import pytesseract
from PIL import Image
from fuzzywuzzy import process
import warnings

warnings.filterwarnings("ignore")

def extract_text_from_image(image_file_path):
    with Image.open(image_file_path) as img:
        text = pytesseract.image_to_string(img)
    return text

def fuzzy_match(text, options):
    
    best_match, score = process.extractOne(text, options)
    if score >= 90:
        return best_match
    else:
        return None

def parse_shipping_info(text):
    lines = text.split('\n')

    # Initialize variables to store information
    dateTimeDetails = {}
    customerDetails = {}
    orderDetails = {}
    staffDetails = {}

    # Define templates for each section
    dateTime_templates = ['Accepted at:', 'Completed at:', 'Boarded at:', 'Picked up at:']
    customer_templates = ['Name:', 'Address:', 'Phone:', 'Email:']
    order_templates = ['Name:', 'Price:', 'Trip type:']
    staff_templates = ['Name:', 'Phone:', 'Email:']

    current_section = None
    for line in lines:
        if 'Date time details' in line:
            current_section = 'dateTimeDetails'
        elif 'Customer details' in line:
            current_section = 'customerDetails'
        elif 'Order details' in line:
            current_section = 'orderDetails'
        elif 'Staff details' in line:
            current_section = 'staffDetails'
        elif current_section == 'dateTimeDetails':
            print(line)
            matched_prop = fuzzy_match(line, dateTime_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()
                dateTimeDetails[key] = value
        elif current_section == 'customerDetails':
            matched_prop = fuzzy_match(line, customer_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()
                customerDetails[key] = value
        elif current_section == 'orderDetails':
            matched_prop = fuzzy_match(line, order_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()
                orderDetails[key] = value
        elif current_section == 'staffDetails':
            matched_prop = fuzzy_match(line, staff_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()
                staffDetails[key] = value

    return dateTimeDetails, customerDetails, orderDetails, staffDetails

image_file_path = "/Users/admin/Desktop/Master CS/Data Engineering/Assignment/test.png"  # Provide the path to your image file
text = extract_text_from_image(image_file_path)
dateTimeDetails, customerDetails, orderDetails, staffDetails = parse_shipping_info(text)

print("DateTime Details:", dateTimeDetails)
print("Customer Details:", customerDetails)
print("Order Details:", orderDetails)
print("Staff Details:", staffDetails)
