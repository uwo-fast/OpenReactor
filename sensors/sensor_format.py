import struct


def form(form, data):
    """
    Contains the formatting for raw measurements.

    Parameters
    ----------
    form : string
        Name of formatting method.
    data : byte array
        Data to be formatted.

    Returns
    -------
    result : string
        Formatted data.
    """
    result = -1
    form = form.casefold()
    print(f"Form: {form}")

    if form == "temp_ada":
        val = data[0] << 8 | data[1]
        result = (val & 0xFFF) / 16.0
        if val & 0x1000:
            result -= 256.0

    elif form == "atlas":
        result = list(map(lambda x: chr(x & ~0x80), list(data)))
        result = result[1:5]
        result = "".join(map(str, result))

    elif form == "byte":
        result = struct.unpack("f", data)
        result = "".join(map(str, result))

    return result
