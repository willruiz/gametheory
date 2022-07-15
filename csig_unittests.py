import numpy as np
import sys
import csig_gui     as cg
import csig_btn     as cb
import csig_logic   as cl
import csig_def     as cd
import csig_np     as cn
import signal_game  as sig

latest_testchar = "E"

def testA_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    
    incr = 0
    for i, i_entry in enumerate(test_matrix):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): 
                test_matrix[i][j][k] = incr
                incr = incr + 1
    cn.fill_nature_half(test_matrix_nature)
    cn.import_matrix(parent_in, test_matrix, test_matrix_nature)
    cn.save_test_matrix(parent_in, test_name)

def testB_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    incr = 0
    for i, i_entry in enumerate(test_matrix):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): 
                test_matrix[i][j][k] = incr
                incr = incr + 1
    test_matrix = test_matrix[::-1]
    cn.fill_nature_half(test_matrix_nature)
    cn.import_matrix(parent_in, test_matrix, test_matrix_nature)
    cn.save_test_matrix(parent_in, test_name)

def testC_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    incr = 16
    for i, i_entry in enumerate(test_matrix):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): 
                test_matrix[i][j][k] = incr
                incr = incr - 1
    cn.fill_nature_half(test_matrix_nature)
    cn.import_matrix(parent_in, test_matrix, test_matrix_nature)
    cn.save_test_matrix(parent_in, test_name)

def testC_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    incr = 16
    for i, i_entry in enumerate(test_matrix):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry):
                test_matrix[i][j][k] = incr
                incr = incr - 1
    cn.fill_nature_half(test_matrix_nature)
    cn.import_matrix(parent_in, test_matrix, test_matrix_nature)
    cn.save_test_matrix(parent_in, test_name)
    
# All zeros
def testD_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    cn.fill_nature_half(test_matrix_nature)
    cn.import_matrix(parent_in, test_matrix, test_matrix_nature)
    cn.save_test_matrix(parent_in, test_name)

# Pooling SEPR_A
def testE_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    test_matrix = np.array([
            [(15,  4),(30, 11)],
            [(25, 89),( 0,  3)],
            [(10,  2),(17,  0)],
            [( 8,  5),( 9,  4)]
            ])
    cn.fill_nature_half(test_matrix_nature)
    cn.import_matrix(parent_in, test_matrix, test_matrix_nature)
    cn.save_test_matrix(parent_in, test_name)
    return test_matrix, test_matrix_nature

def testF_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    pass
    # test_matrix = np.array([
    #     [(52, 46) ( 1, 52)]
    #     [(94, 92) (96, 48)]
    #     [(52, 74) (97, 33)]
    #     [(69, 43) (73,  0)]
    #     ])
    # test_matrix_nature = np.array([
    #     [0.84,0.16]
    #     ])
    # return test_matrix, test_matrix_nature
    

def testG_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    pass

# Generates a signal game matrixes with payoffs in ascending order (1,2,3,4...)
# Runs a basic p2_choice and p1_deviations checks. 
def testA(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == False)

    print("[TestA-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice   == 1)
    assert(parent_in.p2_bot_choice   == 1)
    assert(parent_in.p2_pool_act_alt == 1)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == False)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice   == 1)
    assert(parent_in.p2_bot_choice   == 1)
    assert(parent_in.p2_pool_act_alt == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    print("[TestA-pool]: PASS")

def testB(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == False)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    print("[TestB-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice   == 1)
    assert(parent_in.p2_bot_choice   == 1)
    assert(parent_in.p2_pool_act_alt == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice   == 1)
    assert(parent_in.p2_bot_choice   == 1)
    assert(parent_in.p2_pool_act_alt == 1)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == False)

    print("[TestB-pool]: PASS")

def testC(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == False)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    print("[TestC-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice   == 0)
    assert(parent_in.p2_bot_choice   == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice   == 0)
    assert(parent_in.p2_bot_choice   == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == False)

    print("[TestC-pool]: PASS")

def testD(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)

    print("[TestD-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice   == 0)
    assert(parent_in.p2_bot_choice   == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == False)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice   == 0)
    assert(parent_in.p2_bot_choice   == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == False)

    print("[TestD-pool]: PASS")

def testE(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    print("[TestE-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice   == 0)
    assert(parent_in.p2_bot_choice   == 0)
    assert(parent_in.p2_pool_act_alt == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice   == 1)
    assert(parent_in.p2_bot_choice   == 1)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == True)

    print("[TestE-pool]: PASS")



def testF(parent_in, test_matrix, test_nature):
    pass
def testG(parent_in, test_matrix, test_nature):
    pass



test_functor_list = [testA, testB, testC, 
        testD, testE, testF, testG]
testGEN_functor_list = [testA_gen, testB_gen, testC_gen, 
        testD_gen, testE_gen, testF_gen, testG_gen]

def gen_test_matricies_file(parent_in, tests_in):
    for i, test in enumerate(tests_in):
        test_name = "test" + test
        print("Gen"+test)
        test_matrix = np.zeros((4,2), dtype='i,i')
        test_matrix_nature = np.zeros((1,2))
        testGEN_functor_list[i](parent_in, test_name, test_matrix, test_matrix_nature)
        # tmtrx_out, tnatr_out = testGEN_functor_list[i](parent_in, test_name, test_matrix, test_matrix_nature)
        # cn.import_matrix(parent_in, tmtrx_out, tnatr_out)
        # cn.save_test_matrix(parent_in, test_name)