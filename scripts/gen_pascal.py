""" SoLoud Pascal wrapper generator """

import soloud_codegen

fo = open("../glue/soloud.pas", "w")


C_TO_PAS_TYPES = {
    "int":"integer",
    "void":"void",
    "const char *":"PAnsiChar",  # add extra const check on key? it's not that important
    "char *":"PAnsiChar",
    "unsigned int":"longword",
    "float":"single",
    "double":"double",
    "float *":"PSingle",
    "File *":"TSoloudObject",
    "unsigned char *":"PByte",
    "unsigned char":"byte",
    "short *":"PUint16"
}

for soloud_type in soloud_codegen.soloud_type:
    C_TO_PAS_TYPES[soloud_type + " *"] = "T" + soloud_type

fo.write("""
// SoLoud wrapper for Pascal
// This file is autogenerated; any changes will be overwritten

unit soloud;
{$PACKRECORDS C}
{$mode objfpc}

interface

const
{$IFDEF CPU64} SoLoudLibName = 'soloud_x64.dll'; {$endif}
{$IFDEF CPU86} SoLoudLibName = 'soloud_x32.dll'; {$endif}  

""")

fo.write("// Types\n")
fo.write("type\n")
for soloud_type in soloud_codegen.soloud_type:
    fo.write("  T" + soloud_type + " = Pointer;\n")
fo.write("  TSoloudObject = Pointer;\n")
fo.write("\n")

fo.write("// Enumerations\n")
fo.write("const\n")
for x in soloud_codegen.soloud_enum:
    fo.write('  ' + x + ' = ' + str(soloud_codegen.soloud_enum[x]) + ";\n")
fo.write("\n")

function_decls = ""

for x in soloud_codegen.soloud_type:
    add_type_separator = False
    for y in soloud_codegen.soloud_func:
        if (x + "_") == y[1][0:len(x)+1:]:
            ret = C_TO_PAS_TYPES[y[0]]
            current_decl = 'function  '
            if ret == 'void':
                current_decl = 'procedure '
            current_decl += y[1] + '('
            for z in y[2]:
                if len(z) > 1:
                    if z[1] == 'a'+x:
                        pass
                    else:
                        current_decl += '; '
                    current_decl += z[1] + ': ' + C_TO_PAS_TYPES[z[0]]
            current_decl += ')'
            if ret != 'void':
                current_decl += ': ' + ret
            function_decls += current_decl + '; cdecl; external SoLoudLibName;\n'
            add_type_separator = True
    
    if add_type_separator:
        function_decls += "\n"
    
fo.write(function_decls)
fo.write("""
implementation
end.
""")
fo.close()

print ("soloud.pas generated")
