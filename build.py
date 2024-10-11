#该脚本在 Windows 下编译通过， Linux 与 MacOS 平台暂未测试。

import PyInstaller.__main__
import os
import site

# 获取 site-packages 目录列表
site_packages_paths = site.getsitepackages()

# 查找包含 maa/bin 的路径
maa_bin_path = None
for path in site_packages_paths:
    potential_path = os.path.join(path, 'maa', 'bin')
    if os.path.exists(potential_path):
        maa_bin_path = potential_path
        break

if maa_bin_path is None:
    raise FileNotFoundError("未找到包含 maa/bin 的路径")
# 构建 --add-data 参数
add_data_param = f'{maa_bin_path}{os.pathsep}maa/bin'

# 查找包含 MaaAgentBinary 的路径
maa_bin_path2 = None
for path in site_packages_paths:
    potential_path = os.path.join(path, 'MaaAgentBinary')
    if os.path.exists(potential_path):
        maa_bin_path2 = potential_path
        break

if maa_bin_path2 is None:
    raise FileNotFoundError("未找到包含 MaaAgentBinary 的路径")
# 构建 --add-data 参数
add_data_param2 = f'{maa_bin_path2}{os.pathsep}MaaAgentBinary'

    
# 查找包含 Plyer 的路径
plyer_path = None
for path in site_packages_paths:
    potential_path = os.path.join(path, 'plyer')
    if os.path.exists(potential_path):
        plyer_path = potential_path
        break
    
if plyer_path is None:
    raise FileNotFoundError("未找到包含 Plyer 的路径")
# 构建 --add-data 参数
add_data_param3 = f'{plyer_path}{os.pathsep}plyer'


# 运行 PyInstaller
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--name=IdentityV-Tool',
    f'--add-data={add_data_param}',
    f'--add-data={add_data_param2}',
    f'--add-data={add_data_param3}',
    '--hidden-import=plyer.platforms.win.notification', #处理 Plyer 在 Windows 平台的实现
    '--clean'
    #'--uac-admin' #为应用申请管理员权限，因主分支迁移至 Android 模拟器，现废弃
])