print('Hellow World!!')def readActivityParam():
    paramFileName = 'ActivityParameters.nv'

    f = open(paramFileName, 'r')
    lines = f.readlines()
    f.close()

    dictParam = {}
    matrixParam = {}
    for line in lines:
        tokens = line.strip().split('=')
        if tokens[0] == 'exportParam_sub_job_id':
            pass
        elif tokens[0] == 'importParam_sub_job_id':
            pass
        elif tokens[0].startswith('N_FullMap') > 0:
            matrixParam.update({tokens[0]: tokens[1]})
        else:
            dictParam.update({tokens[0]: tokens[1]})

    return dictParam, matrixParam


def updateParameters(dictParam, matrixParam, currentDir):
    os.chdir(currentDir)
    f = open('ActivityParameters.nv', 'w')
    for key, value in dictParam.items():
        f.write('%s=%s\n' % (key, value))
    for key, value in matrixParam.items():
        f.write('%s=%s\n' % (key, value))
    f.close()

def makeInputFile(dictParam, matrixParam):

    dictList = [dictParam.get('Ini_Temp'), dictParam.get('Final_Temp'), dictParam.get('Ini_FS_Stress'), \
                dictParam.get('Avg_Mesh_Size'), dictParam.get('Min_Mesh_Size'), dictParam.get('HBM_Total_T'), \
                dictParam.get('HBM_STACK_NO'), dictParam.get('Top_Chip_OX'), dictParam.get('HBM_CORE_BO_T'), \
                dictParam.get('HBM_CORE_FO_T'), dictParam.get('HBM_CORE_NCF_T'), dictParam.get('HBM_CORE_X'), \
                dictParam.get('HBM_CORE_Y'), dictParam.get('HBM_BUFFER_BO_T'), dictParam.get('HBM_BUFFER_FO_T'), \
                dictParam.get('HBM_BUFFER_X'), dictParam.get('HBM_BUFFER_Y'), dictParam.get('HBM_GLUE_T'), \
                dictParam.get('HBM_CARRIER_T'), dictParam.get('HBM_CORE_T')]

    fullMapLst = []
    for i in range(23):
        fullMapString = ''
        for j in range(27):
            value = matrixParam.get('N_FullMap[%s,%s]' % (i, j))
            fullMapString += value
        fullMapLst.append(fullMapString)

    macroFile = 'CoW_Warpage_template.py'
    #
    f = open(macroFile, 'r', encoding='UTF-8')
    line = f.readline()
    lst = []

    while line:
        if line.find('Ini_Temp=') >= 0:
            lst.append('%s%s' % ('Ini_Temp=', dictList[0]) + '\n')
        elif line.find('Final_Temp=') >= 0:
            lst.append('%s%s' % ('Final_Temp=', dictList[1]) + '\n')
        elif line.find('Ini_FS_Stress =') >= 0:
            lst.append('%s%s' % ('Ini_FS_Stress = ', dictList[2]) + '\n')
        elif line.find('Avg_Mesh_Size=') >= 0:
            lst.append('%s%s' % ('Avg_Mesh_Size=', dictList[3]) + '\n')
        elif line.find('Min_Mesh_Size=') >= 0:
            lst.append('%s%s' % ('Min_Mesh_Size=', dictList[4]) + '\n')
        elif line.find('HBM_Total_T =') >= 0:
            lst.append('%s%s' % ('HBM_Total_T = ', dictList[5]) + '\n')
        elif line.find('HBM_STACK_NO=') >= 0:
            lst.append('%s%s' % ('HBM_STACK_NO=', dictList[6]) + '\n')
        elif line.find('Top_Chip_OX =') >= 0:
            if line.find('Top_Chip_OX ==') >= 0:
                lst.append(line)
            else:
                lst.append('%s%s #Top Chip 유무 설정 (유:1, 무:0)' % ('Top_Chip_OX = ', dictList[7]) + '\n')
        elif line.find('HBM_CORE_BO_T=') >= 0:
            lst.append('%s%s' % ('HBM_CORE_BO_T=', dictList[8]) + '\n')
        elif line.find('HBM_CORE_FO_T=') >= 0:
            lst.append('%s%s' % ('HBM_CORE_FO_T=', dictList[9]) + '\n')
        elif line.find('HBM_CORE_NCF_T=') >= 0:
            lst.append('%s%s' % ('HBM_CORE_NCF_T=', dictList[10]) + '\n')
        elif line.find('HBM_CORE_X=') >= 0:
            lst.append('%s%s' % ('HBM_CORE_X=', dictList[11]) + '\n')
        elif line.find('HBM_CORE_Y=') >= 0:
            lst.append('%s%s' % ('HBM_CORE_Y=', dictList[12]) + '\n')
        elif line.find('HBM_BUFFER_BO_T=') >= 0:
            lst.append('%s%s' % ('HBM_BUFFER_BO_T=', dictList[13]) + '\n')
        elif line.find('HBM_BUFFER_FO_T=') >= 0:
            lst.append('%s%s' % ('HBM_BUFFER_FO_T=', dictList[14]) + '\n')
        elif line.find('HBM_BUFFER_X=') >= 0:
            lst.append('%s%s' % ('HBM_BUFFER_X=', dictList[15]) + '\n')
        elif line.find('HBM_BUFFER_Y=') >= 0:
            lst.append('%s%s' % ('HBM_BUFFER_Y=', dictList[16]) + '\n')
        elif line.find('HBM_GLUE_T=') >= 0:
            lst.append('%s%s' % ('HBM_GLUE_T=', dictList[17]) + '\n')
        elif line.find('HBM_CARRIER_T=') >= 0:
            lst.append('%s%s' % ('HBM_CARRIER_T=', dictList[18]) + '\n')
        elif line.find('HBM_CORE_T=') >= 0:
            lst.append('%s%s' % ('HBM_CORE_T=', dictList[19]) + '\n')

        elif line.find('N_FullMap = [') >= 0:
            lst.append('N_FullMap = [\n')
            for line in fullMapLst:
                lst.append('    [' + ','.join(str(line)) + '],\n')

        elif line.find('    [') >=0:
            pass

        else:
            lst.append(line)
        line = f.readline()
    f.close()

    fw = open('CoW_Warpage.py', 'w', encoding='UTF-8')
    for line in lst:
        fw.write(line)
    fw.close()

def copyModels(dictParam, matrixParam, currentDir):
    AbaqusDir = r'D:\AVP_SolvingDir\Abaqus'
    # AbaqusDir = r'C:\Temp\AVP_SolvingDir\Abaqus'
    uuidName = uuid.uuid1()

    now = datetime.datetime.now()
    now_format = now.strftime('%Y%m%d_')

    dirName = 'CoW_Warpage_Analysis_' + now_format + str(uuidName)

    fullPathDirName = os.path.join(AbaqusDir, dirName)

    dictParam['workDir'] = fullPathDirName

    os.mkdir(fullPathDirName)

    CowList = ['PKGAuto.py', 'CoW_Warpage.py', 'Extract_Output_CoW_Warpage.py', 'Mat_Prop.inp', 'HBM_Warp.dat', 'c2.inp']
    for file in CowList:
        print(file)
        shutil.copyfile(file, os.path.join(fullPathDirName, file))
    updateParameters(dictParam, matrixParam, currentDir)

    return fullPathDirName



def runSimLab(workDir):

    os.chdir(workDir)
    cmdSimLab = r'D:\Altair\2022.3\SimLab\bin\win64\SimLab.bat -auto CoW_Warpage.py -nographics'
    subprocess.run(cmdSimLab, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    # p.wait()

def runAbaqus(dictParam, matrixParam, workDir, currentDir):
    abqlicInfo = 'abq_info.txt'
    cmdAbqLic = r'D:\SIMULIA\Commands\abaqus.bat licensing dslsStat -a > %s' % abqlicInfo
    p = subprocess.Popen(cmdAbqLic, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()

    f = open(abqlicInfo, 'r')
    lines = f.readlines()
    f.close()

    for line in lines:
        if line.startswith('| QXT') > 0:
            tokens = line.strip().split()
            totalLicense = int(tokens[12])
            inUseLicense = int(tokens[14])
            availableLicense = totalLicense - inUseLicense
            print(availableLicense)
            if availableLicense >= 80:
                infoAbaqusLic = 'There is enough Abaqus license(%s tokens). so Execute to Simulation' % availableLicense
                dictParam['infoAbaqusLic'] = infoAbaqusLic
                os.chdir(workDir)
                os.remove('HBM_Warp.dat')
                cmdAbaqus = r'D:\SIMULIA\Commands\abaqus.bat job=HBM_Warp.inp cpus=4 int'
                p = subprocess.Popen(cmdAbaqus, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                p.wait()

            else:
                infoAbaqusLic = 'There is not enough Abaqus license(%s tokens). so EXIT to Simulation' % availableLicense
                dictParam['infoAbaqusLic'] = infoAbaqusLic
                pass
    updateParameters(dictParam, matrixParam, currentDir)

def getResults(dictParam, matrixParam, workDir, currentDir):
    os.chdir(workDir)
    cmdPostProgram = r'C://ProgramData//aipforge//python.exe Extract_Output_CoW_Warpage.py'
    p = subprocess.Popen(cmdPostProgram, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()

    fileName = 'Output.txt'

    f = open(fileName, 'r')
    lines = f.readlines()
    f.close()

    dictParam['output'] = lines[0]


    updateParameters(dictParam, matrixParam, currentDir)

def makeAbqInputFiles(dictParam, matrixParam, workDir, currentDir):
    simlablicInfo = 'sim_info.txt'
    cmdSimlabLic = r'D:\Altair\2022.3\security\bin\win64\almutil.exe -licstatxml -feature GlobalZoneAP -totals > %s' % simlablicInfo
    p = subprocess.Popen(cmdSimlabLic, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()

    f = open(simlablicInfo, 'r', encoding='UTF-8')
    lines = f.readlines()
    f.close()

    for line in lines:
        if line.startswith('      <FEATURE NAME') > 0:
            tokens = line.strip().split()
            totalLicense = int(tokens[5].strip().split('=')[1].replace('"', ''))
            inUseLicense = int(tokens[4].strip().split('=')[1].replace('"', ''))

            availableLicense = totalLicense - inUseLicense
            print(availableLicense)
            if availableLicense >= 21000:
                infoSimlabLic = 'There is enough SimLab license(%s). so Execute to Simulation' % availableLicense
                dictParam['infoSimlabLic'] = infoSimlabLic
                runSimLab(workDir)
            else:
                infoSimlabLic = 'There is not enough SimLab license(%s). so EXIT to Simulation'% availableLicense
                dictParam['infoSimlabLic'] = infoSimlabLic
                sys.exit()
    updateParameters(dictParam, matrixParam, currentDir)

def main():
    currentDir = os.getcwd()
    dictParam, matrixParam = readActivityParam()
    workDir = dictParam.get('workDir')

    if len(workDir) == 0:
        print('SimLab Macro file is now creating.!!!')
        makeInputFile(dictParam, matrixParam)
        workDir = copyModels(dictParam, matrixParam, currentDir)
        print(workDir)
        print('Abaqus Input file is now creating.!!!')
        makeAbqInputFiles(dictParam, matrixParam, workDir, currentDir)
        runAbaqus(dictParam, matrixParam, workDir, currentDir)
        getResults(dictParam, matrixParam, workDir, currentDir)

    else:
        os.chdir(workDir)
        if not os.path.exists('HBM_TCB_Wafer.slb') is True:
            makeAbqInputFiles(dictParam, matrixParam, workDir, currentDir)
            runAbaqus(dictParam, matrixParam, workDir, currentDir)
            getResults(dictParam, matrixParam, workDir, currentDir)
    #
        elif not os.path.exists('HBM_Warp.odb') is True:
            runAbaqus(dictParam, matrixParam, workDir, currentDir)
            getResults(dictParam, matrixParam, workDir, currentDir)

if __name__ == '__main__':
    main()

