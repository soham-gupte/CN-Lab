# Calculate IP fragmentation and flags for given inputs

data_size = int(input("Enter the data size: "))
mtu_size = int(input("Enter MTU size: "))
print()
# Default:
# mtu_size = 1500
# data_size = 4000

header_size = 20

# MTU part of code

total_data_size = data_size - header_size
frag_data_len = mtu_size - header_size
frag_data_len = frag_data_len - frag_data_len%8

frag_num = 0
res = []
offset = 0
remaining_data = total_data_size
total_data_len = 0
mf = 1

frag_data = 0

while remaining_data > 0 :
    if (remaining_data <= frag_data_len) :
        frag_data = remaining_data
        mf = 0
    else :
        frag_data = frag_data_len
    remaining_data = remaining_data - frag_data_len
    total_data_len += frag_data + header_size
    # res.append(list())
    print(f"Fragment no. {frag_num}:")
    print(f"Length = {frag_data}")
    print(f"MF flag = {mf}")
    print(f"Offset = {offset}\n")
    offset += int(frag_data_len/8)
    frag_num += 1

print(f"Total data length = {total_data_len}")
