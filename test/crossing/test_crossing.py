# txt2tags crossing marks tester (http://txt2tags.org)

import glob
import os

import lib


DIR = os.path.dirname(os.path.abspath(__file__))

# left files are generated from right ones (using smart filters)
ALIASES = {
    'numlist' : 'list',
    'deflist' : 'list',
    'bar2'    : 'bar',
}

# smart filters to allow source inheritance and macros normalization
FILTERS = {
    'deflist' : [ ('pre', '^-( |$)', r':\1') ],
    'numlist' : [ ('pre', '^-( |$)', r'+\1') ],
    'bar2'    : [ ('pre', '--'     , r'==' ) ],
}

# convert FILTERS tuples to txt2tags pre/postproc rules
def addFilters(filters):
    if not filters: return []
    config = []
    cmdline = []
    for filter in filters:
        config.append("%%!%sproc: '%s' '%s'"%filter)
    if config:
        lib.write_file(lib.CONFIG_FILE, '\n'.join(config))
        cmdline = ['-C', lib.CONFIG_FILE]
    return cmdline

def run():
    os.chdir(DIR)
    for infile in glob.glob("*.t2t"):
        basename = infile.replace('.t2t', '')
        outfile = basename + '.html'
        if lib.initTest(basename, infile, outfile):
            cmdline = [infile]
            lib.test(DIR, cmdline, outfile)

    # extra: bar.t2t as TXT
    infile = 'bar.t2t'
    basename = 'bar'
    outfile = basename + '.txt'
    if lib.initTest(basename, infile, outfile):
        cmdline = ['-t', 'txt', '-i', infile]
        cmdline.extend(['--width', '150'])  # to avoid wrapping
        lib.test(DIR, cmdline, outfile)

    # using smart filters, same files generate more than one output
    for alias in ALIASES.keys():
        infile = ALIASES[alias] + '.t2t'
        outfile = alias + '.html'
        if lib.initTest(alias, infile, outfile):
            cmdline = addFilters(FILTERS.get(alias))
            cmdline.append('-H')
            cmdline.extend(['-o', outfile, infile])
            lib.test(DIR, cmdline, outfile)

    # extra: bar2.t2t as TXT
    alias = 'bar2'
    infile = ALIASES[alias] + '.t2t'
    outfile = alias + '.txt'
    if lib.initTest(alias, infile, outfile):
        cmdline = addFilters(FILTERS.get(alias))
        cmdline.append('-H')
        cmdline.extend(['--width', '150'])  # to avoid wrapping
        cmdline.extend(['-t', 'txt', '-o', outfile, infile])
        lib.test(DIR, cmdline, outfile)

    # clean up
    if os.path.isfile(lib.CONFIG_FILE):
        os.remove(lib.CONFIG_FILE)


if __name__ == '__main__':
    run()
