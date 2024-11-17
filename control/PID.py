def PID(input, lastInput, setpoint, kp, ki, kd, er=0, max=100, min=0):
    e = setpoint - input
    er += e
    ei = input - lastInput
    out = kp * e + ki * er - kd * ei
    if out > max:
        out = max
    if out < min:
        out = min
    return out, er
