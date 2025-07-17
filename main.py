import phonenumbers
from phonenumbers import carrier, geocoder, timezone, NumberParseException, number_type, is_valid_number
import sys
import webbrowser
import json
import os
from datetime import datetime

LOG_FILE = "lookup_log.json"

def save_log(entry):
    data = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

    data.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def lookup_number():
    phone = input("\nEnter the number with country code (e.g., +12125551234): ")

    try:
        parsed = phonenumbers.parse(phone)
        if is_valid_number(parsed):
            country = geocoder.description_for_number(parsed, "en")
            operator = carrier.name_for_number(parsed, "en")
            zones = timezone.time_zones_for_number(parsed)
            e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            rfc3966 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.RFC3966)
            possible = phonenumbers.is_possible_number(parsed)
            num_type = number_type(parsed)

            type_dict_en = {
                0: "Unknown",
                1: "Fixed line",
                2: "Mobile",
                3: "Fixed or mobile",
                4: "Fax",
                5: "Emergency",
                6: "Pager",
                7: "UAN",
                8: "VoIP",
                9: "Personal number",
                10: "Voicemail",
                11: "Shared cost",
                12: "Voicemail",
                13: "Unknown"
            }
            num_type_str = type_dict_en.get(num_type, "Unknown")

            print("\n✅ Valid number")
            print(f"🌎 Country: {country}")
            print(f"📞 Carrier: {operator}")
            print(f"🕒 Timezone(s): {zones}")
            print(f"🔢 E164 format: {e164}")
            print(f"🔢 International format: {international}")
            print(f"🔢 National format: {national}")
            print(f"🔢 RFC3966 format: {rfc3966}")
            print(f"🔎 Possible number?: {'Yes' if possible else 'No'}")
            print(f"📱 Number type: {num_type_str}")

            log_entry = {
                "number": phone,
                "country": country,
                "carrier": operator,
                "timezones": list(zones),
                "e164": e164,
                "international": international,
                "national": national,
                "rfc3966": rfc3966,
                "possible": possible,
                "type": num_type_str,
                "timestamp": datetime.now().isoformat()
            }
            save_log(log_entry)
        else:
            print("❌ Invalid number")
    except NumberParseException as e:
        print(f"❌ Error: {e}")

def menu():
    while True:
        print("\n==============================")
        print("        LOOKUP TOOL")
        print("       by @batcheed")
        print("==============================")
        print("1. Phone Number Lookup")
        print("2. Exit")
        option = input("Choose an option: ")

        if option == "1":
            lookup_number()
            while True:
                again = input("\nDo you want to lookup another number? (y/n): ").lower()
                if again == 'y':
                    lookup_number()
                elif again == 'n':
                    break
                else:
                    print("Please enter 'y' or 'n'.")
        elif option == "2":
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    menu()
