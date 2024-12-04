class IPAddress:
    def __init__(self, ipaddress):
        if not isinstance(ipaddress, (list, tuple)) or len(ipaddress) != 4:
            raise ValueError("IP address must be a list or tuple of four integers.")
        self.check(ipaddress)
        self.ipaddress = ipaddress

    def check(self, my_list):
        for i in my_list:
            if i < 0 or i > 255:
                raise ValueError("Each number in the IP address must be between 0 and 255.")

    def __str__(self):
        return f"IP - {'.'.join(map(str, self.ipaddress))}"

    def __repr__(self):
        return f"IPAddress({self.ipaddress})"


# Example usage:
#1 Example with list input
# Uncomment the following lines to test with a list
# ip_list = [int(i) for i in input("Enter IP (separated by dots) - ").split(".")]
# my_ip = IPAddress(ip_list)

#2 Example with string input
# Uncomment the following lines to test with a string split into integers
# ip_str = input("Enter IP (separated by dots) - ")
# my_ip = IPAddress([int(i) for i in ip_str.split(".")])

#3 Example with tuple input
# Uncomment the following lines to test with a tuple
# ip_tuple = tuple(int(i) for i in input("Enter IP (separated by dots) - ").split("."))
# my_ip = IPAddress(ip_tuple)

# Depending on the desired input type, uncomment one of the above sections:
#1 - list
#2 - str
#3 - tuple
print(my_ip)  
print(repr(my_ip))
