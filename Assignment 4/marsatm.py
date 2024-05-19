# AUTHOR:   SANDER BETZ
# ST-NR:    6070000
# ST-MAIL:  S.H.R.Betz@student.tudelft.nl


def marsinit() -> list:
    marstable = []
    with open('Mars_Atmosphere/marsatm.txt', 'r') as dataFile:
        for line in dataFile.readlines():
            n = line.split(' ')
            if n[0] == '**':
                continue
            else:
                marstable.append([float(item.replace('\n', '')) for item in n if item != ''])
    return marstable

def marsatm(h, marstable) -> ...:
    R = 191.84  # gas constant

    def lin_interp(low_height, wanted_height, high_height, low_val, high_val) -> float:
        frac = (wanted_height - low_height) / (high_height - low_height)
        value = (1 - frac) * low_val + frac * high_val
        return value

    for i, (atm_height, atm_temp, atm_rho, atm_c) in enumerate(marstable[:-1]):
        if h < marstable[i + 1][0] * 1000:
            temp = lin_interp(atm_height * 1000, h, marstable[i + 1][0] * 1000, atm_temp, marstable[i + 1][1])
            rho = lin_interp(atm_height * 1000, h, marstable[i + 1][0] * 1000, atm_rho, marstable[i + 1][2])
            c = lin_interp(atm_height * 1000, h, marstable[i + 1][0] * 1000, atm_c, marstable[i + 1][3])
            p = 0
            return (p, temp, rho, c)

# main loop for debugging
if __name__ == '__main__':
    test_atm = marsinit()
    print(marsatm(20000, test_atm))