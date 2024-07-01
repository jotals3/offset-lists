import json

INPUT_FILE = "../tracking.json"
OUTPUT_FILE = "hashlist_10_ordered.txt"

with open(INPUT_FILE, 'r') as file:
    data = json.load(file)

offset_hashlist = []

for key in data:
    if len(data[key]["tracking"]) > 0 and data[key]["popularity"] >= 10:
        hashlist_entry = []

        hashlist_entry.append(data[key]["hash"])  # hash of the resource
        hashlist_entry.append(str(len(data[key]["tracking"])))  # number of ast to block
      
        # need to order the ast list for the plugin to work
        offset_lengths = {}
        sum_bytes = 0
        for ast in data[key]["tracking"]:
            offset_lengths[ast["offset"]] = ast["length"]
            sum_bytes += ast["length"]

        offset_lengths = dict(sorted(offset_lengths.items()))
        hashlist_entry.append(str(sum_bytes))

        for key in offset_lengths:
            hashlist_entry.append(str(key))
            hashlist_entry.append(str(key+offset_lengths[key]))
    
        offset_hashlist.append(hashlist_entry)

print(f"offset hashlist size: {len(offset_hashlist)}")

str_lines = [','.join(entry) for entry in offset_hashlist]

with open(OUTPUT_FILE, 'w') as file:
    file.write('\n'.join(str_lines))


# Data store format:
#
# resource_hash, number_asts, bytes_to_remove, start_ast1, end_ast1, start_ast2, end_ast2 [...]
#
