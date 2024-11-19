def pid(
    input_value, last_input, setpoint, kp, ki, kd, er=0, max_output=100, min_output=0
):
    """
    PID control algorithm.

    Parameters
    ----------
    input_value : float
        Current process variable.
    last_input : float
        Previous process variable.
    setpoint : float
        Desired setpoint.
    kp : float
        Proportional gain.
    ki : float
        Integral gain.
    kd : float
        Derivative gain.
    er : float
        Cumulative error (integral term).
    max_output : float
        Maximum output limit.
    min_output : float
        Minimum output limit.

    Returns
    -------
    output : float
        Control output.
    er : float
        Updated cumulative error.
    """
    error = setpoint - input_value
    er += error
    derivative = input_value - last_input
    output = kp * error + ki * er - kd * derivative
    if output > max_output:
        output = max_output
    elif output < min_output:
        output = min_output
    return output, er
