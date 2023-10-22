## Regex to DFA Converter

A Python implementation to convert Regular Expressions (regex) into Deterministic Finite Automatons (DFA). For Pitt CS1502

### Overview

This tool receives a regular expression as input and produces a Deterministic Finite Automaton (DFA) capable of recognizing the language represented by that regular expression. The transformation is achieved in two stages:

1. Conversion of the regex into a Non-deterministic Finite Automaton (NFA).
2. Conversion of the NFA into a DFA.

### Features

- **Custom Stack Implementation**: For parsing and evaluation of the regex.
- **NFA and DFA Classes**: Distinct classes to represent NFA and DFA and operations on them.
- **Epsilon-closure Computations**: Compute the epsilon-closure of states in an NFA.
- **Relabelling DFA States**: Ensures DFA states are represented with contiguous numerical identifiers.
- **Error Handling**: Detects and reports errors in the regex, such as unmatched parenthesis or missing operands.

### Prerequisites

- Python 3.x

### How to Use

1. Clone the repository

2. cd in

3. Run the program:
   ```
   python converter.py [input-file] [output-file]
   ```

   - `input-file`: Contains the alphabet in the first line and the regular expression in the second line. Following lines contain strings for which you want to check acceptance.
   - `output-file`: Will contain the results (`true` or `false`) for each string in the input file, indicating whether the DFA derived from the regex accepts it.

### Example

For an input file `input.txt` with content:
```
ab
(a|b)*
aa
ba
```

The output file will contain:
```
true
true
```

### Limitations

- The tool assumes that the regex is well-formed. It does provide error messages for some common mistakes, but it's not exhaustive.
- The tool handles only basic regex operators: `*`, `|`, and concatenation.

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### License

[MIT](https://choosealicense.com/licenses/mit/)

### Author

Sade Benjamin

---

For more details, refer to the source code comments and documentation.
