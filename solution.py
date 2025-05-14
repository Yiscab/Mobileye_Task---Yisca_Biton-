import json
from typing import List
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)
class Solution:
    def __init__(self, data_file_path: str, protocol_json_path: str):
        self.data_file_path = data_file_path
        self.protocol_json_path = protocol_json_path

    def _read_data_file(self) -> set[str]:
        """Reads the data file and extracts protocol IDs."""
        try:
            with open(self.data_file_path, 'r') as file:
                data = file.readlines()
            return {line.split()[0] for line in data if line.split()[0]}  # Extract protocol IDs
        except FileNotFoundError:
            logging.error(f"Error: The file {self.data_file_path} was not found.")
            return set()

    def _read_protocol_json(self, version_key: str) -> set[str]:
        """Reads the protocol JSON file and extracts protocols for the given version."""
        try:
            with open(self.protocol_json_path, 'r') as json_file:
                protocol_data = json.load(json_file)
            if version_key not in protocol_data["protocols_by_version"]:
                logging.error(f"Error: The version key {version_key} was not found in the protocol data.")
                return set()
            return set(protocol_data["protocols_by_version"][version_key]["protocols"])
        except FileNotFoundError:
            logging.error(f"Error: The file {self.protocol_json_path} was not found.")
            return set()
        except KeyError as e:
            logging.error(f"Error: Missing key in protocol.json - {e}")
            return set()
        
            
    # Question 1: What is the version name used in the communication session?
    def q1(self) -> str:
        try:
        # Read the data file and extract the version name
            with open(self.data_file_path, 'r') as file:
                data = file.readlines()
                if len(data) == 0:
                    logging.error("Error: The data file is empty.")
                    return None
            
                first_message = data[0].strip()  # Read the first line of the file and strip whitespace
                logging.info(f"First message: {first_message}")
            
            # Ensure there is at least one message in the file
                if '0x1' in first_message:
                    logging.info("'0x1' found in the first message.")
                    if 'bytes,' in first_message:
                        logging.info("'bytes,' found in the first message.")
                        byte_part = first_message.split('bytes,', 1)[1].strip()
                        logging.info(f"Byte part: {byte_part}")
                        bytes_list = byte_part.split()
                        if len(bytes_list) > 0:
                            first_byte = bytes_list[0]
                            logging.info(f"First byte: {first_byte}")
                            version_name = chr(int(first_byte, 16))
                            logging.info(f"Version name: {version_name}")
                            return version_name
                        else:
                            logging.error("Error: No bytes found after 'bytes,'.")
                else:
                    logging.error("Error: '0x1' not found in the first message.")
            return None
        except FileNotFoundError:
            logging.error(f"Error: The file {self.data_file_path} was not found.")
            return None
        except ValueError as e:
            logging.error(f"Error: Failed to convert byte to integer - {e}")
            return None

    # Question 2: Which protocols have wrong messages frequency in the session compared to their expected frequency based on FPS?
    def q2(self) -> List[str]:
        try:
        # Read the data file and extract the version name
            with open(self.data_file_path, 'r') as file:
                data = file.readlines()
            protocol_ids = [line.split()[0] for line in data if '0x' in line] #Extract protocol IDs from lines containing '0x'
            
            # Count occurrences of each protocol ID
            actual_frequencies = Counter(protocol_ids)
            
            # Read the expected frequencies from protocol.json
            with open(self.protocol_json_path, 'r') as json_file:
                protocol_data = json.load(json_file)  # Load protocol data from JSON file
            
            # Compare actual frequencies with expected frequencies
            mismatched_protocols = []
            for protocol_id, protocol_info in protocol_data["protocols"].items():
                expected_frequency = protocol_info["fps"]
                actual_frequency = actual_frequencies.get(protocol_id, 0)  # Get the actual frequency for the protocol IDcted frequency from protocol data
                if actual_frequency != expected_frequency:
                    mismatched_protocols.append(protocol_id)
            return mismatched_protocols
        except FileNotFoundError:
            print(f"Error: The file {self.data_file_path} was not found.")
            return []
        

    # Question 3: Which protocols are listed as relevant for the version but are missing in the data file?
    def q3(self, version_key:str) -> List[str]:
        """
        Identify protocols listed as relevant for the specified version but missing in the data file.
        
        Args:
            version_key (str): The version key to check (e.g., "Version1", "Version2").
        
        Returns:
            List[str]: A list of missing protocols.
        """
        
        actual_protocols = self._read_data_file()#Extract protocol IDs from lines containing '0x'
        expected_protocols = self._read_protocol_json(version_key)  # Read expected protocols from JSON file
        missing_protocols = expected_protocols - actual_protocols  # Find protocols in JSON not in data file
        return list(missing_protocols)

    # Question 4: Which protocols appear in the data file but are not listed as relevant for the version?
    def q4(self,version_key:str) -> List[str]:
        """
        Identify protocols listed as relevant for the specified version but missing in the data file.
        
        Args:
            version_key (str): The version key to check (e.g., "Version1", "Version2").
        
        Returns:
            List[str]: A list of missing protocols.
        """
        try:
            # Use helper functions to read actual and expected protocols
            actual_protocols = self._read_data_file()  # Extract protocol IDs from the data file
            expected_protocols = self._read_protocol_json(version_key)  # Extract expected protocols from JSON
            
            # Find protocols that are in the data file but not in the expected list
            unexpected_protocols = actual_protocols - expected_protocols
            
            return list(unexpected_protocols)
        except FileNotFoundError as e:
            logging.error(f"Error: {e}")
            return []
        except KeyError as e:
            logging.error(f"Error: Missing key in protocol.json - {e}")
            return []

    # Question 5: Which protocols have at least one message in the session with mismatch between the expected size integer and the actual message content size?
    def q5(self) -> List[str]:
        pass

    # Question 6: Which protocols are marked as non dynamic_size in protocol.json, but appear with inconsistent expected message sizes Integer in the data file?
    def q6(self) -> List[str]:
        pass


Solution = Solution("data.txt", "protocol.json")
# Example usage
if __name__ == "__main__":
    print("------- q1 --------")
    print(Solution.q1())
    print("------- q2 --------")
    print(Solution.q2())
    print("------- q3 --------")
    print(Solution.q3("Version1"))
    print("------- q3 --------")
    print(Solution.q3("Version2"))
    print("------- q4 --------")
    print(Solution.q4("Version1"))
    print("------- q4 (version2) --------")
    print(Solution.q4("Version2"))
    # print(Solution.q5())
    # print(Solution.q6())

