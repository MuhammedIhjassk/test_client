from hl7apy.core import Message
from hl7apy.exceptions import ValidationError
from client_side import *
import logging



def construct_adt_a01_message(patient_data):
    try:
        # Verify patient_data contains all required keys
        required_keys = ["MSH", "PID", "NK1", "PV1", "AL1", "EVN"]
        for key in required_keys:
            if key not in patient_data:
                raise KeyError(f"Missing key: {key}")

        # Create the ADT^A01 HL7 message
        message = Message("ADT_A01")

        # MSH Segment
        msh = message.msh
        msh.msh_1 = patient_data["MSH"].get("FieldSeparator", "|")
        msh.msh_2 = patient_data["MSH"].get("EncodingCharacters", "^~\\&")
        msh.msh_3 = patient_data["MSH"].get("SendingApplication", "")
        msh.msh_4 = patient_data["MSH"].get("SendingFacility", "")
        msh.msh_5 = patient_data["MSH"].get("ReceivingApplication", "")
        msh.msh_6 = patient_data["MSH"].get("ReceivingFacility", "")
        msh.msh_7 = patient_data["MSH"].get("DateTimeOfMessage", "")
        msh.msh_9 = patient_data["MSH"].get("MessageType", "ADT^A01")
        msh.msh_10 = patient_data["MSH"].get("MessageControlID", "")
        msh.msh_11 = patient_data["MSH"].get("ProcessingID", "")
        msh.msh_12 = patient_data["MSH"].get("VersionID", "2.5.1")

        # EVN Segment
        evn = message.evn
        evn.evn_1 = patient_data["EVN"].get("EventTypeCode", "A01")
        evn.evn_2 = patient_data["EVN"].get("RecordedDateTime", "")
        evn.evn_3 = patient_data["EVN"].get("DateTimePlannedEvent", "")
        evn.evn_4 = patient_data["EVN"].get("EventReasonCode", "")

        # PID Segment
        pid = message.pid
        pid.pid_1 = patient_data["PID"].get("SetID_PID", "")
        pid.pid_3 = patient_data["PID"].get("PatientIdentifierList", "")
        patient_name = patient_data["PID"].get("PatientName", {})
        pid.pid_5 = f"{patient_name.get('FamilyName', '')}^{patient_name.get('GivenName', '')}^{patient_name.get('MiddleInitialOrName', '')}^{patient_name.get('Suffix', '')}^{patient_name.get('Prefix', '')}"
        pid.pid_7 = patient_data["PID"].get("DateOfBirth", "")
        pid.pid_8 = patient_data["PID"].get("AdministrativeSex", "")
        patient_address = patient_data["PID"].get("PatientAddress", {})
        pid.pid_11 = f"{patient_address.get('StreetAddress', '')}^^{patient_address.get('City', '')}^{patient_address.get('State', '')}^{patient_address.get('Zip', '')}^{patient_address.get('Country', '')}"
        pid.pid_13 = patient_data["PID"].get("PhoneNumberHome", "")
        pid.pid_14 = patient_data["PID"].get("PhoneNumberBusiness", "")
        pid.pid_16 = patient_data["PID"].get("MaritalStatus", "")
        pid.pid_19 = patient_data["PID"].get("SSNNumberPatient", "")

        # NK1 Segment
        nk1 = message.nk1
        nk1.nk1_1 = patient_data["NK1"].get("SetID_NK1", "")
        name = patient_data["NK1"].get("Name", {})
        nk1.nk1_2 = f"{name.get('FamilyName', '')}^{name.get('GivenName', '')}^{name.get('MiddleInitialOrName', '')}"
        nk1.nk1_3 = patient_data["NK1"].get("Relationship", "")
        address = patient_data["NK1"].get("Address", {})
        nk1.nk1_4 = f"{address.get('StreetAddress', '')}^^{address.get('City', '')}^{address.get('State', '')}^{address.get('Zip', '')}^{address.get('Country', '')}"
        nk1.nk1_5 = patient_data["NK1"].get("PhoneNumber", "")

        # PV1 Segment
        pv1 = message.pv1
        pv1.pv1_1 = patient_data["PV1"].get("SetID_PV1", "")
        pv1.pv1_2 = patient_data["PV1"].get("PatientClass", "")
        assigned_location = patient_data["PV1"].get("AssignedPatientLocation", {})
        pv1.pv1_3 = f"{assigned_location.get('PointOfCare', '')}^{assigned_location.get('Room', '')}^{assigned_location.get('Facility', '')}"
        attending_doctor = patient_data["PV1"].get("AttendingDoctor", {})
        pv1.pv1_7 = f"{attending_doctor.get('ID', '')}^{attending_doctor.get('FamilyName', '')}^{attending_doctor.get('GivenName', '')}^{attending_doctor.get('MiddleInitialOrName', '')}^{attending_doctor.get('Degree', '')}"
        referring_doctor = patient_data["PV1"].get("ReferringDoctor", {})
        pv1.pv1_8 = f"{referring_doctor.get('ID', '')}^{referring_doctor.get('FamilyName', '')}^{referring_doctor.get('GivenName', '')}^{referring_doctor.get('MiddleInitialOrName', '')}^{referring_doctor.get('Degree', '')}"
        pv1.pv1_44 = patient_data["PV1"].get("AdmitDateTime", "")

        # AL1 Segment
        al1 = message.al1
        al1.al1_1 = patient_data["AL1"].get("SetID_AL1", "")
        al1.al1_2 = patient_data["AL1"].get("AllergenTypeCode", "")
        al1.al1_3 = patient_data["AL1"].get("Allergen", "")
        al1.al1_4 = patient_data["AL1"].get("AllergySeverityCode", "")
        al1.al1_5 = patient_data["AL1"].get("IdentificationDate", "")

        # Validate the message   
        try:
            message.validate()
            print("Message is valid.")
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None

        # Convert to ER7 format and split segments
        hl7_message = message.to_er7()
        segments = hl7_message.split("\r")
        
        # Join segments with newline for better readability
        formatted_message = "\n".join(segments)
        
        return formatted_message
    
    except KeyError as e:
        print(f"Error: {e}")
        return None   

# Example patient data (ensure this is correctly defined in your script)
patient_data = {
    "MSH": {
        "FieldSeparator": "|",
        "EncodingCharacters": "^~\\&",
        "SendingApplication": "HIS",
        "SendingFacility": "Hospital",
        "ReceivingApplication": "NABIDH",
        "ReceivingFacility": "NABIDH",
        "DateTimeOfMessage": "20230910120000",
        "MessageType": "ADT^A01",
        "MessageControlID": "123456789",
        "ProcessingID": "P",
        "VersionID": "2.5.1"
    },
    "PID": {
        "SetID_PID": "1",
        "PatientIdentifierList": "12345678^^^Hospital^MR",
        "PatientName": {
            "FamilyName": "Doe",
            "GivenName": "John",
            "MiddleInitialOrName": "A",
            "Suffix": "III",
            "Prefix": "Mr."
        },
        "DateOfBirth": "19900101",
        "AdministrativeSex": "M",
        "PatientAddress": {
            "StreetAddress": "123 Main St",
            "City": "City",
            "State": "State",
            "Zip": "12345",
            "Country": "USA"
        },
        "PhoneNumberHome": "(123)456-7890",
        "PhoneNumberBusiness": "(321)654-9870",
        "MaritalStatus": "S",
        "SSNNumberPatient": "987-65-4321"
    },
    "NK1": {
        "SetID_NK1": "1",
        "Name": {
            "FamilyName": "Doe",
            "GivenName": "Jane",
            "MiddleInitialOrName": "A"
        },
        "Relationship": "SPO",
        "Address": {
            "StreetAddress": "123 Oak St",
            "City": "City",
            "State": "State",
            "Zip": "12345",
            "Country": "USA"
        },
        "PhoneNumber": "(987)654-3210"
    },
    "PV1": {
        "SetID_PV1": "1",
        "PatientClass": "I",
        "AssignedPatientLocation": {
            "PointOfCare": "ER",
            "Room": "01",
            "Facility": "Hospital"
        },
        "AttendingDoctor": {
            "ID": "12345",
            "FamilyName": "Smith",
            "GivenName": "John",
            "MiddleInitialOrName": "A",
            "Degree": "Dr."
        },
        "ReferringDoctor": {
            "ID": "67890",
            "FamilyName": "Jones",
            "GivenName": "Mary",
            "MiddleInitialOrName": "B",
            "Degree": "Dr."
        },
        "AdmitDateTime": "20230910"
    },
    "AL1": {
        "SetID_AL1": "1",
        "AllergenTypeCode": "DA",
        "Allergen": "Penicillin",
        "AllergySeverityCode": "SV",
        "IdentificationDate": "NKA"
    },
    "EVN": {
        "EventTypeCode": "A01",
        "RecordedDateTime": "20230910120000",
        "DateTimePlannedEvent": "",
        "EventReasonCode": ""
    }
}
# Usage
hl7_message = construct_adt_a01_message(patient_data)
if hl7_message:
    print(hl7_message)

    # Send the HL7 message using HL7Client
    server_host = '127.0.0.1'  # Update to the actual server address
    server_port = 5000          # Update to the actual server port

    client = HL7Client(server_host, server_port)
    response = client.send_message(hl7_message)
    
    if response:
        print("Received acknowledgment:")
        print(response)
    else:
        print("Failed to receive acknowledgment.")




    

    
