.. _quantities:

**********
Quantities
**********

All quantities defined in ``dcmri``, grouped by type. This page is generated from ``dcmri.QUANTITIES`` at build time.

.. code-block:: text

   +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   |                                                                                 Quantities                                                                                |
   +----------------+------------+------------+-------------------------------------------------------------------+-----------------+----------------------+-------+-----------+
   | Key            | Value      | Unit       | Name                                                              | Group           | Bounds               | DICOM | OSIPI     |
   +----------------+------------+------------+-------------------------------------------------------------------+-----------------+----------------------+-------+-----------+
   | B1corr         | 1          |            | B1-correction factor                                              | electromagnetic | (0, 5)               |       |           |
   | JMz            | 1          | A/cm/sec   | longitudinal magnetization inflow                                 | electromagnetic | (0, 5)               |       |           |
   | M              | 1          | A/cm       | magnetization                                                     | electromagnetic | (0, 5)               |       |           |
   | me             | 1          | A cm2/mL   | equilibrium magnetization                                         | electromagnetic | (0, 5)               |       |           |
   | Mxy            | 1          | A/cm       | transverse magnetization                                          | electromagnetic | (0, 5)               |       |           |
   | Mz             | 1          | A/cm       | longitudinal magnetization                                        | electromagnetic | (0, 5)               |       |           |
   | Mzi            | 1          | A/cm       | longitudinal inlet magnetization                                  | electromagnetic | (0, 5)               |       |           |
   | R1             | 0.65       | Hz         | tissue R1                                                         | electromagnetic | (0, 5)               |       |           |
   | r1             | 3500       | Hz/M       | longitudinal contrast agent relaxivity                            | electromagnetic | (0, 10000.0)         |       |           |
   | R1b            | 0.65       | Hz         | precontrast tissue R1                                             | electromagnetic | (0, 5)               |       |           |
   | R1i            | 0.65       | Hz         | inlet R1                                                          | electromagnetic | (0, 5)               |       |           |
   | r1i            | 3500       | Hz/M       | inlet longitudinal contrast agent relaxivity                      | electromagnetic | (0, 10000.0)         |       |           |
   | R1ib           | 0.65       | Hz         | precontrast inlet R1                                              | electromagnetic | (0, 5)               |       |           |
   | R2             | 2.0        | Hz         | tissue R2                                                         | electromagnetic | (0, 5)               |       |           |
   | r2             | 4000       | Hz/M       | transverse contrast agent relaxivity                              | electromagnetic | (0, 10000.0)         |       |           |
   | R2b            | 20         | Hz         | precontrast tissue R2                                             | electromagnetic | (0, 100)             |       |           |
   | R2s            | 20         | Hz         | tissue R2*                                                        | electromagnetic | (0, 5)               |       |           |
   | r2s            | 20000      | Hz/M       | transverse contrast agent relaxivity                              | electromagnetic | (0, 100000.0)        |       |           |
   | R2sb           | 20         | Hz         | precontrast tissue R2*                                            | electromagnetic | (0, 100)             |       |           |
   | r2se           | 20000      | Hz/M       | extravascular, extracellular transverse contrast agent relaxivity | electromagnetic | (0, 100000.0)        |       |           |
   | r2sq           | 1000       | Hz/M^2     | quadratic transverse contrast agent relaxivity                    | electromagnetic | (0, 10000.0)         |       |           |
   | r2sv           | 20000      | Hz/M       | vascular transverse contrast agent relaxivity                     | electromagnetic | (0, 100000.0)        |       |           |
   | tJMz           | 0.0        | sec        | longitudinal magnetization inflow time points                     | electromagnetic |                      |       |           |
   | tM             | 0.0        | sec        | magnetization time points                                         | electromagnetic |                      |       |           |
   | tMi            | 0.0        | sec        | inlet magnetization time points                                   | electromagnetic |                      |       |           |
   | tMz            | 0.0        | sec        | longitudinal magnetization time points                            | electromagnetic |                      |       |           |
   | tR             | 0.0        | sec        | relaxation rate time points                                       | electromagnetic |                      |       |           |
   +----------------+------------+------------+-------------------------------------------------------------------+-----------------+----------------------+-------+-----------+
   | dose_tolerance | 0.1        |            | dose tolerance                                                    | hyperparameters |                      |       |           |
   | dt             | 0.5        | sec        | pseudo-continuous time step                                       | hyperparameters |                      |       |           |
   | tmax           | 240        | sec        | maximum time point                                                | hyperparameters |                      |       |           |
   +----------------+------------+------------+-------------------------------------------------------------------+-----------------+----------------------+-------+-----------+
   | agent          | gadoterate |            | contrast agent generic name                                       | indicator       |                      |       |           |
   | BAT            | 30         | sec        | bolus arrival time                                                | indicator       | (-30, 30)            |       |           |
   | bdel           | 30         | sec        | delay in a double injection                                       | indicator       | (-30, 30)            |       |           |
   | c              | 0.005      | mmol/mL    | concentration                                                     | indicator       | (0, 1)               |       |           |
   | C              | 0.005      | mmol/cm3   | tissue concentration                                              | indicator       | (0, 1)               |       |           |
   | ci             | 0.005      | mmol/mL    | inlet concentration                                               | indicator       |                      |       |           |
   | dose           | 0.1        | mL/kg      | contrast agent dose                                               | indicator       | (0, 0.2)             |       |           |
   | duration       | 5          | sec        | injection duration                                                | indicator       | (0, 120)             |       |           |
   | J              | 1          | mmol/sec   | indicator flux                                                    | indicator       | (0, 10)              |       |           |
   | Jinj           | 1          | mmol/sec   | indicator flux at the injection site                              | indicator       | (0, 10)              |       |           |
   | rate           | 1          | mL/sec     | injection rate                                                    | indicator       | (0, 10)              |       |           |
   | tC             | 0.0        | sec        | concentration time points                                         | indicator       |                      |       |           |
   +----------------+------------+------------+-------------------------------------------------------------------+-----------------+----------------------+-------+-----------+
   | loss           | None       | a.u.       | loss value of optimized model                                     | inverse problem |                      |       |           |
   | pars           | None       | a.u.       | dictionary with source- and derived parameters                    | inverse problem |                      |       |           |
   | pcov           | None       | a.u.       | dictionary with covariances of free parameters                    | inverse problem |                      |       |           |
   | pfree          | None       | a.u.       | set of free parameters                                            | inverse problem |                      |       |           |
   | popt           | None       | a.u.       | dictionary of optimized free parameter values                     | inverse problem |                      |       |           |
   | psdev          | None       | a.u.       | dictionary with parameter standard deviations                     | inverse problem |                      |       |           |
   +----------------+------------+------------+-------------------------------------------------------------------+-----------------+----------------------+-------+-----------+
   | BF             | 2          | mL/sec     | blood flow                                                        | physiological   | (0, 100)             |       |           |
   | CL             | 10         | mL/sec     | Contrast agent clearance                                          | physiological   | (0.0, 100)           |       |           |
   | CO             | 100        | mL/sec     | cardiac output                                                    | physiological   | (0, 500)             |       |           |
   | D              | 0.85       |            | transit time dispersion                                           | physiological   | (0, 1)               |       |           |
   | Db             | 0.2        |            | bolus transit time dispersion                                     | physiological   | (0, 1)               |       |           |
   | DRF            | 0.5        |            | Differential renal function                                       | physiological   | (0, 1)               |       |           |
   | DRPF           | 0.5        |            | Differential renal plasma flow                                    | physiological   | (0, 1)               |       |           |
   | E              | 0.1        |            | extraction fraction                                               | physiological   | (0.0, 1.0)           |       |           |
   | Ef             | 0.1        |            | final extraction fraction                                         | physiological   | (0.0, 1.0)           |       |           |
   | Ei             | 0.1        |            | initial extraction fraction                                       | physiological   | (0.0, 1.0)           |       |           |
   | EV             | 10000.0    | mL         | plasma volume                                                     | physiological   | (0, 100)             |       |           |
   | F              | 0.02       | mL/sec/cm3 | flow per unit tissue                                              | physiological   | (0, 0.1)             |       |           |
   | fCO            | 0.1        |            | fraction of the cardiac output                                    | physiological   | (0, 0.5)             |       |           |
   | FF             | 0.1        |            | filtration fraction                                               | physiological   | (0, 0.5)             |       |           |
   | ffa            | 0.2        |            | arterial flow fraction                                            | physiological   | (0, 1)               |       |           |
   | ffc            | 0.8        |            | cortical flow fraction                                            | physiological   | (0, 1)               |       |           |
   | ffp            | 0.2        |            | plug-flow fraction in a plucom system                             | physiological   | (0, 1)               |       |           |
   | Fwi            | 0.02       | mL/sec/cm3 | inflow in all water compartments                                  | physiological   | (0, 1)               |       |           |
   | GFR            | 2          | mL/sec     | glomerular filtration rate                                        | physiological   | (0, 10)              |       |           |
   | h              | 1.0        | Hz         | transit time distribution                                         | physiological   | (0.1, 60)            |       |           |
   | H              | 0.45       |            | hematocrit                                                        | physiological   | (0, 1)               |       |           |
   | inlets         | (0,)       |            | water inlet compartments                                          | physiological   |                      |       |           |
   | irf            | 0.02       | mL/sec/cm3 | Impulse response function                                         | physiological   | (0, 10)              |       |           |
   | k              | 0.003      | mL/sec/cm3 | tissue transfer rate                                              | physiological   | (0.0, 0.1)           |       |           |
   | K              | 0.003      | 1/sec      | transfer rate                                                     | physiological   | (0.0, 0.1)           |       |           |
   | kep            | 0.015      | 1/sec      | interstitial excretion rate                                       | physiological   | (0.0, 0.1)           |       |           |
   | kf             | 0.003      | mL/sec/cm3 | final tissue transfer rate                                        | physiological   | (0.0, 0.1)           |       |           |
   | ki             | 0.003      | mL/sec/cm3 | initial tissue transfer rate                                      | physiological   | (0.0, 0.1)           |       |           |
   | Km             | 1          | mmol/mL    | Michaelis-Menten constant                                         | physiological   | (0.0, 10)            |       |           |
   | Ktrans         | 0.015      | mL/sec/cm3 | plasma clearance                                                  | physiological   | (0.0, 0.1)           |       |           |
   | Kw             | 0          | mL/sec/cm3 | water exchange matrix                                             | physiological   | (0, 1)               |       |           |
   | nmGFR          | 2          | mL/sec     | nuclear medicine glomerular filtration rate                       | physiological   | (0, 10)              |       |           |
   | P              | 0.3        |            | porosity                                                          | physiological   | (0, 1)               |       |           |
   | PF             | 1          | mL/sec     | plasma flow                                                       | physiological   | (0, 100)             |       |           |
   | PS             | 0.003      | mL/sec/cm3 | permeability-surface area product                                 | physiological   | (0, 1)               |       |           |
   | PSB            | 0.003      | mL/sec     | whole-body permeability-surface area product                      | physiological   | (0, 1)               |       |           |
   | PSc            | 0.03       | mL/sec/cm3 | transcytolemmal water permeability-surface area product           | physiological   | (0, 100)             |       |           |
   | PSe            | 0.03       | mL/sec/cm3 | transendothelial water permeability-surface area product          | physiological   | (0, 100)             |       |           |
   | PSw            | 0.03       | mL/sec/cm3 | water permeability-surface area product                           | physiological   | (0, 100)             |       |           |
   | PV             | 10000.0    | mL         | plasma volume                                                     | physiological   | (0, 100)             |       |           |
   | RM             | 1          |            | relaxivity mapping                                                | physiological   |                      |       |           |
   | T              | 30         | sec        | mean transit time                                                 | physiological   | (0.0, 60)            |       |           |
   | Tb             | 30         | sec        | bolus mean transit time                                           | physiological   | (0.0, 60)            |       |           |
   | Tf             | 30         | sec        | final mean transit time                                           | physiological   | (0.0, 60)            |       |           |
   | TF             | 0.25       | sec        | inflow time                                                       | physiological   | (0, 1)               |       |           |
   | Ti             | 30         | sec        | initial mean transit time                                         | physiological   | (0.0, 60)            |       |           |
   | TT             | 1.0        | sec        | boundaries of transit time histogram bins                         | physiological   | (0.1, 60)            |       |           |
   | v              | 1          | mL/cm3     | volume fraction                                                   | physiological   | (0, 1)               |       |           |
   | Vmax           | 1          | mmol/sec   | limiting rate in a Michaelis-Menten compartment                   | physiological   | (0.0, 10)            |       |           |
   | vr             | 0.15       |            | Venous return                                                     | physiological   | (0, 1)               |       |           |
   | vw             | 1          | mL/cm3     | water volume fraction                                             | physiological   | (0, 1)               |       |           |
   +----------------+------------+------------+-------------------------------------------------------------------+-----------------+----------------------+-------+-----------+
   | FA             | 15         | deg        | flip angle                                                        | sequence        | (0, 180)             |       |           |
   | field_strength | 3          | T          | magnetic field strength                                           | sequence        | (0, 20)              |       |           |
   | iz             | 0          |            | slice number in a multi-slice acquisition                         | sequence        | (0, 1000)            |       |           |
   | Nk0            | 64         |            | number of acquired phase lines to the center of k-space           | sequence        | (0, 1000)            |       |           |
   | Nph            | 128        |            | number of acquired phase lines in k-space                         | sequence        | (0, 1000)            |       |           |
   | Nz             | 64         |            | number of slices in a multi-slice acquisition                     | sequence        | (0, 1000)            |       |           |
   | PA             | 90         | deg        | preparation Pulse Flip Angle                                      | sequence        | (0, 180)             |       |           |
   | SA             | 0          | deg        | saturation Slab Flip Angle                                        | sequence        | (0, 180)             |       |           |
   | TA             | 2.0        | sec        | acquisition time                                                  | sequence        | (0, 30)              |       |           |
   | tacq           | 240        | sec        | acquisition duration                                              | sequence        | (0, 10000.0)         |       |           |
   | TD             | 0.05       | sec        | prepulse delay                                                    | sequence        | (0, 1)               |       |           |
   | TE             | 0.001      | sec        | echo time                                                         | sequence        | (0, 10)              |       |           |
   | TE1            | 0.001      | sec        | first echo time in a multi-echo sequence                          | sequence        | (0, 1)               |       |           |
   | TE2            | 0.005      | sec        | second echo time in a multi-echo sequence                         | sequence        | (0, 1)               |       |           |
   | TP             | 0.05       | sec        | preparation delay                                                 | sequence        | (0, 1)               |       |           |
   | TR             | 0.005      | sec        | repetition time                                                   | sequence        | (0, 1)               |       |           |
   | tstart         | 0          | sec        | start of the acquisition                                          | sequence        | (0, 10000.0)         |       |           |
   +----------------+------------+------------+-------------------------------------------------------------------+-----------------+----------------------+-------+-----------+
   | AUCC           | 1          | M*sec      | area under the concentration time curve                           | signal          | (0, 1000000000000.0) |       |           |
   | iScal          | 0          |            | indices of calibration signal                                     | signal          |                      |       |           |
   | iStrig         | None       |            | indices of the signal trigger                                     | signal          |                      |       |           |
   | nb             | 1          | a.u.       | number of baseline time points                                    | signal          |                      |       |           |
   | NSR            | 0.0        |            | noise-to-signal ratio                                             | signal          | (0, 100000.0)        |       |           |
   | RE             | 1          |            | relative signal enhancement                                       | signal          | (0, 1000)            |       |           |
   | S              | 1.0        | a.u.       | signal                                                            | signal          | (0, 5)               |       |           |
   | S0             | 1.0        | a.u.       | signal scaling factor                                             | signal          | (0, 5)               |       | Q.MS1.010 |
   | Sb             | 1.0        | a.u.       | signal baseline                                                   | signal          | (0, 5)               |       | Q.MS1.002 |
   | Scal           | 1.0        | a.u.       | calibration signal                                                | signal          | (0, 5)               |       | Q.MS1.002 |
   | Strig          | 1.0        | a.u.       | signal trigger                                                    | signal          | (0, 5)               |       | Q.MS1.002 |
   | tS             | 0.0        | sec        | signal time points                                                | signal          |                      |       |           |
   +----------------+------------+------------+-------------------------------------------------------------------+-----------------+----------------------+-------+-----------+
   | vol            | 150        | cm3        | ROI volume                                                        | whole-body      | (0.0, 1000)          |       |           |
   | weight         | 70         | kg         | body weight                                                       | whole-body      | (0, 300)             |       |           |
   +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
