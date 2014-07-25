#!/usr/bin/env python
# vi: ts=4 sw=4

from __future__ import print_function
import sys
import re

# copied from the pdf and slightly modified:
ivar_info = '''\
* Motor Definition I-Variables 
Ixx00 Motor xx Activation Control 
Ixx01 Motor xx Commutation Enable 
Ixx02 Motor xx Command Output Address 
Ixx03 Motor xx Position Loop Feedback Address 
Ixx04 Motor xx Velocity Loop Feedback Address 
Ixx05 Motor xx Master Position Address 
Ixx06 Motor xx Position Following Enable and Mode
Ixx07 Motor xx Master (Handwheel) Scale Factor 
Ixx08 Motor xx Position Scale Factor
Ixx09 Motor xx Velocity-Loop Scale Factor 
Ixx10 Motor xx Power-On Servo Position Address 
* Motor Safety I-Variables 
Ixx11 Motor xx Fatal Following Error Limit 
Ixx12 Motor xx Warning Following Error Limit 
Ixx13 Motor xx Positive Software Position Limit 
Ixx14 Motor xx Negative Software Position Limit 
Ixx15 Motor xx Abort/Limit Deceleration Rate 
Ixx16 Motor xx Maximum Program Velocity 
Ixx17 Motor xx Maximum Program Acceleration 
Ixx19 Motor xx Maximum Jog/Home Acceleration 
* Motor Motion I-Variables 
Ixx20 Motor xx Jog/Home Acceleration Time 
Ixx21 Motor xx Jog/Home S-Curve Time 
Ixx22 Motor xx Jog Speed 
Ixx23 Motor xx Home Speed and Direction 
Ixx24 Motor xx Flag Mode Control 
Ixx25 Motor xx Flag Address 
Ixx26 Motor xx Home Offset
Ixx27 Motor xx Position Rollover Range 
Ixx28 Motor xx In-Position Band
Ixx29 Motor xx Output/First Phase Offset 
* Motor xx PID Servo Setup I-Variables 
Ixx30 Motor xx PID Proportional Gain 
Ixx31 Motor xx PID Derivative Gain 
Ixx32 Motor xx PID Velocity Feedforward Gain 
Ixx33 Motor xx PID Integral Gain
Ixx34 Motor xx PID Integration Mode 
Ixx35 Motor xx PID Acceleration Feedforward Gain 
Ixx36 Motor xx PID Notch Filter Coefficient N1 
Ixx37 Motor xx PID Notch Filter Coefficient N2 
Ixx38 Motor xx PID Notch Filter Coefficient D1
Ixx39 Motor xx PID Notch Filter Coefficient D2
Ixx40 Motor xx Net Desired Position Filter Gain 
Ixx41 Motor xx Desired Position Limit Band 
Ixx42 Motor xx Amplifier Flag Address 
Ixx43 Motor xx Overtravel-Limit Flag Address 
Ixx44 Motor xx MACRO Slave Command Address 
* Motor Servo and Commutation Modifiers 
Ixx55 Motor xx Commutation Table Address Offset 
Ixx56 Motor xx Commutation Delay Compensation 
Ixx57 Motor xx Continuous Current Limit 
Ixx58 Motor xx Integrated Current Limit 
Ixx59 Motor xx User-Written Servo/Phase Enable 
Ixx60 Motor xx Servo Cycle Period Extension Period 
Ixx61 Motor xx Current-Loop Integral Gain 
Ixx62 Motor xx Current-Loop Forward-Path Proportional Gain 
Ixx63 Motor xx Integration Limit
Ixx64 Motor xx Deadband Gain Factor 
Ixx65 Motor xx Deadband Size 
Ixx66 Motor xx PWM Scale Factor
Ixx67 Motor xx Position Error Limit 
Ixx68 Motor xx Friction Feedforward 
Ixx69 Motor xx Output Command Limit
* Motor Commutation Setup I-Variables 
Ixx70 Motor xx Number of Commutation Cycles (N) 
Ixx71 Motor xx Counts per N Commutation Cycles 
Ixx72 Motor xx Commutation Phase Angle 
Ixx73 Motor xx Phase Finding Output Value 
Ixx74 Motor xx Phase Finding Time 
Ixx75 Motor xx Phase Position Offset 
Ixx76 Motor xx Current-Loop Back-Path Proportional Gain 
Ixx77 Motor xx Magnetization Current 
Ixx78 Motor xx Slip Gain 
Ixx79 Motor xx Second Phase Offset 
Ixx80 Motor xx Power-Up Mode 
Ixx81 Motor xx Power-On Phase Position Address 
Ixx82 Motor xx Current-Loop Feedback Address 
Ixx83 Motor xx Commutation Position Address 
Ixx84 Motor xx Current-Loop Feedback Mask Word 
* Further Motor I-Variables 
Ixx85 Motor xx Backlash Take-up Rate 
Ixx86 Motor xx Backlash Size 
Ixx87 Motor xx Backlash Hysteresis 
Ixx88 Motor xx In-Position Number of Scans 
Ixx90 Motor xx Rapid Mode Speed Select 
Ixx91 Motor xx Power-On Phase Position Format 
Ixx92 Motor xx Jog Move Calculation Time 
Ixx95 Motor xx Power-On Servo Position Format 
Ixx96 Motor xx Command Output Mode Control 
Ixx97 Motor xx Position Capture & Trigger Mode
Ixx98 Motor xx Third-Resolver Gear Ratio 
Ixx99 Motor xx Second-Resolver Gear Ratio 
* Supplemental Motor Setup I-Variables 
# Iyy00/Iyy50 Motor xx Extended Servo Algorithm Enable 
# Iyy10-Iyy39/Iyy60-Iyy89 Motor xx Extended Servo Algorithm Gains 
* System Configuration Reporting 
I4900 Servo ICs Present 
I4901 Servo IC Type 
I4902 MACRO ICs Present
I4903 MACRO IC Types 
I4904 Dual-Ported RAM ICs Present 
I4908 End of Open Memory
I4909 Turbo CPU ID Configuration 
I4910-I4925 Servo IC Card Identification 
I4926-I4941 MACRO IC Card Identification 
I4942-I4949 DPRAM IC Card Identification 
I4950-I4965 I/O IC Card Identification 
* Data Gathering I-Variables 
I5000 Data Gathering Buffer Location and Mode 
I5001-I5048 Data Gathering Source 1-48 Address 
I5049 Data Gathering Period 
I5050 Data Gathering Selection Mask 1 
I5051 Data Gathering Selection Mask 2 
* A/D Processing Table I-Variables 
I5060 A/D Processing Ring Size 
I5061-I5076 A/D Ring Slot Pointers 
I5080 A/D Ring Convert Enable 
I5081-I5096 A/D Ring Convert Codes
* Coordinate System I-Variables 
Isx11 Coordinate System x User Countdown Timer 1 
Isx12 Coordinate System x User Countdown Timer 2 
Isx13 Coordinate System x Segmentation Time 
Isx14 Coordinate System x End-of-Move Anticipation Time 
Isx15 Coordinate System x Segmentation Override 
Isx16 Coordinate System x Segmentation Override Slew 
Isx20 Coordinate System x Lookahead Length 
Isx21 Coordinate System x Lookahead State Control 
Isx50 Coordinate System x Kinematic Calculations Enable 
Isx53 Coordinate System x Step Mode Control 
Isx78 Coordinate System x Maximum Circle Acceleration 
Isx79 Coordinate System x Rapid Move Mode Control 
Isx81 Coordinate System x Blend Disable In-Position Time-Out 
Isx82 Coordinate System x Blend Disable Dwell Time 
Isx83 Coordinate System x Corner Blend Break Point 
Isx84 Coordinate System x Outside Corner Stop Point Control 
Isx85 Coordinate System x Corner Dwell Break Point 
Isx86 Coordinate System x Alternate Feedrate 
Isx87 Coordinate System x Default Program Acceleration Time 
Isx88 Coordinate System x Default Program S-Curve Time 
Isx89 Coordinate System x Default Program Feedrate/Move Time 
Isx90 Coordinate System x Feedrate Time Units 
Isx91 Coordinate System x Default Working Program Number 
Isx92 Coordinate System x Move Blend Disable
Isx93 Coordinate System x Time Base Control Address 
Isx94 Coordinate System x Time Base Slew Rate 
Isx95 Coordinate System x Feed Hold Slew Rate 
Isx96 Coordinate System x Circle Error Limit 
Isx97 Coordinate System x Minimum Arc Length
Isx98 Coordinate System x Maximum Feedrate 
Isx99 Coordinate System x Cutter-Comp Outside Corner Break Point 
* Turbo PMAC2 MACRO IC I-Variables 
I6800/I6850/I6900/I6950 MACRO IC MaxPhase/PWM Frequency Control 
I6801/I6851/I6901/I6951 MACRO IC Phase Clock Frequency Control 
I6802/I6852/I6902/I6952 MACRO IC Servo Clock Frequency Control 
I6803/I6853/I6903/I6953 MACRO IC Hardware Clock Control 
I6804/I6854/I6904/I6954 MACRO IC PWM Deadtime / PFM Pulse Width Control 
I6805/I6855/I6905/I6955 MACRO IC DAC Strobe Word 
I6806/I6856/I6906/I6956 MACRO IC ADC Strobe Word 
I6807/I6857/I6907/I6957 MACRO IC Clock Direction Control 
* Channel-Specific MACRO IC I-variables
I68n0/I69n0 MACRO IC Channel n Encoder/Timer Decode Control 
I68n1/I69n1 MACRO IC Channel n Position Compare Channel Select 
I68n2/I69n2 MACRO IC Encoder n Capture Control 
I68n3/I69n3 MACRO IC Channel n Capture Flag Select Control 
I68n4/I69n4 MACRO IC Channel n Encoder Gated Index Select 
I68n5/I69n5 MACRO IC Channel n Encoder Index Gate State/Demux Control 
I68n6/I69n6 MACRO IC Channel n Output Mode Select 
I68n7/I69n7 MACRO IC Channel n Output Invert Control 
I68n8/I69n8 MACRO IC Channel n PFM Direction Signal Invert Control
I68n9/I69n9 MACRO IC Channel n Reserved for Future Use 
* MACRO IC Ring Setup I-variables 
I6840/I6890/I6940/I6990 MACRO IC Ring Configuration/Status 
I6841/I6891/I6941/I6991 MACRO IC Node Activate Control 
* PMAC2-Style Multi-Channel Servo IC I-Variables 
I7m00 Servo IC m MaxPhase/PWM Frequency Control 
I7m01 Servo IC m Phase Clock Frequency Control 
I7m02 Servo IC m Servo Clock Frequency Control 
I7m03 Servo IC m Hardware Clock Control 
I7m04 Servo IC m PWM Deadtime / PFM Pulse Width Control 
I7m05 Servo IC m DAC Strobe Word
I7m06 Servo IC m ADC Strobe Word
I7m07 Servo IC m Phase/Servo Clock Direction 
* PMAC2-Style Channel-Specific Servo IC I-Variables 
I7mn0 Servo IC m Channel n Encoder/Timer Decode Control
I7mn1 Servo IC m Channel n Position Compare Channel Select 
I7mn2 Servo IC m Channel n Capture Control
I7mn3 Servo IC m Channel n Capture Flag Select Control 
I7mn4 Servo IC m Channel n Encoder Gated Index Select 
I7mn5 Servo IC m Channel n Encoder Index Gate State/Demux Control 
I7mn6 Servo IC m Channel n Output Mode Select 
I7mn7 Servo IC m Channel n Output Invert Control 
I7mn8 Servo IC m Channel n PFM Direction Signal Invert Control 
I7mn9 Servo IC m Channel n Hardware-1/T Control 
* PMAC-Style Servo IC Setup I-Variables 
I7mn0 Servo IC m Channel n Encoder/Timer Decode Control
I7mn1 Servo IC m Channel n Encoder Filter Disable
I7mn2 Servo IC m Channel n Capture Control
I7mn3 Servo IC m Channel n Capture Flag Select Control 
* Conversion Table I-Variables 
I8000-I8191 Conversion Table Setup Lines'''

ranges = {
    'motor': [('%.2d' % x, [('xx', '%d' % x)]) for x in range(1, 33)],
    'macro': [('%d' % n, [(' n ', ' %d' % n)]) for n in range(1, 3)],
    'servo' : [('%d%d' % (m, n),
               [('Servo IC m', 'Servo IC %d' % m),
               ('Channel n', 'Channel %d' % n)])
               for m in range(0, 10) for n in range(1, 5)],
    'servo0' : [('%d0' % m,
                [('Servo IC m', 'Servo IC %d' % m)])
                for m in range(0, 10)],
    }


def cs_range():
    cs = 1
    ret = []
    for s in range(5, 7):
        if s == 0:
            x_range = range(1, 10)
        else:
            x_range = range(1, 7)

        for x in x_range:
            ret.append(('%s%s' % (s, x), [(' x ', ' %d ' % cs)]))
            cs += 1
    return ret

ranges['cs'] = cs_range()

def ivar_to_int(ivar):
    ivar = ivar.upper()
    if not ivar.startswith('I'):
        raise ValueError('not I variable')
    
    if '/' in ivar or '-' in ivar:
        raise ValueError('ivar range')

    return int(ivar[1:])

def int_to_ivar(i):
    return 'I%d' % i

ivars = {}

def eval_ivar(f, ivar, category, desc):
    if '/' in ivar:
        for iv in ivar.split('/'):
            eval_ivar(f, iv, category, desc)
        return
    elif '-' in ivar:
        r0, r1 = [ivar_to_int(iv) for iv in ivar.split('-')]
        for i in range(r0, r1 + 1):
            eval_ivar(f, int_to_ivar(i), category, desc)
    else: 
        try:
            ivar_to_int(ivar)
        except:
            print('Failed: %s' % ivar)
        else:
            print('%s\t%s\t%s' % (ivar, desc, category), file=f)
        
            if ivar in ivars:
                print('Duplicate', ivar, ivars[ivar], '//', (category, desc))

            ivars[ivar] = (category, desc)

def replace_multiple(s, *from_to):
    for from_, to in from_to:
        s = s.replace(from_, to)
    return s

def generate_ivar_info(fn='ivars.csv'):
    category = ''
    with open(fn, 'wt') as f:
        print('# vi: ts=30 sw=30', file=f)
        for line in ivar_info.split('\n'):
            line = line.strip()
            if line.startswith('*'):
                category = line[1:].strip()
                continue
            elif line.startswith('#'):
                continue

            if 'Motor xx' in line:
                class_, replace = 'motor', 'xx'
            elif 'Servo IC m Channel n' in line:
                class_, replace = 'servo', 'mn'
            elif 'Servo IC m' in line:
                class_, replace = 'servo0', 'm'
            elif ('MACRO IC Channel n' in line) or ('MACRO IC Encoder n' in line):
                class_, replace = 'macro', 'n'
            elif 'Coordinate System' in line:
                class_, replace = 'cs', 'sx'
            else:
                class_ = ''
            
            # print('->', line)

            ivar, desc = line.split(' ', 1)
            if class_:
                range_ = ranges[class_]
                for replace_with, desc_replace in range_:
                    eval_ivar(f, ivar.replace(replace, replace_with), 
                              replace_multiple(category, *desc_replace),
                              replace_multiple(desc, *desc_replace))
            else:
                eval_ivar(f, ivar, category, desc)
                print(line, file=sys.stderr)

def parse_mvar_info(fn='mvar_annotated.pmc', output_fn='mem.csv'):
    addr_info = {}

    whitespace = re.compile('[\s]')

    clear_re = re.compile('(.*)->\*')
    m_re = re.compile('M(\d+)->')

    def fix_comment(s):
        if s.startswith('&'):
            s = 'CS %s' % s[1:]
        elif s.startswith('#'):
            s = 'Motor %s' % s[1:]
        
        return s
    
    mem_fix = re.compile('\$0([^,])')
    for line in open(fn, 'rt').readlines():
        line = line.strip()
        if ';' in line:
            line, comment = line.split(';', 1)
            comment = comment.strip()
        else:
            comment = ''

        line = whitespace.subn('', line)[0]
        if not line:
            continue
         
        if '->' in line:
            mvar, mem = line.split('->')
            if mem.strip() == '*':
                continue
            
            mvar = mvar.upper()

            repl = 1
            while repl > 0:
                mem, repl = re.subn('\$0([^,])', r'$\1', mem)
            
            if not comment:
                print('%s points to %s which is %s' % (mvar, mem, comment))
               
            addr_info[mem] = fix_comment(comment)

    with open(output_fn, 'wt') as f:
        print('# vi: sw=20 ts=20', file=f)

        for mem, info in sorted(addr_info.items(), key=lambda (mem, info): '%s %s' % (info.lower(), mem)):
            print('%s\t%s' % (mem, info), file=f)


class Info(object):
    def __init__(self, fn, delim='\t', lower_case_keys=True):
        self.data = data = {}
        for line in open(fn, 'rt').readlines():
            line = line.strip()
            if line.startswith('#'):
                continue

            info = line.split(delim)
            if lower_case_keys:
                info[0] = info[0].lower()

            data[info[0]] = info[1:]
    
    def __getitem__(self, key):
        return self.data[key]

    def search(self, text, in_keys=True, in_data=True, 
               case_insensitive=True):
        if case_insensitive:
            text = text.lower()

        for key, values in self.data.items():
            s = []
            if in_keys:
                s.append(key)
            if in_data:
                s.extend(values)

            s = ''.join(s)
            if case_insensitive:
                s = s.lower()

            if text in s.lower():
                yield (key, values)


if __name__ == '__main__':
    generate_ivar_info()
    parse_mvar_info()
else:
    import os

    module_path = os.path.abspath(os.path.split(__file__)[0])
    ivar_info = Info(os.path.join(module_path, 'ivars.csv'))
    mem_info = Info(os.path.join(module_path, 'mem.csv'))
