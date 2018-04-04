# Quantum Espresso papercup

This project is a temporary wrapper for manipulating the input and output for [Quantum Espresso](http://www.quantum-espresso.org/)'s PW program using Python, for other programs in the Quantum Espresso distribution, it should work under minimal modification.

The project is started and mostly written in a Feburary afternoon that is not too sad in a temporary manner in a room with no window in NYC. But further modification, if ever happens, would seem to be happen in those loomy days.

## Parts of the Program

### Input File Manipulation

For input file, the program follows PW's input format desribed in the [user guide](https://www.quantum-espresso.org/Doc/pw_user_guide/node8.html). The program accepts a template and update it.

The first part of the input, namely the **namelists** as is used in the Fortran 90, is processed by [marshallward](https://github.com/marshallward)'s [f90nml](https://github.com/marshallward/f90nml). The second part, namely the **cards**, is processed using a self-written parser. But since the format is not clearly defined in the user guide, there should be inconsistency within the program (program use empty line to break the cards whereas further tests shows that they should use keywords like `ATOMIC_SPECIES`,
`ATOMIC_POSITIONS` etc).

The corresponding input manipulation program is the `pw_input.py`.

### Output Files

The program initially expects to PW's XML output as is introduced in version 6.2 as is described in the [release note](https://github.com/QEF/q-e/blob/master/Doc/release-notes) instead of the standard output.

> The new XML format with schema is now the default. Use configure option
  `--disable-xml`, or add -D__OLDXML to MANUAL_FLAGS in make.inc, to revert
  to the old xml format. IMPORTANT NOTICE: the new format is incompatibile 
  both with the "old" format and with the previous "new" one: files may be
  in different locations with different names and contain different data.
>
> IMPORTANT NOTICE 2: the "collected" format is now the default
>
> IMPORTANT NOTICE 3: the new format uses FoX instead of iotk

The program intends to use [lxml.objectify](http://lxml.de/objectify.html) to parse the output XML for a smooth experience. The code works but is quite ugly.

However, since it is not fully equivalent to what is in the standard output, further modificaiton is expected.

The corresponding input manipulation program is the `pw_output.py`.

### PW Job Runner Wrapper

We hope to put the batch creation of input file, folder and context creation, programming running, and the output processing all into one place, so we wrote a wrapper for these tasks.

The corresponding input manipulation program is the `pw_job.py`.

### The Glue for Everything

Finally we want to put everything together, we wrote `pw_run.py`. This is how the program is first used.

## Acknoledgement

Thanks to the opensource programs [f90nml](https://github.com/marshallward/f90nml) and [lxml.objectify](http://lxml.de/objectify.html).

Thanks to my professor and colleagues for the opportunity and cooperation.

And thanks to you, for the wonderful January and February I had in the New York City.