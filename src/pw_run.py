KP_list = [
    [1, 1, 2],
    [2, 2, 3],
    [2, 2, 4],
    [3, 3, 4],
    [3, 3, 6],
    [4, 4, 6],
    [4, 4, 8]
]

shift_list = [0, 1]


import numpy
import matplotlib.pyplot as plt

import pw_input
import pw_job

runner = pw_job.PWJobRunner('./scripts/runtime', '../../../bin/pw.x')

PSEUDO_DIR = '../../../pseudo'

def test_ecutwfc_etot(input_obj, ecutwfc, test_name):
    input_obj.nml.update({
        'SYSTEM': {
            'ecutwfc': ecutwfc,
            'ecutrho': ecutwfc * 4
        }
    })
    output = runner.run(test_name, input_obj.dump())
    return output.output.total_energy.etot

def test_KP_etot(input_obj, KP, test_name):
    output = runner.run(test_name, input_obj.dump(), skip_exists=True)
    input_obj.cards['K_POINTS'].lines[0] = list(map(str, KP)) + input_obj.cards['K_POINTS'].lines[0][3:]
    return (float(output.output.total_energy.etot), int(output.output.band_structure.nks))

def do_ecutwfc_test():
    for template_name in ('P21nm', 'Pnnm'):
        ecutwfc_list = range(40, 110, 10)
        input_obj = pw_input.PWInput('./scripts/{template_name}.txt'.format(template_name=template_name))
        input_obj.nml.update({
            'CONTROL': {
                'pseudo_dir': PSEUDO_DIR
            }
        })
        energy = [test_ecutwfc_etot(input_obj, ecutwfc, '{template_name}-ECUT-{ecutwfc}'.format(template_name=template_name, ecutwfc=ecutwfc)) for ecutwfc in ecutwfc_list]
        plt.figure()
        plt.plot(numpy.array(ecutwfc_list), numpy.array([float(energy) for energy in energy]), marker='+')
        plt.xlabel(r'$E_{cut}$ (Rydberg)')
        plt.ylabel(r'$E_{total}$ (Hartree)')
        plt.savefig('scripts/{template_name}-ecutwfc.png'.format(template_name=template_name))

def do_KP_test():
    KP_list = [
        [1, 1, 2],
        [2, 2, 3],
        [2, 2, 4],
        [3, 3, 4],
        [3, 3, 6],
        [4, 4, 6],
        [4, 4, 8]
    ]
    for template_name in ('P21nm', 'Pnnm'):
        input_obj = pw_input.PWInput('./scripts/{template_name}.txt'.format(template_name=template_name))
        input_obj.nml.update({
            'CONTROL': {
                'pseudo_dir': PSEUDO_DIR
            }
        })
        test_result = [test_KP_etot(input_obj, KP, '{template_name}-KP-{KP}'.format(template_name=template_name, KP='-'.join([str(k) for k in KP]))) for KP in KP_list]
        dataset = sorted(zip(KP_list, test_result), key=lambda a: a[1][1])
        X_ticks = ['%s (%d)'%(', '.join([str(i) for i in data[0]]), data[1][1]) for data in dataset]
        Y = [data[1][1] for data in dataset]
        X = range(len(Y))

        plt.figure()
        plt.plot(X, Y, marker='+')
        plt.xticks(X, X_ticks, rotation=-30)
        plt.xlabel(r'nks')
        plt.ylabel(r'$E_{total}$ (Hartree)')
        plt.tight_layout()
        plt.savefig('scripts/{template_name}-KP.png'.format(template_name=template_name))

        
if __name__ == '__main__':
    # do_ecutwfc_test()
    do_KP_test()

#for KP in KP_list:
#    input_obj = pw_input.PWInput('AlOOH-gamma-0Pa-template.txt')
#    input_obj.cards['K_POINTS'].lines[0] = list(map(str, KP)) + input_obj.cards['K_POINTS'].lines[0][3:]
#    print(input_obj.dump())
#
#for shift in shift_list:
#    input_obj = pw_input.PWInput('AlOOH-gamma-0Pa-template.txt')
#    input_obj.cards['K_POINTS'].lines[0] = input_obj.cards['K_POINTS'].lines[0][:3] + ['0', '0', '0']
#    print(input_obj.dump())
