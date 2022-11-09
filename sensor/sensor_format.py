import struct
def form(form,data):
    """
    contains the formatting for raw measurements
    Parameters
    ----------
    form : string
        name of formatting method
    data : byte array
        data to be formatted 
    Returns
    -------
    result : string
        formatted data
    """
    result=-1
    form=form.casefold()
    print("form:{}".format(form))

    if form=="temp_ada":
        val=data[0] << 8 | data[1]
        result=(val & 0xFFF)/16.0
        if val & 0x1000:
            result -=256.0


    elif form=="atlas":
        result=list(map(lambda x: chr(x & ~0x80),list(data)))
        result=result[1:6]
        result="".join(map(str,result))

    elif form=="byte":
        result=struct.unpack('f',data)
        result="".join(map(str,result))
        

    return result