# snake 1 
import re

msg = """YXu0hYq1xQ4,hQXUCw8Cs7nIu8BAxIUADYf\n\nLRYUYw5LI0RYUUYs6hDXU3UIoIBbcm\n.CBSA5LI7RYUU
Ys2hDXU8YBbnIj\n.UIoIBbnI2LI8RYUUYs7hDXU2cYBbnQZ\n.cYBbnQo1LI9RYUUYs7hDXU4UDBk\n.JYUDoIB
bnQo4LI3RYUUYs8hDXU6YLRDbj\n.JYULYh8LI3RYUUYs8hDXU1CUIBIsDJDYH\n.YLhYJ7BDIoYbj\n.LUhAQ
o0LYLDo3U'hYRD2BDIoYbL2XSAQhY0QU0MDYRs0YXU4XSAQXUBW\n.LYBAR8CUIBDoIUoDRb1LUDYs2L
RQRRm\n.CUIRAb3JBAQXL6RYlYh9LLDb0LLYBha\n.CBUhYBIL0CBUIoIBbcY9hg\n.JYohYBIL1YXU5YoDx7x
Q6,CUIASIsnD8YLAxYR0YXU9hQIUDUbnYU4QU3YRYXu\n.LLYAS1JBAQXL7Ys3--
YhQ2JhD2CBsDRYxYRb2CBhQ9YhQ6LAQIlsQ--
9CDO7QU1QJ0XSAQXUBW\n.UI4UDXU5CDO0CDn2UQh7Ys2LAQIlsQ0UD2ULRIx8LLYBhA2YR'AQC1OQe\n.
XoUAv7LI3RYUUYs0hDXU8XSAQXUBW\n.RYlYh0RYlYh5LI9hYUxQ0RYUUYs2hDXU8*UXSIR*9xg\n.OQh4Y
XU3hQIUDUhYnYBbnI9LI1JRDX0QU6,hIDBbcY5L'UI3D7JDs6xg\n.DYJI4YXU6hQIUDUhYnYBbnI9LI9CLDY4Q
U3,hIDBbcY2UI5CDn4Ys8D8JQQS1LYoDbLYnDe\n.DYJI0YRD9YhQ6ShIMhQX2UDYRS4DYJI3--
9L'UYB5QJ8YRQn9xQ0!YLQXU"""

dict = {'s': 'L', 'b': 's', 'w': 'O', 'z': 'G', 'c': 'o', 'J': 'y', 'V': 't', 'P': 'w', 'B': 'f', 'Z': 'q', 'F': 'k', 'O': 'N', 'u': 'A', 'W': 'r', 'K': 'K', 'a': 'D', 'v': 'l',
'g': 'S', 'f': 'x', 'x': 'c', 'N': 'e', 'p': 'b', 'U': 'a', 'j': 'P', 'o': 'Q', 'i': 'I', 'M': 'd', 't': 'U', 'H': 'V', 'X': 'i', 'Y': 'T', 'R': 'H', 'h': 'X', 'L': 'z',
'G': 'F', 'A': 'W', 'm': 'n', 'T': 'u', 'l': 'B', 'C': 'Z', 'q': 'p', 'D': 'v', 'I': 'g', 'n': 'h', 'y': 'C', 'S': 'j', 'k': 'M', 'd': 'J', 'Q': 'E', 'e': 'Y', 'r': 'R',
'E': 'm'}

rev_dict = {value:key for key,value in dict.items()}



print(" ".join([word[::-1] for word in re.split(r'\d',(''.join(rev_dict.get(ch, ch) for ch in msg)).replace("\n"," "))]))
