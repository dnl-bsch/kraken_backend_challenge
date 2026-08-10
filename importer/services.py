def parse_file(file_path: str) -> list[str]:
    """
    Read a file and return its lines as a list of strings.

    Parameters
    ----------
    file_path
        Path to the file to read.

    Returns
    -------
        Lines of the file, each retaining its newline character.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()
    return lines


def read_d0010(lines: list[str]) -> list[dict]:
    """
    Parse D0010 flow lines into a structured list of meter point readings.

    Parameters
    ----------
    lines
        Raw lines from a D0010 file, including header (ZHV) and trailer (ZPT)
        records.

    Returns
    -------
        List of meter point dicts.
    """
    meter_points = []
    current_mpan = None
    current_meter = None

    # TODO skipping information in ZHV / ZPT: header/trailer for now, maybe add later

    for line in lines:
        line = line.rstrip("\n").rstrip("$")
        if not line:
            continue
        fields = line.split("|")
        record_type = fields[0]

        if record_type == "026":
            current_mpan = {"mpan": fields[1], "meters": []}
            meter_points.append(current_mpan)
        elif record_type == "028":
            current_meter = {"serial_number": fields[1], "readings": []}
            current_mpan["meters"].append(current_meter)
        elif record_type == "030":
            current_meter["readings"].append({
                "register_id": fields[1],
                "reading_datetime": fields[2],  # parse as YYYYMMDDHHMMSS
                "reading_value": fields[3],
            })

    return meter_points
