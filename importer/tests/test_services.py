from django.test import TestCase
from pathlib import Path
from importer.services import parse_file, read_d0010

test_file_path = Path(__file__).resolve().parents[2] / "DTC5259515123502080915D0010.uff"

class ParseFileTest(TestCase):
    def test_parses_file(self):
        lines, filename = parse_file(test_file_path)
        assert len(lines) > 0
        assert filename == "DTC5259515123502080915D0010"


class SaveRecordsTest(TestCase):
    def test_read_d0010(self):

        filename = "DTC5259515123502080915D0010"

        lines = [
            "ZHV|0000475656|D0010002|D|UDMS|X|MRCY|20160302153151||||OPER|",
            "026|1234567890123|",
            "028|SN12345|",
            "030|R1|20240101120000|100.5|",
            "030|R2|20240101130000|200.0|",
            "028|SN67890|",
            "030|R1|20240101140000|150.0|",
            "ZPT|0000475656|35||11|20160302154650|",
        ]

        expected_output = {
            "source_file": "DTC5259515123502080915D0010",
            "meter_points": [
            {
                "mpan": "1234567890123",
                "meters": [
                    {
                        "serial_number": "SN12345",
                        "readings": [
                            {"register_id": "R1", "reading_datetime": "20240101120000", "reading_value": "100.5"},
                            {"register_id": "R2", "reading_datetime": "20240101130000", "reading_value": "200.0"},
                        ],
                    },
                    {
                        "serial_number": "SN67890",
                        "readings": [
                            {"register_id": "R1", "reading_datetime": "20240101140000", "reading_value": "150.0"},
                        ],
                    },
                ],
            }
        ]
        }

        assert read_d0010(lines, filename) == expected_output
