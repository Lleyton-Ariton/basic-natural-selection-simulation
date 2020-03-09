import os, sys
import panda3d

dir = os.path.dirname(panda3d.__file__)
del panda3d

if sys.platform in ('win32', 'cygwin'):
    path_var = 'PATH'
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(dir)
elif sys.platform == 'darwin':
    path_var = 'DYLD_LIBRARY_PATH'
else:
    path_var = 'LD_LIBRARY_PATH'

if not os.environ.get(path_var):
    os.environ[path_var] = dir
else:
    os.environ[path_var] = dir + os.pathsep + os.environ[path_var]

del os, sys, path_var, dir


def _exec_tool(tool):
    import os, sys
    from subprocess import Popen
    tools_dir = os.path.dirname(__file__)
    handle = Popen(sys.argv, executable=os.path.join(tools_dir, tool))
    try:
        try:
            return handle.wait()
        except KeyboardInterrupt:
            # Give the program a chance to handle the signal gracefully.
            return handle.wait()
    except:
        handle.kill()
        handle.wait()
        raise

# Register all the executables in this directory as global functions.
pzip = lambda: _exec_tool('pzip')
interrogate = lambda: _exec_tool('interrogate')
egg2flt = lambda: _exec_tool('egg2flt')
egg_retarget_anim = lambda: _exec_tool('egg-retarget-anim')
egg2c = lambda: _exec_tool('egg2c')
flt_info = lambda: _exec_tool('flt-info')
egg2x = lambda: _exec_tool('egg2x')
pview = lambda: _exec_tool('pview')
mayacopy2018 = lambda: _exec_tool('mayacopy2018')
mayacopy2020 = lambda: _exec_tool('mayacopy2020')
obj2egg = lambda: _exec_tool('obj2egg')
image_resize = lambda: _exec_tool('image-resize')
mayacopy2016 = lambda: _exec_tool('mayacopy2016')
mayacopy2011 = lambda: _exec_tool('mayacopy2011')
egg2dxf = lambda: _exec_tool('egg2dxf')
build_patch = lambda: _exec_tool('build_patch')
mayacopy2017 = lambda: _exec_tool('mayacopy2017')
egg_rename = lambda: _exec_tool('egg-rename')
punzip = lambda: _exec_tool('punzip')
text_stats = lambda: _exec_tool('text-stats')
x2egg = lambda: _exec_tool('x2egg')
egg2maya2012 = lambda: _exec_tool('egg2maya2012')
egg2maya2015 = lambda: _exec_tool('egg2maya2015')
test_interrogate = lambda: _exec_tool('test_interrogate')
fltcopy = lambda: _exec_tool('fltcopy')
maya2egg2011 = lambda: _exec_tool('maya2egg2011')
maya2egg2016 = lambda: _exec_tool('maya2egg2016')
egg_palettize = lambda: _exec_tool('egg-palettize')
p3dcparse = lambda: _exec_tool('p3dcparse')
maya2egg2020 = lambda: _exec_tool('maya2egg2020')
maya2egg2018 = lambda: _exec_tool('maya2egg2018')
egg2maya2014 = lambda: _exec_tool('egg2maya2014')
egg2maya20165 = lambda: _exec_tool('egg2maya20165')
egg2maya2013 = lambda: _exec_tool('egg2maya2013')
lwo2egg = lambda: _exec_tool('lwo2egg')
bam2egg = lambda: _exec_tool('bam2egg')
x_trans = lambda: _exec_tool('x-trans')
maya2egg2017 = lambda: _exec_tool('maya2egg2017')
lwo_scan = lambda: _exec_tool('lwo-scan')
mayacopy20165 = lambda: _exec_tool('mayacopy20165')
vrml_trans = lambda: _exec_tool('vrml-trans')
egg_topstrip = lambda: _exec_tool('egg-topstrip')
egg_list_textures = lambda: _exec_tool('egg-list-textures')
interrogate_module = lambda: _exec_tool('interrogate_module')
deploy_stub = lambda: _exec_tool('deploy-stub')
flt_trans = lambda: _exec_tool('flt-trans')
egg_mkfont = lambda: _exec_tool('egg-mkfont')
egg_crop = lambda: _exec_tool('egg-crop')
egg_qtess = lambda: _exec_tool('egg-qtess')
multify = lambda: _exec_tool('multify')
pfm_trans = lambda: _exec_tool('pfm-trans')
pfm_bba = lambda: _exec_tool('pfm-bba')
dxf_points = lambda: _exec_tool('dxf-points')
maya2egg20165 = lambda: _exec_tool('maya2egg20165')
check_md5 = lambda: _exec_tool('check_md5')
show_ddb = lambda: _exec_tool('show_ddb')
egg2obj = lambda: _exec_tool('egg2obj')
flt2egg = lambda: _exec_tool('flt2egg')
mayacopy2012 = lambda: _exec_tool('mayacopy2012')
mayacopy2015 = lambda: _exec_tool('mayacopy2015')
vrml2egg = lambda: _exec_tool('vrml2egg')
dxf2egg = lambda: _exec_tool('dxf2egg')
mayacopy2014 = lambda: _exec_tool('mayacopy2014')
mayacopy2013 = lambda: _exec_tool('mayacopy2013')
check_adler = lambda: _exec_tool('check_adler')
dae2egg = lambda: _exec_tool('dae2egg')
maya2egg2015 = lambda: _exec_tool('maya2egg2015')
maya2egg2012 = lambda: _exec_tool('maya2egg2012')
pdecrypt = lambda: _exec_tool('pdecrypt')
egg2maya2018 = lambda: _exec_tool('egg2maya2018')
egg2maya2020 = lambda: _exec_tool('egg2maya2020')
egg2maya2016 = lambda: _exec_tool('egg2maya2016')
bam_info = lambda: _exec_tool('bam-info')
egg2maya2011 = lambda: _exec_tool('egg2maya2011')
egg_texture_cards = lambda: _exec_tool('egg-texture-cards')
maya2egg2013 = lambda: _exec_tool('maya2egg2013')
egg_trans = lambda: _exec_tool('egg-trans')
check_crc = lambda: _exec_tool('check_crc')
maya2egg2014 = lambda: _exec_tool('maya2egg2014')
egg2maya2017 = lambda: _exec_tool('egg2maya2017')
egg2bam = lambda: _exec_tool('egg2bam')
pencrypt = lambda: _exec_tool('pencrypt')
image_info = lambda: _exec_tool('image-info')
make_prc_key = lambda: _exec_tool('make-prc-key')
image_trans = lambda: _exec_tool('image-trans')
apply_patch = lambda: _exec_tool('apply_patch')
parse_file = lambda: _exec_tool('parse_file')
deploy_stubw = lambda: _exec_tool('deploy-stubw')
egg_optchar = lambda: _exec_tool('egg-optchar')
egg_make_tube = lambda: _exec_tool('egg-make-tube')

