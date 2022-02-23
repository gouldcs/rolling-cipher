import argparse

letter_to_idx = {
    'a':0, 'b':1, 'c':2, 'd':3, 'e':4,
    'f':5, 'g':6, 'h':7, 'i':8, 'j':9,
    'k':10, 'l':11, 'm':12, 'n':13, 'o':14,
    'p':15, 'q':16, 'r':17, 's':18, 't':19,
    'u':20, 'v':21, 'w':22, 'x':23, 'y':24, 'z':25
}

idx_to_letter = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e',
    5:'f', 6:'g', 7:'h', 8:'i', 9:'j', 10:'k', 11:'l',
    12:'m', 13:'n', 14:'o', 15:'p', 16:'q', 17:'r',
    18:'s', 19:'t', 20:'u', 21:'v', 22:'w', 23:'x',
    24:'y', 25:'z'}

def reverse_map(mapping):
    new_mapping = {}
    for k, v in mapping.items():
        new_mapping[v] = k
    print(new_mapping)

def calculate_index(current_index, letter_index, encoding=True):
    alphabet_size = len(idx_to_letter) - 1
    if encoding:
        if current_index + letter_index > alphabet_size:
            return (current_index + letter_index) - alphabet_size
        else:
            return (current_index + letter_index)
    else:
        if letter_index - current_index < 0:
            return alphabet_size + (letter_index - current_index)
        else:
            return (letter_index -  current_index)

def encode_from_text(text, sequence):
    current_index = 0
    tokens = text.lower()
    encoded = ""
    for letter in tokens:
        if letter.isalpha():
            idx = letter_to_idx[letter]
            sequence_offset = sequence[current_index]
            encoded_index = calculate_index(sequence_offset, idx)
            encoded_letter = idx_to_letter[encoded_index]
            encoded += encoded_letter
            current_index = current_index + 1 if current_index < len(sequence) - 1 else 0
        elif letter.isalnum():
            int_letter = int(letter) + sequence[current_index] if int(letter) + sequence[current_index] < 10 else (int(letter) + sequence[current_index]) - 10
            encoded += str(int_letter)
            current_index = current_index + 1 if current_index < len(sequence) - 1 else 0
        else:
            encoded += letter
    return encoded


def decode_from_text(text, sequence):
    current_index = 0
    tokens = text.lower()
    decoded = ""
    for letter in tokens:
        if letter.isalpha():
            idx = letter_to_idx[letter]
            sequence_offset = sequence[current_index]
            decoded_index = calculate_index(sequence_offset, idx, encoding=False)
            decoded_letter = idx_to_letter[decoded_index]
            decoded += decoded_letter
            current_index = current_index + 1 if current_index < len(sequence) - 1 else 0
        elif letter.isalnum():
            int_letter = int(letter) - sequence[current_index] if int(letter) - sequence[current_index] >= 0 else (int(letter) - sequence[current_index]) + 10
            decoded += str(int_letter)
            current_index = current_index + 1 if current_index < len(sequence) - 1 else 0
        else:
            decoded += letter
    return decoded


def parse_doc(path):
    message = ""
    with(open(path, 'r')) as readfile:
        for line in readfile:
            message += line

    return message

def write_message(path, message):
    with(open(path, 'w+')) as writefile:
        writefile.writelines(message)

    return path


def parse_sequence(sequence):
    return [int(a) for a in str(sequence)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform a rolling cypher on some text')
    parser.add_argument('-s', metavar='S', type=int, nargs=1, help='The rotation sequence as an integer')
    parser.add_argument('-i', metavar='I', type=str, nargs=1, help='The path to the input file')
    parser.add_argument('-t', metavar='T', type=str, nargs=1, help='Raw text to encode/decode')
    parser.add_argument('-e', metavar='E', type=str, nargs=1, help='The path to the output encoded file')
    parser.add_argument('-d', metavar='D', type=str, nargs=1, help='The path to the output decoded file')
    args = parser.parse_args()
    sequence = parse_sequence(args.s[0]) if args.s[0] else [1]
    input_text_from_file = args.i[0] if args.i is not None else None
    input_text_in_place = args.t[0] if args.t is not None else None
    output_encoded = args.e[0] if args.e[0] else './encoded.txt'
    output_decoded = args.d[0] if args.d[0] else './encoded.txt'

    if input_text_from_file is None and input_text_in_place is None:
        raise Exception("No input text provided!")
    elif input_text_from_file is None:
        text = input_text_in_place
    else:
        text = parse_doc(input_text_from_file)


    encoded = encode_from_text(text, sequence)
    write_message(output_encoded, encoded)

    text = encoded
    decoded = decode_from_text(text, sequence)
    write_message(output_decoded, decoded)

    print(f"Done! The encoded message can be found in {output_encoded} and the decoded in {output_decoded}")