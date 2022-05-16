import re

t = '<span>显示： 1-48条， 共250条</span><span> </span><span class="a-color-state a-text-bold">&quot;个护电器&quot;</span>'
_text = re.search('超过(\d+,\d+|\d+)个|超过(\d+,\d+|\d+)条|共(\d+,\d+|\d+)个|共(\d+,\d+|\d+)条', str(t), re.S).group(0)

print(_text)