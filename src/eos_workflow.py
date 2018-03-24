import pw_input
import pw_job
import json
import numpy
import scipy.optimize

PSEUDO_DIR = '../../../pseudo'
runner = pw_job.PWJobRunner('./scripts/runtime', '../../../bin/pw.x')

def run_crude_guess(input_obj, press, test_name):
    input_obj.nml.update({
        'CELL': {
            'press': press
        }
    })
    output = runner.run(test_name, input_obj.dump())
    return output.output.total_energy.etot

def run_vc_relax(input_obj, press, test_name):
    input_obj.nml.update({
        'CELL': {
            'press': press
        }
    })
    output = runner.run(test_name, input_obj.dump())
    return output.output.total_energy.etot

def vinet_p(v, v0, k0, kp):
    x = (v / v0) ** (1 / 3)
    xi = 3 / 2 * (kp - 1)
    return 3 * k0 * (1 - x) / x ** 2 * numpy.exp(xi * (1 - x))

def fit_eos(pressure, volume, p0=(100, 1000, 4)):
    popt, pcov = scipy.optimize.curve_fit(vinet_p, volume, pressure)
    return popt

def main():
    cg_input_obj = pw_input.PWInput('./scripts/P21nm-cg.txt')
    test_pressures = [-5.0, 2.0, 0.0, 2.0, 5.0, 10.0, 15.0, 20.0, 25.0]
    volume = [
        run_crude_guess(cg_input_obj, press, 'P21nm-cg-{press}'.format(press=press))
        for press in test_pressures
    ]

    with open('crude_guess_input.json', 'w') as f:
        json.dump({ 'pressure': test_pressures, 'volume': volume }, f)

    v0, k0, kp = fit_eos(pressure, volume)

    with open('crude_guess_result.json', 'w') as f:
        json.dump({ 'v0': v0, 'k0': k0, 'kp': kp }, f)

    vc_input_obj = pw_input.PWInput('./scripts/P21nm-vc.txt')
    test_pressures = [-5.0, 2.0, 0.0, 2.0, 5.0, 10.0, 15.0, 20.0, 25.0]
    volume = [
        run_crude_guess(cg_input_obj, press, 'P21nm-vc-{press}'.format(press=press))
        for press in test_pressures
    ]

    with open('vc_relax_input.json', 'w') as f:
        json.dump({ 'pressure': test_pressures, 'volume': volume }, f)

    v0, k0, kp = fit_eos(test_pressures, volume)

    with open('vc_relax_result.json', 'w') as f:
        json.dump({ 'v0': v0, 'k0': k0, 'kp': kp }, f)


def test_fit():
    P, V = numpy.array([
    #(-5.00, 437.56),
    #(-1.98, 428.03),
    #(0.01, 422.12),
    #(2.01, 416.16),
    #(5.00, 404.00),
    #(10.00, 369.94),
    #(14.98, 314.10),
    #(19.98, 307.59),
    #(25.01, 301.68),
    #(30.00, 296.24),
    #(35.01, 291.17),
    #(40.00, 286.48),
    (6782.79, 60.55),
    (7061.42, 59.34),
    (7236.85, 58.61),
    (7405.12, 57.93),
    (7645.87, 57.00),
    (8021.35, 55.61),
    (8370.43, 54.39),
    (8698.11, 53.31),
    (9007.91, 52.33),
    (9302.44, 51.45),
    (9583.64, 50.63),
    (9853.38, 49.88  ),
    ]).transpose()

    popt = fit_eos(P, V)

    import matplotlib.pyplot as plt

    plt.scatter(V, P)
    V_fit = numpy.linspace(numpy.min(V), numpy.max(V), 100)
    plt.plot(V, vinet_p(V, *popt), marker='+')
    plt.plot(V_fit, vinet_p(V_fit, *popt))
    plt.show()