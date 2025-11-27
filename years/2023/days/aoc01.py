DIGITS = { str(n): n for n in range(1, 10) }
WORDS = { word: index + 1 for index, word in enumerate(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]) }

class TrebuchetCalibrator:
    def __init__(self, digit_map):
        self.__forward_map = digit_map
        self.__reverse_map = { k[::-1]: v for k, v in self.__forward_map.items() }
        self.__forward_starts = { k[0] for k in self.__forward_map }
        self.__reverse_starts = { k[-1] for k in self.__reverse_map }

    def __find_value(self, line, digit_map, start_characters):
        for i, c in enumerate(line):
            if c not in start_characters:
                continue
            substring = line[i:]
            for name, value in digit_map.items():
                if substring.startswith(name):
                    return value
        return 0

    def parse_line(self, line):
        return self.__find_value(line, self.__forward_map, self.__forward_starts) * 10 \
            + self.__find_value(line[::-1], self.__reverse_map, self.__reverse_starts)

    def get_calibration_sum(self, lines):
        return sum(map(self.parse_line, lines))


def solve(calibration_document):
    ans1 = TrebuchetCalibrator(DIGITS).get_calibration_sum(calibration_document)
    ans2 = TrebuchetCalibrator(DIGITS | WORDS).get_calibration_sum(calibration_document)
    return ans1, ans2
