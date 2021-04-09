#usege python HRC_powder_data_proc.py init.txt
import numpy as np
import os
import sys

BGcorrection = True

#========== reading parameters from init file ==========
FH1=open(sys.argv[1])
values=(FH1.readline()).split(' ')
Meas_File=values[0]
values=(FH1.readline()).split(' ')
Meas_File_raw=values[0]
values=(FH1.readline()).split(' ')
Meas_PN=float(values[0])
values=(FH1.readline()).split(' ')
BG_File=values[0]
values=(FH1.readline()).split(' ')
BG_File_raw=values[0]
values=(FH1.readline()).split(' ')
BG_PN=float(values[0])
values=(FH1.readline()).split(' ')
intensitymap_file=values[0]

values=(FH1.readline()).split(' ')
E_lowlim=float(values[0])
values=(FH1.readline()).split(' ')
E_highlim=float(values[0])
values=(FH1.readline()).split(' ')
constE_file=values[0]

values=(FH1.readline()).split(' ')
Q_lowlim=float(values[0])
values=(FH1.readline()).split(' ')
Q_highlim=float(values[0])
values=(FH1.readline()).split(' ')
constQ_file=values[0]

FH1.close()

#=========== checking data files =====================
if(os.path.exists(Meas_File)):
    print("Meas. File : %s"%(Meas_File))
else:
    print("%s does not exist. "%(Meas_File))
    sys.exit()

if(os.path.exists(Meas_File_raw)):
    print("Meas. File (raw) : %s"%(Meas_File_raw))
else:
    print("%s does not exist. "%(Meas_File_raw))
    sys.exit()

if(os.path.exists(BG_File)):
    print("BG File : %s"%(BG_File))
else:
    BGcorrection = False
    print("No BG correction.")

if(os.path.exists(BG_File_raw)):
    print("BG File (raw) : %s"%(BG_File_raw))
else:
    BGcorrection = False
    print("No BG correction.")

print(">>> output files.")
print("intensity map: {0}".format(intensitymap_file))
print("const-E cut: {0}".format(constE_file))
print("const-Q cut: {0}".format(constQ_file))


#=========== reading Q values =====================
FH=open(Meas_File,'r')

line = FH.readline()
values = line.split(',')

Q = np.zeros(len(values))

for ii in range(1,len(values)):
    Q[ii]=float(values[ii])

FH.close()

#=========== BG subtraction and output =====================

MeasMatrix=np.genfromtxt(Meas_File,delimiter=',',skip_header=1)
MeasMatrix_raw=np.genfromtxt(Meas_File_raw,delimiter=',',skip_header=1)


for ii in range(MeasMatrix.shape[0]):
    for jj in range(MeasMatrix.shape[1]):
        if (np.isnan(MeasMatrix[ii][jj])):
            MeasMatrix[ii][jj]=0.0

for ii in range(MeasMatrix_raw.shape[0]):
    for jj in range(MeasMatrix_raw.shape[1]):
        if (np.isnan(MeasMatrix_raw[ii][jj])):
            MeasMatrix_raw[ii][jj]=0.0

CorrectionMatrix=np.zeros(MeasMatrix.shape)
ErrMatrix=np.zeros(MeasMatrix.shape)


for ii in range(MeasMatrix_raw.shape[0]):
    for jj in range(MeasMatrix_raw.shape[1]):
        if ((MeasMatrix_raw[ii][jj] > 0) and (MeasMatrix[ii][jj] > 0)):
            CorrectionMatrix[ii][jj]=MeasMatrix[ii][jj]/MeasMatrix_raw[ii][jj]


E = np.zeros(MeasMatrix.shape[0])
for ii in range(1,MeasMatrix.shape[0]):
    E[ii]=MeasMatrix[ii][0]

if (BGcorrection):
    BGMatrix=np.genfromtxt(BG_File,delimiter=',',skip_header=1)
    BGMatrix_raw=np.genfromtxt(BG_File_raw,delimiter=',',skip_header=1)
    BGsubtMatrix=MeasMatrix/Meas_PN-BGMatrix/BG_PN
    for ii in range(MeasMatrix_raw.shape[0]):
        for jj in range(MeasMatrix_raw.shape[1]):
            if ((MeasMatrix_raw[ii][jj] > 0) and (BGMatrix[ii][jj] > 0)):
                ErrMatrix[ii][jj]=(MeasMatrix_raw[ii][jj]/(Meas_PN**2.0)+BGMatrix_raw[ii][jj]/(BG_PN**2.0))**(0.5)*CorrectionMatrix[ii][jj]
else:
    BGsubtMatrix=MeasMatrix/Meas_PN
    for ii in range(MeasMatrix_raw.shape[0]):
        for jj in range(MeasMatrix_raw.shape[1]):
            if (MeasMatrix_raw[ii][jj] > 0):
                ErrMatrix[ii][jj]=(MeasMatrix_raw[ii][jj]/(Meas_PN**2.0))**(0.5)*CorrectionMatrix[ii][jj]



# output for const-E cut
FH_cE=open(constE_file,'w')
FH_cE.write("#Q(A-1)  E_ave(meV)  Intensity  Error\n")
for index_Q in range(1,Q.shape[0]):
    E_ave=0.0
    Int_ave=0.0
    Err_ave=0.0
    Num=0.0
    for index_E in range(1,MeasMatrix.shape[0]):
        if ((E[index_E]>=E_lowlim)and(E[index_E]<=E_highlim)):
            E_ave+=E[index_E]
            Int_ave+=BGsubtMatrix[index_E][index_Q]
            Err_ave+=ErrMatrix[index_E][index_Q]**2.0
            Num+=1.0
    E_ave=E_ave/Num
    Int_ave=Int_ave/Num
    Err_ave=np.sqrt(Err_ave)/Num
    FH_cE.write("{0}  {1}  {2}  {3}\n".format(Q[index_Q],E_ave,Int_ave,Err_ave))
FH_cE.close()

# output for const-Q cut
FH_cQ=open(constQ_file,'w')
FH_cQ.write("#Q_ave(A-1)  E(meV)  Intensity  Error\n")
for index_E in range(1,MeasMatrix.shape[0]):
    Q_ave=0.0
    Int_ave=0.0
    Err_ave=0.0
    Num=0.0
    for index_Q in range(1,Q.shape[0]):
        if ((Q[index_Q]>=Q_lowlim)and(Q[index_Q]<=Q_highlim)):
            Q_ave+=Q[index_Q]
            Int_ave+=BGsubtMatrix[index_E][index_Q]
            Err_ave+=ErrMatrix[index_E][index_Q]**2.0
            Num+=1.0
    Q_ave=Q_ave/Num
    Int_ave=Int_ave/Num
    Err_ave=np.sqrt(Err_ave)/Num
    FH_cQ.write("{0}  {1}  {2}  {3}\n".format(Q_ave,E[index_E],Int_ave,Err_ave))
FH_cQ.close()

#output for intensity map
FH_map=open(intensitymap_file,'w')
FH_map.write("#Q_ave(A-1)  E(meV)  Intensity  Error\n")
for ii in range(BGsubtMatrix.shape[0]):
    for jj in range(1,Q.shape[0]):
        FH_map.write("{0}  {1}  {2}  {3}  {4}\n".format(Q[jj],MeasMatrix[ii][0],BGsubtMatrix[ii][jj],ErrMatrix[ii][jj],CorrectionMatrix[ii][jj]))
    FH_map.write("\n")
FH_map.close()