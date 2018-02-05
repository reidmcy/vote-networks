import re

def latexPostProcessing(s, add_midrule = False):
    splitLines = s.split('\n')
    retS = '\n'.join(splitLines[:4])
    retLines = []
    for line in splitLines[4:-2]:
        retLines.append(re.sub(r'(^|\s|-)\d+\.?\d*', lambda x : "\\num{{{}}}".format(x.group(0).strip()), line))
    if add_midrule:
        retLines.insert(-2, '\\midrule')
    retS += '\n' + '\n'.join(retLines)
    return retS + '\n' + '\n'.join(splitLines[-2:])

def makeTable(df, caption = '', label = 't1', add_midrule = False):
    print("\\begin{table}[h]")
    print("     \centering")
    print("     \\begin{adjustbox}{center}")
    print(latexPostProcessing(df.to_latex(), add_midrule = add_midrule).strip())
    print("     \\end{adjustbox}")
    print("     \caption{{{}}}\label{{{}}}".format(caption, label))
    print("\end{table}")