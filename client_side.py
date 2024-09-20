# client.py
import socket

class HL7Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_message(self, hl7_message):
        # Wrap the message in MLLP format
        mllp_message = self.wrap_in_mllp(hl7_message)

        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # Connect the socket to the server
                sock.connect((self.host, self.port))

                # Send the MLLP wrapped message
                sock.sendall(mllp_message.encode('utf-8'))

                # Receive acknowledgment
                response = sock.recv(4096).decode('utf-8')
                # Unwrap the acknowledgment
                unwrapped_response = self.unwrap_mllp(response)
                return unwrapped_response

            except socket.error as e:
                print(f"Socket error: {e}")
                return None
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None

    def wrap_in_mllp(self, hl7_message):
        # MLLP frame characters
        SB = '\x0b'  # Start Block
        EB = '\x1c'  # End Block
        CR = '\x0d'  # Carriage Return

        # Wrap the HL7 message with MLLP framing
        mllp_message = f"{SB}{hl7_message}{EB}{CR}"
        return mllp_message

    def unwrap_mllp(self, mllp_message):
        # MLLP frame characters
        SB = '\x0b'  # Start Block
        EB = '\x1c'  # End Block
        CR = '\x0d'  # Carriage Return

        # Remove the MLLP framing characters
        if mllp_message.startswith(SB):
            mllp_message = mllp_message[1:]
        if mllp_message.endswith(CR):
            mllp_message = mllp_message[:-1]
        if mllp_message.endswith(EB):
            mllp_message = mllp_message[:-1]

        return mllp_message
    
    
    
