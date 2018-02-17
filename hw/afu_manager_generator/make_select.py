from math import ceil
from veriloggen import *


def make_select(num_input):
    m = Module('select_%d' % num_input)
    DATA_WIDTH = m.Parameter('DATA_WIDTH', 32)
    clk = m.Input('clk')
    rst = m.Input('rst')
    data_in_valid = m.Input('data_in_valid', num_input)
    inputs = []
    for i in range(num_input):
        inputs.append(m.Input('data_in_%d' % i, DATA_WIDTH))

    data_out = m.OutputReg('data_out', DATA_WIDTH)
    data_out_valid = m.OutputReg('data_out_valid')
    id = 1
    code = 'case(data_in_valid)\n'
    for i in range(num_input):
        code = code + '     %d: data_out <= data_in_%d;\n' % (id, i)
        id = id * 2
    code = code + '     default:data_out <= 0;\nendcase'
    m.Always(Posedge(clk))(
        If(rst)(
            data_out(0)
        ).Else(
            EmbeddedCode(code)
        )
    )
    m.Always(Posedge(clk))(
        If(rst)(
            data_out_valid(0)
        ).Else(
            data_out_valid(EmbeddedCode('|data_in_valid'))
        )
    )
    return m


def make_select_tree_array(num_input, array):
    m_array = []
    while num_input > 8:
        m_array.append(8)
        num_input = num_input - 8
    else:
        m_array.append(num_input)

    array.append(m_array)
    if len(m_array) == 1:
        return array
    else:
        return make_select_tree_array(len(m_array), array)


def make_select_tree(num_input):
    array = []
    array = make_select_tree_array(num_input, array)
    m = Module('select_ff')
    DATA_WIDTH = m.Parameter('DATA_WIDTH', 32)
    clk = m.Input('clk')
    rst = m.Input('rst')
    data_in_valid = m.Input('data_in_valid', num_input)
    inputs = {}
    for i in range(num_input):
        name = 'data_in_%d' % i
        inputs[name] = m.Input(name, DATA_WIDTH)

    data_out = m.Output('data_out', DATA_WIDTH)
    data_out_valid = m.Output('data_out_valid')

    data_out_wires = {}
    data_out_valid_wires = {}

    for i in range(len(array) - 1):
        data_out_valid_wires[i] = m.Wire('data_out_valid_wires_%d' % i, len(array[i]))

    for i in range(len(array) - 1):
        data_out_wires[i] = m.Wire('data_out_wire_%d' % i, DATA_WIDTH, len(array[i]))
    mods = {}
    if len(array) == 1:
        sel_level = array[0]
        con = [('clk', clk), ('rst', rst), ('data_in_valid', data_in_valid)]
        cc = 0
        for p in range(sel_level[0]):
            con.append(('data_in_%d' % p, inputs['data_in_%d' % cc]))
            cc += 1
        con.append(('data_out_valid', data_out_valid))
        con.append(('data_out', data_out))
        if not sel_level[0] in mods.keys():
            mods[sel_level[0]] = make_select(sel_level[0])
        sel = mods[sel_level[0]]
        m.Instance(sel, 'sel_%d_%d' % (0, 0), m.get_params(), con)

    else:
        for i in range(len(array) - 1):
            cc = 0
            sel_idx = 0
            sel_level = array[i]
            for j in range(len(sel_level)):
                if i == 0:
                    con = [('clk', clk), ('rst', rst), ('data_in_valid', data_in_valid[cc:cc + sel_level[j]])]
                    for p in range(sel_level[j]):
                        con.append(('data_in_%d' % p, inputs['data_in_%d' % cc]))
                        cc += 1
                else:
                    con = [('clk', clk), ('rst', rst), ('data_in_valid',data_out_valid_wires[i-1][cc:cc + sel_level[j]])]
                    for p in range(sel_level[j]):
                        con.append(('data_in_%d' % p, data_out_wires[i-1][cc]))
                        cc += 1
                con.append(('data_out_valid', data_out_valid_wires[i][sel_idx]))
                con.append(('data_out', data_out_wires[i][sel_idx]))
                if not sel_level[j] in mods.keys():
                    mods[sel_level[j]] = make_select(sel_level[j])
                sel = mods[sel_level[j]]
                m.Instance(sel, 'sel_%d_%d' % (i, sel_idx), m.get_params(), con)
                sel_idx += 1

        con = [('clk', clk), ('rst', rst), ('data_in_valid', data_out_valid_wires[len(array) - 2])]
        for u in range(array[len(array) - 1][0]):
            con.append(('data_in_%d' % u, data_out_wires[len(array) - 2][u]))
        con.append(('data_out_valid', data_out_valid))
        con.append(('data_out', data_out))
        if not array[len(array) - 1][0] in mods.keys():
            mods[array[len(array) - 1][0]] = make_select(array[len(array) - 1][0])
        sel = mods[array[len(array) - 1][0]]
        m.Instance(sel, 'sel_%d_%d' % (len(array) - 1, 0), m.get_params(), con)

    return m
