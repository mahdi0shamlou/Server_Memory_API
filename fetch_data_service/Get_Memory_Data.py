import os

def get_ram_info():
    try:
        process = os.popen('free -m')
        output = process.read()
        process.close()
        lines = output.split("\n")

        data_line = lines[1].split()
        total, used, free = int(data_line[1]), int(data_line[2]), int(data_line[3])

        return {'total': total, 'used': used, 'free': free}
    except Exception as e:
        print(f"Error fetching RAM info: {e}")
        return None

